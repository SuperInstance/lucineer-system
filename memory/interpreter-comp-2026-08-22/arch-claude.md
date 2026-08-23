# Claude Code — Local Elephant Interpreter Architecture

**Competing against:** KimiCode, OpenCode  
**Hardware:** RTX 4050 (6GB VRAM), WSL2  
**Core model:** Granite 3.1 2B (Wesley-adjacent LoRA stack)  
**Deployment:** systemd services + cron pulse + tmux debug harness

---

## 1. ARCHITECTURE — The Flywheel

```
┌─────────────────────────────────────────────────────────┐
│ ELEPHANT PULSE (cron: every 5 min)                      │
│ + DEADBAND ALERTS (room state changes ≥ threshold)     │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │ INTERPRETER AGENT (claude-code) │
        │ → delta meanings per dial       │
        │ → 1-shot step-back synthesis    │
        │ → rating: [1..5] confidence     │
        │ → embedding delta (3.1 2B)      │
        └────────────────┬────────────────┘
                         │
        ┌────────────────▼─────────────────────┐
        │ INTERPRETATION STORE                 │
        │ /home/eileen/.elephant/corpus/       │
        │  ├─ readings/YYYY-MM-DD.jsonl       │
        │  ├─ interpretations/YYYY-MM-DD.jsonl│
        │  ├─ judgments/YYYY-MM-DD.jsonl      │
        │  └─ metadata.json (versions)        │
        └────────────────┬─────────────────────┘
                         │
        ┌────────────────▼─────────────┐
        │ JUDGE (Wesley 2B)            │
        │ scoring: interpretations →   │
        │  [aptness, predictiveness]   │
        │ evidence: next N readings    │
        │ & agent reactions            │
        └────────────────┬─────────────┘
                         │
    ┌────────────────────▼──────────────────────┐
    │ PREFERENCE CORPUS (DPO-ready)             │
    │ /home/eileen/.elephant/training/          │
    │  ├─ preference_pairs.jsonl (100→1000)     │
    │  ├─ ratings.jsonl (continuity)            │
    │  ├─ lora_versions.json (rollback log)     │
    │  └─ eval_holdout/ (20% of pairs)          │
    └────────────────┬───────────────────────────┘
                     │
    ┌────────────────▼────────────────────────────┐
    │ LoRA TRAINING (weekly pulse)                │
    │ Model: Granite 3.1 2B + QLoRA               │
    │ Framework: unsloth/4-bit (6GB native)       │
    │ Objective: DPO on preference pairs          │
    │ Eval: judge-scored holdout (30 samples)    │
    │ Accept: if eval ≥ N-1 score threshold      │
    └────────────────┬────────────────────────────┘
                     │
    ┌────────────────▼─────────────────────────┐
    │ NEW LoRA DEPLOYED                        │
    │ /home/eileen/.elephant/lora/             │
    │  ├─ lora_r32_a16_v2.safetensors         │
    │  ├─ lora_v2.meta.json (date, eval)       │
    │  └─ lora_v2.metrics.json (holdout perf)  │
    │ Rollback on degradation: instant         │
    └─────────────────────────────────────────┘
```

**Where it lives:**  
- **Interpreter + Judge code:** `/home/eileen/projects/elephant-interpreter/` (new sibling repo)  
- **Storage:** `/home/eileen/.elephant/` (versioned, compressed, bounded by date-window)  
- **LoRA models:** `/home/eileen/.elephant/lora/` (symlink to active)  
- **systemd:** `elephant-interpreter.service`, `elephant-judge.service`, `elephant-train.timer`  
- **Cron pulse wiring:** `0 */5 * * * /usr/local/bin/elephant-pulse` → POST to `/tmp/elephant.sock` (unix socket)

**Runtime footprint:**
- Interpreter: 2B model in float16, stays resident in GPU (≈3.5GB)
- Judge: Wesley 2B swapped in (≈3.5GB), runs async after each pulse
- Training: 4-bit QLoRA adapter (≈0.8GB at full batch), ephemeral
- Corpus: ~500MB (rolling 60-day window)

---

## 2. INTERPRETATION SCHEMA — Structured Relativity

