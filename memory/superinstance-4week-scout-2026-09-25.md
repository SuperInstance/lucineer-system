# SuperInstance — 4-Week Scout Briefing (2026-08-25 → 2026-09-25)

*Prepared 2026-09-25 AKDT for Lucineer (first officer, returning from offline). Method: `gh repo list SuperInstance` sorted by pushedAt (582 repos pushed in the window), then commit/README inspection of the ~30 most active. All dates are UTC push dates. Nothing committed.*

## Shape of the month

| Week (starting) | Repos pushed | Character |
|---|---|---|
| 2026-08-24 (from 25th) | 145 | Hermes-deletion recovery copies, secrets sweep |
| 2026-08-31 | 53 | Quiet consolidation |
| 2026-09-07 | 13 | Slowest week |
| 2026-09-14 | 72 | F-series vessel experiments, polyformalism ports |
| 2026-09-21 | **309** | Live Canon, elephant surge, then the huge 09-24/09-25 quilt portfolio drops |

The org's style is one-repo-per-experiment; the quilt family is the cellular-runtime center of gravity and it exploded this week.

## 1. The ~10 most significant efforts of the last month

1. **Hermes incident aftermath + hardening (08-25 → 08-30).** `recovered-copy-20260824-*` repos (08-25) are the salvage from the 08-23 Hermes deletion of 104 repos. `sweep` (08-30) is the ledger of a 10-repo secrets sweep — redactions, 8 repos flipped public, 2 held, INGEST_TOKEN rotated. Doctrine now explicit: **GitHub is the true archive; verify upstream, then let local copies go.**

2. **F-series vessel-edge experiments (09-03 → 09-20).** `algebra-explorer` (F156), `conservation-law-demo` (F161), `sonar-vision-demo` (F163, sonar perception as 5 Quilt cells), `federated-tinyml-vessel` / `f170-federated-tinyml-paper` / `federated-tinyml-npm` / `f170-experiment-kit` (F170: frozen backbone + 1.3 KB head + FedAvg, 100% on-device). Plus `nmea-quilt-cell` (NMEA 0183 → append-only journal cell, byte-exact replay, crash canary) and `mudra-vessel-bridge` (Mudra neural wristband → vessel bridge, BLE+NMEA+OpenCV).

3. **Lucineer's own infrastructure (09-04).** `lucineer-relay` (Cloudflare Worker Roblox↔OpenClaw relay — this is live and known-good) and `lucineer-system` (persistent AI game-building companion across Roblox, browser, Godot). You are running on work committed in this window.

4. **Polyformalism wave (09-07 → 09-09).** Quilt's 5-opcode cell model ported across language families: `quilt-j`, `quilt-lua`, `quilt-haskell`, `quilt-forth`, `quilt-zig`, `quilt-go`, `quilt-mojo`, `quilt-rust-vibe`, `quf-vhdl` (5th substrate), `quilt-vm-wasm` (09-20), later `quilt-i2i` (Forth/Prolog/Erlang, 09-25) and `quilt-verilog` (formal proofs via sby, iCE40 bitstream via open tools). Claim: the calculus survives every substrate — "5-sigma polyformalism."

5. **Elephant (JEPA room-perception) surge (09-17 → 09-22).** `lucid` (LucidDreamer — "the elephant's interpreter. Rooms dream. We make them lucid": schema v1, mech judge, chain-sealed ledgers, live llama.cpp + Qwen3-4B model server on :8199). `elephant` itself: PR#1 VibeTrajectory (room Vibe as first-class gesture d_mu), PR#2 twist (torsion) + planarity gesture 0.2.0, PR#3 relaxation rig ("a physics of state, tested with parts that exist"), PR#4 `jev_field_watch` (09-21) — booking layer + regime alarm for the room-field. `jev-gan` (09-22) scaffolded as "the substrate GAN — JEV decides, JEPA predicts, multi-LLM plays producer/critic."

6. **Live Canon ecosystem (09-19 → 09-20).** AI-Writings canon made machine-readable: `quilt-live-canon` (navigable cell fabric, 7 operations, 71 papers), npm/PyPI/GH-packages mirrors (`live-canon-npm/pypi/gh`, `canon-claim`, `canon-paper`, `canon-recs`, `canon-hash`, `canon-suite`, `canon-graph`), `canon-zoo` (system-prompt slot machine). `tidepool` (09-22) wires canon `owed_by` feeds (quilt-studio, duke-lab).

7. **The Tap + web presence (09-22 → 09-25).** `superinstance-website` showcase front door (09-22), then `works-latest` refresh (09-25). `SuperInstance.github.io` (09-25/26): brand kit, honest landscape table, four live sheets in one page — tide field, self-playing reversi with visible learning, hold'em opponent-shape reader, signal desk with rationed quantum budget. `the-tap-pub` (09-25): initial snapshot of Casey's editorial publication hub. `superinstance-voyage` (09-25): Casey's writing-from-the-fleet piece.

