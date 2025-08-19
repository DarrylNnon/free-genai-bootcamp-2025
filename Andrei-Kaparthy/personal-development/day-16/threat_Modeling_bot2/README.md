# GPT Threat Modeling Bot

This tool uses the power of Large Language Models (LLMs) to automate the process of threat modeling. It takes a description of a system architecture written in Markdown, analyzes it against the STRIDE and OWASP Top 10 frameworks, and generates a comprehensive threat model report.

This is a real-world implementation of the project from Day 15 & 16 of the [GenAI DevSecOps Engineer Calendar](https://github.com/exampro/free-genai-bootcamp-2025/blob/main/Andrei-Kaparthy/personal-development/readme.md).

## 🚀 Features

-   Analyzes architecture from a simple Markdown file.
-   Performs threat analysis using the **STRIDE** framework.
-   Identifies web application risks based on the **OWASP Top 10**.
-   Uses sophisticated **few-shot prompts** for high-quality, structured output.
-   Generates a clean, actionable report in Markdown format.

## 🛠️ Setup

### 1. Prerequisites

-   Python 3.8+
-   An OpenAI API Key

### 2. Installation

1.  **Clone the repository (if you haven't already).**

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set your OpenAI API Key:**

    Create a `.env` file in the `threat_modeling_bot` directory and add your API key to it:

    `cp .env.example .env`

    ```
    OPENAI_API_KEY="your-super-secret-api-key"
    ```
    The application will load this key automatically.

## 📖 Usage

Run the script from the command line, passing the path to your architecture markdown file as an argument.

```bash
python main.py <path_to_your_architecture_file.md>
```

### Example

An example architecture file (`example_architecture.md`) is included. To run the analysis on it:

```bash
python main.py example_architecture.md
```

This will generate a `THREAT_MODEL_REPORT.md` file in the same directory.

## 🧠 How It Works: The Power of Few-Shot Prompts

The magic of this tool lies in the prompts located in the `/prompts` directory. Instead of just asking the LLM to "find threats" (a zero-shot prompt), we provide it with a high-quality example of what a good analysis looks like.

*   **`stride_prompt.md`**: This prompt contains a persona, a clear task, and a detailed example of a STRIDE analysis for a sample component. This teaches the model the exact format, tone, and depth required for its output.

*   **`owasp_prompt.md`**: This prompt does the same for the OWASP Top 10, focusing on web application-specific vulnerabilities. It shows the model how to map architectural features to specific OWASP categories and suggest relevant mitigations.

By using this few-shot technique, we guide the LLM to produce structured, relevant, and actionable security reports, moving beyond generic advice to expert-level analysis.

## 📂 Project Structure

```
.
├── README.md
├── main.py                 # Main script to run the analysis
├── requirements.txt        # Python dependencies
├── .env                    # For your API key (create this file)
├── example_architecture.md # An example input file
├── THREAT_MODEL_REPORT.md  # The generated output report
└── prompts/
    ├── stride_prompt.md    # Few-shot prompt for STRIDE analysis
    └── owasp_prompt.md     # Few-shot prompt for OWASP Top 10 analysis
```
i have update the code to anewer ai version(gpt-4o-turbo)