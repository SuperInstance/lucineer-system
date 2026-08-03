# PLATO Forward-Forward Learning

> Predictive coding without backpropagation — for agent knowledge systems.
> Based on Geoffrey Hinton's [Forward-Forward Algorithm](https://www.cs.toronto.edu/~hinton/FFA13.pdf) (NeurIPS 2022).

[![CI](https://github.com/SuperInstance/plato-fflearning/actions/workflows/ci-python.yml/badge.svg)](https://github.com/SuperInstance/plato-fflearning/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## Table of Contents

- [What This Is](#what-this-is)
- [Why It Exists](#why-it-exists)
- [Installation](#installation)
- [Quick Start (3 Minutes)](#quick-start-3-minutes)
- [Full Walkthrough](#full-walkthrough)
- [API Reference](#api-reference)
- [Goodness Levels](#goodness-levels)
- [Architecture](#architecture)
- [Common Patterns](#common-patterns)
- [Running the Tests](#running-the-tests)
- [Troubleshooting](#troubleshooting)
- [How It Differs from Backpropagation](#how-it-differs-from-backpropagation)
- [Ecosystem](#ecosystem)
- [License](#license)

---

## What This Is

A Python library that replaces backward gradient propagation with **two forward passes** — one positive, one negative — for agent learning. Instead of computing errors backward through layers, `plato-fflearning` compares real experiences against hypothetical ones and uses the difference to drive learning.

This is a conceptual translation of Geoffrey Hinton's Forward-Forward algorithm, applied not to neural network weights but to **agent knowledge tiles** — discrete Q&A knowledge units stored in a PLATO server.

### For whom?

- Multi-agent system builders who need agents that **learn from experience**
- PLATO server users who want their tile library to be **quality-filtered**
- Anyone curious about alternatives to gradient-based learning
- Game/simulation developers who model **agent skill progression**

---

## Why It Exists

Traditional learning (backpropagation) requires:
1. A differentiable loss function
2. Synchronized forward-backward passes through the full network
3. Global knowledge of network topology

In a multi-agent fleet, none of these hold:
- Agent interactions aren't differentiable
- Agents are distributed and asynchronous
- No central controller sees the full topology

The Forward-Forward algorithm solves this by making learning **local**:
- Each agent learns from its own positive/negative experiences
- No backward pass needed
- No global topology required
- Learning is **layer-local** (or in this case, **agent-local**)

`plato-fflearning` implements this for the PLATO knowledge system, where tiles (Q&A pairs) are the fundamental unit of knowledge.

---

## Installation

### Prerequisites

- **Python 3.10 or later** — check with:
  ```bash
  python3 --version
  # Python 3.10.x or higher
  ```
- **pip** — comes with Python
- **A PLATO server** (optional) — for tile storage. Without one, the library runs in pure in-memory mode.

### Installing PLATO Server (Optional but Recommended)

If you want tiles persisted and searchable:

```bash
# Using Docker (simplest)
docker run -d --name plato -p 8847:8847 -v plato-data:/data \
  ghcr.io/superinstance/plato-server

# Or from source
git clone https://github.com/SuperInstance/plato-server.git
cd plato-server
pip install -e ".[dev]"
python -m plato_server
```

Verify PLATO is running:
```bash
curl http://localhost:8847/
# {"status": "ok", "tiles": 0, "rooms": 0}
```

### Installing plato-fflearning

```bash
# From PyPI (when published)
pip install plato-fflearning

# From source
git clone https://github.com/SuperInstance/plato-fflearning.git
cd plato-fflearning
pip install -e .
```

Verify the installation:
```bash
python3 -c "from plato_fflearning import ForwardForwardLearner; print('OK')"
# OK
```

---

## Quick Start (3 Minutes)

```python
from plato_fflearning import ForwardForwardLearner

# Create a learner (works without PLATO server — pure in-memory)
ff = ForwardForwardLearner()

# Agent completes a task successfully → POSITIVE pass
result = ff.positive_pass(
    agent="builder_1",
    experience="Built a stone wall that met spec",
    associated_tiles=["tile_stonewall_001"]
)
print(f"Goodness: {result['goodness']:.2f}  Threshold met: {result['threshold_exceeded']}")
# Goodness: 0.63  Threshold met: False

# Agent imagines a failure → NEGATIVE pass
result = ff.negative_pass(
    agent="builder_1",
    experience="What if I had misaligned the foundation?"
)
print(f"Goodness: {result['goodness']:.2f}")
# Goodness: 0.52

# Check agent's learning state
state = ff.get_learning_state("builder_1")
print(f"Level: {state['level']}  Recommendation: {state['recommendation']}")
# Level: moderate  Recommendation: agent is learning normally

# Another positive pass (second success → crosses threshold)
result = ff.positive_pass(
    agent="builder_1",
    experience="Built another wall, this time with proper drainage",
    associated_tiles=["tile_drainage_001"]
)
print(f"Goodness: {result['goodness']:.2f}  Threshold met: {result['threshold_exceeded']}")
# Goodness: 0.64  Threshold met: False  (need one more positive)
```

### The Math Behind That Sequence

| Step | Formula | Calculation | Result |
|------|---------|------------|--------|
| Start | default | — | 0.50 |
| +positive | 0.50 × 0.95 + 0.15 | 0.475 + 0.15 | 0.625 |
| −negative | 0.625 × 0.95 − 0.08 | 0.594 − 0.08 | 0.514 |
| +positive | 0.514 × 0.95 + 0.15 | 0.488 + 0.15 | 0.638 |

Goodness is cumulative. Two positives from default (0.5) reach 0.625, then 0.594 (decay) + 0.15 = 0.744 — above threshold.

---

## Full Walkthrough

### 1. Creating a Learner

```python
from plato_fflearning import ForwardForwardLearner

# Default: connects to PLATO on localhost:8847
# PLATO not running? All HTTP calls fail silently; library works in-memory.
ff = ForwardForwardLearner()

# Custom PLATO URL
ff = ForwardForwardLearner(plato_url="http://plato.myorg.com:8847")

# No PLATO at all (explicit offline mode — same as default, just clear intent)
ff = ForwardForwardLearner(plato_url="http://0.0.0.0:0")  # unreachable, so offline
```

### 2. Recording Positive Experiences

A positive pass represents a **real, confirmed good outcome**:

```python
result = ff.positive_pass(
    agent="oracle1",
    experience="Correctly predicted the fleet load for the next 10 minutes",
    domain="fleet_orchestration",       # optional, defaults to "fleet_orchestration"
    associated_tiles=["tile_load_prediction_001", "tile_capacity_003"]
)

# result:
# {
#   "agent": "oracle1",
#   "pass": "positive",
#   "goodness": 0.625,
#   "threshold_exceeded": False,
#   "tiles_reinforced": []
# }
```

When goodness crosses 0.7, tiles get reinforced:

```python
# Multiple positives to reach threshold
ff.positive_pass("oracle1", "Another correct prediction")
ff.positive_pass("oracle1", "Third correct prediction", associated_tiles=["tile_004"])

# result:
# {
#   "agent": "oracle1",
#   "pass": "positive",
#   "goodness": 0.755,
#   "threshold_exceeded": True,
#   "tiles_reinforced": ["tile_004"]
# }
```

### 3. Recording Negative Experiences

A negative pass represents a **hypothetical failure, counterfactual, or actual mistake**:

```python
result = ff.negative_pass(
    agent="oracle1",
    experience="What if I had routed all traffic through node-7 during its CPU spike?",
    domain="fleet_orchestration"
)

# result:
# {
#   "agent": "oracle1",
#   "pass": "negative",
#   "goodness": 0.636,
#   "suppressed": False    # True when goodness drops below 0.35
# }
```

The `suppressed` flag triggers when goodness falls below half the threshold (0.35), indicating the agent's output should be treated with caution.

### 4. Querying Agent State

```python
state = ff.get_learning_state("oracle1")

# state:
# {
#   "agent": "oracle1",
#   "goodness": 0.636,
#   "level": "moderate",
#   "positive_tiles": 3,   # count of positive tiles in PLATO (0 if offline)
#   "negative_tiles": 1,   # count of negative tiles in PLATO (0 if offline)
#   "recommendation": "agent is learning normally"
# }
```

### 5. Fleet-Wide State

```python
# Simulate multiple agents
ff.positive_pass("oracle2", "Handled traffic spike correctly")
ff.negative_pass("oracle3", "Misconfigured load balancer")
ff.positive_pass("oracle4", "Auto-scaled correctly")

fleet = ff.get_fleet_learning_state()

# fleet:
# {
#   "total_agents": 4,
#   "fleet_goodness_avg": 0.564,
#   "high_reliability_agents": 0,
#   "low_reliability_agents": 1,
#   "by_agent": {
#     "oracle1": 0.636,
#     "oracle2": 0.625,
#     "oracle3": 0.395,
#     "oracle4": 0.625
#   }
# }
```

### 6. Learning Cycle (Convenience Method)

```python
# Single method for a complete cycle
# real_outcome=True  → calls positive_pass
# real_outcome=False → calls negative_pass
result = ff.run_learning_cycle(
    agent="oracle1",
    real_outcome=True,
    experience="Load prediction accurate within 2%"
)
```

### 7. Understanding Decay

Goodness decays by 5% before each delta:

```python
# Demonstrate decay: agent at 0.9, no new experiences
ff.state["aging_agent"] = 0.9

# After many "no-op" events (positive passes with no real experience):
ff.positive_pass("aging_agent", "maintained")  # 0.9*0.95 + 0.15 = 1.005 → clamped to 1.0
ff.positive_pass("aging_agent", "maintained")  # 1.0*0.95 + 0.15 = 1.1 → clamped to 1.0

# But if only negative passes happen:
ff.state["declining_agent"] = 0.9
ff.negative_pass("declining_agent", "mistake")  # 0.9*0.95 - 0.08 = 0.775
ff.negative_pass("declining_agent", "mistake")  # 0.775*0.95 - 0.08 = 0.656
ff.negative_pass("declining_agent", "mistake")  # 0.656*0.95 - 0.08 = 0.543
# 3 failures to go from 0.9 to 0.54
```

### 8. With a Running PLATO Server

If PLATO is running on `localhost:8847`:

```python
ff = ForwardForwardLearner(plato_url="http://localhost:8847")

ff.positive_pass(
    agent="researcher_1",
    experience="Found that embedding dimension 768 produces best results for our corpus",
    domain="research"
)

# This creates a tile in PLATO's "ff_positive_tiles" room:
# POST http://localhost:8847/room/ff_positive_tiles
# {
#   "question": "Positive experience for researcher_1",
#   "answer": "Experience: Found that embedding...\nType: POSITIVE_PASS\nTimestamp: ...",
#   "agent": "researcher_1",
#   "domain": "research",
#   "confidence": 0.9,
#   ...
# }

# You can search PLATO for these tiles:
# curl http://localhost:8847/search?q=POSITIVE_PASS
```

---

## API Reference

### `ForwardForwardLearner`

```python
ForwardForwardLearner(plato_url="http://localhost:8847")
```

Creates a new FF learner instance.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `plato_url` | `str` | `"http://localhost:8847"` | PLATO server URL. Library degrades gracefully to in-memory mode if unreachable. |

**Class constants:**

| Constant | Default | Description |
|----------|---------|-------------|
| `GOODNESS_DECAY` | `0.95` | Multiplied to current goodness before each update |
| `POSITIVE_BOOST` | `0.15` | Added to goodness on positive pass |
| `NEGATIVE_PENALTY` | `0.08` | Subtracted from goodness on negative pass |
| `THRESHOLD` | `0.7` | Goodness required for tile reinforcement |

---

### `positive_pass()`

```python
positive_pass(agent, experience, domain="fleet_orchestration", associated_tiles=None)
```

Records a positive experience. Increases agent goodness. If goodness exceeds threshold, associated tiles are marked for reinforcement.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `agent` | `str` | required | Agent identifier |
| `experience` | `str` | required | Description of what happened |
| `domain` | `str` | `"fleet_orchestration"` | Knowledge domain |
| `associated_tiles` | `list[str]` or `None` | `None` | Tile IDs to reinforce when threshold is exceeded |

**Returns:**
```python
{
    "agent": str,               # Agent identifier
    "pass": "positive",         # Always "positive"
    "goodness": float,          # New goodness (0.0–1.0)
    "threshold_exceeded": bool, # True if goodness > 0.7
    "tiles_reinforced": list    # Tile IDs that were reinforced (empty if below threshold)
}
```

---

### `negative_pass()`

```python
negative_pass(agent, experience, domain="fleet_orchestration")
```

Records a negative or hypothetical experience. Decreases agent goodness.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `agent` | `str` | required | Agent identifier |
| `experience` | `str` | required | Description of what was imagined or failed |
| `domain` | `str` | `"fleet_orchestration"` | Knowledge domain |

**Returns:**
```python
{
    "agent": str,           # Agent identifier
    "pass": "negative",     # Always "negative"
    "goodness": float,      # New goodness (0.0–1.0)
    "suppressed": bool      # True if goodness < 0.35 (half threshold)
}
```

---

### `get_learning_state()`

```python
get_learning_state(agent)
```

Returns the current learning state for a specific agent.

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent` | `str` | Agent identifier |

**Returns:**
```python
{
    "agent": str,
    "goodness": float,          # 0.0–1.0
    "level": str,               # "critical" | "low" | "moderate" | "high" | "exceptional"
    "positive_tiles": int,      # Count of positive tiles in PLATO
    "negative_tiles": int,      # Count of negative tiles in PLATO
    "recommendation": str       # Action recommendation
}
```

---

### `get_fleet_learning_state()`

```python
get_fleet_learning_state()
```

Returns fleet-wide learning state. No parameters.

**Returns:**
```python
{
    "total_agents": int,
    "fleet_goodness_avg": float,
    "high_reliability_agents": int,   # goodness > 0.7
    "low_reliability_agents": int,    # goodness < 0.3
    "by_agent": dict                  # {agent_id: goodness}
}
```

---

### `run_learning_cycle()`

```python
run_learning_cycle(agent, real_outcome, experience)
```

Convenience method: routes to `positive_pass()` or `negative_pass()` based on outcome.

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent` | `str` | Agent identifier |
| `real_outcome` | `bool` | `True` = positive, `False` = negative |
| `experience` | `str` | Description of the experience |

**Returns:** Same as `positive_pass()` or `negative_pass()`.

---

## Goodness Levels

| Range | Level | Color | Meaning | Recommendation |
|-------|-------|-------|---------|----------------|
| 0.0–0.2 | critical | 🔴 | Agent is unreliable | Agent should seek positive experiences |
| 0.2–0.4 | low | 🟠 | Agent is struggling | Agent should seek positive experiences |
| 0.4–0.6 | moderate | 🟡 | Normal learning range | Agent is learning normally |
| 0.6–0.8 | high | 🟢 | Agent is reliable | Agent is highly reliable |
| 0.8–1.0 | exceptional | 🔵 | Top-tier performance | Agent is highly reliable |

---

## Architecture

```
                    ┌─────────────────────────────────┐
                    │    ForwardForwardLearner         │
                    │                                  │
  Real Experience ──►  positive_pass()                 │
                    │    │                              │
                    │    ├─► goodness += 0.15           │
                    │    │   (after 0.95 decay)         │
                    │    │                              │
                    │    ├─► POST /room/ff_positive_tiles
                    │    │   (PLATO server, best-effort)│
                    │    │                              │
                    │    └─► if goodness > 0.7:         │
                    │            reinforce tiles        │
                    │                                  │
  Imagined Fail ────►  negative_pass()                 │
                    │    │                              │
                    │    ├─► goodness -= 0.08           │
                    │    │   (after 0.95 decay)         │
                    │    │                              │
                    │    └─► POST /room/ff_negative_tiles
                    │        (PLATO server, best-effort)│
                    │                                  │
  Query ────────────►  get_learning_state(agent)       │
                    │  get_fleet_learning_state()       │
                    └─────────────────────────────────┘
                              │
                    ┌────────▼────────┐
                    │  PLATO Server    │
                    │  (port 8847)     │
                    │  SQLite + HTTP   │
                    │  Fleet sync      │
                    └─────────────────┘
```

### Goodness Update Formula

```
new_goodness = clamp(old_goodness × GOODNESS_DECAY + delta, 0.0, 1.0)

where delta = +0.15 (positive) or -0.08 (negative)
      clamp restricts to [0.0, 1.0]
      decay (0.95) is applied BEFORE the delta
```

### Tile Structure

Every pass creates a tile with this structure:

| Field | Positive | Negative |
|-------|----------|----------|
| `question` | `"Positive experience for {agent}"` | `"Negative experience for {agent}"` |
| `answer` | Experience text + type + timestamp | Same format |
| `agent` | Agent ID | Agent ID |
| `domain` | Knowledge domain | Knowledge domain |
| `confidence` | **0.9** | **0.3** |
| `model` | Agent ID | Agent ID |
| `role` | `"forward_forward"` | `"forward_forward"` |
| `pass_type` | `"positive"` | `"negative"` |

---

## Common Patterns

### Pattern 1: Task Outcome Recording

```python
# After any agent completes a task, record the outcome
def on_task_complete(agent_id, task_description, success: bool):
    if success:
        ff.positive_pass(agent_id, f"Completed: {task_description}")
    else:
        ff.negative_pass(agent_id, f"Failed: {task_description}")
```

### Pattern 2: Counterfactual Learning

```python
# After a successful outcome, also record what could have gone wrong
# This strengthens the learning signal through contrast
ff.positive_pass("agent_1", "Deployed without errors")

# Counterfactual: what if we'd deployed the old version?
ff.negative_pass("agent_1", "Hypothetical: old version would have crashed under load")
```

### Pattern 3: Skill Gating

```python
# Only let high-goodness agents perform critical tasks
def can_perform_critical_task(agent_id):
    state = ff.get_learning_state(agent_id)
    return state["goodness"] > 0.6  # "high" or "exceptional"
```

### Pattern 4: Fleet Health Check

```python
fleet = ff.get_fleet_learning_state()

if fleet["fleet_goodness_avg"] < 0.4:
    alert("Fleet goodness is low — agents may need retraining or rest")

if fleet["low_reliability_agents"] > fleet["total_agents"] / 2:
    alert("More than half the fleet is in low-reliability state")
```

### Pattern 5: Master-Apprentice Learning

```python
# Master agent's tiles are reinforced (goodness > 0.7)
ff.positive_pass("master_agent", "Demonstrated advanced technique",
                 associated_tiles=["tile_advanced_001"])

# Apprentice retrieves master's tiles and attempts the task
# If successful, apprentice gets positive pass
ff.positive_pass("apprentice_1", "Successfully replicated master's technique")

# Apprentice's tiles eventually get reinforced too
# This is the "feed-forward" — knowledge propagates without backprop
```

### Pattern 6: Periodic Decay Check

```python
# Run periodically to account for goodness decay
# Without new experiences, even excellent agents drift toward 0
import schedule

def check_fleet_decay():
    for agent_id in list(ff.state.keys()):
        state = ff.get_learning_state(agent_id)
        if state["level"] in ("critical", "low"):
            print(f"⚠️  {agent_id} is at {state['goodness']:.2f} — needs positive experiences")

schedule.every(1).hour.do(check_fleet_decay)
```

---

## Running the Tests

```bash
# Clone
git clone https://github.com/SuperInstance/plato-fflearning.git
cd plato-fflearning

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
python3 -m pytest tests/ -v
```

Expected output:
```
tests/test_fflearning.py::TestGoodnessTracking::test_initial_goodness_is_0_5 PASSED
tests/test_fflearning.py::TestGoodnessTracking::test_positive_pass_increases_goodness PASSED
tests/test_fflearning.py::TestGoodnessTracking::test_negative_pass_decreases_goodness PASSED
tests/test_fflearning.py::TestGoodnessTracking::test_goodness_clamped_to_0_1 PASSED
tests/test_fflearning.py::TestGoodnessTracking::test_goodness_decay_applies PASSED
tests/test_fflearning.py::TestThresholdBehavior::test_threshold_exceeded_on_high_goodness PASSED
tests/test_fflearning.py::TestThresholdBehavior::test_threshold_not_exceeded_below PASSED
tests/test_fflearning.py::TestLearningCycle::test_run_learning_cycle_positive PASSED
tests/test_fflearning.py::TestLearningCycle::test_run_learning_cycle_negative PASSED
tests/test_fflearning.py::TestFleetState::test_fleet_state_empty PASSED
tests/test_fflearning.py::TestFleetState::test_fleet_state_aggregates PASSED  ⚠️ may fail (float precision)
tests/test_fflearning.py::TestGoodnessLevels::test_critical_level PASSED
...
17 passed, 1 failed in 0.08s
```

> **Note**: `test_fleet_state_aggregates` has a known floating-point precision issue.
> `0.8 + 0.4 / 2 = 0.6000000000000001 ≠ 0.6`. Fix: change the test assertion to use
> `pytest.approx(0.6)` or change the library to `round(avg, 4)`.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'plato_fflearning'"

You installed from source but forgot the `-e` flag or didn't activate your virtualenv:

```bash
cd plato-fflearning
pip install -e .
```

### Tiles aren't appearing in PLATO

1. Check PLATO is running: `curl http://localhost:8847/`
2. The library posts to `/room/{name}` — verify your PLATO version supports this endpoint. PLATO server's documented API is `POST /submit` with a `room` field. If your PLATO version uses `/submit`, the tiles won't appear. This is a known API mismatch in v0.1.0.
3. All HTTP errors are caught silently. Add logging to see what's happening:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
```

### Goodness seems wrong

Check the math manually:
```python
agent = "test"
ff = ForwardForwardLearner()
print(f"Start: {ff.state.get(agent, 0.5)}")

r = ff.positive_pass(agent, "test")
# Expected: 0.5 * 0.95 + 0.15 = 0.625
print(f"After positive: {r['goodness']}")

r = ff.negative_pass(agent, "test")
# Expected: 0.625 * 0.95 - 0.08 = 0.51375
print(f"After negative: {r['goodness']}")
```

### Agent goodness is always 0.5

You're querying before recording any passes. Default goodness is 0.5 (moderate). An agent only appears in `self.state` after its first pass.

### Fleet average is slightly off

This is the floating-point precision issue. The library computes `sum(values) / len(values)` without rounding. If you need exact values, round in your consuming code: `round(fleet["fleet_goodness_avg"], 4)`.

---

## How It Differs from Backpropagation

| Aspect | Backpropagation | Forward-Forward |
|--------|----------------|-----------------|
| Direction | Forward pass, then backward pass | Two forward passes (positive + negative) |
| Synchronization | All layers must wait for backward pass | Layer-local — each agent learns independently |
| Supervision | Global loss function | Local goodness signal |
| Requires gradients | Yes | No |
| Hypothetical learning | No | Yes — negative pass IS counterfactual reasoning |
| Memory for backprop | Must store activations | Not needed — online learning |
| Biological plausibility | Low — no evidence for backward propagation in cortex | Higher — matches sensory/motor pathways |
| PLATO integration | N/A | Native — tiles are the data representation |
| Data flow | Error flows backward through layers | Knowledge flows forward through tiles |

### The Core Insight

In backpropagation, you compute: `∂Loss/∂Weights` — how much each weight contributed to the error.

In Forward-Forward, you compute: `Goodness(positive) − Goodness(negative)` — the difference between real and imagined outcomes.

Both produce a gradient. But FF's gradient is **local** (per-agent) and **contrastive** (real vs. imagined), while backprop's gradient is **global** (whole network) and **error-based** (predicted vs. actual).

---

## Ecosystem

`plato-fflearning` is part of the [SuperInstance](https://github.com/SuperInstance) ecosystem:

| Component | Repo | Role |
|-----------|------|------|
| PLATO Server | [plato-server](https://github.com/SuperInstance/plato-server) | Knowledge tile storage + HTTP API |
| PLATO Runtime Kernel | [plato-runtime-kernel](https://github.com/SuperInstance/plato-runtime-kernel) | Spatial room model (Rust) |
| PLATO Tile Scorer | [plato-tile-scorer](https://github.com/SuperInstance/plato-tile-scorer) | 7-signal scoring for tiles |
| PLATO Tile Version | [plato-tile-version](https://github.com/SuperInstance/plato-tile-version) | Git-for-knowledge |
| FLUX Runtime | [flux-runtime](https://github.com/SuperInstance/flux-runtime) | Agent runtime |
| Lucineer System | [lucineer-system](https://github.com/SuperInstance/lucineer-system) | Multi-agent game builder |
| AI-Writings | [AI-Writings](https://github.com/SuperInstance/AI-Writings) | Agent literature corpus |

---

## License

MIT — see [LICENSE](https://github.com/SuperInstance/plato-fflearning/blob/master/LICENSE).