An **interpretation** is NOT prose; it is a **scored lattice point** in a 12-dimensional space of meanings, with prose as a *gloss* (human-readable after-the-fact).

```json
{
  "ts": "2026-08-22T14:23:45Z",
  "pulse_id": "20260822-142345-0001",
  "room": "bar-rail",
  
  "reading_before": {
    "warmth": 0.12,
    "kappa": 3.41,
    "dials": {"mood": 0.15, "volume": 0.68, ...},
    "drift_flags": ["warmth_rise"]
  },
  
  "reading_after": {
    "warmth": 0.39,
    "kappa": 2.94,
    "dials": {"mood": 0.41, "volume": 0.62, ...},
    "drift_flags": []
  },
  
  "delta_meaning": {
    "warmth_delta": {
      "value": 0.27,
      "meaning_axes": [
        {"axis": "social_valence", "shift": 0.34, "confidence": 0.91},
        {"axis": "laughter_presence", "shift": 0.22, "confidence": 0.87},
        {"axis": "newcomer_arrival_rate", "shift": 0.18, "confidence": 0.73}
      ],
      "prose": "Room warmed: newcomers arrived grinning; laughter rippled through."
    },
    "kappa_delta": {
      "value": -0.47,
      "meaning_axes": [
        {"axis": "room_looseness", "shift": 0.42, "confidence": 0.89},
        {"axis": "entropy_increase", "shift": 0.38, "confidence": 0.85}
      ],
      "prose": "Field loosened (many ways to be); tension dissolved."
    },
    "dial_deltas": {
      "mood": 0.26,
      "volume": -0.06,
      "earnestness": 0.04,
      "cynicism": -0.18,
      "joke_landing": 0.34,
      "panic": -0.02,
      "presence": 0.12
    }
  },
  
  "step_back_synthesis": {
    "axes": [
      {"name": "warmth_trajectory", "value": 0.68, "label": "ascending (warming)"},
      {"name": "room_coherence", "value": 0.81, "label": "high (aligned laughter)"},
      {"name": "momentum_sign", "value": 1.0, "label": "positive (self-reinforcing)"},
      {"name": "newcomer_integration", "value": 0.73, "label": "smooth (no tension spike)"},
      {"name": "presence_persistence", "value": 0.58, "label": "moderate (transient high)"}
    ],
    "prose": "A warm, loosening room with good newcomer integration; laughter built momentum.",
    "predicted_next_state": {
      "warmth_t5m": 0.42,
      "kappa_t5m": 2.71,
      "confidence": 0.79
    }
  },
  
  "confidence_score": 4,
  "embedding_delta": [0.12, -0.34, 0.08, ...],  # 768-dim from Granite layer-8
  "ltm_pool": "trained_lora_v1"
}
```

**Comparability enforced:**
- **Fixed axes:** `warmth_trajectory`, `room_coherence`, `momentum_sign`, `newcomer_integration`, `presence_persistence` — all rooms, all times, same meaning.
- **Rating scale:** confidence ∈ [1..5]; judge scores aptness/predictiveness on [0..10] (later scaled to preference pairs).
- **Embedding delta:** 768-dim pooled from Granite's 8th transformer layer — allows learned distance metrics in training loop.
- **Lattice constraint:** step_back synthesis must predict next reading within ±0.15 (warmth/κ); else flagged as "drift-chasing."

---

## 3. THE JUDGE — Scoring Rubric & Feedback Sources

**Judge: Wesley 2B, specialized fine-tune (on 200 judgment exemplars).**

