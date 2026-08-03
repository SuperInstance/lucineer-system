# vessel-constellation — Deep Dive Analysis

## Overview
An N-body gravitational physics simulation of the SuperInstance fleet, modeling vessels as stars and repos as orbiting planets. Uses symplectic leapfrog integration for energy conservation, tracks conservation laws (total energy E, angular momentum L), detects Lagrange configurations, and simulates perturbation events (repo added/removed, dependency shifts, velocity kicks).

## Architecture

### Vessel Module (`vessel.rs`)
Vessel as gravitational body:
- `name`, `mass` (= repo count), `position` (dependency-space vector), `velocity` (growth rate)
- `distance_to()`: Euclidean distance in n-dimensional dependency-space
- `kinetic_energy()`: ½mv²
- `momentum()`: mv
- `angular_momentum()`: m(r × v) — cross product generalized to 3D
- `center_of_mass()`: weighted average between two vessels
- Serde serializable

### Orbit Module (`orbit.rs`)
Repository orbital mechanics:
- Kepler's 3rd law: ω = √(μ/r³), T = 2π√(r³/μ)
- Core repos (small r) orbit fast, peripheral repos (large r) orbit slow
- `Repo::new()`: auto-computes angular velocity from orbital radius and vessel mass (μ)
- `step(dt)`: advance angle, wrap to [0, 2π)
- `position()`: Cartesian (x,y) from polar coordinates
- `orbital_energy()`: -μ/(2r) for bound orbits
- `verify_kepler()`: self-checks T²μ = 4π²r³

### Gravity Module (`gravity.rs`)
N-body gravitational field:
- `force_between()`: F = Gm₁m₂/r² with direction vector
- `net_force()`: sum of forces from all sources
- `total_potential_energy()`: PE = -G·m₁m₂/r for all pairs
- `potential_at()`: gravitational potential at arbitrary point
- `accelerations()`: force/mass for each vessel
- `is_circular_orbit()`: checks if centripetal = gravitational force
- `is_lagrange_triangle()`: detects equilateral triangle configurations (10% tolerance)

### Conservation Module (`conservation.rs`)
Conservation law tracking:
- `ConservationState`: total_energy (KE+PE), angular_momentum vector, kinetic, potential
- `energy_conserved()`: relative tolerance check
- `angular_momentum_conserved()`: per-component tolerance check
- Tests verify both are conserved to <1% over 100 leapfrog steps

### Constellation Module (`constellation.rs`)
Full system state + evolution:
- **Leapfrog integration** (kick-drift-kick / velocity Verlet):
  1. Half-kick: v(t+dt/2) = v(t) + a(t)·dt/2
  2. Drift: r(t+dt) = r(t) + v(t+dt/2)·dt
  3. Recompute accelerations
  4. Half-kick: v(t+dt) = v(t+dt/2) + a(t+dt)·dt/2
- **Euler integration** (for comparison/testing)
- `evolve(N)`: run N steps, return (initial, final) conservation states
- Leapfrog conserves energy to <0.001% drift vs Euler's 5-15% drift
- `initial_fleet()`: creates the 4-vessel SuperInstance fleet

### Perturbation Module (`perturbation.rs`)
Event system for constellation changes:
- `RepoAdded`: increases vessel mass, adds orbiting repo
- `RepoRemoved`: decreases vessel mass, removes repo
- `DependencyShift`: moves vessel position in dependency-space
- `VelocityKick`: sudden growth spurt
- `apply()`: mutates vessels and repos
- `conservation_delta()`: computes change in E and L

### The Fleet
| Vessel | Mass (repos) | Role |
|---|---|---|
| Forgemaster | 330 | The titan — anchors the system |
| CCC | 116 | The pillar — stabilizes the middle |
| JetsonClaw1 | 76 | The operative — bridges the gap |
| Oracle | 43 | The sentinel — scouts the frontier |

## Key Patterns

1. **Mass = influence**: vessels with more repos exert more gravitational pull
2. **Dependency-space**: multi-dimensional coordinates representing coupling categories
3. **Symplectic integration**: leapfrog preserves Hamiltonian structure → exact conservation
4. **Keplerian orbits**: repos obey T² ∝ r³ — core repos are fast, peripheral are slow
5. **Perturbation events**: discrete changes with measurable conservation impact
6. **Lagrange detection**: stable equilateral configurations → fleet equilibrium points
7. **Velocity = growth rate**: vessels moving fast are growing fast in dependency-space

## Technology
- **Language**: Rust
- **Dependencies**: serde, serde_json (serialization only)
- **Testing**: comprehensive unit tests per module (8-12 tests each)
- **Integration**: leapfrog vs Euler comparison test, full pipeline test
