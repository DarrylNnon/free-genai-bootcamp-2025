# GPT Threat Modeling Bot (Streamlit App)

This is a deployable Streamlit application that uses the power of Large Language Models (LLMs) to automate threat modeling. It fulfills the tasks for Day 17 of the GenAI DevSecOps Engineer bootcamp.

## 🚀 Features

-   **Dual Input Modes**:
    -   Analyze architecture from a written Markdown description.
    -   **New**: Upload a visual architecture diagram (e.g., PNG, JPG) and have the AI convert it to text for analysis.
-   **STRIDE Analysis**: Performs threat analysis using the industry-standard STRIDE framework.
-   **Few-Shot Prompting**: Uses high-quality, example-driven prompts to ensure structured and relevant output.
-   **Ready to Deploy**: Structured for easy deployment on Hugging Face Spaces.

## 🛠️ Local Setup

1.  **Prerequisites**:
    -   Python 3.8+
    -   An OpenAI API Key

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set your OpenAI API Key**:
    Create a `.env` file in this directory and add your API key:
    ```
    OPENAI_API_KEY="your-super-secret-api-key"
    ```

5.  **Run the app**:
    ```bash
    streamlit run streamlit_app.py
    ```

## 🌐 Deploying to Hugging Face Spaces

1.  **Create a new Space**:
    -   Go to `huggingface.co/new-space`.
    -   Give it a name (e.g., `my-threat-modeler`).
    -   Select **Docker** as the Space SDK.
    -   Choose the **Blank** template.
    -   Choose a free hardware tier.

2.  **Upload Files**:
    -   Upload all your project files: `streamlit_app.py`, `requirements.txt`, `Dockerfile`, the `prompts` directory, and this `README.md`.

3.  **Set Secrets**:
    -   In your new Space, go to the **Settings** tab.
    -   Under **Secrets**, add a new secret:
        -   **Name**: `OPENAI_API_KEY`
        -   **Value**: Paste your OpenAI API key here.
The app will build and launch automatically.