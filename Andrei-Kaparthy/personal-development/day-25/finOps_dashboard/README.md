# 📊 Day 25: Interactive FinOps Dashboard

Welcome to Day 25! Today, we're building on the FinOps analysis capabilities from Day 23 and 24 by creating a rich, interactive web dashboard.

The goal is to move beyond static reports and autonomous alerts to provide a user-driven tool for cost exploration. This project directly addresses the Day 25 task: **Add Dash UI with trend graphs 
 GPT output**.

# architechture
/workspace/free-genai-bootcamp-2025/Andrei-Kaparthy/personal-development/day-25/
├── README.md
└── finops_dashboard/
    ├── app.py
    ├── requirements.txt
    ├── .env.example
    ├── assets/
    │   └── style.css
    ├── components/
    │   ├── __init__.py
    │   ├── graphs.py
    │   ├── header.py
    │   ├── report.py
    │   └── uploader.py
    ├── examples/
    │   └── sample_aws_cost_report.csv
    ├── modules/
    │   ├── __init__.py
    │   ├── analyzer.py
    │   └── data_loader.py
    └── prompts/
        └── finops_insights.md


## The Project: An Interactive FinOps Dashboard

This project is a web application built with **Plotly Dash**. It allows a user to:

1.  **Upload their own AWS Cost and Usage CSV file.**
2.  **Instantly see visualizations** of their cost data, such as cost per service and cost over time.
3.  **Trigger a GPT-powered analysis** with the click of a button.
4.  **View the expert-level FinOps report** directly in the web interface.

This approach combines the best of data visualization and generative AI, creating a powerful tool for any engineer or manager looking to understand their cloud spend.

## How to Run

All the code for this project is located in the `finops_dashboard/` directory. Please see the `finops_dashboard/README.md` for detailed setup and execution instructions.

# 📈 Interactive FinOps Dashboard

This Dash application provides an interactive interface for analyzing AWS Cost and Usage reports. It combines data visualization with GPT-powered analysis to deliver actionable FinOps insights.

## 🚀 Features

- **Interactive File Upload**: Users can upload their own AWS Cost CSV files.
- **Dynamic Visualizations**: Automatically generates graphs for cost by service and cost over time.
- **On-Demand AI Analysis**: A "Generate Report" button triggers a call to GPT-4o to analyze the cost data.
- **Few-Shot Prompting**: Uses the expertly crafted prompt from Day 23 to ensure a high-quality, structured analysis.
- **Clean, Modern UI**: A simple and professional interface built with Dash and a custom stylesheet.

## 🛠️ Setup and Installation

Follow these steps to get the dashboard running on your local machine.

### 1. Prerequisites

- Python 3.8+
- An OpenAI API key

### 2. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
# On Windows, use: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and add your OpenAI API key.

```bash
cp .env.example .env
```
Now, edit the `.env` file and add your key:
```
OPENAI_API_KEY="sk-..."
```

## 🏃 How to Run

Execute the `app.py` script from your terminal. An example report is provided in the `examples/` directory that you can use for testing.

```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:8050`. You're ready to analyze!
