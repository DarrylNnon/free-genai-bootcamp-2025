import boto3
import json
import os

# It's best practice to initialize clients outside the handler
bedrock_runtime = boto3.client(service_name='bedrock-runtime')
dynamodb = boto3.resource('dynamodb')

# Get the DynamoDB table name from environment variables
TABLE_NAME = os.environ.get('CHAT_HISTORY_TABLE')
if not TABLE_NAME:
    raise ValueError("Missing environment variable: CHAT_HISTORY_TABLE")

table = dynamodb.Table(TABLE_NAME)

# --- RAG Simulation (from Shot 2) ---
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
    # 1. Get prompt and conversation_id from the API Gateway event
    body = json.loads(event.get('body', '{}'))
    user_prompt = body.get('prompt')
    conversation_id = body.get('conversation_id')

    if not user_prompt or not conversation_id:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: `prompt` and `conversation_id` are required.')
        }

    try:
        # --- Short-Term Memory Step ---
        # 2. Retrieve chat history from DynamoDB
        response = table.get_item(Key={'conversation_id': conversation_id})
        # The history is a list of messages in Claude 3 format
        history = response.get('Item', {}).get('messages', [])

        # --- RAG Steps (Long-Term Memory) ---
        query_embedding = get_embedding(user_prompt)
        relevant_context = search_vector_db(query_embedding)

        # 4. Construct the final prompt with history and RAG context
        final_user_content = f"""
Use the following context to answer the question. If the answer is not in the context, say you don't know.

Context:
{relevant_context}

Question:
{user_prompt}
"""
        # Combine past conversation with the new, context-augmented prompt
        messages_for_llm = history + [
            {"role": "user", "content": [{"type": "text", "text": final_user_content}]}
        ]

        # 5. Prepare the payload for the LLM
        model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        prompt_config = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "messages": messages_for_llm
        }

        # 6. Invoke the model via the Bedrock API
        response = bedrock_runtime.invoke_model(
            body=json.dumps(prompt_config),
            modelId=model_id
        )
        response_body = json.loads(response.get('body').read())
        llm_output_content = response_body['content']
        llm_output_text = llm_output_content[0]['text']

        # --- Update Short-Term Memory ---
        # 7. Save the updated history back to DynamoDB
        # We store the original user prompt and the full AI response content block
        new_user_message = {"role": "user", "content": [{"type": "text", "text": user_prompt}]}
        new_assistant_message = {"role": "assistant", "content": llm_output_content}
        
        updated_history = history + [new_user_message, new_assistant_message]
        
        table.put_item(
            Item={
                'conversation_id': conversation_id, 
                'messages': updated_history
            }
        )

        return {
            'statusCode': 200, 
            'body': json.dumps({'response': llm_output_text})
        }

    except Exception as e:
        print(f"Error processing request: {e}")
        return {'statusCode': 500, 'body': json.dumps('Error processing your request.')}