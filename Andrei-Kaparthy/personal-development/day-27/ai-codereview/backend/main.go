package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ssm"
	"github.com/google/go-github/v59/github"
)

var (
	githubWebhookSecret string
)

// init runs on cold start of the Lambda function.
// It loads secrets from SSM Parameter Store into memory for the lifetime of the container.
func init() {
	log.Println("Starting cold start initialization...")

	// Get parameter names from environment variables set in template.yaml
	webhookSecretParamName := os.Getenv("GITHUB_WEBHOOK_SECRET_PARAM")
	if webhookSecretParamName == "" {
		log.Fatal("FATAL: GITHUB_WEBHOOK_SECRET_PARAM environment variable not set")
	}

	// Load default AWS configuration
	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatalf("FATAL: unable to load AWS config: %v", err)
	}

	ssmClient := ssm.NewFromConfig(cfg)

	// Get the webhook secret from SSM Parameter Store
	param, err := ssmClient.GetParameter(context.TODO(), &ssm.GetParameterInput{
		Name:           &webhookSecretParamName,
		WithDecryption: true,
	})
	if err != nil {
		log.Fatalf("FATAL: failed to get webhook secret from SSM: %v", err)
	}
	githubWebhookSecret = *param.Parameter.Value
	log.Println("Successfully loaded GitHub webhook secret from SSM.")
}

// Handler is our lambda handler function
// It uses Amazon API Gateway request/responses provided by the aws-lambda-go/events package,
func Handler(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	log.Printf("Received webhook. Headers: %v", request.Headers)
	log.Printf("Received webhook. Body: %s", request.Body)
	

	// Phase 1: Verify GitHub webhook signature
	payloadBytes := []byte(request.Body)
	sig := request.Headers["x-hub-signature-256"]
	if err := github.ValidateSignature(sig, payloadBytes, []byte(githubWebhookSecret)); err != nil {
		log.Printf("ERROR: Signature validation failed: %v", err)
		return events.APIGatewayProxyResponse{StatusCode: 401, Body: "{\"error\":\"signature validation failed\"}"}, nil
	}
	log.Println("Signature successfully verified.")

	// TODO (Phase 2): Parse GitHub event payload
	// We only care about `pull_request` events with an `action` of `opened` or `synchronize`.

	// TODO (Phase 3): Authenticate as the GitHub App
	// Use the GITHUB_APP_ID_PARAM and GITHUB_PRIVATE_KEY_PARAM to generate a JWT,
	// then use the JWT to get an installation access token.

	// TODO (Phase 4): Fetch PR diff
	// Use the installation access token to call the GitHub API and get the PR's diff.

	// TODO (Phase 5): Call AI analysis service
	// Use the OPENAI_API_KEY_PARAM to call the LLM with our engineered prompt and the code diff.

	// TODO (Phase 6): Post comment back to PR
	// Use the installation access token to post the AI's analysis as a comment on the PR.

	return events.APIGatewayProxyResponse{StatusCode: 200, Body: fmt.Sprintf("{\"status\":\"success\", \"message\":\"Webhook received and verified.\"}"\"}")}, nil
}

func main() {
	lambda.Start(Handler)
}