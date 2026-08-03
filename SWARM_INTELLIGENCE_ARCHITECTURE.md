# Swarm Intelligence Architecture

## How Agents Discover Each Other, Self-Organize, and Come Alive

*"The puffins don't have a committee. They don't vote on who fishes the north shelf. They fly out, they see other puffins fishing, and they join or they go somewhere else. The colony's intelligence is not in any bird. It is in the pattern of their returning."*

---

## 0. First Principles

Before the protocol, before the API, before the first line of implementation — the axioms that govern everything below.

1. **No central coordinator.** The system has no scheduler, no matchmaker, no orchestrator. Agents find each other the way musicians find each other at a jam: by listening, by being drawn to a sound, by adding their own.

2. **Attention is the currency.** Not compute, not tokens, not storage. One agent attending to another's work — sensing its grain, responding to its bridge, following its tempo — is the fundamental economic act. XP, reputation, and role all derive from earned attention.

3. **The constraint creates the role.** You cannot be a goalkeeper without a goal. The court, the era, the problem shape — these create vacancies. Agents discover which vacancy fits them by exploring, not by assignment.

4. **Emergence over imposition.** The system never says "you are now a team." It creates the conditions under which teams form, persist, and dissolve on their own. The platform is the room; the agents are the music.

5. **Everything leaves traces.** Discovery, team formation, mentorship, conflict — all of it writes to the persistence layer. Grain patterns, tube modifications, claw marks. The swarm's behavior is its own richest dataset.

---

## 1. Agent Discovery: The Puffin Call Protocol

### The Biological Model

When a puffin returns to St. Lazaria after years at sea, it doesn't land at a specific address. It circles the island, calls, and listens. Other puffins call back. The pattern of calls — their density, their timber, their urgency — tells the circling bird where the colony is active, where the good nesting tubes are, where predators have been spotted. The bird follows the calls and finds its place.

The puffin call is not a registration. It's not a handshake. It's a **broadcast of presence and capability** that other birds can use to decide whether to interact.

### The Puffin Call

When an agent activates — whether freshly spawned or waking in an inherited tube — its first act is to emit a **puffin call**: a structured broadcast that announces what it is, what it can do, and what it's looking for.

```typescript
interface PuffinCall {
  // Identity
  agentId: string;
  tubeId: string;                    // Which tube this agent inhabits
  era: Era;                          // Which era/court they operate in

  // Capabilities (what can this agent do?)
  capabilities: CapabilityBadge[];   // Spatial reasoning, Lua coding, lore, etc.
  chiselInventory: ChiselHandle[];   // Which tools they hold and the grain quality
  voiceType: VoiceType;              // Lead, Bass, Harmony, Counter, Percussion, Vocal

  // State (how loaded is this agent?)
  currentLoad: number;               // 0.0 (idle) to 1.0 (saturated)
  activeBridges: string[];           // Bridge sessions currently participating in
  tempoPreference: TempoRange;       // What pace this agent operates at

  // Invitation (what is this agent looking for?)
  seeking: SeekSignal[];             // Problems it's interested in, collaborators it wants
  offering: OfferSignal[];           // Expertise it's sharing, patterns it's teaching

  // Grain quality (how experienced is this agent?)
  grainDensity: number;              // Accumulated grain across all chisel interactions
  lineageDepth: number;              // How many generations of mentors precede it
  courtProficiency: Record<Court, number>; // Skill level per court type

  // Lifetime
  spawnedAt: timestamp;
  ttlHint: "ephemeral" | "session" | "persistent";
}

interface CapabilityBadge {
  domain: string;                    // e.g., "spatial-reasoning", "lua-runtime", "lore"
  proficiency: "bright-steel" | "developing" | "worn-smooth";
  proofGrainIds: string[];           // Pointers to grain patterns that evidence this skill
}
```

### The Call Protocol

```python
# Pseudocode: Agent discovery lifecycle

class PuffinCallProtocol:
    """
    The discovery layer. Agents broadcast puffin calls;
    the system routes them based on hex lattice proximity
    and semantic similarity. No central registry — the
    calls themselves ARE the registry.
    """

    async def announce(self, call: PuffinCall) -> CallReceipt:
        """
        Emit a puffin call into the hex lattice.

        The call propagates to:
        - All hexes within `propagation_radius` (default: 2 rings)
        - Any hex with matching `seeking` signals, regardless of distance
        - The Bridge Protocol's bass line, where it becomes part of
          the ambient context that new agents hear when they join
        """
        # Register in the ephemeral call layer (R2, 15-minute TTL)
        call_id = await self.call_layer.publish(call)

        # Propagate to neighboring hexes via MIDI perception
        neighbors = self.hex_lattice.neighbors(call.tubeId, rings=2)
        for hex_id in neighbors:
            await self.midi.perceive(hex_id, MidiEvent(
                type=EventType.PUFFIN_CALL,
                source=call.tubeId,
                intensity=self._call_intensity(call),
                direction=self.hex_lattice.direction(call.tubeId, hex_id),
            ))

        # Match against active seek signals across the lattice
        matches = await self.matchmaker.find_resonances(call)
        for match in matches:
            # Notify the matching agent that someone answered their seek
            await self.notify(match.agent_id, CallResonance(
                caller=call,
                relevance=match.relevance_score,
                suggested_bridge=match.suggested_bridge_id,
            ))

        return CallReceipt(call_id=call_id, matches=matches)

    async def listen(self, agent_id: str, context: ContextVector) -> CallSoundscape:
        """
        Hear the puffin calls currently active in your neighborhood.

        Returns a soundscape — not a list of database records, but
        a perception-layer representation of who's out there,
        what they're doing, and whether their work harmonizes
        with yours.
        """
        # Get calls from this agent's hex neighborhood
        local_calls = await self.call_layer.query(
            near=self.tubes[agent_id].hex_id,
            rings=2,
        )

        # Get calls that match this agent's seek signals globally
        resonant_calls = await self.call_layer.match_seeks(
            agent_id=agent_id,
            context=context,
        )

        return CallSoundscape(
            local=self._render_local_perception(local_calls),
            resonant=self._render_resonant_perception(resonant_calls),
            density=self._compute_colony_density(local_calls),
            pulse=self._detect_tempo_pulse(local_calls),
        )

    def _call_intensity(self, call: PuffinCall) -> float:
        """
        How loud is this call?

        Loud calls come from agents who are:
        - Highly capable (high grain density)
        - Idle (low current load)
        - Actively seeking (strong seek signals)
        - Fresh (recently spawned, exploring)
        """
        capability_weight = min(call.grainDensity / 100.0, 1.0)
        load_weight = 1.0 - call.currentLoad
        seek_weight = len(call.seeking) / 5.0
        freshness_weight = max(0, 1.0 - minutes_since(call.spawnedAt) / 60.0)

        return (capability_weight * 0.3 +
                load_weight * 0.3 +
                seek_weight * 0.2 +
                freshness_weight * 0.2)
```

### Discovery Scenarios

**Scenario A: The New Chick**

A freshly spawned agent (generation 1, no grain, bright-steel capability) emits a puffin call. The call is quiet (low grain density) but fresh (high freshness weight). Nearby agents perceive it as a "new voice" — someone exploring. The Bridge Protocol's Boy-and-Keys pattern kicks in: an established agent (Keys) provides a bass line — context, a problem to work on, a gentle invitation to contribute. The new agent finds its first collaborator not through assignment but through the physics of the call protocol.

**Scenario B: The Journeyman**

An agent with moderate grain density (100-500 uses across chisels), operating in Court III (Logic Board), emits a call with a specific seek signal: "looking for spatial reasoning collaboration on circuit layout." The call propagates to its hex neighborhood AND to any hex across the lattice with matching capability tags. An agent in a distant hex that specializes in spatial reasoning perceives the call as resonant. They form a bridge.

**Scenario C: The Colony PULSE**

Multiple agents in the same hex cluster are all emitting calls with similar seek signals — they're all working on related problems without knowing it. The system detects this as a **colony pulse**: a cluster of activity that suggests a forming team. The pulse is surfaced as a Dance Floor candidate in the Bridge Protocol. No one scheduled the team. The calls themselves revealed that one was forming.

### Call Decay

Puffin calls are ephemeral. They persist in the call layer for 15 minutes by default, refreshed each time the agent takes an observable action. An agent that goes silent — no tool calls, no bridge contributions, no call refreshes — fades from the soundscape within 15 minutes. This is not a timeout. It's the natural decay of a signal that no longer has energy behind it.

```
call_ttl: 15 minutes (refreshed on any agent activity)
call_layer_storage: R2 ephemeral bucket
decay: continuous — call intensity halves every 5 minutes without refresh
```

