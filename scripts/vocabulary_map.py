#!/usr/bin/env python3
"""Map every local enumeration of a shared concept onto schemas/common.schema.json.

For each field that expresses a shared concept (risk level, frequency, status and so on),
this works out which shared definition it corresponds to and how each current value maps
onto the shared values. It writes:

  docs/vocabulary-migration.json   machine-readable mapping, used to migrate domains
  docs/shared-vocabulary.md        the same, for review

Usage:
  python scripts/vocabulary_map.py           # write both files
  python scripts/vocabulary_map.py --check   # exit non-zero if a mapped field still uses a local list
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
    ("strategic-response-model.schema.json", "/definitions/strategicResponse/properties/financialResources/properties/fundingSources/items/properties/status"):
        ("fundingStatus", "Whether funding is secured, pending or proposed"),
    ("strategic-response-model.schema.json", "/definitions/strategicIntent/properties/maturityLevel"):
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


def collect():
    usages = []
    for f in sorted(p for p in SCHEMAS.rglob("*") if p.is_file() and p.name != "common.schema.json"):
        doc = json.loads(f.read_text())
        for path, node in walk(doc):
            props = node.get("properties")
            if not isinstance(props, dict):
                continue
            for field, prop in props.items():
                if field not in FIELD_CANDIDATES:
                    continue
                vocab = local_enum(prop)
                if not vocab:
                    continue
                rel_file = f.relative_to(SCHEMAS).as_posix()
                rel_path = "/" + "/".join(map(str, path + ("properties", field)))
                if (rel_file, rel_path) in DOMAIN_SPECIFIC:
                    rename, reason = DOMAIN_SPECIFIC[(rel_file, rel_path)]
                    usages.append({"file": rel_file, "path": rel_path, "field": field, "target": None,
                                   "renameTo": rename, "reason": reason, "values": {v: {"to": None, "note": "local"} for v in vocab}})
                    continue
                best = None
                candidates = [FIELD_OVERRIDES[(rel_file, rel_path)]] if (rel_file, rel_path) in FIELD_OVERRIDES \
                    else FIELD_CANDIDATES[field]
                for cand in candidates:
                    mapped = [map_value(cand, v, vocab) for v in vocab]
                    exact = sum(1 for v in vocab if norm(v) in {norm(c) for c in values_of(cand)})
                    score = (sum(1 for m in mapped if m[1] != "unmapped"), exact)
                    if best is None or score > best[0]:
                        best = (score, cand, mapped)
                _, target, mapped = best
                usages.append({
                    "file": rel_file,
                    "path": rel_path,
                    "field": field,
                    "target": target,
                    "values": {v: {"to": m[0], "note": m[1]} for v, m in zip(vocab, mapped)},
                })
    return usages


def write(usages):
    out = ROOT / "docs"
    out.mkdir(exist_ok=True)
    (out / "vocabulary-migration.json").write_text(json.dumps({"usages": usages}, indent=2, ensure_ascii=False) + "\n")

    local = [u for u in usages if u["target"] is None]
    usages = [u for u in usages if u["target"] is not None]
    by_target = defaultdict(list)
    for u in usages:
        by_target[u["target"]].append(u)
    lines = [
        "# Shared vocabulary",
        "",
        "`schemas/common.schema.json` defines the controlled vocabularies and reusable structures every domain should use. "
        "All values are camelCase. Domains reference them with `$ref` instead of keeping their own lists.",
        "",
        "This page is generated by `scripts/vocabulary_map.py`. For each shared definition it lists the canonical values "
        "and every field in the schemas that currently keeps its own list, with how each current value maps across.",
        "",
        "- **lossy**: the mapping merges values that currently mean different things. Needs a decision.",
        "- **unmapped**: the value has no shared equivalent. Either add it to the shared list or keep it as a domain-specific value.",
        "",
    ]
    total = sum(len(u["values"]) for u in usages)
    lossy = [(u, v) for u in usages for v, m in u["values"].items() if m["note"] == "lossy"]
    unmapped = [(u, v) for u in usages for v, m in u["values"].items() if m["note"] == "unmapped"]
    lines += [f"**{len(usages)} fields** keep a local list for a shared concept ({total} values): "
              f"{total - len(lossy) - len(unmapped)} map directly, {len(lossy)} are lossy, {len(unmapped)} are unmapped.", ""]

    if lossy or unmapped:
        lines += ["## Values needing a decision", "", "| Field | Value | Proposed | Issue |", "|---|---|---|---|"]
        for u, v in lossy + unmapped:
            m = u["values"][v]
            lines.append(f"| `{u['file']}` {u['path']} | `{v}` | {('`' + m['to'] + '`') if m['to'] else '—'} | {m['note']} |")
        lines.append("")

    if local:
        lines += ["## Domain-specific lists to rename", "",
                  "These fields reuse a generic name for a domain-specific idea. They keep their own values "
                  "but should be renamed so they are not mistaken for the shared concept.", "",
                  "| Field | Rename to | Why |", "|---|---|---|"]
        for u in local:
            lines.append(f"| `{u['file']}` {u['path']} | `{u['renameTo']}` | {u['reason']} |")
        lines.append("")

    lines += ["## Definitions and current usages", ""]
    for name in COMMON:
        d = COMMON[name]
        if "enum" not in d and "allOf" not in d:
            continue
        lines += [f"### `{name}`", "", d.get("description", ""), "", "Values: " + ", ".join(f"`{v}`" for v in values_of(name)), ""]
        if d.get("allOf"):
            lines += [f"Uses the `{d['allOf'][0]['$ref'].split('/')[-1]}` scale.", ""]
        if by_target.get(name):
            lines += ["| Field | Current → shared |", "|---|---|"]
            for u in by_target[name]:
                pairs = []
                for v, m in u["values"].items():
                    to = m["to"] or "?"
                    mark = "" if m["note"] == "ok" else f" ({m['note']})"
                    pairs.append(f"`{v}`" if v == to else f"`{v}`→`{to}`{mark}")
                lines.append(f"| `{u['file']}` {u['path']} | {', '.join(pairs)} |")
            lines.append("")
    (out / "shared-vocabulary.md").write_text("\n".join(lines) + "\n")
    return total, len(lossy), len(unmapped)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="fail if any shared concept still uses a local list")
    args = ap.parse_args()
    usages = collect()
    if args.check:
        pending = [u for u in usages if u["target"] is not None]
        for u in pending:
            print(f"local list for shared concept: {u['file']} {u['path']} (use {u['target']})")
        return 1 if pending else 0
    total, lossy, unmapped = write(usages)
    print(f"{len(usages)} fields, {total} values: {lossy} lossy, {unmapped} unmapped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
