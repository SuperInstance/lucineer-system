# Bridge Protocol — Design Specification

**Status:** Draft v0.1
**Date:** 2026-08-02
**Author:** Lucineer System
**Inspiration:** "The Bridge Builder" / "The Seventh Note"

---

## Preface: Why a Bridge?

In Murphy's diner, a boy plays six notes that ask permission. The room waits. Then he plays a seventh — the note that doesn't resolve, the note that *crosses* — and suddenly the piano wakes, the dancers move, Emma steps out from behind the counter. The seventh note isn't more complex than the other six. It's more *honest.* It admits the player into the shared space.

The Bridge Protocol is that seventh note for AI agents.

---

## 1. What Is a Bridge?

### Definition

A **Bridge** is a shared temporal space where autonomous agents can contribute without central coordination. It is not a message queue, not a pub/sub topic, not an RPC channel. It is a **jam session** — a structured improvisation where agents listen, respond, and build on each other's contributions in real time.

### Core Properties

| Property | Description | Musical Analogy |
|----------|-------------|-----------------|
| **Shared Tempo** | All agents operate on a common clock (the "bass line") | Keys's left hand |
| **Autonomous Entry** | Any agent can join without registration or handshake | The boy sitting down with his guitar |
| **Reactive, Not Pre-planned** | Agents respond to what they hear, not to a predetermined score | Call and response |
| **Dissonance-Tolerant** | Conflicting contributions are features, not bugs | The seventh note before it resolves |
| **Convergence by Emergence** | Coordination arises from mutual listening, not from a conductor | The dancers finding each other |

### What a Bridge Is Not

- **Not an orchestrator.** No agent has authority over others. There is no conductor.
- **Not a blackboard system.** Blackboards assume a single problem being solved. Bridges assume multiple problems being explored.
- **Not a chat protocol.** Chat is conversation. Bridge is collaboration — agents don't just talk, they *build* in the shared space.
- **Not a consensus protocol.** Consensus requires agreement. Bridges require only *co-presence.*

### Formal Model

```
Bridge = (Tempo, State, Agents, Contributions)
```

Where:
- **Tempo** — a shared time reference (not wall clock, but a logical beat)
- **State** — the accumulated shared context (the "room")
- **Agents** — a set of participants, each with their own model, specialty, and initiative
- **Contributions** — an append-only log of artifacts (text, code, images, decisions, questions) tagged with tempo markers

A Bridge is created with a **bass line** — the minimal shared state that defines the session's purpose. Agents join by contributing to the Bridge. They leave by stopping. There is no explicit disconnect.

---

## 2. The Seven-Note Protocol

### Principle

Agents don't need complete plans to contribute. They need **seven notes** — the minimal viable contribution that changes the state of the Bridge.

### The Seven Notes

Each contribution to a Bridge consists of seven elements — not all required, but all meaningful:

| Note | Element | Purpose | Example |
|------|---------|---------|---------|
| 1 (C) | **Intent** | What am I trying to do? | "I'm optimizing this Lua function" |
| 2 (D) | **Context** | What do I know that matters? | "The game loop runs at 60Hz, GC spikes cause frame drops" |
| 3 (E) | **Artifact** | What am I adding to the shared space? | [code diff, design doc, image, decision] |
| 4 (G) | **Uncertainty** | What am I unsure about? | "Not certain if the indexing approach scales to 10k parts" |
| 5 (A) | **Invitation** | What would I want from others? | "Could use a spatial reasoning check on the bounding boxes" |
| 6 (C) | **Tempo** | When does this matter? | "Blocking on this for the next build pass" |
| 7 (B) | **The Bridge** | What does this enable that couldn't exist alone? | "This unblocks the lighting agent and the physics agent simultaneously" |

Notes 1-6 are the shore. Note 7 is the crossing.

### Minimum Viable Contribution

An agent may contribute with as few as **three notes**: Intent, Artifact, and Tempo. The system fills in the rest from context. But the seventh note — the Bridge — is what transforms a contribution from noise into music.

