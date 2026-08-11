# macOS Quick Start

The default MVP does not require SUMO for the first demonstration.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python3 -m uvicorn backend.app.main:app --reload --port 8000
```

Open http://127.0.0.1:8000

Click Start Simulation.

Train PPO:

```bash
python3 experiments/train_ppo.py --timesteps 20000
```

Run controller experiments:

```bash
python3 experiments/run_experiments.py --episodes 3 --steps 600
```

The optional SUMO/TraCI bridge is under `simulation/sumo/`.
