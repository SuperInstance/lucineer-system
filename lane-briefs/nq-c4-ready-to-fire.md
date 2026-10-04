# READY-TO-FIRE LANE BRIEF — NQ-C4 (drafted by Lucineer on Casey's "go further", 20:02 AKDT 2026-09-03)

**Status: staged. Dispatch when a lane slot frees / toolset allows exec.**

## NQ-C4 — THE THRESHOLD/LEAK SWEEP (son of the metal spike)
Workspace /home/eileen/projects/quilt-verilog, branch g3-kinduction (stash→pull --rebase→pop; never force-push). Context: NQ-C3 PASS (5690e768 in ai-writings; artifacts docs/nq-c3-metal/) — worm touch-arc compiles to Verilog, iverilog == Python byte-for-byte on 3 traces. Corpse finding to interrogate: under TH=strongest-in + half-leak the arc extinguishes at the first synapse. The gate was equivalence, not worm behavior — so WHAT threshold/leak regime lets the arc propagate like the animal?

DELIVERABLES (pre-registration committed FIRST, in ai-writings docs/nq-c4-threshold-leak/ then run, then results, separate commits):
1. Sweep TH ∈ {strongest-in, top-2-in, sum-in ≥ k (k ∈ {2,3,5,10})} × leak ∈ {0, 0.25, 0.5, 0.9} on the SAME 7-cell arc with the SAME verbatim cached weights (hash-asserted against NQ-C1 booking; no re-download).
2. For each (TH, leak): does the spike reach DB (motor) within 100 ticks on a suprathreshold AVM tap? Report propagation reach + latency. Emit Verilog for EVERY surviving regime and bit-exact-check iverilog vs Python on ONE fixed trace each (reuse tb_worm_arc.v pattern).
3. Pre-registered reading: if NO regime propagates → the arc as-wired is not a relay at any linear-threshold regime; book "touch arc needs modulatory state" and the NQ-C5 candidate becomes gap-junction-augmented (FlyWire-style EJ edges — the worm has them; NQ-C2 showed 50.6% intra-cluster). If ≥3 regimes propagate → sensitivity is the finding: biology is degenerate, hardware must encode the WHOLE regime family, book the regime-vector as the cell parameter that matters.
4. Canaries: iverilog == Python on all emitted regimes (hard gate, byte-exact); T1 trace of NQ-C3 must replay identically; no float in-loop.
5. House style: verdict up front, scars booked before running, 30-min cap, work incrementally.

Bridge verification (Lucineer): re-run one regime end-to-end personally; diff traces digit-for-digit.