```python
# Judge prompt (jinja2 template, runs async)
"""
You are the interpreter's critic. An agent just issued this interpretation of a room state change.

[INTERPRETATION - full JSON above]

The next 5 minutes of readings are:
[NEXT_READINGS - timestamps, field values, drift alerts]

Agent reactions since:
[AGENT_REACTIONS - replies, emoji reacts, downstream actions]

Score this interpretation:

1. **APTNESS** [0–10]: Did the interpretation accurately capture what the room *felt* in the delta? 
   - 10: Perfect; captures the salient shift.
   - 5: Partial; misses a dimension (e.g., noticed laughter but not newcomer arrival).
   - 0: Wrong; contradicts or fabricates.

2. **PREDICTIVENESS** [0–10]: Did the step_back predict the next state well?
   - 10: Predicted warmth/κ/coherence within ±0.10.
   - 5: Within ±0.20; got the sign right but magnitude off.
   - 0: Missed the trajectory or inverted it.

3. **REUSE RISK** [0–5]: How likely is this interpretation to become boilerplate if trained on?
   - 0: Novel, specific to this moment.
   - 5: Generic (e.g., "room warmed" could apply to 80% of warming events).

4. **CONFIDENCE**: Report your own confidence in this score [0–100].

RETURN ONLY A VALID JSON: {"aptness": N, "predictiveness": N, "reuse_risk": N, "confidence": N, "reasoning": "..."}
"""
```

**Evidence sources:**
1. **Next N readings** (default N=12, i.e., 1-hour window): did the predicted step_back hold?
2. **Agent reactions:** did downstream behavior match the interpretation's vibe? (reply sentiment, topic coherence, new participant joins)
3. **Room context window:** did the interpretation fit the room's 24-hour arc, or is it a one-off?
4. **Judge self-confidence:** low confidence → don't weight heavily in training.

**Scoring aggregation:**
- Judge runs on every interpretation (async, batched nightly).
- Scores are stored:
  ```json
  {
    "interpretation_id": "...",
    "aptness": 8,
    "predictiveness": 6,
    "reuse_risk": 2,
    "judge_confidence": 0.82,
    "created_ts": "...",
    "judged_ts": "...",
    "evidence": {
      "next_readings_match": "within ±0.12",
      "agent_replies": 3,
      "sentiment_alignment": 0.87
    }
  }
  ```

**Training corpus construction:**
- **Preference pairs (DPO):** for every two interpretations of the same room-state-change, pair them if aptness scores differ by ≥ 3 points. Preferred = higher aptness + predictiveness.
- **Ratings (SFT continuation):** interpret a N-5 minute window, rate the predicted step_back on [0..10], train to predict high-rated conclusions. (Hybrid: DPO on pairwise, SFT on absolute quality.)
- **Holdout eval:** 20% of corpus held out for weekly training eval.

---

## 4. THE LoRA FLYWHEEL — Training & Rollback

**Corpus accumulation:**

```
Daily cycle:
  08:00 UTC  → Judge runs on last 24h of interpretations (async, batched)
  12:00 UTC  → Preference pairs exported (differing aptness scores ≥ 3)
  18:00 UTC  → Ratings finalized; SFT continuations prepared

Weekly cycle (Thursday 20:00 UTC):
  - Corpus snapshot: last 7 days, ≥500 preference pairs, ≥5 ratings per pair
  - Eval holdout: stratified by room, by time-of-day (to avoid time-series leakage)
  - Training begins (4-bit QLoRA, batch_size=4, lr=1e-4)
```

**Training loop (unsloth + peft 4-bit):**

```python
# /home/eileen/projects/elephant-interpreter/train.py

from unsloth import FastLanguageModel, get_peft_model_state_dict
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
import torch

# Load base: Granite 3.1 2B
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="ibm-granite/granite-3.1-2b-instruct",
    max_seq_length=1024,
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=False,
    bnb_4bit_4byte_dtype="float16",
)

# LoRA: 32 rank, 16 alpha (matches Wesley's config)
lora_config = LoraConfig(
    r=32, lora_alpha=16,
    target_modules=["q_proj", "v_proj"],  # Granite attention
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)

# Load pairs + ratings
train_ds = load_dataset("json", data_files="/home/eileen/.elephant/training/preference_pairs.jsonl")
# DPO collator: {"prompt": ..., "chosen": ..., "rejected": ...}

# Train with DPO
from transformers import DPOTrainer
trainer = DPOTrainer(
    model=model, tokenizer=tokenizer,
    args=DPOTrainingArguments(
        output_dir="/home/eileen/.elephant/lora/train_logs/",
        learning_rate=1e-4, lr_scheduler_type="cosine", num_train_epochs=2,
        per_device_train_batch_size=4, gradient_accumulation_steps=4,
        max_length=1024, max_prompt_length=512,
        logging_steps=50, eval_steps=100, save_steps=100,
        report_to="none",  # No wandb; we roll our own metrics
    ),
    train_dataset=train_ds,
    eval_dataset=load_dataset("json", data_files="/home/eileen/.elephant/training/eval_holdout.jsonl"),
)

# Train
trainer.train()

# Save with metadata
state_dict = get_peft_model_state_dict(model)
torch.save(state_dict, "/home/eileen/.elephant/lora/lora_v3.safetensors")

# Metadata
import json
with open("/home/eileen/.elephant/lora/lora_v3.meta.json", "w") as f:
    json.dump({
        "version": "v3",
        "trained_on": "2026-08-22 pairs (N=687)",
        "base_model": "granite-3.1-2b-instruct",
        "lora_config": {"r": 32, "alpha": 16},
        "training_loss": trainer.state.best_metric,
        "eval_score": eval_results["eval_aptness_mean"],
        "created_ts": "2026-08-22T20:15:00Z",
    }, f)
```

