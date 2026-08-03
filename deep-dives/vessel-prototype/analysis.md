# vessel-prototype — Analysis

## What It Does

**vessel-prototype** implements the **Agent/Vessel Separation Architecture** — the distinction between an agent's soul (behavior, goals, memory) and its body (hardware, OS, runtime, sensors). This separation enables agent migration, multi-tenancy, graceful degradation, and fleet-wide scheduling.

### Core Abstractions

1. **AgentSoul** — the portable essence of an agent
   - name, goals, memory_path
   - required_caps (must-have capabilities)
   - preferred_caps (nice-to-have capabilities)
   - state (mutable internal state)
   - `can_run_on(vessel)` — feasibility check
   - `score_vessel(vessel)` — quality of fit

2. **Vessel** — the hardware/runtime hosting agents
   - name, host, OS, arch
   - caps (capability map with availability + priority)
   - active_agents list
   - max_agents limit
   - `can_host(soul)` — capacity + capability check
   - `host(soul)` / `release(soul_name)` — lifecycle

3. **FleetScheduler** — places souls on vessels
   - `find_best_vessel(soul)` — highest-scoring vessel
   - `migrate(soul_name, from_vessel, reason)` — relocate
   - `get_fleet_status()` — bird's-eye view

### Key Innovation: Soul/Body Separation

An agent's identity (soul) is **completely decoupled** from its runtime (vessel). The soul contains goals and memory; the vessel provides capabilities. An agent can migrate between vessels as long as the target meets its required capabilities.

### Key Innovation: Capability-Based Scoring

Each vessel has capabilities with priority scores. Souls score vessels by summing the priorities of their preferred capabilities. This creates a natural ranking system where agents gravitate toward the best-equipped vessels.

### Key Innovation: Graceful Degradation

When a vessel loses a capability (e.g., GPU fails), agents depending on that capability are evicted. The scheduler finds them a new home. This models real hardware failures in a fleet.

### Demo Scenario

The demo creates 3 vessels:
- **Oracle1** — ARM64 server, no GPU (5 agent capacity)
- **JetsonClaw1** — ARM64 edge device with CUDA GPU (3 capacity)
- **Forgemaster** — x64 Windows with RTX 4050 + LoRA (2 capacity)

And 3 souls with different capability requirements, then simulates JetsonClaw1's GPU failing and shows the agent being migrated.

## Code Quality

- **4 source files** (agent.py, __main__.py, pyproject.toml, README.md)
- ~200 lines of clean Python
- Zero dependencies — pure stdlib
- Excellent demo with visual output
- Well-documented dataclasses with proper typing
- Clean separation of concerns

## Relevance to Slackwater

This defines how **agents spawn, migrate, and degrade** in the game. The soul/vessel separation is the difference between an NPC's personality (soul) and their physical form in the game world (vessel). When a vessel is destroyed, the soul can be reincarnated in a new one.