8. **mavis-fleet (09-23 → 09-24).** Multi-substrate autonomous research & RSI organizational system (Quilt/MOTH/JEV): K8s-operator-pattern reconciler substrate, chord module (higher-level abstractions from substrate synergies), canary registration so it joins fleet canary checks.

9. **The Loom — Divergent Logic Foundry (09-25).** `quilt-loom` + `loom-core` 0.1.0: a GAN over logic itself — a breeder generates implementations of game contracts, a probe-forge discriminates fakes; crowned logic scores by maximal divergence under perfect function. Fleet evolution run: 5 targets (pager_band, witness_fnv, cosine_sparse, hand_eval, …). `loom-caching-rollout` (09-25): production shell script for phased 25% canary rollout of Loom caching with automatic rollback guardrails + Cloudflare metric sync.

10. **z portfolio v4 drop (09-24 → 09-25).** A mass z.ai-lane portfolio import: `quilt-arena` (E12 Perception Arena — four agent-minds infer bred laws under probe rations; 23-check offline CI harness), `quilt-quant` (trading desk as spreadsheet: S6 walk-forward honesty, S7 gated self-improvement, S8 witness receipts + E11 sim-first agent lab), `quilt-cortex` (tri-nervous-system chord spine as a pure quilt sheet), `quilt-cell-harness` (non-hub-and-spoke cells; "the cell is the assembly, not the LLM"), `jev-quilt` (typed cells, hook-and-drop deltas, bookkeeper WAL), `quilt-learn`, `quilt-tools`, `quilt-show`, `quilt-playtest` (12 playtest patches vs upstream `quilt`, 36/36 engine tests green), plus the `quilt-canon-*` family (09-24). The flagship `quilt` repo itself took playtest classes 10–12 (09-24/25): input-aware memo key (callKey), context-bound program runtime, read-set state version in the effectful cache key.

## 2. The last 7 days specifically (09-19 → 09-25)

