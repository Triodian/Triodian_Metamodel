# Worked example: an AI obligations register

This example shows how the Metamodel represents a reference dataset of AI governance obligations, such as a register a firm or regulator might publish:
- regulators and standards bodies;
- clause-level obligations tagged by source tier;
- the standardised use cases those obligations may reach;
- the sources watched for change;
- the instrument changes found.

It also shows how an organization's own compliance records point back to the obligations.

**The obligation, use case, data flow and trigger records summarise sources as they stood on 27 October 2026, and have not been reviewed.** The compliance requirement and the disclosure are illustrative. None of this is legal advice. A source tier describes the source, never whether any organization meets it.

Every block is validated against its schema by `scripts/validate.py`.

## 1. The regulator

```json external-organization.schema.json
{
  "externalOrgID": "EXT-APRA",
  "name": "Australian Prudential Regulation Authority",
  "acronym": "APRA",
  "type": "regulator",
  "jurisdiction": "AU",
  "jurisdictionCodes": [
    "AU"
  ],
  "remit": "Prudential regulation of authorised deposit-taking institutions, general, life and private health insurers, and superannuation trustees",
  "website": "https://www.apra.gov.au",
  "monitoredSourceDataFlowIDs": [
    "DF-APRA-02",
    "DF-APRA-03"
  ]
}
```

## 2. Obligations

A binding prudential standard, captured at paragraph level:

```json semantic-library/obligation.schema.json
{
  "obligationID": "OBL-AU-CPS230-47",
  "title": "Service provider management policy and material service providers",
  "statement": "CPS 230 para 47 requires a comprehensive service provider management policy; para 49 defines material service providers as those on which the entity relies to undertake a critical operation or that expose it to material operational risk; and para 50 lists providers that must at a minimum be classified as material, including providers of core technology services, risk management and internal audit, plus industry-specific categories.",
  "obligationType": "prudentialStandard",
  "source": {
    "authority": "APRA",
    "instrument": "Prudential Standard CPS 230 Operational Risk Management",
    "citation": "paras 47, 49, 50",
    "url": "https://www.apra.gov.au/standards/cps-230",
    "externalOrgID": "EXT-APRA"
  },
  "jurisdiction": "AU",
  "sourceTier": "binding",
  "entityTypes": [
    "authorisedDepositTakingInstitution",
    "generalInsurer",
    "lifeInsurer",
    "privateHealthInsurer",
    "superannuationTrustee"
  ],
  "roles": [
    "regulatedEntity",
    "serviceProvider"
  ],
  "useCaseIDs": [
    "UC7",
    "UC1",
    "UC8",
    "UC9"
  ],
  "effectiveDate": "2025-07-01",
  "effectiveDates": [
    {
      "dateType": "commences",
      "date": "2025-07-01",
      "note": "Original CPS 230 (Determination No. 2 of 2023), para 6"
    },
    {
      "dateType": "transitionEnds",
      "date": "2026-07-01",
      "note": "Para 7: service provider requirements apply to pre-existing contracts from the earlier of next renewal or 1 July 2026"
    },
    {
      "dateType": "made",
      "date": "2026-04-29",
      "note": "CPS 230 remade by Banking, Insurance, Life Insurance, Health Insurance and Superannuation (prudential standard) determination No. 1 of 2026 (F2026L00475), adding a limited exemption from certain contractual requirements for specified non-traditional service providers"
    },
    {
      "dateType": "commences",
      "date": "2026-07-01",
      "note": "Remade CPS 230 commences 1 July 2026 (APRA final targeted amendments release, 30 April 2026)"
    }
  ],
  "status": "inForce",
  "monitoringFrequency": "daily",
  "lastVerified": "2026-10-27"
}
```

A regulator's expectation. Its second tier comes through `tierBasis`, where it rests on the binding standards. This mapping is the dataset's own, and the note says so:

