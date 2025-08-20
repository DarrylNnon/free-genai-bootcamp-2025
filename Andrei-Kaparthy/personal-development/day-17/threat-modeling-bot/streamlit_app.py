import streamlit as st
import openai
from dotenv import load_dotenv
import os
import base64
from pathlib import Path

# --- Helper Functions ---

def load_prompt(file_path: str) -> str | None:
    """Loads a prompt from a markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Prompt file not found: {file_path}")
        return None

@st.cache_resource
def get_openai_client():
    """
    Initializes and returns the OpenAI client.
    Handles API key retrieval from .env (local) or st.secrets (deployment).
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except (KeyError, AttributeError):
            pass # No secrets found, will raise error below

    if not api_key:
        raise ValueError(
            "OpenAI API key not found. "
            "Please set it in a .env file or in your Hugging Face Space secrets (OPENAI_API_KEY)."
        )

    return openai.OpenAI(api_key=api_key)

def diagram_to_text(client: openai.OpenAI, image_bytes: bytes) -> str:
    """Converts an architecture diagram image to a textual description using GPT-4o."""
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt_template = load_prompt("prompts/visual_to_text_prompt.md")
    if not prompt_template:
        return "Error: Could not load the visual-to-text prompt."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_template},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=2048,
    )
    return response.choices[0].message.content

def generate_threat_model(client: openai.OpenAI, architecture_description: str) -> str:
    """Generates a STRIDE threat model from an architecture description."""
    full_prompt_text = load_prompt("prompts/stride_prompt.md")
    if not full_prompt_text:
        return "Error: Could not load the STRIDE prompt."

    # Extract persona for system message and the rest for the user message
    try:
        persona_start = full_prompt_text.index("<PERSONA>") + len("<PERSONA>")
        persona_end = full_prompt_text.index("</PERSONA>")
        system_message_content = full_prompt_text[persona_start:persona_end].strip()
        user_prompt_template = full_prompt_text[persona_end + len("</PERSONA>"):].strip()
    except ValueError:
        st.error("Could not parse the STRIDE prompt. Make sure it contains <PERSONA> tags.")
        return "Error: Invalid STRIDE prompt format."

    final_user_prompt = user_prompt_template.format(user_architecture=architecture_description)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message_content},
            {"role": "user", "content": final_user_prompt}
        ],
        temperature=0.2,
        max_tokens=4000,
    )
    return response.choices[0].message.content

# --- Streamlit App ---

st.set_page_config(page_title="Threat Modeling Bot", layout="wide", page_icon="🤖")

st.title("🤖 GPT Threat Modeling Bot")
st.markdown("""
Welcome! This tool helps you automatically generate a **STRIDE threat model** for your system architecture.
You can either **upload an architecture diagram** or **provide a written description in Markdown**.
""")

# --- Initialization ---
try:
    client = get_openai_client()
except ValueError as e:
    st.error(str(e))
    st.stop()

if 'architecture_text' not in st.session_state:
    st.session_state.architecture_text = ""
if 'threat_model' not in st.session_state:
    st.session_state.threat_model = ""

# --- Sidebar for Inputs ---
st.sidebar.header("1. Provide Architecture")
input_method = st.sidebar.radio("Choose input method:", ("Upload Diagram", "Write Description"), label_visibility="collapsed")

if input_method == "Upload Diagram":
    uploaded_file = st.sidebar.file_uploader("Upload a diagram (PNG, JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        if st.sidebar.button("Analyze Diagram", use_container_width=True):
            with st.spinner("Analyzing diagram... This may take a moment."):
                try:
                    image_bytes = uploaded_file.getvalue()
                    description = diagram_to_text(client, image_bytes)
                    st.session_state.architecture_text = description
                    st.session_state.threat_model = "" # Clear old model
                except Exception as e:
                    st.error(f"Failed to analyze diagram: {e}")

elif input_method == "Write Description":
    placeholder_text = """
**High-Level Summary:**
A simple web application that allows users to upload files to an S3 bucket.

**Components:**
- **User:** External user accessing the application via a browser.
- **AWS WAF:** Protects against common web exploits.
- **API Gateway:** Exposes a REST API endpoint for file uploads.
- **AWS Lambda:** Receives the file, validates it, and uploads to S3.
- **S3 Bucket:** Stores the uploaded files.

**Data Flows:**
1. User sends an HTTPS POST request with the file to API Gateway.
2. WAF inspects the request.
3. API Gateway triggers the Lambda function.
4. The Lambda function puts the file into the S3 bucket.
"""
    st.session_state.architecture_text = st.sidebar.text_area(
        "Describe your architecture in Markdown:",
        value=st.session_state.architecture_text or placeholder_text,
        height=300
    )

# --- Analysis Trigger ---
st.sidebar.header("2. Generate Threat Model")
if st.sidebar.button("Analyze Threats", disabled=not st.session_state.architecture_text, type="primary", use_container_width=True):
    with st.spinner("Generating STRIDE threat model... This can take up to a minute."):
        try:
            threat_model = generate_threat_model(client, st.session_state.architecture_text)
            st.session_state.threat_model = threat_model
        except Exception as e:
            st.error(f"Failed to generate threat model: {e}")

# --- Main Content Area for Display ---
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("Architecture Description")
    if st.session_state.architecture_text:
        st.markdown(st.session_state.architecture_text, unsafe_allow_html=True)
    else:
        st.info("Your architecture description will appear here after you provide it.")

with col2:
    st.subheader("Threat Model Report (STRIDE)")
    if st.session_state.threat_model:
        st.markdown(st.session_state.threat_model, unsafe_allow_html=True)
    else:
        st.info("Your generated threat model will appear here.")