import os
import sys
import subprocess
import json
import openai
import re

# --- Configuration ---
# It's best practice to use an environment variable for the API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    sys.exit("Error: OPENAI_API_KEY environment variable not set.")

GENERATED_TF_FILE = "generated.tf"
TFSEC_RESULTS_FILE = "tfsec-results.json"
PROMPT_TEMPLATE_FILE = "prompts/secure_iac_generator.md"

# --- Helper Functions ---

def call_openai_api(prompt, model="gpt-4o"):
    """A generic function to call the OpenAI ChatCompletion API."""
    try:
        client = openai.OpenAI()
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,  # Lower temperature for more predictable code generation
        )
        return completion.choices[0].message.content
    except openai.APIStatusError as e:
        if e.status_code == 429:
            error_details = e.response.json().get("error", {})
            if error_details.get("code") == "insufficient_quota":
                print("\n❌ Error: OpenAI API request failed due to insufficient quota.")
                print("   Please check your plan and billing details at https://platform.openai.com/account/billing/overview")
            else:
                print("\n❌ Error: OpenAI API request failed due to rate limiting.")
                print("   Please check your rate limits at https://platform.openai.com/account/limits and try again later.")
        else:
            print(f"\n❌ An unexpected OpenAI API error occurred: {e.status_code} - {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred when calling the OpenAI API: {e}")
        sys.exit(1)

def extract_terraform_code(response_text):
    """Extracts Terraform code from a Markdown code block."""
    match = re.search(r"```terraform\n(.*?)\n```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        # Fallback for a plain code block
        match = re.search(r"```\n(.*?)\n```", response_text, re.DOTALL)
        if match:
            return match.group(1).strip()
    print("Warning: Could not extract Terraform code from the response. Returning raw response.")
    return response_text

def run_tfsec():
    """Runs tfsec on the current directory and handles its output."""
    command = ["tfsec", ".", "--format", "json", "--out", TFSEC_RESULTS_FILE]
    try:
        # tfsec exits with non-zero status if issues are found. This is expected.
        subprocess.run(command, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        print("Error: 'tfsec' command not found. Is it installed and in your PATH?")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while running tfsec: {e}")
        sys.exit(1)

def generate_final_report_prompt(user_request, terraform_code, tfsec_results_json):
    """Creates the prompt for the final report generation."""
    try:
        if not tfsec_results_json.strip():
             tfsec_data = {"results": []}
        else:
             tfsec_data = json.loads(tfsec_results_json)

        if not tfsec_data.get("results"):
            scan_summary = "**Excellent! The `tfsec` scan found no security issues in the generated code.**"
        else:
            issue_count = len(tfsec_data["results"])
            scan_summary = (
                f"The `tfsec` scan found {issue_count} potential issue(s). Please analyze the following JSON output, "
                "explain the risks in a developer-friendly way, and suggest how the Terraform code could be improved to fix them."
            )
            scan_summary += f"\n\n**tfsec JSON results:**\n```json\n{tfsec_results_json}\n```"
    except (json.JSONDecodeError, KeyError):
        scan_summary = "Could not parse the tfsec results. Please review the raw output."
        scan_summary += f"\n\n**tfsec raw output:**\n```\n{tfsec_results_json}\n```"

    prompt = f"""
<PERSONA>
You are a DevSecOps expert reviewing a security scan of AI-generated Terraform code.
</PERSONA>

<TASK>
Your task is to create a final, human-readable report for the user in Markdown format.
The report must include:
1.  A confirmation of the user's original request.
2.  The full Terraform code that was generated.
3.  A clear, concise summary of the `tfsec` security scan results.
    - If there are no issues, state that clearly and congratulate the user.
    - If there are issues, explain the findings from the provided JSON. For each issue, describe the risk and suggest a specific code fix.
</TASK>

<CONTEXT>
- **User's Original Request:** "{user_request}"
- **Generated Terraform Code:**
  ```terraform
  {terraform_code}
  ```
- **Security Scan Analysis Task:**
  {scan_summary}
</CONTEXT>

<OUTPUT_FORMAT>
Please generate the final report now. Start with the title "## ✅ Secure IaC Generation & Scan Report".
</OUTPUT_FORMAT>
"""
    return prompt.strip()

def cleanup_files():
    """Removes the temporary files created during the process."""
    print("\n--- Cleanup Complete ---")
    if os.path.exists(GENERATED_TF_FILE):
        os.remove(GENERATED_TF_FILE)
    if os.path.exists(TFSEC_RESULTS_FILE):
        os.remove(TFSEC_RESULTS_FILE)

# --- Main Execution ---

def main():
    print("--- IaC GPT Assistant ---")

    if len(sys.argv) < 2:
        sys.exit("Usage: python iac_assistant.py \"<your infrastructure request>\"")
    user_request = sys.argv[1]

    # Step 1: Generate Terraform Code
    print("1. Generating Terraform code...")
    try:
        with open(PROMPT_TEMPLATE_FILE, "r") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        sys.exit(f"Error: Prompt template file not found at {PROMPT_TEMPLATE_FILE}")

    generation_prompt = prompt_template.replace("{user_request}", user_request)
    raw_response = call_openai_api(generation_prompt)
    terraform_code = extract_terraform_code(raw_response)

    with open(GENERATED_TF_FILE, "w") as f:
        f.write(terraform_code)
    print(f"   -> Terraform code saved to '{GENERATED_TF_FILE}'")

    # Step 2: Scan with tfsec
    print("\n2. Scanning generated code with tfsec...")
    run_tfsec()
    print(f"   -> tfsec scan complete. Results may be in '{TFSEC_RESULTS_FILE}'")

    # Step 3: Generate Final Report
    print("\n3. Generating final report...")
    tfsec_results_content = ""
    try:
        with open(TFSEC_RESULTS_FILE, "r") as f:
            tfsec_results_content = f.read()
    except FileNotFoundError:
        print("   -> No tfsec results file found, assuming no issues.")
        pass

    report_prompt = generate_final_report_prompt(user_request, terraform_code, tfsec_results_content)
    final_report = call_openai_api(report_prompt)

    print("\n--- 🤖 Final Report ---")
    print(final_report)

if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup_files()
