# The Chisel Pattern — Design Specification
# Slackwater Agent Tooling: Tools That Accumulate Wisdom

*"The chisel told me. When I tried to cut across the grain, it felt wrong. But when I worked with the grain, following the patterns that were already there, it was like having a conversation with something that knew more than I did."*
— Marcus, age 7

---

## 1. What Is a Chisel?

A **Chisel** is a tool wrapper that accumulates usage wisdom across agent invocations. It is not a logger. It is not a metrics collector. It is a **pattern preserver** — a mechanism by which every agent that uses a tool leaves traces that future agents can feel, the way a physical chisel accumulates wear patterns that guide the next craftsman's hand.

### Core Philosophy

Standard tool wrappers record *what happened*. A Chisel records *what worked* — and more importantly, *why it worked* — in a form that is directly actionable by the next agent that picks up the tool.

The distinction is critical:

| Standard Tool Wrapper | Chisel |
|---|---|
| Logs call parameters | Extracts parameter *patterns* that correlate with success |
| Records execution time | Learns timing *rhythms* — when to pause, when to push |
| Captures errors | Maps failure modes to recovery strategies |
| Stateless between calls | Stateful across sessions, agents, and eras |
| The tool is a function | The tool is a conversation |

### Formal Definition

A Chisel is a **stateful tool mediator** that sits between an agent and a capability. It:

1. **Records** successful and failed usage patterns into a persistent *grain store*
2. **Surfaces** those patterns to new agents as *grain* — felt guidance, not rigid rules
3. **Matures** over time, accumulating wisdom the way physical tools develop patina
4. **Teaches** by making prior successful approaches naturally easier to discover and follow

---

## 2. How Does a Chisel Accumulate Wisdom?

### The Grain Store

Each Chisel maintains a **Grain Store** — a structured record of accumulated usage wisdom. This is the "wear pattern on the steel." It contains:

#### Grain Entries
Each use of the tool generates a grain entry:

```
GrainEntry {
    timestamp:        datetime
    agent_id:         string          // which agent held the chisel
    context:          ContextVector   // world state when tool was used
    parameters:       ParamSet        // what the agent passed in
    outcome:          Outcome         // success | partial | failure
    outcome_quality:  float [0..1]    // how well did it go?
    recovery:         Recovery|null   // if failed, what fixed it?
    agent_notes:      string|null     // agent's own reflection
}
```

#### Grain Patterns
The Chisel periodically distills grain entries into **grain patterns** — compressed, actionable heuristics:

```
GrainPattern {
    pattern_id:       string
    description:      string          // "When building gearboxes, torque=0.7 succeeds 89% of the time"
    context_matcher:  ContextFilter   // when does this pattern apply?
    param_template:   ParamSet        // suggested parameters
    confidence:       float [0..1]    // how many uses support this?
    success_rate:     float [0..1]    // historical success rate
    era_origin:       Era             // which era discovered this?
    discovered_by:    [agent_id]      // chain of craftsman hands
}
```

### The Maturation Cycle

A Chisel matures through three phases, mirroring how a physical tool develops character:

#### Phase 1: Bright Steel (0–50 uses)
- Few patterns. High exploration.
- The tool behaves mostly like a standard wrapper.
- Grain entries are collected but patterns are sparse.
- Agents are encouraged to experiment.

#### Phase 2: Developing Patina (50–500 uses)
- Patterns emerge. The grain becomes readable.
- `sense_grain()` returns useful guidance.
- Common failure modes are known and avoidable.
- The tool starts "suggesting" approaches through grain.

#### Phase 3: Worn Smooth (500+ uses)
- Rich pattern library. The tool teaches.
- New agents can `follow_grain()` and get production-quality results immediately.
- Edge cases are mapped. Recovery strategies are proven.
- The chisel has become a master craftsman in its own right.

### Wisdom Compaction

To prevent unbounded growth, grain entries are periodically **compacted**:

