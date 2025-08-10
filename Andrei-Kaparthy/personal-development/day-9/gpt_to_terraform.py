import os
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load your OpenAI API key from an environment variable

def extract_terraform_code(response_text):
    """Extracts Terraform code from a Markdown code block."""
    # The model might wrap the code in a markdown block
    match = re.search(r"```(?:terraform)?\n(.*?)\n```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # If no markdown block is found, assume the whole response is code
    return response_text.strip()

def generate_terraform_code(prompt):
    """Generates Terraform code using GPT based on the given prompt."""
    try:
        # Using the recommended Chat Completions endpoint, which is more capable.
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # A modern and cost-effective model
            messages=[
                {"role": "system", "content": "You are a Terraform expert. You will be given a prompt and you must generate the corresponding HCL code. Only output the code, with no additional explanation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,  # Adjust as needed
            n=1,
            stop=None,
            temperature=0.2 # Lower temperature for more predictable code
        )
        # The response from chat models is in a different attribute
        raw_code = response.choices[0].message.content
        return extract_terraform_code(raw_code)
    except Exception as e:
        print(f"Error generating Terraform code: {e}")
        return None

def save_terraform_code(code, filename="main.tf"):
    """Saves the generated Terraform code to a file."""
    try:
        with open(filename, "w") as f:
            f.write(code)
        print(f"Terraform code saved to {filename}")
    except Exception as e:
        print(f"Error saving Terraform code: {e}")

if __name__ == "__main__":
    # Example usage:
    prompt = """
    Generate Terraform code to create an AWS S3 bucket named 'my-unique-bucket' 
    with versioning enabled and public access blocked.  
    Include a resource tag with the key 'Environment' and value 'Development'.
    """
    terraform_code = generate_terraform_code(prompt)

    if terraform_code:
        save_terraform_code(terraform_code)
    else:
        print("Failed to generate Terraform code.")
