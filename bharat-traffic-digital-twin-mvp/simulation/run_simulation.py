import argparse
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "simulation" / "sumo" / "config" / "traffic.sumocfg"

def run(controller="fixed", scenario="heterogeneous", gui=False, seconds=300):
    try:
        import traci
    except ImportError as exc:
        raise SystemExit("Install backend/requirements.txt first.") from exc

    binary = "sumo-gui" if gui else "sumo"
    if shutil.which(binary) is None:
        raise SystemExit(f"{binary} was not found on PATH. Install SUMO first.")

    traci.start([binary, "-c", str(CFG), "--start", "--quit-on-end"])
    try:
        for step in range(seconds):
            traci.simulationStep()
            if step % 10 == 0:
                queues = {}
                for edge in ["N2J", "S2J", "E2J", "W2J"]:
                    queues[edge] = sum(
                        traci.lane.getLastStepHaltingNumber(lane)
                        for lane in traci.edge.getLaneIDs(edge)
                    )
                print(f"t={step:4d}s phase={traci.trafficlight.getPhase('J')} queues={queues}")
    finally:
        traci.close()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--controller", choices=["fixed","actuated","ppo"], default="fixed")
    p.add_argument("--scenario", default="heterogeneous")
    p.add_argument("--gui", action="store_true")
    p.add_argument("--seconds", type=int, default=300)
    a = p.parse_args()
    run(a.controller, a.scenario, a.gui, a.seconds)
