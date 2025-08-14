# AI-Native DevSecOps: Day 8 Lessons

Our application is now automatically deployed, but is it secure? Day 8 introduced the "Sec" into DevSecOps. With a working CI/CD pipeline, the focus shifted to layering in security controls at every level of the architecture, from the front door to the data itself.

---

### Lesson 1: Securing the Gateway (The "Auth" Shot)

An open API endpoint is an open invitation for abuse. The first line of defense is securing the API Gateway.

*   **New Components:** API Keys, AWS IAM Roles, or Amazon Cognito User Pools.
*   **How it Works:** I modified the Terraform code to require an API key for all requests. For more advanced security, one could configure IAM-based authorization (for system-to-system calls) or a Cognito User Pool to authenticate end-users directly against the API.
*   **Use Case:** Preventing unauthorized access and protecting against denial-of-service attacks. API keys are great for tracking usage from different clients.

---

### Lesson 2: Securing the Data (The "Encryption" Shot)

If our RAG application handles sensitive documents or conversations, that data must be protected. This means encryption, both in transit and at rest.

*   **New Components:** AWS Key Management Service (KMS), enabling encryption features in DynamoDB and S3.
*   **How it Works:** TLS encrypts data in transit to the API Gateway by default. For data at rest, I enabled server-side encryption on the DynamoDB table (for chat history) and the S3 bucket (where vector data might be stored). This is a simple toggle in Terraform but a critical security control.
*   **Use Case:** Protecting sensitive customer data and chat logs from unauthorized access, even if an attacker gains underlying access to the storage systems. This is a compliance cornerstone.

---

### Lesson 3: Securing the Code (The "SAST" Shot)

Vulnerabilities often hide in our own code or its dependencies. Static Application Security Testing (SAST) helps find them before they reach production.

*   **New Component:** A SAST tool like Snyk, GitHub Advanced Security, or SonarQube integrated into the CI/CD pipeline.
*   **How it Works:** I added a new step to our GitHub Actions workflow. Before deploying, the SAST tool scans the Lambda function's Python code and its `requirements.txt` file. It checks for common security flaws (like injection vulnerabilities) and known vulnerabilities in third-party packages. If a critical issue is found, the pipeline fails, preventing the insecure code from being deployed.
*   **Use Case:** Automatically catching security bugs early in the development cycle, reducing risk and the cost of remediation.

---

## Day 8 Conclusion

Today was about building walls and installing locks. By adding authentication to our API, encrypting our data stores, and integrating automated security scanning into our pipeline, we've shifted security "left." It's no longer an afterthought but an integral, automated part of our development process. Our AI-native application is not just functional and deployable; it's now being built on a secure and resilient foundation.