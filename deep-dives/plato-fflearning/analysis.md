# PLATO Forward-Forward Learning — Architecture Analysis

> **Deep-dive analysis of `plato-fflearning` v0.1.0**
> Repo: https://github.com/SuperInstance/plato-fflearning
> Commit: `7b2cddc` (master, 2025)
> License: MIT

---

## 1. Executive Summary

`plato-fflearning` is a Python library that applies Geoffrey Hinton's **Forward-Forward (FF) algorithm** — a biologically plausible alternative to backpropagation — to the PLATO knowledge-tile ecosystem. Instead of computing gradients backward through a network, FF uses two competing forward passes: one on real data (positive) and one on hypothetical data (negative). The gradient *between* them drives learning.

In PLATO terms: when an agent has a real experience, goodness goes up. When it imagines a failure, goodness goes down. When goodness exceeds a threshold, the agent's knowledge tiles get reinforced in the PLATO server. This replaces gradient descent with **experience-driven tile reinforcement**.

---

## 2. Purpose and Scope

### What it does
- Tracks a **goodness score** (0.0–1.0) per agent
- Records positive and negative experiences as PLATO tiles
- Triggers tile reinforcement when goodness crosses a threshold
- Provides fleet-wide learning visibility

### What it does not do (v0.1.0 limitations)
- **No persistent state**: Goodness is tracked in an in-memory Python dict (`self.state`). If the process restarts, all state is lost.
- **No real tile reinforcement**: `_reinforce_tiles()` is a stub that appends IDs to a list without calling PLATO's `/submit` endpoint.
- **No actual FF computation on neural layers**: This is not a neural network library. It's a conceptual translation of FF principles into agent knowledge management.
- **No negative tile weakening**: Negative passes decrease goodness but don't actually mark tiles as unreliable in PLATO.
- **Floating-point precision bug**: Fleet average test fails due to `0.8 + 0.4 / 2 = 0.6000000000000001 ≠ 0.6`.

### Scope boundary
This is a **v0.1.0 proof-of-concept** that demonstrates how FF principles map onto tile-based knowledge systems. It's architecturally sound but production-incomplete.

---

## 3. File Inventory

| File | Lines | Purpose |
|------|-------|---------|
| `plato_fflearning/__init__.py` | 195 | Entire library — single module |
| `tests/test_fflearning.py` | 174 | 18 tests across 6 test classes |
| `pyproject.toml` | 16 | Build config, deps: `requests>=2.28` |
| `.github/workflows/ci-python.yml` | 28 | CI: Python 3.10/3.11/3.12, flake8 + pytest |
| `README.md` | — | User-facing docs |
| `LICENSE` | — | MIT |

**Total source: 195 lines.** This is a single-file library.

---

## 4. Architecture Deep-Dive

### 4.1 Class: `ForwardForwardLearner`

The entire library is one class with four configuration constants:

```python
GOODNESS_DECAY = 0.95    # Decay applied before each delta
POSITIVE_BOOST = 0.15    # Added on positive pass
NEGATIVE_PENALTY = 0.08  # Subtracted on negative pass
THRESHOLD = 0.7          # Reinforcement trigger
```

### 4.2 Goodness Formula

```
new_goodness = clamp(old_goodness × DECAY + delta, 0.0, 1.0)
```

Where `delta` is `+0.15` for positive passes and `-0.08` for negative passes.

The decay-before-boost formula means:
- **From 0.5** (default): one positive → `0.5 × 0.95 + 0.15 = 0.625`
- **From 0.5**: one negative → `0.5 × 0.95 - 0.08 = 0.395`
- **To reach threshold (0.7)**: needs ~2 consecutive positives from 0.5

This creates an **asymmetric learning dynamic**: positives are nearly 2× stronger than negatives. An agent recovers from failures faster than it descends into them, but goodness decays toward zero over time unless reinforced.

### 4.3 PLATO Integration Points

The library makes HTTP calls to a PLATO server (default: `http://localhost:8847`):

| Method | Endpoint | When |
|--------|----------|------|
| `POST` | `/room/ff_positive_tiles` | Every `positive_pass()` |
| `POST` | `/room/ff_negative_tiles` | Every `negative_pass()` |
| `GET` | `/room/{name}?limit=100` | `get_learning_state()` counts tiles |

**Note**: The library uses `/room/{name}` but PLATO server's documented API uses `/submit` with a `room` field. There's an API mismatch — the library posts to `/room/ff_positive_tiles` while PLATO expects `/submit` with `{"room": "ff_positive_tiles"}`. All HTTP calls are wrapped in `try/except` with silent failure, so the library works standalone (degrading to pure in-memory operation).

### 4.4 Tile Structure

Positive tile:
```json
{
  "question": "Positive experience for oracle1",
  "answer": "Experience: ...\nType: POSITIVE_PASS\nTimestamp: 1234567.89",
  "agent": "oracle1",
  "domain": "fleet_orchestration",
  "confidence": 0.9,
  "model": "oracle1",
  "role": "forward_forward",
  "pass_type": "positive"
}
```

Negative tile:
```json
{
  "question": "Negative experience for oracle1",
  "answer": "Experience: ...\nType: NEGATIVE_PASS\nTimestamp: 1234567.89",
  "agent": "oracle1",
  "domain": "fleet_orchestration",
  "confidence": 0.3,
  "model": "oracle1",
  "role": "forward_forward",
  "pass_type": "negative"
}
```

Confidence is hardcoded: 0.9 for positive, 0.3 for negative.

### 4.5 Goodness Levels

