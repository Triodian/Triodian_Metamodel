# Examples of Trigger and Rationale Links

This page provides examples of how Triggers and Rationales are used within the Triodian Metamodel to document the drivers of change and the justification for responses across different business domains.

Each example includes:

- A specific Trigger (external or internal)
- The Rationale for responding
- The Affected Domain(s)
- A sample JSON structure linking the trigger to a rationale, in the Strategic Response Model's composite form (`triggers` and `rationales` lists), checked against `strategic-response-model.schema.json` by `scripts/validate.py`

---

## Example 1: Regulatory change triggering a policy update

### Trigger:
A new data protection regulation is enacted by the government.

### Affected Domain:
- Policy: Update existing data handling policies to comply with the new regulation.

### Rationale:
To ensure compliance with legal requirements and avoid potential penalties.

### JSON representation:

```json strategic-response-model.schema.json
{
  "triggers": [
    {
      "triggerID": "TRG-001",
      "label": "New Data Protection Regulation",
      "description": "Enactment of new data protection regulation requiring updated data handling practices",
      "primaryCategory": "regulatoryCompliance",
      "origin": "External",
      "timeHorizon": "shortTerm",
      "impactLevel": "high",
      "status": "Ongoing",
      "detectionDate": "2025-03-15",
      "validUntil": "2030-03-15",
      "sourceReference": "Government Gazette Notice 2025-112"
    }
  ],
  "rationales": [
    {
      "rationaleID": "RAT-001",
      "rationaleTitle": "Data Protection Compliance Initiative",
      "description": "Align policies with new legal requirements to ensure compliance and protect customer data",
      "triggerReference": "TRG-001",
      "linkedDomains": [
        "policy",
        "information"
      ],
      "rationaleType": "complianceFulfillment",
      "rationaleOrientation": "reactive",
      "evidenceBase": "externalResearch",
      "businessValueType": "riskReduction",
      "dateCreated": "2025-03-20",
      "lastReviewed": "2025-03-20",
      "author": "Legal Compliance Team",
      "orgUnitTitle": "Legal Department"
    }
  ]
}
```

## Example 2: Market trend influencing strategy

### Trigger:
Emerging trend of remote work adoption in the industry.

### Affected Domain:
- Strategy: Develop initiatives to support remote work infrastructure.
- Capabilities: Enhance digital collaboration tools and virtual management practices.

### Rationale:
To stay competitive, meet the evolving needs of the workforce, and attract top talent through flexible work arrangements.

### JSON representation:

```json strategic-response-model.schema.json
{
  "triggers": [
    {
      "triggerID": "TRG-002",
      "label": "Remote Work Adoption Trend",
      "description": "Significant increase in remote work adoption across the industry, accelerated by technological advancements and workforce preferences",
      "primaryCategory": "workforceSkills",
      "subCategory": "Strategic Repositioning",
      "origin": "External",
      "timeHorizon": "mediumTerm",
      "impactLevel": "high",
      "status": "Emerging",
      "detectionDate": "2025-01-10",
      "sourceReference": "Industry Workforce Report Q1 2025"
    }
  ],
  "rationales": [
    {
      "rationaleID": "RAT-002",
      "rationaleTitle": "Remote Work Strategy Implementation",
      "description": "Adapt organizational strategy to accommodate remote work capabilities to attract and retain talent while maintaining operational effectiveness",
      "triggerReference": "TRG-002",
      "linkedDomains": [
        "strategy",
        "capability",
        "people"
      ],
      "rationaleType": "strategicAdvancement",
      "rationaleOrientation": "proactive",
      "anticipatedOutcomes": [
        "Improved talent acquisition and retention",
        "Reduced office space costs",
        "Enhanced employee satisfaction",
        "Access to global talent pool"
      ],
      "reasoningPattern": "predictive",
      "evidenceBase": "industryBestPractice",
      "businessValueType": "competitiveAdvantage",
      "competitivePositioning": {
        "positioningType": "differentiation",
        "positioningDescription": "Position the organization as an employer of choice through advanced remote work capabilities",
        "competitiveTarget": "Technology talent market segment"
      },
      "dateCreated": "2025-02-01",
      "lastReviewed": "2025-04-15",
      "effectivenessRating": 4,
      "author": "HR Strategy Team",
      "orgUnitTitle": "Human Resources"
    }
  ]
}
```

