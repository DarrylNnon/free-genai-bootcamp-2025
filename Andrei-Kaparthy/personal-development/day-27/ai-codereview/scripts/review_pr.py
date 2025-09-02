import os
import sys
import openai

def get_pr_diff():
    """Reads the pull request diff from a file passed as an argument."""
    diff_file_path = sys.argv[1]
    with open(diff_file_path, 'r') as file:
        return file.read()

def get_review_prompt(diff_content):
    """Reads the prompt template and injects the diff."""
    # Assuming the prompt file is in a 'prompts' subdirectory relative to the script
    script_dir = os.path.dirname(__file__)
    prompt_file_path = os.path.join(script_dir, 'prompts', 'code_review.md')
    
    with open(prompt_file_path, 'r') as file:
        prompt_template = file.read()
    
    return prompt_template.format(diff_content=diff_content)

def get_ai_review(prompt):
    """Calls the OpenAI API to get a code review."""
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-4o",  # Or "gpt-4-turbo"
            messages=[
                {"role": "system", "content": "You are an expert code reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, # Lower temperature for more deterministic, factual reviews
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating AI review: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python review_pr.py <path_to_diff_file>")
        sys.exit(1)

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        sys.exit(1)

    diff = get_pr_diff()
    if not diff.strip():
        print("No changes detected in the diff. Skipping review.")
    else:
        full_prompt = get_review_prompt(diff)
        review = get_ai_review(full_prompt)
        print(review)