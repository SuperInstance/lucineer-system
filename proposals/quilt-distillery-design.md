# quilt-distillery — design proposal (new repo)

*Drafted 2026-09-30 by Lucineer from Casey's brief: "a novel automated training system for training
streamlined jevs to perform tasks in an application through quilted distillation... custom backend
tiny in-browser webgpu/wasm models for intelligent pages with intuitive reactions... simple games
like quilt-arcade for proof-of-concept."*
*Status: proposal. No repo created yet — awaiting Casey's pick on name + go-ahead.*

## One line
An automated **distillery** that turns cheap big-model judgments into tiny, provable, shippable
judgment cells (streamlined jevs) that run client-side in WebGPU/WASM — with every training event
recorded on a quilt tape you can fault-localise.

## Name candidates
- **quilt-distillery** (primary — matches `quilt-arcade` family; the artifact is "distilled")
- `quilt-jevs` (flat, descriptive)
- `jev-hatchery` (on-doctrine: the fleet raises small boats; a hatchery raises small jevs)

## Why this is not "just distillation" (the load-bearing novelty)
1. **Quilted provenance.** The whole pipeline writes a quilt-style tape: `BIND` rows carry the
   *state* (values materialised), `LINK` rows carry the *teacher call + op*, `EFFECT` rows carry the
   *distilled judgment*. XR-1 (2026-09-30) proved the tape is a serialised cell graph with all values
   present, so `find_fault` localises to a specific training event: *"this jev is wrong because of
   teacher cell 412."* Distillation artifacts become auditable, not just accurate.
2. **Gates before labels (CM1 doctrine).** Teacher output must clear a format-first parse gate, then a
   confidence band / cross-teacher quorum, before it can become training signal. Bad teacher output is
   quarantined, never distilled. This is the pincher applied to *labels*.
3. **Pinch the known.** A calibration set of known-answer states bypasses teachers entirely
   (deterministic routing, zero teacher tokens) — exactly the pinch/fallback primitive, now on the
   label path.
4. **Precision by instability (W5b/W5b2).** Ternary export allocates precision by *flip frequency*
   (antirank), not lifetime — W5b killed the lifetime story for from-scratch ternary and W5b2 is
   confirming antirank. This directly sets the size/quality knob for wasm blobs.
5. **Ship where the user is.** The artifact runs in the page (WebGPU fast path, WASM everywhere, no
   server round-trip, no tokens, works offline) — the "intelligent page" reacts intuitively without
   phoning home.

## The jev (artifact contract)
A jev is NOT a chat model. It is: **state features + a small set of typed questions → graded answers.**
- Question types mirror the System One/Jev API: `noul` (graded yes/no 0..1), `choice`, `score`.
- Sizes: 50k–2M params (MLP / tiny GRU / ternary linear stacks). Target artifact: **<300 KB**.
- Acceptance: ≥90% agreement with teacher on held-out states; deterministic (same state → same
  grade); p95 latency <5 ms in-browser; fault-localisation demo passes.

## Pipeline (7 stages, each a module)
1. **jevfile** — the task spec (JSON/YAML): state schema, questions (typed + instructions), reaction
   bindings (answer band → app reaction), acceptance gates. One file = one trainable jev.
2. **Foundry (`harvest.py`)** — state generation. For games: headless loops over quilt-arcade titles
   with scripted/bot player variants → unbounded synthetic states, seeded and recorded. For real apps:
   record live states. Deterministic replay is the point.
3. **Teacher pass (`teacher.py`)** — batched System One API calls (`jev-latest`), plus *local teachers*
   (nimble / tev1 via Ollama — free, offline) and optional DeepInfra roster for a **disagreement map**.
   Every prompt/answer/seed pair is written to the tape.
4. **Gate cells (`gates.py`)** — format-first parse gate → confidence band → quorum; quarantine file for
   rejected labels; pinch calibration set for known-answer routing.
5. **Student fit (`train.py`)** — shared tiny encoder + per-question heads (IE3: dedicated trunks beat
   joint trunks; **routing happens between cells**), or fully per-question micro-cells when n ≤ 3.
   TWN ternary during training; antirank precision plan for export.
6. **Export (`export/`)** — ternary/int8 weights → `quilt-c` → WASM (ternary matmul kernels) +
   WebGPU path (WGSL compute shader) + `jev.js` loader (~200 lines); `onnxruntime-web` as fallback.
7. **Receipt + showcase** — per-jev manifest (teacher IDs, data digests, agreement, params, size,
   tape hash) sealed under `receipts/`; quilt-arcade pages load the jev and render **the why** (graded
   answer + the tape cell that justified it).

## PoC ladder (fits RTX 4050 + CPU + CF free tier)
- **P0 — sensei jev (tictactoe):** teacher = the perfect solver (free, infinite, perfect labels; no
  API at all), student = ternary mini (≤300 KB wasm; stretch: 64 KB), question = `noul` "does this
  move lose?" per empty cell; showcase = a board that heats up with blunders, plus the visible
  learning loop the arcade already loves. Zero teacher cost makes this the honest first proof.
- **P1 — taste jev (reversi spice) + `=JEV()`:** `score` question over position aesthetics with the
  model roster as teachers; ships as a spreadsheet formula so any sheet can call it.
