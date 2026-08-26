# THE DUKE EXPERIMENT — duke-lab session, 2026-08-25

Session: duke-lab / "Unheard Duke" / C, 112 bpm, 4/4, 16 bars, voice @piano held by band-glm.
Artifacts (MCP workspace): score.song, duke-lab.mid, duke-lab.wav, BUILD-JOURNAL.md
Local copies: duke-lab/final-score.song, r1_features.json, r2_features.json, r2_render.json

## R1 notation (before)
@piano | C3-G3-D4 . E4 G4 (rest) C5 . . | Db3-Ab3-Eb4 . F4 Ab4 (rest) Db5 G4 . | A2-E3-G3-D4 . . G4 . F4 E4 . | G2-F3-B3-E4 . A4 . B4 (rest) (rest) (rest) |
@piano | C3-G3-D4 . E4 G4 (rest) C5 . . | C3-G3-D4 . Eb5 . D5 B4 (rest) . | F3-Ab3-C4-E4 . Gb3-B3-Db4-F4 . G3-B3-D4-F4 . A4 . | G2-F3-Ab3-B3 (rest) (rest) D5 (rest) (rest) (rest) (rest) |
@piano | Db4-F4-Ab4-C5 . . . Eb5 Db5 C5 Ab4 | E3-G#3-B3-D5 . . D5 C5 . B4 . | A2-G3-B3-E4 . . C#4-E4-G4-B4 . A4 . . | D3-F3-C4-E4 . Db3-F3-Ab3-B3 . . B4 (rest) . |
@piano | C2-G2-D3 . E3 G3 (rest) C3 . . | Db3-Ab3-Eb4 (rest) (rest) G3-B3-F4 (rest) (rest) (rest) (rest) | C3-G3-Eb4 . D4 . Eb5 D5 B4 (rest) | C2-G2 . . B3-D4-E4-A4 . . . . |

## R2 notation (after) — see final-score.song; identical harmonic skeleton + per-bar vel 50–95,
## answers displaced above C6 (b2 F5-Ab5-Db6, b6 Eb6-D6-B5, b9 Eb6-Db6-C6, b15 Eb6-D6, b16 lone C6),
## b5 late entry, pickups b4 (D4-E4) & b12 (G3-B3).

## Critic verdict 1 (verbatim)
"Not Duke — because the arm never changes weight and the hand never leaves the middle register: it is Duke's vocabulary played with a conservatory body."

## Critic verdict 2 (verbatim)
"Closer — the arm now arcs between bars, the answers sparkle above C6, and the second A is its own sentence. Still not Duke — because inside each bar the arm is one weight, bars 7 and 12 land square, and this render cannot swing."

## Feature deltas R1 -> R2 (means)
syncopation 0.269 -> 0.355 | treble_activity 0.000 -> 0.084 | interval_size 0.440 -> 0.481
register_spread 0.185 -> 0.209 | velocity_mean 0.599 -> 0.559
UNMOVED: velocity_std 0.109 -> 0.113, dynamic_range 0.076 -> 0.080 (intra-bar wall)
Per-bar: b5 sync 0.33 -> 0.67; b6 sync 1.00, treble 0.67; b16 velmean 0.40 = quietest bar; b8/b13 velmean 0.74.

## Verdict: NOT CONVERGED — honest gap declared. Best take = version 4.
Next gradient recorded in BUILD-JOURNAL.md (displace b7 planing, b12 pickup to and-of-4;
intra-bar dynamics + swing inexpressible from the voice).
