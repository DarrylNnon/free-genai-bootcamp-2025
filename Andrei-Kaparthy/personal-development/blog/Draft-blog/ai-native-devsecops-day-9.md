# AI-Native DevSecOps: Day 9 Lessons

Our application is deployed and secure, but is it working correctly? Is it fast? Are users getting good answers? Day 9 was about adding the "Ops" to DevSecOps by instrumenting our system for observability. If you can't see what it's doing, you can't fix or improve it.

---

### Lesson 1: Basic Logging (The "CloudWatch" Shot)

The simplest form of observability is logging. Every Lambda execution generates logs, and knowing how to find and read them is the first step in debugging.

*   **Components:** Amazon CloudWatch Logs.
*   **How it Works:** By default, anything the Lambda function `print()`s to standard output is captured in a CloudWatch Log Group. When an error occurs, the full stack trace appears here. I learned to navigate the console to find the logs for a specific invocation and diagnose a simple bug.
*   **Use Case:** The fundamental tool for debugging serverless functions. "Did it run? Did it crash? What was the error?"

---

### Lesson 2: Structured Logging & Tracing (The "X-Ray" Shot)

Simple print statements are messy. Structured logs are machine-readable, and tracing lets us see the performance of the entire system.

*   **New Components:** Structured logging libraries, AWS X-Ray.
*   **How it Works:** I replaced `print()` statements with a logging library that outputs JSON. This makes logs searchable and easy to parse. Then, I enabled active tracing on the API Gateway and Lambda. This automatically instruments the AWS SDK calls, creating a service map in X-Ray that visualizes the entire request flow: API Gateway -> Lambda -> Bedrock -> DynamoDB, including the latency of each step.
*   **Use Case:** Pinpointing performance bottlenecks. "Is the RAG query slow? Or is the LLM taking a long time to respond?" Tracing answers this instantly.

---

### Lesson 3: AI-Specific Monitoring (The "Guardrails" Shot)

GenAI applications have unique failure modes that traditional monitoring misses. We need to monitor the *quality* and *safety* of the AI's inputs and outputs.

*   **New Component:** LLM evaluation and monitoring logic (e.g., Amazon Bedrock Guardrails, or custom checks).
*   **How it Works:** I implemented a simple check in the Lambda to log the length and a hash of the prompt and response. For a more robust solution, I configured a Bedrock Guardrail to detect and block prompts containing harmful content or responses that reveal Personally Identifiable Information (PII). These events generate specific logs or metrics that can trigger alarms.
*   **Use Case:** Monitoring for prompt injection attacks, ensuring the bot doesn't leak sensitive data from its RAG context, and tracking overall response quality.

---

## Day 9 Conclusion

Today, we gave our application a nervous system. We moved from blind deployment to an observable system where we can track performance, diagnose errors, and, most importantly, monitor the specific behaviors of the AI itself. Combining traditional tracing with AI-specific guardrails provides a comprehensive view of application health. We can now confidently answer not just "Is it up?" but "Is it working well and safely?"