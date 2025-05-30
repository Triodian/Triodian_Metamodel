# Interoperability

This directory contains semantic mapping resources to enable interoperability between the Orthogramic Metamodel and other enterprise architecture and industry-standard frameworks.

Each mapping defines a JSON-LD `@context` file to help align terminology and structure for integration, transformation, and knowledge graph construction.

---

## Available mappings

| Framework                             | Context file                                        | Description                                                                 |
|---------------------------------------|-----------------------------------------------------|-----------------------------------------------------------------------------|
| BIAN (Banking Industry Architecture Network) | [orthogramic-bian.context.jsonld](orthogramic-bian.context.jsonld) | Maps BIAN service domains to Orthogramic domains                            |
| SAP Enterprise Architecture Framework | [orthogramic-sap.context.jsonld](orthogramic-sap.context.jsonld)   | Maps SAP EA concepts to Orthogramic Metamodel domains                       |
| FIBO (Financial Industry Business Ontology) | [orthogramic-fibo.context.jsonld](orthogramic-fibo.context.jsonld) | Aligns Orthogramic properties with formalised financial and regulatory semantics |

---

## BIAN mapping

### Overview
- **Format:** JSON-LD  
- **Purpose:** Enable semantic APIs, business architecture alignment, and integration with banking and enterprise models  
- **Compatibility:** BIAN, schema.org, FOAF, ArchiMate  
- **Version:** 1.0.0  
- **License:** Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)  
- **Context URI:** https://orthogramic.org/context/orthogramic-bian.jsonld  

### Domains
- `ServiceDomain` → `Capabilities`, `Services`, `Information`, `Products`
- `FunctionalPattern` → supports structural analysis of business functions
- `BusinessArea` → maps to Orthogramic `Organization` or `CapabilityGroup`

### Inter-domain and cross-domain relationships
- Service domains reused across capability groups
- Stakeholder-to-service and service-to-process interactions
- Support for mapping regulatory, operational, and functional boundaries

### Strategic Response Model (SRM)
- Aligns BIAN domains with strategic objectives and initiatives
- Enables use of BIAN in capability uplift, risk management, and service rationalisation
- Facilitates transformation roadmap alignment with performance indicators

### Use in Semantic APIs
BIAN’s published RESTful APIs can be semantically annotated using this context to:
- Auto-generate business architecture metadata
- Link banking microservices to capabilities and value streams
- Enable capability maturity analysis via API introspection tools

---

## SAP Enterprise Architecture Framework mapping

### Overview
- **Format:** JSON-LD  
- **Purpose:** Enable semantic APIs, business architecture alignment, and integration with enterprise architecture platforms  
- **Compatibility:** SAP EA Framework, schema.org, FOAF, ArchiMate  
- **Version:** 1.0.0  
- **License:** Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)  
- **Context URI:** https://orthogramic.org/context/orthogramic-sap.jsonld  

### Domains
- `StrategicGoal` → `Strategy`
- `BusinessCapability` → `Capabilities`
- `BusinessProcessSegment` → `ValueStream`
- `GovernancePrinciple` → `Policy`
- `OrganizationalUnit` → `Organization`
- `ChangeInitiative` → `Initiatives`
- `InformationObject` → `Information`
- `ServiceOrProduct` → `Products`, `Services`
- `BusinessRole` → `Stakeholders`
- `PerformanceIndicator` → `Performance`

### Inter-domain and cross-domain relationships
- Capabilities → Value Streams → Initiatives
- Organisational accountability linked to business units
- Strategic goals tied to KPIs and services via policy and capability chains

### Strategic Response Model (SRM)
- Brings structure to SAP EA views of strategic execution
- Maps initiative outcomes to performance and policy domains
- Enables analysis of alignment gaps and prioritisation of capability uplift

### Use in Semantic APIs
_(To be populated)_  
Semantic enrichment of SAP EA data models is possible, but API-level interoperability depends on specific SAP tools (e.g. Enterprise Architecture Designer) and their export options. Use of this context in knowledge graph construction and alignment verification is supported.

---

## Usage

To apply a context, reference the appropriate `.context.jsonld` file in your JSON-LD document. For example:

```json
{
  "@context": "https://raw.githubusercontent.com/Orthogramic/Orthogramic_Metamodel/main/interoperability/orthogramic-sap.context.jsonld",
  "Capabilities": {
    "sap:BusinessCapability": "Customer Relationship Management"
  }
}
```

---

### FIBO (Financial Industry Business Ontology) interoperability

The Orthogramic Metamodel now includes schema-level mappings to the Financial Industry Business Ontology (FIBO), enabling integration with regulatory, financial, and compliance-focused enterprise data ecosystems. These mappings align core Orthogramic business architecture properties—such as `performanceIndicators`, `orgUnitTitle`, `strategicAlignment`, and `stakeholders`—to FIBO-standard properties used in semantic financial models.

#### Overview  
**Format:** JSON-LD  
**Purpose:** Support semantic APIs, enterprise graph alignment, and regulatory interoperability in financial services  
**Compatibility:** FIBO, Schema.org, FOAF, ArchiMate  
**Version:** 1.0.0  
**License:** Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)  
**Context URI:** [orthogramic-fibo.context.jsonld](https://github.com/Orthogramic/Orthogramic_Metamodel/blob/main/interoperability/orthogramic-fibo.context.jsonld)

#### Use cases  
- Integration with financial knowledge graphs and regulatory taxonomies  
- Enhanced traceability of strategic and operational alignment to financial KPIs  
- Cross-domain reasoning and compliance reporting using shared semantics

