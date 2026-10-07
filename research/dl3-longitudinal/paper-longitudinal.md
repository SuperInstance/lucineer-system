# Does the Judgment Boundary Drift? Longitudinal Validation of the Composed Pinch Route on Real Dial Streams

**DL3-LONGITUDINAL** · 2026-10-06
Pre-registered (`PRE-REG.md`, frozen before any run) · negative results first-class

## Abstract

The composed pinch route (JEV calibrated confidence × JEPA transition residual × ternary gate)
achieved FAR 3.3% on synthetic vessel-room data in the explore lane. We validate it
longitudinally on three real dial corpora: a 19-day bar-rail production stream (471 field
polls, 8 dials), a two-room live field daemon log (09-03 → 09-17, 2 s cadence, 9 dials), and
the 182-session nights corpus (6,830 speaks, 10 roster personalities). Three findings. (1)
**The judge does not drift; the stream does.** A fixed pin-probe re-judged daily held noul
0.82–0.85 (std 0.007) across 16 days while daily mean noul on the same room's real
transitions rose 0.64 → 0.82 (Spearman +0.615, p = 0.014), tracking a 4.7× decay in dial
movement as the room settled. Simultaneously the frozen day-1 JEPA kernel decayed (q95
residual trend p = 0.012; soft-exceed 36% → 100% on the-bridge): **semantic plausibility and
structural predictability dissociate over time, moving in opposite directions.** (2) **The
false-accept rate replicates; the false-reject rate breaks.** Composed FAR on real data was
5.0% [1.7–13.7] (3/60) vs 3.3% synthetic — every synthetic-style corruption (45/45) rejected,
every cross-room transplant (8/8) rejected — but FRR was 26.7% vs 0% synthetic, concentrated
exactly where the stale kernel rejected drifting-but-valid transitions. The three accepted
invalids were all same-room cross-day splices: the pinch catches room transplants, not time
transplants. (3) **The boundary that moves with personality is JEPA's, not JEV's.** On night
splices at two roster distances, JEV noul was flat (NEAR 0.356 vs FAR 0.351) while the kernel
residual ladder tracked roster distance exactly (median 0.43 → 0.79 → 1.07 for within /
near / far): the judgment cell reads the room; the manifold carries the personality.

## 1. Introduction

Five experimental lanes (JEV × JEPA × ternary) established, on static synthetic snapshots,
that JEV's calibrated `noul` probability and a JEPA-style transition kernel's residual are
complementary anomaly sensors, and that their ternary composition reduces false accepts 6×
over JEV alone. All five used synthetic corpora. Real dial rooms — the elephant's field
readings — have never been pushed through the composed route, and nothing was known about
JEV's calibration stability over weeks of real traffic.

Three questions, pre-registered before any experiment ran:

- **DL3a:** Does JEV's calibration drift over time — and if noul on real transitions moves,
  is it the judge or the stream that moved?
- **DL3b:** Does the composed route's FAR 3.3% survive real data, where "valid" means
  *measured* consecutive states rather than synthetic plausible ones?
- **DL3c:** Does the route's decision boundary move when the personalities in the room
  change — i.e., does it read the room or the cast?

## 2. Data

All measured data; nothing synthesized for the valid arms (corrupted arms are labeled
semi-real and use real base states).

| corpus | description | longitudinal axis |
|---|---|---|
| **B** bar-rail | live-tap production log, 2026-08-17 → 09-04, 471 polls (~30 min), 8 dials with real variance | 19 calendar days |
| **R** rooms | `roomd` field daemon, the-bridge + doctor-canary, 2 s cadence; dense 09-03/09-04 + coda 09-17 | 13-day frozen-kernel lag |
| **N** nights | 182 sessions (nights 28 + wave3 144 + wave4-pilots 10), 6,830 speaks, 7-dial `field_eff_after` per speak, roster personalities per session | 10 roster compositions |

A recon finding that shaped everything: the roomd log is *not* a continuous 13.5-day stream —
it covers 09-03 (~9 h), 09-04 (~8 h episodic), and 09-17 (~1 h), with a 13-day void. The
weekly+ longitudinal axis is bar-rail; the roomd corpus serves the cross-room and long-lag
arms. Real dial rooms are also low-dimensional (per room, 2–6 of 9 dials move at all).

## 3. Method (frozen; see PRE-REG.md)

