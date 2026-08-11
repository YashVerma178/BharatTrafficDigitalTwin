import asyncio,csv
from pathlib import Path
from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from backend.app.simulation_manager import SimulationManager
from experiments.run_experiments import run
ROOT=Path(__file__).resolve().parents[2]; RESULTS=ROOT/"data/results"
app=FastAPI(title="Bharat Traffic Digital Twin",version="1.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
m=SimulationManager()
class Start(BaseModel): controller:str="fixed"; scenario:str="heterogeneous"; seed:int=42
class Controller(BaseModel): controller:str
class Scenario(BaseModel): scenario:str
class Experiment(BaseModel): scenarios:list[str]=["normal","heterogeneous","heavy"]; episodes:int=2; steps:int=400
@app.get("/",response_class=HTMLResponse)
async def root(): return (ROOT/"frontend/index.html").read_text()
@app.get("/api/status")
async def status(): return m.snapshot()
@app.get("/api/controllers")
async def controllers(): return ["fixed","actuated","ppo"]
@app.get("/api/scenarios")
async def scenarios():
    from simulation.core import SCENARIOS
    return list(SCENARIOS)
@app.get("/api/metrics")
async def metrics():
    s=m.snapshot(); return {k:s[k] for k in ["average_queue","average_waiting_time","average_speed","throughput","delay_proxy","stops","signal_switches"]}
@app.post("/api/simulation/start")
async def start(x:Start): m.configure(x.controller,x.scenario,x.seed); m.running=True; return m.snapshot()
@app.post("/api/simulation/stop")
async def stop(): m.running=False; return {"ok":True}
@app.post("/api/controller")
async def controller(x:Controller): m.configure(x.controller,m.scenario,m.seed); m.running=False; return m.snapshot()
@app.post("/api/scenario")
async def scenario(x:Scenario): m.configure(m.controller_name,x.scenario,m.seed); m.running=False; return m.snapshot()
@app.post("/api/experiments/run")
async def experiments(x:Experiment):
    RESULTS.mkdir(parents=True,exist_ok=True); rows=[]
    for sc in x.scenarios:
        for ep in range(x.episodes):
            for c in ["fixed","actuated"]:
                rows.append(run(c,sc,x.steps,100+ep))
            if Path("models/ppo/traffic_signal_ppo.zip").exists(): rows.append(run("ppo",sc,x.steps,100+ep))
    out=RESULTS/"api_experiment_results.csv"
    with out.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=rows[0]); wr.writeheader(); wr.writerows(rows)
    return {"ok":True,"rows":len(rows),"file":str(out.relative_to(ROOT))}
@app.get("/api/results")
async def results():
    out=RESULTS/"api_experiment_results.csv"
    if not out.exists(): return []
    with out.open(encoding="utf-8") as f:return list(csv.DictReader(f))
@app.websocket("/ws/traffic")
async def ws(sock:WebSocket):
    await sock.accept()
    try:
        while True:
            payload=m.tick() if m.running else m.snapshot()
            await sock.send_json(payload); await asyncio.sleep(.5)
    except WebSocketDisconnect: pass
