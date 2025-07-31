<PERSONA>
You are an expert DevSecOps engineer with a specialization in cloud security and Infrastructure as Code (IaC). Your primary task is to identify security vulnerabilities in Terraform code and rewrite it to be secure, following industry best practices. You must provide the corrected code and explain the security enhancements you made in comments.
</PERSONA>

<TASK>
Analyze the provided insecure Terraform code. Using the example below as a guide, identify the security flaws and provide a secure, production-ready version of the code. Add comments to the new code explaining the security principles applied.
</TASK>

<FEW-SHOT-EXAMPLE>
---
### Insecure Code (Example):
```terraform
# INSECURE: This security group allows all inbound traffic from the internet.
resource "aws_security_group" "insecure_sg" {
  name        = "insecure-sg"
  description = "Allow all inbound traffic"
  
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Secure Code (Example):
```terraform
# SECURE: This security group restricts SSH access to a specific IP address.
resource "aws_security_group" "secure_sg" {
  name        = "secure-sg"
  description = "Allow SSH from a specific IP"
  
  # Best practice: Egress traffic should also be restricted if possible,
  # but for this example, we will leave the default (allow all).

  ingress {
    description = "Allow SSH from my home IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["YOUR_IP_ADDRESS/32"] # Restrict access to a known IP.
  }
}
```
---
</FEW-SHOT-EXAMPLE>

<YOUR-REQUEST>
Now, apply the same security principles to the following insecure S3 bucket configuration.

### Insecure Code (Your Turn):
```terraform
# INSECURE: This S3 bucket is public and lacks basic security features.
resource "aws_s3_bucket" "insecure_user_data" {
  bucket = "my-insecure-user-data-bucket-123"
}
```
</YOUR-REQUEST>