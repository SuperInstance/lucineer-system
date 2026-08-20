# Nights A–C + D — Gate 2 Measurement Report

*2026-08-19 · Nights Runner (subagent) · measurement, not tuning.*
*Base: gate-1 commit `d1d0bf1` (vmf MLE + tapnight edge log, as shipped — zero code changes to `elephant/`).*
*Corpus: commit `cd00bb8` — `data/nights/night-{A,B,C,D,D-cold}.jsonl`, `coarse-anchor.jsonl`, `night-A-repro.jsonl`, `summary.json`; runners `scripts/nights_abc.py`, `scripts/nights_diagnostics.py`. Deterministic: lexical dials, fixed scripts drawn from `examples/tapnight_cycles.py` + `tapnight_themes.py` (verbatim cast/lines), seeded bootstrap.*

---

## 1. Numbers

### Per-night (μ̂, κ) — Nights A/B/C are identical by construction and by measurement

| quantity | value |
|---|---|
| whole-night fit (40 msgs, W=8) | κ̂ = 10.91, CI [8.44, 14.67], warmth_vMF = +0.436, warmth_v0 = +0.253, top dials: mood, earnestness, volume |
| SEG1 fit — warm-earnest (seq 0–19, n=20 windows) | κ̂ = 30.31, ρ = 0.904, warmth_vMF = +0.741, μ̂ ≈ [.586, .524, .545, .000, .201, .163, .136] |
| SEG2 fit — cynical-banter (seq 20–39, n=20) | κ̂ = 30.44, ρ = 0.905, warmth_vMF = −0.254, μ̂ ≈ [−.043, .377, .053, .907, .050, .149, .074] |
| across-night spread (A/B/C, per-seq, max over all seqs × pairs) | max ‖Δμ̂‖ = **0.000000**, max |Δκ| = **0.000000** |

### Noise floor (the thing gate 4 was missing)

| quantity | value |
|---|---|
| **across-night floor (identical scripts)** | **0.000 — exact.** Byte-identical replay verified by md5 of logs with `session_id` stripped (`b0312253…` for both A and the re-run). The dial-space instrument has **no stochastic component**; the encoder-side 0.05 floor has **no analog** here. |
| within-night per-message drift (stable stretches seq 10–19 & 30–39, 60 edges pooled A–C) | mean 0.0276 · median 0.0283 · p95 0.0376 · max 0.0377 |
| transition stretch (seq 20–27) per-message drift | mean 0.0419 · max 0.0459 (peaks at seq 27) |
| jackknife SE(μ̂) scale | 0.098–0.154 → shipped 2×SE deadband ≈ 0.20–0.31 |

### Fine gap (within-cast, within-night: SEG1 → SEG2 in μ̂ space)

| metric | value | vs 0.05 encoder floor | vs 0.10 deadman | vs within-night drift (0.038 max) |
|---|---|---|---|---|
| chord ‖Δμ̂‖ | **1.2285** | 24.6× | **12.3×** | 32.6× |
| cosine 1−μ̂₁·μ̂₂ | **0.7546** | 15.1× | **7.5×** | — |

Identical in all three nights (1.228510 / 0.754618 each) — trivially consistent, because deterministic.

### Coarse anchor (warm SEG1 room vs TTRPG room, both n=20)

| metric | value |
|---|---|
| chord ‖Δμ̂‖ | 0.9409 |
| cosine | 0.4426 (3.5× the encoder-side 0.271 anchor) |
| TTRPG fit | κ̂ = 15.30 (W=8), warmth_vMF = +0.080, μ̂ ≈ [−.008, .165, .518, .000, .216, .798, .148] (panic+earnestness axis) |

**Harness is alive. But note the ordering inversion — see §4.**

### Night D — the newcomer (drifter: cold-cynical vibe, charisma 0.45, entry at seq 24 = 60% of the 40-msg baseline)

