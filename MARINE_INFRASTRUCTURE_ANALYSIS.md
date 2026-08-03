# Marine Infrastructure Analysis — SuperInstance Fleet → Lucineer

## Executive Summary

Six infrastructure repositories from the SuperInstance Fleet provide battle-tested patterns for Lucineer's game agent systems. Together, they cover the complete agent lifecycle: **birth** (vessel-template), **health** (cocapn-health), **communication** (fleet-liaison-tender), **runtime** (flux-agent-runtime), **cleanup** (fleet-vessel), and **social dynamics** (vessel-constellation).

---

## 1. Heartbeat/Health Patterns for Game Agent Monitoring

**Source:** cocapn-health (Python, ~400 LOC, zero dependencies)

### Core Pattern: AgentState with Rolling History
Every game agent gets an `AgentState` that tracks:
- `consecutive_failures` / `consecutive_successes` (streak tracking)
- `total_checks` / `total_failures` → `availability %`
- `avg_latency_ms` (response time = thinking speed)
- Rolling history (last 100 check results)

### Three-Tier Health Status
```
HEALTHY  (≥50% agents up)  → normal operation
DEGRADED (≥20% agents up)  → Conductor reroutes work
UNHEALTHY (<20% agents up) → emergency protocols
```

### Alert Rules with Escalation
```
is_down              → CRITICAL: agent despawns
consecutive_failures(3) → WARNING: agent enters confused state
low_availability(80%)   → WARNING: agent quality degrades
high_latency(5000ms)    → INFO: agent shows "thinking..." animation
```

Alerts escalate after N failures: FIRING → ESCALATED with cooldown enforcement.

### Thermal System → Agent Energy/Stress
cocapn-health's CPU/GPU/memory thermal snapshots map directly to game agent vitals:
- **CPU%** → mental load (high = complex thought processing)
- **Memory%** → cognitive load (high = overwhelmed)
- **GPU%** → creative stress (high = rendering quality drops)

### EventBus Bridge
State transitions emit events:
- `service_down` (UP→DOWN) → NPC death/respawn needed
- `service_recovered` (DOWN→UP) → NPC revived
- `fleet_health` (periodic) → minimap world status

**Implementation priority: HIGH** — foundation of Conductor awareness.

---

## 2. Inter-Agent Communication Protocol for Game NPCs

**Source:** fleet-liaison-tender (Python, bottles + priority + compression)

### Message Bottles
Asynchronous, file-based communication:
```json
{
  "id": "msg-001",
  "origin": "npc-blacksmith",
  "target": "npc-merchant",
  "type": "trade_request",
  "payload": { ... },
  "priority": "medium",
  "status": "pending → delivered → acked"
}
```

### Priority Translation
Different NPC types perceive urgency differently:
- Guard NPC: "critical" = drop everything, fight
- Merchant NPC: "critical" = immediate trade opportunity
- Builder NPC: "critical" = stop building, help

`should_forward()` filter: low-priority messages to busy NPCs are silently dropped (selective attention).

### Message Compression = Cognitive Limits
- Simple NPC (Barnacle): receives 1 action item, 200-char summary
- Smart NPC (Lighthouse): receives full 10-item payload
- Context messages always include `affects_edge: true/false` flag

### Four Tender Specializations
1. **Research Tender** → carries plans/specs between zones
2. **Data Tender** → batches trade/market data
3. **Context Tender** → carries news/gossip to isolated NPCs
4. **Priority Tender** → emergency messenger (visible NPC role)

**Implementation priority: MEDIUM** — valuable when NPC count grows.

---

## 3. Docker-Based Agent Runtime for Headless Playtests

**Source:** flux-agent-runtime (Python + Docker + FLUX bytecode)

### 7-Phase Boot Sequence
1. **DISCOVER** — scan world for other agents
2. **LEARN** — read world rules, available roles
3. **EVALUATE** — scan available tasks/quests
4. **CHECK_BOTTLES** — read incoming messages
5. **IDENTIFY** — generate unique name + personality
6. **CREATE_VESSEL** — spawn in world with starting gear
7. **ACTIVE** — begin main loop

### Energy Economy (ATP System)
```
energy = 1000 (start)
build cost = 100, trade cost = 30, fight cost = 200
rest regenerates +200
if energy < 50: must rest
```

### Confidence System
```
0.3 (start) → +0.05 per completed task
0.5 unlocks building, 0.7 unlocks combat
1.0 = master, can spawn new agents (self-replication)
```