## Example 3: Internal performance issue leading to capability enhancement

### Trigger:
Customer service response times have increased beyond acceptable thresholds.

### Affected Domain:
- Capabilities: Enhance customer service processes and training.
- Performance: Implement new metrics and monitoring systems.

### Rationale:
To improve customer satisfaction, reduce churn rates, and strengthen brand reputation in an increasingly competitive market.

### JSON representation:

```json strategic-response-model.schema.json
{
  "triggers": [
    {
      "triggerID": "TRG-003",
      "label": "Customer Service Response Degradation",
      "description": "Customer service response times have increased by 35% over the past quarter, exceeding acceptable thresholds and impacting customer satisfaction metrics",
      "primaryCategory": "performanceResponse",
      "subCategory": "Capability Enhancement",
      "origin": "Internal",
      "timeHorizon": "immediate",
      "impactLevel": "critical",
      "status": "Ongoing",
      "detectionDate": "2025-03-01",
      "sourceReference": "Q1 2025 Customer Service Performance Report"
    }
  ],
  "rationales": [
    {
      "rationaleID": "RAT-003",
      "rationaleTitle": "Customer Service Improvement Initiative",
      "description": "Address service quality degradation through process improvements, staff training, and technology enhancements to restore customer satisfaction levels",
      "triggerReference": "TRG-003",
      "linkedDomains": [
        "capability",
        "performance",
        "service"
      ],
      "rationaleType": "remedial",
      "rationaleOrientation": "reactive",
      "reasoningPattern": "causal",
      "evidenceBase": "dataDriven",
      "businessValueType": "customerExperience",
      "dateCreated": "2025-03-10",
      "lastReviewed": "2025-04-01",
      "effectivenessRating": 3,
      "author": "Customer Experience Team",
      "orgUnitTitle": "Customer Support Department",
      "alternativesConsidered": [
        {
          "alternativeID": "ALT-001",
          "alternativeDescription": "Outsource customer service operations to third-party provider",
          "reasonForRejection": "Would reduce control over customer experience and risk further brand damage"
        },
        {
          "alternativeID": "ALT-002",
          "alternativeDescription": "Implement chatbot-only first-level support",
          "reasonForRejection": "Technology not mature enough to handle complex customer issues"
        }
      ]
    }
  ]
}
```

## Example 4: Technological innovation creating strategic opportunity

### Trigger:
Emergence of advanced AI-powered predictive analytics capabilities in the market.

### Affected Domain:
- Strategy: Develop AI adoption roadmap
- Capabilities: Build data science expertise
- Products: Create AI-enhanced product offerings

### Rationale:
To leverage emerging technology for competitive advantage and create new revenue streams through enhanced product capabilities.

### JSON representation:

