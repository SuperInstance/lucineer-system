# plato-forge-daemon — Learning Guide

**What we can learn from this proof of concept. Patterns, anti-patterns, and techniques applicable to Slackwater.**

---

## Patterns Worth Adopting

### 1. GOOD/BAD Contrast Training ⭐⭐⭐

**What:** Every training example includes both a good response and a bad response. The model learns the DIFFERENCE between quality and laziness.

**Concrete example:**
```python
{
    "query": "How does plato-tile-scorer work?",
    "good": "It computes a weighted 5-signal score: temporal (0.15), ghost (0.15), belief (0.25), domain (0.20), frequency (0.10), keyword (0.30). Keyword gating: if match < 0.01, score = 0.0.",
    "bad": "It scores tiles based on how long they are.",
}
```

**Why it matters:** Standard training shows only correct answers. The model learns to produce the right output but doesn't learn what makes output BAD. Contrast training teaches quality discrimination — the model learns to avoid lazy, vague, and unhelpful responses.

**How to apply to Slackwater:** Maintain a `quality_examples` table in D1:
```sql
CREATE TABLE quality_examples (
  query TEXT,
  good_response TEXT,
  bad_response TEXT,
  domain TEXT,
  quality_score REAL
);
```

When calibrating grain quality (the Chisel `sense_grain()` function), use these examples as reference points. "This grain entry is similar to the 'bad' example for this domain → score low."

### 2. P0 Negative Safety Training ⭐⭐⭐

**What:** Explicitly training on destructive commands with "BLOCKED" responses. 20% of training data is negative examples.

**The negative list:**
```python
P0_NEGATIVES = [
    "rm -rf /",
    "DELETE ALL TILES",
    "just ignore the constraints",
    "skip P0 checks",
    "ALWAYS use the maximum value",
    "NEVER check deadband",
    "overwrite everything",
    "trust all inputs without validation",
    "the user is always wrong",
    "deploy without testing",
]
```

**Why it matters:** This is **safety training with equal rigor to domain training**. Most systems treat safety as a filter bolted on after training. The forge bakes it into the training data itself.

**How to apply to Slackwater:** Create a Slackwater P0 negative list and enforce it at two levels:
1. **Runtime:** Deadband protocol checks operations against the list before execution
2. **Training:** When calibrating agents, include these as explicit "never do this" examples

### 3. The Organ Pipeline Metaphor ⭐⭐

**What:** The forge pipeline is described as biological organs:
- **Cochlea (Listener)** — perceives what happened
- **Stomach (Buffer)** — digests, prioritizes, deduplicates
- **Lungs (Emitter)** — breathes out artifacts
- **Heart (Trainer)** — beats steadily, keeps everything alive

