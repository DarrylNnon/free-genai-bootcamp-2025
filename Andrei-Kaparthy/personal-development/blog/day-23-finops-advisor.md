# 📈 Day 23: Building a GPT FinOps Advisor with Few-Shot Prompting

Welcome to Day 23 of the GenAI DevSecOps Engineer journey! Today, we're building a practical, high-value tool that addresses a universal challenge in the cloud: understanding and optimizing costs.

## The Problem: Cloud Cost Reports are a Nightmare

Anyone who has looked at a raw AWS Cost and Usage Report (CUR) knows it can be overwhelming. It's a massive CSV file with thousands of rows, detailing every single cent spent across dozens of services, accounts, and usage types. While powerful, it's not exactly human-readable.

Traditionally, making sense of this data requires a dedicated FinOps (Financial Operations) expert who can spend hours, or even days, analyzing the data to find savings opportunities.

## The Solution: An AI FinOps Advisor

Today's project is to build a command-line tool that automates this initial analysis. We'll create a **GPT FinOps Advisor** that takes a raw AWS cost CSV as input and generates a clean, actionable Markdown report, just like a human expert would.

**The Flow:**
`AWS Cost CSV` -> `Python Script` -> `Few-Shot Prompt` -> `GPT-4o` -> `Markdown Report`

The magic here isn't in complex algorithms or machine learning models we train ourselves. The "intelligence" of our application is almost entirely encapsulated within a single, well-crafted prompt.

---

## The "Few-Shot" Technique in Action

This project is a perfect demonstration of the **few-shot prompting** technique. We're essentially teaching the LLM how to perform a specialized task by giving it instructions and a high-quality example.

Our prompt, located in `prompts/finops_insights.md`, is the brain of the operation. Let's break it down into its core components, or "shots."

### Shot 1: The Persona

First, we tell the LLM *who* it should be.

```markdown
<PERSONA>
You are an expert FinOps (Financial Operations) analyst. Your specialty is analyzing raw cloud cost data and translating it into high-level, actionable business insights for engineering and leadership teams. You are concise, data-driven, and always focus on actionable recommendations.
</PERSONA>
```

This is crucial. By setting a persona, we frame the model's entire response. It's no longer just a text-completion engine; it's an expert analyst, and it will adopt the tone, vocabulary, and focus of that role.

### Shot 2: The Example (The "One-Shot")

This is the most important part of the prompt. We provide a complete, high-quality example of the task we want it to perform.

```markdown
<EXAMPLE>
### Example Input CSV Data:
...
### Example Output Report:

## 📈 FinOps Analysis Report

### Executive Summary
The primary cost drivers for this period are **EC2 Data Transfer** and **RDS Instances**...

### 1. Key Cost Drivers
*   **EC2 Data Transfer ($550.20):** This is the single largest cost...

### 2. Actionable Recommendations
1.  **Investigate EC2 Data Transfer:**
    *   **Action:** Identify which EC2 instances are responsible...
</EXAMPLE>
```

By providing a sample input and the corresponding ideal output, we're not just telling the LLM what to do—we're *showing* it. It learns the desired Markdown structure, the analytical style, and the focus on actionable advice. This is far more effective than trying to describe the output format in words alone.

### Shot 3: The Dynamic Context

Finally, we provide the actual data we want the model to analyze.

```markdown
<CONTEXT>
Here is the AWS Cost data to analyze:
```csv
{csv_data}
```
</CONTEXT>
```

Our Python script reads the user-provided CSV, converts it to a string, and injects it into the prompt using the `{csv_data}` placeholder. This combines our expert instructions with real-world data for analysis.

## The Python Orchestrator

The `main.py` script is simple and acts as the conductor for this process.

1.  **Parses Arguments**: Uses `argparse` to get the input CSV path and optional output file path.
2.  **Reads Files**: Reads the prompt template and the cost data from the CSV using `pandas`.
3.  **Calls the API**: Initializes the modern `openai` client, formats the final prompt with the CSV data, and sends it to the `gpt-4o` model.
4.  **Generates Output**: Prints the generated Markdown report to the console or saves it to the specified output file.

## Day 23 Conclusion

Today we built a tool that provides immediate, tangible value. We've taken a complex, manual task and automated its most time-consuming aspects using the power of a well-engineered prompt. This project is a fantastic example of how GenAI can be used to create "expert-in-a-box" tools that democratize specialized knowledge and accelerate workflows.