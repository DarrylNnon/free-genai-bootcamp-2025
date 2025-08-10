import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load your OpenAI API key from an environment variable

def generate_terraform_code(prompt):
    """Generates Terraform code using GPT based on the given prompt."""
    try:
        response = client.completions.create(engine="text-davinci-003",  # Or your preferred engine
        prompt=prompt,
        max_tokens=500,  # Adjust as needed
        n=1,
        stop=None,
        temperature=0.7)
        return response.choices[0].text.strip()
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
