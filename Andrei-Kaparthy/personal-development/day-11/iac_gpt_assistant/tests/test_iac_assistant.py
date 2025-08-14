import json
import subprocess
from unittest.mock import patch

import pytest
from iac_assistant import (
    extract_code_block,
    process_iac_request,
    run_security_scan,
)

# --- Test Data ---
MOCK_TERRAFORM_CODE = 'resource "local_file" "test" {\n  content  = "hello"\n  filename = "${path.module}/hello.txt"\n}'
MOCK_RESPONSE_WITH_CODE = f"Here is the code:\n```terraform\n{MOCK_TERRAFORM_CODE}\n```"
MOCK_TFSEC_CLEAN_RESULT = {"results": []}
MOCK_TFSEC_ISSUES_RESULT = {
    "results": [
        {
            "rule_id": "AVD-GEN-0001",
            "long_id": "generic-secrets-no-plaintext-secrets",
            "rule_description": "Potentially sensitive data stored in plaintext in provider.",
            "severity": "CRITICAL",
        }
    ]
}


def test_extract_code_block_with_terraform():
    """Should extract code from a terraform markdown block."""
    extracted = extract_code_block(MOCK_RESPONSE_WITH_CODE)
    assert extracted == MOCK_TERRAFORM_CODE


def test_extract_code_block_no_block():
    """Should return the original text if no code block is found."""
    text = "just some plain text"
    extracted = extract_code_block(text)
    assert extracted == text


@patch("iac_assistant.subprocess.run")
def test_run_security_scan_clean(mock_subprocess_run):
    """Should handle a clean tfsec scan."""
    # Mock a successful run with no issues
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args=["tfsec", ".", "--format", "json"],
        returncode=0,
        stdout=json.dumps(MOCK_TFSEC_CLEAN_RESULT),
        stderr="",
    )
    result = run_security_scan(MOCK_TERRAFORM_CODE)
    assert result == MOCK_TFSEC_CLEAN_RESULT


@patch("iac_assistant.subprocess.run")
def test_run_security_scan_with_issues(mock_subprocess_run):
    """Should handle a tfsec scan that finds issues."""
    # Mock a run that finds issues (non-zero exit code is normal for tfsec)
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args=["tfsec", ".", "--format", "json"],
        returncode=1,
        stdout=json.dumps(MOCK_TFSEC_ISSUES_RESULT),
        stderr="",
    )
    result = run_security_scan(MOCK_TERRAFORM_CODE)
    assert result == MOCK_TFSEC_ISSUES_RESULT


@patch("iac_assistant.subprocess.run")
def test_run_security_scan_tfsec_panic(mock_subprocess_run):
    """Should handle a tfsec panic."""
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args=["tfsec", ".", "--format", "json"],
        returncode=1,
        stdout="",
        stderr="panic: something went wrong",
    )
    result = run_security_scan(MOCK_TERRAFORM_CODE)
    assert result["results"][0]["severity"] == "CRITICAL"
    assert "tfsec failed to run" in result["results"][0]["rule_description"]


@patch("iac_assistant.subprocess.run", side_effect=FileNotFoundError)
def test_run_security_scan_not_found(mock_subprocess_run):
    """Should return None if tfsec command is not found."""
    result = run_security_scan(MOCK_TERRAFORM_CODE)
    assert result is None


# --- Testing the main orchestrator function ---


@patch("iac_assistant.generate_report")
@patch("iac_assistant.fix_terraform")
@patch("iac_assistant.run_security_scan")
@patch("iac_assistant.generate_terraform")
def test_process_iac_request_happy_path(
    mock_generate_terraform,
    mock_run_security_scan,
    mock_fix_terraform,
    mock_generate_report,
):
    """Test the ideal workflow where initial code is secure."""
    user_request = "create a secure thing"
    mock_generate_terraform.return_value = MOCK_TERRAFORM_CODE
    mock_run_security_scan.return_value = MOCK_TFSEC_CLEAN_RESULT
    mock_generate_report.return_value = "## Final Report\nAll good!"

    result = process_iac_request(user_request)

    mock_generate_terraform.assert_called_once_with(user_request)
    mock_run_security_scan.assert_called_once_with(MOCK_TERRAFORM_CODE)
    # fix_terraform should NOT be called if the scan is clean
    mock_fix_terraform.assert_not_called()
    mock_generate_report.assert_called_once_with(
        user_request, MOCK_TERRAFORM_CODE, json.dumps(MOCK_TFSEC_CLEAN_RESULT)
    )

    assert "error" not in result
    assert result["terraform_code"] == MOCK_TERRAFORM_CODE
    assert result["report"] == "## Final Report\nAll good!"

