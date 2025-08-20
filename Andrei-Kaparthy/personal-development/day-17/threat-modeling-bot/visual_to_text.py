import base64
import os
from openai import OpenAI

# --- Configuration ---
# Make sure to set your OPENAI_API_KEY environment variable.
# You can get a key from https://platform.openai.com/
#
# For local testing, you can use:
# from dotenv import load_dotenv
# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#
# Or directly:
# client = OpenAI(api_key="YOUR_API_KEY")

client = OpenAI()

# --- Function to encode the image to base64 ---
def encode_image(image_path):
  """Encodes an image file to a base64 string."""
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# --- Main function to convert diagram to text ---
def diagram_to_text(image_path: str) -> str:
    """
    Uses a multimodal LLM to generate a textual description of an architecture diagram.
    This text can then be used as input for threat modeling.

    Args:
        image_path: The path to the visual diagram image file.

    Returns:
        A textual description of the diagram.
    """
    if not os.path.exists(image_path):
        return f"Error: Image file not found at {image_path}"

    # Encode the image
    base64_image = encode_image(image_path)

    # Create the prompt for the model
    prompt_messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """
                    Analyze the following architecture diagram. Your goal is to convert it into a detailed textual description that can be used for threat modeling.

                    Describe the key components, services, data flows, and trust boundaries.
                    Identify all components (e.g., user, web server, API gateway, database, lambda function, S3 bucket, external APIs).
                    Describe the connections and interactions between them.
                    Mention any security components like WAF, IAM roles, or VPCs.
                    Format the output as a clear, structured markdown text.
                    """
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]

    try:
        # Call the OpenAI API (using a vision-capable model like gpt-4o)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt_messages,
            max_tokens=1024,
            temperature=0.1, # Lower temperature for more factual, deterministic output
        )

        # Extract the text description
        description = response.choices[0].message.content
        return description.strip()

    except Exception as e:
        return f"An error occurred while calling the API: {e}"

# --- Example Usage ---
if __name__ == "__main__":
    # In a real application, you would get the image path from a file upload or another source.
    # For this example, we'll assume a file named 'architecture_diagram_example.png' exists.
    # You will need to provide your own architecture diagram image.
    example_image_path = "architecture_diagram_example.png"

    # Create a dummy image file if it doesn't exist for demonstration purposes
    if not os.path.exists(example_image_path):
        print(f"Warning: Example image '{example_image_path}' not found.")
        print("Please provide an architecture diagram image to test this script.")
        print("\n--- Expected Workflow ---")
        print(f"1. Place your architecture diagram (e.g., as '{example_image_path}') in this directory.")
        print("2. Set your OPENAI_API_KEY environment variable.")
        print("3. Run the script: python visual_to_text.py")
        exit()


    print(f"Analyzing diagram: {example_image_path}...")
    text_description = diagram_to_text(example_image_path)

    print("\n--- Generated Textual Description ---")
    print(text_description)

    print("\n--- Next Step ---")
    print("This description can now be passed to another LLM call for STRIDE threat analysis.")