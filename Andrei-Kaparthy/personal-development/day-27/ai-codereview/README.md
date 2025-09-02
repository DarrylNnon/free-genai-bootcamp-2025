# 🤖 Smart Review - AI-Powered Code Review as a Service

Smart Review is an intelligent code reviewer that automatically analyzes GitHub pull requests. Powered by advanced language models and expert-engineered prompts, it provides actionable feedback on security vulnerabilities, performance bottlenecks, and coding best practices, right where developers work.

This repository contains the full source code for the Smart Review service.

## ✨ How It Works

Smart Review is built as a **GitHub App** with a serverless backend on AWS. This architecture ensures scalability, security, and ease of use for our customers.

1.  **Installation**: A user installs the Smart Review GitHub App on their repository.
2.  **Webhook Event**: When a pull request is opened or updated, GitHub sends a secure webhook to our backend.
3.  **Authentication**: Our AWS Lambda function authenticates as the GitHub App and generates a short-lived token to access the repository.
4.  **Analysis**: The Lambda fetches the code `diff`, injects it into our proprietary few-shot prompt, and calls a state-of-the-art LLM (e.g., GPT-4o) for analysis.
5.  **Feedback**: The AI-generated review is posted as a comment on the pull request, providing immediate, in-context feedback to the developer.

## 🛠️ Architecture

Our service is composed of three main components:

-   **`.github/app.yml`**: The manifest file that defines our GitHub App, its permissions, and its webhook configuration.
-   **`backend/`**: An AWS SAM application that defines our serverless infrastructure.
    -   **API Gateway**: Provides a public HTTP endpoint to receive webhooks.
    -   **AWS Lambda**: The core of our service, containing all the business logic for processing reviews.
    -   **AWS SSM Parameter Store**: Securely stores our application secrets (API keys, etc.).
-   **`dashboard/`**: A Plotly Dash web application that will serve as our customer-facing portal for management and analytics.

## 🚀 Getting Started (For Developers of Smart Review)

This section is for developers contributing to the Smart Review service.

### 1. Set Up Secrets

Store the required secrets in AWS SSM Parameter Store in the `us-east-1` region (or your preferred region).

```bash
aws ssm put-parameter --name "/smart-review/github/app-id" --value "YOUR_APP_ID" --type "String"
aws ssm put-parameter --name "/smart-review/github/webhook-secret" --value "YOUR_WEBHOOK_SECRET" --type "SecureString"
aws ssm put-parameter --name "/smart-review/github/private-key" --value "YOUR_PRIVATE_KEY_CONTENT" --type "SecureString"
aws ssm put-parameter --name "/smart-review/openai/api-key" --value "sk-YOUR_OPENAI_KEY" --type "SecureString"
```

### 2. Deploy the Backend

Navigate to the `backend/` directory and deploy using the AWS SAM CLI.

```bash
sam build
sam deploy --guided
```

After deployment, update the `webhook_url` in `.github/app.yml` with the `WebhookApiUrl` from the SAM output.

---

**Smart Review S.R.L.** - Building the future of software development.
