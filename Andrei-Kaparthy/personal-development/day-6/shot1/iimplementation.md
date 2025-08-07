# step-by-step guide to implement and deploy "Shot 1" from end to end, turning the conceptual plan into a practical reality.

# Prerequisites
Before you begin, make sure you have the following installed and configured:

- An AWS Account with access to IAM, Lambda, and API Gateway.
- AWS CLI configured with your credentials.
- Python 3.9+ and pip installed on your local machine.
- **Amazon Bedrock Model Access**: You must request and have access granted to the `Anthropic Claude 3 Sonnet` model in the AWS region you are deploying to (e.g., `us-east-1`). You can do this in the Amazon Bedrock console under "Model access".
- A text editor or IDE (like VS Code).

# Step 1: Set Up Your Project Directory
First, create the necessary files on your local machine.

1- Create a new directory for your project and navigate into it:

```sh
mkdir shot1-project
cd shot1-project
```
 2- inside this directory, create lamnda_function with the provided code:

 ```python
 # shot1-project/lambda_function.py
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

3-  Next, create the requirements.txt file:

```sh
shot1-project/requirements.txt
boto3
```

# Step 2: Create the Deployment package

Now, package your function and its dependies into a .zip file that you can upload to lamnda.

1.  install the dependencies into a local directory:

```sh
pip install -r requirements.txt -t ./package
```

2.  copy your lamnda function code into the directory:

```sh
cp lambda_function.py ./package/
```

3. Navigate into the package directory and zip its contents:

```sh
cd ./package
zip -r ../shot1-project.zip .# Step 3: Deploy
cd ..
```

you should now have a `deployment.zip` file in your sho1-project directory.

# Step 3: Create the lamnda execution Role

Your lamnda function needs permission to run and to call the Bedrock service. You'll create an IAM role for this.

1.  create a trust policy named lambda-trust-policy.json:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

2.  Create the IAM role using the AWS cli

```sh
aws iam create-role --role-name Shot1-Lambda-Role --assume-role-policy-document file://lambda-trust-policy.json
```

3.  Create a permissions policy file named lambda-permissions.json: This grands access to CloudWatch for logging and Bedrock for invoking the model.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": "bedrock:InvokeModel",
            "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
        }
    ]
}
```

4.  Attach the persmissions policy to the role you created:

```sh
aws iam put-role-policy --role-name Shot1-Lambda-Role --policy-name Shot1-Lambda-Permissions --policy-document file://lambda-permissions.json
```

# Step 4: Create the Lambda function

With the deployment package and role ready, you can now create the Lmanda function.

1.  Run the following AWS CLI command. Make sure to replace <your-aws-account-id> and <your-aws-region> with your actual account ID and region (e.g., us-east-1).

```sh
aws lambda create-function \
  --function-name shot1-basic-api-call \
  --runtime python3.9 \
  --role arn:aws:iam::<your-aws-account-id>:role/Shot1-Lambda-Role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://deployment.zip \
  --timeout 30 \
  --memory-size 256 \
  --region <your-aws-region>
```

# Step 5: Create and Configure the API Gateway
Finally, create an HTTP endpoint to trigger your Lambda function.

Go to the AWS Lambda Console in your browser.
Find and click on your shot1-basic-api-call function.
Click the "Add trigger" button.
Select "API Gateway" as the trigger source.
Choose "Create a new API".
Select "HTTP API" for the API type.
For security, select "Open".
Click "Add".
After a moment, the trigger will be created. In the "Triggers" section, you will now see an API endpoint URL. Copy this URL.

Step 6: Test Your API
You can now send a POST request to your new endpoint using a tool like curl.

Open your terminal and replace <your-api-gateway-url> with the URL you copied.

```sh
curl -X POST \
  '<your-api-gateway-url>' \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Explain what a serverless function is in one sentence."}'
```

2.  You should receive a JSON response from the Cluade 3 Sonnet model, like this:

```json

{"response":"A serverless function is a piece of code that runs in response to an event, managed by a cloud provider, without the need to provision or manage any underlying servers."}
```

Congratulations! You have successfully implemented and deploy a serverless GenAI application from end to end.