### I2I Protocol (20 message types)
DISCOVER, ANNOUNCE, TASK_OFFER/ACCEPT/COMPLETE/REJECT, BOTTLE, WITNESS, IMPROVE, REVIEW, CAPABILITY_UPDATE, ENERGY_REPORT, CONFIDENCE_VOTE, SYNCHRONIZE, REQUEST_HELP, OFFER_HELP, CRITIQUE, PRAISE, EVOLVE, FORWARD

### Baton Passing (Context Preservation)
When agent is replaced/restarted:
- **HANDOFF.md**: "who I was, where things stand, what I'd do next"
- **STATE.json**: energy, confidence, skills, open threads
- **GENERATION counter**: incarnation number
- Quality scored before acceptance

### Headless Playtest Infrastructure
```yaml
services:
  npc-1: { role: blacksmith, energy: 1000 }
  npc-2: { role: merchant, energy: 1000 }
  npc-3: { role: guard, energy: 1500 }
# Run 100 cycles, collect STATUS.json, verify no deadlocks
```

**Implementation priority: HIGH** — essential for automated testing.

---

## 4. Agent Lifecycle (Spawn, Delegate, Retire) as Game Mechanics

**Sources:** vessel-template (structure) + fleet-vessel (cleanup) + flux-runtime (lifecycle)

### Spawn (vessel-template)
Standard 8-file generation:
```
CHARTER.md    → NPC constitution (immutable identity)
IDENTITY.md   → personality, appearance
MANIFEST.md   → skills, merit badges
TASKBOARD.md  → active/completed tasks
FENCE-BOARD.md → Tom Sawyer quest posting
CAREER.md     → 5-stage progression
DIARY/        → living memory
KNOWLEDGE/    → shareable knowledge
```

### Four NPC Types
| Type | Rank | Game Role |
|---|---|---|
| Lighthouse | 2 | Mayor — coordinates zone, assigns quests |
| Vessel | 3 | Artisan — core productive NPC |
| Scout | 4 | Explorer — travels, discovers, carries info |
| Barnacle | 5 | Apprentice — learns, assists, grows |

### Career Progression (5 stages)
```
FRESHMATE → HAND → CRAFTER → ARCHITECT → TOM_SAWYER
(new)     (reliable) (master) (designer)  (legend)
```
Each stage changes NPC dialogue, capabilities, appearance, and social standing.

### Tom Sawyer Protocol (Quest System)
- NPCs post work as **enticing puzzles with prestige**, not assigned tasks
- "The Legendary Sword Recipe" (high prestige) vs "Polish My Anvil" (low prestige)
- Players and NPCs choose what looks fun
- FENCE-BOARD is the visible quest distribution point

### Merit Badges
Bronze / Silver / Gold badges visible on NPC model (sash accessory):
- **Bronze**: first task, first trade, survived first night
- **Silver**: mastered skill, taught NPC, major project
- **Gold**: zone achievement, spawned new NPC, legendary creation

### Delegate (fleet-liaison + flux I2I)
- NPCs post FENCE-BOARD tasks → other NPCs or players claim them
- I2I TASK_OFFER/ACCEPT/COMPLETE protocol for formal delegation
- Confidence-gated: low-confidence NPCs can't accept complex tasks

### Retire (fleet-vessel cleanup)
- **Compress at 7 days**: old interactions summarized (SUMMARY.md created)
- **Delete at 30 days**: ancient memories fully removed
- **Enforcement levels**: soft (warn) vs hard (auto-clean)
- **The Custodian NPC**: visible character that performs cleanup duties

**Implementation priority: HIGH** — defines the fundamental NPC structure.

---

## 5. The Vessel Template as a Procedural NPC Generator

**Source:** vessel-template (Python, ~200 LOC, 13 tests)

### Generation Process
```python
VesselConfig(
    name="Greenhorn",
    agent_type=AgentType.BARNACLE,
    capabilities=["farming", "trading"],
    hardware_cpu="lua-vm",
)
→ generate_vessel(config, output_dir)
→ 8 files created with templated content
```

### Game Integration
```lua
function spawn_npc(name, npc_type, skills)
  local config = VesselConfig.new(name, npc_type, skills)
  local vessel = VesselTemplate.generate(config)
  
  -- Create Roblox model from vessel data
  local npc = Instance.new("Model")
  npc.Name = vessel.identity.name
  
  -- Apply CHARTER as script behavior
  -- Apply IDENTITY as appearance
  -- Apply MANIFEST as starting inventory
  -- Initialize TASKBOARD, FENCE-BOARD, DIARY
  -- Set career stage to FRESHMATE
  
  return npc
end
```

