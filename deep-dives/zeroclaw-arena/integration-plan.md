# ZeroClaw Arena → Slackwater Integration Plan

> **Author:** Lucineer Research Engineer  
> **Date:** 2026-08-03  
> **Status:** Proposed  
> **Estimated effort:** 5-7 days for Phase 1

---

## Executive Summary

ZeroClaw Arena proves that effective action policies can be learned **without neural networks** — using tile-based Monte Carlo self-play, hash-based vector embeddings, and evolutionary score updates. This maps directly to Slackwater's need for an **algorithmic action layer** that makes fast, free, interpretable decisions, reserving expensive LLM calls for genuine reasoning.

The integration strategy is: **port the patterns, not the code.** ZeroClaw is a research prototype focused on games. Slackwater needs the same algorithms applied to cognitive action selection.

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Slackwater Cognition                        │
│                                                              │
│   ┌─────────────┐   ┌──────────────────┐   ┌─────────────┐  │
│   │ LLM Thinker │   │ ZeroClaw Action  │   │ Conductor   │  │
│   │ (semantic)  │   │ Layer (algo)     │   │ (blender)   │  │
│   │             │   │                  │   │             │  │
│   │ • Intent    │──▶│ • Tile lookup    │──▶│ • Priority  │  │
│   │ • Reasoning │   │ • Vector match   │   │ • Routing   │  │
│   │ • Generation│   │ • Policy evolve  │   │ • Synthesis │  │
│   │ • Costs $   │   │ • Free at runtime│   │             │  │
│   └─────────────┘   └──────────────────┘   └─────────────┘  │
│          │                   │                    │          │
│          └───────────────────┼────────────────────┘          │
│                              ▼                                │
│                    ┌──────────────────┐                       │
│                    │ Action Executor  │                       │
│                    │ (performs action)│                       │
│                    └──────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Algorithmic Action Selection Layer (2-3 days)

### Goal
Port ZeroClaw's TileField + CompiledPolicy to Slackwater's action selection domain.

### Step 1.1: Define Slackwater's "Game"

Create a `SlackwaterActionGame` implementing ZeroClaw's game protocol:

```python
class SlackwaterActionGame:
    """A 'game' where the agent decides how to handle incoming messages."""
    
    # State: (channel, sender_type, urgency, time_window, prior_context_hash)
    # Actions: respond_now, defer_30min, escalate, delegate, stay_silent
    # Outcome: user_satisfaction_score (0-1)
    
    def state(self) -> GameState:
        # Serialize current context to string
        return GameState(
            f"ch={self.channel}|sender={self.sender_type}|urg={self.urgency}|time={self.time_window}",
            self.turn, self.current
        )
    
    def legal_actions(self) -> list[str]:
        return ["respond_now", "defer_30min", "escalate", "delegate", "silent"]
    
    def step(self, action: str) -> tuple[float, bool]:
        # Simulate action outcome
        # Return (satisfaction_score, done)
        ...
```

### Step 1.2: Port TileField

Copy `zeroclaw/tile_field.py` with minimal changes:
- Rename `winner` checks to `positive_outcome`
- Adjust softmax temperature for cognitive domain (start at 0.3)
- Add outcome tracking: each action records satisfaction score (not just win/loss)

### Step 1.3: Simulation-Based Training

Train the tile field by simulating message-handling scenarios:

```python
field = TileField(n_simulations=10, temperature=0.3)

for episode in range(1000):
    # Generate random scenario
    scenario = random_scenario()  # channel, sender, urgency, time
    
    # Monte Carlo: for each action, simulate outcome
    game = SlackwaterActionGame(scenario)
    field.train_game(game)
    
    if episode % 25 == 0:
        field.evolve()
```

### Step 1.4: Compile and Deploy

```python
policy = CompiledPolicy.from_tile_field(field)

# At runtime: O(1) action lookup
action = policy(context_hash)
# "respond_now" — free, instant, interpretable
```

### Deliverable
- `slackwater/action_policy/tile_field.py` — adapted TileField
- `slackwater/action_policy/compiled_policy.py` — adapted CompiledPolicy
- `slackwater/action_policy/game.py` — SlackwaterActionGame
- Trained policy file (lookup table)

---

## Phase 2: Vector Pattern Matching for Insights (1-2 days)

### Goal
Port ZeroClaw's VectorDB for the Conductor's insight correlation system.

### Step 2.1: Port VectorDB

Copy `zeroclaw.py`'s `VectorDB` class (SQLite + BLAKE2b embeddings):

```python
class InsightVectorDB:
    """Vector database for insight pattern matching."""
    
    def insert_insight(self, insight_id: str, text: str, metadata: dict):
        vec = self._hash_to_vector(text)
        self.store(insight_id, vec, metadata)
    
    def find_related(self, current_context: str, top_k: int = 5):
        return self.search(current_context, top_k)
```

### Step 2.2: LLM Canonicalization Layer

Since hash embeddings lack semantic awareness, use the LLM to canonicalize text before embedding:

```python
def canonicalize(text: str) -> str:
    """Use LLM to produce canonical form for embedding."""
    # "URGENT: need help now!" → "urgent_help_request"
    # "Can you assist me quickly?" → "urgent_help_request"
    # Both get the same embedding → vector similarity works
    return llm.canonicalize(text)
```

This gives us **semantic vector matching at zero serving cost** — the LLM runs once during canonicalization, but similarity search is pure math.

### Step 2.3: Pattern Discovery

