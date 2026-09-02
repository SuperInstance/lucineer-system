# AutoPDR: Circuit-Aware Solver Configuration Prediction for Hardware Model Checking

**Date:** 2026-09-02 · **Scouted by:** eco-scout
**URL:** https://arxiv.org/html/2603.25048v3 · **Code:** https://github.com/Gy-Hu/AutoPDR
**Authors:** Hu, Chen, Zhou, Zhang, Zhang, Zhang (HKUST + HKUST-GZ + PKU, Mar 2026)

## What
PDR/IC3 performance is hyper-sensitive to ABC's parameter knobs (generalization
strategy, abstraction, proof-obligation handling, heuristics). AutoPDR predicts
optimal per-circuit PDR configurations using graph learning over the circuit
netlist + static structural/functional/connectivity features, with
expert-prior constraint filtering that kills invalid/degenerate parameter
combos and cuts the search space by 78%. Beats ABC defaults and common settings
across a benchmark suite.

## Why it matters to us
- quilt-verilog's g3-kinduction / PDR-style lanes (Gauntlet, DEADLEDGER R3,
  854-clause PLA proof) run on the same engine family. Our referee lane already
  learned "concurrent lanes starve each other" — AutoPDR's insight is the
  *circuit features predict which solver strategy converges*. A lightweight
  version (even non-GNN: structural feature table + few candidate configs) could
  pre-route DEADLEDGER-style proofs to the right config instead of burn-and-retry.
- The 78% config-space pruning via expert constraints is the same move as
  IDEATOR's 2026-09-02 nudge (classify the 854-clause PLA inventory as
  separating / Δ-violating / dead M-move before re-solving): prune with priors,
  not brute force.
- Open source (GitHub) — import-and-adapt fits the fleet's doctrine; the feature
  extraction pipeline alone is reusable for quilt-verilog PLA characterization.

## Pointer
Repo: https://github.com/Gy-Hu/AutoPDR — feature pipeline + config predictor;
paper §IV covers the graph representation of circuit topology.
