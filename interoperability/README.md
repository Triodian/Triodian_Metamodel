# Interoperability

This directory contains semantic mapping resources to enable interoperability between the Triodian Metamodel and other enterprise architecture and industry-standard frameworks.

Each mapping is a JSON-LD file that aligns Triodian terminology with another framework, for integration, transformation and knowledge graph construction.

All mappings use one Triodian namespace, `https://triodian.com/ontology#` (prefix `triodian:`). `scripts/validate.py` checks that every mapping is valid JSON-LD and that every Triodian term it maps is a property, element type or domain defined in the schemas.

---

## Available mappings

| Framework                             | Context file                                        | Description                                                                 |
|---------------------------------------|-----------------------------------------------------|-----------------------------------------------------------------------------|
| BIAN (Banking Industry Architecture Network) | [triodian-bian.context.jsonld](triodian-bian.context.jsonld) | Maps BIAN service domains to Triodian domains                            |
| SAP Enterprise Architecture Framework | [triodian-sap.context.jsonld](triodian-sap.context.jsonld)   | States which SAP EA concepts correspond to each Triodian domain (`skos:closeMatch`)                       |
| FIBO (Financial Industry Business Ontology) | [triodian-FIBO.context.jsonld](triodian-FIBO.context.jsonld) | Aligns Triodian properties with formalised financial and regulatory semantics |

---

## BIAN mapping

### Overview
- **Format:** JSON-LD  
- **Purpose:** Enable semantic APIs, business architecture alignment, and integration with banking and enterprise models  
- **Compatibility:** BIAN, schema.org, FOAF, ArchiMate  
- **Version:** 1.0.0  
- **License:** Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)  
- **Context URI:** https://triodian.com/context/triodian-bian.jsonld  

### Domains
- `ServiceDomain` → `Capabilities`, `Services`, `Information`, `Products`
- `FunctionalPattern` → supports structural analysis of business functions
- `BusinessArea` → maps to Triodian `Organization` or `CapabilityGroup`

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
- **Context URI:** https://triodian.com/context/triodian-sap.jsonld  

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

The BIAN file is a JSON-LD context: reference it to interpret Triodian JSON as linked data. The SAP and FIBO files are JSON-LD graphs that state correspondences. For example, the SAP file states that `triodian:Capability` is a close match for `sap:BusinessCapability`:

```json
{
  "@id": "triodian:Capability",
  "rdfs:label": "Capability",
  "skos:closeMatch": [{ "@id": "sap:BusinessCapability" }, { "@id": "sap:Capability" }]
}
```

---

### FIBO (Financial Industry Business Ontology) interoperability

The Triodian Metamodel now includes schema-level mappings to the Financial Industry Business Ontology (FIBO), enabling integration with regulatory, financial, and compliance-focused enterprise data ecosystems. These mappings align core Triodian business architecture properties—such as `performanceIndicators`, `orgUnitTitle`, `strategicAlignment`, and `stakeholders`—to FIBO-standard properties used in semantic financial models.

