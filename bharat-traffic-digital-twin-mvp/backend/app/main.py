import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.app.schemas import StartRequest, ControllerRequest, ScenarioRequest
from backend.app.simulation_manager import SimulationManager

app = FastAPI(title="Bharat Traffic Digital Twin MVP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
manager = SimulationManager()

@app.get("/api/status")
async def status():
    return manager.state

@app.get("/api/metrics")
async def metrics():
    s = manager.state
    return {
        "average_queue": round(sum(s["queues"].values())/4,2),
        "average_waiting_time": round(sum(s["waiting_times"].values())/4,2),
        "average_speed": round(sum(s["speeds"].values())/4,2),
        "throughput": s["throughput"]
    }

@app.get("/api/scenarios")
async def scenarios():
    return ["normal","heavy","heterogeneous","bike_heavy","auto_heavy","blockage","monsoon","sensor_failure","sensor_spoofing"]

@app.post("/api/simulation/start")
async def start(req: StartRequest):
    await manager.start(req.controller, req.scenario)
    return {"ok": True, "status": manager.state}

@app.post("/api/simulation/stop")
async def stop():
    await manager.stop()
    return {"ok": True}

@app.post("/api/controller")
async def controller(req: ControllerRequest):
    manager.controller = req.controller
    manager.state["controller"] = req.controller
    return {"ok": True}

@app.post("/api/scenario")
async def scenario(req: ScenarioRequest):
    manager.scenario = req.scenario
    manager.state["scenario"] = req.scenario
    return {"ok": True}

@app.websocket("/ws/traffic")
async def traffic(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            await ws.send_json(manager.state)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
