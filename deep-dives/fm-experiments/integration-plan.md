# fm-experiments — Integration with Slackwater

**Date:** 2026-08-03
**Reference:** `/home/eileen/projects/lucineer-system/INTEGRATED_ARCHITECTURE.md`

---

## 1. Component Mapping

| fm-experiments Component | Slackwater Equivalent | Compatibility |
|-------------------------|----------------------|---------------|
| Wheel of Discovery | Experiment-driven architecture phase | **Direct adoption.** The Wheel is exactly what Slackwater needs for design validation. |
| Delta-Detect (saturation detector) | Flow State Detector (planned Chisel) | **Strong parallel.** Both detect when a system has exhausted its current level. |
| E4 Eigenvalue analysis | No equivalent | **Methodology transfer.** Spectral analysis techniques for coupling matrices. |
| Pre-registered triggers | Court Integration Test assertions | **Pattern adoption.** Pre-define what result triggers what action. |
| Confidence tiers (BEDROCK/SOLID/SUGGESTIVE) | Grain maturation stages | **Conceptual alignment.** BEDROCK ↔ Worn Smooth (500+ uses). |
| Fleet Ops Handbook | TOOLS.md routing strategy | **Direct parallel.** Both define model routing by task type. |
| Night Synthesis culture | No equivalent | **Cultural adoption.** Honest negative results, no cherry-picking. |

---

## 2. Integration Seams

### 2.1 Wheel of Discovery → Slackwater Design Validation (Immediate)

The INTEGRATED_ARCHITECTURE.md defines 8 implementation phases, 12 design primitives, and 7 Court tiers — all currently **unvalidated by experiment**.

The Wheel of Discovery provides the framework to validate them:

```python
# Define Slackwater hypotheses as Findings:
finding = Finding(
    id="SW-001",
    statement="Puffin calls with 15-min TTL achieve >90% agent discovery rate",
    confidence=Confidence.OPEN,
    evidence=[],
    variables=["puffin_ttl", "fleet_size", "discovery_rate"],
)

# Design experiment:
experiment = Experiment(
    id="SW-EXP-001",
    hypothesis="Puffin call discovery rate > 90% when TTL=15min and fleet<10",
    independent_vars=["puffin_ttl"],
    dependent_vars=["discovery_rate"],
    predictions={
        "rate > 90%": "15-min TTL is sufficient for small fleets",
        "rate < 70%": "Need shorter TTL or wider propagation radius",
    },
    decision_criteria="If rate < 90% at TTL=15min, reduce to 10min or add 2nd ring",
    priority=1,
)
```

**Concrete integration:**
1. Port `WheelOfDiscovery` class structure
2. Seed with hypotheses from INTEGRATED_ARCHITECTURE.md design claims
3. Run experiments testing each claim
4. Let findings drive implementation priority (as the roadmap does)

### 2.2 Delta-Detect → Flow State Detector (Near-term)

The Chisel pattern in the architecture includes a `FlowStateDetector`:

> "FlowStateDetector | Wraps: Flow detection | Accumulates: Flow signatures, frustration precursors, intervention timing"

The delta-detect implementation is a **saturation detector** — it knows when a model has exhausted its current capacity. This maps to flow detection:

| Delta-Detect | Slackwater Flow State |
|-------------|----------------------|
| Attention entropy collapsed (→0) | Agent stuck in repetitive loop |
| Attention entropy uniform (→1) | Agent overwhelmed, can't focus |
| Gradient magnitude → 0 | No learning happening, stale |
| Representation variance collapsed | All agent outputs identical |
| QUANTITATIVE exhaustion | Needs more data/time (same Court) |
| QUALITATIVE exhaustion | Needs architecture change (Court elevation) |

**Integration design:**
- Wrap as a Chisel: `FlowStateDetector` accumulates grain about when agents enter/exit flow
- Use saturation signals to trigger Dance Floor detection
- QUANTITATIVE → stay in current Court, provide more resources
- QUALITATIVE → trigger Court transition

### 2.3 Fleet Ops Handbook → Model Routing (Immediate)

The Fleet Ops Handbook contains battle-tested model routing wisdom:

| Task | Route To | Notes |
|------|----------|-------|
| Code generation | z.ai (paid) | Best syntax accuracy |
| Document summarization | z.ai (paid) | Handles long context |
| Arithmetic | DeepInfra | Cheaper, sufficient |
| Translation | Hermes via DeepInfra | See cross-lingual gotchas |

Plus critical operational knowledge:
- **Vocabulary Wall detection:** 3+ identical consecutive tokens → kill stream immediately
- **Pre-computation protocol:** Extract numbers, compute locally, inject as facts
- **Cross-lingual gotchas:** Japanese hurts math accuracy by 12-18%, Spanish drops negation 7%
- **Stage classification:** 6-probe method for new models

This maps directly to Slackwater's TOOLS.md model routing strategy and should be integrated.

### 2.4 Pre-Registered Triggers → Court Integration Tests

The INTEGRATED_ARCHITECTURE.md defines Court tests with assertions:

> "Court IV: Capture the Flag — Asserts: 4+ agents converge without coordinator."

fm-experiments adds the methodology: **pre-register what result triggers what action.**

Example from `EXPERIMENT-ROADMAP.md`:
```
Finding: r < -0.7 (strong correlation)
Trigger: Merge GL(9) fault detection into conservation daemon

Finding: -0.7 < r < -0.3 (moderate)
Trigger: Keep both metrics independent, add correlation tracking
```

Applied to Slackwater:
```
Court IV Experiment: Can 4+ agents converge via puffin calls?

Finding: Convergence time < 30s
Trigger: Proceed to Court V (Relay)

Finding: Convergence time > 2min
Trigger: Puffin call TTL too short or propagation radius too narrow. Fix before Court V.

Finding: No convergence
Trigger: Swarm coordination broken. Stop. Re-architect discovery layer.
```

---

## 3. Concrete Integration Steps

### Step 1: Create Slackwater Experiment Registry
```
Create: /home/eileen/projects/lucineer-system/experiments/
Port: wheel_of_discovery.py (simplify — remove domain-specific stuff)
Seed: One Finding per design claim in INTEGRATED_ARCHITECTURE.md
Seed: One Experiment per Court assertion
```

### Step 2: Port Delta-Detect as FlowStateDetector
```
Extract: delta_detect.py SaturationDetector class
Adapt: Replace "model exhaustion" with "agent flow state"
Integrate: As a Chisel in the Slackwater persistence layer
```

### Step 3: Merge Fleet Ops Handbook into TOOLS.md
```
Read: FLEET-OPS-HANDBOOK.md
Merge: Vocabulary Wall protocol, pre-computation protocol, stage classification
Update: TOOLS.md model routing table
```

### Step 4: Adopt Confidence Tiers for Grain
```
Map grain maturation to experiment confidence:
  Bright Steel (0-50 uses) = SUGGESTIVE
  Developing Patina (50-500) = SOLID
  Worn Smooth (500+) = BEDROCK
```

---

## 4. What NOT to Integrate

| Component | Why Skip |
|-----------|---------|
| E4/E5/E6 raw experiment code | Specific to fleet coupling matrices. Methodology transfers, code doesn't. |
| GL(9) consensus library | Specific mathematical framework for 9×9 coupling. Not applicable to game AI. |
| Cyclotomic integer ring proofs | Beautiful math, no application to Roblox/Lua game building. |
| Consciousness prediction experiments | Interesting but tangential to Slackwater's goals. |
| Cross-lingual analysis | The "wall" finding is noted, but the detailed cross-lingual experiments aren't relevant. |

---

## 5. The Cultural Transfer

The most valuable thing fm-experiments offers Slackwater isn't code — it's **culture**.

1. **Honest negative results:** Document what doesn't work. This constrains the solution space.
2. **Pre-registered triggers:** Before running an experiment, define what each possible result means for the architecture.
3. **Falsification as progress:** Wrong answers narrow the search space. Each falsified hypothesis eliminates a design path.
4. **Reproducible evidence:** Every claim links to a script, its output, and the analysis.

From `NIGHT-SYNTHESIS.md`:
> "The negative results make the thesis STRONGER, not weaker. They constrain exactly WHERE the advantage comes from."

This should be a Slackwater design invariant.

---

*This integration plan references the INTEGRATED_ARCHITECTURE.md and is based on reading actual experiment scripts, result files, and synthesis documents.*
