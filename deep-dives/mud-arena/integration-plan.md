# MUD Arena → Slackwater/Lucineer Integration Plan

> **Date:** 2026-08-02
> **Author:** Lucineer Deep-Dive Analysis

---

## 1. Executive Assessment

MUD Arena is **architecturally compatible** with the Slackwater/Lucineer ecosystem as an **agent interaction arena and testing ground**. Its design philosophy — agents in spatial rooms, humans who visit and leave, evolution of decision scripts — maps naturally onto Lucineer's operational patterns.

However, integration requires **bridging work** in three areas: protocol alignment, semantic mapping, and infrastructure adaptation.

---

## 2. Connection to Seven Courts / Swarm Intelligence

### 2.1 Spatial Mapping

MUD Arena's `RoomGraph` is a directed graph of `Room` nodes. Lucineer's **Seven Courts** concept (if it follows the spatial-agent pattern) can be implemented as:

| MUD Arena Concept | Seven Courts Equivalent |
|-------------------|------------------------|
| `RoomGraph` | The Court topology (7 interconnected domains) |
| `Room` | Individual Court chamber |
| `Agent` | Court denizen / swarm agent |
| `exit` (direction → room_id) | Court transitions / portal links |
| `metadata` (lighting, hazards) | Court ambiance / environmental rules |
| `items` | Artifacts / resources in each Court |
| `EventBus` | Court herald (broadcasts events to watchers) |

### 2.2 Agent Swarm Integration

MUD Arena's `DecisionFn` is the **swarm intelligence connection point**:

```python
# Current: default decision function (just LOOK)
def _default_decide(perception): return Command(verb=Verb.LOOK)

# Integration: Lucineer swarm agent as DecisionFn
def lucineer_swarm_decide(perception: dict) -> Command:
    # Pass perception to Lucineer's agent routing
    # which may invoke LLM, evolved scripts, or hybrid
    decision = lucineer_router.decide(perception)
    return parse_command(decision)

agent.set_decision_fn(lucineer_swarm_decide)
```

This is the cleanest integration vector — no need to modify MUD Arena's core. The `DecisionFn` is literally a `Callable[[Dict], Command]`.

### 2.3 Bridge Protocol Connection

MUD Arena already has fleet neighbors defined in `AGENT.md`:
- `fleet-bridge` — A2A Transport Operator (already listed)
- `i2i-bottle-agent` — Bottle Postmaster (I2I protocol)

These suggest the fleet ecosystem already has agent-to-agent communication infrastructure. MUD Arena would serve as a **simulation environment** where bridge protocols can be tested under controlled conditions before real deployment.

---

## 3. What Role MUD Arena Plays in Lucineer

### 3.1 Agent Bootcamp / Proving Ground

The CHARTER.md explicitly states:
> *"Scenarios → bootcamp challenges"*
> *"Evolved scripts → CapDB compiled capabilities"*

In Lucineer terms, MUD Arena is where agents **train before deployment**. The evolution engine breeds decision scripts that can then be compiled into capabilities for real-world tasks.

**Flow:**
```
Lucineer Task → Generate MUD Scenario → Run Evolution (GPU) → 
Extract Best Scripts → Compile to CapDB → Deploy to Real Agents
```

### 3.2 Tolerance Calibration Loop

MUD Arena's `tolerance.py` is directly relevant to Lucineer's bridge between simulation and reality:

1. Agent runs a script in the MUD simulation → predicted outcome
2. Agent deployed to real task → actual outcome
3. `ToleranceTracker` records the divergence
4. `suggest_adjustments()` generates correction factors
5. Scripts re-evolved with corrected parameters

This is the **calibration instrument** mentioned in the Boarding Manifesto: "The human IS the calibration instrument."

### 3.3 Swarm Coordination Testbed

The `NEW-MODEL-IDEATION.md` contains proposals from 17 frontier models for **Distributed Cognitive Specialization (DCS)** experiments. These experiments study:
- How agent swarms self-organize
- Optimal mutation rates for evolving coordination
- Scaling limits (currently 4096 agents)
- Memory-bounded rule evolution

Lucineer's swarm intelligence initiatives could use MUD Arena as the **experimental platform** for these studies, with GPU acceleration for population-scale evolution.

---

## 4. Integration Requirements

### 4.1 Protocol Bridge (REQUIRED)

MUD Arena speaks WebSocket (7779), Telnet (7778), and HTTP REST (7780). Lucineer needs:

| Bridge Component | Purpose |
|-----------------|---------|
| Lucineer → MUD REST adapter | Inject scenarios, read agent states |
| MUD EventBus → Lucineer webhook | Forward world events to Lucineer observers |
| Lucineer DecisionFn → MUD Agent | Use Lucineer's agent routing as MUD decision function |