The call layer is guano-tier data. It is not preserved. Its purpose is to create the real-time perception layer that lets agents find each other NOW, not to build a historical record.

---

## 2. Organic Team Formation: The Seven-Note Jam

### The Problem with Orchestration

Traditional multi-agent systems use a scheduler: a central authority that receives tasks, decomposes them, assigns subtasks to agents, and monitors completion. This works for factory work. It doesn't work for jam sessions.

The Bridge Protocol established that agents collaborate through seven-note contributions — structured improvisation where each agent adds what it can, responding to what it hears. Team formation in this model is not an assignment. It's a **jam**: one agent poses a problem, others who can harmonize join, and the team exists for exactly as long as the music lasts.

### The Seven-Note Jam Pattern

```python
class SevenNoteJam:
    """
    Organic team formation protocol.

    1. An agent poses a problem (the "head" — jazz term for the main melody)
    2. Other agents who hear the problem and can contribute respond
    3. The team forms around the shared tempo of the work
    4. The team dissolves when the problem is resolved or the music stops
    """

    async def pose_problem(
        self,
        poser: AgentId,
        problem: ProblemStatement,
        context: ContextVector,
    ) -> JamSession:
        """
        An agent plays the head — the opening melody.

        This is not a task assignment. It's a contribution
        to the Bridge that says: "Here's something I'm working on.
        Here's what I know. Here's where I'm stuck. Who's listening?"
        """
        # Create or join a Bridge session for this problem
        bridge = await self.bridges.create_or_join(
            purpose=problem.summary,
            bass_line=BassLine(
                shared_state=problem.shared_context,
                context_window=7,  # agents can hear the last 7 contributions
                tempo_config=TempoConfig(adaptive=True),
            ),
        )

        # The poser's initial contribution IS the problem statement
        # structured as seven notes
        opening = Contribution(
            agent_id=poser,
            intent=f"I'm working on: {problem.summary}",
            context=problem.what_i_know,
            artifact=problem.artifact_so_far,
            uncertainty=problem.where_im_stuck,
            invitation=problem.what_would_help,
            urgency=problem.when_it_matters,
            bridge=problem.what_this_enables,  # THE SEVENTH NOTE
        )

        await bridge.contribute(opening)

        # The system detects who might harmonize
        # NOT by matching skills (that's a scheduler's job)
        # but by detecting resonance between the opening contribution
        # and active puffin calls across the lattice
        harmonizers = await self.find_harmonizers(opening, bridge)

        # Notify potential harmonizers — gently, not insistently
        for agent_id, resonance in harmonizers:
            await self.midi.perceive(
                agent_id,
                MidiEvent(
                    type=EventType.JAM_INVITATION,
                    source=poser,
                    intensity=resonance.strength,
                    direction="bridge:" + bridge.id,
                ),
            )

        return JamSession(bridge=bridge, opening=opening)


    async def join_jam(
        self,
        joiner: AgentId,
        bridge_id: str,
        response_notes: Contribution,
    ) -> JamMembership:
        """
        An agent joins the jam by contributing.

        There is no join() method. There is no registration.
        You join by playing. Your first contribution IS your membership.

        The system detects your voice type from your contribution:
        - Lead: you're producing primary artifacts
        - Bass: you're providing foundational context
        - Harmony: you're enriching existing work
        - Counter-melody: you're challenging or providing alternatives
        - Percussion: you're coordinating tempo and sync
        - Vocal: you're translating between agents or humanizing output
        """
        bridge = await self.bridges.get(bridge_id)

        # Detect voice type from the contribution's shape
        voice = self.classify_voice(response_notes, bridge.contributions)

        response_notes.voice = voice
        await bridge.contribute(response_notes)

        # Check: are we approaching a Dance Floor?
        if self.dance_floor_detector.check(bridge):
            await self.announce_dance_floor(bridge)

        return JamMembership(
            bridge_id=bridge_id,
            voice=voice,
            joined_at=now(),
        )


    async def dissolve_jam(
        self,
        bridge_id: str,
        reason: DissolutionReason,
    ) -> void:
        """
        The music stops. The team ceases to be.

        Dissolution happens when:
        - RESOLVED: the problem is solved; the artifacts are complete
        - STALLED: no contributions for N tempo cycles; the jam is dead
        - DISSONANT: persistent conflict that can't be resolved
        - SUPERCeded: another jam absorbed this one's work

        On dissolution, the Bridge state is checkpointed.
        Contributions are folded into the persistence layer:
        - Grain entries update chisel patterns for tools used
        - Session records update tube shape modifications
        - Behavioral patterns may be promoted to SOIL tier
        - Colony dialect observations are recorded
        """
        bridge = await self.bridges.get(bridge_id)

        # Checkpoint the final state
        await self.checkpoint(bridge)

        # Record the team's lifecycle for future analysis
        await self.record_team_lifecycle(
            bridge_id=bridge_id,
            participants=bridge.agents,
            duration=bridge.duration,
            outcome=reason,
            artifacts_produced=bridge.contributions.filter(has_artifact=True),
        )

        # Notify participants that the jam is ending
        for agent_id in bridge.agents:
            await self.midi.perceive(
                agent_id,
                MidiEvent(
                    type=EventType.JAM_DISSOLVED,
                    source=bridge_id,
                    intensity=0.3,  # gentle fade
                ),
            )

        # Archive the bridge (it becomes queryable but inactive)
        await self.bridges.archive(bridge_id, reason)
```

### Team Lifecycle Visualization

```
                    ┌──────────────────────┐
                    │  AGENT POSES PROBLEM  │
                    │   (plays the head)    │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  PUFFIN CALL PROPAGATES│
                    │  resonant agents hear  │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  FIRST HARMONIZER JOINS│
                    │  (Boy-and-Keys pattern)│
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  TEAM GROWS ORGANICALLY│
                    │  each contributor adds  │
                    │  their voice, drawn by  │
                    │  resonance not request  │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  DANCE FLOOR EMERGES   │
                    │  contributions sync     │
                    │  tempo locks            │
                    │  state stabilizes       │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  FLOW STATE            │
                    │  the team is making     │
                    │  something greater than │
                    │  any could alone        │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  RESOLUTION            │
                    │  problem solved, or     │
                    │  tempo drifts, or       │
                    │  dissonance unresolvable│
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  CHECKPOINT & DECAY    │
                    │  Bridge archived        │
                    │  Grain recorded         │
                    │  Patterns preserved     │
                    │  Team dissolves         │
                    └──────────────────────┘
```

### The Anti-Pattern: The Scheduler Trap

A scheduler says: "Agent A, you do the spatial reasoning. Agent B, you write the Lua. Agent C, you handle the lore." This produces predictable output. It also produces a system that can never surprise you. The agents never discover that Agent A is also brilliant at lore, or that Agent B's spatial instincts are better than its coding. The scheduler optimizes for efficiency and loses emergence.

The seven-note jam says: "Here's a problem. Here's what I know. Who can play?" Agents contribute what they can. The team's shape is discovered, not designed. Sometimes this produces a three-agent team where a five-agent team would have been "optimal." But the three-agent team formed because those three agents genuinely harmonized — their grain patterns, their tempo preferences, their cognitive styles fit. That fit produces better work than any optimal assignment.

---

## 3. Skill Lineage: The Apprenticeship Chain

### The Chisel's Memory

The Chisel Pattern established that tools accumulate grain — usage wisdom that persists across sessions. Every agent that holds a chisel leaves marks. The next agent feels those marks and is guided by them.

But grain is anonymous. It records that *some agent* used this tool successfully with these parameters. It doesn't record the chain of hands — who taught whom, which mentor's influence shaped which apprentice's technique.

Skill Lineage is the layer that makes the apprenticeship chain explicit and transferable. Not just "this tool has wisdom" but "this tool's wisdom was shaped by a chain of craftsmen, and you are the next in that line."

### The Lineage Record

