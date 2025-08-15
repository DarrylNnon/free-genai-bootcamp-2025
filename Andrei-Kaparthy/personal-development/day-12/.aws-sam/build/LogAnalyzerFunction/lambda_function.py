import os
import json
import gzip
import base64
import openai

# --- Environment Variables ---
# It's best practice to use an environment variable for the API key.
# The SAM template passes this in from a deployment parameter.
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("Error: OPENAI_API_KEY environment variable not set.")
openai.api_key = API_KEY

# --- Constants ---
PROMPT_TEMPLATE_PATH = "prompts/log_analyzer_prompt.md"

# --- Prompt Loading ---
# Load the prompt template from the file at cold start for efficiency.
try:
    with open(PROMPT_TEMPLATE_PATH, "r") as f:
        PROMPT_TEMPLATE = f.read()
except FileNotFoundError:
    raise RuntimeError(f"Fatal: Prompt file not found at {PROMPT_TEMPLATE_PATH}")

def analyze_log_entry(log_entry: str) -> str:
    """
    Uses an LLM to analyze a single log entry for security threats.

    Args:
        log_entry: The raw log string to be analyzed.

    Returns:
        A string containing the AI's analysis in Markdown format.
    """
    print(f"Analyzing log entry: {log_entry}")

    # Inject the log entry into our sophisticated few-shot prompt
    prompt = PROMPT_TEMPLATE.format(log_entry=log_entry)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # Use gpt-4 for higher accuracy
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1, # Low temperature for factual, consistent output
            max_tokens=500,
        )
        analysis = response.choices[0].message.content
        print("Successfully received analysis from AI.")
        return analysis.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return f"Error: Could not generate analysis. Details: {e}"

def handler(event, context):
    """
    AWS Lambda handler function.
    This function is triggered by a CloudWatch Logs subscription filter.
    """
    print("Log Analyzer function invoked.")

    # CloudWatch Logs payload is compressed and base64-encoded.
    try:
        compressed_payload = base64.b64decode(event['awslogs']['data'])
        uncompressed_payload = gzip.decompress(compressed_payload)
        log_payload = json.loads(uncompressed_payload)
        print(f"Successfully decoded payload for log group: {log_payload['logGroup']}")
    except Exception as e:
        print(f"Error decoding CloudWatch Logs data: {e}")
        return {"statusCode": 500, "body": "Error decoding payload"}

    # Process each log event in the payload.
    for log_event in log_payload['logEvents']:
        log_entry = log_event['message']

        # --- Core Logic ---
        # 1. Get AI analysis for the log entry
        ai_analysis = analyze_log_entry(log_entry)

        # 2. Print a structured report to the Lambda's logs for review.
        # This creates a permanent record of the finding.
        report = {
            "source_log_group": log_payload.get('logGroup'),
            "source_log_stream": log_payload.get('logStream'),
            "original_log": log_entry,
            "ai_security_analysis": ai_analysis
        }
        print(json.dumps(report, indent=2))

    return {"statusCode": 200, "body": "Successfully processed logs."}