**JEPA kernel:** linear `[s_t, 1] → s_{t+1}`, least squares on the corpus train split
(calibration = bar-rail days 1–3; rooms = 09-03 blocks; nights = sessions 1–100). Residual
thresholds RES_SOFT = q90, RES_HARD = q995 of train residuals. Kernels frozen at calibration
time — the longitudinal stress is the point.

**JEV:** SystemOne `jev-latest`, one `noul` per transition, horizon-appropriate question
(30-minute / 5-minute / next-speak). Key read at use-time; never logged.

**Route (exp4 verbatim):** +1 accept iff `noul ≥ 0.5 ∧ residual ≤ SOFT`; −1 reject iff
`noul < 0.35 ∨ residual > HARD`; else 0 hold. Arms: A accept-all, B JEPA-only, C JEV-only,
D composed. Metrics: FAR (invalid accepted), FRR (valid rejected), hold rate, Wilson 95% CIs.

**Pin-probe (DL3a):** one fixed synthetic moderate transition re-judged daily — a control
input separating judge-side drift from stream-side drift. Numeric warm-up 3 s before every
timed section (no GPU on host; CPU receipt logged per run). Seeds 2718. Total JEV spend 236
calls (95.3k in / 4.7k out tokens, 0 retries), exactly the pre-registered cap.

## 4. Results

### 4.1 DL3a — the judge holds; the stream and the kernel drift (verdict: STREAM_DRIFT)

| series | result |
|---|---|
| pin-probe noul (16 d) | 0.82–0.85, std 0.007, Spearman(day) = 0.27, p = 0.33 → **no judge drift** |
| daily real-transition noul | 0.64 → 0.82, Spearman(day) = +0.615, p = 0.014 → **stream drift** |
| daily median L1 dial movement | 0.62 → 0.14 (≈4.7× decay) — the room settled |
| Spearman(daily L1, daily noul) | −0.43, p = 0.09 (post-hoc, suggestive) |
| kernel q95 residual trend | Spearman(day) = +0.618, p = 0.012 → **kernel decay** |
| the-bridge soft-exceed | 36% (09-04) → 100% (09-17); doctor-canary 8% → 67% |

The drift question decomposes cleanly: JEV's calibration is stable on a fixed input;
its confidence on real transitions rose because the room's transitions became objectively
smaller (settling). In the same window the frozen kernel grew *more* surprised by the same
traffic. Semantic plausibility and structural predictability are different axes that moved in
opposite directions — the fact that the composed route composes exactly these two axes
predicts where it will fail next.

### 4.2 DL3b — the FAR replicates, the FRR breaks (G3 SURVIVES; G1, G2 FAIL)

n = 120 (60 valid real / 60 invalid: rate, range, breadth ×15 semi-real; splice ×15 all-real).

| arm | FAR | FRR | hold |
|---|---|---|---|
| A accept-all | 100% | 0% | 0 |
| B JEPA-only | 5.0% [1.7–13.7] | 43.3% [31.6–55.9] | 0 |
| C JEV-only | 16.7% [9.3–28.0] | 5.0% [1.7–13.7] | 0 |
| D composed | **5.0% [1.7–13.7]** | **26.7% [17.1–39.0]** | 10.8% |

Per-family composed FAR: rate 0/15, range 0/15, breadth 0/15, splice 3/15 (20%). All three
accepts were bar-rail cross-day splices with dial-sized deltas (e.g., earnestness 0.50 →
1.00) that JEV rated 0.62–0.75. Cross-room splices: 8/8 rejected. Complementarity persisted
on real data: 33/120 JEV-vs-JEPA disagreements.

**Why FRR broke:** 14/30 bar-rail valids carried residuals of 80–102 against thresholds of
0.33/0.45. Two stacked causes: (i) the lstsq kernel is rank-deficient on a calibration window
in which three dials never moved (volume, joke_landing, presence) — off-manifold states
extrapolate wildly; (ii) beneath the numeric artifact lies genuine drift: a post-hoc
LOO-regularized ridge kernel (λ = 100) recovers only partially (FRR_D 26.7% → 20.0%, FAR_D
unchanged). The rooms, whose kernels saw richer 09-03 traffic and whose JEV confidence was
high and uniform (0.77–0.81), composed to near-perfection: D-reject 0% (doctor-canary) and
6.7% (the-bridge).

