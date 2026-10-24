# Documentation worked examples

These are the JSON worked examples from the metamodel documentation (03 Sep 2025 edition), one instance per file. `manifest.json` records which schema (and, for element-level examples, which definition) each one should validate against, and the line in the source document it came from.

Run them with:

```bash
python scripts/validate.py --only-doc-examples
```

An example that fails means the documentation and the schema disagree. Decide which one is correct, then fix the schema or update the example (and the documentation) to match.

## Amendments to the documentation's examples

The examples were extracted verbatim and then amended as follows to match agreed schema decisions. The published documentation should be updated in the same way.

**Performance: enum values are camelCase.** All five Performance examples use camelCase values, for example `"Highly Automated"` → `"highlyAutomated"`, `"Lagging Indicator"` → `"laggingIndicator"`, `"Federal Regulations"` → `"federalRegulations"`. This applies to the KPI elements too (`"Lagging KPI"` → `"laggingKPI"`, `"Critical"` → `"critical"`).

**Performance: the KPI list is `performanceKPIs`.** The schema previously named this property `kpi`, so the documentation's KPIs were not validated. The schema now uses `performanceKPIs`, as the documentation does.

**Sub-elements carry a `purpose`.** Service features, information elements and performance KPIs require a `purpose`, and KPIs also require an `owner`. A `purpose` was added to each such sub-element in the Services (5), Information (5) and Performance (5) examples, and each KPI's `owner` was set to the owner of its parent metric.

**Market and Finance validate against rewritten schemas.** The schemas were rewritten to describe market and finance records as the documentation does.

**Market and Finance use the shared vocabulary.** Their dependencies use camelCase domain and dependency values (`"Capability"` → `"capability"`, `"Critical"` → `"critical"`), and the Finance risk level uses the shared four-point scale (`"moderate"` → `"medium"`). The Finance example's `"dependencyType": "Enabler"` has no shared equivalent and is mapped to `"important"`.

**All domains use the shared vocabulary.** Values for shared concepts such as priority, risk level, frequency, status, maturity and automation are camelCase throughout (`"High"` → `"high"`, `"Semi-Automated"` → `"semiAutomated"`, `"PLANNED"` → `"planned"`). Risk levels use the shared four-point scale (`"High Risk"` → `"high"`). See [`docs/vocabulary-migration.json`](../../docs/vocabulary-migration.json) for the full mapping.

**Every record has an identifier.** Records whose schema now requires an identifier were given one in the form `PREFIX-NNN`, for example `capabilityID: "CAP-001"`, `strategyID: "STR-001"`, `orgUnitID: "OU-001"`. A record that also appears among a schema's own embedded examples has the same identifier in both places.

**Products follow the documented attributes.** The Products schema now defines every documented attribute and product-feature element, so the Products examples are checked in full for the first time. Their values are camelCase (`"Information Product"` → `"informationProduct"`, `"B2B"` → `"b2b"`), and risk categories use the shared list (`"Technical"` → `"technology"`, `"Regulatory"` → `"compliance"`). The Innovation example's dependencies use the shared camelCase values, and the Sustainability example's `"third-party verified"` is now `"third-party-verified"`.

## Not included

There is no schema in the repository yet for:

- Model Risk Management sub-domain examples (model profile, governance, validation, monitoring, regulatory framework mapping)
- Cross-domain relationship examples