| quantity | value |
|---|---|
| entry marker | `first_by_author=true` at seq 24; presence_mask gains `drifter` within W; 46 msgs total; pre-entry stream byte-identical to Night A ✓ |
| condition-level displacement (pre-entry sub-room vs drifter-era sub-room) | **chord 0.830 / cos 0.345** — 8.3× deadman, 22× within-night drift max |
| trajectory displacement (cumulative logged fits vs pre-entry fit) | max 0.518 · mean 0.328 · last-8 mean 0.467 |
| κ̂ pre → post era | 21.23 → 47.03 (the room got **tighter**, not looser) |
| charisma observable ‖field_eff − field_raw‖ | 0.646 → 1.262 mean; alignment with drifter direction 0.469 → 0.788 |
| acclimation (roster-at-open, Night D as spec'd) | **flat** — slope −5.6e-5/msg; distance at entry already 0.0014 (pre-warmed; see deviation #2) |
| acclimation (cold-entry variant D′, roster joined at entry) | dist 0.149 → 0.0005, **slope −0.0051/msg** (≈ −34%/10 msgs), decay half-life ≈ 20 msgs; charisma alignment post-entry 0.888; raw field trajectory identical to D, `field_eff` diverges exactly at seq 24 |

### Diagnostics shipped with the fits (spec §1.5)

- **κ(W) sweep** (monotone in W everywhere; report, don't hide): seg1 27.3/30.3/35.5 · seg2 23.0/30.4/37.1 · full night 10.0/13.8/17.5 · TTRPG 17.4/22.2/30.9 for W=4/8/16.
- **corr(warmth_vMF, log κ)** across the 6 room-level fits: **r = −0.22** — tripwire (|r|>0.8) **not tripped**; the MLE disambiguation holds on this corpus (the v0 norm proxy was collinear by construction).
- **Post-hoc deadband (‖Δμ̂‖ > 2·max SE)**: **0/10** stable-SEG1, **0/10** stable-SEG2, **0/8** transition, **0/22** post-entry. Per-message d_mu (0.015–0.046) never reaches the deadband (0.20–0.31). See §4.

### Speaker-holdout probe (dial-tier analog — NOT the pre-registered test)

Full-night μ̂ displacement when one author's messages are removed: critic 0.194 · essayist 0.150 · writer 0.147 · engineer 0.119 · captain 0.102 · poet 0.067; κ̂ ranges 11.2–17.3 vs 13.8 full. No single speaker carries the room direction; structure is distributed (note: removing an author also drops the presence dial's distinct-author count — occupancy is a room statistic, so this mixes content and occupancy by design).

---

## 2. VERDICT against the deadman switch

**The dial-space numbers: fine gap = 1.23 chord / 0.75 cosine, versus the 0.10 deadman threshold — cleared by 12× in 3-of-3 runs, deterministically identical across A/B/C; within-night drift max 0.038 < 0.05 < 0.10 < 0.83 (newcomer) < 1.23 (fine gap). At the tier we could measure, the bet survives, and the harness is demonstrably not dead.**

**Three plain qualifications, none of them polish:**

1. **This is the dial-space analog, not the pre-registered encoder measurement.** The deadman (devils-advocate §3) was registered against the frozen-v2 encoder + contrast head: fine gap 0.015 → ≥ 0.10, speaker-heldout ≥ 0.50 over four nights. None of that apparatus exists here. **The encoder-side deadman remains armed and untested. Nobody should read this run as the switch clearing.**
2. **The pre-registered speaker-heldout condition is UNTESTED at this tier** — there is no classification head to score. The holdout probe above shows distributed (non-collapsed) structure; it is a sanity probe, not the condition.
3. **The measured fine gap is between lexically distinct registers** (warm-earnest vs cynical-banter). Lexical dials separate vocabulary-shifted segments trivially. The deadman's hard case — same-register, different-night (the 0.015 encoder measurement) — maps at the dial tier onto the across-night A/B/C measurement, which is exactly 0.000 because the instrument is deterministic: **at the dial tier the noise floor is zero, so "is the gap above noise?" is no longer the binding question — any real script difference is above noise.** The binding question moves entirely to the encoder tier, where the deadman already sits.

---

## 3. Edge logs

Saved and committed (`cd00bb8`, pushed to `SuperInstance/elephant`): `data/nights/night-A.jsonl`, `night-B.jsonl`, `night-C.jsonl` (42 lines each: open + 40 speaks + close), `night-D.jsonl`, `night-D-cold.jsonl` (48 each), `coarse-anchor.jsonl` (22), `night-A-repro.jsonl` (determinism check), `summary.json` (analysis snapshot). Note: `data/` is gitignored by repo convention; the nights corpus was force-added (`git add -f data/nights/`) per the deliverable — tracked files stay tracked, the rest of `data/` remains ignored.

---

## 4. Deviations & surprises

**Deviations**
1. **Nights A/B/C are byte-identical** (task demanded identical scripts) → the across-night "noise floor" degenerates to a determinism verification, which passed exactly (md5 match). Reported as 0.000, not dressed up as a positive floor; the within-night drift scale (0.028 mean per-message) is reported alongside as the operative microstructure scale — it is real window-sliding drift, not instrument noise.
2. **Night D roster semantics:** the engine acclimates every rostered participant from message 0, so the spec-literal Night-D newcomer (roster at open) is pre-warmed at entry (dist 0.0014, flat curve — measured, not assumed). Added the **D′ cold-entry variant** (roster joined at entry, runner-side, no engine change) which yields the real acclimation curve. Deviation: D′'s `session_open` roster lacks the drifter — the persona/vibe_start live in the runner script, a small replay-honesty gap, noted.
3. **Self-tuning never invoked** (constraint honored: no `tune_participant`, dial-weights frozen; measurement only). Deploy/ untouched. No changes to `vmf.py`/`tapnight.py` — no genuine bugs hit.
4. **Fine gap measured per the task's definition** (two distinct thematic exchanges); the same-register subtle variant is out of assigned scope (see verdict §2.3).

**Surprises**
1. **Ordering inversion:** the within-night thematic shift (1.23 chord) **exceeds** the cross-room coarse anchor (0.94 chord; 0.44 cos). The encoder tier's fine≪coarse structure (0.015 vs 0.271) does **not** replicate in dial space — dial μ̂ separates vocabulary registers more strongly than it separates warm-room vs panic-room. Cross-room retrieval keyed on dial-space fields should not be assumed to inherit encoder-tier geometry.
2. **The shipped per-message deadband never fires** — 0/50 edges, including the segment transition and the newcomer arrival. SE(μ̂) ≈ 0.10–0.15 ≫ per-message d_mu ≈ 0.015–0.046. On the cumulative session-to-date estimator, transitions read as stillness at message grain; the signal lives at condition level (sub-room fits). Gate 4's "edges carry real:null" question now has an empirical answer, and it is conservative.
3. **Night D tightened the room** (κ 21 → 47): a consistent cold-cynical newcomer made the field *more* concentrated, not less — tightness and warmth moved independently, exactly the disambiguation gate 3 wanted (corr r = −0.22 confirms).
4. Determinism is total — identical scripts give bit-identical logs (verified), so three-run consistency for the deadman is trivially satisfied at this tier; three *distinct* runs would only differ if scripts differ.

---

## 10-line summary

1. Nights A/B/C/D/D′ + coarse anchor run on shipped gate-1 code; zero engine changes; logs committed `cd00bb8`.
2. Across-night noise floor = **0.000 exactly** — the dial-space instrument is deterministic (byte-identical replay, md5-verified).
3. Operative within-night drift: per-message ‖Δμ̂‖ mean 0.028, max 0.038 — window-sliding microstructure, not noise.
4. Fine gap (warm-earnest → cynical-banter, same cast, one night): **1.229 chord / 0.755 cosine** = 12.3× the 0.10 deadman, 3/3 nights.
5. Coarse anchor (warm vs TTRPG room): 0.941 chord / 0.443 cos — harness alive, but fine>coarse ordering inverts the encoder tier's 0.015/0.271.
6. Night D newcomer displaces μ̂ by **0.830 chord** (8.3× deadman, 22× drift max); κ rises 21→47 (tighter, not looser); charisma |δ| doubles, alignment 0.47→0.79 (0.89 cold-entry).
7. Acclimation: spec-literal D flat (pre-warmed by roster semantics); cold-entry D′: 0.149→0.0005, slope **−0.0051/msg**, half-life ≈ 20 msgs.
8. Diagnostics: κ(W) monotone (±25% over W∈{4,16}); warmth–logκ corr −0.22 (confound tripwire clear); shipped 2×SE deadband fires 0/50 even at transitions — conservative at message grain.
9. **Verdict: at the dial tier the bet survives — fine gap ≫ 0.10, deterministic 3-run consistency, no single-speaker collapse. But the pre-registered deadman targets the encoder tier (0.015→0.10, speaker-heldout ≥ 0.50): that switch remains ARMED and UNTESTED. This run must not be booked as the deadman clearing.**
10. Biggest surprise: dial-space geometry ≠ encoder geometry (fine>coarse inversion) — cross-room retrieval on dial μ̂ inherits different structure than v3's probe numbers imply.
