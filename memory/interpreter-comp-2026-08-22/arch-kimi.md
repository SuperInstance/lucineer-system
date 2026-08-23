# KIMICODE — Elephant Interpreter Architecture (competition entry)

*Filed 2026-08-22. Opinionated. One horse, ridden: **structured-JSON interpretations with mechanically-checkable predictions, a hybrid judge (deterministic first, model second), DPO flywheel on Qwen3-4B via unsloth QLoRA, and NO identity merge with Wesley.***

---

## 0. The three bets (read these first)

1. **An interpretation is a falsifiable object, not a vibe-essay.** Every interpretation carries numeric predictions on the elephant's own axes (per-dial direction, magnitude band, horizon). That makes "interpretations are relative to each other" *computable* instead of asserted: two interpretations of the same reading can be ranked by what actually happened next. Prose is the human-readable projection of the JSON, never the source of truth. (Ledger = lattice, reading = projection: the JSON is the ledger entry; the prose is one projection of it.)
2. **The judge is mostly arithmetic.** The expensive model-judge is the *second* stage. The first stage is a deterministic scorer that replays the interpretation's predictions against subsequent readings from `production-log.jsonl`. You cannot be sycophantic toward a subtraction.
3. **2B is a toy, 8B is a lie, 4B is the horse.** On 6GB VRAM, QLoRA of a 4B-class model is real (unsloth, 4-bit, ctx 2048, r=16). 8B QLoRA on 6GB "works" only with context so short (~512 tokens) that the corpus format won't fit — that's a demo, not a flywheel. Base model: **Qwen3-4B-Instruct-2507** (Apache-2.0, best JSON discipline and analytical prose in its class as of mid-2026, and it is *not* in the Granite/Liquid family already on the bench — diversity of inductive bias matters for the judge split, §3).

---

## 1. Architecture

### Where it lives