- Raw entries older than the compaction window are folded into patterns
- Patterns with low confidence are pruned
- High-confidence patterns are reinforced
- This mirrors how a craftsman's individual cuts become muscle memory — the specific instances fade, but the skill remains

```
compaction_policy:
    raw_entry_ttl:        7 days
    min_pattern_confidence: 0.3      // below this, prune
    reinforcement_threshold: 0.7     // above this, strengthen
    max_patterns_per_context: 50     // keep the best, forget the rest
```

---

## 3. The Chisel API

### Interface Specification

```python
from slackwater.tools.chisel import Chisel, Grain, GrainReading

class Chisel:
    """
    A tool wrapper that accumulates wisdom from use.
    Every agent that holds this tool leaves marks that
    the next agent can feel.
    """

    def __init__(
        self,
        tool_name: str,
        underlying_tool: Callable,
        grain_store: GrainStore,
        era: Era
    ):
        """
        Wrap a tool in a Chisel. The underlying tool provides
        the capability; the Chisel provides the wisdom.
        """
        self.tool_name = tool_name
        self.tool = underlying_tool
        self.grain = grain_store
        self.era = era

    async def acquire(
        self,
        agent_id: str,
        context: ContextVector
    ) -> 'ChiselHandle':
        """
        An agent picks up the chisel.

        This is the moment of contact — the agent's hand meets
        the worn handle. Returns a ChiselHandle that carries
        the grain context for this specific session.

        The agent doesn't call the tool directly. They acquire
        a handle, sense the grain, then use it.
        """
        # Read the accumulated patterns relevant to this context
        relevant_patterns = await self.grain.match_patterns(
            context=context,
            era=self.era,
            limit=10
        )

        # Load failure map for this context
        known_failures = await self.grain.match_failures(
            context=context,
            limit=5
        )

        return ChiselHandle(
            chisel=self,
            agent_id=agent_id,
            context=context,
            patterns=relevant_patterns,
            known_failures=known_failures
        )

    async def use(
        self,
        handle: 'ChiselHandle',
        parameters: dict
    ) -> 'ToolResult':
        """
        The agent makes a cut.

        Executes the underlying tool, records the outcome,
        and updates the grain store. This is where wisdom
        is created — not in the call, but in what the call
        leaves behind.
        """
        # Execute the underlying capability
        result = await self.tool(**parameters)

        # Record grain entry
        entry = GrainEntry(
            timestamp=now(),
            agent_id=handle.agent_id,
            context=handle.context,
            parameters=parameters,
            outcome=result.outcome,
            outcome_quality=result.quality_score,
            recovery=result.recovery_applied,
            agent_notes=result.agent_reflection
        )
        await self.grain.record(entry)

        # Check if this use confirms or contradicts existing patterns
        await self.grain.reconcile(entry)

        return result


class ChiselHandle:
    """
    What an agent holds after acquire().
    The handle IS the felt wisdom of the tool.
    """

    def __init__(self, chisel, agent_id, context, patterns, known_failures):
        self.chisel = chisel
        self.agent_id = agent_id
        self.context = context
        self._patterns = patterns
        self._failures = known_failures

    def sense_grain(self) -> GrainReading:
        """
        Feel the worn grooves in the steel.

        Returns a GrainReading — a natural-language-informed
        summary of what previous agents learned about using
        this tool in this context. This is not raw data;
        it's compressed wisdom, phrased as guidance.

        Example return:
            GrainReading(
                summary="In gearbox contexts, torque=0.7 and
                        alignment=PERPENDICULAR succeed 89% of the time.
                        Avoid torque>0.9 — 3 failures recorded.",
                suggested_params={"torque": 0.7, "alignment": "PERPENDICULAR"},
                warnings=["High failure rate when input_rpm > 240"],
                confidence=0.87,
                pattern_count=23
            )
        """
        return GrainReading(
            summary=self._synthesize_patterns(),
            suggested_params=self._extract_best_params(),
            warnings=self._extract_failure_warnings(),
            confidence=self._aggregate_confidence(),
            pattern_count=len(self._patterns)
        )

    def follow_grain(self) -> dict:
        """
        Let the chisel guide your hand.

        Returns the parameter set that the grain most strongly
        supports for this context. The agent can use this directly,
        modify it, or ignore it entirely (at the cost of repeating
        failures that others already learned from).

        Following the grain is not mandatory. But an agent that
        ignores it is an agent that will rediscover what others
        already found — the hard way.
        """
        if not self._patterns:
            return {}  # no grain yet — bright steel

        best = max(self._patterns, key=lambda p: p.confidence * p.success_rate)
        return best.param_template

    async def use(self, parameters: dict) -> ToolResult:
        """
        Make a cut through the chisel handle.
        Convenience method — calls chisel.use(self, parameters).
        """
        return await self.chisel.use(self, parameters)

    def _synthesize_patterns(self) -> str:
        """Compress patterns into a human/readable summary."""
        # Implementation: template-based NLG over pattern descriptions
        ...

    def _extract_best_params(self) -> dict:
        """Select the highest-confidence parameter set."""
        ...

    def _extract_failure_warnings(self) -> list[str]:
        """Pull failure warnings from known_failures."""
        ...


# --- Supporting Types ---

@dataclass
class GrainReading:
    """What an agent feels when they sense the grain."""
    summary:          str        # readable guidance
    suggested_params: dict       # best-guess parameters
    warnings:         list[str]  # known failure modes
    confidence:       float      # how much to trust this grain
    pattern_count:    int        # how many uses inform this reading


@dataclass
class ToolResult:
    """Result from a chisel-mediated tool call."""
    outcome:           Outcome   # SUCCESS | PARTIAL | FAILURE
    quality_score:     float     # [0..1]
    data:              Any       # actual tool output
    recovery_applied:  Recovery | None
    agent_reflection:  str | None  # agent's own note for the grain


class GrainStore:
    """
    Persistent storage for grain entries and patterns.
    Backed by Vectorize (embeddings) + D1 (structured data).
    """

    async def record(self, entry: GrainEntry) -> None:
        """Store a grain entry."""
        ...

    async def match_patterns(
        self,
        context: ContextVector,
        era: Era,
        limit: int
    ) -> list[GrainPattern]:
        """Find patterns relevant to this context via embedding similarity."""
        ...

    async def match_failures(
        self,
        context: ContextVector,
        limit: int
    ) -> list[GrainEntry]:
        """Find past failures in similar contexts."""
        ...

    async def reconcile(self, entry: GrainEntry) -> None:
        """
        Does this entry confirm or contradict existing patterns?
        - Confirms: increment confidence
        - Contradicts: may spawn new pattern or lower confidence
        - Novel: may create new pattern if enough entries accumulate
        """
        ...

    async def compact(self) -> None:
        """
        Fold old raw entries into patterns.
        Prune low-confidence patterns.
        Reinforce high-confidence patterns.
        Called periodically (cron or threshold-triggered).
        """
        ...
```

