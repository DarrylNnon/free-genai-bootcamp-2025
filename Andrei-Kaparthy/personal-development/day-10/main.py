import os
import openai
import subprocess
import tempfile

def orchestrate_iac_generation(user_request):
    """Generate IaC code and security report based on user request"""
    try:
        # Generate Terraform code
        terraform_code = generate_terraform_code(user_request)
        
        # Run security scan
        security_report = run_security_scan(terraform_code)
        
        # Combine results
        final_report = f"""# Generated Terraform Code

{terraform_code}

# Security Analysis Report

{security_report}
"""
        return final_report
    
    except Exception as e:
        return f"Error generating IaC: {str(e)}"

def generate_terraform_code(user_request):
    """Generate Terraform code using OpenAI"""
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    prompt = f"""Generate secure Terraform code for: {user_request}

Requirements:
- Use best security practices
- Include proper resource naming
- Add necessary tags
- Include comments

Terraform code:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.3
    )
    
    return response.choices[0].message.content.strip()

def run_security_scan(terraform_code):
    """Run tfsec security scan on generated code"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tf', delete=False) as f:
            f.write(terraform_code)
            tf_file = f.name
        
        # Run tfsec scan
        result = subprocess.run(
            ['/opt/bin/tfsec', tf_file, '--format', 'text'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        os.unlink(tf_file)
        
        if result.returncode == 0:
            return "✅ No security issues found"
        else:
            return f"⚠️ Security issues detected:\n{result.stdout}"
            
    except FileNotFoundError:
        return "⚠️ tfsec not available - security scan skipped"
    except Exception as e:
        return f"⚠️ Security scan failed: {str(e)}"