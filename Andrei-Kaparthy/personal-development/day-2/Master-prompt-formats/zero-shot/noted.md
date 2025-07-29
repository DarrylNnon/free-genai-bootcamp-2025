# master prompt format

# zero-shot

Zero-shot means no few-shot (no demonstrations).

### ✅ Zero-Shot Prompt Format (Best Practice by Top DevSecOps/Cloud Experts)

Here’s the **optimized zero-shot prompt format** that elite engineers and researchers use:


### 🔹 Prompt Format (Zero-Shot)

```plaintext
[Instruction phrase] + [task or question] + [context (optional)] + [constraints or output format]
```


### ✅ Example Templates

1. Information Retrieval

   ```plaintext
   Explain the difference between Kubernetes and Nomad in terms of scalability, fault tolerance, and ease of deployment. Return your answer in bullet points.
   ```

2. Code Generation

   ```plaintext
   Write a secure Python script that scans a directory for all `.yaml` files and validates them against a predefined JSON schema.
   ```

3. **Security Analysis**

   ```plaintext
   Analyze the following Terraform code for security misconfigurations and suggest fixes: [insert code block].
   ```

4. Policy Enforcement (DevSecOps)

   ```plaintext
   Generate an OPA policy that denies deployment of containers with the `latest` tag in a Kubernetes cluster.
   ```

5. **Cloud Architecture**

   ```plaintext
   Describe a high-availability multi-region AWS architecture that supports automatic failover and RTO < 5 minutes. Use a table for components and their purpose.
   ```



### 🔒 Best Practices (Used by Top Engineers)

| Principle             | Description                                               |
| --------------------- | --------------------------------------------------------- |
| **Clarity > Brevity** | No ambiguity. Be explicit.                                |
| **No examples**       | Zero-shot means **no few-shot** (no demonstrations).      |
| **Add constraints**   | Specify format (e.g., JSON, YAML, table, bullet list).    |
| **Be role-aware**     | Prefix with role: *"As a security analyst..."* if needed. |
| **Avoid pronouns**    | Replace *“it”*, *“they”* with specifics.                  |



### ⚠️ Bad vs Good Prompt Example

**🚫 Bad Prompt (Ambiguous)**:

```
How does this tool work?
```

✅ Good Prompt (Zero-Shot):

```plaintext
Explain how HashiCorp Vault works in dynamic secrets management for PostgreSQL. Include the roles, authentication method, and the lifecycle of a credential.
```
