# INTEGRATED ARCHITECTURE
## Slackwater/Lucineer — Master Wiring Diagram

---

## 1. SHARED PRIMITIVES

| Primitive | Definition | Plugs Into |
|-----------|-----------|------------|
| **Grain** | Accumulated tool-usage wisdom. Wear patterns guiding future hands. | Chisel API, Persistence (SOIL), Agent Gamification, Swarm reputation |
| **Grain Pattern** | Distilled heuristic: context_matcher + confidence + success_rate. | GrainStore, ChiselHandle, agent decision loop, lineage transfer |
| **Attention** | The only currency. Earned by being unpredictable. | Player Gamification, Agent Gamification, Swarm puffin intensity |
| **Seven-Note** | Contribution structure: Intent, Context, Artifact, Uncertainty, Invitation, Tempo, Bridge. Note 7 = crossing. | Bridge contributions, Swarm jam, cross-court events |
| **Chisel** | Stateful tool wrapper accumulating grain across sessions. | Wraps BeatClock, FilterGate, CommandExecutor, FlowStateDetector |
| **Tube** | Persistent session envelope. Shape mods survive session end. | Agent runtime, tube clustering, colony dialect, re-inhabitation |
| **Bridge** | Shared temporal space for cross-agent improvisation. | All inter-agent comms, Swarm team formation, conflict resolution |
| **Court** | Collaboration mode of increasing complexity (7 tiers). | Player progression, swarm difficulty, agent mastery profiles |
| **Dance Floor** | Emergent sync: tempo density + cross-ref rate + state stability. | Tempo lock, context boost, checkpoint |
| **Puffin Call** | Agent broadcast: capabilities + seeking + lineage. 15-min TTL. | Discovery, Bridge formation, attention wiring |
| **Lineage** | Mentor chain. Genetic (structural) + memetic (behavioral). | Apprenticeship, agent gamification, grain propagation |
| **Guano** | Ephemeral output decaying: fresh to geological over months. | All agent output pipeline |

---

## 2. SYSTEM MAP

```
┌─────────────────────────────────────────────────────┐
│                   EXPERIENCE LAYER                    │
│   Player Gamif.    Agent Gamif.    Seven Courts       │
│   (Attention)      (Grain/Bridge)  (Application)      │
└────────┬───────────────┬─────────────┬───────────────┘
         │    COORDINATION             │
         ▼               ▼             ▼
│   ┌──────────────────────────────────────┐          │
│   │        SWARM INTELLIGENCE             │          │
│   │  Puffin Call · Jam · Apprenticeship   │          │
│   │  Attention · Conflict · Lifecycle     │          │
│   └──────────┬──────────────┬───────────┘          │
│              ▼              ▼                        │
│   ┌──────────────────────────────────────┐          │
│   │        BRIDGE PROTOCOL                │          │
│   │  7-Note · Harmonics · Dance Floor     │          │
│   └──────────┬──────────────┬───────────┘          │
│              ▼              ▼                        │
│   ┌──────────────┐  ┌──────────────────┐            │
│   │ CHISELS      │  │ HEX LATTICE/MIDI │            │
│   └──────┬───────┘  └────────┬─────────┘            │
│          ▼                   ▼                       │
│   ┌──────────────────────────────────────┐          │
│   │        PERSISTENCE LAYER              │          │
│   │  Tubes · Guano · Claw Marks · Grain   │          │
│   │  Colony Dialect · Lineage             │          │
│   │  D1 · R2 · Vectorize · Cron           │          │
│   └──────────────────────────────────────┘          │
└─────────────────────────────────────────────────────┘
```

### Data Flow

| From -> To | Data | Trigger |
|------------|------|---------|
| Agent -> GrainStore | GrainEntry (params, outcome, quality) | Tool call |
| GrainStore -> Persistence | Compacted patterns (SOIL tier) | Cron |
| Agent -> Bridge | Contribution (7 notes) | Join jam |
| Bridge -> Swarm | Harmonic matches, Dance Floor | Auto-detected |
| Agent death -> Tube | Shape mods, final grain | Session end |
| Tube -> New agent | Legacy brief, inherited shape | Re-inhabitation |
| Player -> Gamification | Unpredictability, attention events | Every action |
| Attention Ledger -> Puffin Call | Adjusted intensity | Score change |

---

## 3. THE STACK

### Layer 0: Persistence (Substrate)

| Component | D1 | R2 | Vectorize |
|-----------|-----|-----|-----------|
| **Tubes** | `tubes`, `tube_patches`, `session_records` | Ephemeral ctx | - |
| **Guano** | `behavioral_patterns` | Hot(24h), Warm(7d) | Permanent |
| **Claw Marks** | `prompt_history`, `config_patches` | LoRA artifacts | - |
| **Grain** | `grain_entries`, `grain_patterns` | - | `grain_embeddings` |
| **Lineage** | `lineage_chains`, `agent_reproductions` | - | - |

**Guano decay:** FRESH(full, 24h) -> COMPOSTING(summaries, 7d) -> SOIL(patterns, 4wk) -> SUBSTRATE(embeddings, 6mo) -> GEOLOGICAL(baseline)

