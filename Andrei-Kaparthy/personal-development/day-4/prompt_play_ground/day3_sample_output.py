secure_s3_output = """
```terraform
# SECURE: This S3 bucket is configured with security best practices.
resource "aws_s3_bucket" "secure_user_data" {
  bucket = "my-secure-user-data-bucket-456" # Please change to a globally unique name
}

# Block all public access to the S3 bucket.
resource "aws_s3_bucket_public_access_block" "secure_user_data_pab" {
  bucket = aws_s3_bucket.secure_user_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable server-side encryption by default.
resource "aws_s3_bucket_server_side_encryption_configuration" "secure_user_data_sse" {
  bucket = aws_s3_bucket.secure_user_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Enable versioning to protect against accidental deletions or overwrites.
resource "aws_s3_bucket_versioning" "secure_user_data_versioning" {
  bucket = aws_s3_bucket.secure_user_data.id
  versioning_configuration {
    status = "Enabled"
  }
}
```

### Explanation of Security Enhancements:
- **`aws_s3_bucket_public_access_block`**: This is the most critical security control. It ensures that no public access can be granted via ACLs or bucket policies, preventing accidental data exposure.
- **`aws_s3_bucket_server_side_encryption_configuration`**: This enforces encryption at rest. All new objects uploaded to the bucket will be automatically encrypted using AWS-managed keys (AES256), protecting data if the physical storage is compromised.
- **`aws_s3_bucket_versioning`**: This adds a layer of data protection. It keeps a history of all object versions, which allows for recovery from accidental deletions or malicious overwrites.
"""