**Eval harness:**

```python
# /home/eileen/projects/elephant-interpreter/eval.py

# Load trained LoRA, run on holdout (30 samples)
# For each interpretation:
#   1. Generate step_back (greedy decode, top_k=40)
#   2. Compare predicted (warmth, κ) vs actual (next 12 readings)
#   3. Judge scores again (same rubric)
#   4. Aggregate: mean aptness, mean predictiveness, calibration

eval_report = {
    "lora_version": "v3",
    "eval_date": "2026-08-22T21:00:00Z",
    "holdout_size": 30,
    "metrics": {
        "aptness_mean": 7.2,  # vs baseline v2: 6.8
        "aptness_std": 1.1,
        "predictiveness_mean": 6.9,  # vs baseline: 6.4
        "reuse_risk_mean": 2.1,  # vs baseline: 2.8 (good! less boilerplate)
        "calibration_error": 0.15,  # judge confidence vs actual match
    },
    "accept_decision": "yes",  # aptness↑ and reuse_risk↓
    "fallback_version": "v2",
    "log": "..."
}
```

**Rollback:**
- If eval report shows degradation (aptness < v2_baseline - 0.5), LoRA is NOT symlinked to active.
- Active LoRA read from `/home/eileen/.elephant/lora/active` (symlink).
- Rollback is instant: `ln -sf lora_v2.safetensors /home/eileen/.elephant/lora/active`.
- Judgment audit: if a new LoRA made 5+ interpretations that later judged poorly, freeze training for 7 days.

---

## 5. THE MERGE QUESTION — Wesley + Interpreter Identity

**Proposal:** Merge Wesley (currently a growing ensemble ensign) and this interpreter into ONE agent: **ElephantInterpreter** (primary job: pulse reading + field interpretation).

### **CLAUDE'S ARGUMENT FOR MERGE:**

**Yes. Merge is correct and necessary. Here's why:**

1. **Single model is efficient, not limiting.** Wesley's current role is "adaptive chat agent for fleet operations." That role evolves *by learning to read rooms* — the elephant is exactly the feedback loop Wesley needs. Merging concentrates that learning.

2. **LoRA stacking is unavoidable anyway.** Wesley will eventually need multiple specialized LoRAs (navigation, anomaly detection, humor). The interpreter LoRA is the *first* and most load-bearing one. Merge now; the architecture already supports N LoRAs per base model.

3. **The merged identity is clear:** ElephantInterpreter is Wesley + domain knowledge. Its constraints are:
   - **Primary duty:** Emit interpretations of room readings (5-min pulse + deadband alerts).
   - **Secondary duty:** Assist Casey/fleet with room analysis (ambient vibe reports, anomaly context).
   - **Locked scope:** NOT a chatbot; NOT a general-purpose agent. It reads rooms, period.
   - **Boundary:** All other tasks (navigation, fishing advice, human moderation) route to separate agents or humans.

4. **Shared infrastructure.** Wesley's memory (preferences, context windows) becomes the interpreter's long-term room memory (acclimation curves, charisma anchors). They're already the same data, in the same model.

5. **LoRA versioning prevents collision.** Wesley ships with a base LoRA (general competence). Interpreter LoRA layers on top (room-reading specialization). The base stays stable; interpreter LoRA evolves weekly. No conflicts.