| Range | Level | Recommendation |
|-------|-------|----------------|
| 0.0–0.2 | critical | Agent needs positive experiences urgently |
| 0.2–0.4 | low | Agent is struggling, needs reinforcement |
| 0.4–0.6 | moderate | Normal learning range |
| 0.6–0.8 | high | Agent is reliable |
| 0.8–1.0 | exceptional | Top-tier performance |

### 4.6 Fleet Operations

`get_fleet_learning_state()` aggregates across all tracked agents:
- Total agent count
- Fleet-wide average goodness
- Count of high-reliability (>0.7) and low-reliability (<0.3) agents
- Per-agent goodness breakdown

---

## 5. Test Analysis

18 tests across 6 classes:

| Test Class | Tests | Coverage |
|-----------|-------|----------|
| `TestGoodnessTracking` | 5 | Initial value, positive/negative effects, clamping, decay |
| `TestThresholdBehavior` | 2 | Threshold crossing, tile reinforcement triggering |
| `TestLearningCycle` | 2 | `run_learning_cycle()` dispatch |
| `TestFleetState` | 2 | Empty fleet, aggregation |
| `TestGoodnessLevels` | 5 | All 5 goodness level bands |
| `TestTileCreation` | 2 | Tile field structure via mock |

**Known failure**: `test_fleet_state_aggregates` — floating point precision (`0.6000000000000001 ≠ 0.6`). The test uses `==` instead of `pytest.approx()`.

**Test quality**: Tests directly manipulate `ff.state` dict rather than going through realistic learning sequences. Mock-based HTTP tests monkey-patch `requests.post` at module level. This works but is fragile.

---

## 6. Design Patterns

### Pattern 1: Experience as Tiles
Every experience — real or imagined — becomes a structured tile stored in PLATO. This means the learning system also builds a searchable experience log.

### Pattern 2: Decay-Based Forgetting
The `0.95` decay factor means old experiences matter less. After ~13 events without reinforcement, an agent's goodness halves. This prevents stale expertise from dominating.

### Pattern 3: Asymmetric Penalties
Positive boost (0.15) is nearly double the negative penalty (0.08). This is deliberate: an agent should recover from failures, not spiral into permanent low-goodness. But it means agents can accumulate unjustified high goodness if negative passes are rare.

### Pattern 4: Threshold-Gated Reinforcement
Tiles only get reinforced when goodness exceeds 0.7. This prevents low-confidence agents from polluting the knowledge base. But there's no corresponding mechanism to *degrade* tiles when goodness is critically low.

### Pattern 5: Silent Degradation
All network calls fail silently. The library works standalone as a pure in-memory goodness tracker. This is good for testing and bad for production — you won't know if PLATO integration is broken.

---

## 7. Dependencies

| Dependency | Version | Purpose |
|-----------|---------|---------|
| `requests` | ≥2.28 | HTTP calls to PLATO server |
| `pytest` | ≥7.0 (dev) | Testing |
| Python | ≥3.10 | Type hints (`Dict[str, float]` etc.) |

No external ML frameworks. No numpy. No torch. Pure Python.

---

## 8. Relationship to Hinton's FF Algorithm

| Hinton's FF (Neural) | PLATO FF (Knowledge) |
|----------------------|---------------------|
| Layer activations | Agent goodness score |
| Positive data (real labels) | Real agent experiences |
| Negative data (wrong labels) | Imagined failures / counterfactuals |
| Goodness = sum of squared activities | Goodness = decayed accumulation of ±delta |
| Layer-local learning | Agent-local learning |
| Backprop-free weight updates | Backprop-free tile reinforcement |
| MNIST, CIFAR benchmarks | Fleet orchestration, knowledge management |

The mapping is conceptual, not mathematical. Hinton's FF computes a literal sum-of-squares goodness per layer; PLATO FF uses a decayed additive accumulator. The key insight transfer is the **dual-pass structure** (positive/negative replacing forward/backward).

---

## 9. Code Quality Assessment

### Strengths
- Clean, readable single-file design
- Good docstrings explaining the FF analogy
- Comprehensive test coverage for the core goodness logic
- Graceful network failure handling
- Type hints throughout

### Weaknesses
- `_reinforce_tiles()` is a no-op stub
- No persistence (in-memory only)
- API mismatch with actual PLATO server (`/room/{name}` vs `/submit`)
- Float precision bug in fleet average
- No way to configure constants (DECAY, BOOST, etc.) without subclassing
- No logging — all failures are silent
- `domain` defaults to `"fleet_orchestration"` — hardcoded bias
- CI config uses `|| true` on pytest, masking failures

---

## 10. Ecosystem Context

`plato-fflearning` sits in the SuperInstance/PLATO ecosystem alongside:

- **plato-server**: The knowledge tile server it calls via HTTP
- **plato-runtime-kernel**: Spatial room model (Rust) — tiles live in rooms
- **plato-tile-scorer**: 7-signal scoring for tiles — FF goodness could become an 8th signal
- **plato-tile-version**: Git-for-knowledge — versioned tile history
- **flux-runtime**: Agent runtime that could consume FF-enriched tiles
- **categorical-agents**: Category theory for agent composition — FF could drive composition decisions

The library is one of 72+ PLATO crates/repos, and represents the **learning layer** of the stack.

---

## 11. Verdict

`plato-fflearning` v0.1.0 is a well-designed proof-of-concept that successfully translates Hinton's Forward-Forward algorithm from neural networks to agent knowledge management. The core insight — that agents can learn from both real experiences (positive passes) and imagined failures (negative passes) without a backward gradient — is sound and interesting.

However, it's architecturally incomplete: in-memory only, stub reinforcement, API mismatch, and one failing test. As a conceptual foundation and design document, it's excellent. As production code, it needs another iteration.

**Rating: 7/10** — Strong design, solid tests, incomplete implementation.
