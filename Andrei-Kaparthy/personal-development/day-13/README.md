# Day 13 Project: Advanced SIEM Log Analyzer with GPT-Powered Alerting

Welcome to Day 13! This project significantly enhances our Day 12 SIEM Log Analyzer, transforming it into a professional-grade, real-time alerting engine. It now produces structured, actionable intelligence ready for automated workflows.

## 🚀 What's New in Day 13?

*   **Structured JSON Analysis**: The AI now returns its findings in a predictable JSON format, making the output reliable and easy to parse.
*   **CVSS Severity Scoring**: The AI assesses each threat and assigns a CVSS 3.1 score and a clear severity level (`None`, `Low`, `Medium`, `High`, `Critical`).
*   **Actionable Recommendations**: Every analysis includes a concise, recommended next step for a human analyst.
*   **Simulated Real-Time Alerting**: The Lambda function identifies `High` and `Critical` alerts and logs a high-visibility message, simulating an immediate page to an on-call engineer.

## 🎯 The Upgraded Flow

**CloudWatch Log Event → Lambda Trigger → GPT Structured Analysis (JSON) → Parsed by Lambda → Conditional Alerting & Structured Log Output**

1.  **CloudWatch Log Event**: A log is sent to the `MonitoredLogGroup`.
2.  **Lambda Function Trigger**: A Subscription Filter invokes our Lambda, passing the log data.
3.  **GPT Structured Analysis**: The Lambda sends the log to the OpenAI API with a sophisticated prompt demanding a **JSON response** that includes a threat summary, CVSS score, and severity.
4.  **Conditional Alerting & Log Output**: The Lambda parses the JSON response.
    *   If the severity is `High` or `Critical`, it prints a prominent alert to its logs.
    *   It always prints the full, structured JSON analysis for a detailed, reviewable record.

## 🛠️ Setup & Deployment

This project uses the AWS Serverless Application Model (SAM) CLI.

### 1. Prerequisites

*   **AWS CLI**: Configured with your credentials.
*   **AWS SAM CLI**: Installation guide.
*   **Docker**: Installation guide. Required by SAM to build the Lambda package.
*   **OpenAI API Key**: You need an API key from OpenAI.

### 2. Deployment Steps

**Step A: Build the Application**

```bash
sam build
```

**Step B: Deploy to AWS**

The `--guided` flag will walk you through the deployment parameters the first time.

```bash
# Stack Name: A unique name, e.g., "siem-log-analyzer-day13"
# AWS Region: Your preferred region, e.g., "us-east-1"
# Parameter OpenAIAPIKey: Paste your OpenAI API key here.
# ... (Accept defaults for the rest) ...

sam deploy --guided
```

SAM will deploy the CloudFormation stack, creating the Lambda function, IAM roles, and the CloudWatch Log Groups.

## 🧪 How to Test

After deployment, send a log to the monitored log group to trigger the analyzer.

1.  **Go to the CloudWatch Console**.
2.  In the left menu, click on **Log groups**.
3.  Find and click on the log group named `/siem/day13/monitored-logs`.
4.  Click **Create log stream**. Give it a name like `test-stream-malicious`.
5.  Click on your new log stream and then **Create log event**.
6.  In the message box, paste a log entry. Try the malicious example below.

    **Malicious Log Example (SQL Injection):**
    ```
    81.7.9.21 - - [10/Oct/2023:14:01:12 +0000] "GET /products?category=books' OR '1'='1' -- HTTP/1.1" 404 512 "https://example.com" "Mozilla/5.0"
    ```

## ✅ Check the Results

1.  Go back to the **Log groups** page in CloudWatch.
2.  Find the log group for our Lambda function. It will be named `/aws/lambda/Day13-SIEM-Log-Analyzer-Function`.
3.  Click on it and view the latest log stream.
4.  You will see the detailed, structured output from the Lambda function. Because the log was malicious, you should see the special alert message!

### Expected Output in CloudWatch

You should see a series of log entries for each invocation. The most important ones will look like this:

```
# The initial log being processed
INFO    Analyzing log: 81.7.9.21 - - [10/Oct/2023:14:01:12 +0000] "GET /products?category=books' OR '1'='1' -- HTTP/1.1" 404 5