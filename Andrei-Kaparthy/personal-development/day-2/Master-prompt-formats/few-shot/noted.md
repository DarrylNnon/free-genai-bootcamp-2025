# Master prompt format

# few-shot


Few-shot prompting is when you **provide a few examples** of input/output to **teach the model how to behave** before giving it a new instruction.

This is used when:

* You want **more control** over the response style.
* You're asking for something **non-trivial or nuanced**.
* You want the model to **infer a pattern** or schema.


### 🔹 **Few-Shot Prompt Format (Optimal)**

```plaintext
[Instruction]
Example 1:
Input: [Example Input]
Output: [Expected Output]

Example 2:
Input: [Example Input]
Output: [Expected Output]


Now, do the same for the following input:
Input: [Your actual input]
Output:
```


### ✅ DevSecOps Examples

#### 🔐 Example 1: IaC Vulnerability Detection

```plaintext
You're a security engine analyzing Terraform code for security misconfigurations.

Example 1:
Input:
resource "aws_security_group" "bad_sg" {
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
Output:
❌ Insecure: Open ingress to all ports from any IP. This exposes the instance to external attacks.
✅ Fix: Restrict ports and CIDR range.

Example 2:
Input:
resource "aws_s3_bucket" "public" {
  acl = "public-read"
}
Output:
❌ Insecure: Public read access on S3 bucket.
✅ Fix: Remove `acl = "public-read"` or use bucket policy to restrict access.

Now, do the same for this input:
Input:
resource "aws_db_instance" "rds" {
  publicly_accessible = true
}
Output:
```


#### 🧠 Example 2: Threat Modeling

```plaintext
Generate threat models using STRIDE based on input components.

Example 1:
Input: API Gateway -> Lambda -> DynamoDB
Output:
- Spoofing: Unauthorized access to API endpoint.
- Tampering: Injection in API payload.
- Repudiation: Lack of logging in Lambda.
- Information Disclosure: Data leak via misconfigured DynamoDB permissions.
- Denial of Service: Abuse of API Gateway limits.
- Elevation of Privilege: Lambda role misconfiguration.

Example 2:
Input: User -> Frontend -> Firebase
Output:
- Spoofing: Fake JWT tokens.
- Information Disclosure: Firestore rules misconfigured.


Now, do the same for:
Input: Mobile App -> API Gateway -> ECS -> RDS
Output:
```


### 🔧 Tips for Crafting Few-Shot Prompts (Used by Elite Engineers)

| Tip                                     | Purpose                                     |
| --------------------------------------- | ------------------------------------------- |
| Use **diverse but consistent examples** | Teaches model generalizable behavior        |
| Keep formatting **identical**           | Consistency improves pattern recognition    |
| Start with **simpler examples**         | Build from easy to complex                  |
| Limit to **2–5 examples**               | After 5, model might forget earlier context |
| Always end with **“Now do the same…”**  | Smooth transition to final task             |


Want tailored few-shot prompt templates for:

* ✅ OPA policy generation
* ✅ CI/CD pipeline hardening
* ✅ Cloud misconfiguration detection
* ✅ K8s YAML mutation/admission controls
