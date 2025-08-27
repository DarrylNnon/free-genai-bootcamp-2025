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