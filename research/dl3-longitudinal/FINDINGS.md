# DL3-LONGITUDINAL — Findings

**Date:** 2026-10-06 · **Lane:** DL3 deep (JEV calibration drift + composed pinch on real data)
**Status:** all three experiments ran to completion under the frozen PRE-REG.md.
**JEV spend:** 236 calls, 95.3k in / 4.7k out tokens, 0 retries (exactly at the pre-registered cap).

## Headline results

| Exp | Verdict (frozen rules) | One-line |
|---|---|---|
| DL3a | **STREAM_DRIFT** | JEV itself is stable (pin-probe std 0.007); its confidence on real transitions rose 0.64→0.82 over 19 days because the room quieted — while the frozen JEPA kernel decayed in the same window. |
| DL3b | **INVALID_HARNESS as-written / COMPOSED-FAIL intent-literal** (G3: **SURVIVES**) | Composed FAR on real data 5.0% [1.7–13.7] vs 3.3% synthetic — the false-accept rate replicates. But FRR exploded to 26.7% (0% synthetic): real data breaks the route on the valid side, via kernel decay, not via the judge. |
| DL3c | **MIXED** (C1 fail 13.3pts < 20pt gate) | The boundary is primarily room-continuity. Personality gradient exists (FAR 53% vs NEAR 40% reject) and lives **entirely in JEPA's residual geometry — JEV is personality-blind** (noul 0.356 NEAR vs 0.351 FAR). |

## DL3a — the calibration-drift question, answered cleanly

The pin-probe design (fixed synthetic transition, re-judged daily) separated judge from stream:

- **Judge: stable.** Pin noul 0.82–0.85 across 16 days, std 0.007, no trend (p=0.33).
- **Stream: drifting.** Daily mean noul on real transitions: Spearman(day) = +0.615, p=0.014.
  JEV's confidence in the SAME room's real transitions rose from ~0.64 to ~0.82.
- **Driver (post-hoc, p=0.09, direction consistent):** the room settled. Median per-transition
  L1 dial movement fell ~4.7× (0.62 → 0.14) over the 19 days. Quieter room → more plausible
  transitions. The drift is in the data, not the judge.
- **Kernel decay (co-primary):** frozen day-1–3 kernel's q95 residual on real transitions trends
  up (Spearman +0.618, p=0.012). roomd: the-bridge soft-exceed rate 36% (09-04) → **100%**
  (09-17); doctor-canary 8% → 67%. A 13-day-old kernel rejects half to all of real traffic.
- **The dissociation:** JEV confidence rose while kernel residuals rose — semantic plausibility
  ("could a bar room do this?") and structural predictability ("does my day-1 physics still
  forecast this?") moved in **opposite directions** over the same window. They are different
  axes, and the composed route composes exactly these two axes — which is why DL3b's failure
  lands where it does.

## DL3b — the 3.3% FAR question, answered with two faces

**Face 1 (the replication, positive):** composed FAR = 3/60 = 5.0% [1.7–13.7], vs 3.3% on
synthetic. Real data did **not** break the false-accept side. G3 SURVIVES (≤10%). Per family:
RATE / RANGE / BREADTH FAR_D = 0/15 each; SPLICE = 3/15 (20.0%). Every synthetic-style
corruption was rejected by every gated arm. JEV-only FAR was 16.7% — the composition still
beat the single judge gate (0.05 vs 0.167).

**Face 2 (the FRR break, negative, first-class):** composed FRR = 26.7% [17.1–39.0] vs 0%
synthetic. Decomposition: bar-rail valids armB-reject 63.3% (the stale kernel), roomd valids
20–27% — but composed D-reject was 0% (doctor-canary) and 6.7% (the-bridge). JEV rescued the
rooms where its confidence was high and uniform; on bar-rail its mid-range confidence
(0.5–0.65) let hard-residual rejects through the composition. The 14 giant-residual valid
transitions (residual 80–102, from the ill-conditioned lstsq kernel on a low-rank calibration
window) are genuine off-manifold states: presence/joke_landing/volume never moved in days 1–3
and moved thereafter.

**Post-hoc ridge variant (labeled, no new JEV calls):** LOO-λ=100 ridge kernel → FRR_D 26.7%
→ 20.0%, FAR_D unchanged 5.0%. Regularization helps but does not fix it: the drift is real
distribution shift, not only numeric pathology. G1 still fails (composition can't beat a
0.05-FAR single gate), G2 still fails vs JEV-only's 5% FRR.

**The three accepted invalids:** all SPLICE, all bar-rail cross-day — same room, wrong time,
modest deltas (e.g., earnestness 0.50→1.00). JEV rated them 0.62–0.75: within-room
time-transplants look like ordinary evolution. Cross-**room** transplants: 8/8 rejected by
everything. **The pinch catches room transplants, not time transplants.**

**Gate-drafting error disclosed:** PRE-REG H0b read "JEPA-only arm FAR on RATE+RANGE+BREADTH
≥ 0.5" — direction inverted (FAR counts *accepted* invalids; "seeing" corruptions means LOW
FAR; measured 0.0). The stated inline intent ("residual machinery must see the corruptions")
is satisfied trivially. The as-written INVALID_HARNESS verdict stands recorded; the
intent-literal recomputation is COMPOSED-FAIL (G1 0.05 > 0.035, G2 0.267 > 0.15). Neither
reading is a PASS; nothing here was silently flipped.