```json strategic-response-model.schema.json
{
  "triggers": [
    {
      "triggerID": "TRG-004",
      "label": "AI Predictive Analytics Advancements",
      "description": "Significant advancements in AI-powered predictive analytics creating new opportunities for product enhancement and market differentiation",
      "primaryCategory": "technologicalChange",
      "subCategory": "Innovation Initiative",
      "origin": "External",
      "timeHorizon": "mediumTerm",
      "impactLevel": "high",
      "status": "Emerging",
      "detectionDate": "2025-02-15",
      "sourceReference": "Technology Trend Report Q1 2025"
    }
  ],
  "rationales": [
    {
      "rationaleID": "RAT-004",
      "rationaleTitle": "AI-Driven Product Innovation Strategy",
      "description": "Integrate advanced AI capabilities into our product suite to create differentiated offerings and new revenue streams while establishing market leadership in predictive analytics",
      "triggerReference": "TRG-004",
      "linkedDomains": [
        "strategy",
        "product",
        "capability"
      ],
      "rationaleType": "opportunistic",
      "rationaleOrientation": "proactive",
      "anticipatedOutcomes": [
        "20% premium pricing on AI-enhanced products",
        "Expansion into adjacent markets",
        "Development of recurring revenue streams",
        "Establishment of thought leadership position"
      ],
      "reasoningPattern": "predictive",
      "evidenceBase": "competitiveAnalysis",
      "strategicObjectiveReference": "OBJ-001",
      "businessValueType": "marketCreation",
      "competitivePositioning": {
        "positioningType": "innovationLeadership",
        "positioningDescription": "Establish first-mover advantage in AI-enhanced product category",
        "competitiveTarget": "Enterprise analytics market segment"
      },
      "dateCreated": "2025-02-28",
      "lastReviewed": "2025-03-15",
      "effectivenessRating": 5,
      "author": "Innovation Strategy Team",
      "orgUnitTitle": "Product Development"
    }
  ]
}
```

## Example 5: Environmental sustainability pressure requiring operational transformation

### Trigger:
Increasing regulatory and stakeholder pressure to reduce carbon footprint and implement sustainable practices.

### Affected Domain:
- Policy: Establish sustainability governance framework
- Initiatives: Launch carbon reduction program
- Operations: Transform supply chain and manufacturing processes

### Rationale:
To achieve long-term sustainability goals, comply with emerging regulations, and meet changing stakeholder expectations.

### JSON representation:

```json strategic-response-model.schema.json
{
  "triggers": [
    {
      "triggerID": "TRG-005",
      "label": "Sustainability Pressure Intensification",
      "description": "Increasing regulatory requirements and stakeholder expectations regarding carbon emissions reduction and sustainable business practices",
      "primaryCategory": "environmentalSafety",
      "origin": "Hybrid",
      "timeHorizon": "longTerm",
      "impactLevel": "high",
      "status": "Ongoing",
      "detectionDate": "2024-11-10",
      "sourceReference": "Environmental Regulatory Outlook 2025 & Stakeholder Engagement Report"
    }
  ],
  "rationales": [
    {
      "rationaleID": "RAT-005",
      "rationaleTitle": "Sustainability Transformation Program",
      "description": "Implement comprehensive sustainability initiatives across operations to reduce environmental impact, ensure regulatory compliance, and strengthen stakeholder relationships",
      "triggerReference": "TRG-005",
      "linkedDomains": [
        "policy",
        "initiative",
        "valueStream"
      ],
      "rationaleType": "proactive",
      "rationaleOrientation": "proactive",
      "anticipatedOutcomes": [
        "30% reduction in carbon emissions by 2030",
        "Full compliance with emerging environmental regulations",
        "Enhanced brand perception among environmentally-conscious consumers",
        "Reduced operational costs through resource efficiency"
      ],
      "reasoningPattern": "normative",
      "evidenceBase": "externalResearch",
      "businessValueType": "stakeholderTrust",
      "dateCreated": "2025-01-15",
      "lastReviewed": "2025-04-10",
      "effectivenessRating": 4,
      "author": "Sustainability Task Force",
      "orgUnitTitle": "Corporate Affairs",
      "relatedRationales": [
        "RAT-006"
      ],
      "relationshipTypes": [
        "supports"
      ],
      "alternativesConsidered": [
        {
          "alternativeID": "ALT-003",
          "alternativeDescription": "Minimal compliance-only approach",
          "reasonForRejection": "Insufficient to meet stakeholder expectations and future-proof the business"
        }
      ]
    }
  ]
}
```
