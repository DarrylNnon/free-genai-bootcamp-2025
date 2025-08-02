# How to Implement and Deploy Shot 2 (RAG)

This guide provides clear, step-by-step instructions to implement and deploy "Shot 2" from end to end. This stage enhances the basic Lambda function with a simulated Retrieval-Augmented Generation (RAG) pipeline.

### Prerequisites

Before you begin, make sure you have the following installed and configured:
*   An **AWS Account** with access to IAM, Lambda, and API Gateway.
*   **AWS CLI** configured with your credentials.
*   **Python 3.9+** and `pip` installed on your local machine.
*   A text editor or IDE (like VS Code).

---

### Step 1: Set Up Your Project Directory

First, create the necessary files on your local machine.

1.  Create a new directory for your project and navigate into it:
    ```bash
    mkdir shot2-project
    cd shot2-project
    ```

2.  Inside this directory, create `lambda_function.py` with the Shot 2 code:

    ```python
    # shot2-project/lambda_function.py
    import boto3
    import json

    bedrock_runtime = boto3.client(service_name='bedrock-runtime')

    def get_embedding(text):
        """Simulates converting text to a vector embedding."""
        print(f"Generating embedding for: {text}")
        return [0.1] * 1536 

    def search_vector_db(embedding):
        """Simulates searching a vector database with the given embedding."""
        print("Searching vector database for relevant context...")
        return """
        Context from knowledge base:
        - The Serverless GenAI Application uses AWS Lambda for compute.
        - Shot 1 is a basic API call to an LLM.
        - Shot 2 adds Retrieval-Augmented Generation (RAG) to provide long-term memory from a knowledge base.
        - RAG works by retrieving relevant documents and adding them as context to the LLM prompt.
        """

    def lambda_handler(event, context):
        body = json.loads(event.get('body', '{}'))
        user_prompt = body.get('prompt')

        if not user_prompt:
            return {
                'statusCode': 400,
                'body': json.dumps('Error: No prompt provided.')
            }

        query_embedding = get_embedding(user_prompt)
        relevant_context = search_vector_db(query_embedding)

        final_prompt = f"""
    Use the following context to answer the question. If the answer is not in the context, say you don't know.

    Context:
    {relevant_context}

    Question:
    {user_prompt}
    """

        model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        prompt_config = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": final_prompt}]}
            ]
        }

        try:
            response = bedrock_runtime.invoke_model(
                body=json.dumps(prompt_config),
                modelId=model_id
            )
            response_body = json.loads(response.get('body').read())
            llm_output = response_body['content'][0]['text']
            return {'statusCode': 200, 'body': json.dumps({'response': llm_output})}
        except Exception as e:
            print(f"Error invoking model: {e}")
            return {'statusCode': 500, 'body': json.dumps('Error processing your request.')}
    ```

3.  Next, create the `requirements.txt` file:
    ```
    # shot2-project/requirements.txt
    boto3
    ```

### Step 2: Create the Deployment Package

Package your function into a `.zip` file for Lambda.

```bash
# Install dependencies into a package directory
pip install -r requirements.txt -t ./package

# Copy your function code into the package
cp lambda_function.py ./package/

# Create the zip file from the package contents
cd package
zip -r ../deployment.zip .
cd ..
```

### Step 3: Create or Verify the Lambda Execution Role

This function requires the same permissions as Shot 1. You can reuse the `Shot1-Lambda-Role` if you have already created it. It needs permissions for `logs:*` (for CloudWatch) and `bedrock:InvokeModel`.

If you have not created the role, please follow **Step 3** from the Shot 1 implementation guide.

### Step 4: Create the Lambda Function

Run the following AWS CLI command to create the new Lambda function. **Remember to replace `<your-aws-account-id>` and `<your-aws-region>`**.

```bash
aws lambda create-function \
  --function-name shot2-rag-api-call \
  --runtime python3.9 \
  --role arn:aws:iam::<your-aws-account-id>:role/Shot1-Lambda-Role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://deployment.zip \
  --timeout 30 \
  --memory-size 256 \
  --region <your-aws-region>
```

### Step 5: Create and Configure the API Gateway

Follow the same steps as in Shot 1 to add an HTTP API trigger to your new `shot2-rag-api-call` function via the AWS Lambda Console. Once created, copy the **API endpoint URL**.

### Step 6: Test Your RAG API

Send a `POST` request to your new endpoint. The prompt should ask a question that can be answered by the hardcoded context in the Lambda function.

```bash
curl -X POST \
  '<your-api-gateway-url>' \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "What does Shot 2 add to the application?"}'
```

You should receive a response that uses the simulated RAG context:

```json
{"response":"Shot 2 adds Retrieval-Augmented Generation (RAG) to provide long-term memory from a knowledge base."}
```

Congratulations! You have successfully deployed a serverless application with a simulated RAG pipeline.