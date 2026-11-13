# Triodian Metamodel

The **Triodian Metamodel** is an open-source, schema-first framework for business architecture. It provides a structured and extensible foundation to describe how an organisation operates, delivers value, and responds to change. Designed for clarity, integration, and automation, it supports strategic alignment, governance, and continuous improvement at scale.

## What’s included

The metamodel is composed of structured JSON Schemas for all core business architecture domains:

- **Strategy** – Goals, drivers, and strategic direction  
- **Capabilities** – What the organisation is able to do  
- **Value Streams** – How value is delivered across stages  
- **Organisation** – Units, roles, structure, and ownership  
- **Stakeholders** – People and groups with influence or interest  
- **Information** – Business-critical data and governance  
- **Performance** – Measurable indicators of success (KPIs)  
- **Initiatives** – Projects and programs driving change  
- **Policy** – Rules, compliance, and governance  
- **Products** – Tangible or intangible deliverables  
- **Services** – Activities that create value through interaction  
- **Customer** – Customer segments, with personas, journeys and relationships
- **Model Risk Management** – A Risk sub-domain: model inventory, governance, validation, monitoring and regulatory framework mapping
- **Cross-Domain Relationships** – Typed, directional links between entities in different domains
- **Inter-unit Domain Relationships** – Links between units and domain artefacts  
- **Semantic Library** – Obligations captured at clause level, and the semantic constraints that govern what AI systems may say or emit, traced to those obligations and to the business context they apply to (see [the advice-boundary example](examples/semantic-library-advice-boundary.md))
- **Strategic Response Model (SRM)** – How the organisation responds to change: Triggers, Rationales, Strategic Intents and Strategic Responses, each in its own schema and grouped by `strategic-response-model.schema.json`
- **Compliance** – Compliance requirements issued by regulators, professional and standards bodies, each made up of clause-level obligations, and the statements of compliance that evidence them (`schemas/compliance/`)
- **Public Reporting** – Public reports and the mandatory disclosures they contain, including AI disclosures a law calls for (`schemas/public-reporting/`)
- **Use Case** – Standardised AI use cases defined on the authority (A), boundary (B) and confidentiality channel (K) scales, so obligations and assessments compare across jurisdictions; UC1 to UC10 are published in [`reference-data/use-cases.json`](reference-data/use-cases.json)
- **Regulated Sector** – The fields an organization works in within a jurisdiction (banking, insurance, superannuation, health, critical infrastructure and others), each grouping the entity types obligations are addressed to, so a user can choose a jurisdiction, then a sector, then the entity type; Australia and Singapore are published in [`reference-data/regulated-sectors.json`](reference-data/regulated-sectors.json); up to five main sectors a jurisdiction carry their own packs, and [adding a jurisdiction](docs/adding-a-jurisdiction.md) sets out how a new one is added
- **Baseline Profile** – Best-practice sector profiles that hold in any jurisdiction (banking, insurance, securities and investment advice, health care, payments, critical infrastructure run by government or by a company, and government in general), drawn from international standard setters and adopted standards, with four controls every profile carries; see [baselines](docs/baselines.md) and [`reference-data/baseline-profiles.json`](reference-data/baseline-profiles.json)
- **Dynamic and Time-Series** – Data flows, timebound metrics and predictive models for live and monitored sources (`schemas/extensions/dynamic-time-series/`)

