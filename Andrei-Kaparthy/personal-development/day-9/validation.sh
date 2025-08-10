#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status.

echo "Starting Terraform validation..."

# Run Checkov
echo "Running Checkov..."
checkov -f main.tf

# Run CloudFormation Guard
echo "Running CloudFormation Guard..."
cfn-guard validate --data main.tf --rules cloudformation_guard_rules.rules --output-format text

echo "Terraform validation complete."