- **P2 — multi-teacher + pinch + curriculum:** disagreement map, calibration-set pinch, and the
  boundary-weighted curriculum probe (teacher-token savings reported honestly).
- **P3 — brood + ambiguity map + wish lists:** nano/mini/full for one jevfile; ambiguity map shipped
  in the bundle; privacy-safe wish-list collection from real visits.

## Repo layout
```
quilt-distillery/
  README.md              # fact: what ships
  DOCTRINE.md            # trail: why tapes+gates+pinch (links XR-1, CM1, W5b/W5b2)
  jevfile.schema.json
  distill/               # harvest.py teacher.py gates.py tape.py train.py
  distill/export/        # wasm build, webgpu shader, jev.js
  arcade-poc/            # P0/P1 games (thin layer over quilt-arcade)
  receipts/              # per-jev manifests + tape hashes
  tests/                 # tape round-trip, gate quarantine, determinism, find_fault
```

## Reuse (do not rebuild)
`quilt-c` (C/WASM), TWN + W5b2 antirank plan (ternary export), CM1 gates + pinch, percept-plugs
witness/HMAC discipline (`D-1..D-6`), i2i-ledger for a jev registry (`book`/`near`), CF Pages + R2 for
the showcase, Ollama nimble/tev1 as free local teachers.

## Creative expansion (the fun part)

### 1. `=JEV()` — judgment cells as spreadsheet cells
The arcade's games are *spreadsheets with rules as cells*. So the artifact shouldn't be a black-box
blob bolted onto a page — it should be **a cell you can type**: `=JEV("blunder", B2:D4)`. One
`=JEV()` function, backed by a ≤300 KB wasm judgment cell, usable in any sheet, any page, any app.
The oldest ubiquitous compute substrate becomes the deployment surface for tiny judgment models.
"Intelligent pages with intuitive reactions" = a sheet that reacts where you're looking.

### 2. Teacher = the solver itself (free, infinite, perfect labels)
For tictactoe/connect4/gomoku, perfect play is *computable*. That makes the teacher free, instant,
deterministic, and infinite — no API, no tokens, no 429s. **P0 becomes: distill the solver into a
sensei jev** that grades every empty cell with "does this lose?" The showcase is a board that heats
up with blunders in real time. Where the roster teachers come in is the *subjective* questions —
"how spicy is this position?" (reversi), "is this player tilting?" (hold'em) — matters of taste,
where multi-teacher disagreement isn't noise, it's the product.

### 3. Curriculum as the student's confusion (lesson mining)
Don't sample states uniformly; sample where curiosity lives: **student uncertainty × teacher
confidence × disagreement × pinch-boundary proximity**. The distillery asks the teacher for lessons
precisely where the student is wrong-but-loud. That's apprenticeship, not compression.
Falsifiable and cheap: boundary-weighted 1k states vs random 1k — agreement gain per teacher token.

### 4. Ambiguity map as a first-class artifact (negative space)
The arcade already ships `NEGATIVE_SPACE.md`. So should every jev: the states where teachers
disagree, or where the student is uncertain, become a sealed **ambiguity map** shipped *with* the
weights. A jev that knows what it doesn't know can hand the hard 3% to a human. Two products, one
pipeline: the student (agreement) and the map (taste).

### 5. Deployment-fed curriculum (the fleet learns from its voyages)
Inference is local, so the *page* can notice its own hard cases — and emit a privacy-safe **wish
list**: feature vectors + the grade it wanted, never raw content. Wish lists from thousands of
visits batch back into the next distillery round. The jev ships, sails, and comes home with
homework. The hundred-boats doctrine, applied to model improvement.

### 6. Rack-flip the page (front = game, back = the ledger that taught it)
Every jev carries its tape hash. Add one affordance: flip the page, and the game's lessons appear —
the training states that shaped this reaction, the teacher's grades, the student's agreement curve.
Click a reaction, see the lessons. Transparency as gameplay. (ActiveLog/ActiveLedger, shipped.)

### 7. The 64 KB challenge (demo-scene constraint)
Nano tier: a jev under **64 KB** — the classic demo-scene budget. Ternary 5–20k params + a tiny wasm
shim fits. Five games, five jevs, each under 64 KB, each with a readable lineage. A memorable
constraint that forces the precision-allocation work (W5b2's antirank) to matter.

### 8. One sheet encoder, many jevs (the stitch)
All five games share one substrate: a grid of cells. So train **one sheet encoder**, then many
question heads — per game, per question. The quilting stitch is literal: the encoder is the thread,
the jevs are the patches. Tests a real question: does grid state transfer across games?

### 9. Hatchery language (doctrine fit)
A **jevfile** is an egg. Training **hatches** a hatchling. A size family is a **brood** (nano/mini/
full — the page picks by device: battery, thermals, GPU). A defect traces through the **lineage**
(tape) back to the bad teacher lesson. The fleet raises small crew, each with its own logbook.

## Honest risk register
- Distillation and in-browser inference are both well-trodden; the *novel* part is the tape+gate+pinch
  provenance loop and the ternary antirank export — if those prove marginal, this becomes a decent
  ordinary distiller.
- WebGPU compute shaders on 6 GB dev card are testable but the *browser* matrix (Safari/iOS) needs
  real-device checks before claiming "everywhere".
- Teacher quality ceiling: a distilled jev cannot beat its teacher; the pitch is *cheap, private,
  offline, auditable*, not *better*.