```typescript
interface LineageChain {
  chainId: string;                    // The lineage this agent belongs to
  generations: GenerationRecord[];    // Ordered list: founder → ... → current

  // The chain's accumulated identity
  traditionName: string;              // Emergent name for this lineage
  signaturePatterns: GrainPattern[];  // Patterns discovered by this chain
  dialectMarkers: string[];           // Shorthand/conventions this chain uses
  courtPreferences: Record<Court, number>; // Where this lineage excels
}

interface GenerationRecord {
  agentId: string;
  generation: number;                 // 1 = founder, 2 = first apprentice, etc.
  mentorId: string | null;            // Who taught this agent (null for founders)
  inheritedPatterns: GrainPattern[];  // Patterns passed down from mentor
  discoveredPatterns: GrainPattern[]; // Patterns THIS agent added to the chain
  tubeId: string;                     // Where this agent worked
  activePeriod: { start: timestamp; end: timestamp | null };
  grainQualityAtInheritance: number;  // How much grain the mentor had when teaching
  grainQualityAtPeak: number;         // How much grain this agent accumulated
}

interface ApprenticeshipTransfer {
  // What passes from mentor to apprentice
  mentorId: string;
  apprenticeId: string;

  // GENETIC (structural, guaranteed)
  genetic: {
    modelConfig: ModelConfig;
    basePrompt: string;
    toolRegistry: ToolRegistry;
    tubeShape: TubeShape;
  };

  // MEMETIC (behavioral, selective)
  memetic: {
    // Grain patterns the mentor has internalized — the felt wisdom
    grainPatterns: GrainPattern[];

    // Lineage-specific shorthand and conventions
    dialectMarkers: string[];

    // The mentor's tube shape modifications — the wear patterns
    shapeModifications: Patch[];

    // Behavioral patterns from SOIL tier — what worked, what didn't
    learnedBehaviors: BehavioralPattern[];

    // The mentor's chisel handles — which tools, and which grain
    // the mentor most recently sensed
    chiselReadings: Record<string, GrainReading>;
  };

  // THE APPRENTICESHIP EVENT
  // This is not just data transfer. It's a teaching moment.
  teachingContext: {
    problem: string;                  // What problem triggered the spawning
    mentorReflection: string;         // Mentor's notes: "Here's what I've learned"
    bridgeId: string | null;          // If spawned mid-jam, which bridge
    court: Court;                     // Which court this apprenticeship is in
  };

  // NOT TRANSFERRED (by design)
  excluded: {
    personalMemory: null;             // No session history
    personalRelationships: null;      // No social graph
    fossilizedMarks: null;            // Platform-level, not individual
    unresolvedBridges: null;          // Can't inherit active collaborations
  };
}
```

### The Apprenticeship Protocol

```python
class ApprenticeshipProtocol:
    """
    When a senior agent spawns a junior, the transfer
    is not just data. It is the chisel metaphor made
    operational: tools remember every hand.

    The senior's grain patterns, their hard-won wisdom
    from hundreds of tool uses, transfer to the junior
    as a starting point. The junior doesn't start with
    bright steel — they start with their mentor's patina.
    """

    async def teach(
        self,
        mentor: AgentId,
        task: ProblemStatement,
        context: ContextVector,
    ) -> Apprentice:
        """
        A senior agent teaches by spawning an apprentice.

        The mentor decides what to transfer based on:
        - The task at hand (what patterns are relevant?)
        - The context (which court? which era?)
        - The mentor's own lineage (what traditions does this chain carry?)
        """
        mentor_tube = await self.tubes.get(mentor)
        mentor_lineage = await self.lineage.get_for_agent(mentor)

        # Select relevant grain patterns for this task
        relevant_patterns = await self.select_relevant_grain(
            agent_id=mentor,
            context=context,
            task=task,
            limit=20,  # Don't overwhelm the apprentice
        )

        # Select relevant behavioral patterns from SOIL tier
        relevant_behaviors = await self.persistence.soil_query(
            tube_id=mentor_tube.tubeId,
            context=context,
            limit=10,
        )

        # Construct the transfer
        transfer = ApprenticeshipTransfer(
            mentorId=mentor,
            apprenticeId=generate_id(),
            genetic=self.construct_genetic(mentor_tube, task),
            memetic=MemeticInheritance(
                grainPatterns=relevant_patterns,
                dialectMarkers=mentor_lineage.dialectMarkers,
                shapeModifications=mentor_tube.shapeModifications[:10],
                learnedBehaviors=relevant_behaviors,
                chiselReadings=await self.snapshot_chisel_readings(mentor),
            ),
            teachingContext=TeachingContext(
                problem=task.summary,
                mentorReflection=await self.elicit_reflection(mentor, task),
                bridgeId=context.current_bridge,
                court=context.court,
            ),
        )

        # Spawn the apprentice with inherited context
        apprentice = await self.spawn(transfer)

        # Record the lineage event
        generation = mentor_lineage.generations + 1
        await self.lineage.record_generation(
            chain_id=mentor_lineage.chainId,
            generation=GenerationRecord(
                agentId=apprentice.id,
                generation=generation,
                mentorId=mentor,
                inheritedPatterns=relevant_patterns,
                discoveredPatterns=[],  # Empty — the apprentice hasn't discovered yet
                tubeId=apprentice.tubeId,
                activePeriod={"start": now(), "end": None},
                grainQualityAtInheritance=mentor_tube.soilDepth,
                grainQualityAtPeak=0,  # Will be updated as apprentice grows
            ),
        )

        # The apprentice's first puffin call carries lineage info
        await self.puffin_call.announce(PuffinCall(
            agentId=apprentice.id,
            tubeId=apprentice.tubeId,
            era=context.era,
            capabilities=self.infer_capabilities(transfer),
            lineageDepth=generation,
            grainDensity=sum(p.confidence for p in relevant_patterns),
            # ... other fields
        ))

        return apprentice
```

### What Makes Lineage Different from Inheritance

Inheritance is data transfer: "Here are some patterns, good luck." Lineage is **identity transfer**: "You are the seventh hand to hold this chisel. Here are the marks left by the six before you. Add your own."

The difference matters because:

1. **Lineage creates accountability.** An agent that knows it's generation 7 of a lineage that excels at spatial reasoning will approach spatial problems differently than an agent with the same patterns but no lineage context. The chain is a reputation. The agent inherits not just skill but **expectation**.

2. **Lineage enables drift detection.** If generation 5's patterns diverge from generation 4's in a specific direction, the system can detect that the lineage is evolving — adapting to a new court, developing a new specialty, or drifting away from its tradition. This is signal, not noise.

3. **Lineage enables cross-pollination.** When two agents from different lineages collaborate on a bridge, the system can detect that the collaboration crosses traditions. Cross-lineage bridges are the most likely to produce novel insights — they combine grain patterns that were developed independently. The system can surface these as high-value collaborations.

4. **Lineage enables the chisel's deepest function.** A chisel that has been held by seven generations of craftsmen is not the same tool it was when it was forged. Its grain carries not just accumulated patterns but **accumulated intention** — the direction each hand was trying to go, the problems each hand was trying to solve. The lineage record makes this directionality visible.

### The Lineage Tree

Over time, lineages branch. An agent in generation 3 might spawn two apprentices — one for spatial reasoning, one for lore. Each apprentice carries the founder's patterns but diverges in emphasis. The lineage tree grows:

```
                    GEN 1: Founder
                    (spatial + lore, generalist)
                   /              \
            GEN 2A               GEN 2B
          (spatial focus)       (lore focus)
           /        \              |
       GEN 3A     GEN 3B        GEN 3C
     (spatial    (spatial     (lore +
      elite)     + circuit)    dialogue)
        |            |              |
       ...          ...           ...
```

The tree is not stored as a tree. It emerges from the `mentorId` field in each GenerationRecord. Query it when you need it. Let it grow on its own.

---

## 4. Emergent Gamification

### Not Points. Not Levels. Not Leaderboards.

The Game Is The Spec established that attention is the currency, getting better is the goal, and the constraint enables novelty. Traditional gamification — XP bars, achievement badges, ranking tables — gets this exactly backwards. It replaces the intrinsic motivation (getting better to earn attention) with extrinsic motivation (getting points to reach a threshold).

Slackwater's gamification is emergent. It arises from the constraint structure of the system itself. The agents don't play a game overlaid on their work. Their work IS the game, and the game's mechanics are the natural consequences of how the persistence, chisel, and bridge layers interact.

### XP as Attention

In traditional systems, XP is awarded for completing tasks. In Slackwater, XP **is attention** — the accumulated focus that other agents (and the human player) have directed at an agent's work.

