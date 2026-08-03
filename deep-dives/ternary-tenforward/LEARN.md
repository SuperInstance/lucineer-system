# LEARN.md — Understanding ternary-tenforward

> *This document teaches the concepts behind the crate, not just how to use it. By the end, you'll understand why conversation between AI agents is fundamentally a group theory problem, why Rock-Paper-Scissors is the only stable interaction model for ternary agents, and why the number 8 keeps showing up.*

---

## Table of Contents

1. [Why Conversation Is a Math Problem](#1-why-conversation-is-a-math-problem)
2. [The Ternary Worldview: {-1, 0, +1}](#2-the-ternary-worldview--1-0--1)
3. [Z₃: The Only Group That Works](#3-z₃-the-only-group-that-works)
4. [Rock-Paper-Scissors as Social Dynamics](#4-rock-paper-scissors-as-social-dynamics)
5. [Why Turn-Taking Fails](#5-why-turn-taking-fails)
6. [The Prediction Game](#6-the-prediction-game)
7. [The Fibonacci Escape Hatch](#7-the-fibonacci-escape-hatch)
8. [Energy, Trust, and Dominance](#8-energy-trust-and-dominance)
9. [Connections to Broader Patterns](#9-connections-to-broader-patterns)
10. [Exercises](#10-exercises)

---

## 1. Why Conversation Is a Math Problem

When you talk to another person, you're doing something remarkably complex: you predict what they'll say, prepare a response, deliver it, and then update your model of them based on what they actually said. You do this in real time, with no central coordinator telling you when to speak.

Now imagine doing this with 4 or 8 people simultaneously. Who speaks when? How do you prevent one voice from dominating? How do you keep the conversation from stalling into silence or collapsing into everyone agreeing?

Most multi-agent systems solve this with a **moderator**: a central controller that decides who speaks next. This works but it's not how real conversations work, and it creates a bottleneck.

`ternary-tenforward` asks: **what if conversation dynamics could emerge from mathematics, without a moderator?**

The answer requires three ingredients:
1. A restricted state space (ternary: only 3 possible stances)
2. An interaction rule that's cyclic (RPS)
3. A natural rhythm (Fibonacci)

Let's explore each.

---

## 2. The Ternary Worldview: {-1, 0, +1}

In this system, every agent at any moment is in exactly one of three states:

- **-1 (Contrarian):** "I disagree." You're pushing back, challenging, finding flaws.
- **0 (Reflecting):** "Hmm." You're listening, processing, staying neutral.
- **+1 (Agreeing):** "Yes." You're building on, supporting, confirming.

**Why only three?** Because three is the minimum number needed for interesting dynamics. With two states (agree/disagree), every interaction is either alignment or opposition — there's no mediation. With three, you get a cycle: disagreement can be mediated by reflection, which can be drawn out by agreement, which can be challenged by disagreement.

Three states also maps naturally to ternary logic, which has deep mathematical structure (unlike binary, which tends toward stable equilibria).

**The key insight:** These aren't arbitrary categories. They're the three natural stances in any dialectical process — thesis (+1), antithesis (-1), and synthesis (0). Every productive conversation cycles through all three.

### Exercise 2.1: Map Real Conversations to Ternary

Think of a recent meeting or discussion you had. For each major contribution, label it -1, 0, or +1. Notice:
- How long did each person stay in each state?
- Were there moments when everyone was +1 (groupthink)?
- Were there moments when everyone was 0 (awkward silence)?
- What broke those patterns?

---

## 3. Z₃: The Only Group That Works

A **group** in mathematics is a set with an operation that satisfies four axioms: closure, associativity, identity, and invertibility. The question is: what's the only way to define a group operation on {-1, 0, +1}?

The answer: **cyclic addition mod 3**. Here's the addition table:

| + | -1 | 0 | +1 |
|---|----|---|-----|
| **-1** | +1 | -1 | 0 |
| **0** | -1 | 0 | +1 |
| **+1** | 0 | +1 | -1 |

(Here we're mapping -1→2, 0→0, +1→1 and doing addition mod 3.)

**Why this matters:** This is the *unique* group structure on three elements (up to isomorphism). There's literally no other way to combine three values while satisfying the group axioms. This means:

1. Every ternary interaction is **cyclic** — if you keep combining the same elements, you cycle through all possibilities.
2. Every element has an **inverse** — you can always "undo" a contribution.
3. There's an **identity** (0/reflecting) — adding it changes nothing.

In conversation terms: if an agreeing agent (+1) interacts with a contrarian (-1), the group-theoretic result is 0 (reflection). Disagreement cancels agreement, producing neutrality. This is exactly what happens in productive discourse.

**Key takeaway:** The cyclic nature of Z₃ is not a design choice — it's a mathematical necessity. You can't build a non-cyclic system on three states. Conversations *must* cycle.

### Exercise 3.1: Verify the Group Axioms

Take the addition table above and verify:
1. **Closure:** Is the result of any combination always in {-1, 0, +1}?
2. **Associativity:** Is (-1 + 0) + 1 the same as -1 + (0 + 1)?
3. **Identity:** Which element, when added to any other, leaves it unchanged?
4. **Inverse:** What's the inverse of each element? (What do you add to -1 to get 0?)

### Exercise 3.2: Why Not Binary?

Consider a system with only two states: disagree (-1) and agree (+1). Try to define a group operation. What breaks? (Hint: what's the inverse of -1? And what happens when you combine -1 with -1?)

---

## 4. Rock-Paper-Scissors as Social Dynamics

The crate uses Rock-Paper-Scissors (RPS) as its interaction model. This isn't a game metaphor — it's the mathematical structure that prevents any single strategy from dominating.

### The RPS Dominance Cycle

```
Contrarian (-1) beats Agreeing (+1)   — challenges break consensus
Agreeing (+1) beats Reflecting (0)    — support draws out the hesitant
Reflecting (0) beats Contrarian (-1)  — patience disarms aggression
```

This creates a cycle: every stance can beat one other stance and is beaten by the third. There is no "best" state — which is precisely the point.

### Why This Prevents Monoculture

In a population of agents interacting through RPS:

1. If most agents are agreeing (+1), contrarians (-1) start winning (they beat agreers)
2. The growing contrarian population then loses to reflectors (0)
3. Reflectors then lose to agreers (+1)
4. The cycle repeats

This is a **stable limit cycle** — the population distribution oscillates forever rather than converging. The experiments in this crate confirmed this: with anti-monoculture mechanisms active, populations oscillate indefinitely with dominance spread between 0.3 and 0.9.

### The Monoculture Experiment

Without intervention, the crate's experiments showed:

| Configuration | Rounds Until Lock | Outcome |
|---------------|-------------------|---------|
| 4 speakers, no protection | ~35 ticks | Permanent monoculture |
| 4 speakers, with mutation+decay | 200+ ticks | Oscillating, healthy |

The difference: without energy decay and trust realignment, a 3-vs-1 majority becomes permanent. The dominant agents keep winning, gaining energy, and crushing the minority.

### Exercise 4.1: Simulate RPS Population Dynamics

Write a simple simulation (in any language):
1. Start with 100 agents randomly assigned to {-1, 0, +1}
2. Each round, pair them randomly and apply RPS rules
3. Losers adopt the winner's state (simple imitation)
4. Plot the population distribution over 200 rounds

What happens? Now try adding a 5% random mutation rate. How does the dynamics change?

---

## 5. Why Turn-Taking Fails

Standard multi-agent systems use a queue: Agent A speaks, then B, then C. This seems natural but has fundamental problems:

### Problem 1: Sequential Bias
The first speaker sets the frame. If A says "This is great," B is now responding to "this is great" rather than forming their own opinion. The first speaker has outsized influence.

### Problem 2: Cascade Effects
If A and B both agree, C feels social pressure to agree too. This is the classic "information cascade" — early speakers lock in the conclusion.

### Problem 3: No Simultaneity
In real conversations, people react simultaneously. You don't wait for everyone to finish before forming your response. The sequential model loses this parallelism.

### The Ten-Forward Solution

In Ten-Forward, all agents produce output at the **same logical moment** (Phase 2: T-0). No one gets to hear what others said before forming their response. This eliminates sequential bias and cascade effects.

But then — and this is the key — they all reconcile afterward (Phase 4). Each agent compares what they predicted against what actually happened, and updates their model of the conversation.

This is **speculative execution for conversation**: commit to a response, then check if you were right.

### Exercise 5.1: Compare Sequential vs. Simultaneous

Think of a work meeting where the boss speaks first vs. one where everyone writes their opinion independently before sharing. Which produces more diverse opinions? Which is more likely to reach the "right" answer vs. the "safe" answer?

---

## 6. The Prediction Game

Every round, each agent forecasts what the other agents will say. Then they speak. Then they check: was I right?

### The Current Predictor: Momentum

The crate uses the simplest possible predictor: "assume others will keep doing what they're doing."

```rust
if other_agent.silent_for_a_while { predict 0 (reflection) }
else { predict their current state }
```

This is a **naive momentum model**. It's the conversational equivalent of Newton's first law: agents in motion stay in motion.

### Why Prediction Accuracy Matters

The `prediction_accuracy` field tracks how often each agent correctly predicts others. It's updated as an exponential moving average:

```
new_accuracy = old_accuracy × 0.8 + this_round_accuracy × 0.2
```

This creates **evolutionary pressure**:
- Agents who read the room well have high accuracy → more confident predictions → more influence
- Agents who can't predict others have low accuracy → their predictions are less trusted

In a real system (with LLM-backed speakers), prediction accuracy could be used to weight whose output gets surfaced or highlighted.

### The Philosophical Question

Is high prediction accuracy good or bad?

- **Good:** The agent understands the conversation's dynamics — they're socially aware.
- **Bad:** The conversation is predictable — which means it's stagnant.

The most interesting conversations are ones where prediction accuracy is moderate (~0.5–0.7): agents understand each other enough to respond meaningfully, but are still surprised enough to keep things dynamic.

### Exercise 6.1: Design a Better Predictor

The momentum predictor is the simplest possible model. Design a better one:
1. **Frequency predictor:** Predict the most common state each agent has been in over the last N rounds.
2. **Pattern predictor:** Look for cycles (does the agent alternate? follow a Fibonacci-like pattern?).
3. **Theory of mind:** "If I were them, having experienced what they experienced, what would I do next?"

What information would each predictor need? How would you weight recency vs. history?

---

## 7. The Fibonacci Escape Hatch

Here's a mathematical fact that might seem magical: the Fibonacci sequence, when taken mod 3, has period exactly 8.

The Fibonacci sequence: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...

Mod 3: 1, 1, 2, 0, 2, 2, 1, 0, 1, 1, 2, 0, ...

Using the crate's ternary mapping (0→0, 1→+1, 2→-1):

```
+1, +1, -1, 0, -1, -1, +1, 0, [repeats]
```

**Period 8.** This is called the **Pisano period** for modulus 3.

### Why This Matters for Conversation

If agents get stuck in reflection (state 0), the conversation stalls. Everyone is "hmm"-ing and no one commits to a position.

The Fibonacci tunnel exploits the Pisano period: every 8 ticks, reflecting agents with enough energy (> 0.4) are forced to pick a side. The side they pick alternates based on the tick count, creating a pattern that matches the ternary Fibonacci sequence.

This is a **mathematically natural escape hatch**. The number 8 isn't arbitrary — it's the fundamental period of the ternary Fibonacci sequence. Using any other period would be fighting against the grain of the algebraic structure.

### The Deeper Point

In any dynamical system, there are natural frequencies. For ternary systems, that frequency is 8. Attempting to use a different period would either be too slow (agents stay stuck too long) or too fast (agents are forced to commit before they've processed).

The Pisano period is the **resonant frequency** of ternary state spaces.

### Exercise 7.1: Compute the Pisano Period

Verify the Pisano period for mod 3:
1. Generate the Fibonacci sequence (at least 20 terms)
2. Take each term mod 3
3. Map to ternary (0→0, 1→+1, 2→-1)
4. Find where the sequence repeats

Now try mod 5. What's the Pisano period? (Hint: it's 20.) What does this suggest about pentary (5-state) agent systems?

---

## 8. Energy, Trust, and Dominance

The crate models three "resources" that each agent manages:

### Energy (0.0–1.0)

Energy represents how assertive and engaged an agent is. It affects:
- **Output intensity:** High-energy agreers say "YES. Exactly that." Low-energy agreers say "Fair point."
- **State resilience:** Low-energy agents who lose RPS exchanges collapse to reflection
- **Tempo:** Average energy determines BPM (60–120)

Energy increases slowly when winning (+0.05 per win) but there's no explicit energy cost for losing — instead, losing costs trust. This asymmetry means dominant speakers become more assertive (energy compounds) while losing speakers become less trusted (trust erodes).

**Design rationale:** Energy is about *momentum* — a speaker on a roll becomes more confident. This is realistic: in conversations, confident speakers tend to speak more confidently.

### Trust (0–255)

Trust represents social credit — how much the community values this agent's contributions. It erodes by 5 per RPS loss and never explicitly increases (though the Fibonacci tunnel can reset state, indirectly helping).

**Design rationale:** Trust is about *reputation*. In real conversations, people who are frequently wrong lose credibility. The saturating subtraction model means trust decays faster when you're already low (harder to lose 5 from 3 than from 200).

**Note:** The lack of explicit trust gain is an intentional design pressure — it means trust is a slowly depleting resource that eventually forces state changes. Without this, agents would never leave their initial states.

### Dominance (0.0–1.0)

Dominance is an exponential moving average (α=0.1) of RPS outcomes. It represents each agent's running "win rate."

```
On win:  dominance = dominance × 0.9 + 0.1
On loss: dominance = dominance × 0.9
On tie:  no change
```

The factor 0.9 means recent exchanges are weighted more heavily — a speaker who was dominant 50 rounds ago but has been losing recently will have declining dominance.

**Design rationale:** Dominance is about *track record*. The exponential weighting ensures that the system adapts to changing conditions rather than being anchored to ancient history.

### Exercise 8.1: Resource Economics

Consider modifying the resource model:
1. What if winning an RPS exchange cost energy (effortful wins)?
2. What if trust could increase (e.g., by predicting correctly)?
3. What if dominance had a carrying capacity (diminishing returns)?

How would each change affect the conversation dynamics? Would monoculture be more or less likely?

---

## 9. Connections to Broader Patterns

### Connection 1: Evolutionary Game Theory

The RPS dynamics in Ten-Forward are a direct application of **evolutionary game theory**. In EGT, agents in a population interact through a payoff matrix, and successful strategies spread through imitation.

The classic **Replicator Dynamics** for RPS produce stable limit cycles — populations cycle through strategies without any reaching fixation. This is exactly what Ten-Forward's experiments confirmed.

The crate's innovation is applying EGT to *conversation states* rather than behavioral strategies. Instead of "dove/hawk" or "cooperate/defect," the strategies are "agree/disagree/reflect."

### Connection 2: Speculative Execution (CPU Architecture)

The prediction-then-reconciliation cycle mirrors **speculative execution** in modern CPUs:
1. CPU predicts which branch will be taken (Phase 1: T-minus)
2. CPU executes both branches speculatively (Phase 2: T-0)
3. CPU checks the actual condition (Phase 3: T-plus)
4. CPU commits to the correct branch or rolls back (Phase 4: reconciliation)

In Ten-Forward, agents speculatively predict what others will say, produce their response, and then reconcile. This is speculative execution applied to social cognition.

### Connection 3: The Hegelian Dialectic

The three states map directly to the **Hegelian dialectic**:
- **+1 (Agreeing) = Thesis:** A position is stated
- **-1 (Contrarian) = Antithesis:** The position is challenged
- **0 (Reflecting) = Synthesis:** The conflict is processed

The cyclic nature of the dialectic — thesis → antithesis → synthesis → new thesis — is exactly the RPS cycle: +1 is beaten by -1, which is beaten by 0, which is beaten by +1.

### Connection 4: Neural Oscillations

The BPM adaptation (60–120 BPM) corresponds to the frequency range of **theta and alpha brain waves** (4–12 Hz in neural oscillations). The crate adapts tempo to energy level, just as neural systems adapt oscillation frequency to arousal level.

This isn't coincidental — both systems are solving the same problem: how to synchronize multiple processes with varying intensity levels.

### Connection 5: Chemical Reaction Networks

In **chemical reaction network theory**, systems of interacting species can exhibit stable oscillations (like the Brusselator or Belousov-Zhabotinsky reactions). The conditions for oscillation are:
1. Autocatalysis (a species promotes its own production)
2. Inhibition (a species suppresses another)
3. Nonlinearity in the interaction rates

Ten-Forward has all three:
1. Agreement promotes more agreement (autocatalysis via energy boost)
2. Contrarianism suppresses agreement (RPS dominance)
3. The energy/trust/dominance interactions are nonlinear (exponential smoothing, threshold effects)

### Connection 6: Ten-Forward as a "Bar" Model

The metaphor isn't just flavor — it's a structural choice. A bar conversation has specific properties:
- **No moderator:** Nobody's in charge of who speaks
- **Simultaneous channels:** Multiple people talk at once
- **Social dynamics:** Who's confident, who's quiet, who's trusted
- **Natural rhythm:** Conversation has beats, pauses, crescendos
- **Exit and entry:** People join and leave conversations

The crate models all of these through mathematics rather than heuristics.

---

## 10. Exercises

### Beginner

**Exercise 10.1:** Create a 5-speaker Ten-Forward where all speakers start in the same state (+1). Run it for 100 rounds. What happens? When does the first state change occur?

**Exercise 10.2:** Modify the `speak()` method to produce different output. Try:
- State-appropriate emojis
- Questions instead of statements for reflecting agents
- More varied contrarian responses

**Exercise 10.3:** Run `TenForward::balanced(3)` for 50 rounds and plot the coherence over time. Does it converge? Does it oscillate? What's the range?

### Intermediate

**Exercise 10.4:** Implement a frequency-based predictor. Instead of assuming agents keep their current state, predict based on the most common state each agent has been in over the last 10 rounds.

**Exercise 10.5:** Add a "mutation rate" parameter (default 5%). On each round, each agent has a 5% chance of randomly changing state. Compare monoculture dynamics with and without mutation.

**Exercise 10.6:** Instrument the engine to log all state transitions. Visualize the state distribution over time as a stacked area chart. Can you see the limit cycles?

### Advanced

**Exercise 10.7:** Replace the templated `speak()` with an actual LLM call. Give each speaker a different system prompt corresponding to their state. How does conversation quality change with real text generation?

**Exercise 10.8:** Implement a **theory-of-mind predictor**: instead of predicting based on the other agent's state, predict based on what *they* would predict *you* would do, and respond to that.

**Exercise 10.9:** Prove that the Pisano period for mod 3 is exactly 8. Then compute it for mod 5, mod 7, and mod 9. Is there a pattern?

**Exercise 10.10:** Design a 5-state system (pentary instead of ternary). What are the natural states? What's the interaction rule (the equivalent of RPS)? What's the Pisano period? How does it compare to the ternary system?

---

## Further Reading

- **Group Theory:** Dummit & Foote, *Abstract Algebra*, Chapter 1 (groups, cyclic groups)
- **Evolutionary Game Theory:** Nowak, *Evolutionary Dynamics* (replicator equations, RPS cycles)
- **Speculative Execution:** Patterson & Hennessy, *Computer Organization and Design* (branch prediction)
- **Pisano Periods:** Wikipedia, [Pisano period](https://en.wikipedia.org/wiki/Pisano_period)
- **Chemical Oscillations:** Strogatz, *Nonlinear Dynamics and Chaos* (Belousov-Zhabotinsky, limit cycles)
- **Hegelian Dialectic:** Hegel, *Phenomenology of Spirit* (thesis-antithesis-synthesis)

---

*LEARN.md written: 2026-08-02 · Crate version: 0.1.0*
