# AI-Native DevSecOps: Day 3 Lessons

Today was a breakthrough moment. The abstract concepts of prompt engineering met the concrete demands of cloud security. The mission was to move beyond generating generic code and start producing secure, production-ready Infrastructure as Code (IaC). This is where the "AI-Native" part of the job title starts to feel real.

---

### Lesson 1: Teaching AI to Think Securely (The "Security as a Pattern" Shot)

The core lesson of the day was that you can't just ask an AI to be secure. You have to *teach* it what "secure" means in a given context. The few-shot prompting technique is the perfect tool for this.

*   **The Method:** Instead of just telling the model to fix insecure code, I provided it with a clear before-and-after example. I showed it an `aws_security_group` resource that was wide open to the internet (`0.0.0.0/0`) and then provided the corrected, secure version that restricted access to a specific IP.
*   **The "Why":** This approach teaches the model the *pattern* of identifying and remediating a specific class of vulnerability. It learns to look for overly permissive rules and replace them with ones that adhere to the principle of least privilege.

---

### Lesson 2: Generating a Secure S3 Bucket (The "Applied IaC Security" Shot)

With the AI primed on the concept of security, I gave it a new task: fix an insecure S3 bucket.

*   **The Insecure Code:** I started with a barebones Terraform resource: `resource "aws_s3_bucket" "insecure_user_data" {}`. This is a common but dangerous starting point, as it defaults to being private but lacks crucial security hardening.
*   **The AI-Generated Secure Code:** The model didn't just add a few lines; it generated a comprehensive, secure configuration using multiple resources. It understood that a secure S3 bucket isn't just one thing, but a combination of controls:
    1.  **`aws_s3_bucket_public_access_block`:** It added a resource to explicitly block all forms of public access.
    2.  **`aws_s3_bucket_server_side_encryption_configuration`:** It enforced server-side encryption by default (SSE-S3/AES256).
    3.  **`aws_s3_bucket_versioning`:** It enabled versioning to protect against accidental data deletion or modification.

The AI also added comments explaining *why* each control was important, just as I had shown it in the example.

---

## Day 3 Conclusion

This was a massive leap forward. I'm no longer just a consumer of AI-generated code; I'm a teacher, guiding the model to produce outputs that meet professional security standards. The ability to transform a one-line insecure resource into a multi-resource, secure configuration with a single, well-crafted prompt is a DevSecOps superpower. The Prompt Engineering Notebook now contains its first truly powerful, reusable security pattern.