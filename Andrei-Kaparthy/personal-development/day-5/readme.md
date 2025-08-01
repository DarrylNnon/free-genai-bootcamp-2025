# Day 5: LLM-Powered Security Audits and Workflow Automation

Welcome to Day 5 of your GenAI DevSecOps journey! Today, we'll tackle two critical, hands-on projects:

1.  **Creating an LLM-powered audit prompt** to find security misconfigurations in CI/CD YAML files.
2.  **Automating a security scanning workflow** where an LLM summarizes the findings from tools like Trivy.

This guide provides the end-to-end instructions, prompts, and code to complete these tasks.

---

## Project 1: Create an LLM Audit Prompt for CI/CD YAML

The goal here is to build a highly effective prompt that can analyze a GitHub Actions workflow file (`.yml`) and identify potential security vulnerabilities. We will use the **few-shot prompting** technique to teach the model *how* to think like a security expert.

### Step 1: Understanding the Few-Shot Prompt Structure

A good few-shot prompt provides the model with a role (persona), a clear task, and most importantly, examples of what "bad" looks like and what "good" looks like. This guides the model to produce more accurate and relevant results than a simple zero-shot ("find vulnerabilities in this file") request.

Our prompt will have four parts:
1.  **`<PERSONA>`**: Defines the expert role the AI should adopt.
2.  **`<TASK>`**: Clearly states the objective.
3.  **`<FEW-SHOT-EXAMPLES>`**: Provides concrete examples of insecure code and its secure alternative, along with explanations.
4.  **`<YOUR-REQUEST>`**: The section where you'll place the YAML code you want to be audited.

### Step 2: The Master Audit Prompt Template

Here is the complete, reusable prompt template. You can save this and use it to audit any GitHub Actions workflow.

<details>
<summary>Click to view the CI/CD YAML Security Audit Prompt</summary>

```markdown
<PERSONA>
You are a world-class DevSecOps and CI/CD security expert. Your expertise lies in identifying subtle and critical security misconfigurations in GitHub Actions workflows. You are meticulous, precise, and always provide actionable feedback with clear reasoning.
</PERSONA>

<TASK>
Analyze the provided GitHub Actions workflow YAML file for security vulnerabilities. For each vulnerability you find, describe the risk, suggest a concrete code fix, and explain why the fix improves security. Use the examples below as a guide for the format and depth of your analysis.
</TASK>

<FEW-SHOT-EXAMPLES>
---
### Example 1: Overly Permissive Permissions
**Insecure Code:**
```yaml
name: Insecure Workflow
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: A step that does something
        run: echo "This step has write-all permissions!"
```

**Analysis:**
- **Vulnerability:** The workflow has no `permissions` block defined at the top level or job level. This grants it the default, highly permissive `write-all` scope for the `GITHUB_TOKEN`.
- **Risk:** A compromised job or action could push malicious code to your repository, modify issues, create releases, and more. This violates the principle of least privilege.
- **Remediation:** Explicitly define the minimal permissions required for the job. If the job only needs to read contents, set `permissions` accordingly.
**Secure Code:**
```yaml
name: Secure Workflow
on: [push]
permissions:
  contents: read # Set default permissions for all jobs to read-only

jobs:
  build:
    runs-on: ubuntu-latest
    # This job inherits the read-only permissions
    steps:
      - name: A step that does something
        run: echo "This step now has read-only permissions."
```
---
### Example 2: Vulnerable to Command Injection
**Insecure Code:**
```yaml
name: Insecure Command Injection
on:
  issue_comment:
    types: [created]
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Potentially injectable step
        run: |
          echo "Adding label ${{ github.event.comment.body }} to issue"
          gh label create "${{ github.event.comment.body }}"
```
**Analysis:**
- **Vulnerability:** The workflow directly uses user-provided input (`github.event.comment.body`) in a `run` script.
- **Risk:** A malicious user could craft a comment like `bug; rm -rf /` to inject arbitrary commands. The shell would execute `gh label create "bug"` and then `rm -rf /`, causing catastrophic damage.
- **Remediation:** Treat all user input as untrusted. Pass it to the script via an environment variable and handle it safely within the action's code, or use actions designed to handle such inputs securely.
**Secure Code:**
```yaml
name: Secure Command Handling
on:
  issue_comment:
    types: [created]
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Use an intermediate action or env var
        env:
          COMMENT_BODY: ${{ github.event.comment.body }}
        run: |
          # The command is now safer as the input is in an env var.
          # A better approach is to use a dedicated action that sanitizes input.
          echo "Adding label $COMMENT_BODY to issue"
          gh label create "$COMMENT_BODY"
```
---
</FEW-SHOT-EXAMPLES>

<YOUR-REQUEST>
Now, apply the same rigorous security analysis to the following GitHub Actions workflow.

### Insecure Code (Your Turn):
```yaml
# PASTE YOUR CI/CD YAML CODE HERE
```
</YOUR-REQUEST>
```
</details>

### Step 3: How to Use the Prompt

1.  Copy the entire prompt template from the section above.
2.  Find a CI/CD YAML file you want to audit.
3.  Paste the content of your YAML file into the `PASTE YOUR CI/CD YAML CODE HERE` section.
4.  Submit the entire prompt to a powerful LLM (like Gemini, GPT-4, etc.).
5.  Review the AI-generated analysis for accuracy and implement the suggested fixes.

This structured, example-driven approach will yield significantly better results than a simple request.

---

## Project 2: Automate Trivy & tfsec Prompt Workflows

This project automates a common DevSecOps task: running a security scanner and then using an LLM to make the output understandable and actionable for developers. We'll create a GitHub Action that:
1.  Runs Trivy to scan for vulnerabilities.
2.  Takes the raw JSON output from Trivy.
3.  Feeds it to a Python script that calls an LLM.
4.  The LLM generates a human-readable summary and posts it as a comment on the pull request.

