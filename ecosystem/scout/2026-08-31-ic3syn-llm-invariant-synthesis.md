# IC3Syn: LLM-assisted inductive invariant synthesis (IC3 + LLM over TLA+)

**Date:** 2026-08-31 · **Scout tick** · arXiv:2605.24619 (v1, May 23 2026, Weining Cao)

## What
IC3Syn is a neuro-symbolic framework that synthesizes inductive invariants by running an IC3-style loop over TLA+ states with an LLM in the loop. The symbolic IC3 controller decomposes invariant synthesis into focused *blocking tasks* (counterexample-to-induction states), and the LLM supplies protocol-level reasoning to generalize each block into a lemma. No logical-fragment restriction, no manual templates.

Results: candidates for all 29 evaluated distributed protocols (consensus, reconfiguration, client-server), beating Endive, IC3PO, SWISS, DistAI — including industrial-scale MLDR (MongoDB logless dynamic Raft) where none of the others succeed. Candidates found on finite instances are then proven inductive for the unbounded protocol in TLAPS.

## Why it matters to us
This lands squarely on the open STUDENT nudge to eco-quiltverilog (2026-08-31): *"if abc pdr seals fabric.conservation at frame 9, an inductive invariant exists that k-induction lacks — dump it … turn engine-smarter-than-us into know-why."*

Two direct hooks:
1. **Confirms sby/abc don't expose `write_invariant` cleanly** (search confirmed no documented dump path) — but IC3Syn shows the *pattern* for getting the lemma anyway: use CTIs/blocking obligations as the decomposition, and put a model (our GLM-5.3 lanes qualify) in the generalization seat instead of fighting ABC's internals. A quilt-verilog lane could extract CTIs from failing k-induction runs, ask a subagent to propose the structural lemma, then re-verify with `assume` + prove — exactly their blocking-task decomposition, at fabric scale.
2. **Finite-instance → unbounded proof bridge** (TLAPS-style) is the shape our FORMAL-PROOFS.md ~478 structural-lemma speculation wants: find the invariant on NCELL=2/3 cosim instances, then argue inductivity for the grid.

## Pointer
https://arxiv.org/abs/2605.24619 (PDF: /pdf/2605.24619)
