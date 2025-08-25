import os
import sys
import argparse
import pandas as pd
import openai
from openai import OpenAI
from dotenv import load_dotenv

# --- Client Initialization ---
# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    sys.exit("Error: OPENAI_API_KEY not found. Please create a .env file and add your key.")
client = OpenAI(api_key=api_key)


def read_prompt_template(filepath="prompts/finops_insights.md"):
    """Reads the prompt template from a file."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        sys.exit(f"Error: Prompt template file not found at {filepath}")

def read_csv_data(filepath):
    """Reads and processes the AWS cost data from a CSV file."""
    try:
        df = pd.read_csv(filepath)
        # For this example, we'll convert the dataframe to a string.
        # In a real-world scenario with large files, you might summarize it first.
        return df.to_string()
    except FileNotFoundError:
        sys.exit(f"Error: CSV file not found at {filepath}")
    except Exception as e:
        sys.exit(f"Error reading or processing CSV file: {e}")

def generate_insights(prompt_template, csv_data):
    """Generates FinOps insights using the LLM."""
    
    final_prompt = prompt_template.format(csv_data=csv_data)

    try:
        print("🤖 Calling OpenAI API to generate FinOps insights... (This may take a moment)")
        response = client.chat.completions.create(
            model="gpt-4o", # Using a powerful and cost-effective model for analysis
            messages=[
                {"role": "system", "content": "You are an expert FinOps analyst providing insights on cloud cost data."},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.2, # Low temperature for factual, deterministic analysis
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        sys.exit(f"Error calling OpenAI API: {e}")

def main():
    """Main function to orchestrate the FinOps advisor."""
    parser = argparse.ArgumentParser(description="GPT FinOps Advisor - Analyze AWS Cost Reports.")
    parser.add_argument("csv_filepath", help="Path to the AWS Cost Explorer CSV file.")
    parser.add_argument("--output", help="Path to save the output Markdown report.", default=None)
    args = parser.parse_args()

    print(f"📄 Reading prompt template...")
    prompt_template = read_prompt_template()

    print(f"📊 Reading cost data from '{args.csv_filepath}'...")
    csv_data = read_csv_data(args.csv_filepath)

    insights = generate_insights(prompt_template, csv_data)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(insights)
        print(f"\n✅ Successfully generated report and saved to '{args.output}'")
    else:
        print("\n--- 📈 FinOps Insights Report ---")
        print(insights)

if __name__ == "__main__":
    main()