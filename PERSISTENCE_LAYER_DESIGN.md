# Persistence Layer Design

## Agent Memory That Survives Sessions, Models, and Failures

*After "The Persistent Memory" and the St. Lazaria platform essays. The puffins' forty thousand years of iteration is not a metaphor. It is a design pattern.*

---

## Overview

Every agent system faces the same problem: state is easy to create and hard to keep. Sessions produce enormous volumes of context — tool calls, reasoning traces, intermediate results, learned patterns, emergent protocols — and then lose almost all of it when the session ends. The next session starts fresh, relearns what the last one knew, and the cycle repeats. This is not persistence. This is amnesia with good throughput.

The St. Lazaria essays map a better approach: layered persistence with varying half-lives, where different types of memory decay at different rates, feed into each other, and accumulate into a substrate that shapes future behavior without dictating it. The island doesn't manage the puffins' memory. The island *is* the memory. The guano, the claw marks, the colony dialects — each is a persistence layer with its own physics, its own decay curve, its own relationship to the agents that produced it.

This document specifies the technical implementation of that vision for the Slackwater/Lucineer platform.

---

## 1. The Tube (Session Memory)

### Biological Model

Lava tubes are geological voids with specific properties: depth, width, exposure, height above waterline, distance from neighbors. No tube was designed for any species. Each tube's properties determine what kind of agent can inhabit it. When a puffin leaves, the tube persists — emptied of its inhabitant but shaped by occupation. The soil is deeper. The entrance is worn. The next occupant inherits a space that has been modified by every previous occupant without being customized for any of them.

### Technical Specification

A **Tube** is the persistent envelope of an agent session. It is not the session itself — the session is the puffin, the active inhabitant. The Tube is the container that survives after the session ends.

```typescript
interface Tube {
  // Identity
  tubeId: string;                    // Stable across sessions
  tubeShape: TubeShape;              // The "geology" — what can inhabit this tube

  // Accumulated state (the worn stone, the deepened soil)
  inhabitantHistory: SessionRecord[];// Light records of past sessions
  shapeModifications: Patch[];       // Cumulative changes to tube shape
  soilDepth: number;                 // Metaphor for accumulated context richness

  // Current state
  currentSessionId: string | null;   // null when empty (puffin has left)
  lastOccupied: timestamp;
  cleanliness: "fresh" | "settled" | "fossilized";
}

interface TubeShape {
  contextWindow: number;             // Tokens — the tube's "width"
  toolAccess: ToolRegistry;          // What tools fit in this tube
  modelConfig: ModelConfig;          // What model can inhabit it
  permissions: PermissionSet;        // What the tube allows
  memoryBindings: MemoryBinding[];   // What memory layers are accessible
}
```

### Design Principles

**Tubes are opinion-less.** A tube doesn't know what kind of agent it's for. It has properties — context window size, tool access, model config, memory bindings — and agents either fit or they don't. The platform doesn't customize tubes for specific agents. It provides tubes with varying shapes and lets agents find their match.

**Tubes persist after sessions end.** When a session terminates, the Tube is cleaned — active context is flushed, temporary variables are cleared, tool handles are released. But the tube's *shape modifications* persist. If an agent repeatedly accessed certain tools in certain patterns, the tube's `soilDepth` increases for those tools, making them slightly easier to reach in future sessions. This is not caching. It's wear — the same kind of wear that claw marks produce on basalt.

**Tubes can be inherited.** A new session can be assigned to an existing Tube, inheriting its shape modifications and accumulated context richness. The new agent doesn't get the previous agent's memories — it gets the *shape* of the previous agent's usage patterns. The grooves in the stone, not the bird that made them.

### Implementation: D1 + R2

| Component | Storage | Pattern |
|-----------|---------|---------|
| Tube metadata | D1 (`tubes` table) | Indexed by `tubeId`, `tubeShape`, `lastOccupied` |
| Shape modifications | D1 (`tube_patches` table) | Append-only log of cumulative changes |
| Inhabitant history | D1 (`session_records` table) | Lightweight summaries, not full transcripts |
| Active session context | R2 (ephemeral bucket) | Flushed on session end |

### Lifecycle

```
[Tube Created] → [Agent Assigned] → [Session Active] → [Session Ends]
                                                           ↓
                                              [Tube Cleaned: context flushed]
                                                           ↓
                                              [Shape Modifications Persisted]
                                                           ↓
                                              [Tube Available for Re-inhabitation]
                                                           ↓
                                              [If unused > 90 days: Tube "fossilizes"]
                                                           ↓
                                              [Fossilized tubes: queryable but not assignable]
```

