import argparse
import os
import sys
from pathlib import Path

import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# The OpenAI client automatically looks for the OPENAI_API_KEY environment variable.
client = OpenAI()


def check_api_key():
    """Check if the OpenAI API key is available in environment variables."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found.")
        print("Please set it in a .env file or as an environment variable.")
        sys.exit(1)

def read_file_content(file_path: Path) -> str:
    """Read the content of a file."""
    if not file_path.is_file():
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
    return file_path.read_text()


def generate_threat_model(architecture_doc: str, prompt_template: str, model_name: str) -> str:
    """
    Generates a threat model report by calling the OpenAI API.

    Args:
        architecture_doc: The string content of the system architecture.
        prompt_template: The few-shot prompt template.
        model_name: The OpenAI model to use for generation.

    Returns:
        The generated threat model report as a string.
    """
    print("🤖 Calling OpenAI API to generate threat model...")
    try:
        final_prompt = prompt_template.format(user_architecture=architecture_doc)

        response = client.chat.completions.create(model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": final_prompt},
        ],
        temperature=0.2)
        print("✅ Report generated successfully.")
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1)

def save_report(report: str, output_path: Path):
    """Saves the report to a file."""
    print(f"💾 Saving report to: {output_path}")
    try:
        output_path.write_text(report)
        print("✅ Report saved successfully.")
    except IOError as e:
        print(f"Error: Could not write to file {output_path}. {e}")
        sys.exit(1)

def main():
    """Main function to run the threat modeling bot."""
    parser = argparse.ArgumentParser(
        description="Generate a threat model from a system architecture markdown file using STRIDE or DREAD frameworks."
    )
    parser.add_argument(
        "architecture_file",
        type=Path,
        help="Path to the markdown file describing the system architecture.",
    )
    parser.add_argument(
        "--framework",
        type=str.upper,
        choices=["STRIDE", "DREAD"],
        default="STRIDE",
        help="The threat modeling framework to use (default: STRIDE).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path to save the output markdown report. If not provided, prints to console.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="The OpenAI model to use (e.g., gpt-4o, gpt-4-turbo, gpt-3.5-turbo).",
    )
    args = parser.parse_args()

    check_api_key()

    # Determine the correct prompt file based on the chosen framework
    prompt_filename = f"{args.framework.lower()}_threat_model_generator.md"
    prompt_path = Path(__file__).parent / "prompts" / prompt_filename

    print(f"📄 Reading architecture from: {args.architecture_file}")
    architecture_content = read_file_content(args.architecture_file)

    print(f"🧠 Using {args.framework} framework. Reading prompt from: {prompt_path}")
    prompt_template_content = read_file_content(prompt_path)

    report = generate_threat_model(architecture_content, prompt_template_content, args.model)

    if args.output:
        save_report(report, args.output)
    else:
        print("\n" + "=" * 20 + " THREAT MODEL REPORT " + "=" * 20 + "\n")
        print(report)


if __name__ == "__main__":
    main()