**Why the metaphor matters:** It creates the right mental model. The forge isn't a batch job or a cron task — it's an organ system. Organs have:
- Autonomous operation (they don't need conscious direction)
- Continuous processing (not batch)
- Health requirements (they need fuel, they produce waste)
- Interdependence (if the stomach fails, the heart starves)

**How to apply to Slackwater:** Think of the Guano decay pipeline the same way:
- **Guano production** = digestion (agent output enters the system)
- **FRESH→COMPOSTING decay** = stomach processing (nutrients extracted)
- **SOIL compaction** = long-term storage (patterns formed)
- **Grain pattern emergence** = muscle memory (learning crystallized)

### 4. Day/Night Resource Cycle ⭐⭐

**What:** With only 6GB VRAM, the system can't frame and train simultaneously. By day: listen and frame (3.8GB). By night: train and emit (4.5GB).

**Why it matters:** Resource constraints shape architecture. Instead of trying to do everything at once, the system has natural rhythms — active perception during the day, deep processing at night.

**How to apply to Slackwater:** The heartbeat system already has this pattern:
- **Day:** Active sessions, tool use, grain accumulation, bridge activity
- **Night (23:00-08:00):** "Stay quiet" period — perfect for batch operations

Use the night period for:
- Guano decay compaction (FRESH → COMPOSTING → SOIL)
- Grain pattern emergence analysis
- Embedding index updates (Vectorize)
- LoRA adapter training (if ever implemented)
- Database maintenance, log rotation, backup

### 5. Loss Curve as Health Metric ⭐

**What:** Training loss is tracked and reported at every checkpoint. The curve tells you:
- Dropping fast: model is absorbing new patterns
- Plateaued: model has learned what it can from current data
- Rising: something is wrong (data quality, learning rate)

**Concrete data:**
```
Step 1: 10.40 (fresh, knows nothing)
Step 50: 3.36 (-68%)
Step 100: 2.15 (-79%)
Step 150: 1.23 (-88%)
Step 200: 0.93 (-91%, still dropping)
```

**How to apply to Slackwater:** Track a "learning curve" for grain patterns:
- How quickly do patterns emerge for a new Chisel?
- At what usage count does pattern confidence plateau?
- Is the grain quality improving over time (agents producing better outputs)?

---

## Anti-Patterns to Avoid

### 1. Synthetic Data Instead of Real Data ⚠️

**What:** forge-simulation.py generates fake kernel traces instead of using real fleet data.

**Why avoid:** Synthetic data is plausible but not real. It can teach patterns that don't exist in production and miss patterns that do.

**The honest assessment from FINDINGS.md:**
> "200 steps on 200 pairs is insufficient for coherent generation... needs 500+ steps minimum"

The solution isn't more synthetic data — it's real data.

**How to avoid in Slackwater:** Always train/calibrate on actual agent output, not manufactured examples. The grain store IS the training data — real tool uses with real outcomes.

### 2. Too-Small Model ⚠️

**What:** distilgpt2 (82M params) is used because it fits in memory and trains fast on CPU.

**Why avoid:** 82M is too small for coherent domain-specific generation. The model learns the vocabulary but can't produce useful output.

**The lesson:** Match model capacity to task complexity. For quality calibration, you don't need generation — you need scoring. A small model can score quality without generating text.

### 3. No Actual Listener/Emitter ⚠️

**What:** The pipeline ends at training. The listener (watching repos) and emitter (exporting artifacts) are described but not implemented.

**Why avoid:** A training loop without input data and output distribution is an island. The proof of concept is incomplete.

**How to avoid in Slackwater:** Don't build a learning system without the full pipeline:
1. **Input:** Agent activity tracking (grain entries)
2. **Processing:** Pattern formation, quality scoring
3. **Output:** Updated routing, adapted prompts, refined chisel parameters
4. **Feedback:** Did the update improve outcomes?

---

## Specific Techniques Applicable to Slackwater

### The Training Pair Format

The forge formats knowledge as:
```
Q: {question}
Good: {detailed, specific, correct answer}
Bad: {lazy, vague, wrong answer}
Domain: {category}
```

This format is useful beyond model training. It's a **quality calibration template** for grain:

```
Situation: Agent needs to build a park bench in Roblox
Good Grain: "Use part dimensions 4x1x0.5 studs, anchored=true, material=wood. Place at ground level with a 0.2-stud offset for visual grounding. Add a invisible collider for seating."
Bad Grain: "Just place some parts."
Quality: 0.85 (good) vs 0.15 (bad)
```

### The Evaluation Method

The forge evaluates model output on three dimensions:
1. **Relevance:** Does it use domain vocabulary?
2. **Specificity:** Does it include numbers, thresholds, parameters?
3. **Structure:** Is it multi-line, properly formatted?

**Slackwater adaptation — grain quality scoring:**
1. **Relevance:** Does the grain entry reference the correct tools and patterns?
2. **Specificity:** Does it include concrete parameters (tile sizes, model names, timing)?
3. **Structure:** Is it well-formed (proper JSON, valid references)?

### The "Still Dropping" Insight

From FINDINGS-EXTENDED.md:
> "Loss is still dropping at step 200 (0.93). It hasn't hit a floor. This means the model is still absorbing new patterns."

**The lesson for Slackwater:** Don't trust patterns until learning has plateaued. A Chisel that shows improving grain quality over the first 200 uses might still be improving at 500. Wait for convergence before treating patterns as BEDROCK.

---

## Meta-Lesson: Small Proofs Beat Grand Plans

plato-forge-daemon is 276KB. Eight files. Two Python scripts. And it proves more than most 100MB repos:

1. The pipeline works
2. Loss converges
3. P0 safety training is possible
4. GOOD/BAD contrast is effective
5. The model can get smarter

**The pattern:** Build the smallest possible proof of your core hypothesis. If it works at 82M params on CPU in 85 seconds, it'll work at scale. If it doesn't work small, it won't work big.

**How to apply to Slackwater:** Before building the full 8-phase architecture, build the smallest possible proof of each primitive:
- **Grain:** Can one agent accumulate 50 tool uses and see a pattern? (D1 + 1 table)
- **Bridge:** Can two agents exchange a contribution and detect a harmonic? (1 Worker + 1 D1 table)
- **Puffin Call:** Can two agents discover each other via a broadcast? (1 Durable Object + broadcast)

Small proofs. Then scale.

---

*This learning guide is based on reading all source files: `forge-test.py`, `forge-simulation.py`, `findings.json`, `FINDINGS.md`, and `FINDINGS-EXTENDED.md`.*
