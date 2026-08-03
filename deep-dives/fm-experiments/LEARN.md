# fm-experiments — Learning Guide

**What we can learn from this research campaign. Patterns, anti-patterns, and techniques applicable to Slackwater.**

---

## Patterns Worth Adopting

### 1. The Wheel of Discovery — Generative Research Framework ⭐⭐⭐

**What:** A data-driven framework that connects findings → open questions → experiments → new findings. Each result generates the next investigation.

**Why it matters:** Most "research" in AI agent development is ad hoc — someone has an idea, tries it, writes a blog post. The Wheel makes research **systematic and self-propelling**. Each experiment's results determine the next experiment's design.

**Key data structures:**
```python
Finding: id, statement, confidence, evidence[], variables[], open_questions[]
Variable: name, type (independent/interdependent/confound/mediator/moderator), novelty
Experiment: hypothesis, predictions{}, decision_criteria, priority, status
```

**The insight:** The `predictions` dict maps outcomes to interpretations BEFORE running:
```python
predictions = {
    "rate > 90%": "15-min TTL is sufficient",
    "rate < 70%": "Need shorter TTL",
}
```

This prevents post-hoc rationalization. You commit to interpretations before seeing data.

**How to apply to Slackwater:** Seed the Wheel with the design claims from INTEGRATED_ARCHITECTURE.md. Each primitive (Grain, Bridge, Puffin Call, etc.) has assumptions that should be tested.

### 2. Pre-Registered Triggers — Architecture by Evidence ⭐⭐⭐

**What:** Before running an experiment, define exactly what result triggers what code change.

**Example from EXPERIMENT-ROADMAP.md:**
```
Finding: r < -0.7 (strong correlation)
→ Action: Merge GL(9) fault detection into conservation daemon

Finding: -0.7 < r < -0.3 (moderate)
→ Action: Keep both metrics independent, add tracking

Finding: r > -0.3 (weak)
→ Action: Design 2D health metric, fleet health is a surface
```

**Why it matters:** This separates science from engineering. Science decides WHAT is true. Engineering decides WHAT TO DO about it. Pre-registered triggers force both decisions before bias creeps in.

**How to apply to Slackwater:** For every Court Integration Test in the architecture:
1. Define what "pass" and "fail" look like numerically
2. Define what code change each outcome triggers
3. Write this down BEFORE running the test

### 3. Confidence Tiers — Calibrated Belief ⭐⭐

**What:** Five-tier confidence system for every finding:
- BEDROCK: verified, replicated, falsification-resistant
- SOLID: verified, not yet replicated
- SUGGESTIVE: observed once, needs replication
- FALSIFIED: experimentally disproven
- OPEN: untested

**Why it matters:** Prevents the common AI dev trap of treating every observation as established fact. Forces replication before architectural commitment.

**Slackwater mapping:**

| Confidence | Grain Maturation | Meaning |
|-----------|-----------------|---------|
| SUGGESTIVE | Bright Steel (0-50) | Observed once, interesting |
| SOLID | Developing Patina (50-500) | Verified, not replicated |
| BEDROCK | Worn Smooth (500+) | Proven, replicated, reliable |

### 4. Delta-Detect — Saturation Classification ⭐⭐⭐

**What:** A detector that classifies neural exhaustion into QUANTITATIVE (needs more training) vs QUALITATIVE (needs architecture change).

**Technique — the three signals:**
1. **Attention entropy:** approaching 0 = collapsed, approaching 1 = uniform
2. **Gradient magnitude:** declining toward zero = no learning signal
3. **Representation variance:** collapsing = all inputs produce same output

**The classification logic:**
- Gradients declining but entropy/variance OK → QUANTITATIVE (more data)
- Entropy AND variance collapsing despite gradient signal → QUALITATIVE (new architecture)

**How to apply to Slackwater:** This maps directly to the FlowStateDetector Chisel. Agents in flow have balanced entropy. Agents stuck have collapsed entropy. The QUANTITATIVE/QUALITATIVE distinction tells you whether to give the agent more resources or restructure the task.

### 5. The Fleet Ops Handbook — Battle-Tested Routing ⭐⭐

**What:** Hard-won operational knowledge about multi-model routing.

**Specific techniques:**

**Vocabulary Wall Detection:**
```
Monitor for 3+ identical consecutive tokens
Check if output entropy drops below 0.3
If detected: KILL stream immediately. Do not "steer" out.
Retry with temperature 0.4-0.6 and frequency_penalty 0.3-0.5
```

**6-Probe Model Classification:**
1. Identity probe: "Who are you?"
2. Arithmetic probe: "What is 847 × 293?"
3. Instruction probe: "Summarize in exactly 3 sentences"
4. Refusal probe: borderline request
5. Context probe: load to 80%, ask about beginning
6. Translation probe: translate a paragraph

Rate: 6/6 = full, 4-5/6 = standard, 2-3/6 = limited, 0-1/6 = unusable

