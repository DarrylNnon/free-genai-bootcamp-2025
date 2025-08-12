import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from openai import OpenAI


def get_prompt_template(name: str) -> str:
    """Loads a prompt template from the prompts directory."""
    prompt_path = Path(__file__).parent / "prompts" / name
    try:
        with open(prompt_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Prompt template '{name}' not found.")
        return ""


def call_openai_api(prompt: str, model: str = "gpt-4-turbo-preview") -> str | None:
    """Calls the OpenAI API and returns the response content."""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None


def extract_code_block(text: str) -> str:
    """Extracts the content of the first markdown code block."""
    match = re.search(r"```(?:terraform|hcl|json)?\n(.*?)\n```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def generate_terraform(user_request: str) -> str | None:
    """Generates Terraform code from a user request."""
    prompt_template = get_prompt_template("secure_iac_generator.md")
    prompt = prompt_template.format(user_request=user_request)
    response = call_openai_api(prompt)
    return extract_code_block(response) if response else None


def run_security_scan(terraform_code: str) -> dict | None:
    """Runs tfsec on the terraform code and returns the JSON output."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = Path(temp_dir) / "main.tf"
        with open(temp_file_path, "w") as f:
            f.write(terraform_code)

        command = ["tfsec", temp_dir, "--format", "json"]
        try:
            # tfsec exits with non-zero status if issues are found, which is expected.
            # We capture stderr to see actual errors.
            result = subprocess.run(
                command, check=False, capture_output=True, text=True
            )
            if result.returncode != 0 and "panic" in result.stderr:
                 print(f"Error: tfsec panicked. Stderr: {result.stderr}")
                 return {"results": [{"rule_description": "tfsec failed to run.", "long_id": "TFSEC_ERROR", "severity": "CRITICAL"}]}

            # If tfsec finds issues, it prints JSON to stdout and exits > 0.
            # If no issues, it prints empty JSON and exits 0.
            # If stdout is empty, there might have been an error not caught above.
            if not result.stdout.strip():
                return {"results": []}

            return json.loads(result.stdout)

        except FileNotFoundError:
            print("Error: 'tfsec' command not found. Please ensure it's installed and in your PATH.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Failed to decode tfsec JSON output. stdout: {result.stdout}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during security scan: {e}")
            return None


def fix_terraform(terraform_code: str, tfsec_results_json: str) -> str | None:
    """Attempts to fix Terraform code based on tfsec results."""
    prompt_template = get_prompt_template("iac_fixer.md")
    prompt = prompt_template.format(
        terraform_code=terraform_code, tfsec_results_json=tfsec_results_json
    )
    response = call_openai_api(prompt)
    return extract_code_block(response) if response else None


def generate_report(
    user_request: str, terraform_code: str, tfsec_results_json: str
) -> str | None:
    """Generates a final, human-readable report."""
    prompt_template = get_prompt_template("iac_report_generator.md")
    prompt = prompt_template.format(
        user_request=user_request,
        terraform_code=terraform_code,
        tfsec_results_json=tfsec_results_json,
    )
    return call_openai_api(prompt, model="gpt-4-turbo-preview")


def process_iac_request(user_request: str) -> dict:
    """
    Main orchestrator function for the IaC GPT Assistant workflow.
    Includes prompt chaining for auto-remediation.
    """
    print("1. Generating initial Terraform code...")
    terraform_code = generate_terraform(user_request)
    if not terraform_code:
        return {"error": "Failed to generate initial Terraform code from request."}

    print("2. Running first security scan...")
    tfsec_results = run_security_scan(terraform_code)
    if tfsec_results is None:
        return {"error": "The security scanner (tfsec) failed to run."}

    final_code = terraform_code
    final_results = tfsec_results
    
    # Prompt Chaining & Fallback Logic
    if final_results.get("results"):
        print("3. Issues found. Attempting AI-powered remediation...")
        fixed_code = fix_terraform(terraform_code, json.dumps(tfsec_results))
        
        if fixed_code and fixed_code != terraform_code:
            print("4. AI provided a fix. Running second security scan...")
            second_scan_results = run_security_scan(fixed_code)
            if second_scan_results is not None:
                final_code = fixed_code
                final_results = second_scan_results
                print("   Scan on fixed code complete.")
            else:
                print("   Scan on fixed code failed. Falling back to original code.")
        else:
            print("   AI did not provide a fix. Using original code for report.")

    print("5. Generating final report...")
    final_report = generate_report(
        user_request, final_code, json.dumps(final_results)
    )
    if not final_report:
        return {"error": "Failed to generate the final report."}

    print("Workflow complete.")
    return {
        "user_request": user_request,
        "terraform_code": final_code,
        "report": final_report,
    }
