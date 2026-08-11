# Research Notes

## Research question
Can a reinforcement-learning traffic signal controller reduce delay and queue formation under heterogeneous traffic conditions representative of an Indian urban intersection?

## Core comparison
Fixed-Time vs Actuated vs PPO.

## Traffic
Cars, motorcycles, auto-rickshaws, buses and trucks.

## State
Queue length, waiting time, flow, speed, vehicle composition, current phase and phase elapsed time.

## Action
Bounded green-time change or phase switch.

## Reward
Negative weighted combination of delay, queue, waiting time and excessive switching.

## Scenarios
Normal, heavy traffic, heterogeneous traffic, bike-heavy, auto-heavy, blockage, monsoon capacity degradation, sensor failure and simulated sensor spoofing.

## Metrics
Average delay, waiting time, queue length, throughput, average speed, stops and signal switches.

## Limitations
Initial results are simulation-based. Parameters are assumptions unless calibrated with real traffic data. No real FASTag, LiDAR, roadside sensor, Jetson or physical traffic-light integration is included.

## Future work
Video/YOLO perception, LiDAR, real FASTag/IoT feeds, multi-intersection coordination, emergency priority, edge deployment and physical controller integration.
