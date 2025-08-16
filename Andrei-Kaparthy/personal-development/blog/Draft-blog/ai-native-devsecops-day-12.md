# AI-Native DevSecOps: Day 12 Lessons

After teaching our AI to act, Day 12 was about giving it the ability to *see*. The mission was to start Project 2: a SIEM (Security Information and Event Management) log analyzer. This system will watch a stream of cloud security logs and use an LLM to spot potential threats that traditional rule-based systems might miss.

---

### Lesson 1: The Data Stream (The "CloudWatch to Lambda" Shot)

*   **Components:** Amazon CloudWatch Logs, Lambda Subscriptions.
*   **How it Works:** The foundation of any SIEM is getting the data. I configured a CloudWatch Log Group to stream its logs directly to a Lambda function. This creates a powerful, event-driven pipeline where every new log entry automatically triggers our analysis code.
*   **Use Case:** Tapping into the central nervous system of an AWS account. This pattern works for any log source: VPC Flow Logs, CloudTrail API calls, or custom application logs.

---

### Lesson 2: The AI Security Analyst (The "Log -> Prompt -> Insight" Shot)

*   **Components:** The Lambda function, a managed LLM service like Amazon Bedrock.
*   **How it Works:** The Lambda function receives the log event from CloudWatch. It then wraps the raw log message in a simple prompt, like: `"You are a senior security analyst. Analyze the following log entry for any potential security threats, anomalies, or malicious activity. Explain your findings: [log_entry]"`. This prompt is then sent to the LLM.
*   **Use Case:** This is the core of the AI-powered analysis. Instead of relying on complex regex and predefined correlation rules, we're leveraging the LLM's vast knowledge to perform an initial assessment of a single log entry.

---

### Lesson 3: The First Pass Summary (The "Raw Text" Shot)

*   **The Output:** The LLM responds with a natural language paragraph, for example: "This log entry appears to show a failed login attempt from an unusual IP address, which could be a sign of a brute-force attack."
*   **The Limitation:** While insightful for a human, this raw text is difficult for other automated systems to use. It's just a string. We can't easily parse it to trigger specific alerts or create tickets based on severity. It's a fantastic proof-of-concept, but not yet a scalable system.

---

## Day 12 Conclusion

Today, we successfully built the first version of our AI-powered SIEM. We have a working pipeline that takes raw logs and produces human-readable security insights. The system can "see" and "think," but its output is unstructured. The next step is to teach it to communicate in a way that our other systems can understand, turning these interesting observations into actionable, automated intelligence.