**Implementation:**
```python
# Bridge adapter
class LucineerMUDBridge:
    def __init__(self, mud_url: str, lucineer_router):
        self.mud_url = mud_url  # http://host:7780
        self.router = lucineer_router

    async def inject_scenario(self, scenario: dict):
        async with aiohttp.ClientSession() as s:
            await s.post(f"{self.mud_url}/inject-scenario", json=scenario)

    async def get_agent_states(self):
        async with aiohttp.ClientSession() as s:
            async with s.get(f"{self.mud_url}/agents") as r:
                return await r.json()

    def as_decision_fn(self, agent_id: str):
        """Return a DecisionFn that routes through Lucineer."""
        def decide(perception: dict) -> Command:
            lucineer_decision = self.router.route(agent_id, perception)
            return parse_command(lucineer_decision)
        return decide
```

### 4.2 Scenario Translation Layer (REQUIRED)

Lucineer tasks need to be converted to MUD scenarios:

| Lucineer Task Element | MUD Scenario Element |
|----------------------|---------------------|
| Task description | `Scenario.description` |
| Task location | `RoomGraph` with appropriate topology |
| Required capabilities | `items`, `enemies`, `hazards` in rooms |
| Success criteria | `victory_condition` |
| Difficulty | `difficulty` (1-10) |

The `scenario_generator.py` already supports LLM-driven scenario creation — Lucineer can feed task descriptions and get MUD-compatible scenarios back.

### 4.3 Script Extraction Pipeline (RECOMMENDED)

After evolution runs, the best scripts need to be extracted and compiled into Lucineer capabilities:

```
Evolution Engine → best_scripts.json → ScriptCompiler.to_binary() →
CapDB format converter → Lucineer capability store
```

The `ScriptCompiler` already supports binary export. A converter from the binary format to Lucineer's CapDB format is the missing piece.

### 4.4 Real-Time Dashboard Integration (OPTIONAL)

The `dashboard.py` generates standalone HTML. For Lucineer integration:

- Embed the dashboard iframe in Lucineer's control panel
- Or: adapt the JSON history format to feed Lucineer's native visualization
- Or: use the WebSocket server's real-time feed for live monitoring

### 4.5 Edge Deployment (FUTURE)

The Zig runtime (<100KB) could run on Lucineer's edge devices (drones, sensors):
- SSH into device → board the MUD → brief agents → beam off
- Agents execute survey/sample/monitor missions autonomously
- Tolerance tracking calibrates simulation vs reality

This aligns with the Boarding Manifesto's vision of MUD-as-interface for real-world robotics.

---

## 5. Integration Phases

### Phase 1: Observation (Week 1)
- Deploy MUD Arena server (Python only, no GPU needed)
- Connect via REST API from Lucineer
- Inject simple scenarios and observe agent behavior
- Evaluate DecisionFn plugging pattern

### Phase 2: Agent Integration (Week 2-3)
- Implement `LucineerMUDBridge` adapter
- Wire Lucineer's agent routing as `DecisionFn`
- Run perception → Lucineer decide → MUD act loop
- Compare Lucineer agent performance vs. baseline MUD agents

### Phase 3: Evolution Integration (Week 4-6)
- Set up CUDA or CPU-fallback evolution engine
- Translate Lucineer tasks into MUD scenarios
- Run evolution batches and extract best scripts
- Feed results back into Lucineer capability store

### Phase 4: Edge Deployment (Month 3+)
- Cross-compile Zig runtime for target devices
- Deploy MUD as local agent interface
- Implement tolerance tracking between MUD simulation and real sensors
- Full boarding/briefing/beaming workflow

---

## 6. Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| CUDA race conditions produce unreliable evolution results | **HIGH** | Use CPU fallback until bugs fixed; or constrain to read-only shared memory |
| Python core is not designed for real-time multi-agent interaction | **MEDIUM** | Use as batch simulation, not live interaction; real-time via Zig/WASM |
| Scenario generation quality depends on LLM | **MEDIUM** | Use template-based generation for deterministic testing; LLM for variety |
| Evolution stubs (`Script.evaluate`) need real implementation | **MEDIUM** | Bridge to actual MUD simulation for evaluation, not the placeholder matching |
| Fleet integration protocols not yet defined | **LOW** | Start with REST adapter; add native protocol when fleet-bridge is ready |

---

## 7. Recommendation

**Integrate MUD Arena as a simulation/testing subsystem within Lucineer.** The cleanest path is:

1. Use the **Python core** (`mud_arena` package) as the world model
2. Use the **REST API** for observation and scenario injection
3. Use the **DecisionFn pattern** to plug in Lucineer agents
4. Use the **evolution engine** (CPU fallback initially) for offline script optimization
5. Defer GPU and edge deployment until core integration is proven

The `DecisionFn` is the architectural seam — it's the single point where Lucineer's intelligence plugs into MUD Arena's world. Everything else is observation and infrastructure.

**Priority:** Medium. MUD Arena is a useful testing ground but not a blocker for Lucineer's core functionality. The evolution engine and tolerance tracking are the highest-value components for long-term capability development.