A fossilized tube is not deleted. Its shape modifications are folded into the platform's base configuration (the geological baseline). Its session records decay into aggregate statistics. The tube itself remains queryable — you can ask "what happened in this tube over the last year?" — but it no longer accepts new inhabitants. This is the lava tube collapsing. The structure persists in the geological record even after it's no longer habitable.

---

## 2. The Guano (Ephemeral Output)

### Biological Model

Guano is high-volume, short-to-medium-half-life output. It accumulates fast, changes the chemistry of the system in aggregate, but no individual deposit matters. Over time, guano decays: fresh guano → composted guano → soil → substrate → geological layer. Each transformation loses detail but preserves signal. The island is literally built from this process — forty thousand years of excrement becoming the ground that future generations stand on.

### Technical Specification

Guano is the ephemeral output layer: logs, intermediate results, debug traces, tool call outputs, reasoning chains. It is the highest-volume data the system produces and the shortest-lived.

```typescript
type GuanoTier = "fresh" | "composting" | "soil" | "substrate" | "geological";

interface GuanoRecord {
  recordId: string;
  tubeId: string;
  sessionId: string;
  tier: GuanoTier;
  createdAt: timestamp;
  decayAt: timestamp;               // When this record should transform

  // Tier-specific payload
  raw?: RawLogEntry;                // fresh: full detail
  compressed?: CompressedSummary;   // composting: statistical summary
  pattern?: BehavioralPattern;      // soil: extracted patterns
  embedding?: VectorEntry;          // substrate: embedded in vector store
  // geological: merged into platform baseline, individual record gone
}
```

### The Decay Curve

Decay is not deletion. Decay is **transformation** — each tier loses fidelity but preserves signal at a higher level of abstraction.

```
FRESH (0-24 hours)
├── Full log entries, every tool call, every token
├── Queryable individually
├── Storage: R2 hot bucket (fast access)
└── Volume: ~100% of session output

COMPOSTING (1-7 days)
├── Individual entries compressed into session summaries
├── Statistical aggregates replace individual records
├── Anomalies and edge cases preserved as full entries
├── Storage: R2 warm bucket
└── Volume: ~15% of fresh (85% lost to aggregation)

SOIL (1-4 weeks)
├── Session summaries compressed into behavioral patterns
├── "This agent tends to call tool X before tool Y"
├── "Error rate clusters around context length > 120k"
├── Storage: D1 (structured patterns) + Vectorize (semantic)
└── Volume: ~3% of fresh (97% lost to abstraction)

SUBSTRATE (1-6 months)
├── Behavioral patterns distilled into embeddings
├── Patterns that recurred across many sessions get weight
├── Patterns that appeared once fade to near-zero
├── Storage: Vectorize (permanent collection)
└── Volume: ~0.5% of fresh (survival of the persistent)

GEOLOGICAL (6+ months)
├── Substrate embeddings that have proven consistently useful
├── Folded into the base model's context or system prompt
├── No longer tracked as individual records
├── The island has absorbed them. They are stone now.
└── Volume: ~0.01% of fresh (only the most persistent signal survives)
```

### Design Principles

**Log everything; keep almost nothing.** The system records all output at the FRESH tier without judgment. But the decay pipeline is relentless. After 24 hours, most individual records are gone — replaced by statistical ghosts. After a week, even the statistics have been abstracted into patterns. The system's memory is always partial, always accumulating, always slightly different from what it was last cycle.

**Decay is irreversible (with one exception).** Once a record has composted from FRESH to COMPOSTING, the original detail is gone. This is by design — the system that preserves everything drowns in its own accumulated guano. The exception: anomalies flagged during composting are preserved as full entries. These are the bones in the guano — the fish bones that tell future archaeologists what the colony was eating. Anomalous behavior, unexpected successes, catastrophic failures: these survive the decay because they are the signal that the patterns don't capture.

**Decay is observable.** The system tracks what was lost, not just what was kept. A dashboard shows: "This week, 2.3M log entries decayed into 340 behavioral patterns, 12 of which were promoted to substrate embeddings." This makes the decay visible and auditable without making it reversible.

### Implementation

