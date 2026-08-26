# DUKE ROUND 3 — duke-lab-r3, 2026-08-25

Session: duke-lab-r3 / "Unheard Duke II" / C, 112 bpm, 4/4, **swing 66%**, 16 bars, @piano held by band-r3.
Artifacts: score.song, duke-lab-r3.mid, duke-lab-r3.wav (34.3 s), BUILD-JOURNAL.md (workspace root), parts/piano.song
Local copies: duke-lab/r3-score.song, r3-part.txt, r3_features.json, r3_render.json, r3_audit.json, r2_audit.json

## Method
- plainsong master (dynamics-and-swing merged; no perf-v1 branch exists) supplies Vel: rows, inline marks (!, @N), cresc/dim, and true long-short swing.
- MCP tool layer does not expose swing on ensemble_open; set swing 66% in the session manifest directly (round-trips through merge into the score header).
- GAN round 3: band pass (opencode/GLM-5.3, brief = R2 score + surviving critiques + new notation powers), then blind critic (same model, notation+features+MIDI evidence only, harsher), then perception_audit.

## R3 notation (full score in score.song)
Identical harmonic skeleton to R2 (same chords, register answers above C6, b5 late entry, b4/b12 pickups) — upgraded with:
- **A Vel: row under every @piano bar** — the arm changes weight inside bars: b1 climbs 84→cresc→88→92→98 then dims; b4 dips 72→68 before lifting to 86; b15 rises to 74 then falls to 54; b16 settles 52→48→40 into the lone C6.
- **Bar 7 displaced**: the Gb7 planing moved one slot later (and-of-2, slot 4 of 8), accented 96; A5 answer at 90.
- **Bar 12 pickup**: G3-B3 moved to the last slot (and-of-4), accented 86, leaning into b13's 92.
- Header: `swing: 66%`.

## Critic verdict (VERBATIM)
> VERDICT: CONVERGED: Duke?
>
> The arm finally changes weight inside bars: every Vel row moves 10–20 units mid-bar (bar 1 climbs 84→98 then dims, bar 4 dips 72→68 before lifting to 86, bar 15 rises to 74 then drops to 54), per-bar velstd spans 0.13–0.26, and the MIDI's 37–105 spread across 116 notes confirms no bar is one weight. The square landings are dead — bar 7 now side-slips Fm7→Gb7→G7 in half steps (sync 0.69, vel 80→96→88→90) and bar 12 descends Dm11→Db7, a tritone-sub slide, with the B4 answer and G3-B3 pickup into bar 13's C2 that lands heavy at 92 and dims to 80. The render swings: offbeats breathe across 0.66–0.89 with early pushes at 0.144–0.333 around the nominal 66% grid — laid-back, not lifeless — and the 34.3 s render is exactly 64 beats, clean compile. No new wound of the same rank: contours rotate between ramps (1, 5), swells (2, 9, 11), dip-rises (4, 12), and falls (6, 13, 16) rather than one mechanical ramp, and the displacement left the harmony intact — four-note stacks in bars 7, 11, 12, with bar 6's three-note Eb6-D6-B5 echo at 60→48 thin by design.

## Numbers vs R2 (means)
| feature | R2 | R3 |
|---|---|---|
| velocity_std | 0.113 | **0.200** |
| dynamic_range | 0.080 | **0.149** |
| syncopation | 0.355 | **0.410** |
| rhythmic_complexity | 0.210 | **0.272** |
| velocity_mean | 0.559 | 0.557 (level held) |

Per-bar: b7 sync 0.00 → **0.69**, velstd 0.13 → 0.18; b12 sync 0.00 → **0.18**; b1 velstd 0.13 → 0.20; b16 velstd 0.14 → 0.20 (ending exhales).

## Swing evidence (measured from the rendered MIDI, ppq 480)
Intra-beat onset positions: 0.144, 0.223, 0.285, 0.333, **0.66**, 0.715, 0.777, 0.856, 0.89.
Straight eighths would sit at 0.5; the 66% long-short pair puts the offbeat at **0.66** — observed. Velocities 37–105 across 116 notes.

## perception_audit — one dial or two?
- R2 (duke-lab): 16 channels → **15 steering dimensions**; `[['dynamic_range', 'velocity_std']]` coupled above |r|>0.9; velocity_std & dynamic_range both verdict COUPLED. Dynamics was ONE dial.
- R3 (duke-lab-r3): 16 channels → **16 steering dimensions**; 0 dead, 0 coupled; velocity_std (std 0.037) and dynamic_range independent. **Dynamics is TWO dials now.**

## Convergence
All three surviving R2 critiques are dead: intra-bar weight (velstd doubled), bars 7/12 unsquared (sync 0.69/0.18), render swings (0.66 offbeats). Critic returned **CONVERGED: Duke?** on its own standards, finding no new wound of the same rank. The lab's question — "can the notation carry a body, not just a vocabulary?" — is answered yes for dynamics and swing.
