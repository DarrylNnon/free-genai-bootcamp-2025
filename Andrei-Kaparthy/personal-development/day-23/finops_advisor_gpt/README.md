# 📈 GPT FinOps Advisor

Welcome to the GPT FinOps Advisor, a project from Day 23 of the "LEGENDARY 60-Day GenAI DevSecOps Engineer" challenge. This tool leverages a Large Language Model (LLM) to analyze raw AWS Cost Explorer data and generate high-level, actionable FinOps insights.

Instead of manually sifting through complex CSV files, this tool provides a clear, expert-level summary that identifies major cost drivers, highlights potential savings, and suggests concrete optimization strategies.

## 🚀 The Flow

The advisor follows a simple but powerful workflow:

**Input (AWS Cost Explorer CSV) → GPT (Few-Shot FinOps Analysis) → Output (Markdown Report)**

1.  **Input**: You provide a CSV file exported from AWS Cost and Usage Reports (CUR) or Cost Explorer.
2.  **GPT Analysis**: The tool reads the CSV, injects the data into a specialized few-shot prompt, and sends it to an LLM. The prompt is engineered to make the LLM act as a seasoned FinOps expert.
3.  **Output**: The bot generates a detailed, well-formatted Markdown report with summaries, key findings, and actionable recommendations.

## 🎯 Objective

- To automate the initial analysis of cloud cost data, saving hours of manual work.
- To democratize FinOps by making expert-level analysis accessible to any engineer.
- To demonstrate a practical, high-value use case for LLMs in cloud management.
- To master the art of few-shot prompting for a specialized, data-driven task.

## 🛠️ Setup and Installation

Follow these steps to get the GPT FinOps Advisor running on your local machine.

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

Execute the `main.py` script from your terminal, passing the path to your cost report CSV file as an argument. An example report is provided in the `examples/` directory.

```bash
python main.py examples/sample_aws_cost_report.csv --output finops_report.md
```

The script will generate a Markdown report named `finops_report.md` in your current directory. If you omit the `--output` flag, the report will be printed directly to the console.