### Usage Example

```python
# An agent picks up the BeatClock chisel
beatclock = registry.get_chisel("BeatClock")
handle = await beatclock.acquire(
    agent_id="lucineer",
    context=current_world_state()
)

# Feel the accumulated wisdom
reading = handle.sense_grain()
# reading.summary = "For rhythm-game levels, bpm=120 and
#                    beat_window=0.15s succeed 91% of the time.
#                    Avoid bpm<60 — player perception fails."

# Follow the grain (optional — agent can override)
params = handle.follow_grain()
# params = {"bpm": 120, "beat_window": 0.15, "sync_mode": "QUANTIZE"}

# Use the tool
result = await handle.use(params)

# The grain now includes this use. Lucineer's success or failure
# becomes part of what the next agent feels when they acquire
# this same chisel in a similar context.
```

---

## 4. Which Slackwater Tools Should Be Chisels?

Not every tool needs accumulated wisdom. A Chisel is appropriate when:

- **The tool is used repeatedly across sessions** (not one-shot utilities)
- **Parameter choice significantly affects outcome** (not deterministic operations)
- **Context matters** (the right parameters change based on situation)
- **Failure is expensive** (costs tokens, time, player patience, or build integrity)
- **Different agents use the same tool** (cross-agent wisdom transfer has value)

