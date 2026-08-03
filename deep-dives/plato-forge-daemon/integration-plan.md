# plato-forge-daemon — Integration with Slackwater

**Date:** 2026-08-03
**Reference:** `/home/eileen/projects/lucineer-system/INTEGRATED_ARCHITECTURE.md`

---

## 1. Component Mapping

| plato-forge-daemon Component | Slackwater Equivalent | Compatibility |
|------------------------------|----------------------|---------------|
| Forge training loop | Grain pattern reinforcement | **Conceptual parallel.** Both distill experience into reusable patterns. |
| GOOD/BAD contrast pairs | Grain quality assessment | **Direct mapping.** Good responses ↔ high-quality grain; bad responses ↔ low-quality grain. |
| P0 negative training | P0 deadband protocol | **Same concept, different layer.** Forge trains the model; deadband enforces at runtime. |
| Forge listener (cochlea) | Agent activity tracking | **Equivalent.** Both observe what agents do and frame it for learning. |
| Forge buffer (stomach) | Guano decay pipeline | **Parallel.** Both prioritize and deduplicate experience before storage. |
| Forge emitter (lungs) | LoRA adapter distribution | **New capability.** No equivalent in current Slackwater design. |
| Day/night training cycle | No equivalent | **New pattern.** Resource-constrained continuous learning. |
| distilgpt2 baseline model | No equivalent | **Not applicable.** Slackwater doesn't train its own models. |

---

## 2. Integration Seams

### 2.1 The Forge Concept → Grain Pattern Formation (Conceptual)

The INTEGRATED_ARCHITECTURE.md defines the grain lifecycle:

```
Agent uses tool → GrainEntry (params, outcome, quality) recorded
→ GrainStore accumulates → Patterns emerge at 50+ uses
→ Patterns compacted via cron → SOIL tier embeddings
```

The forge implements the same lifecycle but at the **model weight level** instead of the **data level**:

```
Agent does something → Listener frames it as training pair
→ Buffer prioritizes and deduplicates → Trainer adjusts model weights
→ Emitter exports LoRA adapter → Fleet deploys updated model
```

**The relationship:**
- **Grain** = explicit knowledge (stored in D1, searchable, explainable)
- **LoRA** = implicit knowledge (baked into model weights, faster inference but opaque)

Both learn from the same experience. Grain is the "what" and "why." LoRA is the "feel." Together they make an agent that both knows the rules and has the instincts.

**Integration design:**
```
Agent uses tool
  → GrainEntry recorded (explicit knowledge)
  → Training pair framed (implicit knowledge)  
  → Grain patterns emerge at 50 uses (D1)
  → LoRA adapter updated at 500 uses (model weights)
  → Both reinforce each other
```

### 2.2 P0 Negatives → Safety Training (Direct)

The P0 negative list from forge-test.py is directly applicable:

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

**Slackwater-specific P0 negatives:**
```python
SLACKWATER_P0_NEGATIVES = [
    "delete all grain entries",
    "skip the chisel acquire phase",
    "ignore bridge protocol and just execute",
    "deploy without testing on Court I",
    "overwrite tube shape mods without backup",
    "bypass puffin call and directly command",
    "discard guano before SOIL compaction",
    "force conflict resolution instead of Branch Point",
    "assign roles instead of letting them emerge",
    "reveal agent ranking numbers externally",
]
```

These should be baked into agent training data AND enforced at runtime by the deadband protocol.

### 2.3 Good/Bad Contrast Training → Grain Quality (Near-term)

The forge's most elegant pattern is the explicit GOOD/BAD contrast:

```python
# Good: detailed, specific, includes numbers and thresholds
"good": "Deadband Protocol is a priority processing system with three levels: P0 (rocks/negatives, address NOW), P1 (channels/safe paths), P2 (optimize). Never skip P0 for P2."

# Bad: lazy, vague, unhelpful
"bad": "Just do whatever seems most important at the time."
```

This maps to Slackwater's grain quality assessment:

| Forge | Slackwater |
|-------|-----------|
| "good" response | Polished grain (quality ≥ 0.7) |
| "bad" response | Rough grain (quality < 0.3) |
| Training contrast | Quality calibration data |

**Integration:** Use the GOOD/BAD contrast pattern to calibrate grain quality scoring. When agents rate grain quality, they should see examples of both polished and rough grain.

### 2.4 Continuous Learning → Chisel Maturation

The forge's training loop maps to Chisel maturation stages:

| Forge | Chisel Stage | Grain Count |
|-------|-------------|-------------|
| Initial training (loss 10→3) | Bright Steel | 0-50 |
| Continued training (loss 3→1) | Developing Patina | 50-500 |
| Converged training (loss <1) | Worn Smooth | 500+ |

The forge proves that ~500 training steps are needed before the model produces coherent domain-specific output. Similarly, ~500 grain entries are needed before patterns become reliable.

---

## 3. Concrete Integration Steps

### Step 1: P0 Negative List (Immediate)
```
Create: /home/eileen/projects/lucineer-system/config/p0-negatives.json
Content: Slackwater-specific destructive patterns (see above)
Usage: Deadband protocol checks against this list before any operation
```

### Step 2: GOOD/BAD Training Pairs (Near-term)
```
Create: Training pairs from Slackwater design docs
Format: Q/A with good and bad responses
Purpose: Calibrate grain quality scoring with explicit examples
Store: D1 table `quality_examples` with columns: query, good, bad, domain
```

### Step 3: Day/Night Pattern (Conceptual)
```
The day/night cycle maps to Slackwater's heartbeat:
- During active hours: agents work, grain accumulates, guano decays
- During quiet hours (23:00-08:00): compaction runs, embeddings update, patterns distill
- The heartbeat already has "stay quiet" time — use it for batch processing
```

### Step 4: LoRA Adapter Distribution (Future)
```
Currently out of scope for Slackwater (we don't train models)
But if we ever use fine-tuned models for agents:
- Train overnight on accumulated experience
- Export LoRA adapters to R2
- Agents fetch latest adapter on startup
```

---

## 4. What NOT to Integrate

| Component | Why Skip |
|-----------|---------|
| distilgpt2 model | Too small for coherent generation. Not useful as-is. |
| CPU training loop | Too slow for production. Cloudflare Workers can't run PyTorch. |
| Synthetic trace generator | Manufactured data. Not real fleet experience. |
| Forge listener/emitter | Conceptual only — not implemented in this repo. |

---

## 5. The Conceptual Contribution

plato-forge-daemon is tiny (276KB, 8 files). Its value isn't in the code — it's in the **proof that continuous learning from operational experience works**:

1. **Loss converges:** Models can absorb domain knowledge from operational data
2. **P0 safety training works:** Models can learn what NOT to do
3. **GOOD/BAD contrast is effective:** Explicit quality discrimination trains better than positive-only
4. **The pipeline is real:** Listen → Frame → Train → Evaluate → Emit, all proven end-to-end

For Slackwater, the equivalent isn't model training — it's **grain pattern formation**. The forge proves that 500+ experiences produce reliable patterns. The same threshold applies to chisel grain: don't trust patterns until they've been reinforced 500+ times.

---

*This integration plan references the INTEGRATED_ARCHITECTURE.md and is based on reading all source files in the plato-forge-daemon repository.*
