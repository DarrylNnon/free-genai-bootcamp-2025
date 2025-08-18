# GPT Threat Modeling Bot

Welcome to the GPT Threat Modeling Bot, a project from Day 15 of the "LEGENDARY 60-Day GenAI DevSecOps Engineer" challenge. This tool automates the generation of a threat model from a system architecture document using either the **STRIDE** or **DREAD** frameworks.

It leverages a powerful Large Language Model (LLM) with a sophisticated few-shot prompt to analyze architecture descriptions and produce high-quality, actionable security reports.

## 🚀 The Flow

The bot follows a simple but powerful workflow:

**Input (Markdown Architecture) → GPT (Few-Shot STRIDE/DREAD Analysis) → Output (Markdown Report)**

1.  **Input**: You provide a Markdown file describing your system's components and data flows.
2.  **GPT Analysis**: The bot injects your architecture into a specialized prompt that teaches the LLM to act as a security expert and perform a STRIDE analysis.
3.  **Output**: The bot prints a detailed, well-formatted Markdown report to your console or saves it to a file.

## 🎯 Objective

- To automate and scale the threat modeling process.
- To provide a consistent and structured approach to identifying security threats early in the design phase.
- To demonstrate the power of few-shot prompting to guide LLMs toward complex, expert-level tasks.

## 🛠️ Setup and Installation

Follow these steps to get the GPT Threat Modeling Bot running on your local machine.

### 1. Prerequisites

- Python 3.8+
- An OpenAI API key

### 2. Clone the Repository

If you haven't already, clone the project to your local machine.

### 3. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
# On Windows, use: .venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Copy the example environment file and add your OpenAI API key.

```bash
cp .env.example .env
```
Now, edit the `.env` file and add your key:
```
OPENAI_API_KEY="sk-..."
```

## 🏃 How to Run

Execute the `main.py` script from your terminal, passing the path to your architecture file as an argument. An example architecture is provided in the `examples/` directory.

```bash
python main.py examples/web_app_architecture.md
```

### Generating a DREAD Report

Use the `--framework` flag to select the DREAD model.
```bash
python main.py examples/web_app_architecture.md --framework DREAD
```

### Saving the Report to a File

Use the `--output` flag to save the generated report to a Markdown file.
```bash
python main.py examples/web_app_architecture.md --output stride_report.md
```

### Combining Flags

You can combine flags to generate a DREAD report and save it to a file.
```bash
python main.py examples/web_app_architecture.md --framework DREAD --output dread_report.md
```

The bot will then generate and print the full STRIDE threat model report to your console.