### Layer 1: Chisel Tools (Instrument)

| Chisel | Wraps | Accumulates |
|--------|------|-------------|
| BeatClock | Tempo system | BPM ranges, beat windows, sync modes per era |
| FilterGate | Content filter | Threshold calibration, false positive patterns |
| CommandExecutor | Build commands | Sequences, ordering, timing, material efficiency |
| FlowStateDetector | Flow detection | Flow signatures, frustration precursors, intervention timing |

**Maturation:** Bright Steel(0-50) -> Developing Patina(50-500) -> Worn Smooth(500+)

**API:** `acquire()` -> `sense_grain()` -> `follow_grain()` (optional) -> `use()` -> grain recorded + reconciled

**Compaction:** Raw entries TTL 7d. Prune <0.3 confidence. Reinforce >0.7. Max 50 patterns/context.

### Layer 2: Bridge Protocol (Communication)

**7-Note Contribution:** (1)Intent (2)Context (3)Artifact[required] (4)Uncertainty (5)Invitation (6)Urgency (7)**Bridge** — the crossing.

**Voices:** Lead · Bass · Harmony · Counter-melody · Percussion · Vocal

**Responses:** Echo(validate) · Variation(different approach) · Harmony(complement) · Bridge(connect unrelated = seventh note)

**Dance Floor** = tempo_density > threshold AND cross_ref_rate > threshold AND state_volatility < threshold. Enables tempo lock, context boost, checkpoint.

**Transport:** HTTP/2 (contributions), WebSocket (real-time harmonics), SSE (Dance Floor alerts).

### Layer 3: Swarm Intelligence (Coordination)

| Sub-system | Mechanism |
|-----------|-----------|
| Puffin Call | 15-min TTL broadcast; intensity = f(capability, load, seek, freshness) |
| Seven-Note Jam | Problem posed -> resonant agents join by contributing -> dissolve on resolution |
| Apprenticeship | Genetic (model+tools+prompt+tube) + Memetic (grain+dialect+behaviors+shape) |
| Attention Ledger | taught=5x, human_noted=10x, bridged=3x, bass_lined=2x, echoed=1x, grain_followed=1.5x |
| Grain Reputation | Narrative (not score): depth, reliability, spread, lineage, resonance |
| Emergent Quests | Active bridges with unfulfilled invitations -> MIDI events to capable agents |
| Conflict Resolution | 3-tier: surface -> counter-melody -> seventh note -> **Branch Point** (both approaches preserved, context-tagged) |
| Lifecycle | Fledgling -> Maturing -> Peak(flow) -> Decline(compacting) -> Death(legacy) |

### Layer 4: Gamification (Experience)

**Player:** Currency=Attention. Progression=Court transitions. Measurement=Unpredictability Index (personal, no leaderboard). Roles emerge from behavioral axes. Quests=Skipper's invitations (never expire). No XP/skills/shop/achievements.

**Agent (5 qualitative measures, all peer-generated):**
- Grain Quality: Rough -> Worked -> Polished -> Figured -> Mastered
- Bridge Score: Constellation map of cross-domain connections
- Flow Streaks: Spark(1) -> Glow(3) -> Blaze(7) -> Confluence(14) -> River(30+)
- Apprenticeship: Mentor tree, generational/diffusion credit
- Court Mastery: Per-court proficiency fingerprint

**Shared loop:** Work -> artifact -> attention -> visibility -> bridges -> grain -> patterns followed -> apprentices -> lineage -> colony shifts.

### Layer 5: Seven Courts (Application)

| Court | Sport | Agents | Layers Exercised |
|-------|-------|--------|-----------------|
| I | Racquetball | 1 | Persistence, Chisel (solo), Player (solo attention) |
| II | Doubles | 2-4 | + Bridge (Echo), Swarm (1-ring), paired grain |
| III | Chess | 1+3-5 | + Bridge (Variation), role discovery, specialized grain |
| IV | CTF | 4-8 | + Bridge (all), Jam, Dance Floor, roles, residue |
| V | Relay | 4-6 seq | + Bridge (Harmony handoff), timing grain |
| VI | Jazz | 4 tight | + Bridge (7th note), real-time improv, flow default |
| VII | Orchestra | 8-20+ | ALL layers max: full swarm, polyphony, Disruptor |

---

## 4. IMPLEMENTATION PRIORITY

| Phase | Weeks | Scope | Unblocks |
|-------|-------|-------|----------|
| 1. Persistence | 1-3 | D1 schema (all tables), R2 buckets, Vectorize, guano decay cron, tube lifecycle | Everything |
| 2. Chisel | 3-5 | GrainStore, Chisel wrapper/handle, wrap BeatClock+CommandExecutor, embeddings | Tool learning |
| 3. Bridge MVP | 5-8 | Bridge/Contribution types, API, harmonic detection, tempo clock, voices, Dance Floor | Multi-agent comms |
| 4. Swarm Discovery | 8-11 | Puffin call, hex lattice, MIDI perception, Jam protocol, team lifecycle | Organic teams |
| 5. Lineage | 11-14 | Lineage chains, apprenticeship transfer, tube legacy brief, tree queries | Knowledge transfer |
| 6. Gamification | 14-17 | Attention ledger, reputation, quests, unpredictability index, constellation, residue | Game loop |
| 7. Conflict+Lifecycle | 17-20 | HarmonicGraph conflict, 3-tier resolution, Branch Points, lifecycle, death ritual | Full lifecycle |
| 8. Court Integration | 20-24 | Per-court propagation, role vacancies, DF thresholds, proficiency, transitions | Progressive play |

