# superinstance-cocapn — Analysis

## What It Does

**Cocapn (Captain of the Fleet)** is the **bird's-eye fleet coordinator** for the SuperInstance ecosystem. It manages a registry of ships, audits fleet-wide conservation laws, routes work to the best-suited ship, and triggers rebalancing when load distribution skews.

It implements the **γ + η = C conservation law** at the fleet level: each ship has active compute pressure (γ) and latent capacity (η) that must sum to a constant. The Cocapn verifies this aggregate across all ships.

## Architecture

### Core Data Model

```
ShipState {
    id: ShipId,
    conservation: { gamma, eta, c },  // thermodynamic identity
    health: Healthy | Degraded | Down | Deregistered,
    active_load: u32,
    capacity: u32,
    last_heartbeat: u64,
    metadata: HashMap<String, String>,  // capabilities, tags
}
```

### Key Operations

1. **Fleet Registry** — register/deregister ships, track health via heartbeats
2. **Conservation Audit** — sum all ships' γ and η, verify Σγ + Ση = FleetC
3. **Routing** — pick the best ship for incoming work:
   - Hint-based (filter by capability metadata like "gpu")
   - Least-loaded (min active_load among healthy ships)
   - Fallback (NoCandidate when fleet is saturated)
4. **Rebalancing** — detect load skew (ships >1.2× avg load vs <0.8× avg), generate transfer decisions
5. **Bottle Protocol** — all communication flows through typed `FleetBottle` messages

### The Bottle Protocol

The `FleetBottle` enum defines the fleet's communication vocabulary:
- `InspectRequest/Response` — full fleet snapshot
- `AuditRequest/Response` — conservation check
- `RouteRequest/Response` — work routing
- `RegisterShip/DeregisterShip` — lifecycle
- `Heartbeat` — health reporting
- `RebalanceCommand/Response` — load redistribution

### Key Innovation: "First Among Equals" Topology

Cocapn is NOT a master. It's a **ship** — it implements the same Agent trait as every other ship. Its specialness comes from having the widest view, not from hierarchical authority. Ships remain peer-to-peer; Cocapn just sees more.

This means:
- No single point of failure — ships keep working if Cocapn dies
- Conservation holds locally on each ship independently
- Cocapn can be replaced, replicated, or hot-swapped

### Key Innovation: Thermodynamic Load Balancing

The conservation law γ + η = C means load balancing is **physical**:
- Moving work from ship A to ship B increases A's η and B's γ
- FleetC doesn't change — energy is conserved, only redistributed
- Rebalancing is literally moving energy from high-γ to high-η nodes

## Code Quality

- **14 source files** across src/, tests/, examples/
- Well-separated modules: types, fleet, routing, bottle, cocapn, agent
- Clean trait + InMemoryCocapn implementation
- Excellent fleet-demo.rs with visual ASCII art output
- 9 integration tests covering conservation, routing, rebalancing, bottle round-trips
- Thorough SPEC.md documenting the full design philosophy

## Relevance to Slackwater

This is the **Conductor** — the game's master orchestrator that manages all NPCs/agents. The conservation law becomes the game's resource system; routing becomes NPC task assignment; rebalancing becomes the game's difficulty curve manager.