#### Overview  
**Format:** JSON-LD  
**Purpose:** Support semantic APIs, enterprise graph alignment, and regulatory interoperability in financial services  
**Compatibility:** FIBO, Schema.org, FOAF, ArchiMate  
**Version:** 1.0.0  
**License:** Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)  
**Context URI:** [triodian-FIBO.context.jsonld](https://github.com/Triodian/Triodian_Metamodel/blob/main/interoperability/triodian-FIBO.context.jsonld)

#### Use cases  
- Integration with financial knowledge graphs and regulatory taxonomies  
- Enhanced traceability of strategic and operational alignment to financial KPIs  
- Cross-domain reasoning and compliance reporting using shared semantics

#### Corrections (October 2026)
- **Namespaces:** prefix IRIs no longer carry trailing spaces, and FIBO module IRIs use the published form `https://spec.edmcouncil.org/fibo/ontology/…`. `rdf:` is declared, so `rdf:Property` resolves.
- **Repointed to existing fields:** `hasParentOrgUnit` → `parentOrgUnitID`, `hasSubOrgUnit` → `subOrgUnitIDs`, `stakeholderRole` → `role`, `contactEmail` → `email`, `contactPhone` → `phone`, `capabilityMaturityLevel` → `maturityLevel`, `confidentialityClassification` → `dataClassification`, `riskLikelihood` → `riskProbability`, `mitigationControl` → `controls`, `serviceLevelAgreement` → `serviceLevelAgreements`, `deliveryChannel` → `channels`.
- **Removed:** the FIBO concepts below named Triodian fields that do not exist. Most describe financial instruments, accounts or transactions, which are operational data rather than business architecture. They are listed as candidates: add the field to a schema first, then restore the mapping.

| Proposed Triodian term | FIBO concept | Meaning |
|---|---|---|
| `accountHolder` | `fibo-fbc-fi-fi:hasAccountHolder` | The party that owns or holds the account. |
| `accountType` | `fibo-fbc-fi-fi:hasAccountType` | The type of financial account (e.g., checking, savings, brokerage). |
| `assetClass` | `fibo-fbc-fity-pty:hasAssetClass` | Classification of a financial instrument based on its nature. |
| `balance` | `fibo-fbc-fi-fi:hasBalance` | The current balance of a financial account. |
| `customerData` | `fibo-fbc-dae-dbt:CustomerAccountData` | Information pertaining to customer accounts. |
| `dataOwner` | `fibo-fnd-rel-rel:isOwnedBy` | The party responsible for the data. |
| `dataSteward` | `fibo-fnd-rel-rel:hasSteward` | The party responsible for the quality and governance of data. |
| `enforcedBy` | `fibo-fnd-agr-agr:hasPartyResponsibleForEnforcement` | The party responsible for enforcing the policy. |
| `expirationDate` | `fibo-fnd-dt-fd:hasExpirationDate` | Date when an entity or agreement ceases to be effective. |
| `hasSourceSystem` | `fibo-fnd-agr-agr:isProducedBy` | System that originates or produces information. |
| `incorporationDate` | `fibo-be-le-fbo:dateOfFormation` | Date an organization was legally formed. |
| `industryAnalysis` | `fibo-ind-ei-ei:hasMarketInsight` | Aggregated market intelligence |
| `initiativeScope` | `fibo-fnd-agr-agr:appliesTo` | The range or extent of an initiative. |
| `jurisdictionOfEstablishment` | `fibo-fnd-plc-loc:hasJurisdiction` | Legal jurisdiction where the organization is established. |
| `legalName` | `fibo-be-le-fbo:hasLegalName` | Formal legal name of an organization. |
| `marketQuote` | `fibo-fbc-mc-mkt:MarketQuote` | Information about the price or value of a security or commodity. |
| `maturityDate` | `fibo-fbc-fity-trm:hasMaturityDate` | The date on which a financial instrument matures. |
| `policyScope` | `fibo-fnd-agr-agr:appliesTo` | The range or extent to which a policy applies. |
| `progressStatus` | `fibo-fnd-utl-av:hasStatus` | Current progress state of an initiative. |
| `registeredAddress` | `fibo-fnd-plc-loc:hasPhysicalAddress` | Official physical address for an organization. |
| `requiredResource` | `fibo-fnd-agr-agr:requires` | Resource required for a capability. |
| `transactionAmount` | `fibo-fnd-acc-cur:hasMonetaryAmount` | The monetary value of a financial transaction. |
| `transactionDate` | `fibo-fnd-dt-fd:hasTransactionDate` | The date when a financial transaction occurred. |
| `transactionType` | `fibo-fbc-finc-finc:hasTransactionType` | The nature or category of a financial transaction. |
| `uniqueId` | `fibo-fnd-utl-av:hasTag` | General unique identifier for any entity, analogous to a tag or identifier. |

