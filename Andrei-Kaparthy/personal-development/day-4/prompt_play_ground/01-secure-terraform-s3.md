# Role: Secure Cloud Infrastructure Architect

## Task:
Generate a secure Terraform configuration for an AWS S3 bucket.

## Context:
The S3 bucket will be used to store sensitive user-uploaded documents.

## Requirements:
- The bucket name should be a variable, e.g., `var.bucket_name`.
- Enable server-side encryption using AWS KMS (SSE-KMS).
- Block all public access.
- Enable versioning to prevent accidental data loss.
- Enforce encryption of data in transit (require SSL).
- Add a bucket policy that only allows access from a specific IAM role (provide a placeholder for the role ARN).
- Add tags for `Environment` and `Project`.