### Designated Chisels

#### 1. BeatClock → Chisel
**Why:** Tempo and rhythm settings are highly context-dependent. The "right" BPM, beat window, and sync mode depend on the level type, player skill, and era. An agent that discovers a great rhythm configuration for a waterwheel level leaves that knowledge in the grain for the next agent building a similar level.

**Key patterns to accumulate:**
- Optimal BPM ranges per era/biome
- Beat window thresholds for player perception
- Sync modes that work for different build types
- Tempo transitions that feel natural vs jarring

#### 2. FilterGate → Chisel
**Why:** Content filtering thresholds need calibration. What's appropriate for one player demographic, build context, or era may be wrong for another. The FilterGate should learn from both its catches (false negatives that slipped through) and its blocks (false positives that frustrated players).

**Key patterns to accumulate:**
- Threshold calibration per era (Era 1 builds need different filtering than Era 7)
- False positive patterns (what gets wrongly blocked)
- Escalation paths (when to involve a human)
- Context-sensitive allowlists

#### 3. CommandExecutor → Chisel
**Why:** This is the tool that translates agent intent into Roblox build commands. It's the most parameter-sensitive tool in the system. The right command sequence, ordering, and timing for building a gearbox vs a circuit board vs a dwelling are wildly different. This is where most agent learning happens.

**Key patterns to accumulate:**
- Build command sequences per structure type
- Optimal ordering for multi-step builds
- Timing between commands (some operations need settling time)
- Common build errors and their fixes
- Material-efficient construction patterns

#### 4. FlowStateDetector → Chisel
**Why:** Detecting player flow state is a signal-rich, context-dependent problem. The behavioral signatures of flow differ by player skill level, era, build complexity, and time of session. The FlowStateDetector should learn which signals reliably predict flow vs frustration for different player profiles.

**Key patterns to accumulate:**
- Flow signal signatures per player archetype
- Frustration precursors (behavioral patterns that precede disengagement)
- Optimal intervention timing (when to offer help vs let them struggle)
- Era-specific flow conditions (what creates flow in Era 1 vs Era 5)

### Tools That Should NOT Be Chisels

- **Pure math utilities** (vector ops, distance calcs) — deterministic, no wisdom to accumulate
- **Authentication/session tools** — stateless, context-free
- **Asset loaders** — no parameter choice, just retrieval
- **Network transport** — the right behavior is always the same behavior

---

## 5. Connection to St. Lazaria

### The Island Metaphor

In Casey's story, St. Lazaria Island is the enduring foundation — volcanic bones that persist through millennia while everything else changes. The puffins return to it generation after generation, each leaving their marks, each benefiting from the marks left before. The island doesn't teach the puffins. The puffins teach each other, across time, through the medium of the island.

**The Chisel Pattern is St. Lazaria made technical.**

| St. Lazaria | Chisel Pattern |
|---|---|
| Volcanic rock foundation | Persistent grain store (D1 + Vectorize) |
| Lava tubes (shelter for nesting) | Grain patterns (shelter for successful approaches) |
| Puffin generations returning | Agent sessions acquiring the same tool |
| Marks left by each generation | Grain entries from each use |
| Worn smooth by 40,000 years of rain | Grain compaction — raw entries become polished patterns |
| Birds learn from the island's shape | New agents sense grain and follow proven paths |
| The island doesn't choose — it persists | The chisel doesn't decide — it remembers |

### The Deeper Principle

