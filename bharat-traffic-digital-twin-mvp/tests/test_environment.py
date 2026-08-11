from simulation.environment.traffic_env import TrafficSignalEnv

def test_shape():
    env = TrafficSignalEnv()
    obs, _ = env.reset(seed=42)
    assert obs.shape == (22,)
    assert env.action_space.n == 4

def test_step():
    env = TrafficSignalEnv()
    obs, _ = env.reset(seed=42)
    obs, reward, done, truncated, info = env.step(1)
    assert obs.shape == (22,)
    assert isinstance(reward, float)
    assert "queue" in info
