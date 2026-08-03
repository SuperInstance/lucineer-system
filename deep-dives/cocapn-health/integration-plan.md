# cocapn-health → Lucineer Game Agent Integration Plan

## Game Agent Health Monitoring System

### Concept: The Conductor's Awareness
The Conductor (Lucineer's orchestration layer) needs real-time awareness of every NPC agent's state. cocapn-health provides the exact pattern: define each game agent as a `ServiceDef`, run periodic checks, track state transitions, and fire alerts when agents degrade.

### Integration Architecture

```
Game Agent (Lua/Roblox)
  ↕ HTTP endpoint or DataStore signal
HealthChecker (per-agent ServiceDef)
  → CheckResult (ok, latency, details)
    → AgentState (rolling history, availability %, failure streaks)
      → AlertManager (rules: is_down, consecutive_failures, low_availability)
        → Conductor decisions (reroute, respawn, degrade gracefully)
```

### Phase 1: Agent Health DataModel
Map cocapn-health types to Roblox game state:

| cocapn-health Type | Game Equivalent |
|---|---|
| `ServiceDef` | NPC Agent definition (name, check endpoint/DataStore key, timeout) |
| `CheckResult` | Per-frame or per-tick agent status (alive, thinking, responding) |
| `AgentState` | NPC's recent performance history (success rate, response time) |
| `HealthStatus` | Fleet/squad status: HEALTHY (all NPCs fine), DEGRADED (some struggling), UNHEALTHY (mass failure) |
| `AlertRule` | Game events: "NPC stuck" (consecutive_failures ≥ 5), "NPC slow" (latency > 200ms) |
| `HealthAlert` | Game alert with escalation: warn player → critical notification |

### Phase 2: The Conductor's Dashboard
- Port `HealthMonitor` as a Lua module running server-side
- Each NPC registers a heartbeat (via RemoteFunction or DataStore)
- Conductor displays fleet status as an in-game minimap overlay
- Failing NPCs get visual indicators (red glow, warning icon)

### Phase 3: Alert-Driven Game Mechanics
- **consecutive_failures(3)**: NPC enters "confused" state, wanders randomly
- **low_availability(50%)**: NPC's building/creation degrades in quality
- **high_latency(5000ms)**: NPC freezes, shows "thinking..." animation
- **is_down**: NPC despawns, death animation, replacement spawned
- **ESCALATED**: nearby NPCs receive distress signal, change behavior

### Phase 4: Thermal System as Game Mechanic
cocapn-health's thermal snapshots (CPU/GPU/memory) translate directly to agent "energy" and "stress":
- **CPU %** → Agent's "mental load" — high CPU means agent is processing complex thoughts
- **Memory %** → Agent's "working memory" — high memory means agent is overloaded
- **GPU %** → Agent's "rendering stress" — visual quality of agent's creations drops

### Phase 5: EventBus Bridge for Multiplayer
- Use the sunset_bridge pattern: emit game events on agent state transitions
- `service_down` → NPC death event broadcast to all clients
- `service_recovered` → NPC respawn/revival event
- `fleet_health` → periodic world-state snapshot for minimap

### Implementation Priority: HIGH
This is the foundation for the Conductor's awareness. Without health monitoring, the game can't know which agents need help, replacement, or rerouting.

### Key Code to Port
1. `AgentState` with rolling history → Lua table with ring buffer
2. `AlertManager.evaluate()` → Conductor's per-tick decision loop
3. `HealthReport.to_markdown()` → Admin/debug overlay
4. `HealthCache` with TTL → DataStore-backed status cache