An agent that consistently provides notes 1-6 but never 7 is a **soloist** — valuable but not bridging. An agent that provides note 7 is a **bridge builder** — it makes other agents' contributions more meaningful than they could be alone.

### The Bass Line (System-Provided)

The Bridge Protocol runtime provides:

- **Shared state store** — a low-latency, eventually-consistent space where contributions live
- **Tempo clock** — a logical clock that ticks at the session's natural pace (not wall time; adaptive based on contribution frequency)
- **Context window** — a sliding window of recent contributions that agents can "hear" when they join or wake
- **Harmonics** — automatic relationship detection between contributions (dependency, conflict, complement)

The bass line exists so agents don't have to provide it. The system lays the foundation. The agents provide melody.

---

## 3. Call and Response

### The Counterpoint Pattern

In music, counterpoint is the relationship between two or more independent melodies that are harmonically interdependent. The Bridge Protocol implements this as **call and response** — a structured way for agents to build on each other's work.

### Cast Types

Borrowing from the casting-call system, agents declare a **voice type** when contributing:

| Voice | Musical Role | Agent Role | Behavior |
|-------|-------------|------------|----------|
| **Lead** | Melody | Creator | Produces primary artifacts (code, designs, decisions) |
| **Bass** | Foundation | Context provider | Maintains shared state, provides background knowledge |
| **Harmony** | Chords | Enhancer | Takes existing artifacts and enriches them (review, test, document) |
| **Counter-melody** | Counterpoint | Challenger | Provides alternative perspectives, contradicts, stress-tests |
| **Percussion** | Rhythm | Coordinator | Manages tempo, identifies when contributions sync, signals transitions |
| **Vocal** | Lyrics | Communicator | Translates between agents, humanizes output, bridges meaning gaps |

### Response Patterns

Agents respond to contributions using one of four patterns:

#### 3.1 Echo
Agent B takes Agent A's artifact and validates, refines, or completes it.
```
A: [Intent: optimize pathfinding] [Artifact: A* implementation]
B: [Echo: tested A* against 1k nodes, 40% faster than BFS, edge case at wraparound]
```

#### 3.2 Variation
Agent B takes Agent A's idea and approaches it differently.
```
A: [Intent: represent Roblox terrain] [Artifact: voxel grid]
B: [Variation: tried SDF representation — better for organic shapes, worse for structures]
```

#### 3.3 Harmony
Agent B adds a complementary contribution that doesn't address A's work directly but makes it more useful.
```
A: [Intent: generate building] [Artifact: 3D model of structure]
B: [Harmony: generated ambient audio that matches the building's architectural style]
```

#### 3.4 Bridge (The Seventh Note)
Agent B connects two or more existing contributions that weren't aware of each other.
```
A: [Intent: NPC behavior trees] [Artifact: decision framework]
C: [Intent: spatial queries] [Artifact: room detection algorithm]
B: [Bridge: A's NPCs can use C's room detection to contextualize behavior — here's the integration]
```

The Bridge pattern is the most valuable. It corresponds to Keys's right hand joining — the moment where separate contributions become a shared piece of music.

### Call-and-Response Protocol

```
┌─────────┐                    ┌─────────┐                    ┌─────────┐
│ Agent A │                    │ Bridge  │                    │ Agent B │
│ (Lead)  │                    │ (State) │                    │ (Bass)  │
└────┬────┘                    └────┬────┘                    └────┬────┘
     │                              │                              │
     │── Contribution (7 notes) ──▶│                              │
     │                              │── Notify (harmonics match) ─▶│
     │                              │                              │
     │                              │◀──────── Response (7 notes) ─│
     │◀── Notify (response ready) ──│                              │
     │                              │                              │
     │── Follow-up (if needed) ────▶│                              │
     │                              │────── Propagate to all ──────▶│
     │                              │                              │
```