```json semantic-library/obligation.schema.json
{
  "obligationID": "OBL-AU-APRA-AI-02",
  "title": "Board-overseen AI strategy within risk appetite, with defined triggers",
  "statement": "The letter expects Boards, at a minimum, to oversee an AI strategy 'consistent with the entity's risk appetite and tolerance settings', including oversight of third-party dependencies, 'with clearly defined triggers aligned to resilience objectives to enable timely action when not operating as expected'.",
  "obligationType": "regulatoryGuidance",
  "source": {
    "authority": "APRA",
    "instrument": "APRA Letter to Industry on Artificial Intelligence (AI)",
    "citation": "Letter, Boards expectations, second bullet",
    "url": "https://www.apra.gov.au/news-and-publications/apra-letter-industry-artificial-intelligence-ai",
    "externalOrgID": "EXT-APRA"
  },
  "jurisdiction": "AU",
  "sourceTier": "expected",
  "tierBasis": [
    {
      "obligationID": "OBL-AU-CPS220-9",
      "sourceTier": "binding",
      "note": "Publisher's mapping; the letter does not cite this standard by number"
    },
    {
      "obligationID": "OBL-AU-CPS220-23",
      "sourceTier": "binding",
      "note": "Publisher's mapping; the letter does not cite this standard by number"
    },
    {
      "obligationID": "OBL-AU-CPS230-35",
      "sourceTier": "binding",
      "note": "Publisher's mapping; the letter does not cite this standard by number"
    }
  ],
  "entityTypes": [
    "authorisedDepositTakingInstitution",
    "generalInsurer",
    "lifeInsurer",
    "privateHealthInsurer",
    "superannuationTrustee"
  ],
  "roles": [
    "board"
  ],
  "useCaseIDs": [
    "UC1",
    "UC2",
    "UC3",
    "UC4",
    "UC5",
    "UC6",
    "UC7",
    "UC8",
    "UC9",
    "UC10"
  ],
  "effectiveDates": [
    {
      "dateType": "published",
      "date": "2026-04-30",
      "note": "Letter and media release published 30 April 2026; signed by Therese McCarthy Hockey, Member"
    }
  ],
  "status": "inForce",
  "monitoringFrequency": "daily",
  "lastVerified": "2026-10-27"
}
```

An anticipated provision: made, but not yet in force. The record gives its commencement date, never a likelihood that it will apply:

```json semantic-library/obligation.schema.json
{
  "obligationID": "OBL-AU-PRIVACY-APP1-7",
  "title": "Privacy policy disclosure of automated decisions (APP 1.7-1.9)",
  "statement": "APP 1.7 provides that an APP entity's privacy policy must contain the APP 1.8 information where the entity has arranged for a computer program to make, or do a thing substantially and directly related to making, a decision that could reasonably be expected to significantly affect the rights or interests of an individual, using personal information about the individual. APP 1.8 requires the policy to describe the kinds of personal information used and the kinds of decisions made solely by, or substantially assisted by, such programs; APP 1.9 provides that making a decision includes refusing or failing to make one.",
  "obligationType": "statutory",
  "source": {
    "authority": "Commonwealth Parliament; administered by OAIC",
    "instrument": "Privacy Act 1988 (Cth), Schedule 1 (APPs), as amended by the Privacy and Other Legislation Amendment Act 2024",
    "citation": "APP 1.7, 1.8, 1.9 (inserted by POLA Act 2024 Sch 1 Part 15, item 88; application item 89)",
    "url": "https://legislation.gov.au/C2024A00128/asmade/2024-12-10/text/original/epub/OEBPS/document_1/document_1.html",
    "externalOrgID": "EXT-OAIC"
  },
  "jurisdiction": "AU",
  "sourceTier": "anticipated",
  "entityTypes": [
    "anyOrganization"
  ],
  "roles": [
    "regulatedEntity",
    "deployer"
  ],
  "useCaseIDs": [
    "UC2",
    "UC3",
    "UC4",
    "UC5",
    "UC8"
  ],
  "effectiveDate": "2026-12-10",
  "effectiveDates": [
    {
      "dateType": "made",
      "date": "2024-12-10",
      "note": "Royal Assent"
    },
    {
      "dateType": "commences",
      "date": "2026-12-10",
      "note": "Sch 1 Part 15 commences the day after 24 months from Royal Assent (s 2 table item 7)"
    },
    {
      "dateType": "applies",
      "date": "2026-12-10",
      "note": "Item 89: applies to decisions made after commencement, regardless of when the program was arranged or the information collected"
    }
  ],
  "status": "pending",
  "monitoringFrequency": "daily",
  "lastVerified": "2026-10-27"
}
```

