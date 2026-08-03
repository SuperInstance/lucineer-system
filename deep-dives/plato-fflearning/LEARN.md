# LEARN.md — Understanding Forward-Forward Learning

> An educational companion to `plato-fflearning`.
> This file teaches the *concepts*, not just the API.
> Read this if you want to understand *why* this approach exists and *how* it connects to deeper patterns.

---

## Table of Contents

1. [The Problem: Why Backpropagation Is Weird](#1-the-problem-why-backpropagation-is-weird)
2. [Hinton's Insight: Two Forward Passes](#2-hintons-insight-two-forward-passes)
3. [The Goodness Function](#3-the-goodness-function)
4. [From Neural Layers to Agent Knowledge](#4-from-neural-layers-to-agent-knowledge)
5. [Why Asymmetric Penalties?](#5-why-asymmetric-penalties)
6. [Decay: The Forgetting Curve](#6-decay-the-forgetting-curve)
7. [Threshold Gating: Why 0.7?](#7-threshold-gating-why-07)
8. [The PLATO Connection: Tiles as Knowledge Atoms](#8-the-plato-connection-tiles-as-knowledge-atoms)
9. [Counterfactual Learning: The Power of "What If"](#9-counterfactual-learning-the-power-of-what-if)
10. [Connection to Broader Patterns](#10-connection-to-broader-patterns)
11. [Exercises](#11-exercises)
12. [Further Reading](#12-further-reading)

---

## 1. The Problem: Why Backpropagation Is Weird

Backpropagation is how nearly all neural networks learn. It works by:

1. **Forward pass**: Input data flows through the network, producing a prediction.
2. **Compute loss**: Compare the prediction to the correct answer.
3. **Backward pass**: Compute the gradient of the loss with respect to every weight, flowing backward from output to input.
4. **Update**: Adjust each weight by a small amount proportional to its gradient.

This is extremely effective. But it's also **biologically implausible**:

- **The backward pass requires symmetric weights**: To compute gradients backward, you need the transpose of the forward weights. Neurons don't have symmetric reciprocal connections.
- **It requires storing all intermediate activations**: The backward pass needs the outputs of every layer from the forward pass. This means holding the entire computation graph in memory.
- **It requires global synchronization**: All layers must complete the forward pass before any layer can learn. No layer can update locally.
- **It can't learn online**: Each training example requires a complete forward-backward cycle. You can't learn from streaming data without batching.

Geoffrey Hinton — one of the fathers of deep learning — argued for years that backpropagation can't be how the brain actually works. In 2022, he proposed the **Forward-Forward algorithm** as a biologically plausible alternative.

### Why this matters for agents (not just brains)

Multi-agent systems face the same structural problems as biological neural networks:

- **Agents are distributed**: No central controller sees all agent interactions.
- **Agents are asynchronous**: They operate at different speeds and don't share a global clock.
- **Agent interactions aren't differentiable**: You can't compute a gradient through a conversation between two agents.
- **Agents need to learn online**: They can't wait for a batch of experiences to accumulate before updating.

Forward-Forward learning addresses all of these by making learning **local** and **contrastive**.

---

## 2. Hinton's Insight: Two Forward Passes

The Forward-Forward algorithm replaces the forward-backward cycle with two forward passes:

| Pass | Input | Goal |
|------|-------|------|
| **Positive** | Real, correctly-labeled data | Make the layer output "high goodness" |
| **Negative** | Corrupted, mislabeled, or generated data | Make the layer output "low goodness" |

The learning rule for each layer is:

```
If positive data → increase goodness
If negative data → decrease goodness
```

The **gradient between positive and negative** replaces the gradient from backprop. No backward pass. No symmetric weights. No global synchronization.

### The key conceptual move

Instead of asking "how wrong was I?" (error-based learning), FF asks **"was this real or imagined?"** (contrastive learning).

This is a profound shift:
- **Error-based**: You need to know the correct answer to compute the error.
- **Contrastive**: You need to know whether the experience is real or hypothetical.

In agent terms:
- **Error-based**: "The correct response was X, I said Y, my error is X−Y."
- **Contrastive**: "I actually did X (positive) vs. I imagined doing Y (negative)."

Contrastive learning doesn't require a gold standard. It requires **experience**.

---

## 3. The Goodness Function

In Hinton's original formulation, "goodness" is the **sum of squared activities** in a layer:

```
Goodness = Σ aᵢ²
```

where `aᵢ` is the activity (output) of neuron `i` in the layer. High activity = high goodness = positive data. Low activity = low goodness = negative data.

The learning rule adjusts weights to:
- **Increase** Σ aᵢ² for positive data
- **Decrease** Σ aᵢ² for negative data

In `plato-fflearning`, goodness is simplified to a **scalar per agent**:

```
goodness = clamp(goodness × 0.95 + delta, 0.0, 1.0)
```

where delta is `+0.15` (positive) or `−0.08` (negative).

This isn't mathematically equivalent to Hinton's formulation, but it captures the same intuition: goodness rises with real experience and falls with hypothetical failures.

### Exercise: Think about it

Why is goodness a single scalar and not a vector? What would you lose by tracking goodness per-domain instead of per-agent?

> **Answer**: A single scalar gives you a quick reliability signal ("is this agent trustworthy?"). Per-domain goodness would be more informative ("is this agent good at X but bad at Y?") but requires more state and more experiences to calibrate each domain.

---

## 4. From Neural Layers to Agent Knowledge

The conceptual mapping from neural FF to PLATO FF:

| Neural FF | PLATO FF |
|-----------|----------|
| A neural network layer | An agent |
| Layer weights | Agent's knowledge tiles |
| Layer activations | Agent's goodness score |
| Positive data (correct labels) | Real successful experiences |
| Negative data (wrong labels) | Imagined or actual failures |
| Weight update rule | Goodness update + tile reinforcement |
| Threshold for goodness | 0.7 (triggers tile reinforcement) |

The key translation: in neural FF, **weights** are what's learned. In PLATO FF, **tiles** are what's learned. Weights are continuous-valued matrices; tiles are discrete Q&A knowledge units.

This means PLATO FF is doing **discrete learning** — it's deciding which knowledge units to reinforce, not adjusting continuous parameters. This is closer to how humans curate knowledge: you don't adjust the "weights" of a fact, you either remember it or forget it, trust it or doubt it.

---

## 5. Why Asymmetric Penalties?

The library uses:
- **Positive boost: 0.15**
- **Negative penalty: 0.08**

Positives are almost 2× as strong as negatives. Why?

### Biological rationale

In neuroscience, the **dopaminergic reward system** is asymmetric:
- Rewards (positive prediction errors) produce strong dopamine signals
- Punishments (negative prediction errors) produce weaker, more diffuse signals

This asymmetry may exist because **in nature, missing a reward is usually recoverable, but pursuing a harmful target can be fatal**. Better to be cautious (strong positive, weak negative) than reckless.

### System design rationale

In a multi-agent fleet, you want:
- **Fast recovery from failures**: An agent that had a bad experience shouldn't be permanently crippled
- **Slow accumulation of trust**: Goodness rises faster than it falls, but you need multiple positives to cross threshold
- **Stability**: If penalties were as strong as boosts, agents would oscillate between high and low goodness

### The math

From 0.5 (default):
- **3 positive passes**: 0.5 → 0.625 → 0.744 → 0.857 (crosses 0.7 on pass 2)
- **3 negative passes**: 0.5 → 0.395 → 0.295 → 0.200 (drops to "critical" on pass 3)
- **3 positives then 3 negatives**: 0.5 → 0.857 → 0.734 → 0.617 → 0.506 (still moderate)

So an agent that proves itself reliable over 3 successes takes 3 failures to fall back to moderate. The asymmetry creates **hysteresis** — once you're trusted, it takes effort to lose that trust, but you also don't get trust for free.

---

## 6. Decay: The Forgetting Curve

The `GOODNESS_DECAY = 0.95` factor applies before every update:

```
new_goodness = old_goodness × 0.95 + delta
```

This means an agent's goodness **drifts toward zero** without new experiences. After N events without reinforcement:

| Events | Goodness from 1.0 | Goodness from 0.5 |
|--------|-------------------|-------------------|
| 0 | 1.000 | 0.500 |
| 5 | 0.950⁵ = 0.735 | 0.500 × 0.950⁵ = 0.368 |
| 10 | 0.950¹⁰ = 0.540 | 0.500 × 0.950¹⁰ = 0.270 |
| 20 | 0.950²⁰ = 0.292 | 0.500 × 0.950²⁰ = 0.146 |

But note: decay only happens when a pass occurs (positive or negative). If no passes occur, goodness is frozen. Decay is **event-driven**, not time-driven.

### Connection to Ebbinghaus

Hermann Ebbinghaus discovered the **forgetting curve** in 1885: memory retention decays exponentially over time. The formula is roughly:

```
R = e^(−t/S)
```

where R is retention, t is time, and S is memory strength.

FF decay (`0.95^n`) is a discrete approximation of this: each event acts like a time step in the forgetting curve. This isn't coincidental — both describe the same phenomenon: **memories weaken without reinforcement**.

### Design question

Should decay be time-based or event-based?

- **Event-based (current)**: Goodness only changes when something happens. Simple, but means an idle agent retains its score indefinitely.
- **Time-based**: Goodness decays as a function of wall-clock time. More realistic, but requires a background process to apply decay.

### Exercise

An agent starts at goodness 1.0. How many positive passes does it take to get back to 0.7 after 20 negative passes? (Hint: 20 negative passes from 1.0 gives 0.292. Then positives: 0.292 → 0.427 → 0.556 → 0.678 → 0.795.)

---

## 7. Threshold Gating: Why 0.7?

The `THRESHOLD = 0.7` determines when tiles get reinforced. Why 0.7?

### From 0.5 (default), it takes 2 positive passes to cross:
- Pass 1: 0.5 × 0.95 + 0.15 = 0.625
- Pass 2: 0.625 × 0.95 + 0.15 = 0.744 ✓

### From 0.5, it takes 3 negative passes to reach critical (<0.2):
- Pass 1: 0.5 × 0.95 − 0.08 = 0.395
- Pass 2: 0.395 × 0.95 − 0.08 = 0.295
- Pass 3: 0.295 × 0.95 − 0.08 = 0.200

So 0.7 creates a gate that requires **two consecutive successes** to pass — a simple noise filter. A single lucky positive isn't enough; you need two in a row.

This is reminiscent of **n-confirmation blocks** in blockchain: one block isn't enough, you need N confirmations to trust the transaction. 0.7 effectively requires 2-confirmation before knowledge gets reinforced.

### Exercise

What happens if you lower the threshold to 0.6? What changes in system behavior?

> **Answer**: From 0.5, a single positive pass reaches 0.625, which exceeds 0.6. So every single positive experience would trigger tile reinforcement. This makes the system more responsive but also more vulnerable to noise — a single lucky outcome can cement knowledge that may be wrong.

---

## 8. The PLATO Connection: Tiles as Knowledge Atoms

PLATO stores knowledge as **tiles** — discrete Q&A pairs with metadata:

```json
{
  "question": "How do you handle a fleet overload?",
  "answer": "Redistribute load across backup nodes, then scale up...",
  "agent": "oracle1",
  "domain": "fleet_orchestration",
  "confidence": 0.9,
  "tags": ["scaling", "load-balancing"],
  "test_hints": ["check_cpu_thresholds", "verify_failover"]
}
```

Tiles are the fundamental unit of knowledge in the PLATO ecosystem. They're:
- **Atomic**: Each tile captures one piece of knowledge
- **Structured**: Q&A format with rich metadata
- **Searchable**: PLATO provides keyword and semantic search
- **Versionable**: `plato-tile-version` provides Git-like versioning
- **Scorable**: `plato-tile-scorer` evaluates quality across 7 dimensions

### How FF learning uses tiles

In FF learning, tiles serve two roles:

1. **Input**: Each experience (positive or negative) is recorded as a tile. The tile captures what happened, when, and by whom.
2. **Output**: When goodness exceeds threshold, associated tiles get **reinforced** — their confidence increases, making them more likely to be retrieved in future queries.

This creates a **filter**: only knowledge from agents with proven track records gets permanently reinforced. The tile library self-curates based on agent reliability.

### Connection to memory consolidation

In cognitive neuroscience, **memory consolidation** is the process where:
1. An experience creates a short-term memory (hippocampus)
2. If the experience is repeated or emotionally significant, the memory is transferred to long-term storage (neocortex)
3. Unused memories decay over time

FF learning mirrors this:
1. Every pass creates a tile in PLATO (short-term memory)
2. When goodness exceeds threshold, associated tiles get reinforced (consolidation)
3. Unreinforced tiles remain but aren't boosted — they may eventually be pruned

---

## 9. Counterfactual Learning: The Power of "What If"

The most innovative aspect of FF learning is the **negative pass** — learning from experiences that *didn't happen*.

### What is counterfactual learning?

Counterfactual thinking is a hallmark of human intelligence:
- "What if I had taken that other job?"
- "What if I hadn't seen the stop sign?"
- "What would have happened if I deployed the old code?"

We learn as much from imagined alternatives as from real outcomes. In fact, **counterfactual learning is how we prepare for situations we haven't encountered yet**.

### How FF implements it

```python
# Real outcome: the deploy succeeded
ff.positive_pass("agent_1", "Deployed v2.1 — all systems green")

# Counterfactual: what if we'd deployed the buggy version?
ff.negative_pass("agent_1", "Hypothetical: v2.0 would have crashed — memory leak in connection pool")
```

The negative pass:
1. Decreases goodness (small penalty)
2. Creates a tile documenting the counterfactual (available for future retrieval)
3. Doesn't trigger reinforcement (goodness went down, not up)

This means the system accumulates **both positive knowledge** (what works) **and negative knowledge** (what doesn't work). A searching agent can find both.

### Why this is powerful

Traditional learning only records what actually happened. FF learning records **the space of what could have happened**. This:

- **Accelerates learning**: You don't need to actually fail to learn from failure
- **Creates contrastive examples**: The system understands the boundary between success and failure
- **Builds intuition**: Negative tiles document edge cases and failure modes

### Exercise

Design a counterfactual learning loop for a coding agent:

```python
# The agent writes a function and it passes tests
ff.positive_pass("coder_1", "Implemented merge_sort — all tests pass",
                 associated_tiles=["tile_merge_sort"])

# Counterfactual: what if they'd used bubble sort for large inputs?
ff.negative_pass("coder_1", "Hypothetical: bubble sort would be O(n²) — "
                            "timeout on inputs > 10K elements")
```

Think about: what are other useful counterfactuals for a coding agent? When would counterfactual learning be misleading?

---

## 10. Connection to Broader Patterns

### Pattern 1: Actor-Critic Architecture

In reinforcement learning, the **actor-critic** pattern has:
- **Actor**: Takes actions
- **Critic**: Evaluates actions

FF learning maps to this:
- **Actor**: The agent performing tasks
- **Critic**: The FF system evaluating outcomes (positive/negative pass)

But in FF, the critic is the *outcome itself*, not a separate model. The world is the critic.

### Pattern 2: Bayesian Belief Updating

In Bayesian inference, you update your belief based on evidence:

```
P(H|E) = P(E|H) × P(H) / P(E)
```

FF learning does a simplified version:
- **Prior**: Current goodness score
- **Evidence**: Positive or negative pass
- **Posterior**: Updated goodness score

The decay factor acts like **prior weighting**: old evidence contributes less, so the posterior is dominated by recent evidence.

### Pattern 3: Evolutionary Fitness

In evolutionary algorithms:
- Individuals have a **fitness score**
- High-fitness individuals reproduce (their genes propagate)
- Low-fitness individuals die out

FF learning:
- Agents have a **goodness score**
- High-goodness agents' tiles get **reinforced** (their knowledge propagates)
- Low-goodness agents' tiles remain **unreinforced** (their knowledge doesn't spread)

Tiles are the "genes" of the knowledge system. Goodness is the "fitness." Reinforcement is "reproduction."

### Pattern 4: Contrastive Learning (SimCLR, CLIP)

In modern self-supervised learning, **contrastive methods** learn by:
- Pulling together positive pairs (e.g., two augmentations of the same image)
- Pushing apart negative pairs (e.g., two different images)

FF learning is a temporal version of this:
- **Positive pair**: (experience, outcome=good) — pull together
- **Negative pair**: (experience, outcome=bad) — push apart

The agent learns to associate its behavior with outcomes.

### Pattern 5: Reinforcement Learning without Backpropagation

Standard RL uses temporal-difference learning, which requires backprop-through-time. FF offers an alternative:

- **State**: Current goodness
- **Action**: The agent's behavior
- **Reward**: Positive pass (good outcome)
- **Penalty**: Negative pass (bad outcome)
- **Policy update**: Goodness-driven tile reinforcement (no gradient computation)

This makes FF learning applicable to **non-differentiable environments** — like multi-agent conversations, game worlds, and real-world robotics.

---

## 11. Exercises

### Exercise 1: Tune the Constants

The current constants are:
```python
GOODNESS_DECAY = 0.95
POSITIVE_BOOST = 0.15
NEGATIVE_PENALTY = 0.08
THRESHOLD = 0.7
```

What happens if you change them to:
- `DECAY = 0.99, BOOST = 0.05, PENALTY = 0.05, THRESHOLD = 0.8`?
- `DECAY = 0.80, BOOST = 0.30, PENALTY = 0.20, THRESHOLD = 0.5`?

Describe the resulting system behavior in terms of:
- How many successes are needed to cross threshold
- How fast agents recover from failures
- Whether the system is stable or oscillates

### Exercise 2: Multi-Domain Goodness

Modify `ForwardForwardLearner` to track goodness per-domain instead of per-agent:

```python
self.state: Dict[str, Dict[str, float]] = {}  # agent -> {domain -> goodness}
```

What changes in the API? How does `get_fleet_learning_state()` need to adapt?

### Exercise 3: Implement Tile Weakening

Currently, negative passes only decrease goodness. Implement actual tile weakening:

```python
def negative_pass(self, agent, experience, domain="fleet_orchestration",
                  associated_tiles=None):
    # ... existing code ...
    if associated_tiles and new_goodness < self.THRESHOLD * 0.5:
        self._weaken_tiles(associated_tiles)
    return result

def _weaken_tiles(self, tile_ids):
    """Mark tiles as unreliable in PLATO."""
    for tile_id in tile_ids:
        # POST to PLATO with reduced confidence
        pass
```

### Exercise 4: Time-Based Decay

Add a `tick()` method that applies decay based on elapsed time:

```python
def tick(self):
    """Apply time-based decay to all agents."""
    for agent in self.state:
        self.state[agent] *= 0.99  # 1% decay per tick
```

How often should `tick()` be called? What are the trade-offs?

### Exercise 5: Goodness-Weighted Retrieval

Design a system where search results from PLATO are weighted by the source agent's goodness:

```python
def weighted_search(self, query):
    results = requests.get(f"{self.plato_url}/search?q={query}").json()
    weighted = []
    for tile in results:
        agent_goodness = self._get_agent_goodness(tile["agent"])
        tile["weight"] = agent_goodness
        weighted.append(tile)
    return sorted(weighted, key=lambda t: t["weight"], reverse=True)
```

What are the implications? When would this be better or worse than plain search?

### Exercise 6: Negative Pass from Failure Prediction

Design a **pre-emptive** negative pass: before an agent attempts a task, it predicts whether it will succeed. If it predicts failure, record a negative pass:

```python
def predict_and_act(self, agent, task):
    prediction = self.predict_success(agent, task)
    if prediction["will_succeed"]:
        result = self.positive_pass(agent, f"Predicted success: {task}")
    else:
        result = self.negative_pass(agent, f"Predicted failure: {task}")
    return result
```

How does this differ from post-hoc learning? What are the risks?

---

## 12. Further Reading

### Primary Sources

- **Hinton, G. (2022)**. *The Forward-Forward Algorithm: Some Preliminary Investigations*. [Paper](https://www.cs.toronto.edu/~hinton/FFA13.pdf) | [NeurIPS Talk](https://neurips.cc/virtual/2022/invited-talk/55869)
- **Hinton, G. (2023)**. *The Forward-Forward Algorithm: Some Preliminary Investigations*. [arXiv:2212.13345](https://arxiv.org/abs/2212.13345)

### Background

- **Ebbinghaus, H. (1885)**. *Memory: A Contribution to Experimental Psychology*. The original forgetting curve.
- **Sutton, R. & Barto, A. (2018)**. *Reinforcement Learning: An Introduction*. Actor-critic architecture.
- **Chen, T. et al. (2020)**. *SimCLR: A Simple Framework for Contrastive Learning*. Contrastive learning in vision.
- **Radford, A. et al. (2021)**. *CLIP: Learning Transferable Visual Models*. Contrastive learning across modalities.

### PLATO Ecosystem

- [PLATO Server](https://github.com/SuperInstance/plato-server) — Knowledge tile storage
- [PLATO Runtime Kernel](https://github.com/SuperInstance/plato-runtime-kernel) — Spatial room model
- [PLATO Tile Scorer](https://github.com/SuperInstance/plato-tile-scorer) — 7-signal tile quality scoring
- [FLUX Runtime](https://github.com/SuperInstance/flux-runtime) — Agent computation runtime
- [SuperInstance Org](https://github.com/SuperInstance/SuperInstance) — The full ecosystem

### Conceptual

- **γ + η = C**: The conservation law that governs the SuperInstance ecosystem — usable cognitive energy plus entropy equals a fixed budget. Every learning system operates within this budget.
- **Mortal Computing**: Hinton's proposal that future computers will be inseparable from their hardware, making backprop impossible and necessitating FF-like algorithms.

---

## Summary

Forward-Forward learning is built on three deep ideas:

1. **Learning can be local**: Agents don't need global information to learn. They learn from their own experiences, positive and negative.
2. **Contrast drives understanding**: The difference between what worked and what didn't is a sufficient learning signal. No gradients needed.
3. **Knowledge is discrete**: Tiles — not weights — are the natural representation for agent knowledge. Learning means deciding which tiles to trust.

These ideas are ancient (we've always learned from experience), newly formalized (Hinton's 2022 paper), and practically implemented (this library). The gap between neural network theory and agent knowledge management is smaller than it appears.

The forward pass is experience. The negative pass is imagination. The difference is learning.
