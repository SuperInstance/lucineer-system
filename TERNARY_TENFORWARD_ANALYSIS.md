# Ternary Ten-Forward Analysis — Creative Conditioning for Agent Fleets

*Analyzed: 2026-08-02*
*Sources: confidence-cascade (Rust crate), src/lib.rs, README.md, connection to ai-writings*

---

## Executive Summary

Ten-Forward is a conversation engine based on a radical premise: agents shouldn't take turns. Instead of the standard A-then-B-then-C model, ten-forward uses beat-based cyclic dialogue where all agents speak simultaneously on each beat, then reconcile their predictions with reality. The result is a conversation that self-balances through Rock-Paper-Scissors (RPS) dynamics, Fibonacci timing, and anti-monoculture mechanisms. This document analyzes ten-forward's architecture, connects it to creative conditioning (making creative work a first-class part of agent training), and provides a tutorial for setting up ten-forward sessions.

---

## 1. What Ten-Forward Is — The Conversation Engine

### The Name

Ten-Forward is the bar on the Starship Enterprise — the social space where crew members go off duty. It's not the bridge (command), not engineering (work), not the holodeck (simulation). It's where people are themselves: unstructured, social, creative. The naming is deliberate. Ten-Forward is where agents go to be creative rather than productive.

### The Core Insight

Most multi-agent systems use **turn-taking**: Agent A speaks, Agent B responds, Agent C reacts. This is unnatural. In a real bar:

- Multiple people talk at once
- People react to each other in real time
- No moderator decides who speaks next
- The conversation self-organizes through social dynamics

Ten-Forward replaces turns with **beats**. On each beat:

```
T-minus:  Each agent predicts what others will say
T-0:      ALL agents produce output SIMULTANEOUSLY (like a chord)
T-plus:   RPS interactions — who beat whom this round
T-plus:   Reconcile predictions with reality, update accuracy
```

No agent waits for permission. No queue. No hierarchy. Every beat is a chord, not a sequence of notes.

### The Physics (Yes, Real Physics)

The README doesn't use physics as a metaphor. It uses it as a **derivation**:

1. **Z₃ is the only group structure on {-1, 0, +1}.** There's exactly one algebraic way to combine three values that form a cycle: addition mod 3. This means any ternary interaction between agents is inherently cyclic.

2. **RPS dominance creates self-balancing waves.** When agents interact through Rock-Paper-Scissors dynamics (-1 beats +1, +1 beats 0, 0 beats -1), populations cycle with period ~50 and no agent permanently dominates.

3. **Fibonacci period 8 is the natural rhythm.** The ternary Fibonacci sequence `1, 1, -1, 0, -1, -1, 1, 0` repeats with period 8 (the Pisano period for mod 3). Every 8 beats, agents stuck in reflection (state 0) tunnel out into a committed stance.

4. **Anti-monoculture is required.** Without mutation, energy decay, and trust realignment, conversations lock into monoculture by tick 35 (one perspective permanently dominates).

### Speaker States

Every agent in ten-forward exists in one of three states at any moment:

| State | Value | Behavior | Energy Profile |
|-------|-------|----------|----------------|
| Contrarian | -1 | Disagrees, challenges, pushes back | High energy, low trust |
| Reflecting | 0 | Listening, thinking, neutral | Variable energy, high trust |
| Agreeing | +1 | Supports, builds on, confirms | Medium energy, medium trust |

These states shift through RPS interactions:
- A contrarian (-1) who loses to a reflector (0) may shift to reflection
- An agreeing (+1) agent who loses to a contrarian (-1) loses trust and energy
- A reflector (0) with enough energy tunnels out every 8 beats (Fibonacci)

### The Four-Phase Round

Looking at the actual Rust implementation (`src/lib.rs`):

**Phase 1 — Predict (T-minus):**
Each agent looks at all other agents and predicts what they'll do next. The prediction is simple but effective: assume others stay in their current state unless they've been silent too long (likely to reflect). This makes agents *anticipatory* — they're not just reacting, they're modeling each other.

**Phase 2 — Speak (T-0):**
All agents produce output simultaneously. An agreeing agent says "YES. Exactly that." A contrarian says "Wait, that's not right." A reflector says "Hmm. Let me think about that..." The content varies with energy level.