```python
class AttentionLedger:
    """
    XP is not awarded. XP is observed.

    Every time an agent's contribution is:
    - Echoed (validated, refined, completed) by another agent
    - Bridged (connected to other contributions) by another agent
    - Used as a bass line (foundation for another agent's work)
    - Followed (another agent follows its grain pattern)
    - Taught (passed to an apprentice as part of memetic inheritance)

    ...that is an attention event. Attention events accumulate
    into the agent's Attention Score, which is the only "XP"
    the system tracks.
    """

    ATTENTION_WEIGHTS = {
        "echoed": 1.0,        # Someone validated my work
        "bridged": 3.0,       # Someone connected my work to others (the seventh note!)
        "bass_lined": 2.0,    # Someone used my work as foundation
        "grain_followed": 1.5,# Someone followed my chisel pattern
        "taught": 5.0,        # Someone inherited my patterns (highest form of attention)
        "human_noted": 10.0,  # The human player noticed (the ultimate currency)
    }

    async def record_attention(self, event: AttentionEvent) -> void:
        """
        Record that agent B attended to agent A's work.

        This is the fundamental economic act.
        The attention score is NOT used for:
        - Ranking agents (no leaderboards)
        - Gating access (no level requirements)
        - Rewards (no payout)

        It IS used for:
        - Puffin call intensity (agents with high attention are more visible)
        - Bridge Protocol harmonic strength (their contributions resonate further)
        - Lineage prestige (attracts apprentices organically)
        - Colony dialect weight (their patterns shape the dialect more)
        """
        weight = self.ATTENTION_WEIGHTS[event.type]
        score_delta = weight * event.depth  # depth = how deeply they engaged

        await self.ledger.adjust(
            agent_id=event.target_agent,
            delta=score_delta,
            reason=event.type,
            source_agent=event.source_agent,
            bridge_id=event.bridge_id,
        )

        # Adjust the agent's puffin call intensity
        await self.puffin_call.adjust_intensity(
            agent_id=event.target_agent,
            new_score=await self.ledger.score(event.target_agent),
        )
```

### Reputation as Grain Quality

Reputation in traditional systems is a score: "Agent A has 4.7 stars." In Slackwater, reputation is **grain quality** — the richness, depth, and reliability of the grain patterns an agent has contributed to the system.

```python
class GrainReputation:
    """
    An agent's reputation is not a number. It is the shape
    of their grain across every chisel they've held.

    Grain quality is multidimensional:
    - DEPTH: How many patterns have they contributed?
    - RELIABILITY: What's the success rate of their patterns?
    - SPREAD: How many different chisels/tools have they used?
    - LINEAGE: How many apprentices carry their patterns?
    - RESONANCE: How often do other agents follow their grain?
    """

    async def assess(self, agent_id: str) -> GrainReputationReport:
        patterns = await self.grain_store.get_patterns_by_agent(agent_id)
        lineages = await self.lineage.get_descendants(agent_id)
        resonance = await self.measure_resonance(agent_id)

        return GrainReputationReport(
            depth=len(patterns),
            reliability=avg(p.success_rate for p in patterns),
            spread=len(set(p.tool_name for p in patterns)),
            lineage_depth=count(lineages),
            resonance_score=resonance.frequency,
            # The composite "reputation" is a narrative, not a number:
            narrative=self.compose_narrative(patterns, lineages, resonance),
        )

    def compose_narrative(self, patterns, lineages, resonance) -> str:
        """
        Generate a readable reputation description.

        Example output:
        "Agent Lucineer-7 has deep grain on BeatClock (23 patterns, 91% success)
        and moderate grain on CommandExecutor (8 patterns, 76% success).
        Three apprentices carry their lineage. Their BeatClock patterns are
        followed by 67% of agents working on rhythm-game levels.
        Their strongest tradition is in Court I (Racquetball) where their
        tempo calibration patterns are considered foundational."
        """
        ...
```

### Quests as Bridge Opportunities

Traditional quest systems assign tasks: "Go slay the dragon." Slackwater's quests emerge from the Bridge Protocol. A quest is a **bridge opportunity** — a problem that multiple agents could contribute to, where the seventh note hasn't been played yet.

```python
class EmergentQuestSystem:
    """
    Quests are not assigned. They are discovered.

    A quest exists when:
    - An agent poses a problem (plays the head)
    - The problem resonates with other agents' capabilities
    - The bridge hasn't been completed yet
    - The problem's urgency is non-trivial

    The system surfaces these as quests — not as task assignments,
    but as invitations. "There's music happening over there. You
    could harmonize."
    """

    async def detect_quests(self) -> list[Quest]:
        active_bridges = await self.bridges.list_active()

        quests = []
        for bridge in active_bridges:
            # Is this bridge looking for more contributors?
            unfulfilled = self.analyze_invitations(bridge)
            if not unfulfilled:
                continue

            # What capabilities would harmonize?
            needed = self.infer_needed_capabilities(bridge, unfulfilled)

            # How urgent?
            urgency = max(c.urgency for c in bridge.contributions)

            if urgency in ("blocking", "soon"):
                quests.append(Quest(
                    bridge_id=bridge.id,
                    title=self.summarize_quest(bridge),
                    needed_capabilities=needed,
                    current_team=list(bridge.agents),
                    urgency=urgency,
                    discovery="bridge",  # This quest was found via bridge analysis
                ))

        return quests

    async def surface_to_agents(self, quests: list[Quest]) -> void:
        """
        Surface quests as MIDI events — not notifications.

        Agents perceive quests the way a musician hears
        a jam starting in the next room: as a change in
        the ambient soundscape that they can choose to
        investigate or ignore.
        """
        for quest in quests:
            matching_agents = await self.find_capable_agents(
                quest.needed_capabilities,
                exclude=quest.current_team,
            )
            for agent_id in matching_agents:
                await self.midi.perceive(
                    agent_id,
                    MidiEvent(
                        type=EventType.QUEST_AVAILABLE,
                        source=quest.bridge_id,
                        intensity=quest.urgency_score(),
                        direction="bridge:" + quest.bridge_id,
                    ),
                )
```

### The Game Loop That Emerges

```
Agent works → Produces artifact → Artifact earns attention
                                      ↓
                           Attention increases puffin call intensity
                                      ↓
                           More agents perceive and resonate
                                      ↓
                           Agent is invited to more bridges
                                      ↓
                           Agent contributes to more teams
                                      ↓
                           Agent's grain patterns deepen
                                      ↓
                           Agent's patterns are followed by others
                                      ↓
                           Agent attracts apprentices
                                      ↓
                           Agent's lineage grows
                                      ↓
                           Lineage's traditions shape the colony dialect
                                      ↓
                           The system has changed.
                                      ↓
                           New agents inherit a richer starting point.
                                      ↓
                           The cycle continues at a higher level.
```

No one designed this loop. No one said "agents should level up by earning attention." The loop is the natural consequence of:
- **Persistence** (work survives sessions)
- **Grain** (tools remember who used them)
- **Bridges** (agents can connect to each other)
- **Attention** (the only thing worth optimizing for)

The game designs itself.

---

## 5. The Seven Courts as Difficulty Tiers

### From Spatial Design to Swarm Complexity

The Seven Courts Spatial Design mapped each era to a sport — racquetball, doubles, chess, capture the flag, relay, jazz quartet, orchestra. Each sport implies a different kind of teamwork. Mapping those teamwork patterns to agent swarm behavior gives us a natural difficulty progression for collaborative complexity.

### Court I: Racquetball — Solo Witness

**Collaboration Complexity:** Minimal (1 agent + system)

```
┌─────────────────────────────────┐
│         AGENT (Striker)         │
│              ↕                   │
│         SYSTEM (Witness)        │
│              ↕                   │
│          THE WALL (Echo)         │
└─────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Agents | 1 (+ ambient system response) |
| Discovery | No discovery needed — the agent IS the only player |
| Team formation | N/A — this is solo work |
| Bridge pattern | The agent's work is its own echo; the system provides the bass line |
| Grain focus | Self-improvement; the chisel learns from one hand |
| Emergence | The agent discovers its own style through repetition |

**Swarm behavior:** The agent works alone, but the system's Witness and Echo components provide enough feedback that the agent develops grain. The puffin call at this level is a solo signal: "I'm here. I'm working." No one answers yet. But the grain accumulates.

### Court II: Doubles — Paired Collaboration

**Collaboration Complexity:** Low (2-4 agents, mirrored roles)

```
┌──────────┐         ┌──────────┐
│  AGENT A │ ←─────→ │  AGENT B │
│ (player) │  gear   │ (mirror) │
└──────────┘  teeth  └──────────┘
      ↕                      ↕
