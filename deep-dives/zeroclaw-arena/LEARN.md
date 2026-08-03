# ZeroClaw Arena — Learning Guide

> **For:** Engineers integrating ZeroClaw patterns into Slackwater  
> **Goal:** Understand the algorithms deeply enough to port them

---

## Core Concept: Tile-Based Monte Carlo

Most game AI uses neural networks to evaluate board positions. ZeroClaw uses **tiles** — decompositions of game state into local patterns that each accumulate independent statistics.

### What is a Tile?

A tile is simply: `state_string → {action: {score, chosen, won}}`

For Tic-Tac-Toe, the state string `"X O  X   "` is one tile. The tile records that action `"6"` (bottom-left) has been chosen 3 times with 2 wins (score: 0.67).

### Why Tiles Work

Tiles work because game states have **structure**:
- The same position reached by different move orders has the same strategic value
- Local patterns (two-in-a-row, center control) transfer across positions
- Statistics accumulate independently per state, avoiding interference

### Why Tiles Work Without Neural Networks

Neural networks provide two things: **generalization** (similar states → similar values) and **function approximation** (compact representation of huge state spaces).

ZeroClaw gets generalization from:
1. **Monte Carlo simulation** — estimates action value by random rollout, works for any state
2. **Hamming distance nearest-neighbor** — finds similar board states for fallback
3. **Tile decomposition** — local patterns transfer across positions

And compact representation from:
1. **Sparse tiles** — only visited states get entries (1,238 tiles for TTT, not 3^9 = 19,683)
2. **Compilation** — trained field compresses to best-action-per-state lookup
3. **Hierarchical clustering** — group similar tiles into meta-strategies (8 clusters for 10x compression)

---

## The Learning Loop

### Step 1: Monte Carlo Estimation

For each possible action, simulate random games from that action to the end:

```
Action "4" (center):
  Simulation 1: X plays 4 → random play → X wins ✓
  Simulation 2: X plays 4 → random play → O wins ✗
  Simulation 3: X plays 4 → random play → draw ✗
  
  sim_score = 1/3 = 0.33
```

More simulations = more accurate but slower. Default: 20 simulations split across actions.

### Step 2: Confidence-Weighted Blending

Early in training, trust simulation (Monte Carlo). Later, trust learned scores (empirical win rates):

```python
confidence = min(visits / 20.0, 0.8)  # cap at 80% trust
value = confidence * learned_score + (1 - confidence) * sim_score
```

This prevents early overfitting to lucky/unlucky rollouts while gradually shifting to empirical data.

### Step 3: Softmax Selection

Instead of always picking the best action (greedy), sample proportional to value:

```python
probs = softmax(values / temperature)
action = random.choice(actions, p=probs)
```

- **Low temperature (0.1):** nearly greedy — always picks highest value
- **High temperature (2.0):** nearly uniform — lots of exploration
- **Optimal (0.15-0.3):** mostly exploit, occasionally explore (confirmed by temperature sweep)

### Step 4: Outcome Recording

After the game ends, update all visited tiles:

```python
for (state_str, action) in history:
    tile[state_str][action]["chosen"] += 1
    if won:
        tile[state_str][action]["won"] += 1
```

### Step 5: Score Evolution

Every 25 games, adjust scores toward empirical win rates:

```python
for tile in tiles.values():
    for action, data in tile.items():
        if data["chosen"] > 0:
            wr = data["won"] / data["chosen"]
            data["score"] += 0.05 * (wr - data["score"])
            data["score"] = clamp(data["score"], 0.05, 0.95)
```

The 0.05 learning rate means it takes ~20 updates to fully shift. This prevents overfitting to recent games.

---

## Compilation: Training → Deployment

The trained tile field needs numpy, random, and Monte Carlo simulation. The compiled policy needs **nothing** — just string matching.

### How Compilation Works

1. For each visited state where it's X's turn:
   - Find the action with highest `empirical_wr + exploration_bonus`
   - Store `state_str → best_action` in lookup dict