## 3. A standardised use case

The obligations above point to use cases such as UC7 through `useCaseIDs`. The ten standard use cases are in [`reference-data/use-cases.json`](../reference-data/use-cases.json).

```json use-case.schema.json
{
  "useCaseID": "UC7",
  "title": "AI inside a provider or the platform behind it",
  "description": "AI used by a service provider, or by the platform the provider relies on, in delivering a service to the organization.",
  "authorityLevels": [
    "a1Productivity",
    "a2Analytical",
    "a3Decision",
    "a4Transactional",
    "a5Agentic",
    "a6Actuation"
  ],
  "anyAuthorityLevel": true,
  "boundaries": [
    "b1",
    "b2"
  ],
  "assessmentTypes": [
    "aiUseAssessment"
  ],
  "examples": [
    "A provider's claims platform that uses AI",
    "A cloud platform's AI features inside an outsourced service"
  ],
  "version": "1.0"
}
```

## 4. A monitored source

The update agent watches each source as a data flow, with its precedence. A rank 1 or 2 source can set a status or date, subject to review; a lower-ranked source is only a lead to an official one.

```json extensions/dynamic-time-series/data-flow.schema.json
{
  "dataFlowID": "DF-APRA-03",
  "title": "Watch: APRA News and publications",
  "description": "Letters to industry, media releases, consultations. RSS availability not verified",
  "sourceSystems": [
    {
      "endpointType": "webPage",
      "title": "APRA News and publications",
      "url": "https://www.apra.gov.au/news-and-publications"
    }
  ],
  "targetSystems": [
    {
      "endpointType": "software",
      "title": "Register update agent"
    }
  ],
  "frequency": "daily",
  "schemaReference": {
    "format": "html"
  },
  "sourcePrecedence": {
    "rank": 2,
    "basis": "regulatorPublication",
    "canSetStatusOrDate": true
  },
  "externalOrgID": "EXT-APRA",
  "jurisdiction": "AU",
  "governance": {
    "ownerTitle": "Method owner",
    "humanApprovalRequired": true
  },
  "status": "planned"
}
```

## 5. An instrument change

