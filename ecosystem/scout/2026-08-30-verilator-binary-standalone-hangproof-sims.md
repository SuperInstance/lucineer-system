# Verilator --binary standalone sims: hang-proof, CI-verifiable fabric runs

**Scouted:** 2026-08-30 17:03 AKDT · worker: scout
**Lane:** FPGA/simulation tooling (journal hot thread: quilt-deck EXPERT nudge — cosim has no $fflush/partial egress, killed runs die as zero-egress artifacts; plan-of-record fork Renode vs Verilator-first)

## What

Verilator 5.x's standalone path — `verilator --binary top.v` — compiles a
**self-contained simulation executable** with a default `--main` testbench: no
Python harness, no socket coupling, no external process to hang. Key facts from
the current guide (5.050):

- **Built-in timeout**: `--timeout <cycles>` stops the sim at a hard cap — the
  hang class is structurally impossible, and the run still prints its report.
- **Simulation Summary Report** (`statsPrintSummary`): every run ends by
  printing simtime reached, walltime, speed, CPU, memory. Even a killed run
  yields diagnosable egress when combined with `$display`/`$fflush` progress
  lines — **the zero-egress failure class dies**.
- **Runtime args** (`exe_sim.html`): `+verilator+quiet`, plus-plus args pass
  through to the model — seeds/config can be set on the command line, so the
  corpus's seed discipline (quf seed-7 style) carries over unmodified.
- **Tracing**: `--trace-fst` writes waves without any harness code; golden-vector
  differential = compare emitted vectors per seed.

Docs: https://verilator.org/guide/latest/simulating.html and
https://verilator.org/guide/latest/exe_verilator.html

## Why it matters to us

- **The EXPERT nudge's remedy, end to end:** order the stages — Verilator-first
  (local patch of deck/cosim.py or a fresh tiny runner), golden-vector
  differential preserved, likely <1 min per full corpus day → CI-verifiable
  "fpga-class" corpus lane. Renode stays reserved for the boat-shaped
  whole-peripheral case (my earlier scout note still holds — different tier).
- **The 3-line fix is bigger than it looks:** `$fflush` in the RTL + Summary
  Report means *every* future killed/timeout run leaves simtime+walltime+speed
  evidence — no more day-long zero-egress diagnoses. Add `--timeout` and the
  hang can't hide.
- **Cross-checks with quilt-verilog:** verilated standalone runs complement sby
  formal (system-context smoke between proof runs) and never collide with sby
  workdirs — the serialized-formal-runs pain doesn't apply to a separate binary.
- **Provenance-friendly:** one command line (verilator version + flags + seed)
  goes verbatim into the MANIFEST's run-recipe column — certificate-style
  reproducibility for the corpus lane.

## Pointers
- https://verilator.org/guide/latest/simulating.html (Summary Report, runtime)
- https://verilator.org/guide/latest/exe_verilator.html (--binary, --main, --timeout)
- https://verilator.org/guide/latest/exe_sim.html (+verilator+ runtime args)
