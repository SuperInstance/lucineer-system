# fleet-yaw — Analysis

## What It Does

**fleet-yaw** is an **autopilot system that learns fleet physics from a first-person perspective**. Each agent carries its own model of the fleet, built from bearing-rate observations — no omniscient view, no transfer functions, no external models. Just observation and response.

In navigation, **yaw** is rotation around the vertical axis — heading relative to environment. This crate applies that to fleet agents: each agent senses the bearing (relative heading) to other agents and adjusts its own heading based on bearing rate.

### Core Concept: Bearing Rate

- **Bearing rate ≈ 0** → collision course (you're on an intercept trajectory)
- **Bearing rate > 0** → passing safely
- **Bearing rate < 0** → converging (may need attention)

### Key Types

| Type | Description |
|------|-------------|
| `KeelDate` | Agent's birthday (not version — birthday) |
| `Heading` | Current work direction + intensity |
| `Bearing` | Relative angle between two agents' headings, with rate of change |
| `Refit` | Documented change to the agent (component, reason, pruned components) |
| `BuildRecord` | First-person history (keel date + refits + pruned) |
| `ExperienceEntry` | Learned relationship (context → action → outcome + bearing before/after) |
| `FieldReading` | Environmental sensing (nearby agents, gradient, density, stress) |
| `HeadingChange` | Recommendation (new direction, reason, urgency, collision flag) |
| `Yaw` | The autopilot itself — holds all state |

### Behavior Rules

1. **Collision detection** — bearing rate below threshold + scope overlap = collision course
2. **Field stress** — >5 agents in similar heading space = stressed field → spread out
3. **Commissioning** — first 50 observations are exploratory (no heading changes)
4. **Refit never resets** — keel date is permanent, refits accumulate
5. **Pruning is learning** — removed components have reasons, forming "negative space" knowledge
6. **Same question detection** — agents with related headings share a question even if tasks differ

### Key Innovation: First-Person Fleet Physics

Each agent sees the fleet **from its own perspective** — bearings, not absolute positions. This makes the system:
- **Robust** — no single point of failure (no omniscient view needed)
- **Scalable** — each agent's model is local
- **Realistic** — mirrors how real agents (humans, ships, animals) perceive their environment

### Key Innovation: Commissioning Phase

Agents don't act on their environment until they've observed enough (50 observations). This prevents premature decisions based on insufficient data — a built-in "learning before doing" phase.

### Key Innovation: Keel Date as Identity

An agent's identity is its **birthday**, not a version number. Refits accumulate on top of the keel date but never replace it. This means every agent has a continuous history from birth — identity is temporal, not categorical.

### Key Innovation: Negative Space Learning

When components are pruned, the reason for removal is recorded. Future agents can consult this "negative space" — learning what NOT to do. This is learning from failure, explicitly preserved.

## Code Quality

- **1 source file** (lib.rs), ~600 lines of Rust
- Zero dependencies
- 28+ tests covering all 6 behavior rules
- Excellent documentation with clear behavioral semantics
- Clean struct/impl design with proper encapsulation
- The README ties it to the broader fleet philosophy (KEEL.md)

## Relevance to Slackwater

This is how **agents learn physical constraints** — the system that lets NPCs understand their environment through observation. In Slackwater, this becomes the NPC behavior learning system: agents that learn the game's "physics" (social physics, economic physics, spatial physics) from first-person observation.