Port ZeroClaw's `analyze_patterns()` to find cognitive patterns:

- **Action-context patterns:** "When sender=primary AND urgency=high → respond_now wins 85%"
- **Temporal patterns:** "Messages after 23:00 → defer_30min has 72% satisfaction"
- **Cross-context transfer:** "Discord patterns partially transfer to Telegram"

### Deliverable
- `slackwater/insights/vector_db.py`
- `slackwater/insights/pattern_discovery.py`
- `slackwater/insights/canonicalize.py`

---

## Phase 3: Evolution Engine for Self-Tuning (1-2 days)

### Goal
Port ZeroClaw's evolution loop for continuous policy weight optimization.

### Step 3.1: Outcome Tracking

Every action records its outcome:

```python
class ActionOutcome:
    action: str
    context_hash: str
    satisfaction_score: float  # 0-1, from user feedback or proxy metrics
    timestamp: float
```

### Step 3.2: Periodic Evolution

Daily evolution pass (via heartbeat or cron):

```python
def evolve_action_policies():
    field = load_action_field()
    
    for context_hash, tile in field.tiles.items():
        for action, data in tile.items():
            recent_outcomes = get_recent_outcomes(context_hash, action, days=7)
            if recent_outcomes:
                avg_satisfaction = mean(o.satisfaction_score for o in recent_outcomes)
                data["score"] += 0.05 * (avg_satisfaction - data["score"])
                data["score"] = clamp(data["score"], 0.05, 0.95)
    
    save_action_field(field)
    recompile_policy(field)
```

### Step 3.3: Hierarchical Context Clustering

Port the hierarchical tiles experiment to group similar contexts:

```python
# Cluster contexts into 8 "strategy archetypes"
contexts = [t.score_vector for t in field.tiles.values()]
labels, centroids = kmeans(contexts, k=8)

# Result: "evening_casual", "morning_urgent", "group_social", etc.
```

This gives the Conductor a vocabulary of **discovered strategy types** — not designer-specified categories.

### Deliverable
- `slackwater/action_policy/evolution.py`
- `slackwater/action_policy/clustering.py`
- Heartbeat job for daily evolution

---

## Phase 4: Fast Path / Slow Path Routing (1 day)

### Goal
Use the compiled policy to route decisions: free lookup for common cases, LLM for novel ones.

### Implementation

```python
def route_decision(context: dict) -> str:
    context_hash = hash_context(context)
    policy = load_compiled_policy()
    
    # Fast path: known context, high confidence
    if context_hash in policy.lookup:
        confidence = policy.confidence(context_hash)
        if confidence > 0.8:
            return policy(context_hash)  # Free. Instant. Done.
    
    # Medium path: similar context found
    similar = policy.nearest_neighbor(context_hash)
    if similar and similar.distance <= 3 and similar.confidence > 0.6:
        return policy(similar.hash)  # Probably good enough
    
    # Slow path: novel context → LLM reasoning
    return llm_decide(context)  # Expensive but necessary
```

### Cost Projection

If 80% of decisions hit the fast path (typical for bounded contexts):
- **Before:** 100% LLM calls × $0.01 each = $1.00 per 100 decisions
- **After:** 80% free + 20% LLM = $0.20 per 100 decisions
- **Savings:** 80% cost reduction on action selection

---

## Risk Mitigation

| Risk | Mitigation |
|---|---|
| Action policy overfits to early data | Use 0.05 learning rate + clamp [0.05, 0.95] |
| Semantic mismatch in hash embeddings | LLM canonicalization layer |
| Stale policy (context drift) | Daily evolution + monthly full retrain |
| Wrong action on novel context | Confidence threshold gates fast path (0.8) |
| No user feedback for satisfaction score | Proxy metrics: response time, follow-up messages, explicit reactions |

---

## Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| Fast path hit rate | >70% of decisions | Log lookup vs LLM calls |
| Action satisfaction | >80% of actions rated positive | User feedback / proxy |
| LLM cost reduction | >50% reduction in action-selection calls | Cost tracking |
| Policy convergence | Stable within 2 weeks of training | Score variance over time |
| Interpretability | 100% of decisions traceable | Tile entry audit log |

---

## Timeline

| Phase | Days | Deliverable |
|---|---|---|
| 1: Action Selection Layer | 2-3 | TileField + CompiledPolicy ported, first trained policy |
| 2: Vector Pattern Matching | 1-2 | Insight VectorDB + canonicalization + pattern discovery |
| 3: Evolution Engine | 1-2 | Self-tuning loop + hierarchical clustering |
| 4: Fast/Slow Routing | 1 | Decision router with confidence thresholds |
| **Total** | **5-7** | **Full algorithmic action layer** |

---

## Long-Term Vision

Once Phase 1-4 are live, future enhancements:

1. **Cross-agent tournaments** — multiple Slackwater instances compete; winners' policies are promoted (the arena model from `FUTURE-INTEGRATION.md`)
2. **Meta-learning** — the system learns HOW to learn (which reward shaping, which temperature, which exploration rate works best for different context types)
3. **Federated policy evolution** — policies from multiple deployments share insights (like ZeroClaw's cross-game transfer, but across users)
4. **Compiled policy distribution** — ship optimized policies as versioned artifacts (like ZeroClaw's `to_python()` output), enabling A/B testing of different policy versions

The endgame: **millions of free action decisions, with LLM reasoning reserved for the 20% of decisions that genuinely require it.**