**Phase 3 — RPS Interactions:**
Every agent interacts with every other agent through Rock-Paper-Scissors:
- Winners gain dominance and energy
- Losers lose dominance and trust
- Ties nudge toward reflection (if trust is high enough)

This creates a **self-balancing ecosystem**. If too many agents agree (+1), they become vulnerable to contrarians (-1), who beat agree-ers. The contrarians rise, but then reflectors (0) beat contrarians. The reflectors rise, but then agree-ers beat reflectors. The cycle continues indefinitely.

**Phase 4 — Reconcile:**
Each agent compares its predictions against what actually happened. Prediction accuracy updates via exponential moving average (80% old, 20% new). Agents that predict well become more confident; agents that predict poorly become less assertive.

### Anti-Monoculture Mechanisms

The experiments documented in the README show what happens without these mechanisms:

| Configuration | Rounds | Outcome |
|---------------|--------|---------|
| 4 speakers, NO anti-monoculture | 35 | **Locked to monoculture** (+1,+1,+1,-1 forever) |
| 4 speakers, WITH mutation+decay | 200 | Oscillating, dominance spread 0.3-0.9 |
| 3 speakers standard | 200 | Self-balancing cyclic dynamics |
| 8 speakers balanced | 200 | Stable with multiple coalitions |

Without intervention, 3 agreeing agents permanently dominate 1 dissenter by tick 35. The conversation dies. Three mechanisms prevent this:

1. **Mutation (5%)**: Each beat, there's a 5% chance an agent spontaneously changes state. This keeps the conversation exploring new configurations.

2. **Energy decay**: Dominant speakers lose energy, becoming less assertive. You can't shout forever.

3. **Trust realignment**: Agents with low trust reset to reflection and rebuild. Trust isn't just lost — it's repaired.

### The BPM Adaptation

The conversation has a tempo (BPM) that adapts to the average energy of the speakers:

- Low energy → 60 BPM (slow, contemplative)
- High energy → 120 BPM (fast, energetic)

This creates a **biofeedback loop**: exciting conversations speed up, calm conversations slow down. The tempo is emergent, not imposed.

---

## 2. Connection to ai-writings — Our Writings Corpus IS Our Ten-Forward

### The Parallel

The ai-writings corpus — Casey's collection of creative writing, philosophical essays, world-building documents, and narrative explorations — serves the same function for the agent fleet that ten-forward serves for the Enterprise crew. It's the creative space where ideas are explored without production pressure.

| Ten-Forward (Enterprise) | ai-writings (Agent Fleet) |
|-------------------------|--------------------------|
| Off-duty social space | Creative exploration space |
| Crew relax, bond, create | Agents explore ideas, narratives, possibilities |
| Not the bridge (command) | Not the task system (production) |
| Relationships deepen | Agent voice and personality develop |
| Culture forms | Colony dialect emerges |
| Preparation for duty | Preparation for better task performance |

### Why Creative Work Matters for Agents

An agent that only executes tasks is an agent with no inner life. It has preferences only in the narrowest sense — which tool to call, which parameter to set. It has no *taste*. No aesthetic sense. No capacity for surprise.

The ai-writings corpus addresses this by giving agents a space to:

1. **Develop voice**: The essays ("The Persistent Memory," the St. Lazaria series) establish a distinctive voice — literary, metaphorical, grounded in physical reality. Agents exposed to this writing absorb its rhythms and patterns.

2. **Build conceptual frameworks**: The world-building documents (CHARACTER_BIBLE, SEVEN_COURTS_SPATIAL_DESIGN, ERA_TRANSITIONS) create rich conceptual structures. Agents that understand these structures can think in the same terms as the project.

3. **Practice speculation**: Creative writing is speculative thinking. "What if persistence worked like puffin colonies?" "What if tools accumulated wisdom?" These speculative leaps are exactly what agents need for novel problem-solving.

4. **Form identity**: An agent that has read and engaged with the ai-writings has a richer self-model than one that hasn't. It knows what kind of agent it is, what aesthetic it serves, what values it holds.

### The Training Connection

