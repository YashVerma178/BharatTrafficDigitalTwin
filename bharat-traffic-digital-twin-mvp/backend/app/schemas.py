from typing import Literal
from pydantic import BaseModel

Controller = Literal["fixed","actuated","ppo"]
Scenario = Literal[
    "normal","heavy","heterogeneous","bike_heavy","auto_heavy",
    "blockage","monsoon","sensor_failure","sensor_spoofing"
]

class StartRequest(BaseModel):
    controller: Controller = "fixed"
    scenario: Scenario = "heterogeneous"
    gui: bool = False

class ControllerRequest(BaseModel):
    controller: Controller

class ScenarioRequest(BaseModel):
    scenario: Scenario