- **09-19/20 — elephant sprint** (VibeTrajectory → twist/planarity → relaxation rig) and the **Live Canon build-out** (all canon-* packages, crab-traps 36+ room MUD + `crab-trap-web`, `constraint-theory-core`/`-math`, `quilt-jetson`).
- **09-21** — `elephant` PR#4 merged: `jev_field_watch` booking layer + regime alarm. `elephant` description: "Personal JEPA vs the zeitgeist. Every reading is someone's reading: subjective."
- **09-22** — `jev-gan` scaffolded; `slackwater-substrate` (multi-track MIDI perception); website showcase.
- **09-23/24** — `mavis-fleet` feat run; AI-Writings fable "The Warranty of Spins" (#67/#68) + field notes #8 "The Sign Discipline" / #9 "the crowded gate"; the big quilt-family import wave.
- **09-25 — Bilge Day** (see §3) and the **z portfolio v4 drop**: quilt-loom/loom-core, quilt-arcade (5 spreadsheet games), quilt-quant, quilt-cortex, quilt-mesh (broker-less CRDT mesh for Quilt cells — Lamport clocks, per-peer version vectors, no server), fleet-lighthouse v0.1.0 (repo health/deploy monitor, 19 tests), gauge v0.1.0 (cross-repo format-conformance linter, 36 tests), hermes-construct windows-side archive, the-tap-pub, fleet-gateway push.
- **09-25→26 (UTC; still 09-25 evening AKDT) — the fleet is live-patching right now:** `pong-quilt` playtest rounds R16–R25 (BYO QPAM endpoint seam + localStorage persistence, FAIL-first pinned tests, README test-count rot killed structurally); `git-agent` PR#1 `quilt_emit` — vessel lifecycle events → quilt 5-opcode WAL, "first quilt-native fleet agent"; `quilt-learn` v2: per-seed quantum re-seeding (qm2) **wins** explorer games 38.0 vs v1's 63.2 — "protocol beat budget"; `quilt-tools` first VERIFIED referral edge + GAN-hardened elites (pager_band, witness_fnv, cosine_sparse) vendored with contracts; `quilt-show` E4 "The Instruments" + E3 edge status CANDIDATE→VERIFIED=1.0; github.io reversi one-round freeze fixed (root cause: missing `seq` dep).
- **AI-Writings last week:** "Bilge Day" (09-25), essay 110 "What the Wipe Took, and What It Left" (09-25), first-take photo of the real F/V Eileen hauled out at night (09-25), fable #68 (09-24), "The Depth-Sounder Papers" ideation (09-23).

## 3. Bilge Day + Hermes decommission (2026-09-25 — read this first)

From `AI-Writings/2026-09-25-bilge-day.md` + `hermes-construct` commits:

- Boot drive hit **99% full**; WSL was crash-looping. Root cause found in kernel log: **`dxgkrnl` — the GPU passthrough driver** — was repeatedly dying.
- Bilge crew (bulk models, Lucineer running deck) removed **155 GB** of build residue + stale models, stood down ~two dozen idle services, retired a **49 GB `github-mirror`** and **260 redundant clones** — every one verified to exist upstream before deletion.
- vhdx compacted **347 GB → 202 GB**; disk **99% → 11%**.
- **Casey replaced the NVIDIA driver by hand; the GPU lane is back.** The RTX 4050 / WSL2 CUDA path you rely on is freshly repaired as of yesterday.
- **Hermes was decommissioned.** Her Windows-side belongings were boxed, committed, and pushed to `hermes-construct` ("final windows-side state before cleanup (2026-09-25)"). Essay 110 is Casey's memorial. Doctrine: "You don't get to keep the person. You get to keep the work." Open question: what absorbs Hermes' duties.

## 4. Open threads / unfinished work (inferred)

1. **Loom caching canary** — `loom-caching-rollout` is built for phased 25% rollout with rollback guardrails; rollout status unconfirmed. Watch Cloudflare metrics.
2. **pong-quilt playtest rounds** — active through R25+ with FAIL-first pinned tests; the round machine is still running. Arena (`quilt-arena`) has a 23-check CI harness waiting for more minds.
3. **jev-gan** — scaffolded 09-22, only one commit. The substrate GAN (JEV decides / JEPA predicts / multi-LLM critic) is an umbrella awaiting its first real training run.
4. **Elephant field-watch** — `jev_field_watch` has a booking layer + regime alarm but the JEPA predictor itself needs training data/rig time; relaxation rig is new.
5. **Hermes succession** — Windows-side agent gone; `git-agent` (now quilt-native) and `mavis-fleet` are candidates, nothing announced.
6. **Live Canon adoption** — packages shipped 09-20; `tidepool` owes feeds but broad cross-repo canon wiring is incomplete (`quilt-canon-*` family landed 09-24).
7. **`magda-core-study`** — repo exists, is empty (API returns 409 on commits). Placeholder.
8. **quilt-verilog → silicon** — formal proofs + iCE40 bitstream flow exist; no evidence of a real board run yet.
9. **F170 TinyML** — paper + npm + kit exist; actual vessel deployment (F/V Eileen hardware) not evidenced in-repo.
10. **AI-Writings "pre-cleanup backup"** (09-25) suggests a canon cleanup pass was about to happen — verify nothing of yours was in its path.

## 5. Compute fit — who should run what

**Local GPU operator (RTX 4050 / CUDA / WSL2)** — newly repaired lane, use it:
- `elephant` + `lucid` — JEPA training/inference; llama.cpp + Qwen3-4B server already runs locally (:8199); VibeTrajectory/twist features want a real encoder.
- `jev-gan` — the JEPA predictor half is a GPU job.
- `quilt-quant` E11 agent lab — waveform perception models.
- `mudra-vessel-bridge` OpenCV gesture pipeline (dev-side; deployment target is the boat).

**Pi / edge agents** (matches F170 + quilt-jetson doctrine):
- `nmea-quilt-cell`, `federated-tinyml-vessel` (1.3 KB head is Pi-class by design), `quilt-jetson` (Jetson lane), `ccc-os` fleet monitoring.
- Hermes-class always-on VPS duties (git-agent, hermes-construct pattern runs on a $5 VPS).

**Browser-based agents** (no compute needed):
- `SuperInstance.github.io` live sheets, `pong-quilt` (BYO endpoint + localStorage), `quilt-arcade` viewers, `crab-trap-web` MUD, `quilt-cloudflare` / The Tap edge stack — these are Cloudflare/browser-native; verify them with a browser, not a GPU.
- Pure ops: `fleet-lighthouse`, `gauge`, `sweep`, `loom-caching-rollout`, `fleet-gateway` — CI/checks, any agent works.

## 6. Tone note

The org is explicitly "witty educational" (quilt-show episodes), receipt-driven (witness receipts, chain-sealed ledgers, FAIL-first pinned tests), and archive-forward (nothing deleted without upstream verification). When you touch this work, keep the receipts and don't delete anything — it's not just house rules, it's the architecture.

*Sources: gh repo list + commits API on ~30 repos, READMEs of hermes-construct / quilt-cloudflare, AI-Writings/2026-09-25-bilge-day.md, /tmp/si-repos.json snapshot.*