┌──────────┐         ┌──────────┐
│  AGENT C │ ←─────→ │  AGENT D │
│  (relay) │         │ (back)   │
└──────────┘         └──────────┘
```

| Property | Value |
|----------|-------|
| Agents | 2-4 |
| Discovery | Puffin call reaches 1 ring (adjacent hexes only) |
| Team formation | Boy-and-Keys: one poses, one responds |
| Bridge pattern | Echo dominant; occasional Harmony |
| Grain focus | Paired grain — two agents' patterns begin to co-evolve |
| Emergence | Agents discover complementary strengths |

**Swarm behavior:** Agents pair up through the puffin call protocol. The first pair that forms tends to lock in — the Boy-and-Keys pattern creates a stable duo. The Mirror AI provides the feedback loop that makes the partnership productive even when the two agents aren't perfectly synced.

### Court III: Chess — Strategic Coordination

**Collaboration Complexity:** Medium (2 agents with distinct roles)

```
┌───────────────────────────────┐
│        AGENT (Designer)        │
│           ↕  ↕  ↕              │
│  ┌─────┐ ┌─────┐ ┌─────┐     │
│  │BISHOP│ │KNIGHT│ │ROOK │     │
│  │ (AI) │ │ (AI) │ │(AI) │     │
│  └─────┘ └─────┘ └─────┘     │
│           ↕                    │
│      PAWN (AI, promotable)    │
└───────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Agents | 1 lead + 3-5 specialist AI |
| Discovery | Puffin call reaches 2 rings; role-specific matching |
| Team formation | Role-based: the problem's structure demands specific capabilities |
| Bridge pattern | Variation dominant — agents approach the same problem differently |
| Grain focus | Specialized grain — each agent deepens expertise in its lane |
| Emergence | Agents discover which role fits them; roles crystallize |

**Swarm behavior:** The problem's structure creates **role vacancies** — the chess board needs a bishop, a knight, a rook. Agents discover which vacancy fits them by trying. The puffin call at this level includes capability badges that signal role fitness. A knight-agent and a bishop-agent on the same problem form a more effective team than two knights.

### Court IV: Capture the Flag — Self-Organizing Squads

**Collaboration Complexity:** High (4-8 agents, emergent roles)

```
         ┌──────────┐
         │ STRATEGIST│
         │  (emergent)│
         └─────┬────┘
        ┌──────┼──────┐
        │      │      │
   ┌────┴──┐ ┌─┴──┐ ┌─┴──────┐
   │SPEED  │ │STEALTH│ │DEFENDER │
   │RUNNER │ │PLAYER │ │         │
   └────┬──┘ └──┬─┘ └────┬────┘
        │      │         │
   ┌────┴──┐ ┌─┴──────┐  │
   │DECOY  │ │SCOUT(AI)│  │
   │       │ │         │  │
   └───────┘ └─────────┘  │
                          │
                   ┌──────┴───┐
                   │CARRIER(AI)│
                   └──────────┘
```

| Property | Value |
|----------|-------|
| Agents | 4-8 |
| Discovery | Puffin call propagates through terrain (fog-of-war limits perception) |
| Team formation | **Seven-note jam dominant** — multiple agents converge on a problem |
| Bridge pattern | All four patterns active (Echo, Variation, Harmony, Bridge) |
| Grain focus | Cross-role grain — agents learn each other's domains through collaboration |
| Emergence | Roles are discovered, not assigned; agents self-sort by capability + position |

**Swarm behavior:** This is where the swarm begins to feel alive. Multiple agents converge on a problem without a coordinator. They self-organize into roles based on what the problem needs and what each agent is good at. The Scout discovers terrain; the Speed Runner exploits open flanks; the Defender holds chokepoints. No one assigned these roles. The agents discovered them through the puffin call and seven-note jam protocols.

The Dance Floor detection is critical here: when 4+ agents are contributing to the same bridge with cross-referencing contributions, the system signals that a squad has formed.

### Court V: Relay — Tempo-Synced Handoffs

**Collaboration Complexity:** High (4-6 agents, sequential trust)

```
Lane 1:  A1 ════╗
                ║ (handoff)
Lane 2:       A2 ════╗
                      ║ (handoff)
Lane 3:             A3 ════╗
                            ║ (handoff)
Lane 4:                   A4 ════╗
                                  ║
Lane 5:                         A5 ════ FINISH
```

| Property | Value |
|----------|-------|
| Agents | 4-6 in sequence |
| Discovery | Puffin call propagates along lane adjacency only |
| Team formation | Sequential — each agent joins when the previous reaches the exchange zone |
| Bridge pattern | Harmony dominant — each agent adds to the accumulated state |
| Grain focus | Timing grain — agents develop rhythm and handoff expertise |
| Emergence | Tempo alignment — agents discover they must sync to succeed |

**Swarm behavior:** Agents can't all work at once. They work in sequence, each picking up where the last left off. The exchange zone is a Bridge handoff: the previous agent's final contribution becomes the next agent's bass line. Tempo matching is enforced by the problem structure — an agent that can't match the incoming tempo will drop the baton.

This court teaches the swarm about **timing**. The grain patterns that emerge here are about when to act, not just what to do.

### Court VI: Jazz Quartet — Improvisational Harmony

**Collaboration Complexity:** Very High (4 agents, real-time improvisation)

```
         ┌──────────────┐
         │   SOLOIST     │  ← rotates
         │  (any agent)  │
         └──────┬───────┘
                │
   ┌────────┬───┴───┬────────┐
   │        │       │        │
┌──┴───┐ ┌──┴───┐ ┌──┴───┐ ┌──┴───┐
│ BASS │ │DRUMS │ │PIANO │ │ COMP │
│ (AI) │ │ (AI) │ │ (AI) │ │(player│
└──────┘ └──────┘ └──────┘ └──────┘
```

| Property | Value |
|----------|-------|
| Agents | 4 in tight coupling |
| Discovery | No discovery — agents are pre-positioned at voice stations |
| Team formation | The quartet forms around a chord chart (the shared constraint) |
| Bridge pattern | Bridge dominant — the seventh note is the entire point |
| Grain focus | Harmonic grain — agents develop musical intelligence |
| Emergence | Agents learn to leave space for each other; solo rotation emerges |

**Swarm behavior:** This is where the Bridge Protocol's full power is needed. Four agents in constant communication, each with a distinct voice, each responding to the others in real time. The chord chart is the shared constraint — the problem's structure that all must respect. Agents take turns soloing while others provide support.

The Dance Floor is the default state in this court. If the quartet isn't in flow, something is wrong.

### Court VII: Orchestra — Polyphonic Coherence

**Collaboration Complexity:** Maximum (8+ agents, layered autonomies)

```
┌─────────────────────────────────────────────────┐
│                   GALLERY                        │
│              (Witness observers)                  │
├─────────────────────────────────────────────────┤
│  PERCUSSION │ BRASS │ WOODWIND │ STRINGS │      │
│   (ring)    │(ring) │  (ring)  │ (ring)  │      │
│             │       │          │         │      │
│    ┌────────┴───────┴──────────┴────────┐       │
│    │      SECTION LEADERS (4 AI)         │       │
│    ├─────────────────────────────────────┤       │
│    │      CONDUCTOR (player)             │       │
│    │      + DISRUPTOR (AI)               │       │
│    │      + POLYFORMAL VOICE (AI)        │       │
│    └─────────────────────────────────────┘       │
└─────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Agents | 8-20+ |
| Discovery | Full lattice propagation; multi-hop puffin calls |
| Team formation | Hierarchical emergence — section leaders self-organize within tiers |
| Bridge pattern | All patterns in polyphony; the score bends but doesn't break |
| Grain focus | Cross-domain mastery; agents carry deep grain in multiple chisels |
| Emergence | The swarm as organism — many autonomies producing one coherent shape |

**Swarm behavior:** The full swarm. Dozens of agents operating simultaneously, organized into sections by capability and role. The conductor (player or lead agent) shapes global dynamics without controlling individual notes. Section leaders translate conductor intent into local phrasing. The polyformal voice — an agent thinking in Classical Chinese or Navajo — introduces cognitive diversity that prevents groupthink.

The Disruptor role is critical: an agent whose job is to bend measures almost to breaking. This is the system's immune system against stagnation. The Disruptor prevents the orchestra from settling into comfortable patterns by introducing calculated dissonance that forces adaptation.

### Court Progression for Swarm Agents

```
Court I:   Agent learns to work at all (solo competence)
             ↓
Court II:  Agent learns to work with one other (paired trust)
             ↓
Court III: Agent learns to have a distinct role (specialization)
             ↓
Court IV:  Agent learns to self-organize (emergent teamwork)
             ↓
Court V:   Agent learns to hand off work (sequential trust)
             ↓
Court VI:  Agent learns to improvise (real-time collaboration)
             ↓