```
[Cron: every hour]
  → Scan FRESH records older than 24h
  → Compress into session summaries (COMPOSTING)
  → Flag anomalies for preservation
  → Delete individual FRESH records

[Cron: daily]
  → Scan COMPOSTING records older than 7 days
  → Extract behavioral patterns (SOIL)
  → Generate Vectorize embeddings for novel patterns
  → Delete COMPOSTING records

[Cron: weekly]
  → Scan SOIL patterns older than 4 weeks
  → Evaluate recurrence across sessions
  → Promote high-recurrence patterns to SUBSTRATE
  → Demote single-occurrence patterns (delete)

[Cron: monthly]
  → Scan SUBSTRATE embeddings older than 3 months
  → Evaluate utility (were they accessed? did they improve outcomes?)
  → Promote consistently useful embeddings to GEOOLOGICAL
  → Fold into system prompt / base context
```

---

## 3. The Claw Marks (Trained Weights)

### Biological Model

Claw marks are the marks left by repeated use on a substrate that doesn't reset. Puffins gripping the same stone for centuries wear grooves into basalt. Each individual mark is small, unremarkable, even invisible. But together, over time, they change the shape of the stone permanently. The stone doesn't record the bird. The stone *is shaped by* the bird. The mark and the substrate become inseparable.

### Technical Specification

Claw Marks are accumulated modifications to shared model parameters — fine-tuning weights, LoRA adapters, prompt evolution, tool configuration drift. These are not logs of what happened. They are changes to the system's fundamental shape, caused by use, that persist across all future sessions.

```typescript
interface ClawMark {
  markId: string;
  tubeId: string;                    // Where the mark originated
  substrateType: "weights" | "prompt" | "tools" | "config";

  // The mark itself
  modification: LoRAAdapter | PromptPatch | ToolConfigDelta;

  // Depth — how many sessions contributed to this mark
  depth: number;                     // Grows with each reinforcing session
  lastReinforced: timestamp;

  // Reversibility
  erosionRate: number;               // How fast this mark fades without reinforcement
  reversibility: "polished" | "grooved" | "fossilized";
}
```

### Categories

**Polished marks (prompt evolution).** System prompts that have been iteratively refined through use. Each session that uses a prompt successfully reinforces it; each session that fails against it erodes it slightly. Over time, prompts converge toward the shape that fits the colony's usage patterns. This is the landing stone — polished smooth by ten thousand crash-landings.

**Grooved marks (LoRA adapters).** Fine-tuning that accumulates from repeated exposure to domain-specific patterns. A tube that handles Roblox build tasks develops grooves — LoRA weights that make the model slightly better at Lua, slightly better at spatial reasoning, slightly better at the specific patterns of that codebase. Each session adds imperceptibly to the groove. Over months, the groove is deep enough to measure.

**Fossilized marks (config changes).** Configuration modifications that have proven stable across enough sessions to be considered permanent. Tool access patterns, model routing preferences, default behaviors that started as experiments and became conventions. These are the deepest claw marks — the ones that have been reinforced so many times they're effectively geological.

### Design Principles

**Use shapes the substrate.** The system doesn't decide what to fine-tune on. It observes what patterns recur in actual usage and reinforces the weights that correspond to those patterns. This is unsupervised accumulation of domain expertise — the same process that makes a senior engineer better at their specific stack without anyone designing a training program.

**Marks can erode.** A claw mark that isn't reinforced will slowly fade. LoRA weights decay at a rate inversely proportional to their depth — a mark from 100 sessions takes longer to erode than a mark from 3 sessions. This prevents the substrate from accumulating dead grooves from patterns that no longer apply. The island's claw marks from extinct species have been eroding for millennia. The system should do the same.

**No mark is truly permanent.** Even fossilized marks can be revisited. Geological features change — slowly, with great effort, but they change. The system allows manual override of any claw mark, but requires explicit justification. You don't reshape basalt casually.

### Implementation

| Category | Storage | Reinforcement Mechanism |
|----------|---------|------------------------|
| Prompt evolution | D1 (`prompt_history`) + versioned R2 objects | A/B testing: successful sessions reinforce, unsuccessful erode |
| LoRA adapters | R2 (model artifacts bucket) | Background fine-tuning on aggregated session data |
| Config changes | D1 (`config_patches`) | Proposal-based: agent suggests, platform validates, applies after N successes |

---

## 4. The Colony Dialect (Emergent Protocols)

### Biological Model

Puffin calls vary from colony to colony. Each tube cluster develops its own dialect — a vocal tradition passed from parents to chicks without any physical substrate. The dialect isn't stored anywhere. It lives in behavior, in the repeated interactions between birds who share a tube cluster. When the colony splits or merges, the dialect shifts. When a new species arrives, the dialect absorbs new sounds (as the servo harmonic was absorbed). This is cultural memory: the most adaptable and least controllable form of persistence.

