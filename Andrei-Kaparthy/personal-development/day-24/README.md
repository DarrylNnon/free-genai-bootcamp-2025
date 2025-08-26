# 🚀 Day 24: Building an Autonomous FinOps Agent

Welcome to Day 24! Yesterday, we built a FinOps Advisor *tool*. It was powerful, but it required a human to run it. Today, we take the next evolutionary step: we're transforming that tool into an autonomous **AI Agent**.

This project directly addresses the Day 24 task: **Build prompt for anomaly detection + cost remediation**. We're not just building a prompt; we're building the entire agentic system around it.

## The Evolution: From Reactive Tool to Proactive Agent

The key difference between a tool and an agent is proactivity.

*   **The Tool (Day 23):** A human runs a script on a CSV file. It's a reactive process. `Human -> Tool -> Report`
*   **The Agent (Day 24):** The system listens for events and acts on its own. It's a proactive, autonomous loop. `AWS Anomaly Event -> Agent -> Analysis -> Action`

Our FinOps Agent is a serverless application designed to run 24/7 in the cloud, acting as a tireless digital FinOps analyst.

**The Flow:**
`AWS Cost Anomaly Detection` -> `SNS Topic` -> `AWS Lambda` -> `Few-Shot Prompt` -> `GPT-4o` -> `Structured JSON Analysis` -> `Remediation (Alert/CLI)`

---

## The "Brain": An Engineered Few-Shot Prompt

The intelligence of our agent is encapsulated in a single, carefully engineered prompt: `finops_agent/prompts/cost_anomaly_remediation.md`. This isn't just a question; it's a detailed instruction manual for the AI.

### Shot 1: The Persona & Task

We start by defining the agent's role and its output constraints.

```markdown
<PERSONA>
You are an autonomous FinOps AI Agent... Your output must be a single, valid JSON object...
</PERSONA>

<TASK>
Analyze the provided AWS Cost Anomaly JSON data... Your response MUST be a single JSON object with the following structure...
</TASK>
```
This is critical. We're forcing the LLM to act as a structured data processor, not a chatbot. The `response_format={"type": "json_object"}` parameter in our Python code ensures this.

### Shot 2: The Example (The "One-Shot")

We provide a high-quality example of an input anomaly and the exact JSON output we expect.

```markdown
<EXAMPLE>
### Example Input Anomaly Data:
...
### Example Output JSON:
{
  "anomaly_id": "...",
  "summary": "...",
  "root_cause_analysis": "...",
  "remediation_plan": {
    "type": "AUTOMATED_CLI",
    "description": "...",
    "payload": "aws ec2 describe-volumes ...",
    "is_destructive": false
  },
  "confidence_score": 0.95
}
</EXAMPLE>
```
This example teaches the model everything: the desired analytical depth, the tone, and most importantly, the concept of a **safe, non-destructive remediation action**. It learns to suggest `describe` commands before `delete` commands.

### Shot 3: The Context

Finally, we inject the live data from the AWS alert into the prompt.

```markdown
<CONTEXT>
Here is the new AWS Cost Anomaly data to analyze:
```json
{anomaly_data}
```
</CONTEXT>
```

## The "Body": A Serverless Orchestrator

The agent's logic lives in a Python-based AWS Lambda function, defined by a SAM template (`finops_agent/template.yaml`).

*   **`main.py`:** This is the core orchestrator.
    1.  It's triggered by an SNS message when AWS detects a cost anomaly.
    2.  It loads the prompt and injects the anomaly data.
    3.  It calls the GPT-4o model to get the structured JSON analysis.
    4.  It parses the JSON and routes the remediation plan.
*   **Safety First (`AGENT_MODE`):** A crucial feature is the `AGENT_MODE` environment variable.
    *   In `ALERT_ONLY` mode (the default), the agent will only post detailed alerts to Slack, even if the proposed action is a "safe" CLI command. A human must approve the action.
    *   In `AUTO_REMEDIATE` mode, the agent is authorized to execute non-destructive CLI commands. This should be used with extreme caution.

---

## How to Run This Agent

This isn't a simple script; it's a serverless application that lives in your AWS account. Here’s how to get it running, framed as a series of steps.

### Shot 1: The Setup (Configure the AWS Environment)

Before deploying the agent, you need to set up its environment.

1.  **Enable AWS Cost Anomaly Detection:** In the AWS Cost Management console, create a monitor to watch your costs. This is the agent's "eyes."
2.  **Create an SNS Topic:** Create a new Amazon SNS topic (e.g., `CostAnomalyNotifications`). This will be the "nervous system" that transmits alerts.
3.  **Configure Anomaly Subscriptions:** Link your cost monitor to the SNS topic. Configure it to send a notification to the SNS topic whenever a new anomaly is detected.
4.  **Store Secrets:** Store your `OPENAI_API_KEY` and `SLACK_WEBHOOK_URL` in AWS Systems Manager (SSM) Parameter Store as `SecureString` parameters. The SAM template is pre-configured to read from `/finops/openai/apikey` and `/finops/slack/webhook`.

    You can create these using the AWS CLI. **Remember to replace the placeholder values with your actual secrets and run these in the same AWS region you are deploying to.**

    ```bash
    # Create the OpenAI API Key parameter
    aws ssm put-parameter \
        --name "/finops/openai/apikey" \
        --value "sk-YOUR_OPENAI_API_KEY" \
        --type "SecureString"

    # Create the Slack Webhook URL parameter
    aws ssm put-parameter \
        --name "/finops/slack/webhook" \
        --value "https://hooks.slack.com/services/T0000/B0000/XXXXXXXXXXXXXXXX" \
        --type "SecureString"
    ```

### Shot 2: The Deployment (Using AWS SAM)

The agent is packaged as an AWS SAM application for easy deployment.

1.  **Install AWS SAM CLI:** If you haven't already, install the SAM CLI.
2.  **Build the Application:** Navigate to the `finops_agent` directory and run:
    ```bash
    sam build
    ```
3.  **Deploy the Agent:** Deploy the application using the guided deployment process. You will need to provide the ARN of the SNS topic you created in Shot 1.
    ```bash
    sam deploy --guided
    ```
    SAM will package your code, create the Lambda function, set up the necessary IAM roles and permissions, and subscribe the function to the SNS topic.

### Shot 3: The Trigger (The First Anomaly)

Once deployed, the agent is live and waiting.

1.  **Waiting:** The Lambda function is dormant, costing you nothing.
2.  **Event:** AWS Cost Anomaly Detection identifies a spike in your spending and publishes a message to your SNS topic.
3.  **Action:** The SNS subscription instantly triggers the `FinOpsAgentFunction` Lambda.
4.  **Analysis & Response:** The Lambda function executes the `main.py` script, calling the LLM for analysis and posting the structured result to Slack, all within seconds.

The agent is now your autonomous watchdog, monitoring your cloud costs 24/7.

## Day 24 Conclusion

Today, we've built a system that moves beyond simple automation. We created an autonomous agent that can perceive its environment (cost anomalies), reason about the cause (via an LLM), and take action (alerting or remediation). This is the future of DevSecOps: building intelligent, scalable systems that act as force multipliers for engineering teams, allowing them to focus on building value, not fighting fires.
