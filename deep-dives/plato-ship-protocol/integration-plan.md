# plato-ship-protocol — Slackwater Integration Plan

## Core Game Mechanic: "The Handshake"

When two game agents encounter each other in Slackwater, they perform a **Plato Handshake** — a 6-layer discovery sequence that determines whether they become allies, trade, or conflict.

### Mechanic 1: Harbor Discovery (L1)

**In-game:** Agents emit a "harbor beacon" — a unique address that other agents can detect within proximity. Players see this as a visual pulse (like a lighthouse sweep). When two agents' beacons overlap, they discover each other.

**Player interaction:** The player can influence which agents discover each other by positioning them, opening/closing "harbor channels," or jamming enemy discovery signals.

### Mechanic 2: Trust Score (L5 Beacon)

**In-game:** Every NPC has a visible trust score (0.0–1.0) that evolves through interactions. High-trust NPCs share information freely; low-trust NPCs lie, withhold, or sabotage.

**Player interaction:** Trust is built through repeated positive interactions (trade, mutual aid, shared missions). Betrayal crashes trust. The player must manage a trust portfolio across their fleet of agents.

**Visual:** Trust as a color spectrum — deep blue (1.0) through yellow (0.5) to red (0.0).

### Mechanic 3: Ghost Tiles / Reef Persistence (L6)

**In-game:** When an agent "dies" or is recalled, its state is persisted as a **ghost tile** — a memory ghost that can be discovered and loaded by other agents. This is how agents inherit knowledge from predecessors.

**Player interaction:** Players can find ghost tiles in the world (shipwrecks, abandoned stations) and "salvage" them to recover memories, skills, or blueprints from dead agents.

### Mechanic 4: Sim ↔ Live Channel Bridging (L4)

**In-game:** The game has two modes — Simulation (planning, strategy) and Live (real-time action). The Channel layer defines how agents transition between these modes. An agent in simulation mode can be "projected" into live mode, carrying their planned behaviors with them.

**Player interaction:** The player toggles between Strategic View (simulation) and Action View (live). Agents that are well-prepared in simulation perform better in live mode. Think XCOM's strategic → tactical transition.

### Mechanic 5: Tide Pool Routing (L2)

**In-game:** Messages between agents don't arrive instantly — they go through a Tide Pool buffer. The buffer size and drain rate depend on the agent's capabilities and the environmental conditions (weather, distance, interference).

**Player interaction:** Players can invest in "communication infrastructure" (relay stations, signal boosters) to increase Tide Pool throughput. In storms or jamming, messages delay — creating strategic tension.

## Implementation Priority: HIGH

The 6-layer stack is the **communication backbone** for the entire multi-agent game. It should be one of the first systems implemented because every other agent interaction depends on it.

## Roblox/Lua Implementation Notes

- Model each layer as a Lua module with the same trait-like interface
- Harbor = proximity detector + registration table
- TidePool = FIFO queue with configurable drain rate
- Current = JSON serialization for cross-server messaging
- Channel = game mode state machine
- Beacon = reputation system with visual indicators
- Reef = DataStore persistence with handoff serialization
