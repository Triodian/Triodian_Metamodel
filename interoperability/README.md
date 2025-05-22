# Orthogramic Metamodel – JSON-LD Ontology Summary

This document defines the structured, schema-based representation of business architecture domains used by **Orthogramic**, with mappings designed for semantic interoperability with external frameworks including **BIAN**, **TOGAF**, and **schema.org**.

## Overview

* **Format**: JSON-LD
* **Purpose**: Enable semantic APIs, business architecture alignment, and integration with banking and enterprise models
* **Compatibility**: BIAN, schema.org, FOAF, ArchiMate
* **Version**: 1.0.0
* **License**: Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)
* **Context URI**: https://orthogramic.org/context/orthogramic-bian.jsonld

## Domains

### Capabilities
Defines what an organisation is able to do, independent of how it is done. Serves as the bridge between strategy and operations. **Mapped to**: `bian:BusinessCapability`

### Services
Represents business or technical offerings delivered to customers, internal stakeholders, or partner systems. **Mapped to**: `bian:ServiceDomain`

### Stakeholders
Describes people, groups, or institutions that influence or are influenced by the organisation. **Mapped to**: `foaf:Agent`

### Value Streams
Models the stages of value creation — showing how value flows from initiation to outcome. **Mapped to**: `bian:ValueStream`

### Initiatives
Captures programs, projects, or major efforts that enable change and implement strategy. **Mapped to**: `bian:InitiativeProgram`

### Policy
Describes regulatory obligations, internal controls, and formal decision-making rules. **Mapped to**: `bian:PolicyRule`

### Information
Captures data entities, structures, and custodianship aligned with business capabilities and governance. **Mapped to**: `schema:Dataset` (complemented by BIAN data specification constructs)

### Performance
Measures outcomes and progress via KPIs and metrics linked to strategic objectives. **Mapped to**: `bian:PerformanceAssessment`, `bian:PerformanceIndicator`

### Strategic Response Model (SRM)
Links **Triggers**, **Rationales**, and **Strategic Responses** across domains to support dynamic alignment and decision-making. **Mapped to**:
* `bian:TriggerEvent`
* `bian:RationaleForChange`
* `bian:ResponseStrategy`

## Use in Semantic APIs

This metamodel enables:
* Federated querying of architecture data
* Business-aligned API responses
* Linked data representations of capability maps, governance models, and change strategies
* Interoperability between banking systems (via BIAN) and enterprise architecture platforms

## Attribution

This ontology mapping is published under the **Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)** licence. It is intended for reuse, extension, and implementation in open and enterprise environments.
