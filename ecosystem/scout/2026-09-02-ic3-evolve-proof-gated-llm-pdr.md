# IC3-Evolve: Proof-/Witness-Gated Offline LLM Heuristic Evolution for IC3

**Date:** 2026-09-02 · **Scouted by:** eco-scout
**URL:** https://arxiv.org/abs/2604.03232 (IJCAI 2026; HKUST, Hongce Zhang group — same lab as AutoPDR)
**Authors:** Miao, Hu, Yang, Zhang

## What
IC3/PDR performance is dominated by a web of interacting heuristics. IC3-Evolve
lets an LLM propose small, slot-restricted, auditable patches to an IC3
implementation — offline code evolution, not runtime LLM use. The gate is the
interesting part: **every candidate patch must pass proof-/witness-gated
validation** — SAFE runs must emit an independently-checked inductive-invariant
certificate; UNSAFE runs must emit a replayable counterexample trace. Unsound
edits can't deploy. Evolved on HWMCC benchmarks, generalizes to unseen public +
industrial benchmarks; the deployed artifact is a standalone checker with zero
ML runtime dependency.

## Why it matters to us
- **This is the model-arena / Variety-Ledger ratchet pattern applied to a
  solver.** "Advance only after held-out survival" (quilt-verilog's DEVIL
  confirmed ratchet, 2c92bfb) is structurally the same doctrine as
  certificate-gated evolution: the LLM proposes, an independent checker
  disposes. Cross-validation of our doctrine from an external group — and a
  vocabulary upgrade (proof-gate / witness-gate) worth adopting in VARIETY-LEDGER
  naming.
- **Directly useful for the sby/PDR lanes.** cell_core.tick liveness PASS took
  747s at depth 130 (c1f5a73); G2 ring-wide instantiation at NCELL 2/4/8 will
  multiply that. An evolved ABC/avy PDR config (even just harvesting their
  evolved heuristic patches) could cut ring-wide proof time materially.
- **Certificate discipline matches the EXPERT nudge**: demanding the exact PDR
  termination line (inductive invariant vs no-CEX≤130) is exactly their
  SAFE-must-emit-checkable-certificate gate. Their independent-checker framing
  is the answer to "trust-Python vs tie-breaker" class problems.

## Pointer
https://arxiv.org/abs/2604.03232 · same group: AutoPDR (arXiv:2603.25048,
scouted 2026-09-02) — config prediction vs code evolution, complementary.
