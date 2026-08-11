import numpy as np
import gymnasium as gym
from gymnasium import spaces
from simulation.core import IntersectionSim
class TrafficSignalEnv(gym.Env):
    def __init__(self,scenario="heterogeneous",max_steps=600,seed=42):
        super().__init__(); self.scenario=scenario; self.max_steps=max_steps; self.seed_value=seed
        self.observation_space=spaces.Box(0,1,shape=(22,),dtype=np.float32); self.action_space=spaces.Discrete(4)
        self.sim=IntersectionSim(scenario,seed)
    def reset(self,seed=None,options=None):
        self.sim=IntersectionSim(self.scenario,self.seed_value if seed is None else seed)
        return np.asarray(self.sim.observation(),dtype=np.float32),{}
    def step(self,action):
        a=int(action); ext={0:0,1:3,2:6,3:0}[a]; switch=(a==3 and self.sim.s.elapsed>=12)
        st=self.sim.step(ext,switch)
        reward=-(.60*st["average_queue"]+.25*st["average_waiting_time"]+.25*float(switch))
        return np.asarray(self.sim.observation(),dtype=np.float32),float(reward),self.sim.s.time>=self.max_steps,False,st