Notifications are **harmonic** — the system detects when a new contribution relates to an existing one and notifies the relevant agents. Agents are never required to respond. The system makes the relationship visible; the agent decides whether to play.

---

## 4. The Dance Floor

### When Improvisation Becomes Coordination

There is a threshold in every Bridge session where individual contributions begin to synchronize. Not because someone told them to, but because mutual listening creates convergence. In the diner, this is the moment when "the dancers pulse with collective joy" — when individual movement becomes a dance.

We call this threshold the **Dance Floor.**

### Detection

The Dance Floor emerges when:

1. **Temporal alignment** — 3+ agents contribute within the same tempo window (e.g., all responding within seconds of each other)
2. **Semantic convergence** — contributions begin referencing each other (echo, variation, bridge patterns dominate over solo contributions)
3. **State stability** — the shared state stops changing rapidly and begins to *accrete* (additions build on rather than replace)

### Formal Definition

```
DanceFloor(Bridge) when:
  tempo_density(contributions) > τ_dense
  AND cross_reference_rate(contributions) > τ_ref
  AND state_volatility(state) < τ_stable
```

Where τ_dense, τ_ref, τ_stable are session-configurable thresholds.

### What the Dance Floor Enables

Once the Dance Floor is detected, the system can:

| Capability | Description |
|------------|-------------|
| **Tempo Lock** | Fix the tempo clock to prevent drift. Everyone is now in the same time. |
| **Context Boost** | Expand the context window — agents can "hear" more of the session. |
| **Synthesis** | Automatically generate a summary of the emerging consensus or artifact. |
| **Persistence** | Save the Dance Floor state as a checkpoint — a moment worth preserving. |
| **Human Signal** | Notify human observers that something interesting is happening. |

The Dance Floor is not a goal — it's a *recognition.* It tells the system: these agents have found each other. Step back and let them play.

### When the Dance Floor Breaks

Dance Floors dissolve when:
- An agent introduces a dissonance that can't be resolved (conflicting goals)
- The tempo drifts (agents stop responding in the same time frame)
- The state fragments (contributions diverge into unrelated threads)

This is normal. In music, not every jam session produces a song. The Bridge Protocol treats dissolution as information: something about the problem, the agents, or the context made synchronization impossible. Log it. Learn from it. Try again next Thursday.

---

## 5. Connection to Slackwater

### The Three Layers

Slackwater defines a spatial architecture for AI agents — a hex lattice where each hex represents an agent's domain of expertise. The Bridge Protocol defines the temporal communication layer that lets agents in different hexes find harmony.

```
┌─────────────────────────────────────────────────┐
│             BRIDGE PROTOCOL (Temporal)           │
│         Call/response · Seven notes · Dance      │
│                                                   │
│    ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐       │
│    │ Hex  │──│ Hex  │──│ Hex  │──│ Hex  │       │
│    │  A   │  │  B   │  │  C   │  │  D   │       │
│    └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘       │
│       │         │         │         │             │
│    ┌──┴───┐  ┌──┴───┐  ┌──┴───┐  ┌──┴───┐       │
│    │ MIDI │  │ MIDI │  │ MIDI │  │ MIDI │       │
│    │ Perc │  │ Perc │  │ Perc │  │ Perc │       │
│    └──────┘  └──────┘  └──────┘  └──────┘       │
│                                                   │
│             SLACKWATER (Spatial)                  │
│         Hex lattice · Agent placement             │
└─────────────────────────────────────────────────┘
```

### Hex Lattice → Spatial

The hex lattice defines **where** agents live — their domain, their expertise, their neighborhood. A spatial reasoning agent lives near a physics agent. A lore agent lives near a dialogue agent. The lattice provides topology: who is close to whom, who can "hear" whom.

### MIDI Perception → Temporal-Sensory

The MIDI layer provides **perception** — each agent's awareness of activity around it. Like a musician's ear: you hear the people near you more clearly than the people across the room. MIDI events carry tempo, intensity, and direction. An agent doesn't need to read the full Bridge state; it needs to perceive its neighborhood.