All domains are defined using [JSON Schema](https://json-schema.org/), ensuring they are machine-readable and interoperable across platforms.

## Why Triodian?

Triodian differs from traditional frameworks like BIZBOK in key ways:

- **Open-source and transparent** – Freely licensed under the Apache License 2.0  
- **Schema-first and digital** – Designed for automation, integration, and validation  
- **Inclusive and scalable** – Usable by strategists, analysts, and business teams, not just architects  
- **Real-time and actionable** – Supports dynamic alignment and structured decision-making  
- **Integrated** – Performance and policy domains are built in, not bolted on  

For a comparison with BIZBOK, see:  
[Comparing the Triodian Metamodel with BIZBOK](https://triodian.atlassian.net/wiki/spaces/OM/pages/245137981)

## Getting started

Visit the documentation to begin:

- [Model overview](https://triodian.atlassian.net/wiki/spaces/OM/pages/290914392)  
- [Getting started guide](https://triodian.atlassian.net/wiki/spaces/OM/pages/290914392)  
- [New to Business Architecture](https://triodian.atlassian.net/wiki/spaces/OM/pages/288948263)  
- [Familiar with BIZBOK](https://triodian.atlassian.net/wiki/spaces/OM/pages/288948285)  
- [Getting started by problem](https://triodian.atlassian.net/wiki/spaces/OM/pages/291274855)

Each schema includes examples and structured fields to help your team model capabilities, initiatives, and performance in a consistent and transparent way.

## Obligations as a reference dataset

Obligations can be published as a reference dataset, such as a register of AI governance obligations by jurisdiction. Each record carries:
- `sourceTier`: `binding`, `expected`, `anticipated` or `adopted`. `adopted` is a voluntary standard an organisation has adopted for itself, such as the controls of ISO/IEC 42001:2023 Annex A; which of its records apply to a client is set by the client's own Statement of Applicability, not by the record;
- `jurisdiction`, `entityTypes`, `roles` and `useCaseIDs`;
- `effectiveDates` and `lastVerified`.

Regulators and standards bodies are External Organization records. Each new or amended instrument is a Trigger, linked to the obligations it affects. A source tier describes the source, never an organisation's position.

## Governance interface

The [`governance-interface/`](governance-interface) folder defines a contract for services that govern records written against the Metamodel. Such a service validates submitted records, routes changes to named reviewers, and returns published records with a hash-chained provenance trail. The folder contains:
- the message schemas, in `schemas/governance/`;
- an HTTP binding, `governance-interface/openapi.yaml`;
- an example dataset policy, in `governance-interface/example-policies/`.

The Metamodel version is in [`VERSION`](VERSION).

## Exchange formats

The Triodian AI governance apps pass a few files to each other: the matter brief, the board directions, the calibration set, the register extract (the in-use feed, which carries the findings), the board view and the confidentiality position. [`exchange/`](exchange) publishes each as a versioned JSON Schema with examples, so anyone can check a file, build a tool that reads one, or import one into another platform. They keep the field names the apps already use, so they sit outside `schemas/` and its domain naming rules. `scripts/validate_exchange.py` checks them in CI.

## Validating the schemas

Every change is checked by `scripts/validate.py`, which runs in CI on each push and pull request:

```bash
pip install -r scripts/requirements.txt
python scripts/validate.py                    # structural checks
python scripts/validate.py --doc-examples     # plus the documentation's worked examples
```

The structural checks confirm that every schema is well-formed JSON, valid against its declared JSON Schema draft, free of non-standard keywords (such as `attributes`, `elements` or `nullable`), that every `$ref` resolves, and that each schema's embedded examples validate against it.

Every schema file is kebab-case, ends in `.schema.json`, and has an `$id` of `https://triodian.com/schemas/` followed by its path. Every property has a description. The interoperability mappings in [`interoperability/`](interoperability) are valid JSON-LD and map only terms the schemas define.

Shared concepts such as priority, risk level, frequency, status, maturity and domain type are defined once in [`schemas/common.schema.json`](schemas/common.schema.json), with camelCase values, and domains reference them with `$ref`. [`docs/shared-vocabulary.md`](docs/shared-vocabulary.md) lists the shared values and shows which domains still keep their own lists and how those map across. Regenerate it with `python scripts/vocabulary_map.py`.

Every domain schema has the same structure. The root is the domain's main record (an Initiative, a Value Stream, a Policy), and its element types (a Program, a Value Stream Stage, a Capability Function) are named, camelCase entries under `definitions`, referenced with `$ref`. All schemas use JSON Schema draft-07, and all definition names, property names and enumerated values are camelCase. Composite schemas such as `strategic-response-model.schema.json` group records defined in other schemas.

Relationships between domains use [`schemas/cross-domain-relationship.schema.json`](schemas/cross-domain-relationship.schema.json): one of 37 relationship types (such as `funds`, `enables`, `governs`, `informs`), with priority, impact area, frequency and strength. Relationships are directional, from an initiating domain to a receiving one. Passive domains (Information, Performance, Product, Service) receive relationships but never initiate them; the schema and validator enforce this. A relationship can be a record of its own, or listed in a domain record's `crossDomainRelationships`, where the containing record is the source. Records that refer to entities in other domains without a typed relationship, such as a Trigger's `affectedEntities`, use the shared `entityReference`.

Every object a schema defines rejects fields it does not define (`"additionalProperties": false`), so a misspelt or undocumented field fails validation instead of being silently accepted. The validator enforces this for every schema.

Every record has a required identifier named after its entity, such as `capabilityID`, `strategyID` or `orgUnitID`, using the shared `identifier` definition. Records link to each other by these identifiers. Fields such as `orgUnitID`, `parentCapabilityID` and `relatedStrategyIDs` sit alongside the corresponding name fields (`orgUnitTitle`, `parent`, `relatedStrategies`), which are kept for readability.

The worked examples published in the metamodel documentation are kept in [`examples/doc-examples`](examples/doc-examples) and validated against their schemas in CI, so the documentation and the schemas cannot drift apart.

## Contributing

We welcome your input! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to propose improvements, submit pull requests, or engage with the community.

Contribution guidelines and project manifesto are also available at:  
[Contribution Guidelines](https://triodian.atlassian.net/wiki/spaces/OM/pages/291799095)  
[Open Source Manifesto](https://triodian.atlassian.net/wiki/spaces/OM/pages/291799095)

## Licence

This repository and its contents are licensed under the  
**Apache License, Version 2.0**  
See [LICENSE](LICENSE) or [view licence](https://www.apache.org/licenses/LICENSE-2.0).

You are free to use, modify, and redistribute this work, including commercially, provided you retain the licence and copyright notices and state any significant changes you make.
