import streamlit as st
from pathlib import Path

# --- Page Config ---
st.set_page_config(
    page_title="Prompt Playground",
    page_icon="🛠️",
    layout="wide"
)

# --- Helper Functions ---
@st.cache_data
def load_prompt_template(filepath):
    """Loads a prompt template from a given filepath."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Prompt file not found: {filepath}")
        return ""

# --- Main App ---
st.title("🛠️ Prompt Playground")
st.markdown("A space to experiment with different prompt engineering techniques for DevSecOps.")

# --- Sidebar for Configuration ---
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", help="Get your key from https://platform.openai.com/account/api-keys")

    st.header("Prompt Selection")
    # Dynamically find all .md files in the 'prompts' directory
    prompt_dir = Path("prompts")
    prompt_files = [f.name for f in prompt_dir.glob("*.md")] if prompt_dir.exists() else []

    if not prompt_files:
        st.warning("No prompt files found in the 'prompts' directory. Please add some .md files.")
        selected_prompt_file = None
    else:
        selected_prompt_file = st.selectbox(
            "Choose a prompt template:",
            prompt_files
        )

# --- Main Content Area ---
if selected_prompt_file:
    # Load the selected prompt template
    prompt_template_path = prompt_dir / selected_prompt_file
    prompt_template = load_prompt_template(prompt_template_path)

    st.subheader("1. Edit Your Prompt")
    st.markdown("Modify the template below. This is what will be sent to the model.")

    prompt_text = st.text_area(
        "Prompt Template",
        value=prompt_template,
        height=400,
        label_visibility="collapsed"
    )

    if st.button("🚀 Generate Response"):
        if not api_key:
            st.warning("Please enter your OpenAI API Key in the sidebar.")
        elif not prompt_text.strip():
            st.warning("Prompt cannot be empty.")
        else:
            with st.spinner("Generating response..."):
                # --- THIS IS WHERE YOU'LL CALL THE LLM ---
                # In the next step, you'll replace this with a real API call.
                # Example:
                # from openai import OpenAI
                # client = OpenAI(api_key=api_key)
                # response = client.chat.completions.create(
                #     model="gpt-4-turbo-preview",
                #     messages=[{"role": "user", "content": prompt_text}]
                # )
                # result = response.choices[0].message.content

                # For now, we'll use the known good output from Day 3 as a placeholder.
                from day3_sample_output import secure_s3_output
                result = secure_s3_output

            st.subheader("2. Model Response")
            st.markdown(result)
else:
    st.info("Create a `prompts` directory and add `.md` prompt templates to get started.")