*(Note: A similar flow would work for `tfsec` by having it output JSON and adjusting the prompt accordingly.)*

### Step 1: The Directory Structure

For this project, you'll need the following file structure in your repository:

```
.
├── .github/
│   └── workflows/
│       └── security-scan-summary.yml  # Our main GitHub Actions workflow
├── scripts/
│   └── summarize_scan.py            # Python script to call the LLM
├── Dockerfile                         # A sample Dockerfile for Trivy to scan
└── requirements.txt                   # Python dependencies
```

### Step 2: The Components

Let's create each file. You would create these files in your local project directory.

#### `Dockerfile` (for scanning)
This is a simple file with a known vulnerability for demonstration purposes.

```dockerfile
# Use an older base image with known vulnerabilities for this demo
FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip install flask==1.1.2

CMD ["python", "app.py"]
```

#### `requirements.txt` (for the Python script)
This file lists the Python libraries our script needs.

```
openai
```

#### `scripts/summarize_scan.py`
This Python script will be the bridge between the scanner's output and the LLM. It reads the JSON, constructs a prompt, calls the OpenAI API (you can adapt this for other models), and prints the summary.

```python
import os
import sys
import json
import openai

# It's best practice to use an environment variable for the API key
# In GitHub Actions, this will be set as a secret.
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    sys.exit("Error: OPENAI_API_KEY environment variable not set.")

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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # Or gpt-4 for better results
            messages=[
                {"role": "system", "content": "You are a helpful DevSecOps assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
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
```

#### `.github/workflows/security-scan-summary.yml`
This is the heart of the automation. This workflow runs on every pull request.

```yaml
name: Security Scan and AI Summary

on:
  pull_request:
    branches: [ main ]

permissions:
  contents: read
  pull-requests: write # Required to post a comment

jobs:
  trivy-scan-and-summarize:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build Docker image for scanning
        run: docker build -t my-app-scan:latest .

      - name: Run Trivy vulnerability scanner
        id: trivy-scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'my-app-scan:latest'
          format: 'json'
          output: 'trivy-results.json'
          ignore-unfixed: true
          severity: 'CRITICAL,HIGH'
          # Continue on error so the next step can run
        continue-on-error: true

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'

      - name: Install Python dependencies
        run: pip install -r requirements.txt

      - name: Generate AI Summary
        id: ai-summary
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          SUMMARY=$(python scripts/summarize_scan.py < trivy-results.json)
          # Use heredoc to handle multiline summary for the output
          echo "summary<<EOF" >> $GITHUB_OUTPUT
          echo "$SUMMARY" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Post summary to PR comment
        uses: actions/github-script@v7
        if: steps.trivy-scan.outcome == 'failure' # Only comment if vulnerabilities are found
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const output = `## 🤖 AI Security Scan Summary

            ${{ steps.ai-summary.outputs.summary }}`;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            })
```

### Step 3: Setting Up the Repository

1.  **Add the Code:** Create the four files (`Dockerfile`, `requirements.txt`, `scripts/summarize_scan.py`, and `.github/workflows/security-scan-summary.yml`) in your local repository with the content provided above.

2.  **Set the OpenAI API Key:**
    *   In your GitHub repository, go to `Settings` > `Secrets and variables` > `Actions`.
    *   Click `New repository secret`.
    *   Name the secret `OPENAI_API_KEY`.
    *   Paste your OpenAI API key as the value.
    *   Click `Add secret`.

### Step 4: Seeing it in Action

1.  Commit all the files to a new branch in your repository and push it to GitHub.
    ```bash
    git checkout -b feature/ai-security-scanner
    git add .
    git commit -m "feat: Add AI-powered security scanner workflow"
    git push origin feature/ai-security-scanner
    ```

2.  Create a **Pull Request** from your new branch (`feature/ai-security-scanner`) to the `main` branch.

3.  Go to the "Actions" tab of your repository. You will see the "Security Scan and AI Summary" workflow running for your pull request.

4.  Once the workflow completes, check your Pull Request. Because Trivy found vulnerabilities in our sample `Dockerfile`, the `github-actions` bot will have posted a new comment containing the AI-generated summary.

#### Example Pull Request Comment

You should see a comment that looks something like this:

> ## 🤖 AI Security Scan Summary
>
> **Critical vulnerabilities found!**
>
> Here is a summary of the most critical issues discovered in the Docker image:
>
> *   **Package:** `jinja2` (installed from `flask==1.1.2`)
>     *   **Severity:** `CRITICAL`
>     *   **Risk:** This version is vulnerable to Server-Side Template Injection (SSTI), which can lead to remote code execution.
> *   **Package:** `werkzeug` (installed from `flask==1.1.2`)
>     *   **Severity:** `HIGH`
>     *   **Risk:** Contains a vulnerability related to improper handling of HTTP request data, which could be exploited.
> *   **Package:** `gnupg` (OS package)
>     *   **Severity:** `HIGH`
>     *   **Risk:** An older version of GnuPG with known vulnerabilities is present in the base image.
>
> Please review the full Trivy scan logs in the workflow run for more details and remediation steps.

---

## Conclusion

Congratulations on completing Day 5! You have successfully:

*   Crafted a sophisticated **few-shot prompt** to perform a security audit on CI/CD files, learning how to guide an LLM with expert examples.
*   Built a complete, **end-to-end automated workflow** that integrates a security scanner (Trivy) with an LLM to make security reports developer-friendly and actionable.

These are foundational skills for an AI-Native DevSecOps Engineer. You're not just running tools; you're building intelligent systems that augment and automate security processes. Keep up the great work!