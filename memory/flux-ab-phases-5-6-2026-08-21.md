# FLUX A/B Reconciliation — Phases 5 & 6 (docs + cutover) — 2026-08-21

**Branch:** reconcile/isa-unified-interpreter (PR #28) · **Suite: 2740 passed** (2739 at Phase 4 end, +1)

## Phase 5 — Docs
- `docs/RECONCILIATION.md` (6.3 KB) — the full timeline: Phase 1 interpreter path → 2 toolchain → 3 conformance vectors → 4 dual-mode tests → 5 docs → 6 cutover, with landmine resolutions (JZ=Format F, imm16 BE) and the pre-existing bugs found (LOOP back-offset, BCAST rs1 aliasing).
- `docs/OPCODE-RECONCILIATION.md` (32.8 KB) — the detailed opcode-by-opcode A/B mapping table.
- `isa_unified.py` header rewritten: module = System B (canonical); System A = opcodes.py, preserved byte-for-byte, selectable via `Interpreter(isa="system_a")`; corrections documented.

## Phase 6 — Cutover
- **Interpreter default flipped: `isa: str = "unified"`** (was "system_a"). All dispatch now goes through the converged System B table by default.
- **System A preserved**: `Interpreter(isa="system_a")` still selects the legacy table for byte-for-byte compat with pre-cutover bytecode. No mapping deleted.
- Examples (01_hello_world, 05_bytecode_playground, flux_fleet_calc/sim/flowchart), retro implementations, tracer, profiler, repl, CLI, debugger, pipeline/e2e all updated to the unified default.
- **Full suite: 2740 passed** (cutover validated BEFORE commit — never merge red).

## State
Phases 1–6 COMPLETE. PR #28 holds the full reconciliation. System B is canonical; System A is a preserved legacy mode. The fleet's A2A bytecode now executes correctly (TELL→A2A dispatch, not VLOAD).
