import argparse
from pathlib import Path
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from simulation.environment.traffic_env import TrafficSignalEnv

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--timesteps", type=int, default=10000)
    p.add_argument("--output", default="models/ppo/ppo_traffic_signal")
    a = p.parse_args()
    env = Monitor(TrafficSignalEnv())
    model = PPO("MlpPolicy", env, verbose=1, seed=42)
    model.learn(total_timesteps=a.timesteps)
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    model.save(a.output)
    print(f"Saved {a.output}.zip")

if __name__ == "__main__":
    main()
