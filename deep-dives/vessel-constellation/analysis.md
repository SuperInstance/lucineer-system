# vessel-constellation — Analysis

## What It Does

**vessel-constellation** is an **N-body gravitational simulation** of a fleet of software vessels and their orbiting repositories. It models the fleet as a celestial mechanics problem:

- **Vessels** are stars — massive gravitational bodies (mass = repo count)
- **Repos** are planets — orbiting their vessel with Keplerian dynamics
- **Dependencies** are gravity — F = G·m₁·m₂/r²
- **Conservation laws** — total energy E and angular momentum L are preserved

### The Fleet

| Vessel | Repos | Role |
|--------|-------|------|
| Forgemaster | 330 | The titan — anchors the system |
| CCC | 116 | The pillar — stabilizes the middle |
| JetsonClaw1 | 76 | The operative — bridges the gap |
| Oracle | 43 | The sentinel — scouts the frontier |

### Modules

1. **vessel** — Vessel as gravitational body (mass, position, velocity, KE, momentum, angular momentum, center of mass)
2. **orbit** — Repo orbits: Kepler's 3rd law (T² ∝ r³), angular velocity, period, position, energy
3. **gravity** — N-body forces: pairwise F=ma, potential energy, potential field, circular orbit detection, Lagrange triangle detection
4. **conservation** — State tracking: total energy (KE+PE), angular momentum, with tolerance-based conservation checks
5. **perturbation** — Events: repo added/removed (mass change), dependency shift (position change), velocity kick (growth spurt)
6. **constellation** — Full state + symplectic leapfrog integration

### Key Innovation: Symplectic Leapfrog Integration

The system uses **kick-drift-kick** (velocity Verlet) integration:
1. Half-kick: v(t+dt/2) = v(t) + a(t)·dt/2
2. Drift: r(t+dt) = r(t) + v(t+dt/2)·dt
3. Recompute accelerations
4. Half-kick: v(t+dt) = v(t+dt/2) + a(t+dt)·dt/2

This preserves the Hamiltonian structure — energy drift is <0.001% over 1000 steps, compared to 5-15% for Euler integration. This is critical because the simulation must remain stable over long game sessions.

### Key Innovation: Lagrange Point Detection

The system can detect when three vessels form a **stable equilateral configuration** (Lagrange L4/L5). This is when the fleet is in its most harmonious arrangement — no vessel is pulling too hard on any other.

### Key Innovation: Perturbation as First-Class Event

Adding/removing a repo isn't just a data change — it's a **physical event** that propagates through the N-body system. The mass change alters the gravitational field, shifting every other vessel's orbit. The system tracks the conservation delta (ΔE, ΔL) of each perturbation.

### Key Innovation: Repos Follow Kepler's Third Law

Core repos (small orbital radius) orbit fast — they're close to the vessel's center of mass. Peripheral repos (large radius) orbit slowly. This means **important things happen quickly, peripheral things happen slowly** — a natural priority system derived from physics.

## Code Quality

- **14 source files**, ~1,200 lines of Rust
- Excellent modular architecture (6 modules, each independently testable)
- 40+ tests across all modules
- Conservation verification tests (the physics actually works)
- Serde support for save/load
- Beautiful ASCII art documentation in README
- Proper mathematical notation and formulas throughout

## Relevance to Slackwater

This is the **spatial dynamics engine** for game agents. Instead of repos orbiting vessels, game agents orbit faction headquarters. The gravitational metaphor becomes the relationship system — powerful factions attract more agents, dependencies between factions create gravitational pull.
