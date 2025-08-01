import os
import sys
import json
from openai import OpenAI

# It's best practice to use an environment variable for the API key
# In GitHub Actions, this will be set as a secret.
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    sys.exit("Error: OPENAI_API_KEY environment variable not set.")

client = OpenAI(api_key=api_key)

def get_scan_summary(scan_json_data):
    """
    Uses an LLM to summarize security scan results.
    """
    prompt = f"""
    You are a DevSecOps assistant. Your task is to summarize a security scan report for a developer.
    The report is in JSON format from the Trivy scanner.

    Analyze the following Trivy JSON output and provide a concise, human-readable summary in Markdown format.

    The summary should include:
    1. An overall assessment (e.g., "Critical vulnerabilities found!").
    2. A brief list of the top 3-5 most critical vulnerabilities.
    3. For each listed vulnerability, mention the Package, Severity, and a simple one-sentence description of the risk.
    4. A concluding sentence encouraging the developer to review the full report.

    Do not include remediation advice unless it's present in the JSON. Keep the summary brief and to the point.

    Trivy JSON data:
    ```json
    {scan_json_data}
    ```

    Markdown Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or gpt-4 for better results
            messages=[
                {"role": "system", "content": "You are a helpful DevSecOps assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == "__main__":
    # The Trivy JSON output will be piped into this script
    json_input = sys.stdin.read()
    
    # Basic validation
    if not json_input:
        sys.exit("Error: No JSON data piped to script.")

    summary = get_scan_summary(json_input)
    print(summary)