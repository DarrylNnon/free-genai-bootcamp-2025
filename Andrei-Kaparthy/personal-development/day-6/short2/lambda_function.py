import boto3
import json

# It's best practice to initialize clients outside the handler
bedrock_runtime = boto3.client(service_name='bedrock-runtime')

# --- RAG Simulation ---
# In a real application, this would call an embedding model (e.g., Amazon Titan)
def get_embedding(text):
    """Simulates converting text to a vector embedding."""
    print(f"Generating embedding for: {text}")
    # Return a dummy vector. The length and values don't matter for this simulation.
    return [0.1] * 1536 

def search_vector_db(embedding):
    """Simulates searching a vector database with the given embedding."""
    print("Searching vector database for relevant context...")
    # In a real RAG setup, this would query a vector store like OpenSearch,
    # Pinecone, or ChromaDB and return relevant document chunks.
    # For this simulation, we'll return a hardcoded context.
    return """
    Context from knowledge base:
    - The Serverless GenAI Application uses AWS Lambda for compute.
    - Shot 1 is a basic API call to an LLM.
    - Shot 2 adds Retrieval-Augmented Generation (RAG) to provide long-term memory from a knowledge base.
    - RAG works by retrieving relevant documents and adding them as context to the LLM prompt.
    """

def lambda_handler(event, context):
    # 1. Get the user's prompt from the API Gateway event
    body = json.loads(event.get('body', '{}'))
    user_prompt = body.get('prompt')

    if not user_prompt:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: No prompt provided.')
        }

    # --- RAG Steps ---
    # 2. Convert user prompt to an embedding
    query_embedding = get_embedding(user_prompt)

    # 3. Search the vector database for relevant context
    relevant_context = search_vector_db(query_embedding)

    # 4. Construct the final prompt with the retrieved context
    final_prompt = f"""
Use the following context to answer the question. If the answer is not in the context, say you don't know.

Context:
{relevant_context}

Question:
{user_prompt}
"""

    # 5. Prepare the payload for the LLM
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

    # 6. Invoke the model via the Bedrock API
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