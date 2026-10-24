#!/usr/bin/env python3
"""Validate the Triodian Metamodel schemas.

Checks, in order:
  1. Every file under schemas/ is well-formed JSON.
  2. Every schema declares a supported $schema and is valid against that meta-schema.
  3. No non-standard structural keywords ("attributes"/"elements" used in place of
     "properties"/"definitions", or OpenAPI-style "nullable"), and every object that
     defines properties rejects fields it does not define (additionalProperties: false).
  4. Every schema has the same structure: JSON Schema draft-07; the root of each domain schema
     is the domain's main record (no wrapper properties, no oneOf); element types are named
     under "definitions"; definition and property names are camelCase; passive domains
     (as listed in cross-domain-relationship.schema.json) do not initiate relationships.
  5. Every $ref resolves, whether local (#/...) or to another schema file.
  6. Every record type requires an identifier (a property named "<entity>ID" or "id").
  7. Every example embedded in a schema's top-level "examples" validates against that schema.
  8. (--doc-examples) Every worked example from the documentation, listed in
     examples/doc-examples/manifest.json, validates against its schema.

Exit status is non-zero if any check that was run fails.

Usage:
  python scripts/validate.py                 # checks 1-7
  python scripts/validate.py --doc-examples  # checks 1-8
  python scripts/validate.py --only-doc-examples
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urldefrag, urljoin

from jsonschema import Draft7Validator, Draft202012Validator
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"
DOC_EXAMPLES = ROOT / "examples" / "doc-examples"
BASE_URI = "https://triodian.com/schemas/"

DRAFT = "http://json-schema.org/draft-07/schema#"
VALIDATORS = {
    DRAFT: Draft7Validator,
    "http://json-schema.org/draft-07/schema": Draft7Validator,
    "https://json-schema.org/draft/2020-12/schema": Draft202012Validator,
}
NON_STANDARD = {"attributes", "elements", "nullable"}
CAMEL = re.compile(r"[a-z][a-zA-Z0-9]*")
# Schema file for each domain value that can appear in a relationship.
DOMAIN_FILES = {"information": "information.schema.json", "performance": "performance.schema.json",
                "product": "products.schema.json", "service": "services.schema.json"}
# Schemas that are not a domain record of their own.
NOT_RECORDS = {
    # shared vocabulary
    "common.schema.json",
    # composites that group records defined in other schemas
    "external-organizations-composite.schema.json",
    "strategic-response-model.schema.json",
    "extensions/business-analysis.json",
    # extension describing an aspect of a Technology record
    "extensions/technology/TechnologyOneWellArchitectedFrameworkExtension",
}

failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"  FAIL  {msg}")


def schema_files() -> list[Path]:
    return sorted(p for p in SCHEMA_DIR.rglob("*") if p.is_file())


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def walk(node, path=()):
    """Yield (json_path, dict) for every object in a JSON document."""
    if isinstance(node, dict):
        yield path, node
        for k, v in node.items():
            yield from walk(v, path + (k,))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, path + (i,))


def is_schema_object(node: dict) -> bool:
    return any(k in node for k in ("type", "properties", "$ref", "enum", "items", "$schema"))


def check_parse(files: list[Path]) -> dict[Path, dict]:
    print("1. Files are well-formed JSON")
    docs = {}
    for f in files:
        try:
            docs[f] = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(f"{rel(f)}: {e}")
    return docs


def check_meta(docs: dict[Path, dict]) -> None:
    print("2. Schemas are valid against their declared meta-schema")
    for f, d in docs.items():
        cls = VALIDATORS.get(d.get("$schema"))
        if cls is None:
            fail(f"{rel(f)}: unsupported or missing $schema {d.get('$schema')!r}")
            continue
        for err in cls(cls.META_SCHEMA).iter_errors(d):
            fail(f"{rel(f)}: {'/'.join(map(str, err.absolute_path)) or '<root>'}: {err.message[:160]}")


def check_keywords(docs: dict[Path, dict]) -> None:
    print("3. No non-standard keywords, and objects reject undefined fields")
    for f, d in docs.items():
        for path, node in walk(d):
            # Skip the contents of property maps, where any key is a legitimate field name.
            if path and path[-1] in ("properties", "definitions", "$defs", "examples"):
                continue
            if any(p == "examples" for p in path):
                continue
            if not is_schema_object(node):
                continue
            for kw in NON_STANDARD & node.keys():
                fail(f"{rel(f)}: /{'/'.join(map(str, path))}: non-standard keyword {kw!r}")
            if isinstance(node.get("properties"), dict) and "additionalProperties" not in node \
                    and "patternProperties" not in node:
                fail(f"{rel(f)}: /{'/'.join(map(str, path))}: accepts undefined fields "
                     "(add \"additionalProperties\": false)")


def is_identifier(name: str) -> bool:
    return name == "id" or name.endswith("ID")


def is_record_schema(f: Path) -> bool:
    return f.relative_to(SCHEMA_DIR).as_posix() not in NOT_RECORDS


def record_schemas(f: Path, d: dict):
    """Yield (label, schema) for the record type a domain schema describes: its root."""
    if is_record_schema(f):
        yield rel(f), d


def check_structure(docs: dict[Path, dict]) -> None:
    print("4. Every schema has the same structure")
    for f, d in docs.items():
        if d.get("$schema") != DRAFT:
            fail(f"{rel(f)}: uses {d.get('$schema')!r}; all schemas use {DRAFT}")
        for path, node in walk(d):
            if "examples" in path:
                continue
            here = "/" + "/".join(map(str, path))
            if "$defs" in node and not (path and path[-1] == "properties"):
                fail(f"{rel(f)}: {here}: use \"definitions\", not \"$defs\"")
            if path and path[-1] == "properties" and isinstance(node, dict):
                for k in node:
                    if not CAMEL.fullmatch(k):
                        fail(f"{rel(f)}: {here}: property name {k!r} is not camelCase")
        for k in d.get("definitions", {}):
            if not CAMEL.fullmatch(k):
                fail(f"{rel(f)}: definition name {k!r} is not camelCase")
        if not is_record_schema(f):
            continue
        props = d.get("properties")
        if d.get("type") != "object" or not isinstance(props, dict) or not props:
            fail(f"{rel(f)}: root must be the domain's main record (an object with properties)")
            continue
        for kw in ("oneOf", "anyOf", "allOf"):
            if kw in d:
                fail(f"{rel(f)}: root uses {kw}; put each record type in its own schema or under definitions")
        if all(isinstance(v, dict) and v.get("type") == "object" and "properties" in v for v in props.values()):
            fail(f"{rel(f)}: root wraps its record in {list(props)}; make the record the root")
    xdr = SCHEMA_DIR / "cross-domain-relationship.schema.json"
    if xdr in docs:
        source = docs[xdr]["properties"]["sourceDomain"]
        passive = next((b["not"]["enum"] for b in source.get("allOf", []) if "not" in b), [])
        for domain in passive:
            f = SCHEMA_DIR / DOMAIN_FILES.get(domain, "")
            if f in docs and "crossDomainRelationships" in docs[f].get("properties", {}):
                fail(f"{rel(f)}: {domain} is a passive domain and must not initiate relationships "
                     "(remove crossDomainRelationships; model them from the initiating domain)")


def check_identifiers(docs: dict[Path, dict]) -> None:
    print("6. Every record type requires an identifier")
    for f, d in docs.items():
        for label, schema in record_schemas(f, d):
            required = [r for r in schema.get("required", []) if is_identifier(r)]
            if not required:
                own = [k for k in schema.get("properties", {}) if is_identifier(k)]
                hint = f" ({own[0]} exists but is not required)" if own else ""
                fail(f"{label}: no required identifier{hint}")


def build_registry(docs: dict[Path, dict]) -> tuple[Registry, dict[Path, str]]:
    registry = Registry()
    uris = {}
    for f, d in docs.items():
        if d.get("$schema") not in VALIDATORS:
            continue
        res = Resource.from_contents(d)
        canonical = BASE_URI + f.relative_to(SCHEMA_DIR).as_posix()
        aliases = {canonical, f.as_uri()}
        if "$id" in d:
            aliases.add(d["$id"])
        for uri in aliases:
            registry = registry.with_resource(uri, res)
        uris[f] = d.get("$id", canonical)
    return registry.crawl(), uris


def check_refs(docs, registry, uris) -> None:
    print("5. Every $ref resolves")
    for f, d in docs.items():
        if f not in uris:
            continue
        base = uris[f]
        for path, node in walk(d):
            ref = node.get("$ref")
            if not isinstance(ref, str):
                continue
            target = urljoin(base, ref)
            uri, fragment = urldefrag(target)
            try:
                resolver = registry.resolver(base_uri=base)
                resolver.lookup(ref)
            except Unresolvable:
                fail(f"{rel(f)}: /{'/'.join(map(str, path))}: $ref {ref!r} does not resolve")


def validate_instance(schema_doc: dict, uri: str, pointer: str, instance, registry) -> list[str]:
    cls = VALIDATORS[schema_doc["$schema"]]
    # Always validate through the registered URI so relative $refs (e.g. common.schema.json) resolve.
    schema = {"$ref": uri + pointer}
    validator = cls(schema, registry=registry)
    errs = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
    return [f"/{'/'.join(map(str, e.absolute_path))}: {e.message[:200]}" for e in errs]


def check_embedded_examples(docs, registry, uris) -> None:
    print("7. Embedded schema examples validate")
    for f, d in docs.items():
        if f not in uris or d.get("type") != "object":
            continue
        for i, ex in enumerate(d.get("examples") or []):
            if not isinstance(ex, dict):
                continue
            for msg in validate_instance(d, uris[f], "", ex, registry):
                fail(f"{rel(f)} example[{i}]{msg}")


def check_doc_examples(docs, registry, uris) -> None:
    print("8. Documentation worked examples validate")
    manifest = json.loads((DOC_EXAMPLES / "manifest.json").read_text(encoding="utf-8"))
    passed = 0
    for entry in manifest["examples"]:
        schema_path = SCHEMA_DIR / entry["schema"]
        if schema_path not in uris:
            fail(f"{entry['instance']}: schema {entry['schema']} not loadable")
            continue
        instance = json.loads((DOC_EXAMPLES / entry["instance"]).read_text(encoding="utf-8"))
        errs = validate_instance(docs[schema_path], uris[schema_path], entry.get("pointer", ""), instance, registry)
        if errs:
            fail(f"{entry['instance']} -> {entry['schema']}{entry.get('pointer', '')} ({len(errs)} error(s))")
            for e in errs[:5]:
                print(f"          {e}")
            if len(errs) > 5:
                print(f"          ... {len(errs) - 5} more")
        else:
            passed += 1
    print(f"  {passed}/{len(manifest['examples'])} documentation examples pass")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--doc-examples", action="store_true", help="also validate the documentation's worked examples")
    ap.add_argument("--only-doc-examples", action="store_true", help="validate only the documentation's worked examples")
    args = ap.parse_args()

    files = schema_files()
    docs = check_parse(files)
    registry, uris = build_registry(docs)
    if args.only_doc_examples:
        failures.clear()
        check_doc_examples(docs, registry, uris)
    else:
        check_meta(docs)
        check_keywords(docs)
        check_structure(docs)
        check_refs(docs, registry, uris)
        check_identifiers(docs)
        check_embedded_examples(docs, registry, uris)
        if args.doc_examples:
            check_doc_examples(docs, registry, uris)

    print(f"\n{len(failures)} failure(s) across {len(files)} schema files")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
