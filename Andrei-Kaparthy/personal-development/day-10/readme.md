# Day 10: IaC GPT Assistant - Web Interface & AWS Deployment

This project builds a Flask web interface for the "IaC GPT Assistant" and configures it for deployment on AWS Lambda via the AWS Serverless Application Model (SAM).

## Architecture

1.  **Frontend**: A simple HTML/CSS/JS interface served by Flask.
2.  **Backend**: A Flask application that receives user requests.
3.  **API Gateway (HTTP API)**: Exposes the Lambda function as a public web endpoint.
4.  **AWS Lambda**: Hosts the Flask application and the core Python logic.
5.  **`tfsec` Lambda Layer**: A separate layer containing the `tfsec` binary, making it available to the Lambda function.
6.  **OpenAI API**: Called by the Lambda function to generate code and reports.

## Prerequisites

Before you begin, ensure you have the following installed and configured:

*   **AWS CLI**: Configured with your AWS credentials (`aws configure`).
*   **AWS SAM CLI**: Installation Guide
*   **Docker**: Must be running on your local machine. SAM uses it to build deployment packages.
*   **OpenAI API Key**: Your secret key from OpenAI.

## Step-by-Step Deployment Guide

### Step 1: Create the `tfsec` Lambda Layer

Our Lambda function needs the `tfsec` binary to run. We'll package it into a Lambda Layer.

1.  **Create a directory structure for the layer:**
    ```bash
    mkdir -p tfsec-layer/bin
    cd tfsec-layer
    ```

2.  **Download the `tfsec` binary for Amazon Linux 2 (x86_64):**
    ```bash
    # Note: Check for the latest version on the tfsec releases page
    curl -L -o bin/tfsec https://github.com/aquasecurity/tfsec/releases/download/v1.28.1/tfsec-linux-amd64
    chmod +x bin/tfsec
    ```

3.  **Publish the layer to your AWS account:**
    ```bash
    aws lambda publish-layer-version \
      --layer-name tfsec-binary-layer \
      --description "tfsec v1.28.1 binary" \
      --license-info "MIT" \
      --zip-file fileb://<(zip -r - .) \
      --compatible-runtimes python3.9 \
      --compatible-architectures x86_64
    ```

4.  **Copy the `LayerVersionArn`** from the JSON output. It will look something like `arn:aws:lambda:us-east-1:123456789012:layer:tfsec-binary-layer:1`. You will need this for the deployment step.

    ```bash
    cd ..
    ```

### Step 2: Build the SAM Application

Now, we build the Flask application and its dependencies into a deployment package.

```bash
# Navigate to the day-10 directory
cd /path/to/your/project/day-10

sam build
```

### Step 3: Deploy the Application

This command will deploy all the resources defined in `template.yaml` to your AWS account.

```bash
sam deploy --guided
