# Bharat Traffic Digital Twin — Research MVP

## Research question
Can reinforcement learning reduce delay and queue formation under heterogeneous traffic at an urban intersection?

## Implemented
4-way intersection, heterogeneous vehicle mix, Fixed-Time, Actuated, PPO/Gymnasium environment, scenario engine, metrics, experiments, FastAPI, WebSocket dashboard, and optional SUMO/TraCI bridge.

## Metrics
Average queue, waiting time, speed, throughput, delay proxy, stops, signal switches.

## Scenarios
Normal, heavy, heterogeneous, bike-heavy, auto-heavy, blockage, monsoon, sensor failure, sensor spoofing.

## Research boundary
The default engine is a lightweight deterministic simulator so the MVP runs without a system-level SUMO installation. SUMO/TraCI files are included separately. Simulation results must be labelled simulation results and must not be presented as field measurements.