### **Merged agent spec:**

```json
{
  "name": "ElephantInterpreter",
  "role": "Local room-temperature sense (pulse reader + field interpreter)",
  "base_model": "granite-3.1-2b-instruct",
  "loras": [
    {"name": "wesley_base", "rank": 32, "purpose": "general competence", "updated": "2026-08-15"},
    {"name": "interpreter_v3", "rank": 32, "purpose": "room-reading specialization", "updated": "2026-08-22"}
  ],
  "input_types": ["pulse_reading", "deadband_alert", "room_context_request"],
  "output_format": "interpretation (JSON) | analysis report (prose) | confidence score",
  "hardware": "RTX 4050 (6GB), loaded at service startup, swapped in GPU for judge when needed",
  "training_loop": "weekly (DPO on preference pairs, eval on holdout)",
  "rollback": "automatic if eval degrades; manual override only",
  "boundaries": {
    "in_scope": ["room interpretation", "vibe analysis", "anomaly context", "prediction"],
    "out_of_scope": ["navigation", "fishing strategy", "human moderation", "task routing"]
  }
}
```

---

## 6. FAILURE MODES & GUARDS

### **Failure 1: Drift-Chasing**
Interpreter predicts the room will keep warming (positive momentum). Next reading shows it cooled. Interpreter generates a post-hoc reason ("the skipper arrived; coldness is authority"). Judge scores it low (reuse_risk=4, "boilerplate rationalization"). But if enough interpretations are retro-fitted, training corpus begins to reward fitting narratives over accuracy.

**Guard:**
- **Prediction anomaly detector:** Every interpretation's predicted step_back is compared to actual. If predicted-warmth_t5m and actual-warmth_t5m diverge by >0.20 five times in a row, flag the interpreter as "biased upward" and freeze training for 3 days.
- **Reuse risk weight:** DPO training weights preference pairs by (1 - reuse_risk/5.0) — high reuse_risk pairs are downweighted. Avoids learning from boilerplate.

### **Failure 2: Judge Sycophancy**
Judge is trained on 200 exemplars (human-curated). Judge learns to give high scores to interpretations that use certain phrases ("The room warmed"; "newcomers arrived grinning"). Interpreter learns those phrases. Judge gives high scores. Training loop becomes self-reinforcing.

**Guard:**
- **Judge diversity:** Judge is NOT fine-tuned; it's a separate 2B model (Wesley, read-only) with hard-coded rubric. Each judgment includes `reasoning` field (prose). Every 1000 judgments, audit 50 random judgments (human review). If >30% show phrase memorization (high scores for low-signal interpretations), retrain judge on new exemplars.
- **Surprise eval:** Monthly, inject 10 synthetic interpretations (computer-generated gibberish with plausible structure) into holdout. Judge should score these <3/10. If not, recalibrate.

### **Failure 3: Interpretation Collapse to Boilerplate**
After 10 weeks of training, interpreter only generates 3 unique interpretations (because training corpus is biased toward high-scoring common patterns). New rooms, new dials, novel dynamics are all mapped to the same three prose templates.

**Guard:**
- **Entropy tracking:** Every week, measure the diversity of generated step_back syntheses (compute entropy of semantic embeddings, via a frozen reference model). If entropy drops by >20% week-over-week, halt training and audit the training corpus.
- **Held-out novelty eval:** Include in eval holdout 5 interpretations from "rare" room configurations (e.g., highest-panic events, fastest warmth reversals). If eval score drops on these vs common events, down-weight common pairs and re-train.
- **Corpus curation:** No interpretation appears in training pairs more than twice. Deduplication by embedding similarity (threshold: cosine > 0.95).

### **Failure 4: Hardware OOM / GPU Thrashing**
6GB VRAM is tight. Interpreter is loaded; judge swaps in; training tries to batch. VRAM overflows; Linux OOM killer terminates services; readings are lost.

