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