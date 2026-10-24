#!/usr/bin/env python3
"""Report how the schemas use the shared vocabulary in schemas/common.schema.json.

Writes docs/shared-vocabulary.md: the shared definitions, which fields use each, the
domain-specific values some fields add, fields to rename, and any field that keeps its
own list for a shared concept (with how its values would map across).

Usage:
  python scripts/vocabulary_map.py           # write docs/shared-vocabulary.md
  python scripts/vocabulary_map.py --check   # exit non-zero if any shared concept uses a local list
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
COMMON = json.loads((SCHEMAS / "common.schema.json").read_text())["definitions"]

# Field names that express a shared concept, and the shared definitions they may map to
# (the best fit is chosen from the field's current values).
FIELD_CANDIDATES = {
    "riskLevel": ["riskLevel"],
    "severity": ["severity"],
    "criticality": ["criticality"],
    "priority": ["priority"],
    "importanceLevel": ["importance"],
    "impactLevel": ["ratingLevel", "changeMagnitude", "impactMagnitude"],
    "impact": ["ratingLevel", "impactMagnitude", "changeMagnitude"],
    "confidenceLevel": ["confidenceLevel"],
    "alignmentLevel": ["alignmentLevel"],
    "likelihood": ["likelihood"],
    "probability": ["likelihood"],
    "complexity": ["complexity"],
    "frequency": ["frequency"],
    "reviewFrequency": ["frequency"],
    "monitoringFrequency": ["frequency"],
    "reportingFrequency": ["frequency"],
    "updateFrequency": ["frequency"],
    "engagementFrequency": ["frequency"],
    "measurementFrequency": ["frequency"],
    "timeHorizon": ["timeHorizon"],
    "trend": ["performanceTrend", "quantityTrend"],
    "status": ["workStatus", "documentStatus"],
    "implementationStatus": ["implementationStatus"],
    "complianceStatus": ["complianceStatus"],
    "lifecycle": ["lifecycleStage", "adoptionStage"],
    "lifecycleStage": ["lifecycleStage", "adoptionStage"],
    "maturityLevel": ["maturityLevel"],
    "automation": ["automationLevel"],
    "automationLevel": ["automationLevel"],
    "riskCategories": ["riskCategory"],
    "domainType": ["domainType"],
    "dependencyType": ["dependencyStrength"],
    "geographicScope": ["geographicScope"],
    "level": ["likelihood", "impactMagnitude", "effectiveness", "ratingLevel", "simpleLevel"],
}

# Fields whose meaning can't be inferred from their values alone.
FIELD_OVERRIDES = {
    ("risk-management.schema.json", "/properties/riskSeverity/properties/level"): "riskLevel",
    ("risk-management.schema.json", "/properties/residualRisk/properties/level"): "riskLevel",
    ("social-change.json", "/properties/internationalSupport/items/properties/level"): "simpleLevel",
}

# Synonyms, keyed by normalised current value. A value of (target, "lossy") marks a mapping
# that merges distinct meanings and needs a decision.
SYNONYMS = {
    "ratingLevel": {"moderate": "medium", "highrisk": "high", "mediumrisk": "medium", "lowrisk": "low",
                    "verylow": ("low", "lossy"), "veryhigh": ("critical", "lossy"),
                    "negligible": ("low", "lossy")},
    "confidenceLevel": {"moderate": "medium"},
    "simpleLevel": {"moderate": "medium"},
    "alignmentLevel": {"weak": "low", "moderate": "medium", "strong": "high",
                       "critical": ("high", "lossy"), "perfect": ("high", "lossy")},
    "likelihood": {"moderate": "medium"},
    "impactMagnitude": {"significant": "major", "minimal": "negligible", "critical": ("severe", "lossy")},
    "changeMagnitude": {},
    "effectiveness": {},
    "frequency": {"eventtriggered": "eventDriven", "biannually": "semiAnnually"},
    "timeHorizon": {},
    "performanceTrend": {"worsening": "declining"},
    "quantityTrend": {},
    "workStatus": {"planning": "planned", "active": "inProgress", "ongoing": "inProgress", "implementing": "inProgress",
                   "suspended": "onHold", "abandoned": "cancelled", "canceled": "cancelled",
                   "identified": "proposed", "evaluating": "proposed", "failed": ("cancelled", "lossy")},
    "documentStatus": {},
    "implementationStatus": {"notimplemented": "notStarted", "planning": "planned", "implementing": "inProgress",
                             "piloting": "inProgress", "earlyimplementation": "inProgress", "ongoing": "inProgress",
                             "identified": "notStarted", "evaluating": "planned", "completed": "implemented",
                             "upgrading": "operational", "established": "operational", "mature": "operational",
                             "decommissioning": "retiring", "replaced": "retired"},
    "complianceStatus": {"partial": "partiallyCompliant", "exempted": "exempt", "inprogress": "underReview"},
    "lifecycleStage": {"operations": "operational", "optimisation": "optimization"},
    "adoptionStage": {},
    "maturityLevel": {"developing": "repeatable", "optimized": "optimizing", "advanced": ("managed", "lossy")},
    "automationLevel": {"partiallyautomated": "semiAutomated", "mostlyautomated": "highlyAutomated"},
    "riskCategory": {"technicaltechnology": "technology", "technical": "technology", "complianceregulatory": "compliance",
                     "regulatory": "compliance", "resourcecapacity": "people", "resource": "people", "labor": "people",
                     "organizational": "people", "externalenvironmental": "external",
                     "securitycybersecurity": "security", "cybersecurity": "security", "quality": "dataQuality",
                     "availability": "technology", "communication": "relationship",
                     "diplomatic": ("political", "lossy"), "interpretation": ("other", "lossy")},
    "domainType": {},
    "dependencyStrength": {"minimal": "optional", "informational": "optional"},
    "geographicScope": {"international": "multinational", "localcitymetropolitan": "local",
                        "regionalstateprovince": "regional", "globalworldwide": "global",
                        "virtualdigitalpresenceonly": "virtual"},
}
for alias in ("priority", "criticality", "importance", "riskLevel", "severity"):
    SYNONYMS[alias] = SYNONYMS["ratingLevel"]
SYNONYMS["implementationStatus"]["monitoring"] = "operational"
SYNONYMS["domainType"].update({"standard": ("policy", "lossy"), "process": ("capability", "lossy")})

# Fields that reuse a generic name for a domain-specific idea. They keep their own list,
# but should be renamed so they no longer look like the shared concept.
DOMAIN_SPECIFIC = {
    ("information.schema.json", "/properties/lifecycle"):
        ("informationLifecycleStage", "Stages of data handling (creation, active use, archive, disposal), not a delivery lifecycle"),
    ("performance-indicator.schema.json", "/properties/statusHistory/items/properties/status"):
        ("targetStatus", "Position against target (above, on, below), not work progress"),
    ("shared-initiative.schema.json", "/properties/crossOrgDependencies/items/properties/dependencyType"):
        ("dependencyKind", "What is depended on (information, capability, resource, decision, approval), not how strongly"),
    ("supply-chain.schema.json", "/definitions/supplyChainProcess/properties/processDependencies/items/properties/dependencyType"):
        ("sequenceRelationship", "Process sequencing (predecessor, successor, concurrent), not dependency strength"),
    ("strategic-response.schema.json", "/properties/financialResources/properties/fundingSources/items/properties/status"):
        ("fundingStatus", "Whether funding is secured, pending or proposed"),
    ("strategic-intent.schema.json", "/properties/maturityLevel"):
        ("intentMaturity", "How established a strategic intent is (conceptual to optimizing), not capability maturity"),
}


def norm(v: str) -> str:
    v = re.sub(r"\(.*?\)", "", v)               # drop qualifiers such as "(1 year)"
    v = re.sub(r"^level\s*\d+\s*-\s*", "", v, flags=re.I)  # "Level 2 - Repeatable"
    return re.sub(r"[^a-z0-9]", "", v.lower())


def values_of(defname: str) -> list[str]:
    d = COMMON[defname]
    if "enum" in d:
        return d["enum"]
    return values_of(d["allOf"][0]["$ref"].split("/")[-1])


def map_value(defname: str, value: str, vocab: list[str]):
    canon = {norm(c): c for c in values_of(defname)}
    n = norm(value)
    # CMMI ordering: when "quantitatively managed" is present, plain "managed" is level 2.
    if defname == "maturityLevel" and any(norm(x) == "quantitativelymanaged" for x in vocab):
        if n == "managed":
            return "repeatable", "ok"
        if n == "quantitativelymanaged":
            return "managed", "ok"
    if n in canon:
        return canon[n], "ok"
    syn = SYNONYMS.get(defname, {}).get(n)
    if syn is None:
        return None, "unmapped"
    return (syn[0], syn[1]) if isinstance(syn, tuple) else (syn, "ok")


def walk(node, path=()):
    if isinstance(node, dict):
        yield path, node
        for k, v in node.items():
            yield from walk(v, path + (k,))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, path + (i,))


def local_enum(prop: dict):
    if not isinstance(prop, dict):
        return None
    if "enum" in prop:
        return [v for v in prop["enum"] if v is not None]
    items = prop.get("items")
    if isinstance(items, dict) and "enum" in items:
        return [v for v in items["enum"] if v is not None]
    return None


def shared_ref(prop):
    """If prop uses a shared definition, return (definition, domain-specific extra values)."""
    if not isinstance(prop, dict):
        return None
    node = prop.get("items") if prop.get("type") == "array" and isinstance(prop.get("items"), dict) else prop
    branches = [node] + node.get("allOf", []) + node.get("anyOf", [])
    ref = next((b["$ref"] for b in branches if isinstance(b, dict) and "common.schema.json#/definitions/" in b.get("$ref", "")), None)
    if ref is None:
        return None
    extras = [v for b in node.get("anyOf", []) if isinstance(b, dict) for v in b.get("enum", [])]
    return ref.rsplit("/", 1)[-1], extras


def collect():
    """Return (local, references): local lists of shared concepts, and fields using shared definitions."""
    local, references = [], []
    for f in sorted(p for p in SCHEMAS.rglob("*") if p.is_file() and p.name != "common.schema.json"):
        doc = json.loads(f.read_text())
        rel_file = f.relative_to(SCHEMAS).as_posix()
        for path, node in walk(doc):
            props = node.get("properties")
            if not isinstance(props, dict):
                continue
            for field, prop in props.items():
                rel_path = "/" + "/".join(map(str, path + ("properties", field)))
                used = shared_ref(prop)
                if used:
                    references.append({"file": rel_file, "path": rel_path, "definition": used[0], "extras": used[1]})
                    continue
                if field not in FIELD_CANDIDATES:
                    continue
                vocab = local_enum(prop)
                if not vocab:
                    continue
                if (rel_file, rel_path) in DOMAIN_SPECIFIC:
                    rename, reason = DOMAIN_SPECIFIC[(rel_file, rel_path)]
                    local.append({"file": rel_file, "path": rel_path, "target": None,
                                  "renameTo": rename, "reason": reason, "values": vocab})
                    continue
                candidates = [FIELD_OVERRIDES[(rel_file, rel_path)]] if (rel_file, rel_path) in FIELD_OVERRIDES \
                    else FIELD_CANDIDATES[field]
                best = None
                for cand in candidates:
                    mapped = [map_value(cand, v, vocab) for v in vocab]
                    exact = sum(1 for v in vocab if norm(v) in {norm(c) for c in values_of(cand)})
                    score = (sum(1 for m in mapped if m[1] != "unmapped"), exact)
                    if best is None or score > best[0]:
                        best = (score, cand, mapped)
                _, target, mapped = best
                local.append({"file": rel_file, "path": rel_path, "target": target,
                              "values": {v: {"to": m[0], "note": m[1]} for v, m in zip(vocab, mapped)}})
    return local, references


def write(local, references):
    pending = [u for u in local if u["target"] is not None]
    renames = [u for u in local if u["target"] is None]
    by_def = defaultdict(list)
    for r in references:
        by_def[r["definition"]].append(r)
    extended = [r for r in references if r["extras"]]

    lines = [
        "# Shared vocabulary",
        "",
        "[`schemas/common.schema.json`](../schemas/common.schema.json) defines the controlled vocabularies and reusable "
        "structures every domain uses. All values are camelCase. Domains reference them with `$ref` rather than keeping "
        "their own lists; where a domain genuinely needs extra values, it adds them alongside the shared list.",
        "",
        "This page is generated by `scripts/vocabulary_map.py` and checked in CI. "
        "[`vocabulary-migration.json`](vocabulary-migration.json) records how the previous domain-specific values were mapped.",
        "",
        f"**{len(references)} fields** use a shared definition; {len(extended)} of them add domain-specific values. "
        f"**{len(pending)} fields** keep their own list for a shared concept.",
        "",
    ]
    if pending:
        lines += ["## Fields still keeping their own list", "",
                  "Replace these with a reference to the shared definition.", "",
                  "| Field | Use | Current → shared |", "|---|---|---|"]
        for u in pending:
            pairs = ", ".join(f"`{v}`→`{m['to'] or '?'}`" + ("" if m["note"] == "ok" else f" ({m['note']})")
                              for v, m in u["values"].items())
            lines.append(f"| `{u['file']}` {u['path']} | `{u['target']}` | {pairs} |")
        lines.append("")
    if extended:
        lines += ["## Domain-specific additions", "",
                  "These fields accept the shared list plus a few values specific to their domain.", "",
                  "| Field | Shared definition | Additional values |", "|---|---|---|"]
        for r in extended:
            lines.append(f"| `{r['file']}` {r['path']} | `{r['definition']}` | {', '.join(f'`{v}`' for v in r['extras'])} |")
        lines.append("")
    if renames:
        lines += ["## Domain-specific lists to rename", "",
                  "These fields reuse a generic name for a domain-specific idea. They keep their own values "
                  "but should be renamed so they are not mistaken for the shared concept.", "",
                  "| Field | Rename to | Why |", "|---|---|---|"]
        for u in renames:
            lines.append(f"| `{u['file']}` {u['path']} | `{u['renameTo']}` | {u['reason']} |")
        lines.append("")

    lines += ["## Definitions", ""]
    for name, d in COMMON.items():
        lines += [f"### `{name}`", "", d.get("description", ""), ""]
        if "enum" in d or "allOf" in d:
            lines += ["Values: " + ", ".join(f"`{v}`" for v in values_of(name)), ""]
            if d.get("allOf"):
                lines += [f"Uses the `{d['allOf'][0]['$ref'].split('/')[-1]}` scale.", ""]
        users = by_def.get(name, [])
        if users:
            files = sorted({r["file"] for r in users})
            lines += [f"Used by {len(users)} field(s) in: " + ", ".join(f"`{f}`" for f in files), ""]
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "shared-vocabulary.md").write_text("\n".join(lines) + "\n")
    return pending


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="fail if any shared concept still uses a local list")
    args = ap.parse_args()
    local, references = collect()
    pending = [u for u in local if u["target"] is not None]
    if args.check:
        for u in pending:
            print(f"local list for shared concept: {u['file']} {u['path']} (use {u['target']})")
        print(f"{len(references)} fields use the shared vocabulary; {len(pending)} keep their own list")
        return 1 if pending else 0
    write(local, references)
    print(f"{len(references)} fields use the shared vocabulary; {len(pending)} keep their own list")
    return 0


if __name__ == "__main__":
    sys.exit(main())