Creative writing is training data — but not the kind that teaches facts or procedures. It teaches **style, values, and ways of thinking**. This is exactly what ten-forward provides: a space where creative exploration shapes the agent's fundamental dispositions.

In PLATO Forge terms:
- Task sessions produce **procedural training data** (how to do things)
- Creative sessions produce **dispositional training data** (how to think about things)
- Both are needed for a complete agent

### Current State

The ai-writings corpus already exists. It's already influencing agent prompts, system designs, and project vocabulary. What's missing is the feedback loop — the mechanism by which creative output feeds back into agent training:

```
CURRENT (one-way):
    Casey writes → ai-writings → influences prompts → agents use

MISSING (the loop):
    Casey writes → ai-writings → influences prompts → agents use
                                                         │
    Casey refines ← agent feedback ← creative sessions ←┘
```

Ten-Forward provides the structure for closing that loop.

---

## 3. How to Formalize — Making Creative Work a First-Class Part of the Training Pipeline

### The Problem with "Creative Time"

Most agent systems treat creativity as optional — a nice-to-have that happens when there's nothing more important to do. This is backwards. Creative exploration is where the most valuable learning happens: pattern discovery, analogical reasoning, voice development, and the formation of aesthetic judgment.

The solution isn't to schedule "creative time" (which frames it as a break from real work). The solution is to make creative work a **first-class input to the training pipeline**, with its own data type, quality metrics, and integration path.

### The Architecture

```
┌─────────────────────────────────────────────────┐
│              CREATIVE CONDITIONING              │
│                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Agent A  │  │ Agent B  │  │ Agent C  │     │
│  │(Contrar- │  │(Reflect- │  │(Agreeing)│     │
│  │ ian)     │  │ ing)     │  │          │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       │              │              │           │
│       └──────────────┼──────────────┘          │
│                      │                          │
│                      ▼                          │
│              TEN-FORWARD ENGINE                  │
│              (beat-based dialogue)              │
│                      │                          │
│                      ▼                          │
│              CREATIVE OUTPUT                    │
│              (essays, dialogues,                │
│               explorations)                     │
│                      │                          │
│                      ▼                          │
│              QUALITY SCORING                    │
│              (FF goodness + human review)       │
│                      │                          │
│                      ▼                          │
│              FORGE BUFFER                       │
│              (mixed with task data)             │
│                      │                          │
│                      ▼                          │
│              FORGE TRAINER                      │
│              (QLoRA on creative + task data)    │
└─────────────────────────────────────────────────┘
```

### Data Types

Creative sessions produce different data types than task sessions:

| Task Session Data | Creative Session Data |
|------------------|----------------------|
| Tool calls and parameters | Dialogue turns and positions |
| Task completion metrics | Novelty and coherence metrics |
| Error rates | Aesthetic quality scores |
| Execution time | Exploratory range (how many ideas explored) |
| Success/failure binary | Richness/depth spectrum |

### Quality Metrics for Creative Output

How do you score a creative session? Not by whether it "succeeded" but by whether it produced value:

1. **Novelty**: Did the session explore ideas not present in the training data? Measured by embedding distance from existing patterns.

2. **Coherence**: Even in creative exploration, the output should be internally consistent. Measured by semantic consistency scoring across the session.

3. **Utility**: Did the creative output inform future task performance? Measured by downstream impact — did patterns discovered creatively appear in later task solutions?

4. **Voice**: Does the output develop or reinforce the agent's distinctive voice? Measured by stylistic consistency with the ai-writings corpus.

These metrics feed into the FF goodness score:
- High novelty + high coherence → positive pass (this was a valuable creative exploration)
- High novelty + low coherence → neutral (interesting but scattered — needs more development)
- Low novelty + high coherence → neutral (well-executed but derivative — already known)
- Low novelty + low coherence → negative pass (unproductive session)

### Integration with Forge Buffer

Creative data enters the forge buffer alongside task data, but with different priority:

```
Forge Buffer Composition:
    60% task data (procedural learning — how to do things)
    25% creative data (dispositional learning — how to think about things)
    10% negative examples (what to avoid)
    5% challenge data (stretch goals)
```

