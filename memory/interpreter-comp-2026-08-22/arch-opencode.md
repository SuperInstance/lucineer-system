# mahout — the elephant's interpreter
### OPENCODE's competing architecture · interpreter-comp-2026-08-22

*The elephant reads the room. The mahout reads the elephant.* A mahout is
not the elephant and never rides it into the room — the keeper's job is to
know what the animal is feeling, certificate its blind spots, and say so in
words the crew can score. That division of labor is the whole architecture.

**Grounding read:** `elephant/README.md`, `docs/production-notes.md`,
`research-penrose-fleet-2026-08-21.md` §0–§2 (ledger=lattice, reading=
projection, warmth=window decoration, confound=phason, seal=Ammann bars).

---

## §0. The picks (opinionated, on the record)

| Question | My horse | Why in one line |
|---|---|---|
| Where it lives | **New sibling repo `SuperInstance/mahout`** | elephant stays numpy-only, import-free; mahout carries the torch. Never imported *by* elephant. |
| Base model | **Qwen3-4B-Instruct-2507**, unsloth 4-bit QLoRA | The largest model that *honestly trains* on 6GB; analytical class >> 2B. (§4 has the VRAM math.) |
| Judge | **Mechanical-first**: deterministic Python scoring of forecasts + LLM judge adapter second + human anchor third | Most of "did the room move as predicted" is arithmetic, not opinion. Unbribeable by construction. |
| Training | **SFT cold start (~100 gold) → best-of-3 DPO flywheel, weekly** | Best-of-n at generation time manufactures preference pairs for free on one laptop. |
| Schema | **Structured-canonical JSON + bounded prose**, fixed enums, quantized buckets, contrast graph, phase certificate | Comparability by construction, not by hope. |
| Merge with Wesley | **NO on weights and role; YES as a tool Wesley consults** | An interpreter embedded in the agent cannot certificate its own phason (§5). |

