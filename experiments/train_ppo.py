import argparse
from pathlib import Path
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from simulation.environment.traffic_env import TrafficSignalEnv
ap=argparse.ArgumentParser(); ap.add_argument("--timesteps",type=int,default=20000); ap.add_argument("--output",default="models/ppo/traffic_signal_ppo"); a=ap.parse_args()
model=PPO("MlpPolicy",Monitor(TrafficSignalEnv()),verbose=1,seed=42); model.learn(total_timesteps=a.timesteps)
Path(a.output).parent.mkdir(parents=True,exist_ok=True); model.save(a.output); print("Saved",a.output+".zip")
