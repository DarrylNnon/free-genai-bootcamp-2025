from typing import List, Literal
from pydantic import BaseModel, Field

class SimulationStep(BaseModel):
    """
    Defines a single step in an adversarial simulation plan.
    """
    step_number: int = Field(..., description="The sequential number of the step.")
    description: str = Field(..., description="A clear, concise description of the action to be taken in this step.")
    command: str = Field(..., description="The exact command to be executed for this step.")
    platform: Literal["windows", "linux", "macos"] = Field(..., description="The target operating system for the command.")
    expected_observables: str = Field(..., description="The expected logs, events, or artifacts that this step should generate.")

class SimulationPlan(BaseModel):
    """
    Defines the overall structure for a MITRE ATT&CK simulation plan.
    """
    technique_id: str = Field(..., description="The MITRE ATT&CK technique ID (e.g., T1053.005).")
    technique_name: str = Field(..., description="The full name of the MITRE ATT&CK technique.")
    tactic: str = Field(..., description="The MITRE ATT&CK tactic(s) associated with the technique (e.g., Execution, Persistence).")
    scenario_description: str = Field(..., description="A high-level overview of the attack scenario being simulated.")
    steps: List[SimulationStep] = Field(..., description="A list of detailed, step-by-step actions to perform the simulation.")