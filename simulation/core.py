import math, random
from dataclasses import dataclass, field

DIRECTIONS=("north","south","east","west")
VEHICLES=("car","motorcycle","auto","bus","truck")
SCENARIOS={
"normal":(.70,1.0,{"car":.65,"motorcycle":.15,"auto":.10,"bus":.05,"truck":.05}),
"heavy":(1.35,1.0,{"car":.65,"motorcycle":.15,"auto":.10,"bus":.05,"truck":.05}),
"heterogeneous":(1.0,1.0,{"car":.55,"motorcycle":.25,"auto":.10,"bus":.05,"truck":.05}),
"bike_heavy":(1.0,1.0,{"car":.35,"motorcycle":.45,"auto":.10,"bus":.05,"truck":.05}),
"auto_heavy":(1.0,1.0,{"car":.40,"motorcycle":.20,"auto":.30,"bus":.05,"truck":.05}),
"blockage":(1.0,.55,{"car":.55,"motorcycle":.25,"auto":.10,"bus":.05,"truck":.05}),
"monsoon":(1.0,.70,{"car":.55,"motorcycle":.25,"auto":.10,"bus":.05,"truck":.05}),
"sensor_failure":(1.0,1.0,{"car":.55,"motorcycle":.25,"auto":.10,"bus":.05,"truck":.05}),
"sensor_spoofing":(1.0,1.0,{"car":.55,"motorcycle":.25,"auto":.10,"bus":.05,"truck":.05})
}
@dataclass
class State:
    time:int=0; phase:int=0; elapsed:int=0; remaining:int=30
    queues:dict=field(default_factory=lambda:{d:0.0 for d in DIRECTIONS})
    waiting:dict=field(default_factory=lambda:{d:0.0 for d in DIRECTIONS})
    speed:dict=field(default_factory=lambda:{d:13.0 for d in DIRECTIONS})
    counts:dict=field(default_factory=lambda:{v:0 for v in VEHICLES})
    throughput:int=0; stops:int=0; switches:int=0

class IntersectionSim:
    def __init__(self,scenario="heterogeneous",seed=42):
        if scenario not in SCENARIOS: raise ValueError("unknown scenario "+scenario)
        self.scenario=scenario; self.rng=random.Random(seed); self.reset()
    def reset(self):
        self.s=State(); return self.snapshot()
    def observation(self):
        x=[min(self.s.queues[d]/80,1) for d in DIRECTIONS]
        x += [min(self.s.waiting[d]/120,1) for d in DIRECTIONS]
        x += [min(self.s.speed[d]/15,1) for d in DIRECTIONS]
        x += [min(self.s.counts[v]/100,1) for v in VEHICLES]
        x += [float(self.s.phase==0),float(self.s.phase==1)]
        x += [min(self.s.elapsed/60,1),min(self.s.remaining/60,1)]
        return x
    def step(self,extension=0,switch=False):
        demand,capacity,mix=SCENARIOS[self.scenario]
        if switch and self.s.elapsed>=12: self.s.remaining=0
        wave=.85+.25*(.5+.5*math.sin(self.s.time/55))
        for d in DIRECTIONS:
            bias=1.15 if d in ("north","south") else .95
            self.s.queues[d]+=.38*demand*wave*bias*self.rng.uniform(.9,1.1)
        green=("north","south") if self.s.phase==0 else ("east","west")
        service=.95*capacity*(.95+.08*mix["motorcycle"]-.12*mix["bus"]-.10*mix["truck"])
        service*=1+min(max(extension,0),8)*.08
        departed=0
        for d in DIRECTIONS:
            out=min(self.s.queues[d],service) if d in green else 0
            self.s.queues[d]=max(0,self.s.queues[d]-out); departed+=int(out)
            self.s.waiting[d]+=self.s.queues[d]
            self.s.speed[d]=max(2,13.5-.13*self.s.queues[d])
            if self.s.queues[d]>2 and d not in green: self.s.stops+=1
        self.s.throughput+=departed; self.s.time+=1; self.s.elapsed+=1; self.s.remaining=max(0,self.s.remaining-1)
        if self.s.remaining==0:
            self.s.phase=1-self.s.phase; self.s.elapsed=0; self.s.remaining=30; self.s.switches+=1
        total=sum(self.s.queues.values()); self.s.counts={v:int(total*p) for v,p in mix.items()}
        return self.snapshot()
    def snapshot(self):
        aq=sum(self.s.queues.values())/4; aw=sum(self.s.waiting.values())/4; av=sum(self.s.speed.values())/4
        return {"time":self.s.time,"phase":"NORTH_SOUTH" if self.s.phase==0 else "EAST_WEST",
        "phase_index":self.s.phase,"phase_elapsed":self.s.elapsed,"phase_remaining":self.s.remaining,
        "queues":{k:round(v,2) for k,v in self.s.queues.items()},
        "waiting_times":{k:round(v,2) for k,v in self.s.waiting.items()},
        "speeds":{k:round(v,2) for k,v in self.s.speed.items()},
        "vehicle_counts":self.s.counts.copy(),"throughput":self.s.throughput,"stops":self.s.stops,
        "signal_switches":self.s.switches,"average_queue":round(aq,2),
        "average_waiting_time":round(aw,2),"average_speed":round(av,2),"delay_proxy":round(aw+sum(self.s.queues.values()),2)}