**Gate integrity:** PRE-REG gate H0b was drafted with an inverted direction ("FAR ≥ 0.5" for
a harness-validity check whose intent was "the kernel must *see* corruptions"; measured FAR
0.0 satisfies the intent trivially). The as-written verdict INVALID_HARNESS is recorded; the
intent-literal recomputation is COMPOSED-FAIL (G1: 0.05 > 0.7 × 0.05; G2: 0.267 > 0.15).
G3 (the replication question): SURVIVES.

### 4.3 DL3c — JEV reads the room; the manifold carries the personality (verdict: MIXED)

| group | n | noul mean | residual median | reject (D) |
|---|---|---|---|---|
| within-night | 30 | 0.544 | 0.431 | 6.7% |
| NEAR splice (same cast) | 15 | 0.356 | 0.786 | 40.0% |
| FAR splice (jd ≥ 0.5) | 15 | 0.351 | 1.069 | 53.3% |

C1 (personality gate, ≥ 20 pts): 13.3 pts → FAIL (direction correct, CIs overlap). C2
(room-only null): NEAR − within = 33 pts → FAIL. The gradient exists but below gate. The
decisive observation is *where* it lives: JEV's noul distribution is identical for NEAR and
FAR (arm C rejects 93% of both) while the kernel residual ladder orders within < near < far
monotonically. The judgment cell is personality-blind at the semantic layer; roster identity
survives only in the geometry of the field's dynamics. Booked (C3): per-composition
within-night noul means span 0.395–0.617 (≫ pin noise 0.007) — different casts may sit
differently on the boundary, but n = 3–6 per composition confounds cast with session state.

## 5. Discussion

**Room vs personality.** The lane's motivating question — "does JEV's boundary move as
personalities change?" — resolves to *no at the layer asked*: JEV's semantic boundary is a
room-continuity detector, indifferent to who is in the room (on splice-class inputs).
Personality is real and measurable, but it lives one layer down, in the transition kernel's
state-space: fields evolve on cast-specific manifolds (residual median 0.43 vs 0.79 vs 1.07).
A personality monitor should therefore be built on kernel geometry (or cast-conditional
kernels), not on the judge.

**The two-axis dissociation.** JEV confidence rose while kernel residuals rose over the same
19 days. Any system that composes them inherits both signals' failure modes asymmetrically:
here the composition's FAR was protected by disagreement (either sensor alone can veto
accepts) but its FRR was exposed (either sensor alone can force rejects — and the stale kernel
did). Ternary composition is asymmetric by design; longitudinal drift turns that asymmetry
into a one-way ratchet toward holds and false rejects.

**Deployment guidance (for CM1 r7).** (1) Calibration windows must exercise every dial;
dead dims make lstsq kernels rank-deficient and their off-manifold extrapolations explosive —
use ridge at minimum. (2) Ship kernels with a drift monitor: the daily soft-exceed series
(the-bridge 36% → 100%) is the cheapest early-warning channel, computable with zero JEV
spend. (3) Rolling refit beats frozen thresholds on settling rooms; the pin-probe (one fixed
judgment per period) is the cheapest judge-side health check and held rock-stable here.
(4) The route's blind spot is time-transplants within a room; if replay/forgery matters,
add a state-recency channel — neither JEV nor the residual saw those.

## 6. Limitations

Bar-rail polls are ~30-min aggregates of a message window: "transitions" are coarse. The
roomd corpus's 13-day void reduces the long-lag arm to n = 5–8 blocks/day. DL3b's
rate/range/breadth families are semi-real (real base states, synthetic deltas) — only splice
is all-real. Nights ground truth assumes within-night evolution is valid by construction.
C3's composition-level means are underpowered. P3's drift-driver correlation is p = 0.09.
One drafting error in a harness gate (disclosed, both readings reported).

## 7. Artifacts

`PRE-REG.md` (frozen) · `dl3a_out.json` / `dl3b_out.json` / `dl3c_out.json` (full trial
records incl. every JEV prompt text, residuals, arms, ledgers, warm-up receipts) ·
`dl3_posthoc.json` (labeled post-hoc: ridge variant, FRR decomposition, drift drivers) ·
`dl3a.log` / `dl3b.log` / `dl3c.log` · `dl3_common.py`, `dl3a_longitudinal.py`,
`dl3b_pinch_real.py`, `dl3c_personality.py`, `dl3_posthoc.py`.

**JEV ledger:** 236 calls, 95,338 input / 4,720 output tokens, 0 retries.
