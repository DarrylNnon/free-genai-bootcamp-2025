# Day 13 Notes: From Log Analyzer to Alerting Engine

Welcome to Day 13! Today, we're evolving our Day 12 project from a proof-of-concept into a professional-grade security tool. The goal is to make the AI's output not just interesting, but **actionable** and **reliable**.

This is the difference between a cool experiment and a system you can build a real security workflow around.

---

### The Upgrade: Structured Intelligence

On Day 12, our Lambda function received a raw text string from the AI. This is fine for a demo, but in a real system, we need predictable, machine-readable data. Today's key upgrade is **structured output**.

**Old Way (Day 12):**
> "This log looks like a potential SQL injection attack. It seems malicious."

**New Way (Day 13):**
```json
{
  "summary": "A potential SQL injection attempt was detected...",
  "is_malicious": true,
  "threat_type": "SQL Injection",
  "severity": "High",
  "cvss_score": 7.5,
  "recommended_action": "Block the source IP address..."
}
```

---

### Key Concepts for Day 13

1.  **Prompting for Structured Output (JSON):**
    The most significant change is in our prompt. We are explicitly instructing the LLM to format its response as a JSON object. By providing a clear schema and few-shot examples that adhere to this schema, we dramatically increase the reliability of the output. This is a fundamental technique for integrating LLMs into automated workflows.

2.  **Standardized Severity (CVSS):**
    Instead of vague terms like "bad" or "dangerous," we are asking the AI to classify the severity using a well-known industry standard: the **Common Vulnerability Scoring System (CVSS)**. This provides a consistent, numerical way to prioritize alerts. An analyst can immediately see that a CVSS 9.8 alert is more urgent than a 4.5.

3.  **Actionable Intelligence:**
    A good alert doesn't just identify a problem; it tells you what to do next. By adding `recommended_action` to our desired output, we turn the AI into a true assistant. It provides the "first step" for a human analyst, reducing response time.

4.  **Programmatic Alerting in the Lambda:**
    Because the output is now predictable JSON, our Python code can parse it. The Lambda function will now act as a dispatcher. It checks the `severity` field and, if it's `High` or `Critical`, it logs a high-visibility message. This simulates creating a high-priority ticket or sending a page to an on-call engineer.

By implementing these changes, you're demonstrating a mature approach to building AI-native security systems. You're not just calling an API; you're engineering a reliable, intelligent, and automated security process.