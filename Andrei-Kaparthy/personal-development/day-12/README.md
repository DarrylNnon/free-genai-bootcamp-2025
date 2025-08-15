**Day 12 (Fri)**:  
  - Start Project 2: SIEM Log Analyzer with GPT  
  - Connect CloudWatch/Stackdriver → Lambda → GPT 
# Day 12 Project: SIEM Log Analyzer with GPT

Welcome to Day 12! Today's project is to build a serverless "SIEM Log Analyzer." This system automatically ingests logs from AWS CloudWatch, uses a GPT model to perform a security analysis on them, and logs the results for review.

## 🚀 The Flow

The architecture is a powerful and common serverless pattern:

**CloudWatch Log Event → Lambda Function Trigger → GPT Analysis → CloudWatch Log Output**

1.  **CloudWatch Log Event**: A log is sent to a designated CloudWatch Log Group. For this project, we'll manually send logs to test the system.
2.  **Lambda Function Trigger**: A CloudWatch Subscription Filter is configured to watch the log group. When a new log arrives, it automatically invokes our Lambda function, passing the log data as the event payload.
3.  **GPT Analysis**: The Lambda function receives the log, formats it into a sophisticated "few-shot" prompt, and sends it to the OpenAI API for analysis.
4.  **CloudWatch Log Output**: The Lambda function takes the AI's analysis and prints it to its own logs, creating a permanent, reviewable record.

## 🎯 Objective

*   To build a real-time, event-driven, serverless security analysis pipeline.
*   To use AWS SAM for defining and deploying cloud infrastructure as code.
*   To practice writing a Lambda function that integrates with other AWS services and external APIs.
*   To design an effective **few-shot prompt** for a specific, structured analysis task.

## 🛠️ Setup

This project uses the AWS Serverless Application Model (SAM) CLI.

### 1. Prerequisites

*   **AWS CLI**: [Configured with your credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).
*   **AWS SAM CLI**: [Installation guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).
*   **Docker**: [Installation guide](https://docs.docker.com/engine/install/). Docker is required by SAM to build the Lambda deployment package.
*   **OpenAI API Key**: You need an API key from OpenAI.

### 2. Project Structure

```
.
├── README.md
├── notes.md
├── template.yaml         # The AWS SAM template defining our infrastructure
└── src/
    ├── lambda_function.py  # The core Python code for our Lambda
    ├── requirements.txt    # Python dependencies
    └── prompts/
        └── log_analyzer_prompt.md # The few-shot prompt template
```

### 3. Deployment

Follow these steps to deploy the application to your AWS account.

**Step A: Build the Application**

The `sam build` command compiles your source code and dependencies into a deployment package.

```bash
sam build
```

**Step B: Deploy to AWS**

The `sam deploy` command deploys your application to the AWS cloud. The `--guided` flag will walk you through the deployment parameters the first time.

```bash
# You will be prompted for parameters.
# Stack Name: A unique name for this project, e.g., "siem-log-analyzer"
# AWS Region: Your preferred region, e.g., "us-east-1"
# Parameter OpenAIAPIKey: Paste your OpenAI API key here.
# ... (Accept defaults for the rest) ...

sam deploy --guided
```

SAM will create a CloudFormation changeset and deploy your resources. This will create the Lambda function, the necessary IAM roles, and the two CloudWatch Log Groups.

## 🧪 How to Test

After deployment, you need to send a log to the monitored log group to trigger the analyzer.

1.  **Find the Log Group Name**: Go to the AWS CloudFormation console, find the stack you just deployed (e.g., `siem-log-analyzer`), and look at the "Resources" tab. Find the `MonitoredLogGroup` and copy its name. It will look something like `siem-log-analyzer-MonitoredLogGroup-XXXXXXXX`.

2.  **Create a Log Stream**:
    *   Go to the AWS CloudWatch console.
    *   In the left menu, click on "Log groups".
    *   Find and click on the `MonitoredLogGroup` from the step above.
    *   Click "Create log stream". Give it a name like `test-stream`.

3.  **Submit a Log Event**:
    *   Click on your new `test-stream`.
    *   Click "Create log event".
    *   In the message box, paste a log entry. Try these examples one at a time.

    **Benign Log Example:**
    ```
    192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/v1/healthcheck HTTP/1.1" 200 15 "-" "ELB-HealthChecker/2.0"
    ```

    **Malicious Log Example (SQL Injection):**
    ```
    81.7.9.21 - - [10/Oct/2023:14:01:12 +0000] "GET /products?category=books' OR '1'='1' -- HTTP/1.1" 404 512 "https://example.com" "Mozilla/5.0"
    ```

4.  **Check the Results**:
    *   Go back to the "Log groups" page in CloudWatch.
    *   Find the log group for our Lambda function. It will be named `/aws/lambda/siem-log-analyzer-LogAnalyzerFunction-XXXXXXXX`.
    *   Click on it and view the latest log stream.
    *   You will see the output from the Lambda function, including the detailed analysis from GPT for the log you submitted.

## 🧹 Cleanup

To remove all the resources created by this project, run the following command:

```bash
sam delete
```