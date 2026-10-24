# Documentation worked examples

These are the JSON worked examples from the metamodel documentation (03 Sep 2025 edition), one instance per file. `manifest.json` records which schema (and, for element-level examples, which definition) each one should validate against, and the line in the source document it came from.

Run them with:

```bash
python scripts/validate.py --only-doc-examples
```

All examples pass, and CI fails if one stops passing. An example that fails means the documentation and the schema disagree: decide which is correct, then fix the schema or update the example (and the documentation) to match.

## Amendments to the documentation's examples

The examples were extracted verbatim and then amended as follows to match agreed schema decisions. The published documentation should be updated in the same way.

**Performance: enum values are camelCase.** All five Performance examples use camelCase values, for example `"Highly Automated"` → `"highlyAutomated"`, `"Lagging Indicator"` → `"laggingIndicator"`, `"Federal Regulations"` → `"federalRegulations"`. This applies to the KPI elements too (`"Lagging KPI"` → `"laggingKPI"`, `"Critical"` → `"critical"`).

**Performance: the KPI list is `performanceKPIs`.** The schema previously named this property `kpi`, so the documentation's KPIs were not validated. The schema now uses `performanceKPIs`, as the documentation does.

**Sub-elements carry a `purpose`.** Service features, information elements and performance KPIs require a `purpose`, and KPIs also require an `owner`. A `purpose` was added to each such sub-element in the Services (5), Information (5) and Performance (5) examples, and each KPI's `owner` was set to the owner of its parent metric.

**Market and Finance validate against rewritten schemas.** The schemas were rewritten to describe market and finance records as the documentation does.

**Market and Finance use the shared vocabulary.** Their dependencies use camelCase domain and dependency values (`"Capability"` → `"capability"`, `"Critical"` → `"critical"`), and the Finance risk level uses the shared four-point scale (`"moderate"` → `"medium"`). The Finance example's `"dependencyType": "Enabler"` has no shared equivalent and is mapped to `"important"`.

**All domains use the shared vocabulary.** Values for shared concepts such as priority, risk level, frequency, status, maturity and automation are camelCase throughout (`"High"` → `"high"`, `"Semi-Automated"` → `"semiAutomated"`, `"PLANNED"` → `"planned"`). Risk levels use the shared four-point scale (`"High Risk"` → `"high"`). See [`docs/vocabulary-migration.json`](../../docs/vocabulary-migration.json) for the full mapping.

**Every enumerated value is camelCase.** Values in all domains are camelCase, not only shared concepts (`"Core Business"` → `"coreBusiness"`, `"Policy_Change"` → `"policyChange"`, `"spare-parts"` → `"spareParts"`). Regulations use their short names (`"GDPR (General Data Protection Regulation)"` → `"gdpr"`, `"Basel III (Banking)"` → `"basel3"`).

**Every record has an identifier.** Records whose schema now requires an identifier were given one in the form `PREFIX-NNN`, for example `capabilityID: "CAP-001"`, `strategyID: "STR-001"`, `orgUnitID: "OU-001"`. A record that also appears among a schema's own embedded examples has the same identifier in both places.

**Products follow the documented attributes.** The Products schema now defines every documented attribute and product-feature element, so the Products examples are checked in full for the first time. Their values are camelCase (`"Information Product"` → `"informationProduct"`, `"B2B"` → `"b2b"`), and risk categories use the shared list (`"Technical"` → `"technology"`, `"Regulatory"` → `"compliance"`). The Innovation example's dependencies use the shared camelCase values, and the Sustainability example's `"third-party verified"` is now `"third-party-verified"`.

**Cross-domain relationships are records with identifiers.** The documentation's three relationship examples (nine relationships) are checked one relationship per file, each given a `relationshipID` (`CDR-001` to `CDR-009`). Domains are camelCase (`"Value Stream"` → `"valueStream"`), and `metadata.impact` is named `impactArea`, because it classifies the area affected rather than a magnitude.

