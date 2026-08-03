# vessel-constellation → Lucineer Agent Dynamics Integration Plan

## Agent Attraction/Repulsion Dynamics

### Concept: NPC Social Physics
The constellation physics simulates how NPCs attract and repel each other based on their "mass" (importance/influence) and "position" in a multi-dimensional trait space. This creates emergent social structures without scripting every relationship.

### Integration Architecture

```
NPC Agents as Gravitational Bodies
  ├── Mass = influence (completed tasks, connections, wealth)
  ├── Position = trait vector (skills, personality dimensions)
  ├── Velocity = growth direction (what they're developing toward)
  └── Repos = orbiting creations (buildings, items, relationships)

Gravitational Field
  → High-mass NPCs attract others (form guilds, cities)
  → Low-mass NPCs orbit high-mass ones (apprenticeship, employment)
  → Similar-position NPCs repel (competition for same niche)
  → Different-position NPCs attract (complementary skills)

Conservation Laws
  → Total "social energy" of a zone stays balanced
  → Adding/removing NPCs perturbs the system measurably
  → System self-corrects toward equilibrium
```

### Phase 1: NPC Trait Space
Map dependency-space to NPC trait dimensions:

| Dimension | Range | Meaning |
|---|---|---|
| Combat | 0-10 | Fighting ability, aggression |
| Crafting | 0-10 | Building, creation skill |
| Social | 0-10 | Charisma, trade ability |
| Knowledge | 0-10 | Information, research |
| Exploration | 0-10 | Travel, discovery |

Each NPC has a position vector in this 5D trait space. Distance between NPCs = how similar they are.

### Phase 2: Gravitational NPC Dynamics
```lua
NPCVessel = {
  name = "blacksmith",
  mass = 15,  -- based on total completed tasks, wealth, connections
  position = { combat=3, crafting=9, social=4, knowledge=6, exploration=2 },
  velocity = { 0.1, 0.0, -0.05, 0.2, 0.0 },  -- growing crafting + knowledge
}

-- Gravitational attraction between blacksmith and merchant
-- F = G * mass_blacksmith * mass_merchant / distance²
-- distance = euclidean(trait_blacksmith, trait_merchant)
```

**Attraction rules:**
- High-mass NPC + nearby-position NPC → strong attraction (mentorship)
- High-mass NPC + distant-position NPC → weak attraction (trade route)
- Low-mass NPC + high-mass NPC → orbital relationship (apprentice orbits master)
- Two high-mass NPCs at same position → competition → instability → one gets pushed away

### Phase 3: Orbiting Creations
Map repos to NPC creations/buildings:

```lua
NPCCreation = {
  name = "blacksmith-forge",
  vessel = "blacksmith",
  orbital_radius = 1.0,  -- close = core creation, far = peripheral
  angle = 1.2,           -- current orbital position
  angular_velocity = kepler_omega(1.0, vessel_mass),
}

-- Core creations (small radius): the forge itself, primary tools
-- Standard creations (medium r): trade goods, commissioned works  
-- Peripheral creations (large r): gifts, decorations, experimental items
```

Core creations orbit fast (always relevant), peripheral creations orbit slowly (occasionally relevant). This creates a natural attention model — NPCs focus on core creations most of the time.

### Phase 4: Zone Equilibrium via Conservation Laws
Each zone/region of the game world has conserved quantities:

```lua
ZoneState = {
  total_energy = sum(kinetic) + sum(potential),  -- social energy
  angular_momentum = ...,                         -- rotational tendency
}

-- When a new NPC spawns (perturbation):
--   RepoAdded event → mass increases → energy shifts
--   Other NPCs adjust their orbits
--   System evolves toward new equilibrium

-- When an NPC dies/leaves (perturbation):
--   RepoRemoved event → mass decreases → gravitational field weakens
--   Orbiting creations may "escape" (become unowned)
--   Other NPCs drift to fill the gap
```

### Phase 5: Perturbation Events as Game Events
```lua
-- Player completes a major quest for an NPC
Perturbation.VelocityKick {
  vessel = "merchant",
  delta = { 0.0, 0.0, 0.5, 0.0, 0.0 },  -- social skill boost
}
-- → Merchant starts moving toward high-social region
-- → Other social NPCs adjust

-- Player builds something for an NPC
Perturbation.RepoAdded {
  vessel = "blacksmith",
  mass_delta = 1.0,
}
-- → Blacksmith's gravitational pull increases
-- → Apprentice NPCs pulled closer

-- War/disaster destroys creations
Perturbation.RepoRemoved {
  vessel = "guard-captain",
  mass_delta = 5.0,
}
-- → Guard captain's influence drops
-- → Criminal NPCs push outward (less restraint)
```

### Phase 6: Lagrange Points as Stable Zones
When three high-mass NPCs form an equilateral triangle, a Lagrange point exists:
- New NPCs spawned at Lagrange points are stable
- These become "town centers" or "market squares"
- Players discover them as safe, balanced zones
- Disrupting the triangle (NPC death) destabilizes the zone

### Phase 7: Leapfrog Evolution for World Simulation
Run the constellation simulation server-side:
- Each tick (1 second? 1 minute game-time?) = one leapfrog step
- NPCs physically drift toward/away from each other in trait space
- Their position changes affect dialogue, trade, quest availability
- Over hours/days, social structures emerge organically

### Implementation Priority: MEDIUM
Fascinating for emergent behavior but complex to implement and tune. More valuable as a late-phase feature when NPC count is high enough for dynamics to matter.

### Key Code to Port
1. `Vessel` struct → Lua NPC trait vector with mass
2. `GravitationalField` → NPC social dynamics calculator
3. Leapfrog integrator → server-side world evolution tick
4. `Perturbation` events → game event response system
5. `is_lagrange_triangle()` → stable zone detection
6. `ConservationState` → zone health/balance metrics