2. For unknown states at runtime:
   - Find nearest known state by Hamming distance (≤3 character differences)
   - If none found: heuristic fallback (center → corners → edges)

### The Compiled Artifact

```python
def compiled_policy(board_str):
    _lookup = { "         ": "8", "X       O": "2", ... }
    if board_str in _lookup:
        return _lookup[board_str]
    # ... nearest neighbor fallback ...
```

For Tic-Tac-Toe: ~800 entries, ~15KB of Python, zero imports. Runs in ~0.001ms per move.

---

## Vector DB Pattern Matching

Beyond per-state tiles, ZeroClaw uses a vector database for cross-cutting pattern discovery.

### Embedding

```python
def hash_to_vector(text, dim=64):
    h = blake2b(text.encode(), digest_size=dim).digest()
    vec = [b / 255.0 for b in h]
    return normalize(vec)  # unit length
```

**Properties:**
- Deterministic: same text → same vector, always
- Fixed dimension: 64 floats regardless of input length
- Normalized: cosine similarity = dot product

**Limitation:** Hash embeddings have no semantic awareness. "Hello" and "Hi" get unrelated vectors. This is fine for exact pattern matching but poor for semantic similarity.

### Pattern Discovery

The `analyze_patterns()` method finds four types of patterns:

1. **Winning actions per state prefix** — "states starting with 'X O' → action '4' wins 72%"
2. **Feature predictors** — "bigram 'XO' appears in 68% of winning states"
3. **Closing patterns** — "last 3 moves in winning games: [4, 2, 6]"
4. **Similar state, different action** — "states A and B are 94% similar but prefer different actions"

### Cross-Game Transfer

The GPU engine can find similar states across different games:

- Tic-Tac-Toe ↔ Connect 4 max similarity: 0.9121 (both grid games)
- Tic-Tac-Toe ↔ Blackjack max similarity: 0.9098 (structural, not semantic)
- Winning states in one game can be losing in another (anti-correlation at 0.84 similarity)

**Insight:** Structural patterns transfer across games with similar topology. Grid games share "center control" patterns. But transfer can be negative — a winning TTT position might map to a losing Blackjack configuration.

---

## Experiments — What We Learned

### Temperature Sweep
**Finding:** Optimal temperature is 0.15-0.3. Too low (0.01) = no exploration, overfits. Too high (>1.0) = too random, doesn't converge.

### Reward Shaping
**Finding:** Binary rewards (win=1, loss=0) outperform all alternatives. Progressive bonuses and shaped rewards actually hurt performance by adding noise to the signal.

### Hierarchical Tiles
**Finding:** Clustering tiles into 8 "meta-strategies" using k-means on score vectors achieves comparable performance to flat tiles at ~10x compression. This proves intelligence has natural hierarchical structure.

### Tile Capacity
**Finding:** 42% of tiles can be pruned (those with <2 visits) with <2pp performance loss. The "important" tiles concentrate visits naturally.

### Evolutionary Strategy Optimization
**Finding:** Evolving the learning hyperparameters (exploration rate, temperature, mutation rate, reward decay) via genetic algorithm beats random by +10pp after 15 generations.

### Adversarial Training
**Finding:** Training against a learning opponent (adversarial) produces slightly more robust policies than training against random opponents (69.5% vs 68.1% win rate).

---

## Key Takeaways for Slackwater Integration

1. **The "learn with simulation, deploy with lookup" pattern is the core insight.** Training uses expensive Monte Carlo; deployment uses free dict lookups.

2. **Evolutionary score updates work.** The simple `score += 0.05 * (observed - expected)` formula is a robust learning rule that works without gradients.

3. **Hash embeddings are fast but semantically blind.** Fine for exact-state pattern matching; pair with LLM for semantic understanding.

4. **Tile decomposition enables factored learning.** Different aspects of context (channel, time, user, urgency) can learn independently, then compose at decision time.

5. **The compilation step is the deployment bridge.** Training artifacts (heavy, needs dependencies) → compiled artifacts (light, zero dependencies) is the path from development to production.