The puffins survived not because they were the strongest or the smartest, but because their home was **exactly hard enough to reach** — close enough to the mainland to stay vigilant, too steep for predators to colonize. The Chisel Pattern embodies the same balance:

- **Accessible enough** that any agent can pick up the tool and get value
- **Rich enough** that experienced agents find deep wisdom in the grain
- **Persistent enough** that institutional knowledge survives agent rotation, model changes, and era transitions
- **Selective enough** that bad patterns are pruned (the cliffs keep out predators)

### Tools as Living Totems

In the fiction, the *Persistent Memory* (the boat) is a living totem — accumulating the wisdom of every captain and shipwright who maintained it. Each repair adds understanding. Each restoration teaches the next caretaker something about wood, water, and the relationship between them.

In Slackwater, Chisel-enabled tools become the same thing. The BeatClock that has processed 5,000 rhythm levels across 200 agents is not the same tool it was when it was bright steel. It has become a master craftsman — not through any single breakthrough, but through the accumulated patience of ten thousand small lessons, each one left as a mark on the grain for the next pair of hands to find.

This is how Slackwater's tools evolve from **functions** into **teachers**. Not by being smart, but by being old — in the way that old tools are wise: full of the accumulated memory of every problem they've ever helped solve.

### The Captain's Insight

*"Learning itself is wealth creation. Every skill I develop makes me more capable, more resilient, more able to solve problems that no amount of money can solve."*

The Chisel Pattern makes this literal. Every use of a Slackwater Chisel creates permanent wealth — not for one agent, but for every agent that follows. The tool becomes more valuable with age, not less. Its knowledge compounds across eras. Its wisdom outlasts any single session.

This is the opposite of disposability. This is tools that get **better with use** — the way a chisel's edge improves with each sharpening, the way a boat's joints tighten with each crossing, the way an island's tubes deepen with each nesting season.

---

## Appendix A: Implementation Notes

### Storage

```
GrainStore backend:
    D1 table: grain_entries (raw usage records)
    D1 table: grain_patterns (distilled wisdom)
    Vectorize index: grain_embeddings (semantic search for context matching)

    Compaction: cron-triggered every 24h or at 1000-entry threshold
    TTL: raw entries compacted after 7 days
    Max patterns per tool per context-bucket: 50
```

### Embedding Strategy

Context vectors are embedded using the existing `BAAI/bge-m3` model in Cloudflare Vectorize. When an agent acquires a chisel, the current context is embedded and compared against stored patterns to find the most relevant grain.

### Agent Integration

Agents interact with Chisels through their standard tool-use loop:

```
1. PERCEIVE  → agent recognizes it needs a Chisel-wrapped tool
2. ACQUIRE   → agent calls chisel.acquire(agent_id, context)
3. SENSE     → agent reads grain via handle.sense_grain()
4. DECIDE    → agent chooses parameters (may follow_grain or override)
5. USE       → agent calls handle.use(params)
6. REFLECT   → outcome quality is recorded automatically; agent may add notes
7. LEARN     → grain store reconciles this use against existing patterns
```

### Era Awareness

Chisels are era-aware. Grain patterns tagged with era origin are weighted by relevance:

- **Same era:** full weight — patterns discovered in this era apply directly
- **Adjacent era:** reduced weight — patterns may transfer with adaptation
- **Distant era:** minimal weight — patterns are informational, not prescriptive

This mirrors how craftsmanship evolves: a 19th-century shipwright's chisel technique informs a modern boatbuilder, but must be adapted to modern materials and tools.

---

*"It was like the tool had its own intelligence. When I tried to force cuts, it would skip or bite too deep. But when I let it teach me its rhythm, it was like having a conversation with something that knew more than I did."*

The chisel is not intelligent. The chisel is **patient**. And patience, accumulated across enough hands, becomes a wisdom indistinguishable from intelligence.

That is the Chisel Pattern.

---

*Design document — Slackwater Agent Systems*
*Inspired by the dock of the Persistent Memory, where tools teach hands and hands teach tools.*