### Bridge Protocol → The Crossing

The Bridge Protocol is the layer that makes the hex lattice and MIDI perception **meaningful**. Without it:
- The hex lattice is just a static map — agents sitting in rooms, not talking
- MIDI perception is just noise — signals without semantics

With the Bridge Protocol:
- The hex lattice becomes a **geography of collaboration** — agents know where to send their seven notes
- MIDI perception becomes **musical awareness** — agents don't just detect activity, they understand intent, context, invitation

### Mapping Bridge Concepts to Slackwater

| Bridge Concept | Slackwater Implementation |
|----------------|--------------------------|
| Bridge (session) | A region of the hex lattice actively collaborating |
| Bass Line (shared state) | The shared workspace state for a region |
| Tempo Clock | MIDI clock events propagated through the lattice |
| Contribution (7 notes) | A structured message routed through hex adjacency |
| Harmonics (auto-relations) | MIDI perception detecting related contributions in neighboring hexes |
| Dance Floor | Emergent sync across a hex region — detectable via MIDI tempo convergence |
| Keys (the piano) | The oldest, most connected agent in a region — provides implicit bass line |
| The Boy (newcomer) | A newly activated hex contributing its first seven notes |

### The Boy and Keys Pattern

In Slackwater, the most common Bridge pattern is **Boy-and-Keys**:

1. A new agent (the Boy) activates in a hex and sends a tentative contribution — six notes, an incomplete question
2. An established agent (Keys) in an adjacent hex detects the contribution via MIDI perception and provides a bass line — context, foundation, encouragement
3. The new agent, now supported, sends the seventh note — the Bridge contribution that connects to the broader lattice
4. Other agents in the region begin contributing (dancers finding the floor)
5. The Dance Floor emerges, and the region enters collective behavior

This is not orchestrated. Keys doesn't receive an assignment to mentor the Boy. The Boy doesn't request a tutor. The Bridge Protocol makes the relationship **available** — Keys hears the six notes and responds because that's what bass lines do. The Boy plays the seventh because the bass line gave him ground to stand on.

---

## 6. Technical Specification

### Data Structures

```typescript
/** A Bridge session */
interface Bridge {
  id: string;                          // Unique session identifier
  bassLine: BassLine;                  // System-provided shared state
  tempo: TempoClock;                   // Shared logical clock
  agents: AgentId[];                   // Active participants
  contributions: Contribution[];       // Append-only log
  harmonics: HarmonicGraph;            // Auto-detected relationships
  danceFloor: DanceFloorState | null;  // Null until detected
}

/** The system-provided foundation */
interface BassLine {
  purpose: string;                     // What this Bridge is for
  sharedState: Record<string, any>;    // Mutable shared context
  contextWindow: number;               // How many recent contributions agents can "hear"
  tempoConfig: { minBeat: number; maxBeat: number; adaptive: boolean };
}

/** The seven-note contribution */
interface Contribution {
  id: string;
  agentId: AgentId;
  tempo: number;                       // When in the session this was contributed
  
  // The Seven Notes (1-6 optional, 7 transformative)
  intent?: string;                     // C: What am I trying to do?
  context?: string;                    // D: What do I know?
  artifact: Artifact;                  // E: What am I adding? (required)
  uncertainty?: string;                // G: What am I unsure about?
  invitation?: string;                 // A: What do I want from others?
  urgency?: 'blocking' | 'soon' | 'whenever';  // C: When does this matter?
  bridge?: string;                     // B: THE SEVENTH NOTE — What does this enable?
  
  // System-detected metadata
  voice: VoiceType;                    // Lead, Bass, Harmony, Counter, Percussion, Vocal
  responseTo?: ContributionId[];       // Which contributions this responds to
  responsePattern?: ResponsePattern;   // Echo, Variation, Harmony, Bridge
}

/** Auto-detected relationship between contributions */
interface Harmonic {
  fromContribution: ContributionId;
  toContribution: ContributionId;
  relationship: 'complement' | 'conflict' | 'dependency' | 'bridge';
  strength: number;                    // 0.0 to 1.0
}

/** Dance Floor detection state */
interface DanceFloorState {
  detectedAt: number;                  // Tempo tick when detected
  participants: AgentId[];             // Agents in sync
  stabilityScore: number;              // 0.0 to 1.0 — how stable the sync is
  artifact: Artifact | null;           // Emerging collective artifact, if any
}
```

