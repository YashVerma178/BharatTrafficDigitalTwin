from simulation.core import IntersectionSim
from simulation.controllers.controllers import FixedTimeController,ActuatedController,PPOController
class SimulationManager:
    def __init__(self):
        self.running=False; self.controller_name="fixed"; self.scenario="heterogeneous"; self.seed=42
        self.sim=IntersectionSim(self.scenario,self.seed); self.controller=FixedTimeController()
    def configure(self,controller,scenario,seed=42):
        self.controller_name=controller; self.scenario=scenario; self.seed=seed; self.sim=IntersectionSim(scenario,seed)
        self.controller={"fixed":FixedTimeController,"actuated":ActuatedController,"ppo":PPOController}[controller]()
    def snapshot(self):
        s=self.sim.snapshot(); s.update(controller=self.controller_name,scenario=self.scenario,running=self.running)
        s["sensor_status"]="ANOMALY" if self.scenario=="sensor_spoofing" else ("PARTIAL" if self.scenario=="sensor_failure" else "OK")
        s["sensor_anomaly"]=self.scenario=="sensor_spoofing"; return s
    def tick(self):
        st=self.sim.snapshot(); action=self.controller.act(self.sim.observation()) if self.controller_name=="ppo" else self.controller.act(st)
        self.sim.step(*action); return self.snapshot()
