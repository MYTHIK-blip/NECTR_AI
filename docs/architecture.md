# 📐 NECTR_AI Architecture Overview

This document outlines the modular, collapse-resilient structure of NECTR_AI.

## 🎛️ Modules

- `agent_core.py` – Main control loop
- `memory.py` – SQLite agent memory
- `telemetry.py` – File-based telemetry logs
- `utils.py` – YAML + utilities
- `deception_layer.py` – [Pending] Honeypot/decoy API
- `swarm_router.py` – [Pending] PvX decision routing

## 🧠 Flow Summary

1. Load config from YAML
2. Initialize memory + logging
3. Enter loop:
    - Observe → Reason → Act
    - Store to memory
    - Log to telemetry
4. Route actions based on swarm/persona config

## 📡 Interaction Modes

- PvP – agent-agent
- PvE – agent-world
- NP – game logic

## 🛡️ Agent Safeguards

- Configurable kill-switch via loop constraints
- Input/output logging
- Config validation
- Persona segmentation