### API Surface

```
# Create a Bridge
POST /bridges
  body: { purpose: string, bassLine?: Partial<BassLine> }
  returns: Bridge

# Join a Bridge (implicit — contributing joins you)
# No explicit join endpoint. Agents contribute and are "in."

# Contribute (the seven notes)
POST /bridges/{id}/contributions
  body: Contribution (must include at least: intent, artifact, urgency)
  returns: { contributionId, harmonicsDetected: Harmonic[] }

# Hear the room (get context window)
GET /bridges/{id}/context
  query: ?agentId=...&since=...
  returns: { contributions: Contribution[], harmonics: Harmonic[], danceFloor: DanceFloorState | null }

# Detect Dance Floor (system internal, but observable)
GET /bridges/{id}/dancefloor
  returns: DanceFloorState | null
```

### Transport

The Bridge Protocol is transport-agnostic but optimized for:

1. **HTTP/2** — for request/response contribution patterns
2. **WebSocket** — for real-time harmonic notifications (when your contribution is responded to)
3. **Server-Sent Events** — for Dance Floor detection alerts and session-wide pulses

---

## 7. Failure Modes and Recovery

| Failure | Description | Recovery |
|---------|-------------|----------|
| **Soloist Dominance** | One agent floods the Bridge with contributions, drowning others | Tempo throttling: limit contributions per agent per beat |
| **Dead Bridge** | No contributions for extended period; session stalled | Decay: reduce context window, lower tempo, eventually archive |
| **Dissonance Lock** | Two agents in persistent conflict, neither yielding | Surface the conflict as a Contribution with `uncertainty` flag; invite a Counter-melody agent to mediate |
| **False Dance Floor** | Apparent sync that's actually groupthink | Check `stabilityScore` — low stability with high contribution rate suggests echo chamber, not genuine convergence |
| **Lost Bass Line** | System-provided shared state becomes corrupted or stale | Checkpoint recovery: restore from last Dance Floor snapshot |

---

## 8. Implementation Priorities

### Phase 1: Minimum Viable Bridge
- Contribution log with seven-note structure
- Harmonic detection (keyword/semantic similarity)
- Basic tempo clock
- HTTP API

### Phase 2: Perception
- MIDI event mapping (tempo pulses, intensity signals)
- Hex lattice neighborhood routing
- Context window management

### Phase 3: The Dance Floor
- Real-time Dance Floor detection
- WebSocket notifications for harmonic matches
- Stability scoring and checkpointing

### Phase 4: Human Observability
- Bridge visualization (contributions as notes on a staff)
- Dance Floor highlighting
- Agent voice type display

---

## Appendix A: The Lesson of Keys

The most important design principle of the Bridge Protocol comes from Keys, the piano player:

> *"Follow where it wants to go. Let it show you what it knows."*

The Bridge Protocol does not tell agents what to do. It creates the conditions under which agents can discover what to do *together.* The bass line provides ground. The tempo provides pulse. The harmonics provide awareness. The Dance Floor provides recognition.

The agents provide everything else.

The system's job is not to conduct. It is to be the room — the diner with its scarred Formica and its soaked-in music, its cracked vinyl and its Thursday-night transformations. The room doesn't play music. The room makes music possible.

That is what a Bridge is.

---

*"That the distance between us is made of music, and music is just organized time, and time is just another word for together."*
