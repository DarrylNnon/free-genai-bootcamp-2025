import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_finops_analysis(csv_data: str) -> str:
    """
    Analyzes the given CSV data using a few-shot prompt with GPT.
    """
    try:
        # Load the master prompt
        with open("prompts/finops_insights.md", "r") as f:
            prompt_template = f.read()

        # Inject the live data into the prompt
        final_prompt = prompt_template.format(csv_data=csv_data)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert FinOps analyst."},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except FileNotFoundError:
        return "Error: The prompt file 'prompts/finops_insights.md' was not found."
    except Exception as e:
        return f"An error occurred while communicating with the OpenAI API: {e}"