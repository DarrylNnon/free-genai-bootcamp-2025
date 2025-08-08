import os
import shutil
import subprocess
import sys
from pathlib import Path

import typer
from dotenv import load_dotenv
from openai import OpenAI

app = typer.Typer()


def check_for_tfsec():
    """Check if tfsec is installed and in the system's PATH."""
    if not shutil.which("tfsec"):
        typer.secho(
            "Error: tfsec is not installed or not in your PATH.", fg=typer.colors.RED
        )
        typer.echo("Please install it from: https://github.com/aquasecurity/tfsec")
        raise typer.Exit(1)


def create_terraform_prompt(user_request: str) -> str:
    """Creates a few-shot prompt for generating secure Terraform code."""
    return f"""
You are an expert DevSecOps engineer specializing in secure Terraform infrastructure.
Your task is to generate secure Terraform HCL code based on a user's request.

Follow these rules:
1.  Produce only Terraform HCL code.
2.  Do not add any explanations, comments, or markdown formatting like ```hcl.
3.  Apply security best practices (e.g., no hardcoded secrets, principle of least privilege, enable logging/encryption).
4.  The code should be complete and ready to run.

---
### Example 1
**User Request:** "An S3 bucket for private logs"

**Terraform Code:**
resource "aws_s3_bucket" "log_bucket" {{
  bucket = "my-private-log-bucket-unique-name"
}}

resource "aws_s3_bucket_public_access_block" "log_bucket_access_block" {{
  bucket = aws_s3_bucket.log_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}}

resource "aws_s3_bucket_server_side_encryption_configuration" "log_bucket_sse" {{
  bucket = aws_s3_bucket.log_bucket.id

  rule {{
    apply_server_side_encryption_by_default {{
      sse_algorithm     = "AES256"
    }}
  }}
}}

resource "aws_s3_bucket_versioning" "log_bucket_versioning" {{
  bucket = aws_s3_bucket.log_bucket.id
  versioning_configuration {{
    status = "Enabled"
  }}
}}
---
### User Request
**User Request:** "{user_request}"

**Terraform Code:**
"""


def generate_terraform_code(prompt: str) -> str:
    """Calls the OpenAI API to generate Terraform code."""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful DevSecOps assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        typer.secho(f"Error calling OpenAI API: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


def run_tfsec_scan(directory: Path) -> str:
    """Runs tfsec on the specified directory and returns the output."""
    typer.echo("\n--- 🛡️ Running tfsec security scan... ---\n")
    try:
        # Run tfsec with a custom format for cleaner output
        result = subprocess.run(
            ["tfsec", str(directory), "--format", "pretty"],
            capture_output=True,
            text=True,
            check=False,  # Don't raise exception on non-zero exit code
        )
        return result.stdout if result.stdout else result.stderr
    except FileNotFoundError:
        # This case should be caught by check_for_tfsec, but as a fallback
        typer.secho("Error: tfsec command not found.", fg=typer.colors.RED)
        raise typer.Exit(1)
    except Exception as e:
        typer.secho(f"An error occurred while running tfsec: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


@app.command()
def main(user_request: str):
    """
    IaC GPT Assistant: Generate and scan Terraform code from a natural language request.
    """
    load_dotenv()
    check_for_tfsec()

    if not os.getenv("OPENAI_API_KEY"):
        typer.secho("Error: OPENAI_API_KEY not found in .env file.", fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho("🤖 Generating Terraform code...", fg=typer.colors.CYAN)
    
    # --- Step 1: Input -> GPT ---
    prompt = create_terraform_prompt(user_request)
    generated_code = generate_terraform_code(prompt)

    # --- Step 2: GPT -> Terraform (File) ---
    output_dir = Path("generated")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "main.tf"
    output_file.write_text(generated_code)

    typer.secho("✅ Terraform code generated successfully!", fg=typer.colors.GREEN)
    typer.echo("\n--- 📄 Generated Terraform Code (generated/main.tf) ---\n")
    typer.secho(generated_code, fg=typer.colors.YELLOW)

    # --- Step 3: Terraform -> tfsec ---
    scan_results = run_tfsec_scan(output_dir)

    # --- Step 4: tfsec -> Report ---
    typer.echo("\n--- 📊 tfsec Report ---\n")
    typer.echo(scan_results)

    # Clean up the generated file after the run
    # shutil.rmtree(output_dir)

if __name__ == "__main__":
    app()

