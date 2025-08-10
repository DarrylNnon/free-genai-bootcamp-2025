#!/bin/bash

echo "Starting Terraform validation..."

# Run Checkov
echo "Running Checkov..."
checkov -f main.tf || echo "Checkov failed, but continuing..."

# Run CloudFormation Guard
echo "Running CloudFormation Guard..."
cfn-guard validate --data main.tf --rules cloudformation_guard_rules.rules --output-format text || echo "CloudFormation Guard failed, but continuing..."

echo "Terraform validation complete."
