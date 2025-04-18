# Examples of Trigger and Rationale Links

This page provides examples of how **Triggers** and **Rationales** are used within the Orthogramic Metamodel to document the drivers of change and the justification for responses across different business domains.

Each example includes:
- A specific **Trigger** (external or internal)
- The **Rationale** for responding
- The **Affected Domain(s)**
- A sample JSON structure linking the trigger to a rationale and a domain response

---

## Example 1: Regulatory change triggering a policy update

**Trigger:**  
A new data protection regulation is enacted by the government.

**Affected Domain:**  
- `Policy`: Update existing data handling policies to comply with the new regulation.

**Rationale:**  
To ensure compliance with legal requirements and avoid potential penalties.

**JSON representation:**

```json
{
  "trigger": {
    "type": "RegulatoryChange",
    "description": "Enactment of new data protection regulation"
  },
  "affectedDomain": "Policy",
  "rationale": {
    "type": "Compliance",
    "description": "Align policies with new legal requirements to ensure compliance"
  }
}

## Example 2: Market trend influencing strategy
**Trigger:**
Emerging trend of remote work adoption in the industry.

**Affected Domain:**

Strategy: Develop initiatives to support remote work infrastructure.

**Rationale:**  
To stay competitive and meet the evolving needs of the workforce.

**JSON representation:**
{
  "trigger": {
    "type": "MarketTrend",
    "description": "Increase in remote work adoption across the industry"
  },
  "affectedDomain": "Strategy",
  "rationale": {
    "type": "Competitiveness",
    "description": "Adapt strategy to accommodate remote work and attract talent"
  }
}


## Example 3: Internal performance issue leading to capability enhancement
**Trigger:**
Customer service response times have increased beyond acceptable thresholds.

**Affected Domain:**

Capabilities: Enhance customer service processes and training.

**Rationale:**  
To improve customer satisfaction and retention rates.

**JSON representation:**
```json
{
  "trigger": {
    "type": "PerformanceIssue",
    "description": "Customer service response times exceeding acceptable limits"
  },
  "affectedDomain": "Capabilities",
  "rationale": {
    "type": "CustomerSatisfaction",
    "description": "Improve service quality to retain customers"
  }
}