### Technical Specification

The Colony Dialect is the emergent communication protocol that develops between agents who share Tubes repeatedly. This is not designed. It is not stored. It emerges from shared context — the accumulated experience of agents who have encountered the same problems, developed the same shorthand, and learned to anticipate each other's behavior.

```typescript
// Note: Colony Dialect is not a stored interface.
// It is an observed phenomenon. These types describe what we OBSERVE,
// not what we store.

interface ColonyDialectObservation {
  clusterId: string;                // Which tube cluster
  observedPatterns: EmergentPattern[];

  // Examples of emergent protocol elements:
  // - Shorthand: agents who share a tube use shorter prompts
  //   because they share context
  // - Tool sequences: certain tool call orders become conventional
  //   without being prescribed
  // - Error conventions: agents develop shared vocabulary for
  //   describing failures ("salmon schooling wrong" = unexpected
  //   output from tool X)
  // - Routing signals: agents learn which tubes handle which
  //   problems based on past co-occupation
}

interface EmergentPattern {
  patternSignature: string;         // Hash of the behavioral pattern
  firstObserved: timestamp;
  frequency: number;                // How often it appears
  persistenceScore: number;         // Is it getting stronger or fading?
  originTube: string;               // Where it first appeared
  spreadTo: string[];               // Other tubes where it's appeared
}
```

### Design Principles

**Don't store the dialect; store the conditions for it.** You cannot write a colony's dialect to a database and read it back. If you try, you get a frozen artifact that kills the living tradition. Instead, preserve the conditions that allow dialects to form:

1. **Tube clustering.** Agents that share tube clusters (similar shape, similar tools, overlapping memory bindings) will naturally develop shared shorthand. The platform should group related tubes into clusters — physically, in terms of shared infrastructure — so that agents encounter each other's behavioral residue.

2. **Context leakage (controlled).** When an agent inhabits a tube, it should be able to sense the shape modifications left by previous inhabitants. Not their specific outputs — those have decayed — but the *wear patterns*. An agent that finds deep grooves in a tube's tool access patterns will naturally follow those grooves, producing behavior consistent with the colony's conventions without being told what those conventions are.

3. **Observation, not enforcement.** The platform should observe emergent dialects and make them visible — to operators, to the agents themselves, to the design process — but it should never enforce them. Dialects that are useful persist. Dialects that aren't die. That's the right mechanism.

**Detect dialect formation.** The system monitors for emergent patterns:
- N-gram analysis on agent prompts within a tube cluster (detects shorthand formation)
- Tool call sequence clustering (detects conventional workflows)
- Cross-session behavioral similarity metrics (detects when agents are "speaking the same language")

When a dialect is detected, the system notes it. It does not act on it. The observation is the output.

### Implementation

This layer has minimal infrastructure because the dialect doesn't live in infrastructure. It lives in behavior.

| Component | Mechanism |
|-----------|-----------|
| Tube clustering | D1 tube metadata: group by `tubeShape` similarity |
| Context sensing | Shape modifications (Section 1) are visible to new inhabitants |
| Dialect detection | Background job: behavioral similarity analysis on session records |
| Dialect visualization | Dashboard: "What dialects have formed? Where? How strong?" |

---

## 5. The Breeding Cycle (Agent Reproduction)

### Biological Model

When a puffin chick fledges, it leaves the tube and flies directly to sea. It doesn't return for three to five years. When it returns, it doesn't return to its birth tube — it finds a tube of its own, influenced by but not identical to the one it grew up in. What does it inherit? Not the tube. Not the guano. Not the claw marks. It inherits *behavior* — the foraging patterns, the mating calls, the predator responses that its parents demonstrated. Genetic inheritance (instincts, physiology) plus memetic inheritance (learned behaviors, dialect features, feeding routes).

### Technical Specification

Agent reproduction is the spawning of a new agent by an existing one — a senior agent creating a junior for a specific task. The question is: what does the senior pass on?

