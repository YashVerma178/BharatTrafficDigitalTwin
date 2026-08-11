import argparse,csv
from pathlib import Path
from simulation.core import IntersectionSim
from simulation.controllers.controllers import FixedTimeController,ActuatedController,PPOController

def run(controller,scenario,steps,seed,model="models/ppo/traffic_signal_ppo"):
    sim=IntersectionSim(scenario,seed)
    c={"fixed":FixedTimeController(),"actuated":ActuatedController(),"ppo":PPOController(model)}[controller]
    q=w=v=0
    for _ in range(steps):
        st=sim.snapshot()
        action=c.act(sim.observation()) if controller=="ppo" else c.act(st)
        sim.step(*action)
        st=sim.snapshot(); q+=st["average_queue"]; w+=st["average_waiting_time"]; v+=st["average_speed"]
    return {"controller":controller,"scenario":scenario,"seed":seed,"steps":steps,
    "average_queue":round(q/steps,4),"average_waiting_time":round(w/steps,4),
    "average_speed":round(v/steps,4),"delay_proxy":round((q+w)/steps,4),
    "throughput":sim.s.throughput,"stops":sim.s.stops,"signal_switches":sim.s.switches}

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--episodes",type=int,default=3); ap.add_argument("--steps",type=int,default=600)
    ap.add_argument("--scenarios",nargs="+",default=["normal","heterogeneous","heavy"]); a=ap.parse_args()
    rows=[]
    for sc in a.scenarios:
        for ep in range(a.episodes):
            for c in ["fixed","actuated"]:
                rows.append(run(c,sc,a.steps,100+ep))
            if Path("models/ppo/traffic_signal_ppo.zip").exists(): rows.append(run("ppo",sc,a.steps,100+ep))
    out=Path("data/results/controller_comparison.csv"); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=rows[0]); wr.writeheader(); wr.writerows(rows)
    print("Saved",out,"rows",len(rows))
