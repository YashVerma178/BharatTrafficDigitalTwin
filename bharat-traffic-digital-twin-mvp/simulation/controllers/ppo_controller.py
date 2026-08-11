from pathlib import Path

class PPOController:
    def __init__(self, model_path="models/ppo/ppo_traffic_signal"):
        self.model_path = Path(model_path)
        self.model = None

    def load(self):
        from stable_baselines3 import PPO
        if not Path(str(self.model_path) + ".zip").exists():
            raise FileNotFoundError(
                f"PPO model not found at {self.model_path}.zip. Train it first."
            )
        self.model = PPO.load(str(self.model_path))

    def predict(self, observation):
        if self.model is None:
            self.load()
        action, _ = self.model.predict(observation, deterministic=True)
        return int(action)