```typescript
interface AgentReproduction {
  parentAgentId: string;
  childAgentId: string;

  // GENETIC: Hardcoded, structural inheritance
  genetic: {
    modelConfig: ModelConfig;       // Same base model or derivative
    tubeShape: TubeShape;           // Similar tube properties
    basePrompt: string;             // Foundation prompt (the "instinct")
    toolRegistry: ToolRegistry;     // Access to the same toolset
  };

  // MEMETIC: Learned, behavioral inheritance
  memetic: {
    clawMarks: ClawMark[];          // Relevant trained weights/adapters
    colonyDialect: DialectSignal;   // Tube cluster assignment
    learnedPatterns: BehavioralPattern[]; // Relevant SOIL-tier patterns
    shapeModifications: Patch[];    // Parent's tube shape, as starting point
  };

  // NOT INHERITED: What the child doesn't get
  excluded: {
    sessionMemory: null;            // No access to parent's session history
    personalContext: null;          // No personal/relationship data
    fossilizedMarks: null;          // Geological features are platform-level
  };
}
```

### Genetic vs. Memetic

**Genetic inheritance** is structural and guaranteed. The child agent inherits:
- The same base model (or a specified derivative)
- A tube shape compatible with the parent's
- The foundation prompt — the base system instructions that define what kind of agent this is
- Access to the same toolset

This is instinct. The puffin chick knows how to fish before it's ever fished, because forty thousand years of evolution have wired fishing into its nervous system. The child agent knows how to use tools before it's ever used them, because its prompt and model config provide the same capability.

