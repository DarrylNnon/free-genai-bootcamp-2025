Day 6 (Sat):

-   Study Cloud-Native GenAI Architecture (Serverless + LLM)
-   Draft blog: “AI-Native DevSecOps: Day 1 Lessons”


# study guide 

Of course! It's Day 6, and you're tackling one of the most exciting topics in modern software engineering. I love your idea of using the "few-shot" technique to learn. Just as we give a language model examples to help it understand a task, I'll provide you with a series of architectural "shots" or patterns. Each one is a real-world scenario that adds a new capability, building from a simple starting point to a powerful, end-to-end system.

Let's get you ready to understand, implement, and teach Cloud-Native GenAI architecture.

The "Few-Shot" Guide to Serverless GenAI Architecture
The core idea of a Cloud-Native GenAI Architecture is to build intelligent applications that are scalable, resilient, and efficient by leveraging cloud services. Using Serverless (like AWS Lambda) means you don't manage servers, you only pay for what you use, and it scales automatically—perfect for unpredictable AI workloads.


Shot 1: The Basic API Call (The "Zero-Shot" Architecture)
This is the simplest, most fundamental pattern. The goal is to send a prompt to an LLM and get a response.

Real-World Scenario: A simple "Ask Me Anything" feature on a static website where a user asks a question and gets an answer directly from a general-purpose LLM.

Architectural Components:

API Gateway: Provides an HTTP endpoint for your website to call.
AWS Lambda: The serverless compute function that contains the logic.
Managed LLM Service: An API like Amazon Bedrock or OpenAI that hosts the powerful LLM. You don't run the model; you just call it.
How it works:

A user on your website submits a prompt.
The website's frontend sends the prompt to your API Gateway endpoint.
API Gateway triggers your Lambda function, passing the user's prompt.
The Lambda function calls the Amazon Bedrock API with the prompt.
Bedrock processes the prompt with a model (e.g., Claude 3) and returns a response.
Your Lambda function sends this response back through API Gateway to the user.
Implementation (AWS Lambda - Python):


# lambda_function.py
import boto3
import json

# It's best practice to initialize the client outside the handler
bedrock_runtime = boto3.client(service_name='bedrock-runtime')

def lambda_handler(event, context):
    # 1. Get the user's prompt from the API Gateway event
    body = json.loads(event.get('body', '{}'))
    user_prompt = body.get('prompt')

    if not user_prompt:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: No prompt provided.')
        }

    # 2. Prepare the payload for the LLM (this example is for Claude 3)
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    prompt_config = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_prompt}]
            }
        ]
    }

    # 3. Invoke the model via the Bedrock API
    try:
        response = bedrock_runtime.invoke_model(
            body=json.dumps(prompt_config),
            modelId=model_id,
            contentType='application/json',
            accept='application/json'
        )
        
        # 4. Parse the response and extract the text
        response_body = json.loads(response.get('body').read())
        llm_output = response_body['content'][0]['text']

        return {
            'statusCode': 200,
            'body': json.dumps({'response': llm_output})
        }

    except Exception as e:
        print(f"Error invoking model: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing your request.')
        }
```

# shot 2

Shot 2: Adding Long-Term Memory (RAG Architecture)
The basic pattern has no knowledge of your private data. Retrieval-Augmented Generation (RAG) solves this by giving the LLM context from your documents.

Real-World Scenario: A customer support chatbot that answers questions based on your company's internal knowledge base of product manuals and policies.

New Architectural Components:

Vector Database: A specialized database (e.g., Amazon OpenSearch Serverless, Pinecone, Chroma) to store and efficiently search through "embeddings" (numerical representations of your text).
S3 Bucket: To store your source documents (PDFs, .txt, etc.).
Embedding Model: A model (like Amazon Titan Embeddings) that converts text into vectors.
How it works: It's a two-part process:

Offline Data Ingestion (to build the memory):

You upload your product manuals to an S3 bucket.
An S3 event triggers a Lambda function that reads the document, splits it into chunks, converts each chunk into a vector using an embedding model, and stores it in the Vector Database.
Online Inference (when the user asks a question):

The user asks, "How do I reset the password on product X?"
The request hits your main Lambda function.
The Lambda converts the user's question into a vector.
It then queries the Vector DB to find the most relevant text chunks from your manuals.
The Lambda constructs a new, more detailed prompt: "Context: [Relevant text from manuals]... Question: How do I reset the password on product X?"
This combined prompt is sent to the LLM, which now has the right information to give a factual, specific answer.
Implementation Snippet (The RAG logic inside your Lambda):


```
# Inside your lambda_handler, before calling the LLM
# (This is a simplified example)

# 1. Convert user query to an embedding
query_embedding = get_embedding(user_prompt) # A helper function calls the embedding model

# 2. Search the vector database
# Your vector_db_client would be specific to OpenSearch, Pinecone, etc.
relevant_docs = vector_db_client.search(query_embedding, top_k=3)
context_str = " ".join([doc['text'] for doc in relevant_docs])

# 3. Construct the final prompt for the LLM
final_prompt = f"""
Use the following context to answer the question. If the answer is not in the context, say you don't know.

Context:
{context_str}

Question:
{user_prompt}
"""

# 4. Now, send `final_prompt` to the LLM as in Shot 1
# ... rest of the code
```


# SHOT 3:

Shot 3: Adding Short-Term Memory (Conversational State)
RAG provides long-term knowledge, but a good chatbot also needs to remember the last few things you said.

Real-World Scenario: A multi-turn conversation where you can ask follow-up questions like "What about the other model?" and the bot knows what you're referring to.

New Architectural Component:

State Database: A fast key-value database like Amazon DynamoDB to store conversation history.
How it works:

When a conversation starts, a unique conversation_id is created.
The user sends a message. The Lambda function is triggered.
The Lambda uses the conversation_id to retrieve the past few messages from DynamoDB.
It prepends the chat history to the current prompt before sending it to the LLM.
After the LLM responds, the Lambda saves the new user message and the AI's response back to DynamoDB under the same conversation_id.
Implementation Snippet (DynamoDB logic):

``` python

# Inside your lambda_handler
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('YourChatHistoryTable')

def lambda_handler(event, context):
    # ...
    conversation_id = body.get('conversation_id')
    
    # 1. Get history
    response = table.get_item(Key={'conversation_id': conversation_id})
    history = response.get('Item', {}).get('messages', [])
    
    # 2. Prepare messages for LLM (history + new prompt)
    messages_for_llm = history + [{"role": "user", "content": user_prompt}]
    
    # ... call LLM with messages_for_llm ...
    
    # 3. After getting llm_output, update history
    history.append({"role": "user", "content": user_prompt})
    history.append({"role": "assistant", "content": llm_output})
    
    # 4. Save updated history back to DynamoDB
    table.put_item(Item={'conversation_id': conversation_id, 'messages': history})
    
    # ... return response ...
```

End-to-End: The Complete Picture
By combining these shots, you get a powerful, scalable, and intelligent serverless application.

Full Flow: A user with a conversation_id sends a prompt. The Lambda function:

Retrieves chat history from DynamoDB (Shot 3).
Converts the user's prompt to an embedding.
Searches the Vector DB for relevant documents (Shot 2).
Constructs a final, detailed prompt containing chat history, RAG context, and the user's question.
Calls the Managed LLM (e.g., Bedrock) for the final answer (Shot 1).
Updates the chat history in DynamoDB.
Returns the answer to the user.
This architecture is robust and forms the basis for most modern GenAI applications. You can even add more "shots" like Agents (giving the LLM tools to call other APIs) for even more advanced functionality.
