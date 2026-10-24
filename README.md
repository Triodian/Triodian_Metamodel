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
- **Inter-unit Domain Relationships** – Links between units and domain artefacts  
- **Strategic Response Model (SRM)** – How the organisation responds to triggers and rationales

All domains are defined using [JSON Schema](https://json-schema.org/), ensuring they are machine-readable and interoperable across platforms.

## Why Triodian?

Triodian differs from traditional frameworks like BIZBOK in key ways:

- **Open-source and transparent** – Freely licensed under Creative Commons  
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

## Validating the schemas

Every change is checked by `scripts/validate.py`, which runs in CI on each push and pull request:

```bash
pip install -r scripts/requirements.txt
python scripts/validate.py                    # structural checks
python scripts/validate.py --doc-examples     # plus the documentation's worked examples
```

The structural checks confirm that every schema is well-formed JSON, valid against its declared JSON Schema draft, free of non-standard keywords (such as `attributes`, `elements` or `nullable`), that every `$ref` resolves, and that each schema's embedded examples validate against it.

The worked examples published in the metamodel documentation are kept in [`examples/doc-examples`](examples/doc-examples) and validated against their schemas, so drift between the documentation and the schemas is visible.

## Contributing

We welcome your input! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to propose improvements, submit pull requests, or engage with the community.

Contribution guidelines and project manifesto are also available at:  
[Contribution Guidelines](https://triodian.atlassian.net/wiki/spaces/OM/pages/291799095)  
[Open Source Manifesto](https://triodian.atlassian.net/wiki/spaces/OM/pages/291799095)

## Licence

This repository and its contents are licensed under the  
**Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**  
[View licence](https://creativecommons.org/licenses/by-sa/4.0/)

You are free to use, adapt, and redistribute this work with attribution and under the same licence.