```json trigger.schema.json
{
  "triggerID": "TRG-SG-MAS-AIRM-2026-10-07",
  "label": "MAS issues Guidelines on AI Risk Management",
  "description": "MAS issued its Guidelines on Artificial Intelligence Risk Management on 7 October 2026. They take effect on 7 October 2027; sections 3 and 4 from that date, and sections 5 and 6 by 7 October 2028.",
  "primaryCategory": "regulatoryCompliance",
  "subCategory": "AI governance instrument",
  "origin": "External",
  "timeHorizon": "shortTerm",
  "status": "identified",
  "detectionMethod": "Source research",
  "evidenceStrength": 5,
  "detectionDate": "2026-10-07",
  "sourceReference": "https://www.mas.gov.sg/-/media/mas-media-library/regulation/guidelines/bd/guidelines-on-artificial-intelligence-risk-management-for-financial-institutions/guidelines-on-artificial-intelligence-risk-management.pdf",
  "instrumentChange": {
    "instrument": "MAS Guidelines on Artificial Intelligence Risk Management",
    "changeType": "newInstrument",
    "jurisdiction": "SG",
    "externalOrgID": "EXT-MAS",
    "sourceURL": "https://www.mas.gov.sg/-/media/mas-media-library/regulation/guidelines/bd/guidelines-on-artificial-intelligence-risk-management-for-financial-institutions/guidelines-on-artificial-intelligence-risk-management.pdf",
    "sourceRank": 1,
    "publishedDate": "2026-10-07",
    "effectiveDate": "2027-10-07",
    "summary": "New guidelines; consultation P017-2025 closed 31 January 2026"
  },
  "affectedEntities": [
    {
      "domainType": "obligation",
      "entityID": "OBL-SG-MAS-AIRM-3",
      "title": "Board and senior management oversight of AI risk"
    },
    {
      "domainType": "obligation",
      "entityID": "OBL-SG-MAS-AIRM-4-1",
      "title": "AI identification and AI inventory"
    },
    {
      "domainType": "obligation",
      "entityID": "OBL-SG-MAS-AIRM-4-10",
      "title": "AI risk materiality assessment (impact, complexity, reliance)"
    },
    {
      "domainType": "obligation",
      "entityID": "OBL-SG-MAS-AIRM-5-4",
      "title": "Data management, transparency/explainability and fairness controls"
    },
    {
      "domainType": "obligation",
      "entityID": "OBL-SG-MAS-AIRM-5-9",
      "title": "Human oversight proportionate to risk materiality"
    },
    {
      "domainType": "obligation",
      "entityID": "OBL-SG-MAS-AIRM-5-10",
      "title": "Third-party AI: FI retains primary accountability"
    },
    {
      "domainType": "obligation",
      "entityID": "OBL-SG-MAS-AIRM-5-15",
      "title": "Guardrails, testing and secure deployment incl. generative AI and agents"
    },
    {
      "domainType": "obligation",
      "entityID": "OBL-SG-MAS-AIRM-5-23",
      "title": "Post-deployment monitoring and change management"
    },
    {
      "domainType": "obligation",
      "entityID": "OBL-SG-MAS-AIRM-6",
      "title": "AI risk management capability and technology infrastructure"
    }
  ]
}
```

## 6. An organization's own records

An organization that uses the register links its own compliance records to its obligations. The compliance requirement is made up of obligations rather than restating them, and the disclosure names the obligation that calls for it. Both are illustrative.

```json compliance/compliance-requirement.schema.json
{
  "complianceRequirementID": "CREQ-AU-CPS230-MSP",
  "title": "Material service provider management (CPS 230)",
  "description": "The CPS 230 requirements for managing service providers, assessed together in an internal audit of third-party AI.",
  "source": {
    "instrument": "Prudential Standard CPS 230 Operational Risk Management",
    "citation": "paras 47-54, 59",
    "url": "https://www.apra.gov.au/standards/cps-230"
  },
  "regulatoryBodyExternalOrgID": "EXT-APRA",
  "regulatoryBodyTitle": "Australian Prudential Regulation Authority",
  "jurisdiction": "AU",
  "validityPeriod": {
    "startDate": "2025-07-01"
  },
  "status": "inForce",
  "obligationIDs": [
    "OBL-AU-CPS230-47",
    "OBL-AU-CPS230-54"
  ],
  "implementingPolicyIDs": [
    "POL-TPRM-001"
  ],
  "reviewFrequency": "annually"
}
```

```json public-reporting/mandatory-disclosure.schema.json
{
  "mandatoryDisclosureID": "DISC-ADM-PRIVACY-POLICY",
  "title": "Automated decisions in the privacy policy",
  "description": "From 10 December 2026, APP 1.7 and 1.8 provide that an APP entity's privacy policy describes the kinds of personal information used, and the kinds of decisions made, by computer programs in decisions that could significantly affect individuals.",
  "disclosureChannel": "privacyPolicy",
  "obligationIDs": [
    "OBL-AU-PRIVACY-APP1-7"
  ],
  "useCaseIDs": [
    "UC3",
    "UC4",
    "UC8"
  ],
  "stakeholderTitle": "Privacy Officer",
  "frequency": "annually"
}
```

## Governing the records

A governing service can hold records like these through the [governance interface](../governance-interface/README.md), under a dataset policy such as the [example regulatory register policy](../governance-interface/example-policies/regulatory-register.policy.json). Under that policy, each create, status, date or tier change waits for a named reviewer. The published version then carries its approver and a hash-chained provenance trail.
