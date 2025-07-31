# mini-Project 1: Prompt Playground (CLI or Streamlit)

This Streamlit application serves as a playground for experimenting with and testing various prompt engineering techniques, particularly for DevSecOps use cases like generating secure Infrastructure as Code (IaC).

## 🎯 Objective

The goal is to create a simple web UI where you can:
1.  Load pre-defined prompt templates from a directory.
2.  Edit the prompts in real-time.
3.  Send the prompts to an LLM (like OpenAI's GPT models).
4.  View the generated response.

This project directly applies the concepts from Day 2 (Prompt Formats) and Day 3 (Generating Secure IaC).

## How to Run

1.  **Navigate to the project directory:**
    ```bash
    cd /workspace/free-genai-bootcamp-2025/Andrei-Kaparthy/personal-development/day-4/prompt_playground
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

-   `app.py`: The main Streamlit application code.
-   `requirements.txt`: Python dependencies.
-   `prompts/`: A directory containing all your prompt templates in Markdown (`.md`) format.
-   `README.md`: This file.
