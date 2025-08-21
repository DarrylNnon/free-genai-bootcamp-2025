# The "secret sauce" of the application.
# This few-shot prompt template guides the LLM to generate a structured
# and realistic adversarial simulation plan in JSON format.

FEW_SHOT_PROMPT_TEMPLATE = """
You are an expert cybersecurity red teamer and AI assistant. Your task is to generate a detailed, step-by-step adversarial simulation plan based on a given MITRE ATT&CK® technique ID.

The output must be a single, valid JSON object that conforms to the provided Pydantic models. Do not include any text or explanations outside of the JSON object.

Here are some examples of how to structure the plan:

---
**EXAMPLE 1**

**Technique ID:** T1053.005

**Generated Plan:**
```json
{
    "technique_id": "T1053.005",
    "technique_name": "Scheduled Task/Job: Scheduled Task",
    "tactic": "Execution, Persistence, Privilege Escalation",
    "scenario_description": "An adversary creates a scheduled task on a Windows host to execute a malicious payload at a specific time or on a recurring basis. This ensures persistence on the system and can be used to run code with higher privileges.",
    "steps": [
        {
            "step_number": 1,
            "description": "Create a simple malicious payload (e.g., a script that writes a file to disk) to be executed by the scheduled task. This simulates the stage where an attacker places their tool on the system.",
            "command": "echo 'echo \\"Adversary was here\\" > C:\\\\Users\\\\Public\\\\persistence.txt' > C:\\\\Users\\\\Public\\\\payload.bat",
            "platform": "windows",
            "expected_observables": "File creation: C:\\\\Users\\\\Public\\\\payload.bat. Command line execution of 'echo'."
        },
        {
            "step_number": 2,
            "description": "Create a new scheduled task to run the payload every day at 2:00 PM. This is the core of the persistence technique.",
            "command": "schtasks /create /tn \\"MaliciousUpdater\\" /tr \\"C:\\\\Users\\\\Public\\\\payload.bat\\" /sc DAILY /st 14:00",
            "platform": "windows",
            "expected_observables": "Process creation of 'schtasks.exe' with '/create' argument. New entry in the Task Scheduler library. Windows Event ID 4698 (A scheduled task was created). Registry modification in HKLM\\\\SOFTWARE\\\\Microsoft\\\\Windows NT\\\\CurrentVersion\\\\Schedule\\\\TaskCache\\\\Tree."
        },
        {
            "step_number": 3,
            "description": "Verify the task has been created and is waiting to run. This is a reconnaissance step an attacker might take.",
            "command": "schtasks /query /tn \\"MaliciousUpdater\\"",
            "platform": "windows",
            "expected_observables": "Process creation of 'schtasks.exe' with '/query' argument. Network connections are not expected, but process activity will be present."
        }
    ]
}
```
---
**EXAMPLE 2**

**Technique ID:** T1574.002

**Generated Plan:**
```json
{
    "