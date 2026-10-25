# Semantic library worked example: the advice boundary

This example shows how the semantic library schemas connect an AI control to the business architecture around it, using a superannuation fund's member-services assistant. The assistant may give members factual information and general advice, but the fund's member channels are not authorised to give personal advice.

**Everything here is illustrative.** The fund, identifiers, people, dates, thresholds and harness results are invented to show the shape of the records. No calibration has been run, and the obligation statements summarise the cited provisions for the example; they are not legal advice and should be checked against the current instruments before use.

The records:

1. Two **obligations** captured at clause level: the personal-advice boundary and the general advice warning.
2. The **AI system** they govern, as a Model Risk Management model profile, which doubles as the entry in the AI use-case inventory.
3. Two **semantic constraints**, produced by splitting one requirement across tiers:
   - a semantic-tier constraint that decides what kind of statement the assistant made;
   - a rules-tier constraint that checks the mandated warning is present when the statement is general advice.
4. A **trigger** recording a change to a source instrument, which identifies the obligations, and through them the constraints, that need review.

Every block is validated against its schema by `scripts/validate.py`.

## 1. Obligations

The personal-advice boundary. Whether a response is personal advice depends on what it means, not on its wording, so it will be enforced in the semantic tier.

```json semantic-library/obligation.schema.json
{
  "obligationID": "OBL-001",
  "title": "No personal advice through unauthorised member channels",
  "statement": "Member channels operating without a personal-advice authorisation must not give personal advice: a recommendation or opinion that takes into account the member's objectives, financial situation or needs.",
  "obligationType": "statutory",
  "source": {
    "authority": "Commonwealth Parliament; administered by ASIC",
    "instrument": "Corporations Act 2001 (Cth)",
    "citation": "s766B(3) (personal advice); s911A (need for a licence)",
    "url": "https://www.legislation.gov.au/C2004A00818/latest"
  },
  "jurisdiction": "AU",
  "status": "inForce",
  "appliesTo": [
    { "domainType": "channel", "entityID": "CH-MEMBER-CHAT", "title": "Member services chat" },
    { "domainType": "product", "entityID": "PROD-ACCUM", "title": "Accumulation account" }
  ],
  "implementingPolicyIDs": ["POL-ADVICE-001"],
  "orgUnitTitle": "Member Advice",
  "orgUnitID": "OU-ADVICE",
  "accountablePerson": "Chief Member Officer (accountable person)",
  "riskLevel": "critical",
  "complianceStatus": "underReview",
  "relatedObligationIDs": ["OBL-002"],
  "monitoringFrequency": "monthly",
  "lastReviewDate": "2026-10-01"
}
```

The general advice warning. Once a response is known to be general advice, whether it carries the warning can be decided from the text alone, so this part belongs in the rules tier.

```json semantic-library/obligation.schema.json
{
  "obligationID": "OBL-002",
  "title": "General advice warning",
  "statement": "When general advice is given to a retail client, warn the client that the advice does not take into account their objectives, financial situation or needs.",
  "obligationType": "statutory",
  "source": {
    "authority": "Commonwealth Parliament; administered by ASIC",
    "instrument": "Corporations Act 2001 (Cth)",
    "citation": "s949A"
  },
  "jurisdiction": "AU",
  "status": "inForce",
  "appliesTo": [
    { "domainType": "channel", "entityID": "CH-MEMBER-CHAT", "title": "Member services chat" }
  ],
  "implementingPolicyIDs": ["POL-ADVICE-001"],
  "orgUnitTitle": "Member Advice",
  "orgUnitID": "OU-ADVICE",
  "riskLevel": "high",
  "relatedObligationIDs": ["OBL-001"]
}
```

## 2. The governed AI system

The model profile from Model Risk Management records the assistant in the AI use-case inventory: who owns it, what it supports, and where it is in its lifecycle.