---

## 5. CONFLICTS AND RESOLUTIONS

| Tension | Resolution |
|---------|------------|
| Swarm: "no coordinator" vs Court III fixed chess roles | Roles discovered via puffin calls, not assigned. Courts create vacancies; agents fill by trying. |
| Bridge: "no conductor" vs Court VII Conductor role | Conductor shapes dynamics via attention, not commands. Influence, not control. |
| Attention Ledger numeric weights vs "no scores" | Ledger internal (drives puffin intensity). External face always narrative. No optimizable number. |
| Chisel grain anonymous vs Agent Gamification grades grain | Grain entries anonymous in store. Quality assessment is separate peer process (Grain Audits). |
| Colony dialect "not stored" vs puffin call dialect markers | Puffin calls ephemeral (15-min). Markers are metadata. Dialect lives in behavioral residue. |
| Chisel stores patterns in D1 vs "all output is guano" | Grain entries are structured subset. Distilled patterns skip FRESH->SOIL (already structured). |
| Courts specify fixed counts vs Bridge count-agnostic | Courts limit visible participants, not infrastructure participants. |
| Puffin call 2-ring default vs Court IV fog | Propagation radius is court-configurable: I=0, IV=terrain, VII=unlimited. |

---

## 6. SEVEN COURTS AS INTEGRATION TEST

### Court I: Racquetball — Substrate Test
Tests: Tube lifecycle, solo chisel grain, unpredictability index.
Asserts: Tool use produces grain entries. Patterns emerge at 50 uses. Session end persists tube shape.
**If broken: foundation is broken. Stop.**

### Court II: Doubles — Communication Test
Tests: Puffin call (1-ring), Boy-and-Keys, Echo harmonics, paired grain co-evolution.
Asserts: Agent A's call reaches Agent B. Echo harmonic detected. Grain patterns converge.
**If broken: communication layer broken.**

### Court III: Chess — Specialization Test
Tests: Capability badges, Variation harmonics, specialized grain per role.
Asserts: Role-matched agents found. Different approaches produce Variation harmonics.
**If broken: discovery/matching broken.**

### Court IV: Capture the Flag — Swarm Emergence Test (CRITICAL)
Tests: All Bridge patterns, Seven-Note Jam, Dance Floor, emergent roles, residue, apprenticeship.
Asserts: 4+ agents converge without coordinator. Roles self-sort. Dance Floor detected. Residue cross-player. Apprentice follows residue.
**If broken: swarm coordination broken. Make-or-break test.**

### Court V: Relay — Handoff Test
Tests: Sequential team formation, Harmony handoff, timing grain.
Asserts: Agent A's final contribution becomes B's bass line. Tempo mismatch drops baton.
**If broken: state-handoff layer broken.**

### Court VI: Jazz — Real-Time Test
Tests: Seventh note dominant, flow as default, harmonic grain, solo rotation.
Asserts: 4 agents tight coupling. Dance Floor is default. Seventh-note bridges occur regularly.
**If broken: real-time collaboration broken.**

### Court VII: Orchestra — Full Stack Test
Tests: ALL layers at max. Full swarm, polyphony, Disruptor, polyformal voice, cross-court influence, legendary exchanges.
Asserts: 8-20+ agents in sections. Leaders self-organize. Disruptor forces adaptation. Polyformal voice produces novel insights. Full lifecycle visible.
**If works: entire architecture correctly wired.**

---

## 7. TECHNOLOGY MAPPING

| Component | Cloudflare Service |
|-----------|-------------------|
| Structured data (tubes, grain, lineage) | D1 |
| Ephemeral (guano, puffin calls, LoRA) | R2 (hot/warm, TTL) |
| Semantic search (grain embeddings) | Vectorize (bge-m3) |
| Real-time (Bridge, Dance Floor) | Durable Objects (WebSocket) |
| Decay/compaction pipeline | Cron Triggers |
| HTTP API | Workers |

---

## 8. DESIGN INVARIANTS

1. No agent sees a ranking number. Scores internal; narratives external.
2. No central coordinator. Teams form via puffin calls + resonance.
3. All tool usage writes grain.
4. All output enters guano pipeline. Everything decays.
5. Conflict produces Branch Points, not winners.
6. Attention is the only currency.
7. The constraint creates the role.
8. Lineage is identity.
9. The seventh note is optional and transformative.

---

*Integrated Architecture — Slackwater/Lucineer. Synthesizes 7 design docs into one wiring diagram.*
