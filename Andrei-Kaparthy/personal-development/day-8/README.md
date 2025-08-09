# Day 8 Project: IaC GPT Assistant

Welcome to Day 8! Today's project is to build an end-to-end "Infrastructure as Code (IaC) GPT Assistant." This command-line tool takes a natural language request (e.g., "create a secure database") and orchestrates an entire DevSecOps workflow.

## 🚀 The Flow

The assistant follows this automated sequence:

**Input → GPT → Terraform → tfsec → Report**

1.  **Input**: You provide a plain English request for cloud infrastructure.
2.  **GPT**: The assistant uses a sophisticated "few-shot" prompt to ask a Large Language Model (LLM) to generate secure Terraform code based on your request.
3.  **Terraform**: The generated code is saved to a local file.
4.  **tfsec**: The `tfsec` security scanner analyzes the generated code for misconfigurations and vulnerabilities.
5.  **Report**: The assistant uses the LLM again to interpret the `tfsec` results and generate a final, human-readable report that includes the code, the findings, and suggestions for improvement.

## 🎯 Objective

*   To build a practical, AI-driven DevSecOps tool.
*   To practice few-shot prompting for generating high-quality, secure code.
*   To automate the feedback loop of code generation and security scanning.
*   To integrate multiple tools (`python`, `openai`, `tfsec`) into a single workflow.

## 🛠️ Setup

### 1. Environment Variables

This script requires an OpenAI API key. Set it as an environment variable in your terminal. If you are using Gitpod, you can set this in your Gitpod Account settings.

```bash
export OPENAI_API_KEY="sk-..."
```

### 2. Python Dependencies

Install the required Python library:

```bash
pip install -r requirements.txt
```

### 3. Tooling (for Gitpod)

This project requires `terraform` and `tfsec`. If you are using the Gitpod environment for this bootcamp, these tools are automatically installed for you based on the `.gitpod.yaml` configuration file at the root of the repository.

If you are running locally, please ensure you have Terraform and tfsec installed and available in your system's PATH.

## 🏃 How to Run

Execute the script from your terminal, passing your infrastructure request as a string argument.

**Example:**

```bash
python iac_assistant.py "Create a secure S3 bucket for private logs"
```

The script will then execute the full workflow and print the final report to your console.

### Example Output

```
--- IaC GPT Assistant ---
1. Generating Terraform code...
   -> Terraform code saved to 'generated.tf'

2. Scanning generated code with tfsec...
   -> tfsec scan complete. Results saved to 'tfsec-results.json'

3. Generating final report...

--- 🤖 Final Report ---

## ✅ Secure IaC Generation & Scan Report

Here is the summary of your request to "Create a secure S3 bucket for private logs".

### Generated Terraform Code

... (Terraform code appears here) ...

### 🛡️ Security Scan Summary

**Excellent! The `tfsec` scan found no security issues in the generated code.**

--- Cleanup Complete ---
```