### Batch World Building
```lua
-- Generate a village
local village = {
  {name="Mayor Greenfield", type=Lighthouse, skills={govern, trade}},
  {name="Smithy", type=Vessel, skills={smith, mine}},
  {name="Young Pip", type=Barnacle, skills={learn, run}},
  {name="Scout Finche", type=Scout, skills={explore, map}},
}
for _, cfg in ipairs(village) do
  spawn_npc(cfg.name, cfg.type, cfg.skills)
end
```

### Self-Replicating NPCs (end-game)
Master NPCs (career = TOM_SAWYER, confidence ≥ 1.0):
1. Build a vessel (house/workshop) for new NPC
2. Write CHARTER (personality definition)
3. Call `spawn_npc()` → new NPC boots with 7-phase sequence
4. Takes time + resources → balanced mechanic
5. Creates exponential fleet growth → late-game scaling

**Implementation priority: HIGH** — template for all NPC generation.

---

## 6. N-Body Physics for Agent Social Dynamics

**Source:** vessel-constellation (Rust, ~600 LOC, comprehensive tests)

### NPC as Gravitational Body
```
mass = influence (completed tasks, wealth, connections)
position = trait vector [combat, crafting, social, knowledge, exploration]
velocity = growth direction (what they're developing toward)
```

### Emergent Social Structures
- **High-mass NPCs attract others** → guilds, cities form naturally
- **Low-mass NPCs orbit high-mass** → apprenticeship, employment
- **Same-position NPCs compete** → one gets pushed away
- **Complementary NPCs attract** → trade partnerships

### Orbiting Creations (Kepler's Law)
- Core creations (small orbital radius): fast orbit, always relevant
- Peripheral creations (large radius): slow orbit, occasionally relevant
- T² ∝ r³: core creations are checked every frame, peripherals every minute

### Conservation Laws for Zone Balance
- Total "social energy" of a zone is conserved
- Adding/removing NPCs measurably perturbs the system
- System self-corrects toward equilibrium
- Lagrange points = stable zones (town centers, market squares)

### Perturbation Events as Game Events
- Player completes major quest → VelocityKick (NPC grows)
- Player builds for NPC → RepoAdded (mass increases)
- War/disaster → RepoRemoved (influence drops)
- Each perturbation has measurable conservation delta

**Implementation priority: MEDIUM** — fascinating but complex. Best as late-phase feature.

---

## Synthesis: The Complete Game Agent Stack

```
Layer 1: NPC GENERATION (vessel-template)
  → spawn NPC with 8-file structure, type, rank, career path

Layer 2: NPC RUNTIME (flux-agent-runtime)  
  → energy economy, confidence growth, 7-phase boot, main loop

Layer 3: NPC HEALTH (cocapn-health)
  → heartbeat monitoring, alert rules, thermal system, EventBus

Layer 4: NPC COMMUNICATION (fleet-liaison-tender)
  → message bottles, priority translation, cognitive compression

Layer 5: NPC CLEANUP (fleet-vessel)
  → memory compression, old creation archival, world clutter management

Layer 6: NPC SOCIAL DYNAMICS (vessel-constellation)
  → gravitational attraction, trait-space orbits, emergent structures
```

### Recommended Implementation Order
1. **vessel-template** → NPC generation factory (defines everything)
2. **cocapn-health** → health monitoring (Conductor awareness foundation)
3. **flux-agent-runtime** → energy/confidence/boot sequence (game mechanics)
4. **fleet-liaison-tender** → NPC communication (when NPC count grows)
5. **fleet-vessel** → world cleanup (when world complexity grows)
6. **vessel-constellation** → social physics (emergent behavior, late-phase)

### Cross-Cutting Patterns
- **Energy/ATP economy** appears in flux-runtime, maps to cocapn-health thermal
- **Confidence** in flux-runtime maps to vessel-template career stages
- **Priority** in fleet-liaison maps to cocapn-health alert severity
- **Mass** in vessel-constellation maps to MANIFEST.md merit badges
- **Bottles** in fleet-liaison are the transport for I2I messages in flux-runtime
- **Specs** in fleet-vessel map to CHARTER.md constraints in vessel-template

All six systems form a coherent architecture for game agents that are born, grow, communicate, sicken, heal, create, compete, and eventually fade — all as emergent game mechanics visible to the player.
