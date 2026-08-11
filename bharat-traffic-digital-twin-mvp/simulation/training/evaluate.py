import argparse
from pathlib import Path
import numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--episodes", type=int, default=5)
    a = p.parse_args()
    from stable_baselines3 import PPO
    from simulation.environment.traffic_env import TrafficSignalEnv
    model_file = Path("models/ppo/ppo_traffic_signal.zip")
    if not model_file.exists():
        raise SystemExit("Train PPO first: python simulation/training/train_ppo.py")
    model = PPO.load("models/ppo/ppo_traffic_signal")
    scores = []
    for _ in range(a.episodes):
        env = TrafficSignalEnv()
        obs, _ = env.reset()
        score = 0.0
        for _ in range(env.max_steps):
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, _, _ = env.step(action)
            score += reward
            if done:
                break
        scores.append(score)
    print("Mean PPO evaluation reward:", float(np.mean(scores)))

if __name__ == "__main__":
    main()
