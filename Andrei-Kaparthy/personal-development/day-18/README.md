# ATT&CK-GPT Adversarial Simulator

**ATT&CK-GPT** is a production-ready, LLM-powered tool designed to generate realistic adversarial simulation plans based on the MITRE ATT&CK® framework. It provides a structured, automated way for security teams to test their defenses against specific attacker techniques.

## Problem Statement

Modern security operations centers (SOCs) and blue teams need to continuously validate their detection and response capabilities. Manually creating realistic attack scenarios is time-consuming, requires deep expertise, and can be difficult to scale. While automated breach and attack simulation (BAS) tools exist, they can be expensive and lack the flexibility to generate novel or customized scenarios.

## Solution

This project leverages the power of Large Language Models (LLMs) to bridge this gap. By providing a specific MITRE ATT&CK technique ID, **ATT&CK-GPT** uses a sophisticated few-shot prompt to instruct an LLM (like GPT-4) to generate a detailed, step-by-step simulation plan.

The output is a structured JSON object, making it easy to integrate with other security tools, such as SIEMs, SOAR platforms, or automated testing frameworks.

## Features

*   **MITRE ATT&CK Aligned**: Generates simulations for any specified ATT&CK technique.
*   **LLM-Powered**: Uses state-of-the-art language models to create creative and realistic scenarios.
*   **Structured Output**: Delivers simulation plans in a validated JSON format using Pydantic models.
*   **Platform-Specific Commands**: Provides commands for Windows, Linux, and macOS where applicable.
*   **Actionable Intelligence**: Includes expected observables for each step, guiding defenders on what to look for.
*   **Production-Ready**: Built with a clean architecture, configuration management, and clear separation of concerns.

## Architecture Overview

The application is designed with modularity and scalability in mind:

*   **`config/settings.py`**: Manages configuration (e.g., API keys) via environment variables.
*   **`src/models/simulation_plan.py`**: Defines the Pydantic data models for the simulation plan, ensuring type safety and structured data.
*   **`src/utils/prompts.py`**: Contains the core few-shot prompt template that guides the LLM's behavior. This is the "secret sauce" of the application.
*   **`src/core/llm_handler.py`**: A dedicated client for interacting with the LLM API.
*   **`src/core/simulation_generator.py`**: The main service that orchestrates the process of generating a simulation plan.
*   **`scripts/run_simulation.py`**: A command-line interface (CLI) for easily running the simulator.

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd attack-gpt-simulator
    ```

2.  **Install dependencies:**
    This project uses Poetry for dependency management.
    ```bash
    poetry install
    ```

3.  **Configure Environment Variables:**
    Copy the example environment file and add your LLM API key.
    ```bash
    cp .env.example .env
    ```
    Now, edit `.env` and insert your API key:
    ```
    LLM_API_KEY="sk-your-openai-api-key-here"
    ```

## Usage

Use the `run_simulation.py` script to generate a plan. You must provide a MITRE ATT&CK technique ID as an argument.

**Example:** Generate a simulation for "Scheduled Task/Job: Scheduled Task" (T1053.005).

```bash
poetry run python scripts/run_simulation.py T1053.005
```

### Example Output

The script will print a formatted JSON object containing the complete simulation plan.

```json
{
    "technique_id": "T1053.005",
    "technique_name": "Scheduled Task/Job: Scheduled Task",
    "tactic": "Execution, Persistence, Privilege Escalation",
    "scenario_description": "An adversary creates a scheduled task on a Windows host to execute a malicious payload at a specific time or on a recurring basis. This ensures persistence on the system.",
    "steps": [
        {
            "step_number": 1,
            "description": "Create a simple malicious payload (e.g., a script that writes a file to disk) to be executed by the scheduled task.",
            "command": "echo 'echo \"Adversary was here\" > C:\\Users\\Public\\persistence.txt' > C:\\Users\\Public\\payload.bat",
            "platform": "windows",
            "expected_observables": "File creation: C:\\Users\\Public\\payload.bat. Command line execution of 'echo'."
        },
        {
            "step_number": 2,
            "description": "Create a new scheduled task to run the payload every day at 2:00 PM.",
            "command": "schtasks /create /tn \"MaliciousUpdater\" /tr \"C:\\Users\\Public\\payload.bat\" /sc DAILY /st 14:00",
            "platform": "windows",
            "expected_observables": "Process creation of 'schtasks.exe' with '/create' argument. New entry in the Task Scheduler library. Windows Event ID 4698 (A scheduled task was created)."
        }
    ]
}
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for bugs, feature requests, or improvements to the prompt templates.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.