Rejected alternatives, for the record: Granite 3.1 2B as interpreter base
(trains fine, analytical ceiling too low — it stays Wesley's body);
LFM2.5-2.6B (hybrid SSM arch, LoRA support experimental — keep on the bench
as the speed comparator); Qwen3-8B (does NOT train on 6GB; inference-only
oracle at best); elephant subcrate (pollutes the numpy-only doctrine);
 wesley-adjacent placement (couples the certificate to the confound).

---

## §1. Architecture

### 1.1 Data flow (end to end)

```
 elephant side (unchanged doctrine, additive fields)          mahout side
┌────────────────────────────────────────────┐   ┌─────────────────────────────────────────┐
│ cron: examples/production_probe.py (pulse) │   │ mahout/watch.py (systemd user service)  │
│ elephant/roomd.py (opt. drift daemon)      │   │  tails data/production-log.jsonl        │
│        │ both append lines:                │   │        │ inotify                        │
│        ▼ {ts, room, trigger, field, …}     │   │        ▼                                │
│  data/production-log.jsonl ───────────────►│──►│ queue (sqlite mahout/data/queue.db)    │
│                                            │   │        ▼ best-of-3, ~20s each           │
│                                            │   │  mahout/generate.py → llama-server      │
│                                            │   │   :8199 (Qwen3-4B + current LoRA)      │
│                                            │   │        │ 3 candidates                   │
│                                            │   │        ▼ winner (judge-mech fast path) │
│                                            │   │  mahout/data/interpretations.jsonl     │
│                                            │   │  losers → mahout/data/candidates.jsonl │
│                                            │   │        ▼ T+2h or +30 events (delayed)  │
│                                            │   │  judge_mech.py (deterministic)         │
│                                            │   │  judge_llm.py  (judge adapter)         │
│                                            │   │        │ judgments.jsonl               │
│                                            │   │        ▼ weekly, ≥300 new pairs        │
│                                            │   │  train_dpo.py (timer 02:00, GPU)       │
│                                            │   │   → eval.py → promote.py               │
│                                            │   │        ▼ atomic symlink                │
│                                            │   │  adapters/current → vN; merged GGUF;   │
│                                            │   │  restart llama-server                  │
└────────────────────────────────────────────┘   └─────────────────────────────────────────┘
```

### 1.2 Elephant-side trigger wiring (a ~40-line diff, nothing more)

The probe already exists and cron'd. Add two things, both additive:

1. **Trigger metadata** on every log line: `trigger: "pulse" | "drift"`,
   `prev_ts`, and `deltas: {warmth: -0.36, kappa: +0.19, ...}` (field
   before→after). Deadband logic (|d_warmth| > 0.30, etc.) computes here,
   where the previous reading already lives. The log line shape stays a
   superset of today's — old lines still parse.
2. **`elephant/roomd.py`** — optional tiny daemon (argparse, no deps) for
   low-latency drift: reads via the existing space adapters on a 60s tick,
   emits the same lines to the same file. Cron probe stays as the
   heartbeat even if roomd dies. Two paths, one log — never two truths.

### 1.3 mahout repo layout

```
~/projects/mahout/
  mahout.toml                  # rooms, deadbands, judge timing, ports, bands
  mahout/
    schema.py                  # Interpretation dataclass + enums + validation
    watch.py                   # tail → queue (the daemon)
    generate.py                # context builder + best-of-3 + JSON repair
    judge_mech.py              # deterministic scoring (calibration, specificity, boilerplate)
    judge_llm.py               # judge-adapter prompts + rubric scoring
    evidence.py                # subsequent readings, reply trees, reactions
    train_sft.py  train_dpo.py # unsloth QLoRA
    eval.py      promote.py    # genesis set, holdout, win-rate gate, symlink flip
    seal.py                    # sha256 chain over interpretations.jsonl
  bin/mahoutd                  # single entrypoint (serve / watch / judge / train / eval)
  data/
    queue.db                   # sqlite job queue (survives reboot, replayable)
    interpretations.jsonl      # chain-sealed; the canonical record
    candidates.jsonl           # best-of-n losers (DPO fuel)
    judgments.jsonl            # mech+LLM scores
    judgments-human.jsonl      # captain's weekly anchor ratings
    corpus/v0.1/*.jsonl        # versioned training extracts (SFT, DPO)
    evals/genesis-40.jsonl     # frozen, human-annotated, NEVER trained on
  adapters/
    frozen-genesis/            # SFT v0, the last-resort rollback
    v0.2/ v0.3/ ... current -> v0.3
    gguf/mahout-4b-q4km-v0.3.gguf
  ~/.config/systemd/user/
    mahout-watch.service       # the daemon, Restart=always
    mahout-judge.timer         # sweeps missed judgments every 30min
    mahout-train.timer         # checks pair-count nightly 02:00, trains Sundays
```

Process model: **systemd user services, not tmux** (survive logout,
restart on failure, journald logs). A `make tail` tmux target exists for
interactive dev, but production never depends on a pane being open.
Training kills and restarts llama-server around itself (VRAM is the
scarce resource on a 4050).

### 1.4 The chain seal (the Ammann bar)

Every `interpretations.jsonl` line carries `prev_sha256` — the same
discipline as crab-traps' D1 edge ledger. Consequence from the Penrose
dictionary: the lineage of interpretation is *locally decodable global
phase*. Any single sealed line testifies which history it belongs to;
tampering or branch-forking is detectable from one line. This is cheap
(10 lines of `seal.py`) and it makes the corpus court-admissible to
itself — DPO pairs can be verified as "really from adapter v0.2."

---

## §2. The interpretation schema

**Both, with structure canonical and prose bounded.** The structured part
is what's scored, compared, and trained on; the prose is what humans read.
Prose may never carry load-bearing claims absent from the structure.

```json
{
  "id": "tap-2026-08-22T21:14Z-0031",
  "seal": {"prev_sha256": "ab12…", "this_sha256": "cf90…"},
  "trigger": "drift",
  "reading_ref": {"ts": "2026-08-22T21:14Z", "log_line_sha": "…"},
  "adapter": "v0.3",
  "deltas": [
    {"dial": "warmth", "d": -0.36, "bucket": "large-down",
     "confidence": 0.71,
     "mechanism": "joke-missed",          // enum, see below
     "evidence": ["msg:4187", "msg:4192"]}
  ],
  "step_back": {
    "phase": "fraying",                    // enum
    "temperature_call": "cooling",         // 5-point enum
    "tightness_call": "tightening",        // κ
    "vstar_call": "presence-thinning",     // volume+/presence- axis
    "momentum": {"warmth": "falling", "kappa": "rising", "vstar": "falling"},
    "story": "The toast that landed flat broke the room's stride; the
              quiet after it is people deciding whether to try again
              or settle the tab. (44w)",
    "contrast_links": [
      {"rel": "similar", "id": "tap-2026-08-19T22:02Z-0027", "why": "post-miss deflation"},
      {"rel": "opposite", "id": "tap-2026-08-15T23:40Z-0019", "why": "same joke, roared"}],
    "forecast": {
      "horizon": "next_pulse",
      "warmth": {"sign": "-", "bucket": "small-down"},
      "kappa":  {"sign": "+", "bucket": "small-up"},
      "vstar":  {"sign": "-", "bucket": "small-down"},
      "would_falsify": "warmth recovers > -0.10 without roster change"}
  },
  "phase_certificate": {
    "warmth_is_decoration": true,
    "basis": "warmth carries fiber mass (REG-1: cos(W,v*)≈0.11); read via v* and quote evidence, not as room temperature",
    "carried_phason": "adapter v0.3, room-history tap, no roster shift observed"}
}
```

**The enums (frozen at v1; changes are corpus-version events):**

- `mechanism` ∈ {joke-missed, joke-roared, arrival-of-presence,
  departure-of-presence, sincerity-drop, irony-spike, panic-seed,
  panic-spread, external-event, closing-time, newcomer-acclimation,
  charisma-pull, roster-shift, unknown} — a closed vocabulary the
  judge can search for in subsequent messages.
- `phase` ∈ {warming, cooling, tightening, loosening, gelling, fraying,
  static, breaking} — exactly one per interpretation.
- `bucket` ∈ {large-down, small-down, flat, small-up, large-up} —
  quantized magnitudes (|d| bands aligned to the deadband: small straddles
  noise, large ≥ deadband), because a 2B–4B model cannot rank raw floats
  honestly but can call buckets.
- `story` ≤ 50 words, must cite ≥ 2 message ids that also appear in
  `evidence` (validated in `schema.py`; a failing story is rejected and
  the next-best candidate wins).

**How comparability and relativity are enforced — three layers:**

1. **Fixed axes** (the enums + buckets): every interpretation answers the
   same slot-set, so any two are row-comparable without embedding voodoo.
2. **Contrast graph** (`contrast_links`): each interpretation must relate
   to ≥ 1 prior interpretation (similar/opposite + why). Meaning from
   contrast is the elephant's own doctrine (sauna/plunge); this makes the
   interpretation corpus a self-ordering graph instead of a pile.
3. **Embedding index** (a `sentence-transformers` mini model, CPU): the
   structured part is serialized canonically and embedded; the index
   gives (a) nearest-neighbor ordering for "relative to each other,"
   (b) the boilerplate-distance detector (§6), (c) retrieval for
   contrast-link suggestions.

**Why the phase certificate is load-bearing, not decoration:** REG-1
proved warmth is a fiber functional misread as room temperature. An
interpreter that forgets this will narrate the reader's phason as the
room's weather — the classic failure, now with a measured 84° error. The
certificate forces every interpretation to carry the confound annotation
(ZeroClaw's ANNOTATE-not-kill ruling, made structural). Forecasts on
warmth are still allowed — but each is tagged with what would falsify it,
and the mechanical judge scores warmth forecasts on *sign only*, never
magnitude, honest to λ* < 1 (the room signal is a faint perturbation on
the fiber).

---

## §3. The judge

**Opinion: the judge is 60% arithmetic, 30% model, 10% human.** The fleet
insight from REG-1 applies to judges too: the strongest evidence is
cross-time and mechanical, not another model's vibes.

### 3.1 Timing and evidence

A judgment fires at **T+2h or +30 room events** (whichever first) after
each interpretation, via the watch daemon's scheduler + the belt-and-
suspenders timer. Evidence window = interpretation → judgment:

| Source | What it proves | Where from |
|---|---|---|
| Subsequent readings (≥ 2 probe lines) | calibration: did warmth/κ/v* move as forecast | production-log.jsonl — *deterministic* |
| Messages since | aptness: does the named mechanism's vocabulary recur (reply pressure, laughter tokens, panic lexicon) | space adapters (ChatSpace already normalizes reply trees; MudSpace events) |
| Human reactions | emoji/quote-reactions to the room's content, count + polarity | adapter ingest (additive) |
| Agent responses | did downstream agent behavior shift as the phase call implied | room agents' output logs |
| Roster delta | was it actually a roster-shift phason, not room motion | author sets before/after |

### 3.2 Rubric (100 pts)

| Axis | Wt | Scorer | Method |
|---|---|---|---|
| Calibration | 35 | **mech** | sign accuracy on warmth/κ/v* forecasts vs realized deltas, bucket-weighted (large-right > small-right); falsify-clause honored = bonus |
| Aptness | 25 | **mech+LLM** | mechanism keywords retrieved in window (mech similarity); LLM judge adjudicates ambiguous hits against message text |
| Specificity | 15 | **mech** | count of unique grounded message ids; template penalty for enum repetition |
| Contrast | 10 | **mech** | contrast_links resolve, and targets aren't the same 3 ids every time |
| Craft | 15 | **LLM** | 1–5 on the story: does it name *this* room, or any room? |

Bands: **≥ 75 gold** (SFT/DPO-chosen eligible), **45–74 usable**,
**< 45 rejected** (DPO-rejected when paired with a gold sibling).
LLM judge = the *same Qwen3-4B base with a separate judge adapter*,
prompted with the message window + rubric, temperature 0. Cold start:
**Seed-2.0-pro via DeepInfra** as critic (fleet precedent from the
production notes) until judge-vs-human agreement (§3.3) crosses 70%.

### 3.3 The human anchor (the anti-Goodhart organ)

The captain rates **5 random interpretations/week**, three questions
(calibration yes/no; aptness 1–5; boilerplate yes/no) into
`judgments-human.jsonl`. Judge-vs-human agreement is tracked on a
dashboard line; **if it drops below 70% for two consecutive weeks, the
judge adapter is flagged for recalibration and promotion freezes.** The
judge can be gamed; the mechanical scorer can't; the human anchors the
drift between them.

### 3.4 Feeding the corpus

- **SFT (once, cold start):** ~100 gold events — 40 hand-written by
  Casey/captain on Tap + wheelhouse transcripts, 60 best-of-8 distilled
  under Seed-2.0-pro critique, all human-checked. Never expanded with
  self-output (no self-distillation — that's the collapse road).
- **DPO (the flywheel):** best-of-3 already yields ranked candidates per
  event; a pair enters the corpus when score gap ≥ 25 and winner ≥ 75.
  Chosen = winner, rejected = loser. If pairs run sparse (quiet weeks),
  fall back to **KTO** on unary scores — noted, not the horse.
- **Never trained on:** `genesis-40`, the frozen human-annotated eval
  set; and anything from `evals/holdout-14d/` (rolling last-14-days).

---

## §4. The LoRA flywheel

### 4.1 Honest 6GB math (RTX 4050, WSL2, unsloth 4-bit QLoRA)

| Model | Weights (4-bit) | QLoRA @ seq4096, b1+accum, ckpt | Verdict |
|---|---|---|---|
| Qwen3-1.7B | ~1.2 GB | ~3 GB | trains easily; too weak analytically |
| Granite 3.1 2B | ~1.6 GB | ~3.5 GB | trains fine; Wesley's body, not this job |
| LFM2.5-2.6B | ~1.9 GB | ~4 GB* | *hybrid SSM; unsloth LoRA experimental — bench comparator only |
| **Qwen3-4B** | ~2.5 GB | **~5.2–5.5 GB** | **trains. the horse.** |
| Qwen3-8B | ~5 GB | OOM / glacial w/ offload | **does not train on 6GB.** inference-only oracle (Q4_K_M GGUF ≈ 4.9 GB), CPU-offloadable for eval-time second opinions |

Serving: `llama-server` with merged **Q4_K_M** export per promoted
adapter (~2.7 GB resident, room for KV cache at 8k ctx). DPO params:
r=16, α=32, β=0.1, lr 1e-4, 2 epochs, seq ≤ 3072, ≥ 300 pairs to arm.

### 4.2 The loop

1. **Nightly 02:00 timer:** count new pairs; if < 300, exit (no
   undernourished training runs).
2. **Sunday train:** DPO on `corpus/vN` (immutable snapshot; corpus
   versions are append-only, schema-versioned, DPO pairs expire at 90
   days to shed stale-judge judgments).
3. **Eval gauntlet** (all four must pass):
   - genesis-40 blind pairwise vs current adapter, position-swapped,
     LLM-judged: **win-rate ≥ 55%**;
   - mechanical calibration on holdout-14d: **not worse**;
   - boilerplate-distance (mean embedding distance to 10-NN of prior
     stories): **not lower**;
   - JSON validity rate ≥ 98% (schema.py as judge).
4. **Promote:** `adapters/current` symlink flip (atomic), export merged
   GGUF, restart llama-server. Keep last 3; `frozen-genesis` is the
   floor. Any failed gate = silent no-op, current keeps serving —
   **rollback is "the symlink never moved."**

We know the new LoRA is better because it must beat the incumbent on a
set it has never seen *and* not regress on the two failure detectors.
Weeks where nothing passes are healthy weeks.

---

## §5. The merge question — against merging Wesley and the interpreter

**No.** Three reasons, one of them fatal:

1. **The phason argument (fatal).** The Penrose dictionary's deepest
   result: the reader's personality *is* the internal-space offset, and
   it is structurally invisible from inside the room chart — REG-1
   measured the warmth/physical-axis angle at ~84°. Wesley is *made of*
   personality fiber — that's what an ensign is. An interpreter fused
   with Wesley cannot certificate Wesley's phason any more than a patch
   of tiling can determine its γ. The interpretation would launder the
   reader's mood as the room's weather *by theorem, not by bug.*
   Separation of duties isn't org hygiene here; it's the cut E∥ ⊥ E⊥.
2. **Identity capture.** Wesley's job is growing — first-person,
   speaking into rooms, accumulating attachments. The interpreter's job
   is third-person, never speaking into rooms (read-only doctrine from
   the production notes; the write seam stays human-approved). A merged
   agent optimizes the pulse cadence (many small jobs/day) and the
   ensign's conversations become interruptions of the meter-reader.
3. **Catastrophic forgetting.** A task LoRA on shared weights would
   carve Wesley's growth for a gain in dial narration. Different jobs,
   different bases today (Granite 2B vs Qwen 4B) — merge the
   *infrastructure*, not the weights.

**The boundary table (what the relationship IS):**

| | mahout | Wesley |
|---|---|---|
| Person | third person about the room | first person in the room |
| Speaks into rooms | never (dry-run narrator lines at most, human `--write`) | yes, that's the job |
| Memory | readings + interpretations only | relationships, attachments, growth |
| Base | Qwen3-4B + mahout adapters | Granite 3.1 2B |
| Reads the other | — | **yes: interpretations land in Wesley's context as room narration** (via the existing nudge/tint seams — the elephant *nudges*, never drives) |

So Wesley consults the mahout the way a deckhand reads the barometer:
informed by, never fused with. **Revisit conditions** (write them down
now): merge onto one base only when (a) Wesley's body ≥ 8B-class local,
(b) roles live as separate adapters with the judge *external to both*,
(c) the phase certificate survives a quarter without a drift incident.

---

## §6. Failure modes and guards

| # | Failure | Signature | Guard (structural) + detector |
|---|---|---|---|
| 1 | **Drift-chasing** — interpreting deadband noise, pulses of phason flips | interpretation rate ↑ while mech calibration hovers 50% | Rate cap: ≤ 1 non-pulse interpretation/hr/room; `real`-flag discipline (delta > 2·max SE gates generation); detector: interpretation-to-reading ratio dashboard |
| 2 | **Sycophancy toward the judge** (Goodhart) | judge scores ↑, human agreement ↓, calibration flat | 35/100 of the rubric is unbribeable arithmetic; judge-vs-human < 70% for 2 wks freezes promotion; genesis-40 never trained on; pairs need gap ≥ 25 *and* winner ≥ 75 (absolute floor, not just ranking) |
| 3 | **Boilerplate collapse** — every story is "the room feels a shift" | mean embedding 10-NN distance ↓; `mechanism` entropy ↓ | Eval gate: boilerplate-distance may not decrease on promote; story must cite ≥ 2 grounded msg ids (rejected at schema validation); mechanism enum histogram monitored — any value > 35% share fires review |
| 4 | **Phason re-entry** — narrating the reader's fiber as room weather | warmth forecasts "confidently right" while phase_certificate lines vanish | Certificate is schema-required (validation, not convention); warmth scored on sign only; eval set includes phason-trap items (roster-shift events labeled as such) |
| 5 | **Tap overfit** — an interpreter that only knows one bar | great on Tap, incoherent on wheelhouse/synthetic rooms | genesis-40 spans Tap + wheelhouse + fleet-sim rooms; contrast eval requires cross-room links weekly |
| 6 | **Corpus rot** — DPO pairs from a stale/broken judge | promoted adapters plateau then regress on genesis | 90-day pair expiry; corpus versions immutable; genesis is frozen (a regression there is unmaskable) |
| 7 | **GPU contention / OOM** — training starves serving, laptop throttles | llama-server OOM at 02:01 | train pipeline stops server first, restarts after (or on failure, via systemd); seq caps in config; anything 4B never trains on CPU |
| 8 | **Silent fallback dishonesty** — model down, mahout fakes it | interpretations continue during outages | Fleet rule from the production notes: emit `[FALLBACK: no-interpretation]` skeleton lines (deltas + bucket labels, no story, marked `template: true`), never prose. Fallback lines never enter the corpus |

The meta-guard over all eight: **the chain-sealed record + the frozen
genesis set + the mechanical scorer** form three artifacts no adapter can
rewrite. The flywheel can only spin as fast as what it cannot touch.

---

## §7. Build order (two weeks to first DPO)

- **Days 1–3:** schema.py + watch.py + trigger diff in elephant probe; chain seal; FALLBACK skeletons flowing.
- **Days 4–7:** base Qwen3-4B served; gold corpus (40 hand + 60 distilled); SFT v0 → `frozen-genesis`; genesis-40 annotated.
- **Days 8–10:** judge_mech + evidence plumbing; judge cold-start on Seed-2.0-pro; judgments flowing.
- **Days 11–14:** best-of-3 → candidates; train_dpo + eval gauntlet + promote; first Sunday run. Interpretations enter Wesley's context via nudge seams (read-only).

---

## Provenance

Read: `/tmp/interpreter-brief.md`, `elephant/README.md`, `elephant/docs/production-notes.md`, `memory/research-penrose-fleet-2026-08-21.md` §0–§2. Written by OPENCODE (zai-coding-plan/glm-5.3) for interpreter-comp-2026-08-22. This file is the only artifact; no repos touched.
