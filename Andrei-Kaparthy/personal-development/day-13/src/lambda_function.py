import os
import gzip
import base64
import json
import logging
from openai import OpenAI

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize OpenAI client
# It's best practice to use environment variables for API keys
try:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None

def load_prompt_template():
    """Loads the prompt template from the file."""
    try:
        with open("prompts/log_analyzer_prompt.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("Prompt template file not found.")
        return None

def get_ai_analysis(log_data, prompt_template):
    """Sends the log data to OpenAI for analysis and expects a JSON response."""
    if not client or not prompt_template:
        return None

    prompt = prompt_template.format(log_data=log_data)

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful security analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"} # Enforce JSON output
        )
        analysis_content = response.choices[0].message.content
        return json.loads(analysis_content)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON response from AI: {analysis_content}")
        return {"error": "Invalid JSON response from AI", "raw_response": analysis_content}
    except Exception as e:
        logger.error(f"An error occurred with the OpenAI API call: {e}")
        return {"error": str(e)}

def handler(event, context):
    """
    AWS Lambda handler for processing CloudWatch log events.
    """
    # 1. Decode and decompress the log data from CloudWatch
    try:
        compressed_payload = base64.b64decode(event['awslogs']['data'])
        uncompressed_payload = gzip.decompress(compressed_payload)
        log_payload = json.loads(uncompressed_payload)
    except Exception as e:
        logger.error(f"Failed to decode/decompress log data: {e}")
        return {'statusCode': 500, 'body': 'Error processing log data'}

    prompt_template = load_prompt_template()
    if not prompt_template:
        return {'statusCode': 500, 'body': 'Could not load prompt template'}

    # 2. Process each log event
    for log_event in log_payload['logEvents']:
        log_message = log_event['message']
        logger.info(f"Analyzing log: {log_message}")

        # 3. Get analysis from GPT
        analysis = get_ai_analysis(log_message, prompt_template)

        if analysis:
            # 4. Log the structured analysis
            # Use json.dumps for pretty printing the JSON output
            logger.info("--- AI Security Analysis ---")
            logger.info(json.dumps(analysis, indent=2))

            # 5. SIMULATE REAL-TIME ALERTING
            severity = analysis.get("severity", "None").upper()
            if severity in ["HIGH", "CRITICAL"]:
                alert_message = f"🚨🚨🚨 {severity} SEVERITY ALERT DETECTED! 🚨🚨🚨"
                logger.warning(alert_message)
                logger.warning(f"Threat Type: {analysis.get('threat_type')}")
                logger.warning(f"Recommendation: {analysis.get('recommended_action')}")
            logger.info("--- End of Analysis ---")