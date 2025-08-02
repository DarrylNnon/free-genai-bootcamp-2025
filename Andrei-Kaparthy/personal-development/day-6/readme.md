# Serverless GenAI Application

This project demonstrates the step-by-step implementation of a Cloud-Native GenAI architecture using AWS Lambda, Amazon Bedrock, and other serverless services. The implementation follows the "few-shot" learning guide, progressing from a simple API call to a complete conversational AI with long-term and short-term memory.

## Project Structure

The project is divided into three stages, or "shots," each in its own directory. Each stage builds upon the previous one.

```
.
├── shot1/
│   ├── lambda_function.py  # Basic LLM API call
│   └── requirements.txt
├── shot2/
│   ├── lambda_function.py  # Adds RAG for long-term memory
│   └── requirements.txt
├── shot3/
│   ├── lambda_function.py  # Adds DynamoDB for short-term memory
│   └── requirements.txt
└── readme.md               # This file
```

---

## Shot 1: The Basic API Call

This is the simplest form of the application. It provides a Lambda function that takes a user prompt and gets a direct response from an LLM (Anthropic's Claude 3 Sonnet via Amazon Bedrock).

### Components
-   **API Gateway (Not implemented here):** Would provide the HTTP endpoint.
-   **AWS Lambda (`shot1/lambda_function.py`):** Contains the core logic to call the LLM.
-   **Amazon Bedrock:** The managed service that hosts the LLM.

### How to Deploy (Conceptual)
1.  Create an AWS Lambda function.
2.  Create a `deployment.zip` file containing `lambda_function.py` and the dependencies from `requirements.txt`.
3.  Upload the zip file to your Lambda function.
4.  Configure an API Gateway trigger to invoke the Lambda via an HTTP POST request.
5.  Ensure the Lambda's execution role has permissions for `bedrock:InvokeModel`.

---

## Shot 2: Adding Long-Term Memory (RAG)

This stage enhances the Lambda function with Retrieval-Augmented Generation (RAG). It retrieves relevant information from a private knowledge base (simulated here) before calling the LLM.

### New Components
-   **Vector Database (Simulated):** A placeholder function `search_vector_db` simulates searching a vector store like Amazon OpenSearch Serverless or Pinecone.
-   **Embedding Model (Simulated):** The `get_embedding` function simulates converting text to a vector using a model like Amazon Titan Embeddings.

### How it Works
The Lambda function in `shot2/lambda_function.py` now performs these additional steps:
1.  Takes the user's prompt.
2.  Converts the prompt into a vector embedding.
3.  Uses the embedding to search a vector database for relevant context.
4.  Constructs a new, more detailed prompt that includes this context.
5.  Sends the enhanced prompt to the LLM.

---

## Shot 3: Adding Short-Term Memory (Conversational State)

This is the final, complete version of the application. It adds short-term memory to the RAG architecture, allowing for multi-turn, context-aware conversations.

### New Components
-   **Amazon DynamoDB:** A fast, serverless NoSQL database is used to store and retrieve chat history for each conversation. The table name is configured via the `CHAT_HISTORY_TABLE` environment variable.

### How it Works
The Lambda function in `shot3/lambda_function.py` combines all logic:
1.  Receives a `prompt` and a `conversation_id`.
2.  Retrieves the chat history for that `conversation_id` from DynamoDB.
3.  Performs the RAG steps from Shot 2 (embedding, vector search) to get relevant context.
4.  Constructs a final prompt containing the chat history, the RAG context, and the new user prompt.
5.  Sends the final prompt to the LLM.
6.  After receiving the LLM's response, it appends the new user message and the AI response to the history.
7.  Saves the updated history back to DynamoDB.

### How to Deploy (Conceptual)
1.  Create a DynamoDB table with a primary key of `conversation_id` (String).
2.  Create an AWS Lambda function and set an environment variable `CHAT_HISTORY_TABLE` to your table's name.
3.  Ensure the Lambda's execution role has permissions for `bedrock:InvokeModel` and DynamoDB actions (`dynamodb:GetItem`, `dynamodb:PutItem`).
4.  Deploy the code from the `shot3` directory.
5.  Configure an API Gateway that passes `prompt` and `conversation_id` in the request body.
---

## Shot 3: Adding Short-Term Memory (Conversational State)

This is the final, complete version of the application. It adds short-term memory to the RAG architecture, allowing for multi-turn, context-aware conversations.

### New Components
-   **Amazon DynamoDB:** A fast, serverless NoSQL database is used to store and retrieve chat history for each conversation. The table name is configured via the `CHAT_HISTORY_TABLE` environment variable.

### How it Works
The Lambda function in `shot3/lambda_function.py` combines all logic:
1.  Receives a `prompt` and a `conversation_id`.
2.  Retrieves the chat history for that `conversation_id` from DynamoDB.
3.  Performs the RAG steps from Shot 2 (embedding, vector search) to get relevant context.
4.  Constructs a final prompt containing the chat history, the RAG context, and the new user prompt.
5.  Sends the final prompt to the LLM.
6.  After receiving the LLM's response, it appends the new user message and the AI response to the history.
7.  Saves the updated history back to DynamoDB.

### How to Deploy (Conceptual)
1.  Create a DynamoDB table with a primary key of `conversation_id` (String).
2.  Create an AWS Lambda function and set an environment variable `CHAT_HISTORY_TABLE` to your table's name.
3.  Ensure the Lambda's execution role has permissions for `bedrock:InvokeModel` and DynamoDB actions (`dynamodb:GetItem`, `dynamodb:PutItem`).
4.  Deploy the code from the `shot3` directory.
5.  Configure an API Gateway that passes `prompt` and `conversation_id` in the request body.