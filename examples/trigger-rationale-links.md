# Examples of Trigger and Rationale Links

This page provides examples of how Triggers and Rationales are used within the Orthogramic Metamodel to document the drivers of change and the justification for responses across different business domains.

Each example includes:

- A specific Trigger (external or internal)
- The Rationale for responding
- The Affected Domain(s)
- A sample JSON structure linking the trigger to a rationale

---

## Example 1: Regulatory change triggering a policy update

### Trigger:
A new data protection regulation is enacted by the government.

### Affected Domain:
- Policy: Update existing data handling policies to comply with the new regulation.

### Rationale:
To ensure compliance with legal requirements and avoid potential penalties.

### JSON representation:

```json
{
  "trigger": {
    "triggerID": "e8f9a012-3b4c-5d6e-7f8a-9b0c1d2e3f4a",
    "label": "New Data Protection Regulation",
    "description": "Enactment of new data protection regulation requiring updated data handling practices",
    "primaryCategory": "Regulatory_Compliance",
    "origin": "External",
    "timeHorizon": "Short_Term",
    "impactLevel": "High",
    "status": "Ongoing",
    "detectionDate": "2025-03-15",
    "validUntil": "2030-03-15",
    "sourceReference": "Government Gazette Notice 2025-112"
  },
  "rationale": {
    "rationaleID": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
    "rationaleTitle": "Data Protection Compliance Initiative",
    "description": "Align policies with new legal requirements to ensure compliance and protect customer data",
    "triggerReference": "e8f9a012-3b4c-5d6e-7f8a-9b0c1d2e3f4a",
    "linkedDomains": ["Policy", "Information"],
    "rationaleType": "Compliance_Fulfillment",
    "rationaleOrientation": "Reactive",
    "evidenceBase": "External_Research",
    "businessValueType": "Risk_Reduction",
    "dateCreated": "2025-03-20",
    "lastReviewed": "2025-03-20",
    "author": "Legal Compliance Team",
    "orgUnitTitle": "Legal Department"
  }
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

```json
{
  "trigger": {
    "triggerID": "c7d8e9f0-1a2b-3c4d-5e6f-7g8h9i0j1k2l",
    "label": "Remote Work Adoption Trend",
    "description": "Significant increase in remote work adoption across the industry, accelerated by technological advancements and workforce preferences",
    "primaryCategory": "Workforce_Skills",
    "subCategory": "Strategic Repositioning",
    "origin": "External",
    "timeHorizon": "Medium_Term",
    "impactLevel": "High",
    "status": "Emerging",
    "detectionDate": "2025-01-10",
    "sourceReference": "Industry Workforce Report Q1 2025"
  },
  "rationale": {
    "rationaleID": "m3n4o5p6-q7r8-s9t0-u1v2-w3x4y5z6a7b8",
    "rationaleTitle": "Remote Work Strategy Implementation",
    "description": "Adapt organizational strategy to accommodate remote work capabilities to attract and retain talent while maintaining operational effectiveness",
    "triggerReference": "c7d8e9f0-1a2b-3c4d-5e6f-7g8h9i0j1k2l",
    "linkedDomains": ["Strategy", "Capabilities", "Workforce_Skills"],
    "rationaleType": "Strategic_Advancement",
    "rationaleOrientation": "Proactive",
    "anticipatedOutcomes": [
      "Improved talent acquisition and retention",
      "Reduced office space costs",
      "Enhanced employee satisfaction",
      "Access to global talent pool"
    ],
    "reasoningPattern": "Predictive",
    "evidenceBase": "Industry_Best_Practice",
    "businessValueType": "Competitive_Advantage",
    "competitivePositioning": {
      "positioningType": "Differentiation",
      "positioningDescription": "Position the organization as an employer of choice through advanced remote work capabilities",
      "competitiveTarget": "Technology talent market segment"
    },
    "dateCreated": "2025-02-01",
    "lastReviewed": "2025-04-15",
    "effectivenessRating": 4,
    "author": "HR Strategy Team",
    "orgUnitTitle": "Human Resources"
  }
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

```json
{
  "trigger": {
    "triggerID": "d5e6f7g8-h9i0-j1k2-l3m4-n5o6p7q8r9s0",
    "label": "Customer Service Response Degradation",
    "description": "Customer service response times have increased by 35% over the past quarter, exceeding acceptable thresholds and impacting customer satisfaction metrics",
    "primaryCategory": "Performance_Response",
    "subCategory": "Capability Enhancement",
    "origin": "Internal",
    "timeHorizon": "Immediate",
    "impactLevel": "Critical",
    "status": "Ongoing",
    "detectionDate": "2025-03-01",
    "sourceReference": "Q1 2025 Customer Service Performance Report"
  },
  "rationale": {
    "rationaleID": "t1u2v3w4-x5y6-z7a8-b9c0-d1e2f3g4h5i6",
    "rationaleTitle": "Customer Service Improvement Initiative",
    "description": "Address service quality degradation through process improvements, staff training, and technology enhancements to restore customer satisfaction levels",
    "triggerReference": "d5e6f7g8-h9i0-j1k2-l3m4-n5o6p7q8r9s0",
    "linkedDomains": ["Capabilities", "Performance", "Services"],
    "rationaleType": "Remedial",
    "rationaleOrientation": "Reactive",
    "alternativeConsidered": [
      {
        "alternativeID": "j7k8l9m0-n1o2-p3q4-r5s6-t7u8v9w0x1y2",
        "alternativeDescription": "Outsource customer service operations to third-party provider",
        "reasonForRejection": "Would reduce control over customer experience and risk further brand damage"
      },
      {
        "alternativeID": "z3a4b5c6-d7e8-f9g0-h1i2-j3k4l5m6n7o8",
        "alternativeDescription": "Implement chatbot-only first-level support",
        "reasonForRejection": "Technology not mature enough to handle complex customer issues"
      }
    ],
    "reasoningPattern": "Causal",
    "evidenceBase": "Data_Driven",
    "businessValueType": "Customer_Experience",
    "dateCreated": "2025-03-10",
    "lastReviewed": "2025-04-01",
    "effectivenessRating": 3,
    "author": "Customer Experience Team",
    "orgUnitTitle": "Customer Support Department"
  }
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

```json
{
  "trigger": {
    "triggerID": "p9q0r1s2-t3u4-v5w6-x7y8-z9a0b1c2d3e4",
    "label": "AI Predictive Analytics Advancements",
    "description": "Significant advancements in AI-powered predictive analytics creating new opportunities for product enhancement and market differentiation",
    "primaryCategory": "Technological_Change",
    "subCategory": "Innovation Initiative",
    "origin": "External",
    "timeHorizon": "Medium_Term",
    "impactLevel": "High",
    "status": "Emerging",
    "detectionDate": "2025-02-15",
    "sourceReference": "Technology Trend Report Q1 2025"
  },
  "rationale": {
    "rationaleID": "f5g6h7i8-j9k0-l1m2-n3o4-p5q6r7s8t9u0",
    "rationaleTitle": "AI-Driven Product Innovation Strategy",
    "description": "Integrate advanced AI capabilities into our product suite to create differentiated offerings and new revenue streams while establishing market leadership in predictive analytics",
    "triggerReference": "p9q0r1s2-t3u4-v5w6-x7y8-z9a0b1c2d3e4",
    "linkedDomains": ["Strategy", "Products", "Capabilities"],
    "rationaleType": "Opportunistic",
    "rationaleOrientation": "Proactive",
    "anticipatedOutcomes": [
      "20% premium pricing on AI-enhanced products",
      "Expansion into adjacent markets",
      "Development of recurring revenue streams",
      "Establishment of thought leadership position"
    ],
    "reasoningPattern": "Predictive",
    "evidenceBase": "Competitive_Analysis",
    "strategicObjectiveReference": "v1w2x3y4-z5a6-b7c8-d9e0-f1g2h3i4j5k6",
    "businessValueType": "Market_Creation",
    "competitivePositioning": {
      "positioningType": "Innovation_Leadership",
      "positioningDescription": "Establish first-mover advantage in AI-enhanced product category",
      "competitiveTarget": "Enterprise analytics market segment"
    },
    "dateCreated": "2025-02-28",
    "lastReviewed": "2025-03-15",
    "effectivenessRating": 5,
    "author": "Innovation Strategy Team",
    "orgUnitTitle": "Product Development"
  }
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

```json
{
  "trigger": {
    "triggerID": "l7m8n9o0-p1q2-r3s4-t5u6-v7w8x9y0z1a2",
    "label": "Sustainability Pressure Intensification",
    "description": "Increasing regulatory requirements and stakeholder expectations regarding carbon emissions reduction and sustainable business practices",
    "primaryCategory": "Environmental_Safety",
    "origin": "Hybrid",
    "timeHorizon": "Long_Term",
    "impactLevel": "High",
    "status": "Ongoing",
    "detectionDate": "2024-11-10",
    "sourceReference": "Environmental Regulatory Outlook 2025 & Stakeholder Engagement Report"
  },
  "rationale": {
    "rationaleID": "b3c4d5e6-f7g8-h9i0-j1k2-l3m4n5o6p7q8",
    "rationaleTitle": "Sustainability Transformation Program",
    "description": "Implement comprehensive sustainability initiatives across operations to reduce environmental impact, ensure regulatory compliance, and strengthen stakeholder relationships",
    "triggerReference": "l7m8n9o0-p1q2-r3s4-t5u6-v7w8x9y0z1a2",
    "linkedDomains": ["Policy", "Initiatives", "Value_Stream"],
    "rationaleType": "Proactive",
    "rationaleOrientation": "Proactive",
    "anticipatedOutcomes": [
      "30% reduction in carbon emissions by 2030",
      "Full compliance with emerging environmental regulations",
      "Enhanced brand perception among environmentally-conscious consumers",
      "Reduced operational costs through resource efficiency"
    ],
    "alternativeConsidered": [
      {
        "alternativeID": "r9s0t1u2-v3w4-x5y6-z7a8-b9c0d1e2f3g4",
        "alternativeDescription": "Minimal compliance-only approach",
        "reasonForRejection": "Insufficient to meet stakeholder expectations and future-proof the business"
      }
    ],
    "reasoningPattern": "Normative",
    "evidenceBase": "External_Research",
    "businessValueType": "Stakeholder_Trust",
    "dateCreated": "2025-01-15",
    "lastReviewed": "2025-04-10",
    "effectivenessRating": 4,
    "author": "Sustainability Task Force",
    "orgUnitTitle": "Corporate Affairs",
    "relatedRationales": ["h5i6j7k8-l9m0-n1o2-p3q4-r5s6t7u8v9w0"],
    "relationshipTypes": ["supports"]
  }
}
```