**New repo: `SuperInstance/elephant-interpreter`** (`/home/eileen/projects/interpreter/`, Python package `interp/`). Not an elephant subcrate. The elephant is the *sense* — it computes numbers and must stay numpy-pure and import-light (its README's own doctrine). The interpreter is the *voice* — it drags in torch, transformers, peft, a model server. Coupling them poisons elephant's test suite and deployability on boats. The seam between them is already built and already honest: **`data/production-log.jsonl`**, one JSON line per reading. The interpreter consumes that file; elephant never knows the interpreter exists. Same pattern as crab-traps and fleet-radio — siblings reading the ledger, not organs inside the elephant.

### Components and data flow

```
elephant production_probe.py (cron, existing)
      │  appends readings (pulse + deadband alerts)
      ▼
data/production-log.jsonl  ──tail/follow──►  interp-infer.service
      │                                        │  1. builds prompt: current reading
      │                                        │     + trailing window + drift context
      │                                        │  2. samples TWO candidate interpretations
      │                                        │     (temp 0.7 / 0.9) from local server
      │                                        ▼
      │                              data/interpretations.jsonl   (chain-sealed)
      │                                        │
      │                     ┌──────────────────┼────────────────────┐
      │                     ▼                  ▼                    ▼
      │           interp-score.timer    interp-judge.service   human reactions
      │           (deterministic,       (remote critic model,  (Tap /api reactions,
      │            realized vs           pairwise A/B +         replies, downstream
      │            predicted deltas)     rubric prose)          behavior — JEPA side)
      │                     │                  │                    │
      │                     └──────────────────┼────────────────────┘
      │                                        ▼
      │                              data/scores.jsonl  →  corpus builder
      │                                        │  (preference pairs + SFT seeds,
      │                                        │   versioned by content hash)
      │                                        ▼
      │                              interp-train.timer  (weekly / ≥150 new pairs)
      │                                        │  unsloth QLoRA → candidate adapter
      │                                        ▼
      │                              eval harness (held-out + blind A/B)
      │                                        │  promote?  symlink flip + restart
      │                                        ▼
      │                              adapters/current → llama.cpp --lora
      ▼
rollback: adapters/ keeps last 3; flip back in seconds
```

**Storage** (all ext4 under `/home/eileen/projects/interpreter/data/`, never `/mnt/c`, per fleet law):

- `interpretations.jsonl` — append-only, one JSON object per interpretation, **sha256 chain-sealed** exactly like the quilt/crab-traps ledger (`seal = sha256(prev_seal ‖ canonical_json)`). The seal is the Ammann bar: any single entry locally testifies which global history it belongs to, which is what makes corpus-version diffs and rollback auditable.
- `scores.jsonl` — judge + deterministic scores, keyed by interpretation id.
- `corpus/v<N>/` — immutable dataset snapshots: `sft.jsonl`, `dpo.jsonl`, `eval_holdout.jsonl`, `MANIFEST.json` (source id ranges, seal head, counts, git commit of builder). Never edit a versioned corpus; build `v<N+1>`.
- `interp.db` (SQLite) — indexes only (by ts, room, dial, score). JSONL is truth; SQLite is a rebuildable cache. O(batch) memory everywhere: corpus builder streams, never loads.

**What runs where** (WSL2, systemd is available — use it, per fleet infra rules; tmux is dev-only):

- `ollama.service` / `llama-server.service` — inference server, user unit, `Restart=always`, `MemoryMax=5G`. Serving: **llama.cpp server** with base GGUF Q4_K_M + `--lora adapters/current.gguf`. Adapter swap = symlink flip + `systemctl --user restart`. Ollama is the dev frontend; llama.cpp is production because LoRA hot-swap is a first-class flag, not a Modelfile rebuild.
- `interp-infer.service` — Python daemon following `production-log.jsonl` (`inotify` + 30s poll fallback). Rate-limited: max 6 interpretations/hour, deadband alerts get priority queue. Emits two candidates per trigger.
- `interp-score.timer` — every 15 min: deterministic scorer over interpretations whose horizon has elapsed.
- `interp-judge.service` — on-demand, remote critic call (DeepInfra, per production-notes precedent), nightly batch, hard daily cost cap.
- `interp-train.timer` — weekly Sun 03:00, or immediately when ≥150 new scored pairs land. `ConditionPathExists=` on the corpus manifest.

### Trigger wiring

The elephant's roomd already fires two ways; the interpreter treats them differently:

- **Pulse readings** → interpretation only if the trailing-window state is *interesting* (|Δ any dial| > 0.1 over window, or κ crossing 2.6/3.2 bands). Flat rooms get a heartbeat line, not an interpretation. This is guard #1 against corpus dilution (§6).
- **Deadband alerts** (d_warmth = −0.36 past 0.30, etc.) → always interpret, two candidates, priority. These are the high-value training rows: the room *spoke*.

---

## 2. The interpretation schema

JSON is the ledger entry; prose is derived. Schema v1:

```json
{
  "id": "ix-20260822-0042",
  "reading_ref": {"log": "production-log.jsonl", "line": 1337, "seal": "…"},
  "trigger": "deadband:d_warmth",
  "model": {"base": "Qwen3-4B-Instruct-2507", "adapter": "adr-0007", "temp": 0.7},
  "deltas": [
    {"dial": "warmth",   "observed_delta": -0.36, "meaning": "closing-time exodus, not conflict",
     "predicted_direction": "-", "predicted_magnitude_band": "0.2-0.5", "horizon_min": 60, "confidence": 0.7},
    {"dial": "presence", "observed_delta": -0.18, "meaning": "regulars leaving, not lurkers",
     "predicted_direction": "-", "predicted_magnitude_band": "0.1-0.3", "horizon_min": 60, "confidence": 0.6}
  ],
  "step_back": {
    "prose": "The room is emptying kindly — warmth and presence falling together with κ rising is a closing-time signature, not a fight. Expect quiet, not cold.",
    "room_arc": "winding_down",          // enum: warming | cooling | winding_down | tightening | scattering | stable
    "falsifiable_claim": "warmth stays in [-0.5,-0.1] and volume < 0.3 for the next hour"
  },
  "axes": {"specificity": null, "aptness": null, "calibration": null},   // filled by judge
  "phase_certificate": {"reader": "room-elephant", "adapter": "adr-0007", "warmth_confound_note": "warmth is a fiber decoration; v* is the physical axis — per REG-1"},
  "prev_seal": "…", "seal": "…"
}
```

Design rulings:

- **Per-dial delta-meaning is structured**: `meaning` is free text (≤12 words, enforced — forces compression), but `predicted_direction`, `predicted_magnitude_band` (enum: `0-0.1 / 0.1-0.3 / 0.2-0.5 / 0.5+`), `horizon_min`, and `confidence` are machine-checkable. The step-back's `falsifiable_claim` is constrained to comparisons over named dials — the deterministic scorer parses it with a tiny grammar, not an LLM.
- **Comparability is enforced three ways**, because one mechanism alone collapses:
  1. *Fixed prediction axes* — every interpretation bets on the same dials in the same units, so realized-vs-predicted error is a commensurable scalar across all interpretations, ordered by definition.
  2. *Fixed rubric axes* — `specificity / aptness / calibration` on a 0–3 scale, same rubric for every judge call (§3).
  3. *Pairwise Elo* — the judge's A/B picks within the same reading feed an Elo table over (adapter, temperature) configurations. Elo is the "relative to each other" the Captain asked for, literally.
- **The phase certificate is mandatory.** Per the Penrose dictionary (§3.1 of the fleet research): warmth is a window decoration on the reader's fiber, not a physical room coordinate. Every interpretation names *who is reading* (which adapter, which preset) and carries the confound annotation. You cannot kill the phason; you annotate it. An interpretation without a certificate is rejected at ingest.
- **Two candidates per trigger** is load-bearing: it manufactures preference pairs *for free* at inference time — the DPO corpus is a byproduct of normal operation, not a separate labeling program.

---

## 3. The judge

Two stages, in strict order. The model judge never sees a row the deterministic stage hasn't scored.

**Stage 1 — deterministic scorer (`interp/score.py`, pure Python, no model):**

For each interpretation whose horizon elapsed, replay `production-log.jsonl`:

- **Direction score**: fraction of dial predictions with correct sign (weight by confidence).
- **Magnitude score**: predicted band vs realized |Δ| — band hit = 1, adjacent = 0.5, else 0.
- **Claim check**: parse `falsifiable_claim` grammar; realized readings satisfy it? boolean.
- Composite `mechanical ∈ [0,3]`. This is 60% of the final score. It cannot be charmed.

**Stage 2 — model judge (remote, DeepInfra Seed-2.0-pro per fleet precedent):**

- **Pairwise**: for each reading's two candidates, blind A/B (order randomized, model identities stripped) on rubric: *which read is more apt, more specific, better calibrated given what happened since*. Winner/loser → DPO pair + Elo update.
- **Absolute**: 0–3 on `specificity` (does it name concrete dials/actors/timescales, or could this prose apply to any room on any night? — the anti-boilerplate axis), `aptness` (does the story match the numbers), `calibration` (confidence vs outcome).
- **Evidence bundle** given to the judge: the interpretation, the trailing 10 readings before it, the 10 after, and **human/agent feedback**: Tap reactions, replies quoting or referencing the interpretation, downstream behavior (did agents act on the read — e.g. someone "lit the woodstove"). Feedback ingest is an adapter behind the existing `Space` seam; v1 ships Tap-only, others as adapters land.
- **Anti-collusion rule**: the judge is *never* the same model family as the interpreter, and never sees interpreter prose from the same adapter generation twice in one batch without deterministic scores attached. Judge prompts and rubric versioned in `judge/RUBRIC.md`, hashed into every score row.

**How scores feed the corpus:**

- **Bootstrap (weeks 0–4): SFT.** First ~200 interpretations: candidates judged, winners + captain-edited rewrites → `sft.jsonl` (schema-perfect exemplars). You need SFT first because DPO cannot teach JSON grammar; it can only rank.
- **Steady state: DPO.** Pairwise losers/winners → `dpo.jsonl`. Chosen DPO over PPO (no reward model to overfit, no online loop to destabilize on a laptop) and over KTO (we have genuine pairs from the two-candidate design — throwing away the pairing would be waste).
- Hard rule: **no row enters any corpus without a deterministic score attached.** Judge-only rows are how sycophancy gets baked in.

---

## 4. The LoRA flywheel

**Training reality check on RTX 4050 6GB (WSL2):**

| Base | 4-bit weights | QLoRA trainable on 6GB? | Verdict |
|---|---|---|---|
| 2B (Granite 3.1, LFM2.5) | ~1.5GB | easily, ctx 4096+ | trains, but the analytical ceiling is the problem, not VRAM. Both bench models stay as **baselines**, not the horse. |
| **Qwen3-4B-Instruct-2507** | ~2.8GB | yes — unsloth, r=16, α=32, ctx 2048, grad-ckpt, paged_adamw_8bit, batch 1×accum 8 | **the horse.** Fits with ~1GB headroom; quality jump over 2B is the entire point of the exercise. |
| 8B (Qwen3-8B etc.) | ~5.2GB | only at ctx ≤512 with everything paged — corpus rows are ~700-900 tokens | dishonest. Don't. Revisit on a GPU upgrade. |

**Loop:**

1. `interp-train.timer` fires (weekly or ≥150 new pairs). Corpus builder streams `interpretations.jsonl` + `scores.jsonl` → `corpus/v<N+1>/` with **time-split holdout**: last 14 days of readings are always eval, never train (prevents the flywheel from grading its own homework on memorized rooms).
2. unsloth QLoRA: SFT warm-start only for adapter 0; thereafter DPO from the current adapter. ~40-70 min/run on the 4050 at 4B — fine overnight. `MemoryMax=10G` on the train unit; nice 19.
3. Adapter exported → merged → GGUF Q4_K_M → `adapters/adr-NNNN.gguf` + `adr-NNNN.json` (corpus version, seal head, hyperparams, eval results).

**Eval harness — how we know the new adapter is better:**

- **Held-out mechanical**: run candidate vs champion over the 14-day holdout readings; deterministic scorer must not regress (Δmechanical ≥ −0.05).
- **Blind judge A/B**: 50 sampled holdout readings, both adapters interpret, remote judge picks blind. Promote iff win-rate ≥ 55% AND specificity axis non-regressing.
- **Canary suite** (`eval/canaries.json`): 20 hand-written readings with known-right interpretations (the fight, the closing time, the joke that landed — from production-notes' own table). Candidate must stay within rubric distance of the known-right answers. This catches silent capability rot that Elo can miss.
- Promote = atomic symlink flip `adapters/current` + `systemctl --user restart llama-server`. Recorded in `adapters/LEDGER.md`.

**Rollback:** last 3 adapters kept on disk; `interp-ctl rollback` flips the symlink back and restarts. Because every interpretation records its adapter id, a bad generation is *identifiable and quarantinable* in the corpus — bad-generation rows are excluded from future corpus builds by adapter id. The chain seal makes the quarantine boundary auditable.

---

## 5. The merge question — NO, with a shared substrate

Casey proposes merging Wesley (ensign, growing) and the interpreter into one agent whose primary job is pulse analysis. **Against the identity merge. For the infrastructure merge.**

Three arguments, in escalating order of how much I believe them:

1. **The repo already settled this.** Room-Elephant vs Personal-Elephant: the zeitgeist must be *neutral* — two readers of the same room get the same field — while a personality is dial_weights + bias + attachments, i.e., precisely a *non-neutral* reader. Wesley is a personality: an ensign with a name, a growth arc, attachments. An interpreter with attachments is a Personal-Elephant; its readings stop being the room's light and become Wesley's mood lighting. Merge the identities and you have built, by definition, a reader whose fiber confound is now *the product*. The Penrose result says the reader's γ is already an irreducible confound — the last thing you do is give the instrument a bigger γ on purpose.
2. **Judge contamination.** Wesley acts in rooms (replies, reactions). If the interpreter is Wesley, the judge's "did the room move as predicted" evidence includes the interpreter's own actions — self-fulfilling reads: predict cooling, go quiet, room cools, score 3/3. The flywheel learns to make itself right, not to be right. A separate interpreter has no hands; that impotence is its epistemic virtue. (The elephant nudges; it doesn't drive. The interpreter shouldn't even nudge — it *testifies*.)
3. **Blast radius and cadence.** Wesley is growing — his weights/prompts churn on a personality-development cadence. The interpreter wants glacial, eval-gated change. One agent means one rollback story: a personality regression rolls back the instrument, or an instrument promotion ships an untested personality.

**The merged substrate (the part Casey is right about):** one inference server (`llama-server` hosts base + N LoRA adapters — Wesley's adapter and the interpreter's are siblings), one adapter registry, one corpus toolchain, one eval harness, shared memory store schema. Two identities, one body of plumbing. If in six months the interpreter's readings become Wesley's primary sensory cortex — Wesley *consumes* interpretations as input — that's the right coupling direction: the ensign reads the instrument; the instrument never becomes the ensign.

---

## 6. Failure modes and guards

| Failure | Mechanism | Guard |
|---|---|---|
| **Drift-chasing** | Every deadband alert begets an interpretation; alert storms on noisy nights flood the corpus with redundant panic | Priority queue + 6/hour cap; alert dedup — same dial re-crossing within 30 min extends the existing interpretation's horizon instead of spawning a new one; corpus builder downweights clusters (max 2 rows/room/hour in training data) |
| **Sycophancy toward the judge** | Interpreter learns the judge's prose taste, not room truth | Deterministic scorer is 60% of the score and cannot be charmed; judge is a different model family; rubric hashed and versioned; monthly captain audit of 10 random pairs — if judge/captain agreement < 70%, judge rubric is the bug, fix it before next training cycle |
| **Boilerplate collapse** | "The room is shifting in a complex way" scores fine on vibe, says nothing | `specificity` axis is a first-class scored dimension; `meaning` field capped at 12 words with a banned-phrase list (`eval/boilerplate.txt`, embedding-similarity screen against corpus — rows >0.92 cosine to any prior row get specificity ≤1 automatically); canary suite demands concrete dials |
| **Self-echo / feedback loop** | Interpreter's own write-backs (if ever given a voice) re-enter the room and get read | v1: interpreter is read-only — no `/api/speak`, ever; write-back stays human-approved per production-notes lesson #2. Interpreter-authored content anywhere is tagged and excluded from its own input window |
| **Phason confound baked into weights** | The LoRA learns the warmth decoration as if it were the room | Phase certificate on every row keeps the annotation in the training data itself; corpus includes the v*/warmth distinction in system prompt; REG-1's 82–84° result cited in the SFT seed set so the model can *say* "this is a fiber reading" when it is |
| **Corpus poisoning / drift of taste** | A bad adapter generation contaminates future training | Adapter id on every row; quarantine by id; corpus versions immutable with sealed manifests; rebuild-from-ledger always possible |
| **WSL2 OOM during training** | 6GB VRAM + Windows host pressure | batch 1 + grad accum; paged optimizer; train at 03:00; `MemoryMax` on the unit; if OOM kills a run, the timer retries with ctx 1536 — degraded but alive, and the degradation is logged in the adapter manifest |
| **Elo inflation** | Both candidates get better vs judge but neither gets truer | Mechanical score is Elo-independent; canaries are absolute, not relative. Promote gate requires all three |

---

## Closing position

Build the interpreter as a **sealed-ledger instrument with falsifiable predictions**, judge it arithmetic-first, train it DPO-on-4B, and keep it identity-separate from Wesley on shared plumbing. The elephant computes the field; the interpreter testifies about it; the judge checks the testimony against the ledger; the LoRA folds the verdicts back into the voice. Every piece of that loop already has a fleet analogue — the chain seal is the Ammann bar, the phase certificate is the γ-annotation doctrine, the deterministic scorer is `imbalance ≡ d_mu` wearing a judge's robe. Nothing here is a new metaphysics. That's the point: the fleet's math already knows how to do this.
