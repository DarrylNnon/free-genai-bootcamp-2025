import os
import json
import logging
import requests
from pathlib import Path
from openai import OpenAI

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize clients
# It's best practice to initialize clients outside the handler function
# to take advantage of Lambda's execution context reuse.
try:
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
    PROMPT_FILE_PATH = Path(os.environ.get("PROMPT_FILE", "prompts/cost_anomaly_remediation.md"))
    AGENT_MODE = os.environ.get("AGENT_MODE", "ALERT_ONLY") # Default to safe mode
except KeyError as e:
    logger.error(f"Missing environment variable: {e}")
    # This will cause the Lambda initialization to fail, which is intended.
    raise

def load_prompt_template() -> str:
    """Loads the prompt template from the specified file."""
    try:
        with open(PROMPT_FILE_PATH, "r") as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Prompt file not found at {PROMPT_FILE_PATH}")
        raise

def get_ai_analysis(anomaly_data: dict) -> dict | None:
    """Sends anomaly data to the LLM and gets a structured analysis."""
    prompt_template = load_prompt_template()
    
    # Inject the real anomaly data into the prompt
    prompt = prompt_template.format(anomaly_data=json.dumps(anomaly_data, indent=2))

    try:
        logger.info("Calling OpenAI API for analysis...")
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2, # Lower temperature for more deterministic, factual output
            response_format={"type": "json_object"},
        )
        analysis_text = response.choices[0].message.content
        logger.info(f"Received analysis: {analysis_text}")
        return json.loads(analysis_text)
    except Exception as e:
        logger.error(f"Error calling OpenAI API or parsing response: {e}")
        return None

def post_to_slack(message: str):
    """Posts a message to a Slack channel."""
    if not SLACK_WEBHOOK_URL:
        logger.warning("SLACK_WEBHOOK_URL not set. Skipping Slack notification.")
        return
    
    try:
        payload = {"text": message, "mrkdwn": True}
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        logger.info("Successfully posted to Slack.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error posting to Slack: {e}")

def handle_remediation(analysis: dict):
    """Handles the remediation plan from the AI analysis."""
    plan = analysis.get("remediation_plan", {})
    plan_type = plan.get("type")
    
    if plan_type == "SLACK_ALERT":
        message = f"🚨 *FinOps Agent Alert* 🚨\n\n*Summary:* {analysis.get('summary')}\n*Recommendation:* {plan.get('description')}\n*Details:* ```{plan.get('payload')}```"
        post_to_slack(message)
    elif plan_type == "MANUAL_INVESTIGATION":
        message = f"🕵️ *FinOps Agent: Manual Investigation Required* 🕵️\n\n*Summary:* {analysis.get('summary')}\n*Analysis:* {analysis.get('root_cause_analysis')}\n*Recommendation:* {plan.get('description')}\n*Details:* ```{plan.get('payload')}```"
        post_to_slack(message)
    elif plan_type == "AUTOMATED_CLI":
        cli_command = plan.get('payload')
        is_destructive = plan.get('is_destructive', True) # Default to destructive if not specified
        
        message = f"🤖 *FinOps Agent: Automated Action Proposed* 🤖\n\n*Summary:* {analysis.get('summary')}\n*Action:* `{plan.get('type')}`\n*Command:* ```{cli_command}```\n*Destructive:* `{is_destructive}`"
        
        if AGENT_MODE == "AUTO_REMEDIATE" and not is_destructive:
            # In a real-world scenario, you would use boto3 to execute the action.
            # For this example, we will just log and alert.
            # e.g., result = os.system(cli_command)
            logger.info(f"AGENT_MODE is AUTO_REMEDIATE. Would execute safe command: {cli_command}")
            message += "\n\n*Status:* `EXECUTED` (Simulated)"
        else:
            logger.warning(f"AGENT_MODE is {AGENT_MODE} or action is destructive. Skipping execution.")
            message += f"\n\n*Status:* `SKIPPED` (Mode: {AGENT_MODE}, Destructive: {is_destructive})"
        
        post_to_slack(message)
    else:
        logger.warning(f"Unknown remediation plan type: {plan_type}")
        post_to_slack(f"⚠️ *FinOps Agent: Error*\n\nReceived unknown remediation plan type: `{plan_type}` for anomaly `{analysis.get('anomaly_id')}`")


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    Triggered by an SNS message from AWS Cost Anomaly Detection.
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    # Extract the message from the SNS event
    try:
        # The anomaly data is a JSON string inside the SNS message
        message_str = event['Records'][0]['Sns']['Message']
        anomaly_data = json.loads(message_str)
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        logger.error(f"Error parsing SNS event: {e}")
        return {"statusCode": 400, "body": "Error parsing event."}

    logger.info(f"Analyzing anomaly: {anomaly_data.get('anomalyId')}")
    
    # Get AI analysis
    analysis = get_ai_analysis(anomaly_data)
    
    if not analysis:
        post_to_slack(f"⚠️ *FinOps Agent: Analysis Failed*\n\nCould not get AI analysis for anomaly data: ```{json.dumps(anomaly_data)}```")
        return {"statusCode": 500, "body": "Failed to get AI analysis."}
        
    # Handle the remediation based on the analysis
    handle_remediation(analysis)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Analysis complete.", "analysis": analysis})
    }