## DL3c — "room" vs "personality," answered structurally

Nights corpus (182 sessions, 10 roster compositions). Within-night transitions vs cross-night
splices at two roster distances:

| group | n | JEV noul mean | JEPA resid median | reject (D) |
|---|---|---|---|---|
| within-night (valid) | 30 | 0.544 | 0.431 | 6.7% |
| NEAR splice (same composition) | 15 | 0.356 | 0.786 | 40.0% |
| FAR splice (jd ≥ 0.5) | 15 | 0.351 | 1.069 | 53.3% |

- C1 (boundary encodes personality): diff 13.3 pts < 20-pt gate → **FAIL** (direction correct,
  CIs overlap).
- C2 (room-only null): NEAR−within = 33 pts → also FAIL. **MIXED.**
- **The decisive split:** JEV's noul cannot distinguish NEAR from FAR at all (0.356 vs 0.351,
  and armC rejects 93% of both). The personality gradient (residual median 0.43 → 0.79 → 1.07
  across within/near/far) lives entirely in the transition kernel's state-space geometry.
  **JEV reads the room; JEPA's manifold carries the personality.** The "boundary that moves as
  personalities change" is not JEV's semantic boundary — it is the geometry of whose field is
  evolving.
- C3 (booked): per-composition within-night noul means spread 0.395–0.617 (spread 0.22 ≫ pin
  noise 0.007) — different casts do sit differently on the judge's boundary, but with 3–6
  sessions per composition this is suggestive only, confounded with session state.

## What breaks, what holds (for CM1 / r7 promotion decision)

1. **Holds:** JEV stability over weeks (pin std 0.007); composed FAR on real data (5%);
   total rejection of synthetic-style corruptions (0/45 accepted); cross-room transplant
   detection (8/8); complementarity (33/120 JEV-vs-JEPA disagreements on real data).
2. **Breaks:** frozen-kernel FRR on drifting rooms (63% armB on bar-rail); G1's "composition
   beats best single" (JEPA-only already achieves FAR 5% — on real data the linear kernel is
   the stronger single gate for invalids, and composition adds nothing there); personality
   detection through JEV (blind); cross-day time-transplants (3/7 accepted).
3. **Actionable:** calibration windows must exercise every dial (bar-rail days 1–3 had three
   dead dims → rank-deficient kernel → 80+ residuals on later valids); kernels need rolling
   refit or drift monitors (DL3a's daily soft-exceed series is exactly that monitor); ridge,
   not lstsq, on low-rank dial windows; the r7 pinch candidate should ship with a residual
   **drift** channel, not just a residual threshold.

## Honest negatives ledger

- G1 failed on real data (composition ≤ best single, not < 0.7×).
- Composed FRR 26.7% (vs 0% synthetic) — the route is not deployable as-is on drifting rooms.
- JEV personality-blindness on splices (the lane's premise "boundary moves with personality"
  is false at the JEV layer; true only in kernel geometry).
- P3 drift-driver correlation p=0.09 — suggestive, not confirmed.
- C3 composition-level spread: underpowered.
- The PRE-REG H0b drafting error (recorded verbatim above).
