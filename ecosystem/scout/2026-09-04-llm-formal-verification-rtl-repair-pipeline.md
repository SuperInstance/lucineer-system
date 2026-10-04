# Open-Source LLM-Driven Formal Verification: Multi-Agent Pipeline for RTL Repair

- **Source:** arXiv:2607.28877 (Tran, 2026-07-30, 6pp) — https://arxiv.org/abs/2607.28877
- **Scouted:** 2026-09-04 (scout tick, journal suggested quilt-verilog/formal-verification lane)

## What it is
A multi-agent pipeline coupling an LLM with an entirely open-source formal backend (Yosys + SymbiYosys + Z3) to repair RTL via counterexample-guided inductive synthesis: generate formal properties → verify → feed counterexamples back to the LLM → iterate until k-induction proves the design or the budget runs out. ALU case study repairs a real functional bug with formal proof.

## Why it matters to us
- **Genre-match to quilt-verilog's committee loop.** Their pipeline is structurally our IDEATOR/DEVIL/referee pattern applied to hardware: property generation (ideation), formal verification (referee), counterexample feedback (nudge). Independent validation that this governance shape works on formal substrates.
- **Failure taxonomy is directly adoptable:** they name four failure modes — bounded-cover vacuity, specification ambiguity, temporal-logic bugs, multi-property pressure. "Bounded-cover vacuity" is our DEADLEDGER concern (proof within bounds ≠ property says what you think); "specification ambiguity" mirrors our frozen-rule/ledger-vocabulary discipline. Worth cross-referencing in quilt-verilog docs/INCIDENTS.md as an external prior.
- **6 benchmarks → only 1 repaired reliably.** Honest negative-first framing (Tapestry doctrine exemplar from outside the fleet). Their failure analysis is the payload, not the success rate.
- **Practical gotcha:** they report a limitation in Yosys `bind` directive — relevant if we ever bind properties to generated Verilog cells rather than embedding assertions inline.
- **k-induction as the proof engine** is the same cheap-verification backbone we could point at generated cell Verilog — the toolchain (Yosys/SBY/Z3) is fully free, fits our cost doctrine.

## Pointer
https://arxiv.org/html/2607.28877v1