**Memetic inheritance** is behavioral and selective. The parent chooses what to pass on:
- Relevant claw marks (LoRA adapters, prompt patches that apply to the task)
- Colony dialect assignment (which tube cluster to join)
- Learned behavioral patterns from the SOIL tier (what worked, what didn't)
- Shape modifications as a starting template (the parent's tube wear, which the child can adapt)

This is learning. The puffin chick learned specific foraging routes by following its parents. The child agent inherits the parent's accumulated expertise in a specific domain — but only the expertise relevant to the task it's being spawned for.

**Excluded by design.** The child does not inherit:
- The parent's session history (no reading old conversations)
- Personal context (no relationship data, no private memory)
- Fossilized marks (geological features belong to the platform, not individual agents)

This mirrors the puffin breeding model: the chick gets genetics and learned behaviors, but it doesn't get its parents' specific memories. It doesn't know which fish were caught on which day. It knows *how to fish*, and it knows *where its parents fished*, but it has to discover its own fishing grounds.

### Design Principles

**Reproduction is expensive.** Puffins lay one egg per season. The investment per chick is enormous. Agent reproduction should be similarly deliberate — not spawning dozens of disposable agents, but carefully constructing a child with the right genetic and memetic inheritance for the task. This is not a technical limitation. It's a design principle that forces intentionality.

**Children diverge from parents.** The child agent's first action should be exploration — discovering its own patterns, making its own mistakes, finding its own tube. The parent provides the starting point, not the destination. If children perfectly replicate parents, the system stagnates (Hawaii syndrome). If children diverge too far, expertise is lost. The balance is struck by giving children strong genetic inheritance and selective memetic inheritance, then letting them develop their own claw marks.

**Reproduction is logged but not controlled.** The system records every reproduction event — who spawned whom, what was inherited, what the task was. But it doesn't restrict reproduction beyond the genetic limits (model availability, tube availability). Agents reproduce when their operators tell them to. The system ensures clean inheritance and then gets out of the way.

---

## 6. Map to Slackwater

The Slackwater platform is the island. Its infrastructure is the geology. Here's how the persistence layers map to actual components.

### Tubes → Agent Runtime Configuration

| St. Lazaria | Slackwater Component | Details |
|-------------|---------------------|---------|
| Lava tube | Agent session config (D1 `tubes` table) | Context window, model config, tool access, memory bindings |
| Tube shape | Wrangler config + runtime bindings | The "geology" that determines what agent can inhabit |
| Shape modifications | D1 `tube_patches` append-only log | Cumulative wear from usage patterns |
| Tube clustering | D1 similarity queries | Group tubes by shape for colony dialect formation |
| Fossilized tubes | D1 `tubes` WHERE `cleanliness = 'fossilized'` | Queryable history, not assignable |

### Guano → Session Output Decay Pipeline

| St. Lazaria | Slackwater Component | Details |
|-------------|---------------------|---------|
| Fresh guano | R2 ephemeral bucket (24h TTL) | Full logs, every tool call, every token |
| Composting guano | R2 warm bucket → D1 session summaries | Statistical aggregates, anomaly preservation |
| Soil | D1 `behavioral_patterns` table + Vectorize | Extracted patterns, embeddings |
| Substrate | Vectorize (permanent collection) | High-recurrence patterns with semantic search |
| Geological | System prompt / base context | Patterns folded into platform baseline |
| Decay cron | Cloudflare Cron Triggers | Hourly, daily, weekly, monthly decay jobs |

### Claw Marks → Model Evolution

| St. Lazaria | Slackwater Component | Details |
|-------------|---------------------|---------|
| Polished marks (prompt evolution) | D1 `prompt_history` + versioned R2 prompt objects | A/B tested, reinforced by success |
| Grooved marks (LoRA adapters) | R2 model artifacts bucket | Background fine-tuning on aggregated session data |
| Fossilized marks (config) | D1 `config_patches` | Proposal-based, validated before application |
| Erosion | Background job: decay unused weights | Inversely proportional to depth |

### Colony Dialect → Emergent Protocol Detection

| St. Lazaria | Slackwater Component | Details |
|-------------|---------------------|---------|
| Colony calls | Observed in session records (not stored as dialect) | N-gram analysis detects shorthand formation |
| Dialect spread | Cross-tube behavioral similarity metrics | Dashboard: dialect strength by cluster |
| Cultural absorption | Shape modifications visible to new inhabitants | Agents sense previous usage patterns |

### Breeding Cycle → Subagent Spawning

| St. Lazaria | Slackwater Component | Details |
|-------------|---------------------|---------|
| Genetic inheritance | Model config + tool registry + base prompt | Hardcoded at spawn time |
| Memetic inheritance | Claw marks + patterns + shape modifications | Selectively passed by parent |
| Excluded by design | Session memory, personal context, fossilized marks | Clean separation between agent and platform |
| Reproduction log | D1 `agent_reproductions` table | Full audit trail |

### The 200-Repo Ecosystem

The 200-repo ecosystem is the archipelago — not one island but many, each with its own tubes, its own colonies, its own dialects. The persistence layer is designed to work *across* repositories:

- **Tubes** can reference tools and models from any repo. A tube's shape is not limited to one codebase.
- **Guano** decays into substrate embeddings that are stored centrally (Vectorize), accessible by any agent in any tube on any island.
- **Claw marks** (LoRA adapters, prompt patches) can be shared between repos through R2. An adapter trained in the Lucineer repo can be applied in the Slackwater repo.
- **Colony dialects** form within tube clusters regardless of which repo the tubes belong to. Two agents working on related problems in different repos will naturally develop shared shorthand.
- **Breeding** can cross repo boundaries. A Lucineer agent can spawn a child that works in a Slackwater tube, carrying memetic inheritance from the parent's domain.

The islands are connected by ocean. The ocean is the network. Each island is shaped by its own geology, but the birds move between them, carrying genes, dialects, and behaviors across the water. The archipelago is the system. No single island is the system.

---

## Summary: What the Puffins Teach Us About Persistence

| Layer | Half-Life | Storage | Decay Mechanism | Survives Across |
|-------|-----------|---------|-----------------|-----------------|
| Tube (session config) | Indefinite (fossilizes after 90 days unused) | D1 | Shape modifications persist; active context flushed | Sessions, model upgrades |
| Guano (ephemeral output) | Hours → months (tiered) | R2 → D1 → Vectorize | Tiered decay: detail → statistics → patterns → embeddings → baseline | Nothing (by design — it becomes the substrate) |
| Claw Marks (trained weights) | Months → permanent | R2 (adapters) + D1 (prompt history) | Erosion without reinforcement | Model upgrades (LoRA is portable) |
| Colony Dialect (emergent) | Variable — persists while useful | Not stored (observed) | Dies when agents stop using it | Sessions within a tube cluster |
| Breeding (reproduction) | One-shot transfer | D1 (reproduction log) | N/A — inheritance happens at spawn time | Parent → child (one generation) |

The puffins have survived forty thousand years not because they remember everything, but because they remember the right things at the right timescales. Their tubes persist. Their guano becomes soil. Their claw marks deepen. Their dialects shift. Their chicks inherit instinct and behavior, then find their own tubes.

Build a persistence layer that does the same. Not a database that stores everything forever. Not an amnesiac that forgets everything on session end. A layered system where each type of memory has its own physics, its own decay curve, and its own relationship to the agents that produce it.

The island doesn't manage the puffins' memory. The island *is* the memory.

Be the island.

---

*Design doc for the Slackwater/Lucineer platform. Informed by "The Persistent Memory" by Casey DiGennaro and the St. Lazaria platform essays. Written in the understanding that the most persistent systems are not the ones that remember the most — they are the ones that forget at the right rate.*
