# How to Implement and Deploy Shot 3 (Conversational RAG)

This guide provides clear, step-by-step instructions to implement and deploy "Shot 3" from end to end. This final stage completes the application by adding short-term conversational memory using **Amazon DynamoDB**, allowing for context-aware, multi-turn conversations.

### Prerequisites

*   An **AWS Account** with access to IAM, Lambda, API Gateway, and DynamoDB.
*   **AWS CLI** configured with your credentials.
*   **Python 3.9+** and `pip` installed on your local machine.

---

### Step 1: Create the DynamoDB Table

First, you need a database to store the chat history. We will create a DynamoDB table where each item represents a conversation, identified by a unique `conversation_id`.

1.  Define the table name. We'll use `ChatHistoryTable`.
2.  Run the following AWS CLI command to create the table.

    ```bash
    aws dynamodb create-table \
        --table-name ChatHistoryTable \
        --attribute-definitions AttributeName=conversation_id,AttributeType=S \
        --key-schema AttributeName=conversation_id,KeyType=HASH \
        --billing-mode PAY_PER_REQUEST
    ```
    This command creates a simple, serverless table with `conversation_id` as its primary key.

### Step 2: Set Up Your Project Directory

1.  Create a new directory for your project:
    ```bash
    mkdir shot3-project
    cd shot3-project
    ```

2.  Inside this directory, create `lambda_function.py` with the Shot 3 code:

    ```python
    # shot3-project/lambda_function.py
    import boto3
    import json
    import os

    bedrock_runtime = boto3.client(service_name='bedrock-runtime')
    dynamodb = boto3.resource('dynamodb')
    TABLE_NAME = os.environ.get('CHAT_HISTORY_TABLE')
    table = dynamodb.Table(TABLE_NAME)

    def get_embedding(text):
        """Simulates converting text to a vector embedding."""
        print(f"Generating embedding for: {text}")
        return [0.1] * 1536 

    def search_vector_db(embedding):
        """Simulates searching a vector database."""
        print("Searching vector database for relevant context...")
        return """
        Context from knowledge base:
        - The Serverless GenAI Application uses AWS Lambda for compute.
        - Shot 1 is a basic API call to an LLM.
        - Shot 2 adds Retrieval-Augmented Generation (RAG) for long-term memory.
        - Shot 3 adds Amazon DynamoDB for short-term conversational memory.
        - The `conversation_id` is used to track chat history in DynamoDB.
        """

    def lambda_handler(event, context):
        body = json.loads(event.get('body', '{}'))
        user_prompt = body.get('prompt')
        conversation_id = body.get('conversation_id')

        if not user_prompt or not conversation_id:
            return {
                'statusCode': 400,
                'body': json.dumps('Error: `prompt` and `conversation_id` are required.')
            }

        try:
            response = table.get_item(Key={'conversation_id': conversation_id})
            history = response.get('Item', {}).get('messages', [])

            query_embedding = get_embedding(user_prompt)
            relevant_context = search_vector_db(query_embedding)

            final_user_content = f"""
    Use the following context to answer the question. If the answer is not in the context, say you don't know.

    Context:
    {relevant_context}

    Question:
    {user_prompt}
    """
            messages_for_llm = history + [
                {"role": "user", "content": [{"type": "text", "text": final_user_content}]}
            ]

            prompt_config = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2048,
                "messages": messages_for_llm
            }

            response = bedrock_runtime.invoke_model(
                body=json.dumps(prompt_config),
                modelId='anthropic.claude-3-sonnet-20240229-v1:0'
            )
            response_body = json.loads(response.get('body').read())
            llm_output_content = response_body['content']
            llm_output_text = llm_output_content[0]['text']

            new_user_message = {"role": "user", "content": [{"type": "text", "text": user_prompt}]}
            new_assistant_message = {"role": "assistant", "content": llm_output_content}
            updated_history = history + [new_user_message, new_assistant_message]
            
            table.put_item(
                Item={'conversation_id': conversation_id, 'messages': updated_history}
            )

            return {'statusCode': 200, 'body': json.dumps({'response': llm_output_text})}
        except Exception as e:
            print(f"Error processing request: {e}")
            return {'statusCode': 500, 'body': json.dumps('Error processing your request.')}
    ```

3.  Create the `requirements.txt` file:
    ```
    # shot3-project/requirements.txt
    boto3
    ```

### Step 3: Create the Deployment Package

Package your function and dependencies into a `.zip` file.

```bash
pip install -r requirements.txt -t ./package
cp lambda_function.py ./package/
cd package
zip -r ../deployment.zip .
cd ..
```

### Step 4: Update the Lambda Execution Role

The Lambda function now needs permission to read from and write to the DynamoDB table. We will update the `Shot1-Lambda-Role` with these permissions.

1.  Create a new permissions policy file named `lambda-permissions-shot3.json`. **Remember to replace `<your-aws-account-id>` and `<your-aws-region>`**.

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                "Resource": "arn:aws:logs:*:*:*"
            },
            {
                "Effect": "Allow",
                "Action": "bedrock:InvokeModel",
                "Resource": "arn:aws:bedrock:*:*:foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
            },
            {
                "Effect": "Allow",
                "Action": ["dynamodb:GetItem", "dynamodb:PutItem"],
                "Resource": "arn:aws:dynamodb:<your-aws-region>:<your-aws-account-id>:table/ChatHistoryTable"
            }
        ]
    }
    ```

2.  Attach this updated policy to the role. This command overwrites the previous policy with the new one that includes DynamoDB permissions.
    ```bash
    aws iam put-role-policy \
        --role-name Shot1-Lambda-Role \
        --policy-name Shot1-Lambda-Permissions \
        --policy-document file://lambda-permissions-shot3.json
    ```

### Step 5: Create the Lambda Function

Now, create the Lambda function, making sure to pass the DynamoDB table name as an environment variable. **Remember to replace `<your-aws-account-id>` and `<your-aws-region>`**.

```bash
aws lambda create-function \
  --function-name shot3-conversational-rag \
  --runtime python3.9 \
  --role arn:aws:iam::<your-aws-account-id>:role/Shot1-Lambda-Role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://deployment.zip \
  --timeout 60 \
  --memory-size 512 \
  --region <your-aws-region> \
  --environment "Variables={CHAT_HISTORY_TABLE=ChatHistoryTable}"
```

### Step 6: Create and Configure the API Gateway

Follow the same steps as in Shot 1 and 2 to add an **HTTP API** trigger to your new `shot3-conversational-rag` function via the AWS Lambda Console. Copy the resulting **API endpoint URL**.

### Step 7: Test Your Conversational API

To test the conversational memory, you must send at least two requests with the same `conversation_id`.

1.  **First Request:** Ask an initial question.

    ```bash
    curl -X POST \
      '<your-api-gateway-url>' \
      -H 'Content-Type: application/json' \
      -d '{"prompt": "What does Shot 3 add?", "conversation_id": "conv-123"}'
    ```
    The model should respond using the RAG context: `{"response":"Shot 3 adds Amazon DynamoDB for short-term conversational memory."}`

2.  **Second Request (Follow-up):** Ask a follow-up question. Use the **same `conversation_id`**.

    ```bash
    curl -X POST \
      '<your-api-gateway-url>' \
      -H 'Content-Type: application/json' \
      -d '{"prompt": "Why is that component important?", "conversation_id": "conv-123"}'
    ```
    Because the model now has the history of the first question, it will understand that "that component" refers to DynamoDB and give a relevant answer about its role in maintaining conversational state.

Congratulations! You have successfully deployed a complete, conversational GenAI application with both long-term (RAG) and short-term (DynamoDB) memory.