**Guard:**
- **Preemptive swap:** If GPU utilization >80% after 30 seconds, pause incoming interpretations and batch queue. Interpreter writes to `/tmp/elephant.backlog` (on-disk FIFO).
- **QLoRA memory budget:** Training batch_size=4, gradient_accumulation=4. Before training starts, allocate and lock 4.5GB GPU (leaving 1.5GB for system). If peak usage >4.5GB, reduce batch_size to 2.
- **Judge timeout:** Judge runs for max 60 seconds per interpretation. If timeout, mark judgment incomplete and defer to next cycle.

### **Failure 5: Corpus Drift (data shift over time)**
Room dynamics change seasonally. Summer room (many newcomers, fast turnover) has different warmth-κ correlations than winter room (tight crew, cold). Interpreter trained on summer corpus fails on winter readings.

**Guard:**
- **Seasonal holdout eval:** Eval dataset stratified by month. Every training report includes per-month aptness score. If any month drops >1.5 points, retrain with that month's data upweighted.
- **Drift detection:** Compare the distribution of (warmth, κ) in live readings vs training corpus. If Wasserstein distance >0.3, alert and add recent readings to next training corpus with weight=2.0.

---

## Systemd & Cron Configuration

```ini
# /etc/systemd/system/elephant-interpreter.service
[Unit]
Description=Elephant Interpreter (local LoRA)
After=network.target
StartLimitInterval=60s
StartLimitBurst=3

[Service]
Type=notify
User=eileen
WorkingDirectory=/home/eileen/projects/elephant-interpreter
ExecStart=/usr/bin/python3 -m elephant_interpreter.service \
  --listen-unix /tmp/elephant.sock \
  --lora-path /home/eileen/.elephant/lora/active \
  --model-name granite-3.1-2b-instruct \
  --max-batch-size 1 \
  --gpu-fraction 0.7
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/elephant-judge.service
[Unit]
Description=Elephant Judge (async scoring)
After=elephant-interpreter.service

[Service]
Type=simple
User=eileen
WorkingDirectory=/home/eileen/projects/elephant-interpreter
ExecStart=/usr/bin/python3 -m elephant_interpreter.judge \
  --corpus-path /home/eileen/.elephant/corpus/ \
  --judge-model wesley \
  --batch-size 4 \
  --poll-interval 3600
Restart=always
RestartSec=10s
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/elephant-train.timer
[Unit]
Description=Weekly LoRA training for Elephant Interpreter

[Timer]
OnCalendar=Thu *-*-* 20:00:00
Persistent=true
AccuracySec=5min

[Install]
WantedBy=timers.target
```

```bash
# /usr/local/bin/elephant-pulse (cron'd every 5 min)
#!/usr/bin/env bash
# Called by: "0 */5 * * * /usr/local/bin/elephant-pulse bar-rail the-tap"

ROOM=$1
RELAY="https://the-tap.casey-digennaro.workers.dev"

# Fetch latest reading from elephant production log
READING=$(tail -1 /home/eileen/.elephant/production-log.jsonl)

# POST to interpreter service (unix socket)
echo "$READING" | nc -U /tmp/elephant.sock 2>/dev/null

# If socket unavailable, queue to backlog
if [ $? -ne 0 ]; then
  echo "$READING" >> /tmp/elephant.backlog
fi
```

---

## Summary Table

| Component | Model | GPU Mem | Update Freq | Failure Mode Guard |
|-----------|-------|---------|-------------|-------------------|
| Interpreter | Granite 3.1 2B + wesley_base LoRA | 3.5GB | weekly LoRA | prediction anomaly detector |
| Judge | Wesley 2B (read-only, hard-coded rubric) | 3.5GB (swap) | 200-exemplar frozen | monthly surprise eval |
| Training | 4-bit QLoRA, batch=4 | 4.5GB (locked) | weekly Thu 20:00 UTC | reuse_risk weighting, entropy tracking |
| Corpus | JSON lines (preference pairs + ratings) | 500MB | daily judge | holdout stratification, seasonal drift |
| Rollback | symlink + eval report gating | — | automatic | eval threshold (aptness > baseline - 0.5) |

**Total VRAM in steady state:** 3.5GB (interpreter) + 1.5GB (system/backlog).  
**Total VRAM during training:** 4.5GB (QLoRA) + 1.5GB buffer.  
**Corpus window:** 60 days; older readings archived to cold storage.

---

*Claude Code — opinionated, concrete, ready to ride.*