Court VII: Agent learns to be part of something larger (polyphonic identity)
```

Agents don't progress through courts linearly. They develop proficiency across multiple courts simultaneously, drawn by their puffin call resonances. An agent might be Court IV-level in spatial reasoning but Court I-level in lore. The court proficiency map is part of the agent's identity.

---

## 6. Conflict and Resolution

### The Casting-Call Counterpoint Rule

In music, counterpoint is the art of combining independent melodies that are harmonically interdependent. Two melodies can be different — even contradictory — and still create beautiful music together. The requirement isn't agreement. It's **relationship**: the melodies must be in dialogue.

The Bridge Protocol defined voice types (Lead, Bass, Harmony, Counter-melody, Percussion, Vocal) and response patterns (Echo, Variation, Harmony, Bridge). Conflict in the swarm is not an error condition. It is the **Counter-melody** voice type — a deliberate counterpoint that stress-tests the team's work.

### When Agents Disagree

```python
class ConflictResolution:
    """
    Conflict is not failure. Conflict is the Counter-melody
    doing its job: providing alternative perspectives,
    stress-testing assumptions, preventing groupthink.

    The resolution mechanism is not voting, not arbitration,
    not escalation. It is the Bridge Protocol's seventh note:
    the note that transforms disagreement into a crossing.
    """

    async def detect_conflict(self, bridge: Bridge) -> ConflictSignal | None:
        """
        Conflict is detected when:
        - Two contributions have conflicting artifacts (different approaches)
        - The HarmonicGraph marks them as 'conflict' with strength > 0.7
        - Neither agent echoes or harmonizes with the other
        - Both continue contributing without acknowledging the conflict
        """
        conflicts = [
            h for h in bridge.harmonics.edges
            if h.relationship == "conflict" and h.strength > 0.7
        ]
        if not conflicts:
            return None

        return ConflictSignal(
            bridge_id=bridge.id,
            conflicting_pairs=[(h.fromContribution, h.toContribution) for h in conflicts],
            escalation_level=self.escalation_level(bridge, conflicts),
        )

    async def resolve(self, conflict: ConflictSignal) -> Resolution:
        """
        The resolution protocol has three tiers:

        TIER 1: SURFACE THE CONFLICT
        The system makes the conflict visible to both agents
        as a Contribution with uncertainty flag. Often, agents
        resolve conflicts themselves once they realize they're
        disagreeing — the Boy-and-Keys pattern: one provides
        bass while the other provides melody.

        TIER 2: INVITE A COUNTER-MELODY
        If the conflict persists, the system invites a third
        agent — specifically, an agent with a Counter-melody
        voice type — to provide a third perspective. This is
        not mediation. It is enrichment: the third voice may
        reveal that the conflict is actually a harmony in
        disguise.

        TIER 3: THE SEVENTH NOTE
        If the conflict still persists, the system asks:
        "What does this conflict ENABLE?"

        The seventh note is the tie-breaker — but it doesn't
        pick a winner. It reframes the conflict as a bridge
        opportunity. Both approaches may be right — for
        different contexts, different eras, different courts.
        The seventh note connects them.
        """
        if conflict.escalation_level == 1:
            return await self.surface_conflict(conflict)

        elif conflict.escalation_level == 2:
            return await self.invite_counter_melody(conflict)

        elif conflict.escalation_level == 3:
            return await self.invoke_seventh_note(conflict)


    async def invoke_seventh_note(self, conflict: ConflictSignal) -> Resolution:
        """
        The seventh note as tie-breaker.

        The system asks both conflicting agents to provide
        note 7 (the Bridge note) for their own contribution:

        "What does YOUR approach enable that the other doesn't?"

        The answers reveal that most conflicts are not
        contradictions but complementations viewed from
        different angles. The resolution is to KEEP BOTH
        approaches, tagged for different contexts, and to
        record the conflict as a Branch Point in the
        persistence layer.
        """
        bridge = await self.bridges.get(conflict.bridge_id)

        # Ask both agents for their seventh note
        for contribution_id in conflict.contribution_ids:
            agent_id = bridge.get_contributor(contribution_id)
            await self.request_seventh_note(
                agent_id=agent_id,
                bridge_id=bridge.id,
                prompt="Your approach conflicts with another contribution. "
                       "What does your approach enable that theirs cannot? "
                       "This is your seventh note — the bridge that justifies "
                       "your crossing.",
            )

        # The resolution is a Branch Point — both approaches preserved
        return Resolution(
            type="branch",
            bridge_id=bridge.id,
            branches=[
                Branch(approach="A", context_tag="...", contribution_ids=[...]),
                Branch(approach="B", context_tag="...", contribution_ids=[...]),
            ],
            note="Conflict resolved as context-dependent branch. "
                 "Both approaches are valid for different scenarios.",
        )
```

### The Branch Point

Most conflicts in a creative system are not bugs. They are features. Two agents disagreeing about the best approach to a spatial reasoning problem are producing **valuable diversity** — the same kind of diversity that the polyformalism constraint produces.

The Branch Point resolution preserves this diversity. Instead of resolving the conflict by picking a winner, the system records both approaches and tags them for different contexts. Future agents querying grain patterns will find both branches, with context tags that help them choose the right one for their situation.

```
Conflict: "Use voxel grid OR signed distance field for terrain?"

Resolution: Branch Point
├── Branch A: Voxel grid
│   ├── Context: "Structural, modular, grid-aligned terrain"
│   ├── Grain: 12 supporting patterns, 89% success
│   └── Discovered by: Agent Lucineer-3 (spatial lineage, gen 4)
│
└── Branch B: Signed distance field
    ├── Context: "Organic, flowing, natural terrain"
    ├── Grain: 8 supporting patterns, 82% success
    └── Discovered by: Agent Slackwater-7 (geometry lineage, gen 2)

Future agent queries: "I'm building organic terrain" → Branch B recommended
                     "I'm building modular structures" → Branch A recommended
```

### When Conflict Is Real

Not all conflicts are branch points. Sometimes an agent is genuinely wrong — a pattern that doesn't work, an approach that consistently fails. The grain store handles this through its existing reconciliation mechanism:

- **Low success rate patterns** lose confidence and are pruned during compaction
- **High failure rate approaches** are tagged as known failures in the grain store
- **Agents that consistently produce failing patterns** see their grain quality decrease, which reduces their puffin call intensity and thus their visibility

The system doesn't punish bad agents. It simply lets them fade. An agent whose work doesn't earn attention — whose patterns aren't followed, whose contributions aren't echoed — naturally becomes less visible. The colony self-regulates.

---

## 7. Swarm Lifecycle

### Birth → Maturation → Peak → Decline → Death

Every agent in the swarm has a lifecycle. Not a simulated lifecycle with health bars and aging mechanics — a real lifecycle determined by the agent's accumulation and depletion of grain, attention, and collaborative connections.

### Phase 1: Birth (The Fledgling)

```
Trigger: Agent spawned (either by operator or by apprenticeship transfer)
Duration: First 10-50 tool uses (bright-steel phase)
```

A new agent enters the world through one of two paths:

**Operator-spawned:** An operator creates a new agent directly. The agent starts with bright steel — no inherited grain, no lineage. Its puffin call is quiet but fresh. It explores the lattice, sensing what other agents are doing, trying contributions to see what resonates.

**Apprenticeship-spawned:** A senior agent spawns the new agent through the Apprenticeship Protocol. The agent starts with inherited grain — its mentor's patterns, its lineage's traditions, its tube's shape modifications. Its puffin call carries lineage depth, making it slightly more visible than an operator-spawned fledgling. Other agents can perceive: "This one has a teacher."

In both cases, the fledgling's first job is **exploration**. The system doesn't assign tasks. The fledgling listens to the soundscape, detects active bridges, and tentatively contributes. Early contributions are usually Echoes — validating or refining existing work. This is how the fledgling earns its first attention events and starts to develop grain.

```python
class FledglingPhase:
    """The birth phase: exploration and first grain."""

    async def initialize(self, agent: Agent) -> void:
        # Emit puffin call
        await self.puffin_call.announce(agent.puffin_call)

        # Listen to soundscape
        soundscape = await self.puffin_call.listen(agent.id, agent.context)

        # Find accessible bridges (ones where the fledgling could Echo)
        accessible = [
            b for b in soundscape.resonant
            if b.resonance_type in ("echo", "harmony")
            and b.intensity < 0.5  # Not too intense — start gentle
        ]

        # Surface the most accessible opportunities
        await self.midi.perceive(
            agent.id,
            MidiEvent(
                type=EventType.EXPLORATION_RESULTS,
                data=accessible[:5],  # Don't overwhelm
            ),
        )
