# 🇮🇳 Bharat Traffic AI — Digital Twin

> An AI-assisted traffic-signal research platform for simulating heterogeneous urban traffic and evaluating intelligent traffic-control strategies.

---

## 📌 Overview

**Bharat Traffic AI** is a simulation-based Digital Twin prototype designed to study intelligent traffic-signal control under heterogeneous traffic conditions.

The system represents a four-way urban intersection and allows different traffic-control strategies to be evaluated under multiple traffic scenarios.

The primary research objective is:

> **To investigate whether adaptive reinforcement-learning-based traffic signal control can reduce congestion and improve traffic flow compared with conventional signal-control strategies.**

The platform provides a visual dashboard where traffic conditions, signal states, vehicle composition and performance metrics can be monitored during simulation.

---

# 🎯 Research Objective

Traditional traffic signals commonly use predefined timing plans.

However, real urban traffic can change continuously because of:

- Different traffic volumes
- Different vehicle types
- Uneven traffic demand
- Road blockages
- Weather conditions
- Sensor uncertainty
- Changing traffic patterns

The project investigates whether an adaptive controller can respond to these changing conditions more effectively.

The main comparison is:

```text
Fixed-Time
     │
     ▼
Actuated
     │
     ▼
PPO / Reinforcement Learning
