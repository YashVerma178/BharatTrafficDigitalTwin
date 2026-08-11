class FixedTimeController:
    name="fixed"
    def act(self,state): return (0,False)

class ActuatedController:
    name="actuated"
    def __init__(self,min_green=12,max_green=55): self.min_green=min_green; self.max_green=max_green
    def act(self,state):
        if state["phase_elapsed"]<self.min_green:return (0,False)
        if state["phase_elapsed"]>=self.max_green:return (0,True)
        ns=state["queues"]["north"]+state["queues"]["south"]; ew=state["queues"]["east"]+state["queues"]["west"]
        cur=ns if state["phase_index"]==0 else ew; other=ew if state["phase_index"]==0 else ns
        return (5 if cur>other*1.15 else 0,False)

class PPOController:
    name="ppo"
    def __init__(self,path="models/ppo/traffic_signal_ppo"): self.path=path; self.model=None
    def act(self,obs):
        if self.model is None:
            from stable_baselines3 import PPO
            self.model=PPO.load(self.path)
        a,_=self.model.predict(obs,deterministic=True); a=int(a)
        return ({0:0,1:3,2:6,3:0}[a], a==3)
