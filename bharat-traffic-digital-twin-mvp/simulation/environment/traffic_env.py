import numpy as np
import gymnasium as gym
from gymnasium import spaces

class TrafficSignalEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, scenario="heterogeneous", max_steps=300):
        super().__init__()
        self.scenario = scenario
        self.max_steps = max_steps
        self.step_count = 0
        self.observation_space = spaces.Box(0.0, 1.0, shape=(22,), dtype=np.float32)
        self.action_space = spaces.Discrete(4)

    def _state(self):
        t = self.step_count / max(self.max_steps, 1)
        q = float(np.clip(0.2 + 0.55 * (0.5 + 0.5*np.sin(t*12)), 0, 1))
        return np.asarray(
            [q, q*.8, q*.9, q*.7] + [q]*8 + [0.5]*8 + [0.0, min(t, 1.0)],
            dtype=np.float32
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.step_count = 0
        return self._state(), {}

    def step(self, action):
        self.step_count += 1
        obs = self._state()
        queue = float(obs[:4].sum())
        delay = queue
        switch_penalty = 0.05 if int(action) == 3 else 0.0
        reward = float(-delay - 0.25*queue - switch_penalty)
        terminated = self.step_count >= self.max_steps
        return obs, reward, terminated, False, {
            "queue": queue, "delay_proxy": delay,
            "switching_penalty": switch_penalty
        }
