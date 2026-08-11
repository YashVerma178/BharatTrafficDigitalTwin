# Bharat Traffic Digital Twin — MVP

Simulation-first research prototype for adaptive traffic signal control under heterogeneous Indian-style traffic.

## Core MVP
- One 4-way SUMO intersection
- Cars, motorcycles, auto-rickshaws, buses, trucks
- Python + TraCI traffic state
- Fixed-time and actuated controllers
- PPO training/evaluation scaffold
- FastAPI + WebSocket backend
- React/Vite dashboard
- Scenario configuration
- CSV experiment output

This is a simulation prototype. It does not integrate real FASTag, LiDAR, Jetson hardware, physical signals, or real sensors.

## Run

Install Python 3.11+, Node 18+, and SUMO.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
```

Build the SUMO network first:

```bash
cd simulation/sumo/network
netconvert --node-files intersection.nod.xml --edge-files intersection.edg.xml --connection-files intersection.con.xml --tllogic-files intersection.tll.xml --output-file intersection.net.xml --proj false
cd ../../..
```

Run SUMO:

```bash
python simulation/run_simulation.py --controller fixed --scenario heterogeneous --gui
```

Backend:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Train PPO:

```bash
python simulation/training/train_ppo.py --timesteps 10000
```

Evaluate:

```bash
python simulation/training/evaluate.py
```

Do not report performance percentages until actual SUMO experiments have been executed.