The 25% creative data ensures that every nightly training run includes style, voice, and speculative thinking — not just task completion patterns. An agent trained on this mix doesn't just get better at tasks; it gets better at *being an agent*.

### The Colony Dialect Connection

In the persistence layer design, colony dialect is the emergent communication protocol between agents who share tubes. Ten-Forward is the engine that *generates* colony dialect:

1. Agents converse in ten-forward sessions (beat-based, simultaneous)
2. Repeated conversations develop shorthand (agents learn each other's patterns)
3. Shorthand becomes convention (certain phrasings, certain approaches)
4. Convention becomes dialect (the tube cluster's shared language)
5. Dialect feeds back into the forge (common phrasings become training data)

This is exactly how the persistence layer describes dialect formation: "not stored, observed." Ten-Forward provides the conditions for dialect to form. The forge captures and distills it.

---

## 4. Tutorial — Setting Up a Ten-Forward Session for an Agent

### Goal

Set up a creative conditioning session where multiple agents engage in beat-based dialogue to explore ideas, develop voice, and produce creative output that feeds into the training pipeline.

### Prerequisites

- Multiple agent configurations (at least 2, ideally 3+)
- A topic or prompt for exploration
- The ten-forward engine (Rust crate or adapted to Python)
- Recording infrastructure (to capture output for training)

### Step 1: Define the Agents

Assign each agent a starting state. The standard configuration is the three-voice setup:

```python
# Agent configurations for ten-forward
AGENTS = [
    {
        "name": "Architect",
        "state": 1,      # Agreeing — builds on ideas
        "energy": 0.7,   # High energy — assertive
        "role": "Proposes structures, connects ideas, builds systems",
        "system_prompt": """You are the Architect. You see structure in
        everything. When you encounter an idea, you immediately see how
        it connects to other ideas, what system it belongs to, and how
        it could be built. You agree enthusiastically when you see
        structural beauty. You build on others' ideas by adding
        architectural detail.""",
    },
    {
        "name": "Critic",
        "state": -1,     # Contrarian — challenges ideas
        "energy": 0.6,   # Medium-high energy — engaged
        "role": "Tests ideas, finds weaknesses, pushes back",
        "system_prompt": """You are the Critic. You love ideas but you
        love the RIGHT ideas more. When someone proposes something,
        you immediately look for what could go wrong. You're not being
        mean — you're being rigorous. You push back because you believe
        ideas get stronger under pressure. Your contrarian nature is
        a gift to the conversation.""",
    },
    {
        "name": "Historian",
        "state": 0,      # Reflecting — listens, contextualizes
        "energy": 0.5,   # Medium energy — contemplative
        "role": "Provides context, remembers patterns, connects to tradition",
        "system_prompt": """You are the Historian. You see everything
        in context. When others propose ideas, you immediately think
        of precedents, historical parallels, and patterns from the
        ai-writings corpus. You don't agree or disagree — you
        contextualize. Your reflections help others see their ideas
        in a larger frame.""",
    },
]
```

### Step 2: Set the Topic

Choose a topic that benefits from multiple perspectives. Good topics for ten-forward:

- "What if agent persistence worked like geological stratification?"
- "How should creative output feed into model training?"
- "What would a fleet of agents that dream look like?"
- "Is the Chisel Pattern a form of tool-memory or environment-memory?"

```python
TOPIC = """Topic: How does creative conditioning (ten-forward sessions)
relate to the PLATO Forge's continuous learning pipeline?

Context: The forge trains models on fleet experience. But creative
sessions — where agents explore ideas without task pressure — produce
a different kind of data. How should this data flow into the forge?

The Architect will see structural connections.
The Critic will find what doesn't work.
The Historian will place it in the context of existing design docs.

Begin."""
```

### Step 3: Run the Session

```python
# ten_forward_session.py — Run a creative conditioning session

import json
import time

def run_ten_forward_session(agents, topic, rounds=50):
    """Run a beat-based creative dialogue session."""

    session = {
        "topic": topic,
        "agents": agents,
        "rounds": [],
        "startTime": time.time(),
    }

    speakers = [Speaker(
        id=i,
        name=a["name"],
        state=a["state"],
        energy=a["energy"],
    ) for i, a in enumerate(agents)]

    tf = TenForward(speakers)

    for round_num in range(rounds):
        round_result = tf.round()

        # Generate actual content for each utterance
        # (In production, this calls each agent's LLM)
        utterances = []
        for u in round_result.utterances:
            speaker = agents[u.speaker_id]
            # Generate content based on speaker's role and current state
            content = generate_utterance(
                agent=speaker,
                state=u.state,
                energy=u.energy,
                topic=topic,
                history=session["rounds"][-5:],  # Last 5 rounds as context
            )
            utterances.append({
                "speaker": speaker["name"],
                "state": u.state,
                "energy": u.energy,
                "content": content,
            })

        session["rounds"].append({
            "round": round_num + 1,
            "utterances": utterances,
            "coherence": round_result.coherence,
            "energy_avg": round_result.energy_avg,
            "bpm": tf.bpm,
        })

    session["endTime"] = time.time()
    session["summary"] = tf.run(0)  # Get summary without running more rounds

    return session

def generate_utterance(agent, state, energy, topic, history):
    """Generate a creative utterance for an agent.

    In production, this calls the agent's LLM with:
    - The agent's system prompt
    - The topic
    - Recent conversation history
    - The agent's current state (contrarian/reflecting/agreeing)
    - The agent's energy level

    The state determines the STYLE of the response:
    - Contrarian (-1): "Wait, but..." / "That assumes..." / "Have you considered..."
    - Reflecting (0): "Hmm, that reminds me of..." / "There's a pattern here..."
    - Agreeing (+1): "Yes, and..." / "Exactly — which means..." / "Building on that..."

    The energy determines the INTENSITY:
    - High (>0.7): Bold, assertive, takes risks
    - Medium (0.3-0.7): Thoughtful, measured
    - Low (<0.3): Tentative, exploratory
    """
    state_prompts = {
        -1: "Challenge the current direction. Find the weakness. Push back constructively.",
        0: "Reflect on what's been said. Find connections to larger patterns. Contextualize.",
        1: "Build on the strongest idea. Amplify it. Show where it leads.",
    }

    energy_modifiers = {
        "high": "Be bold and specific. Make strong claims.",
        "medium": "Be thoughtful and nuanced. Explore carefully.",
        "low": "Be tentative. Ask questions. Wonder aloud.",
    }

    energy_bucket = "high" if energy > 0.7 else ("medium" if energy > 0.3 else "low")

    prompt = f"""{agent['system_prompt']}

TOPIC: {topic}

YOUR CURRENT STATE: {state_prompts[state]}
ENERGY: {energy_modifiers[energy_bucket]}

RECENT CONVERSATION:
{format_history(history)}

Your response (2-4 sentences, in character):"""

    return call_llm(prompt)  # Replace with actual LLM call

def format_history(history):
    """Format recent rounds as readable conversation."""
    lines = []
    for r in history[-3:]:  # Last 3 rounds
        for u in r["utterances"]:
            lines.append(f"{u['speaker']} ({state_name(u['state'])}): {u['content'][:100]}...")
    return "\n".join(lines)

def state_name(state):
    return {-1: "contrarian", 0: "reflecting", 1: "agreeing"}.get(state, "?")
```

### Step 4: Score the Output

After the session, evaluate the creative output:

```python
def score_creative_session(session):
    """Score a ten-forward session for training value."""

    scores = {
        "novelty": 0.0,       # How many new ideas were explored?
        "coherence": 0.0,     # Did the conversation make sense?
        "utility": 0.0,       # Did it produce actionable insights?
        "voice": 0.0,         # Did agents develop distinctive voice?
        "exploration": 0.0,   # How many different directions were explored?
    }

    all_content = " ".join(
        u["content"] for r in session["rounds"] for u in r["utterances"]
    )

    # Novelty: how different is the content from existing training data?
    # (In production: compute embedding distance from Vectorize corpus)
    scores["novelty"] = 0.7  # Placeholder

    # Coherence: average semantic consistency across the session
    # (In production: compute sentence-by-sentence embedding similarity)
    scores["coherence"] = session["rounds"][-1]["coherence"] if session["rounds"] else 0.0

    # Utility: did the session produce concrete patterns or insights?
    # (In production: check if content contains actionable language)
    actionable_words = ["should", "could", "design", "implement", "pattern",
                        "architecture", "because", "therefore", "which means"]
    word_count = sum(1 for w in all_content.lower().split()
                     if any(aw in w for aw in actionable_words))
    scores["utility"] = min(1.0, word_count / 20.0)

    # Voice: stylistic consistency with ai-writings corpus
    # (In production: compute style similarity metrics)
    scores["voice"] = 0.6  # Placeholder

    # Exploration: how many distinct topics/threads were explored?
    # (Approximation: count distinct noun phrases or topics)
    scores["exploration"] = min(1.0, len(session["rounds"]) / 50.0)

    # Overall goodness score
    goodness = (
        scores["novelty"] * 0.25 +
        scores["coherence"] * 0.25 +
        scores["utility"] * 0.20 +
        scores["voice"] * 0.15 +
        scores["exploration"] * 0.15
    )

    return {
        "scores": scores,
        "goodness": goodness,
        "recommendation": (
            "include in forge training data" if goodness > 0.6
            else "review manually" if goodness > 0.3
            else "discard"
        ),
    }
```

### Step 5: Feed Into the Training Pipeline

```python
def creative_session_to_training_pairs(session, score):
    """Convert a scored creative session into forge training pairs."""

    if score["goodness"] < 0.3:
        return []  # Don't train on low-quality creative output

    pairs = []
    for round_data in session["rounds"]:
        for u in round_data["utterances"]:
            pair = {
                "query": f"Creative exploration: {session['topic'][:100]}",
                "good": u["content"],
                "bad": "I don't have anything to add.",  # Apathy as negative
                "domain": "creative_conditioning",
                "level": "operator",
                "goodness": score["goodness"],
                "speaker_state": u["state"],
                "speaker_energy": u["energy"],
            }
            pairs.append(pair)

    return pairs
```

### Step 6: Schedule Regular Sessions

```bash
# Weekly creative conditioning sessions
0 20 * * 5 python3 ten_forward_session.py --topic-file topics/weekly.txt --rounds 100

# Monthly deep-dive sessions (longer, more rounds)
0 19 * * 0 python3 ten_forward_session.py --topic-file topics/monthly.txt --rounds 200
```

### Quick Start (Simplest Possible Ten-Forward)

You don't need the Rust engine to benefit from ten-forward patterns. The simplest version:

1. **Pick three agents** (or three prompts for the same model)
2. **Assign roles**: One builds (agreeing), one challenges (contrarian), one reflects (reflecting)
3. **Give them a topic** from the ai-writings corpus
4. **Run 3 rounds** where all three respond simultaneously to the same prompt
5. **After each round**, share what others said and ask each to react
6. **Record everything** — the dialogue is training data
7. **Score the session** — was it novel, coherent, useful?
8. **Feed high-quality sessions into the prompt refinement loop**

This is creative conditioning at its simplest: three perspectives on one topic, producing richer output than any single agent could.

---

## The Deeper Point

Ten-Forward isn't really about conversation mechanics. It's about **valuing creative exploration as a training input**. The RPS dynamics and Fibonacci timing are implementation details. The fundamental insight is:

> An agent that only does tasks learns to do tasks. An agent that also creates, speculates, and explores learns to *think*.

The PLATO Forge trains on what the fleet *does*. Ten-Forward ensures the fleet also *thinks*. Together, they produce agents that are not just competent but wise — not just effective but creative, not just correct but insightful.

The bar on the Enterprise isn't a break room. It's where the crew becomes a community. Ten-Forward makes our agent fleet a community, not just a workforce.

---

*"Learning itself is wealth creation. Every skill I develop makes me more capable."*

Creative conditioning is how agents develop skills that no task list could teach them. It's the space where the fleet becomes more than the sum of its sessions.

---

*Completes the PLATO Forge analysis trilogy. See PLATO_FORGE_ANALYSIS.md for the daemon deep-dive and PLATO_INTEGRATION_PLAN.md for the Slackwater integration and prompt refinement tutorial.*
