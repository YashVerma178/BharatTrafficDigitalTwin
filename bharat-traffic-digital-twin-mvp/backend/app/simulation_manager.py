import asyncio
import random
from datetime import datetime, timezone

class SimulationManager:
    def __init__(self):
        self.running = False
        self.controller = "fixed"
        self.scenario = "heterogeneous"
        self.task = None
        self.state = self._initial()

    def _initial(self):
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "current_phase": "NORTH_SOUTH",
            "phase_remaining": 30,
            "queues": {"north":0,"south":0,"east":0,"west":0},
            "waiting_times": {"north":0,"south":0,"east":0,"west":0},
            "speeds": {"north":0,"south":0,"east":0,"west":0},
            "vehicle_counts": {"car":0,"motorcycle":0,"auto":0,"bus":0,"truck":0},
            "throughput": 0,
            "controller": self.controller,
            "scenario": self.scenario,
            "sensor_status": "OK",
            "anomaly": False,
        }

    async def start(self, controller, scenario):
        self.controller, self.scenario, self.running = controller, scenario, True
        if not self.task or self.task.done():
            self.task = asyncio.create_task(self._loop())

    async def stop(self):
        self.running = False
        if self.task:
            self.task.cancel()
            self.task = None

    async def _loop(self):
        while self.running:
            self.tick()
            await asyncio.sleep(1)

    def tick(self):
        factor = {
            "normal":.7,"heavy":1.5,"heterogeneous":1.0,"bike_heavy":1.2,
            "auto_heavy":1.25,"blockage":1.8,"monsoon":1.6,
            "sensor_failure":1.0,"sensor_spoofing":1.0
        }[self.scenario]
        for d in self.state["queues"]:
            q = max(0, int(random.gauss(15*factor,5)))
            self.state["queues"][d] = q
            self.state["waiting_times"][d] = round(q*1.7,1)
            self.state["speeds"][d] = round(max(1,12-q/8),1)
        self.state["vehicle_counts"] = {
            "car":int(30*factor),"motorcycle":int(18*factor),
            "auto":int(8*factor),"bus":int(3*factor),"truck":int(2*factor)
        }
        self.state["throughput"] = int(500/factor)
        self.state["controller"] = self.controller
        self.state["scenario"] = self.scenario
        self.state["anomaly"] = self.scenario == "sensor_spoofing"
        self.state["sensor_status"] = "ANOMALY" if self.state["anomaly"] else "OK"
        self.state["timestamp"] = datetime.now(timezone.utc).isoformat()
        self.state["phase_remaining"] -= 1
        if self.state["phase_remaining"] <= 0:
            self.state["phase_remaining"] = 30
            self.state["current_phase"] = (
                "EAST_WEST" if self.state["current_phase"]=="NORTH_SOUTH"
                else "NORTH_SOUTH"
            )
