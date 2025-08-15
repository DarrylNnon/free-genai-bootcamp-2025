# Day 12 Notes: Building an AI-Powered SIEM Log Analyzer

Welcome to Day 12! Today, we're building our second major project: a fully automated SIEM (Security Information and Event Management) Log Analyzer. This tool will connect directly to your cloud environment, ingest logs in real-time, and use an LLM to perform intelligent security analysis.

**The Flow: CloudWatch → Lambda → GPT**

This architecture is a classic serverless pattern, prized for its scalability, cost-effectiveness, and low operational overhead. Let's break down each component.

---

### Station 1: The Source (Amazon CloudWatch Logs)

In any cloud environment, services, applications, and infrastructure components constantly generate logs. These logs are a firehose of data, recording everything from simple status updates to critical error messages and potential security events.

*   **What it is:** CloudWatch is AWS's native monitoring and observability service. We'll create a specific **Log Group** to act as a centralized collection point for logs we want to analyze.
*   **The Trigger:** The magic that connects the source to our processor is a **Subscription Filter**. We configure this filter to watch our Log Group. As soon as a new log entry arrives, the filter automatically triggers our Lambda function, forwarding the log data for processing. This is an event-driven, real-time connection.

---

### Station 2: The Processor (AWS Lambda)

This is the serverless compute engine that does the work. It's a small, stateless function that exists only to execute a specific task when triggered.

*   **Why Lambda?** We don't need a server running 24/7 just to wait for logs. Lambda lets us pay only for the milliseconds of compute time we use. It scales automatically from zero to thousands of invocations, handling a trickle or a flood of logs with ease.
*   **The Task:** Our Lambda function has a clear job:
    1.  Receive the event data from the CloudWatch Subscription Filter.
    2.  The data arrives compressed (`gzip`) and encoded (`base64`), so the first step is to decode it to get the raw log text.
    3.  Pass the raw log text to our "Intelligence" component (GPT).
    4.  Receive the analysis back from the AI.
    5.  Log the final report for a human operator to review.

---

### Station 3: The Intelligence (GPT with Few-Shot Prompting)

This is where we inject the AI into our DevSecOps workflow. Raw logs are often cryptic. An LLM can act as a tireless, expert security analyst, available 24/7 to interpret them.

*   **The Challenge:** Simply asking an LLM "Is this log bad?" is unreliable. This is a "zero-shot" prompt, and the results can be inconsistent.
*   **The Solution: Few-Shot Prompting.** We dramatically improve the AI's performance by providing it with examples within the prompt itself. Our prompt will teach the model *how* to think like a security analyst.

    ```
    <PERSONA>
    You are a senior security analyst...
    </PERSONA>

    <TASK>
    Analyze the log, identify threats, and classify severity...
    </TASK>

    <EXAMPLE 1: BENIGN>
    Input: "GET /healthcheck 200 OK"
    Analysis: "Benign activity..."
    </EXAMPLE>

    <EXAMPLE 2: MALICIOUS>
    Input: "GET /products?id=1' OR '1'='1"
    Analysis: "Potential SQL Injection attempt detected..."
    </EXAMPLE>

    <INPUT>
    {actual_log_from_lambda}
    </INPUT>
    ```

By providing these examples, we "steer" the model to produce a structured, accurate, and reliable analysis every time. This technique is fundamental to building production-grade AI systems.



