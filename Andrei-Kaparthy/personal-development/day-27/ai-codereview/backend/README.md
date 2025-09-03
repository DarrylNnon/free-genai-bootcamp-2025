# Smart Review - Backend Service

This directory contains the AWS SAM application for the Smart Review backend. This service is responsible for receiving GitHub webhooks, analyzing pull requests, and posting comments.

## Architecture

*   **`template.yaml`**: The AWS SAM template that defines all our cloud resources, including the API Gateway, Lambda function, and IAM permissions.
*   **`webhook/`**: The source code for our main Lambda function, written in Go.

## Prerequisites

*   AWS CLI (configured)
*   AWS SAM CLI
*   Docker
*   Go 1.x

## Development

### Building the Application

The `sam build` command compiles the Go application and prepares it for deployment. If you are running this inside a container or on a different architecture than AWS Lambda (e.g., an M1 Mac), you should use the `--use-container` flag.

```bash
# For native environments (e.g., Linux x86_64)
sam build

# For non-native environments (e.g., Mac M1/M2)
sam build --use-container
```

### Deploying the Application

The `sam deploy --guided` command will walk you through deploying the application to your AWS account. It will prompt you for the necessary parameters, such as the names of the SSM secrets.

```bash
sam deploy --guided
```

After deployment, the command will output the `WebhookApiUrl`. You must update the `url` field in the `.github/app.yml` manifest with this value for the GitHub App to function.