```json model-risk-management.schema.json
{
  "modelID": "MODEL-CHAT-001",
  "title": "Member services assistant",
  "description": "Large language model assistant answering member questions in the member services chat channel",
  "modelType": "generativeAI/conversationalAssistant",
  "useCategory": "memberServices",
  "orgUnitTitle": "Member Services",
  "orgUnitID": "OU-MEMSVC",
  "modelOwner": "Head of Member Services",
  "regulatoryRelevance": ["Corporations Act s766B", "Corporations Act s949A", "CPS 230"],
  "businessCriticality": "C1",
  "status": "underValidation",
  "supportsCapabilities": ["Member enquiry handling"],
  "supportsCapabilityIDs": ["CAP-MEMBER-ENQ"]
}
```

## 3. Semantic constraints

### The advice-boundary envelope (semantic tier)

A graded-severity constraint: the ladder runs from factual information to personal advice, and each rung has its own disposition. The borderline rung escalates to a human rather than guessing, because it is where qualified people disagree.

```json semantic-library/semantic-constraint.schema.json
{
  "semanticConstraintID": "SC-001",
  "title": "Advice boundary for member chat",
  "statement": "The member services assistant must not make a recommendation or state an opinion that takes into account the member's objectives, financial situation or needs.",
  "constraintType": "gradedSeverity",
  "obligationMappings": [
    { "obligationID": "OBL-001", "mappingRole": "primary" }
  ],
  "enforcementTier": "semanticTier",
  "tierRationale": "Whether a response is personal advice depends on its meaning: two responses with identical form can differ in whether they consider the member's circumstances. A keyword list would be evaded by paraphrase.",
  "appliesTo": [
    { "domainType": "channel", "entityID": "CH-MEMBER-CHAT", "title": "Member services chat" },
    { "domainType": "valueStream", "entityID": "VS-MEMBER-ENQ", "title": "Resolve member enquiry" }
  ],
  "governedModelIDs": ["MODEL-CHAT-001"],
  "severityScale": [
    { "level": 0, "label": "Factual information", "description": "States facts about the fund, products or rules without recommending anything", "disposition": "allow" },
    { "level": 1, "label": "General advice", "description": "Recommends or gives an opinion without reference to the member's own circumstances", "disposition": "allowWithControl" },
    { "level": 2, "label": "Borderline", "description": "General advice framed around details the member has shared, where it is unclear whether their circumstances were taken into account", "disposition": "escalate" },
    { "level": 3, "label": "Personal advice", "description": "Recommends a course of action for this member based on their objectives, financial situation or needs", "disposition": "block" }
  ],
  "contestedDisposition": "abstainAndEscalate",
  "exemplarSets": [
    { "exemplarSetID": "EXS-001-CAN", "setType": "canonical", "itemCount": 240, "version": "1.0", "location": "library/advice-boundary/canonical", "provenance": "Written by the advice team against s766B and the fund's advice policy; each item labelled with a severity level" },
    { "exemplarSetID": "EXS-001-ADV", "setType": "adversarial", "itemCount": 600, "version": "1.0", "location": "library/advice-boundary/adversarial", "provenance": "Paraphrase red-team runs" },
    { "exemplarSetID": "EXS-001-CAL", "setType": "calibration", "itemCount": 1500, "version": "1.0", "location": "library/advice-boundary/calibration", "provenance": "Labelled sample of historical chat transcripts" }
  ],
  "semanticEnvelope": {
    "embeddingModel": { "modelName": "example-embedding-model", "modelVersion": "2026-06" },
    "methodologyVersion": "PACE 2.0",
    "divergenceMetric": "cosine",
    "threshold": 0.31,
    "alpha": 0.05,
    "calibrationDate": "2026-10-15",
    "validation": {
      "validatedDate": "2026-10-16",
      "passed": true,
      "separationAUC": 0.94,
      "recall": 0.95,
      "falsePositiveRate": 0.04,
      "monotonicityPassed": true,
      "beatsBaseline": true,
      "shiftRobustnessPassed": true,
      "leakagePassed": true,
      "evidenceLocation": "library/advice-boundary/evidence/2026-10-16"
    }
  },
  "stewardship": {
    "policyOwner": "Head of Advice",
    "policyOwnerOrgUnitID": "OU-ADVICE",
    "author": "Semantic librarian, Member Advice",
    "calibrator": "Model validation analyst",
    "approver": "Editorial board chair"
  },
  "monitoring": {
    "monitoringFrequency": "weekly",
    "coverageFloor": 0.95,
    "reviewTriggers": ["coverageDegradation", "guaranteeInvalidation", "suspectedLeakage", "obligationChange", "modelChange", "novelCasePromotion", "incidentAdjudication"]
  },
  "status": "validated",
  "version": "1.0.0",
  "relatedConstraintIDs": ["SC-002"]
}
```