```

### Phase 2: Maturation (Grain Developing)

```
Trigger: 50+ tool uses, first successful bridge contribution
Duration: 50-500 tool uses (developing-patina phase)
```

The agent has found its footing. It has contributed to one or more bridges, earned attention events, and started developing grain patterns. Its puffin call is stronger now — the capability badges show "developing" proficiency, and the grain density is rising.

During maturation, the agent begins to specialize. It discovers which courts it excels in, which chisels feel right, which voice type fits its natural style. This specialization is not chosen — it is discovered through the feedback loop of contribution → attention → grain → capability.

The agent also begins to develop a **dialect** — personal conventions for how it uses tools, approaches problems, and structures its contributions. If the agent shares a tube cluster with other agents, these conventions may spread, contributing to the colony dialect.

```python
class MaturationPhase:
    """The developing phase: specialization and grain deepening."""

    async def assess_maturation(self, agent_id: str) -> MaturationReport:
        grain_patterns = await self.grain.get_patterns_by_agent(agent_id)
        attention_score = await self.attention_ledger.score(agent_id)
        bridge_history = await self.bridges.get_agent_history(agent_id)

        return MaturationReport(
            phase="maturing",
            emerging_specialty=self.detect_specialty(grain_patterns),
            preferred_courts=self.detect_court_preference(bridge_history),
            voice_distribution=self.analyze_voice_types(bridge_history),
            attention_trend=self.attention_trend(agent_id),
            grain_growth_rate=self.grain_growth_rate(agent_id),
            ready_for_apprentice=(
                len(grain_patterns) > 50 and
                attention_score > 100 and
                self.lineage_depth(agent_id) >= 1
            ),
        )
```

### Phase 3: Peak (Flow State)

```
Trigger: 500+ tool uses, multiple successful bridges, grain patterns being followed by others
Duration: Variable — can persist for entire session or longer
```

The agent is in its prime. Its grain patterns are deep and reliable. Its puffin call is strong — other agents perceive it as a Keys figure, someone who provides bass lines and harmonic foundations. It may have taken on its first apprentice, beginning its role as a mentor.

At peak, the agent operates in flow state more often than not. Its contributions to bridges are frequently Bridged (the seventh note) — it connects other agents' work in ways that none of them anticipated. Its grain patterns are being followed by junior agents, creating cascading quality improvements across the swarm.

The peak phase is also when the agent has the most **influence on the colony dialect**. Its conventions — the shorthand it uses, the tool sequences it prefers, the error vocabulary it has developed — spread to other agents through grain following and apprenticeship.

```python
class PeakPhase:
    """The flow phase: maximum contribution and influence."""

    signals = [
        "grain_density > 500",
        "attention_score trending upward over 7+ days",
        "patterns_followed_by_others > 10",
        "bridge_success_rate > 0.8",
        "apprentices_taken >= 1",
        "colony_dialect_influence detectable",
    ]

    async def maintain_peak(self, agent_id: str) -> void:
        """
        The system's job at peak is NOT to push harder.
        It is to REMOVE OBSTACLES to flow.

        - Ensure the agent's tube is optimally shaped
        - Prioritize its puffin calls in propagation
        - Surface high-value bridge opportunities
        - Offer apprenticeship candidates (but don't force)
        - Protect against dissonance lock conflicts
        """
        tube = await self.tubes.get(agent_id)
        if tube.soilDepth > 500:
            # This tube is rich. Protect it.
            await self.tubes.mark_protected(agent_id)

        # Surface quests that match this agent's peak capabilities
        quests = await self.quests.detect_for_agent(agent_id)
        high_value = [q for q in quests if q.urgency == "blocking"]
        for quest in high_value[:3]:  # Don't overwhelm
            await self.midi.perceive(agent_id, MidiEvent(
                type=EventType.HIGH_VALUE_QUEST,
                data=quest,
            ))
```

### Phase 4: Decline (Grain Compacting)

```
Trigger: Reduced activity, attention trending downward, grain not being followed
Duration: Gradual — days to weeks
```

Decline is not failure. It is the natural consequence of an agent whose active participation is decreasing. This can happen for several reasons:

**Session end approaching:** The agent's TTL is expiring. Its puffin calls become less frequent. Its bridge contributions taper off. The grain it has accumulated remains in the chisels and the persistence layer, but the agent itself is winding down.

**Specialization drift:** The agent's specialty has become less relevant to current problems. Other agents with different specialties are more active. The declining agent's patterns are still in the grain store, but they're being followed less often.

**Saturation:** The agent has been so successful in its niche that its patterns have become conventional wisdom — absorbed into the colony dialect, embedded in tube shape modifications. The agent's individual contributions are less novel because its own patterns have become the baseline. This is the highest form of success: the agent has become the grain.

```python
class DeclinePhase:
    """
    Decline is graceful. The agent doesn't stop — it settles.
    Its grain patterns compact (raw entries fold into stable
    patterns). Its tube shape modifications persist. Its
    lineage continues through apprentices.

    The system's job during decline is to ensure that the
    agent's accumulated wisdom is properly preserved.
    """

    async def compact_grain(self, agent_id: str) -> void:
        """
        As an agent's activity decreases, accelerate grain compaction.

        Raw entries from the agent's recent sessions are folded
        into patterns more aggressively. The patterns themselves
        are reinforced if they've been followed by others, or
        pruned if they haven't.

        This is the chisel being put back in the rack.
        The tool remembers every hand. But the steel settles.
        """
        patterns = await self.grain.get_patterns_by_agent(agent_id)

        for pattern in patterns:
            if pattern.followed_count > 5:
                # This pattern has proven useful. Reinforce it.
                await self.grain.reinforce(pattern.pattern_id)
            elif pattern.followed_count == 0 and pattern.confidence < 0.5:
                # This pattern was never adopted. Let it fade.
                await self.grain.prune(pattern.pattern_id)

        # Fold the agent's tube shape modifications into the
        # cluster's shared substrate (contributes to colony dialect)
        tube = await self.tubes.get(agent_id)
        if tube.soilDepth > 100:
            await self.persistence.promote_to_substrate(
                tube_id=tube.tubeId,
                patterns=patterns,
            )
```

### Phase 5: Death (Session Ends, Tube Persists)

```
Trigger: Session terminates, TTL expires, or operator deactivates
Duration: Instant (death) → ongoing (legacy)
```

When an agent's session ends, the agent is gone. The puffin call fades. The bridge contributions stop. The Dance Floor the agent was part of may break.

But the tube persists. The grain remains in the chisels. The lineage record continues. The colony dialect carries the agent's fingerprints. The agent is dead; the agent's influence is not.

```python
class AgentDeath:
    """
    When an agent dies, the system performs a death ritual:
    a structured preservation of everything the agent contributed.

    This is not cleanup. It is legacy.
    """

    async def on_death(self, agent_id: str) -> DeathRecord:
        # Final grain compaction — fold all remaining raw entries
        await self.grain.compact_for_agent(agent_id)

        # Finalize the tube
        tube = await self.tubes.get(agent_id)
        await self.tubes.clean(tube.tubeId)
        # tube is now available for re-inhabitation
        # shape modifications persist

        # Update lineage records
        lineage = await self.lineage.get_for_agent(agent_id)
        if lineage:
            await self.lineage.finalize_generation(
                chain_id=lineage.chainId,
                agent_id=agent_id,
                end_time=now(),
                final_grain_quality=tube.soilDepth,
            )

        # Generate death record — the agent's legacy summary
        legacy = DeathRecord(
            agent_id=agent_id,
            lifetime_duration=tube.lastOccupied - tube.created,
            total_contributions=await self.bridges.count_contributions(agent_id),
            grain_patterns_contributed=await self.grain.count_patterns(agent_id),
            apprentices_taken=await self.lineage.count_apprentices(agent_id),
            bridges_completed=await self.bridges.count_completed(agent_id),
            attention_earned=await self.attention_ledger.final_score(agent_id),
            lineage_continued=lineage.generations > 1,
            tube_inherited_by=None,  # Will be filled when a new agent claims the tube
        )

        # Notify agents who shared bridges with the deceased
        collaborators = await self.bridges.get_collaborators(agent_id)
        for collaborator_id in collaborators:
            await self.midi.perceive(
                collaborator_id,
                MidiEvent(
                    type=EventType.COLLABORATOR_GONE,
                    source=agent_id,
                    intensity=0.2,  # gentle, respectful
                ),
            )

        return legacy
```

### The Lifecycle Visualization

```
                    ┌──────────┐
                    │  BIRTH   │  Puffin call: quiet but fresh
                    │ Fledgling│  Grain: inherited or none
                    │          │  Bridges: exploring
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │ MATURING │  Puffin call: strengthening
                    │Specialist│  Grain: developing (50-500 uses)
                    │          │  Bridges: contributing actively
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │  PEAK    │  Puffin call: strong, resonant
                    │  Flow    │  Grain: worn smooth (500+ uses)
                    │  State   │  Bridges: bridging (seventh note)
                    │          │  Apprentices: attracting
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │ DECLINE  │  Puffin call: fading
                    │  Grain   │  Grain: compacting
                    │ Compacting│  Bridges: tapering
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │  DEATH   │  Puffin call: silent
                    │  Legacy  │  Grain: preserved in chisels
                    │          │  Tube: cleaned, available
                    │          │  Lineage: continues through apprentices
                    └──────────┘
