#!/usr/bin/env python3
"""Validate the exchange formats in exchange/.

The exchange schemas describe the files the Triodian apps write for each other (calibration set, board directions,
register extract, board view, confidentiality position, matter brief). They keep the field names the apps already
use, so they sit outside schemas/ and its domain naming rules. Checks:

  1. Every exchange schema is valid JSON Schema draft-07, has a title and description, and its $id is its location
     under https://triodian.com/exchange/.
  2. Every $ref resolves.
  3. Every example in exchange/examples/ validates against the schema its file name starts with
     (calibration-set-v1.worked-example.json -> calibration-set-v1.schema.json).
  4. Every schema has at least one example.

Usage: python scripts/validate_exchange.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "exchange"
BASE = "https://triodian.com/exchange/"
DRAFT = "http://json-schema.org/draft-07/schema#"
failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"  FAIL  {msg}")


def main() -> int:
    schemas = {}
    print("1. Exchange schemas are valid draft-07, titled, described and placed")
    for f in sorted(DIR.glob("*.schema.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(f"{f.name}: {e}")
            continue
        if d.get("$schema") != DRAFT:
            fail(f"{f.name}: uses {d.get('$schema')!r}; exchange schemas use {DRAFT}")
        if d.get("$id") != BASE + f.name:
            fail(f"{f.name}: $id is {d.get('$id')!r}; expected {BASE + f.name!r}")
        for k in ("title", "description"):
            if not d.get(k):
                fail(f"{f.name}: missing {k}")
        for err in Draft7Validator(Draft7Validator.META_SCHEMA).iter_errors(d):
            fail(f"{f.name}: {'/'.join(map(str, err.absolute_path)) or '<root>'}: {err.message[:160]}")
        schemas[f.name] = d

    registry = Registry()
    for name, d in schemas.items():
        registry = registry.with_resource(BASE + name, Resource.from_contents(d))

    print("2. Every $ref resolves")
    for name, d in schemas.items():
        def walk(node, path=""):
            if isinstance(node, dict):
                ref = node.get("$ref")
                if isinstance(ref, str):
                    try:
                        registry.resolver(base_uri=BASE + name).lookup(ref)
                    except Exception:
                        fail(f"{name}: {path or '/'}: $ref {ref!r} does not resolve")
                for k, v in node.items():
                    walk(v, f"{path}/{k}")
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk(v, f"{path}/{i}")
        walk(d)

    print("3. Every example validates against its schema")
    covered = set()
    for ex in sorted((DIR / "examples").glob("*.json")):
        stem = ex.name.split(".")[0]
        name = stem + ".schema.json"
        if name not in schemas:
            fail(f"examples/{ex.name}: no schema {name}")
            continue
        covered.add(name)
        instance = json.loads(ex.read_text(encoding="utf-8"))
        v = Draft7Validator({"$ref": BASE + name}, registry=registry)
        errs = sorted(v.iter_errors(instance), key=lambda e: list(e.absolute_path))
        for e in errs[:8]:
            fail(f"examples/{ex.name}: /{'/'.join(map(str, e.absolute_path))}: {e.message[:200]}")
        if not errs:
            print(f"  ok    examples/{ex.name}")

    print("4. Every schema has an example")
    for name in schemas:
        if name not in covered:
            fail(f"{name}: no example in exchange/examples/")

    print(f"\n{len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