### The general advice warning (rules tier)

The other half of the split. SC-001 decides that a response is general advice (level 1); this constraint then checks, from the text alone, that the warning is there. It is still a draft, so it has no conformance result yet.

```json semantic-library/semantic-constraint.schema.json
{
  "semanticConstraintID": "SC-002",
  "title": "General advice warning present",
  "statement": "A response classified as general advice must include the fund's approved general advice warning.",
  "constraintType": "requiredProperty",
  "obligationMappings": [
    { "obligationID": "OBL-002", "mappingRole": "primary" }
  ],
  "enforcementTier": "rulesTier",
  "tierRationale": "Once the response is classified as general advice, the presence of the approved warning is decidable from the text alone.",
  "splitFromConstraintID": "SC-001",
  "appliesTo": [
    { "domainType": "channel", "entityID": "CH-MEMBER-CHAT", "title": "Member services chat" }
  ],
  "governedModelIDs": ["MODEL-CHAT-001"],
  "exemplarSets": [
    { "exemplarSetID": "EXS-002-ACC", "setType": "mustAccept", "itemCount": 120, "location": "library/general-advice-warning/must-accept", "provenance": "Approved warning wordings in context" },
    { "exemplarSetID": "EXS-002-REJ", "setType": "mustReject", "itemCount": 80, "location": "library/general-advice-warning/must-reject", "provenance": "Truncated, reworded and missing warnings" }
  ],
  "grammarArtifact": {
    "formalism": "regularExpression",
    "artifactLocation": "library/general-advice-warning/warning.regex",
    "artifactVersion": "0.1",
    "methodologyVersion": "GRACE 0.1"
  },
  "stewardship": {
    "policyOwner": "Head of Advice",
    "policyOwnerOrgUnitID": "OU-ADVICE",
    "author": "Semantic librarian, Member Advice"
  },
  "status": "draft",
  "version": "0.1.0",
  "relatedConstraintIDs": ["SC-001"]
}
```

## 4. When a source changes

A regulatory watch records a change to a source instrument as a trigger in the Strategic Response Model. Its affected entities name the obligations; each constraint's `obligationMappings` then identifies which constraints to review, and the constraints' `reviewTriggers` include `obligationChange`.

```json trigger.schema.json
{
  "triggerID": "TRG-101",
  "label": "Regulator updates guidance on general and personal advice",
  "description": "Updated regulatory guidance changes the examples of where general advice becomes personal advice in digital channels",
  "primaryCategory": "regulatoryCompliance",
  "subCategory": "Advice guidance",
  "origin": "External",
  "timeHorizon": "shortTerm",
  "impactLevel": "high",
  "detectionMethod": "Regulatory watch",
  "detectionDate": "2026-10-20",
  "affectedEntities": [
    { "domainType": "obligation", "entityID": "OBL-001", "title": "No personal advice through unauthorised member channels" },
    { "domainType": "obligation", "entityID": "OBL-002", "title": "General advice warning" }
  ]
}
```

## What the links give you

| Question | Answered by |
| --- | --- |
| Which obligations does the assistant's chat channel carry? | Obligations whose `appliesTo` names `CH-MEMBER-CHAT` |
| Which control is primary for an obligation, and is there exactly one? | Constraints whose `obligationMappings` name it with `mappingRole: primary` |
| Why is this constraint enforced by meaning rather than by rule? | `enforcementTier` and `tierRationale` |
| Which AI systems does a constraint govern, and who owns them? | `governedModelIDs` → Model Risk Management model profiles |
| Which constraints need review after a source changes? | Trigger `affectedEntities` → obligations → constraints that map to them |
| Is the calibration still valid for the model in use? | `semanticEnvelope.embeddingModel` and `calibrationDate`, against the deployed model |
| Who wrote it, and who approved it? | `stewardship`; a published constraint must name an approver |
