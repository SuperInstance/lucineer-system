# vessel-constellation — Slackwater Integration Plan

## Core Game Mechanic: "The Constellation"

The N-body simulation becomes the game's **faction and relationship system**. Factions are stars; agents are planets; the gravitational field is the political/cultural force between factions.

### Mechanic 1: Faction Gravity

**In-game:** Factions have mass proportional to their membership count. Powerful factions attract new members easily (gravitational pull). Small factions must work harder to retain members.

**Player interaction:**
- Joining a faction changes your "orbital position" relative to it
- Being in a high-mass faction provides stability but limits freedom
- Being in a low-mass faction is risky but offers more influence (your mass matters more)

**Visual:** A star-map view of the faction constellation. Faction sizes pulse with membership changes. Gravitational field lines show the political landscape.

### Mechanic 2: Orbital Mechanics for Agent Relationships

**In-game:** Agents orbit their faction headquarters following Kepler's third law:
- **Core agents** (small radius) — fast orbit, high influence, tightly bound
- **Standard agents** (medium radius) — moderate orbit, moderate influence
- **Peripheral agents** (large radius) — slow orbit, low influence, easily lost

**Player interaction:** The player can move closer to or farther from a faction's center. Moving closer increases influence but requires more commitment (faster orbit = more activity). Moving outward gives freedom but reduces impact.

**T² ∝ r³ means:** Doubling your distance from center means your "orbital period" (time to complete a full cycle of duties) increases by 2.83×. Core agents cycle through tasks quickly; peripheral agents are slow but steady.

### Mechanic 3: Conservation Laws as Game Balance

**In-game:** The total energy and angular momentum of the system are conserved. This means:
- **You can't create or destroy political power** — only move it around
- **Joining a faction changes the equilibrium** — other agents shift in response
- **Removing a faction member creates a perturbation** — the system must rebalance

**Player interaction:** Major faction changes (joining, leaving, betrayal) trigger visible perturbation waves across the constellation. The player sees the system rebalance in real-time.

### Mechanic 4: Perturbation Events

**In-game:** Four types of perturbation events, each with gameplay consequences:

- **Member Joined** (RepoAdded) — faction mass increases, gravitational pull strengthens
- **Member Left** (RepoRemoved) — faction weakens, nearby agents may drift away
- **Ideology Shift** (DependencyShift) — faction moves in "idea-space," changing relationships
- **Growth Spurt** (VelocityKick) — sudden faction expansion, disrupting neighbors

**Player interaction:** Each perturbation creates ripples. The player can trigger perturbations (recruiting, persuading, sabotaging) and must manage the consequences.

### Mechanic 5: Lagrange Points as Safe Zones

**In-game:** When three factions form a stable equilateral triangle (Lagrange configuration), the spaces between them are **safe zones** — gravitationally neutral regions where agents can exist without being pulled toward any faction.

**Player interaction:**
- Safe zones are valuable real estate — neutral ground for diplomacy, trade, hiding
- Players can try to engineer Lagrange configurations by balancing faction powers
- When a Lagrange point collapses (faction mass changes), everyone in the safe zone is launched into the nearest faction's gravity well

### Mechanic 6: Leapfrog Time Progression

**In-game:** The game world advances in discrete time steps using leapfrog integration. Each step:
- Agents move along their orbits
- Gravitational forces update
- Conservation laws are verified

**Player interaction:** The player can fast-forward time (watching orbits evolve) or slow it down (for precise positioning). Time control is a strategic resource.

### Mechanic 7: Multi-Agent Spatial Dynamics

For Lucineer's multi-agent future, the constellation system models **agent-to-agent spatial relationships**:

- Agents have mass (importance/connectedness)
- Agents gravitate toward each other based on shared dependencies
- Agent clusters form natural "constellations" — teams that work well together
- Breaking up a constellation (removing a key agent) perturbs the whole system

## Implementation Priority: MEDIUM

The constellation system is the strategic layer — it's what makes the game world feel alive and interconnected. It becomes important once the basic agent and faction systems are working.

## Roblox/Lua Implementation Notes

- 2D simulation is sufficient (the game is 3D but relationships are 2D/abstract)
- Vessel = faction object with mass attribute
- Repo = agent with orbital parameters
- Leapfrog: update positions and velocities in alternating half-steps
- Conservation check: track total E and L, display as "world health" meter
- Lagrange detection: check if three factions form an equilateral triangle
- Perturbation events as game events with ripple animations
- Visual: a star map overlay accessible from the pause menu
