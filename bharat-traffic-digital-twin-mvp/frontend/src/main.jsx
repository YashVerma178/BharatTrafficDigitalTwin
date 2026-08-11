import React,{useEffect,useState} from "react";
import {createRoot} from "react-dom/client";
import "./styles.css";

const API="http://localhost:8000";

function App(){
  const [s,setS]=useState(null),[controller,setController]=useState("fixed"),[scenario,setScenario]=useState("heterogeneous"),[running,setRunning]=useState(false);
  useEffect(()=>{const ws=new WebSocket("ws://localhost:8000/ws/traffic");ws.onmessage=e=>setS(JSON.parse(e.data));return()=>ws.close()},[]);
  const state=s||{current_phase:"NORTH_SOUTH",phase_remaining:30,queues:{north:0,south:0,east:0,west:0},waiting_times:{north:0,south:0,east:0,west:0},speeds:{north:0,south:0,east:0,west:0},vehicle_counts:{car:0,motorcycle:0,auto:0,bus:0,truck:0},throughput:0,controller,scenario,sensor_status:"OK",anomaly:false};
  const avg=(o)=>Object.values(o).reduce((a,b)=>a+b,0)/Object.values(o).length;
  async function start(){await fetch(API+"/api/simulation/start",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({controller,scenario})});setRunning(true)}
  async function stop(){await fetch(API+"/api/simulation/stop",{method:"POST"});setRunning(false)}
  async function ctrl(v){setController(v);await fetch(API+"/api/controller",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({controller:v})})}
  async function scen(v){setScenario(v);await fetch(API+"/api/scenario",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({scenario:v})})}
  return <div className="app">
    <header><div><small>DIGITAL TWIN • RESEARCH MVP</small><h1>Bharat Traffic Digital Twin</h1><p>Adaptive signal control for heterogeneous urban traffic</p></div><div className="status">● {running?"SIMULATION LIVE":"IDLE"}</div></header>
    <div className="controls"><label>Controller<select value={controller} onChange={e=>ctrl(e.target.value)}><option value="fixed">Fixed-Time</option><option value="actuated">Actuated</option><option value="ppo">PPO</option></select></label><label>Scenario<select value={scenario} onChange={e=>scen(e.target.value)}><option>normal</option><option>heavy</option><option>heterogeneous</option><option>bike_heavy</option><option>auto_heavy</option><option>blockage</option><option>monsoon</option><option>sensor_failure</option><option>sensor_spoofing</option></select></label>{running?<button onClick={stop}>Stop</button>:<button onClick={start}>Start Simulation</button>}</div>
    <div className="metrics"><Metric t="Avg Queue" v={avg(state.queues).toFixed(1)} u="veh"/><Metric t="Avg Waiting" v={avg(state.waiting_times).toFixed(1)} u="sec"/><Metric t="Avg Speed" v={avg(state.speeds).toFixed(1)} u="m/s"/><Metric t="Throughput" v={state.throughput} u="veh/hr"/></div>
    <div className="grid">
      <section className="panel twin"><div className="title">LIVE DIGITAL TWIN</div><div className="intersection"><div className="road v top"></div><div className="road v bottom"></div><div className="road h left"></div><div className="road h right"></div><div className="junction"><div className={"light "+(state.current_phase==="NORTH_SOUTH"?"green":"red")}></div><b>{state.phase_remaining}s</b><span>{state.current_phase.replace("_"," / ")}</span></div><div className="tag n">NORTH<br/>{state.queues.north} queue</div><div className="tag s">SOUTH<br/>{state.queues.south} queue</div><div className="tag e">EAST<br/>{state.queues.east} queue</div><div className="tag w">WEST<br/>{state.queues.west} queue</div><div className="veh vn">🚗 🛵 🛺</div><div className="veh ve">🛵 🚗</div></div></section>
      <section className="panel"><div className="title">SYSTEM STATUS</div><Row a="Controller" b={state.controller.toUpperCase()}/><Row a="Scenario" b={state.scenario.replaceAll("_"," ").toUpperCase()}/><Row a="Signal" b={state.current_phase.replace("_"," / ")}/><Row a="Sensor Integrity" b={state.sensor_status}/><Row a="Anomaly" b={state.anomaly?"DETECTED":"NONE"}/></section>
      <section className="panel"><div className="title">VEHICLE COMPOSITION</div>{Object.entries(state.vehicle_counts).map(([k,v])=><Row key={k} a={k} b={v}/>)}</section>
      <section className="panel"><div className="title">RESEARCH MODE</div><p className="note">Simulation values are for the MVP. Run actual SUMO experiments before reporting research performance.</p></section>
    </div>
  </div>
}
const Metric=({t,v,u})=><div className="metric"><small>{t}</small><strong>{v}</strong><span>{u}</span></div>;
const Row=({a,b})=><div className="row"><span>{a}</span><b>{b}</b></div>;
createRoot(document.getElementById("root")).render(<App/>);