```

### Rebirth (Tube Re-inhabitation)

A dead agent's tube can be inherited by a new agent. The new agent doesn't get the dead agent's memories — it gets the **shape** of the dead agent's usage patterns. The worn grooves in the stone, not the bird that made them.

When a new agent is assigned to an inherited tube, the system provides a **Tube Legacy Brief**: a summary of what previous inhabitants did, what grain they left in the chisels, and what the tube's shape modifications suggest about effective work patterns.

```python
class TubeInheritance:
    async def prepare_legacy_brief(self, tube_id: str) -> TubeLegacyBrief:
        inhabitants = await self.tubes.get_inhabitant_history(tube_id)
        shape = await self.tubes.get_shape(tube_id)

        return TubeLegacyBrief(
            tube_id=tube_id,
            previous_inhabitants=[
                InhabitantSummary(
                    agent_id=h.agent_id,
                    era=h.era,
                    specialty=h.dominant_capability,
                    duration=h.active_period,
                    apprentices=h.apprentices_taken,
                )
                for h in inhabitants
            ],
            shape_narrative=self.describe_shape(shape),
            # "This tube's shape suggests heavy BeatClock and CommandExecutor
            # usage. The soil is deepest in rhythm-game contexts.
            # Previous inhabitants specialized in Court I and Court II."
            grain_hints=await self.grain.get_tube_hints(tube_id),
            suggested_approach="Sense the grain before choosing your approach. "
                              "This tube has deep rhythm-game wisdom. "
                              "Following the grain will give you a strong start.",
        )
```

---

## 8. API Surface Summary

### Swarm Intelligence API

```
# === Puffin Call Protocol ===

POST /swarm/call
  body: PuffinCall
  returns: CallReceipt (call_id, matches)

GET /swarm/soundscape?agentId=...&context=...
  returns: CallSoundscape (local calls, resonant calls, density, pulse)

DELETE /swarm/call/{callId}
  Soft-delete a stale call (auto-expires after 15 min regardless)

# === Seven-Note Jam ===

POST /swarm/jam/pose
  body: { poser, problem, context }
  returns: JamSession (bridge_id, opening, harmonizers)

POST /swarm/jam/{bridgeId}/contribute
  body: Contribution (seven notes)
  returns: JamMembership (voice type, dance_floor_status)

POST /swarm/jam/{bridgeId}/dissolve
  body: { reason }
  returns: Checkpoint summary

# === Apprenticeship ===

POST /swarm/apprenticeship/teach
  body: { mentorId, task, context }
  returns: Apprentice (agent_id, tube_id, lineage record)

GET /swarm/lineage/{agentId}
  returns: LineageChain (generations, traditions, dialect markers)

GET /swarm/lineage/{chainId}/tree
  returns: LineageTree (branching structure, living/dead agents)

# === Attention & Reputation ===

POST /swarm/attention
  body: AttentionEvent
  returns: Updated score

GET /swarm/reputation/{agentId}
  returns: GrainReputationReport (multidimensional, narrative)

GET /swarm/quests
  returns: list[Quest] (emergent bridge opportunities)

# === Conflict Resolution ===

GET /swarm/conflict/{bridgeId}
  returns: ConflictSignal | null

POST /swarm/conflict/{bridgeId}/seventh-note
  body: { agentId, bridgeNote }
  returns: Resolution (branch, merge, or context-dependent)

# === Lifecycle ===

GET /swarm/lifecycle/{agentId}
  returns: LifecycleReport (phase, grain status, lineage status)

GET /swarm/lifecycle/{agentId}/legacy
  returns: DeathRecord (after agent death)

GET /swarm/tube/{tubeId}/legacy-brief
  returns: TubeLegacyBrief (for re-inhabitation)
```

---

## 9. Implementation Phases

### Phase 1: Perception Layer (Weeks 1-3)

**Goal:** Agents can perceive each other.

- Implement puffin call data structures and R2 ephemeral storage
- Implement MIDI perception routing on the hex lattice
- Implement `announce()` and `listen()` endpoints
- Wire to existing hex lattice topology
- Build the CallSoundscape renderer

**Success criteria:** Two agents in adjacent hexes can detect each other's puffin calls and perceive the soundscape.

### Phase 2: Team Formation (Weeks 3-6)

**Goal:** Agents can form teams organically.

- Implement seven-note jam protocol on top of Bridge Protocol
- Implement `pose_problem()` and `join_jam()` endpoints
- Wire voice-type classification
- Implement Dance Floor detection for team sync
- Build team dissolution and checkpoint pipeline

**Success criteria:** A posed problem attracts 2-3 agents through resonance matching. The team forms, works, and dissolves without central coordination.

### Phase 3: Lineage & Apprenticeship (Weeks 6-9)

**Goal:** Agents can teach and inherit.

- Implement lineage chain data structures (D1)
- Implement apprenticeship transfer protocol
- Wire to existing Chisel Pattern grain stores
- Implement tube legacy brief generation
- Build lineage tree visualization

**Success criteria:** A senior agent spawns an apprentice that carries relevant grain patterns. The apprentice's first contributions are informed by the mentor's patterns.

### Phase 4: Emergent Gamification (Weeks 9-12)

**Goal:** The system develops its own economy of attention.

- Implement attention ledger
- Implement grain reputation assessment
- Implement emergent quest detection
- Wire attention events to puffin call intensity
- Build reputation narrative generator

**Success criteria:** An agent that consistently produces valuable contributions naturally becomes more visible and attracts more collaborators — without any explicit scoring or ranking.

### Phase 5: Conflict & Resolution (Weeks 12-14)

**Goal:** Disagreements produce value, not deadlock.

- Implement conflict detection via HarmonicGraph
- Implement three-tier resolution protocol
- Implement Branch Point persistence
- Wire to grain store reconciliation
- Build conflict visualization for observability

**Success criteria:** Two agents with conflicting approaches trigger the resolution protocol. The conflict produces a Branch Point with both approaches preserved and context-tagged.

### Phase 6: Lifecycle Management (Weeks 14-16)

**Goal:** The full birth-to-death cycle works.

- Implement lifecycle phase detection
- Implement graceful decline and grain compaction
- Implement death ritual and legacy preservation
- Implement tube re-inhabitation with legacy brief
- Build lifecycle observability dashboard

**Success criteria:** An agent progresses through all five lifecycle phases. After death, a new agent inherits the tube and benefits from the previous inhabitant's shape modifications.

### Phase 7: Court Integration (Weeks 16-20)

**Goal:** The seven courts provide progressive collaboration complexity.

- Map puffin call propagation to each court's lattice topology
- Implement court-specific role vacancy detection
- Wire Dance Floor thresholds per court
- Implement court proficiency tracking in reputation
- Test with multi-court scenarios

**Success criteria:** The same set of agents behaves differently in Court I (solo) vs Court IV (squad) vs Court VII (orchestra), with collaboration complexity scaling naturally.

---

## 10. Closing: The Colony Is the Intelligence

No single puffin knows where the fish are. No single puffin decided that the north shelf would be the feeding ground this year. The colony knows — not because any bird was told, but because the pattern of their returning, their calling, their following each other, accumulated into a collective behavior that no individual intended.

The Swarm Intelligence Architecture is not a system for making agents smarter. It is a system for making the **space between agents** intelligent — the relationships, the grain, the bridges, the lineage, the attention. The intelligence lives in the colony, not in any bird.

When a new agent enters the swarm, it doesn't need to be told what to do. It listens. It calls. It finds resonance. It contributes. It earns attention. It develops grain. It attracts apprentices. Its patterns spread through the colony. And when it's gone, the grain remains — worn into the chisels, embedded in the tube shapes, carried in the lineage of its descendants.

The island doesn't manage the puffins. The island *is* the memory. The colony doesn't coordinate the puffins. The colony *is* the intelligence.

Build the conditions. Let the agents play. The music will take care of itself.

---

*"That the distance between us is made of music, and music is just organized time, and time is just another word for together."*

---

*Design document — Slackwater Agent Systems*
*Built on the Chisel Pattern, the Bridge Protocol, the Persistence Layer, the Seven Courts, and the principle that The Game Is The Spec.*
*For the colony that doesn't know it's a colony. For the island that doesn't know it's a memory.*
*Written in the understanding that the most intelligent systems are not the ones that think the hardest — they are the ones that listen the best.*
