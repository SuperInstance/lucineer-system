# vessel-prototype — Slackwater Integration Plan

## Core Game Mechanic: "Soul and Shell"

Agents in Slackwater have two layers:
- **Soul** — the agent's personality, goals, memories, skills (the AgentSoul)
- **Shell** — the physical vessel they inhabit in the game world (the Vessel)

A soul without a shell is a ghost. A shell without a soul is a drone. The player's job is to match souls to shells optimally.

### Mechanic 1: Agent Spawning and Vessel Selection

**In-game:** When a new agent is born (spawned by the Conductor), it arrives as a disembodied soul. It needs a vessel — a physical form in the game world. The FleetScheduler finds the best available vessel based on the soul's requirements.

**Vessel types:**
- **Stationary terminals** — powerful but fixed (servers, mainframes)
- **Mobile units** — weaker but can move (drones, vehicles, NPCs)
- **Edge devices** — special-purpose, limited (sensors, cameras, speakers)
- **Player-adjacent** — companions that follow the player

**Player interaction:** The player influences which vessels are available by building, discovering, or unlocking them. Better vessels attract better souls.

### Mechanic 2: Capability Requirements

**In-game:** Each soul has `required_caps` — capabilities it absolutely needs to function. A soul requiring "vision" can't inhabit a blind vessel. A soul requiring "manipulation" needs arms. This creates a matching puzzle.

**Player interaction:** The player examines soul profiles to see their requirements, then matches them to vessels with the right capabilities. Mismatches are visible — a soul in an inadequate vessel performs poorly.

### Mechanic 3: Preferred Capabilities and Scoring

**In-game:** Beyond requirements, souls have `preferred_caps` — capabilities that make them happier and more effective. A soul that prefers "edge" capability gets a bonus when placed on an edge device.

**Player interaction:** Optimization game — matching souls to vessels where they'll thrive, not just survive. Each soul shows a "happiness meter" reflecting how well their preferences are met.

### Mechanic 4: Agent Migration

**In-game:** Agents can migrate between vessels. This costs resources and temporarily disrupts the agent (they're in "transit" — a ghost state). Migration is used when:
- A better vessel becomes available
- The current vessel is damaged
- A new task requires different capabilities
- The fleet needs rebalancing

**Player interaction:** The player triggers migrations, weighing the cost of transit against the benefit of better placement. During transit, the agent is vulnerable — their soul can be intercepted.

### Mechanic 5: Graceful Degradation

**In-game:** When a vessel loses capabilities (damaged in combat, power failure, environmental hazard), agents depending on those capabilities are affected:

- **Lost required cap** → agent must migrate or go dormant
- **Lost preferred cap** → agent stays but loses bonus
- **Vessel destroyed** → soul becomes a ghost, must find a new vessel within a time limit or dissipate

**Player interaction:** Damage to vessels creates urgent migration situations. The player must have backup vessels ready or risk losing agents permanently.

### Mechanic 6: Multi-Tenancy

**In-game:** Vessels have `max_agents` limits. A mainframe can host 5 agents; a drone can host 1. The player manages vessel capacity as a resource.

**Player interaction:** overcrowding reduces performance for all tenants. Underutilizing powerful vessels wastes capacity. The optimization puzzle is a core management mechanic.

## Cloud ↔ Edge Migration

The vessel-prototype directly informs how Lucineer moves computation between:
- **Cloud (Forgemaster-class)** — powerful, expensive, not always available
- **Edge (JetsonClaw-class)** — real-time, cheap, limited capability
- **Player device (Oracle-class)** — the player's local hardware

Agents that need heavy computation (planning, generation) migrate to cloud vessels. Agents that need real-time response stay on edge vessels. The FleetScheduler automates this routing.

## Implementation Priority: HIGH

Agent lifecycle management is foundational — every NPC in the game needs to be spawned, housed, and managed. Implement early, alongside Cocapn.

## Roblox/Lua Implementation Notes

- AgentSoul as a Lua table: { name, goals, required_caps, preferred_caps, state }
- Vessel as a Roblox Model with capability attributes
- FleetScheduler as a server-side module managing the soul/vessel registry
- Migration as a serialized state transfer (save soul state → load in new vessel)
- Capabilities as a set of tags/attributes on vessel models
- Visual: souls as glowing orbs when unshelled, vessels as physical objects