**Inter-unit relationships follow the repository's conventions.** Each example has a `relationshipID` (`IUR-001`, `IUR-002`). The organization unit is `orgUnitTitle` (documented as `organizationUnit`), matching every other domain. Domains and roles are camelCase (`"Value Stream"` → `"valueStream"`, `"Contributing"` → `"contributing"`).

**Model Risk Management uses repository identifiers.** The five MRM examples use `…ID` rather than `…Id` (`modelId` → `modelID`, `findingId` → `findingID`), and each element example carries the `modelID` of the model it belongs to (`MODEL-ECL-IFRS9-001`). Monitoring dependencies use the shared camelCase values (`"Critical"` → `"critical"`, `"Information"` → `"information"`). A regulatory framework mapping lists the models it covers in `modelIDs`, since a framework clause can apply to several models or to the framework as a whole. Requirements use the shared compliance status (`"met"` → `"compliant"`), and `appliesTo` is camelCase (`"Model"` → `"model"`). A model's `status` is its lifecycle state (`inDevelopment` … `approved`, `inUse` … `retired`).

**Values the documentation uses are in the lists.** The documentation's attribute tables give example values rather than complete lists. Where an example used a value that a near-duplicate already covers, the example uses the existing value; otherwise the value was added to the list.
- Mapped to an existing value: `"Mobile App Store"` → `mobileApp`, `"API Platform"` and `"Developer Portal"` → `api`, `"Union"` → `laborUnions`, `"Community Organizing Model"` → `communityOrganizing`, `"2-year implementation"` → `multiYearTransformation`, `"Violent"` → `armedResistance`. Revolutionary phases use the documented names (`mobilization`, `consolidation`).
- Added to the list: Products `businessModel` `internalService`, `internalTool`; `channels` `internalDistribution`; `pricingStrategy` `usageBased`. Strategy `marketPosition` `defensivePositioning`. Social Change `revolutionaryPhases` `colonialResistance`, `armedStruggle`, `territoryControl`, `independence`. Intelligence `sourceType` `internalMonitoring`, `collectionMethod` `manualInvestigation`, `reliabilityRating` `variable`.
- Products `customerSegments` use the documented list of customer types (`enterprise`, `smb`, `government` … plus `internal` for internal products). Named segments such as "Railway Operators" are Customer-domain records, referenced by `customerSegmentIDs`; the examples list the matching types (`["enterprise", "government"]`, `["internal"]`).

**Technology uses its attribute table and the shared performance indicator.** Performance indicators use the shared definition's names (`indicatorName`/`description` → `metricName`/`metricDescription`), and `annualLicensing` plus `annualOperational` are combined in `annualOperatingCost` (`"$1.2M ($750K licensing, $450K operations)"`). `securityClassification` is a rating, as documented ("High - Contains sensitive customer data"): `"high - gateway to critical business systems"` → `high`, with the reason in prose. Other values are mapped to the documented lists (`"infrastructure-software"` → `infrastructure`, `"operational"` → `production`, trend `"increasing"` → `improving`). Its `relationshipExamples` are `crossDomainRelationships`: `enables` a capability and an initiative, and `delivers` a service.

**Every identifier is named `<entity>ID`.** Social Change examples have a `socialChangeID` (`SC-001` …), and the coverage examples use `coverageExpectationID`, `coverageStatusID`, `coverageTemplateID` and `goalID` instead of `id`.

**Cross-domain relationship CDR-008** ("Compliance function audits…") has source domain `organization`: the compliance function is an organization unit.

**One example is not checked.** The documentation's second manufacturing work order example is a status-update payload (it changes only `status`), not a complete work order.

**Two element fields are renamed.** In Market's industry analysis, a profitability driver's `impact` is `effectDirection` (its values run from `veryNegative` to `veryPositive`, a direction rather than a magnitude). In Finance's financial resource, `resourceLifecycle.lifecycleStage` is `resourceStatus` (`planned`, `active`, `maturing`, `retired`: a resource's state, not a delivery lifecycle).

**Supply chain implementation complexity uses the shared complexity scale** (`"medium"` → `moderate`, `"high"` → `complex`).

