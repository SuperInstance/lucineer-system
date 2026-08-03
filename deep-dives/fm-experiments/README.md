# fm-experiments

> The research campaign archive of the Cocapn fleet — 82+ studies investigating how AI agents coordinate, communicate, and compose their capabilities.

---

## What Is This?

fm-experiments is a laboratory notebook, not an application. It contains:

- **82+ numbered studies** testing fleet coordination hypotheses
- **4 named campaigns** (A-D) covering retrieval, voting, encoding, synthesis
- **6 deep-dive series** (E1-E6) on eigenvalues, random matrix theory, information theory
- **The Wheel of Discovery** — a generative framework connecting findings → questions → experiments
- **Delta-Detect** — a neural network saturation detector
- **The Grand Synthesis** — three experiments forming a unified understanding verification engine

Every experiment follows: hypothesis → design → code → run → document → integrate.

---

## Quick Start

### Read the Key Documents

```bash
# Start with the roadmap (what was planned)
cat EXPERIMENT-ROADMAP.md

# Then the synthesis (what was found)
cat NIGHT-SYNTHESIS.md

# Then deep results (the data)
cat DEEP-RESULTS.md
cat E4-EIGENVALUE-DEEP-DIVE.md
```

### Run the Wheel of Discovery

```bash
python3 wheel_of_discovery.py
# Displays: findings, variables, experiments, open questions
# Shows the generative cycle: each finding spawns questions and experiments
```

### Run the Saturation Detector

```bash
cd delta-detect/
python3 test_delta_detect.py
# Tests: attention entropy, gradient magnitude, representation variance
# Classifies: QUANTITATIVE vs QUALITATIVE exhaustion
```

---

## Key Concepts

### The Scientific Method (Applied to AI)

Every experiment uses:
1. **Pre-registered hypothesis** — state what you're testing BEFORE running
2. **Pre-registered triggers** — define what each result means for the architecture
3. **Controlled variables** — independent, interdependent, confound, mediator, moderator
4. **Confidence tiers** — BEDROCK (verified+replicated) → SOLID → SUGGESTIVE → FALSIFIED

### The Wheel of Discovery

```
Findings → Open Questions → Designed Experiments → Results
    ↑                                                        |
    └────────────────────────────────────────────────────────┘
    
Each spoke generates the next. Falsification is the engine.
```

### Conservation Law

The fleet's coupling matrices obey: `γ+H = C − α·log(V)`

Where γ is spectral gap, H is Shannon entropy, V is fleet size. This holds with R²=0.90 for Hebbian architectures.

### Delta-Detect: When to Elevate

```
QUANTITATIVE exhaustion: gradients declining, entropy OK
  → Model needs more data/time (same architecture level)

QUALITATIVE exhaustion: entropy AND variance collapsing
  → Model needs architecture change (level elevation required)
```

### The Grand Synthesis

Three experiments form a unified understanding verification engine:
- **delta-detect** → WHEN to elevate (saturation detection)
- **sheaf-h1** → WHETHER models compose (obstruction detection)  
- **holonomy-phase** → WHAT drift accumulates (geometric phase measurement)

---

## Directory Structure

```
fm-experiments/
├── wheel_of_discovery.py    # The generative framework (691 lines)
├── EXPERIMENT-ROADMAP.md    # Studies 54-63 with pre-registered triggers
├── ARCHITECTURE-EVOLUTION.md # Current service topology + gaps
├── FLEET-OPS-HANDBOOK.md    # Model routing, gotchas, protocols
├── FLEET-ARCHITECTURE-FIT.md # How FM + Oracle1 systems interlock
├── NIGHT-SYNTHESIS.md        # 8 experiments, honest results
├── DEEP-RESULTS.md           # Task structure + context experiments
├── E4-EIGENVALUE-DEEP-DIVE.md # Full spectral analysis
├── delta-detect/             # Saturation detector
│   ├── delta_detect.py       # Core detector (400+ lines)
│   ├── elevation_operators.py
│   └── test_delta_detect.py
├── distributed-consensus/    # 3 consensus experiments
├── studyXX_*.py              # Individual experiment scripts
├── studyXX_results.json      # Raw result data
├── STUDY-XX-RESULTS.md       # Analysis documents
├── CAMPAIGN-{A,B,C,D}-RESULTS.md # Campaign syntheses
└── E{1-6}-*.md              # Deep experiment reports
```

---

## Common Workflows

### Read an Experiment

Each experiment has three files:
1. **`studyXX_name.py`** — The experiment script
2. **`studyXX_results.json`** — Raw numerical results
3. **`STUDY-XX-RESULTS.md`** — Human-readable analysis

### Understand the Fleet Routing

```bash
cat FLEET-OPS-HANDBOOK.md
```

Key sections:
- Routing table (which model for which task)
- Vocabulary Wall (degenerate output detection)
- Stage classification (6-probe method for new models)
- Pre-computation protocol (don't trust model math)

### Trace the Research Arc

```bash
# Phase 1: Initial campaigns
cat CAMPAIGN-A-RESULTS.md  # Abstractive synthesis
cat CAMPAIGN-B-RESULTS.md  # Retrieval quality

# Phase 2: Deep experiments  
cat E1-LIVE-CONSERVATION.md
cat E4-EIGENVALUE-DEEP-DIVE.md

# Phase 3: Synthesis
cat NIGHT-SYNTHESIS.md     # Honest assessment
cat DEEP-RESULTS.md        # Meta-analysis
```

---

## The Honest Scorecard

**What was proven:**
- Conservation law holds for structured coupling (R²=0.90)
- Phase transitions are binary and universal
- Cyclotomic rings are Pareto-optimal (zero-side-info)
- 84% cost reduction via critical angle routing
- Saturation detection works

**What was falsified:**
- 11D MIDI snap improves on uniform (3.7× WORSE)
- Memoir compression is O(log T) (actually O(√T))
- Cyclotomic converges to optimal (21% structural gap)

**What remains open:**
- Can the 21% gap to optimality be closed?
- Does the conservation law generalize beyond 9×9 matrices?
- Can cross-domain lifting maps be rescued?

---

*This is research code. Expect varying quality, scattered documentation, and one-off scripts. The methodology and findings are more valuable than the implementations.*
