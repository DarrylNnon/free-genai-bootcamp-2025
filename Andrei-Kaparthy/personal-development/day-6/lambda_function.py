import boto3
import json

# It's best practice to initialize clients outside the handler
bedrock_runtime = boto3.client(service_name='bedrock-runtime')
# In a real application, you would initialize your vector DB client here
# from my_vector_db_client import VectorDBClient
# vector_db_client = VectorDBClient()

def get_embedding(text, model_id='amazon.titan-embed-text-v1'):
    """
    Placeholder function to convert text to an embedding using Bedrock.
    In a real application, this would also be part of a separate module.
    """
    body = json.dumps({"inputText": text})
    response = bedrock_runtime.invoke_model(
        body=body, modelId=model_id, contentType='application/json', accept='application/json'
    )
    response_body = json.loads(response.get('body').read())
    return response_body.get('embedding')

def search_vector_db(query_embedding, top_k=3):
    """
    Placeholder for searching your vector database.
    The implementation depends on your choice (OpenSearch, Pinecone, etc.).
    """
    # This is a mock response.
    print(f"Searching vector DB for embedding (first 5 values): {query_embedding[:5]}...")
    return [
        {'text': 'To reset your password, go to the settings page and click "Reset Password".'},
        {'text': 'Product X manuals state that password resets are handled via the user profile section.'},
        {'text': 'Company policy requires passwords to be at least 12 characters long.'}
    ]


def lambda_handler(event, context):
    # 1. Get the user's prompt from the API Gateway event
    body = json.loads(event.get('body', '{}'))
    user_prompt = body.get('prompt')

    if not user_prompt:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: No prompt provided.')
        }

    # --- Shot 2: RAG Logic ---
    # 2a. Convert user query to an embedding
    try:
        query_embedding = get_embedding(user_prompt)
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return {'statusCode': 500, 'body': json.dumps('Error processing your request.')}

    # 2b. Search the vector database for relevant context
    relevant_docs = search_vector_db(query_embedding, top_k=3)
    context_str = " ".join([doc['text'] for doc in relevant_docs])

    # 2c. Construct the final prompt for the LLM with the retrieved context
    final_prompt = f"""
Use the following context to answer the question. If the answer is not in the context, say you don't know.

Context:
{context_str}

Question:
{user_prompt}
"""
    # --- End of Shot 2 Logic ---

    # 3. Prepare the payload for the LLM (this example is for Claude 3)
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    prompt_config = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": final_prompt}]
            }
        ]
    }

    # 4. Invoke the model via the Bedrock API
    try:
        response = bedrock_runtime.invoke_model(
            body=json.dumps(prompt_config),
            modelId=model_id,
            contentType='application/json',
            accept='application/json'
        )
        
        # 5. Parse the response and extract the text
        