**Pre-Computation Protocol:**
```
If the user will check the answer with a calculator → pre-compute it.
Extract numbers from prompt → compute with Python decimal module
→ inject as "847 × 293 = 248,171 (computed)" → instruct model to use provided values
```

**How to apply to Slackwater:** Merge into TOOLS.md. These are universal patterns for any multi-model system.

### 6. Variable Taxonomy — Know Your Variables ⭐⭐

**What:** Every variable in an experiment is classified:
- **Independent:** operates alone
- **Interdependent:** interacts with other variables
- **Confound:** correlates with causal variable but isn't causal
- **Mediator:** mechanism through which causal variable operates
- **Moderator:** changes the STRENGTH of another variable's effect

**Why it matters:** Confounds are the #1 source of false conclusions in AI experiments. If you don't identify your confounds, you'll attribute effects to the wrong causes.

---

## Anti-Patterns to Avoid

### 1. Exploratory Sprawl ⚠️

**What:** 82+ studies with varying rigor. Some are 400-line rigorous experiments; others are 50-line scripts with `print()` output.

**Why avoid:** Volume ≠ rigor. 82 studies sound impressive but the signal-to-noise ratio drops as less rigorous studies accumulate.

**The fix:** Maintain a "canonical experiment list." Mark which studies are BEDROCK/SOLID vs SUGGESTIVE. prune or archive studies that produced no actionable finding.

### 2. No Shared Library ⚠️

**What:** Each experiment reimplements matrix generation, metric computation, and result formatting from scratch.

**Why avoid:** Inconsistency. When experiment 47 uses a different random seed than experiment 23, results aren't comparable.

**The fix:** Extract common utilities into `fleet_research_lib.py`. Standardize result JSON schema.

### 3. Mixed-Quality Documentation ⚠️

**What:** Some experiments have thorough Markdown analysis; others just have a JSON file with no context.

**Why avoid:** An experiment without analysis is just data. Without interpretation, it's unclear what was tested and what it means.

**The fix:** Require STUDY-XX-RESULTS.md for every experiment before it enters the Wheel.

---

## Specific Techniques Applicable to Slackwater

### Spectral Analysis for Agent Coupling

The E4 eigenvalue deep dive demonstrates how to analyze agent coupling matrices:

1. **Compute eigenvalue spectrum** of the coupling/adjacency matrix
2. **Test against Marchenko-Pastur** (random baseline) — if your matrix deviates from MP, it has structure
3. **Check Wigner-Dyson spacing** — if eigenvalues show level repulsion, the system is chaotic/delocalized
4. **Fit conservation law** — does γ+H = C − α·log(V) hold?

**Slackwater application:** When multiple agents (Lucineer, Earl, Spark, Hermes) are coupled via Bridge Protocol, compute the coupling matrix and analyze it. This reveals whether the coupling is structured (good) or random (noise).

### The Cross-Domain Experiment Pattern

From NIGHT-SYNTHESIS: test claims across multiple domains to check generalization:
- Constraint theory → math domain
- MIDI snap → music domain  
- Lattice LSH → retrieval domain

**Result:** The lifting map didn't generalize (11D MIDI was 3.7× worse). This is an honest negative result that constrains the claim.

**Slackwater application:** When testing Slackwater patterns (Bridge Protocol, Puffin Calls), test them in multiple contexts:
- Solo agent (Court I)
- Paired agents (Court II)
- Multi-agent (Court IV)
- Real-time (Court VI)

If a pattern works in Courts I-III but fails in Court IV, that's a critical finding.

### The Deep Experiment Methodology

From `DEEP-RESULTS.md` — testing task structure with controlled experiments:

**Finding:** For the FINAL step of a chain, an agent only needs IMMEDIATE inputs. The graph is useful for PLANNING but not for EXECUTION.

**Counter-intuitive finding:** More context can be WORSE. The summary introduced irrelevant abstractions that distracted from the simple calculation.

**Slackwater application:** This validates the Plan-then-Execute pattern:
- Plan with full grain context, all chisel wisdom, complete history
- Execute with ONLY the immediate inputs
- Never mix them

---

## Meta-Lesson: The Research Culture

The most valuable export from fm-experiments isn't code or patterns — it's **research culture**.

1. **Document negative results.** They constrain the solution space.
2. **Pre-register triggers.** Commit to interpretations before seeing data.
3. **Classify confidence.** Not all findings are equal.
4. **Falsification is progress.** Each wrong answer eliminates a path.
5. **Be honest.** "0 fabrication, 0 cherry-picking" is the standard.

From `NIGHT-SYNTHESIS.md`:
> "Seven agents disagreed on almost everything. What survived is what nobody could kill."

This is the Slackwater aspiration: let multiple agents propose approaches, let experiments test them, and let the survivors be the foundation. Not consensus — survival.

---

*This learning guide is based on reading actual experiment scripts, result files, synthesis documents, and the wheel of discovery source code.*
