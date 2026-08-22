# FLUX System A→B Reconciliation Plan (Phases 1-6, verified)

**Author:** subagent (FLUX opcode A/B reconciliation)
**Date:** 2026-08-21
**Repo:** `SuperInstance/flux-runtime`
**Source of truth for targets:** `src/flux/bytecode/isa_unified.py` (System B)
**Companion truth doc:** `memory/flux-ab-truth-2026-08-21.md`

---

## 0. Guiding constraints (hard rules from task)

1. **Never break a green test.** Baseline: **2651 passed** on `main` @ `20afa5e`.
   Every committed step must leave `pytest tests/` green.
2. **Never delete an opcode mapping.** Both systems' tables are preserved and
   annotated. System A lives in `opcodes.py`; System B in `isa_unified.py` (and
   a new `opcodes_unified.py` IntEnum mirror). The migration **adds** the
   unified path and only flips the *default* at the final cutover.
3. **Small committed steps** — a crash must never lose more than one coherent,
   green commit.
4. **Check for foreign activity** — done (truth doc §8): no active agent on the
   migration; only 2 stale dependabot PRs. Proceeding.

---

## 1. One-way convergence strategy

Converge on **System B** (`isa_unified.py`) as the single canonical numbering.
Because a single byte cannot mean two things in one dispatch, the transition is
done with an explicit **ISA selector** on the interpreter (and later the
encoder/assembler):

- `isa="system_a"` (default) — legacy System A, unchanged, keeps all 2651 tests
  and all deployed bytecode green during transition.
- `isa="unified"` — System B, the converged target.

The final phase flips the default to `"unified"` (one-way converge) after all
consumers are migrated, with a tagged rollback point.

Both systems' tables are **preserved in docs** (`docs/` gets a reconciled
side-by-side table; `opcodes.py` keeps System A; `opcodes_unified.py` documents
System B alongside it).

---

## 2. Phase 1 — Interpreter (EXECUTED NOW, this pass)

**Goal:** make the interpreter able to *correctly execute* unified (System B)
bytecode, without disturbing System A.

**Changes:**
1. New `src/flux/bytecode/opcodes_unified.py` — `UnifiedOp(IntEnum)` generated
   from `isa_unified.py`'s `build_unified_isa()` (single source of truth), plus
   a format table. This is the "System B annotated" artifact.
2. `src/flux/vm/interpreter.py`:
   - `__init__(..., isa: str = "system_a")`; normalize `"system_b"/"unified"` →
     `"unified"`; store `self.isa`.
   - Add `_step_unified()` implementing System B dispatch, and route `_step()`
     to it when `self.isa == "unified"` (single entry point, so `execute()`,
     debugger, tracer all honor the selector).
   - System B formats (NOT identical to System A): HALT/NOP/RET Format A;
     INC/DEC/NOT/NEG/PUSH/POP Format B; MOVI `0x18` Format D (3-byte imm8);
     MOVI16 `0x40` Format F (4-byte imm16); arithmetic/compare/memory/move/
     branch `0x20-0x3F` Format E; JMP/CALL/LOOP Format F; A2A `0x50-0x5F`
     Format E (register triple → A2A handler); C_THRESH `0x69` Format D.
   - Unimplemented reserved/extended ranges raise `VMInvalidOpcodeError` with a
     clear "not implemented in unified mode" message (no silent wrong op).
3. New `tests/test_conformance_unified.py`:
   - Executes every concrete `TEST_VECTORS` entry from `test_conformance.py`
     through `Interpreter(bytes, isa="unified")` and asserts the expected
     register values (this is the missing P0 Signal/VM conformance gate).
   - End-to-end: compile a Signal A2A program → run through `isa="unified"` →
     assert TELL/ASK/BCAST dispatch to the A2A handler (kills the TELL→VLOAD
     bug with a regression test).
   - Assert System A default is unchanged (legacy path still intact).

**Acceptance:** `pytest tests/` green (2651 + new tests); conformance vectors
pass in unified mode; no System A bytecode regressed.

**Commit + push** to a branch and open a PR (or push to `main` if allowed) —
see §7.

---

## 3. Phase 2 — Compiler & toolchain alignment

**Goal:** the whole toolchain round-trips System B.

- `src/flux/bytecode/encoder.py` / `decoder.py` / `disasm.py`: add a System B
  mode (mirror `UnifiedOp` + unified formats) so encode→decode→execute is
  consistent in unified mode. Keep System A mode default.
- `src/flux/asm/cross_assembler.py` + `opcodes_compat.py`: add a unified-target
  mnemonic table (mnemonics `ADD/SUB/MUL/...` already alias; map them to System
  B values when `--target unified`).
- `signal_compiler.py`: already emits System B — verify its output now executes
  on `isa="unified"` (covered by the Phase 1 end-to-end test) and mark it as
  the canonical A2A compiler.

**Acceptance:** round-trip tests green for both ISAs.

---

## 4. Phase 3 — Conformance vectors

- Convert `tests/test_conformance.py` from a data-only file into an executable,
  **dual-mode** suite: `run_conformance_tests(runner)` wired to both the System
  A (legacy expectations, annotated) and System B (unified) interpreters.
- Fix any remaining wrong vector (e.g. the historical INC/DEC/PUSH third-
  numbering was already corrected in `main`; re-audit for stragglers).
- Add coverage for the A2A range (currently zero conformance vectors touch
  `0x50-0x5F`).

**Acceptance:** conformance suite is executable and green in both modes; A2A
vectors present.

---

## 5. Phase 4 — Tests (migrate System A bytecode)

- The ~2651 tests, retro games, and examples hard-code System A byte values.
  Migrate them to run under the correct ISA selector (`isa="system_a"` until the
  cutover, then `isa="unified"`). Prefer semantic assertions over raw hex so
  the same test can run in both modes.
- Keep green at every sub-step.

**Acceptance:** full suite green; no raw System A hex in tests except where
  explicitly testing legacy decoding.

---

## 6. Phase 5 — Docs (single reconciled table, both preserved)

- Add `docs/OPCODE-TABLE-RECONCILED.md`: side-by-side System A ↔ System B ↔
  mnemonic table for all 256 slots, with the System A column marked "legacy".
- Mark `docs/OPCODE-RECONCILIATION.md` as superseded by the executed migration
  (keep it for history — archive by rename, not delete).
- `docs/ISA_UNIFIED.md` becomes the canonical reference; `opcodes.py` gets a
  header note pointing at `opcodes_unified.py` for System B.

---

## 7. Phase 6 — Cutover (one-way converge) + rollback

- Flip the interpreter default `isa` to `"unified"` (and encoder/assembler
  defaults) — the actual one-way convergence.
- Tag the pre-cutover state: `git tag pre-isa-cutover` (and
  `pre-opcode-reconciliation` at the start of Phase 1).
- **Rollback path:** revert default to `"system_a"` (one-line) or `git revert`
  the cutover commit; System A table is never deleted, so legacy bytecode
  remains executable indefinitely.

**Acceptance:** full suite green on unified default; legacy mode still green;
  rollback documented and tested.

---

## 8. Risk & rollback summary

| Phase | Risk | Rollback |
|-------|------|----------|
| 1 (now) | LOW — additive, opt-in | remove `isa="unified"` usage; System A untouched |
| 2 | MED | keep System A default until green |
| 3 | LOW | revert vector wiring |
| 4 | MED | migrate per-file, keep green |
| 5 | LOW | docs-only |
| 6 | HIGH | `git tag pre-isa-cutover`; revert default |

Every phase lands as its own green commit; `quilt` is not touched; no opcode
mapping is ever deleted.

---

## 9. Estimated remaining effort

Phases 2-6 ≈ the reconciliation doc's ~20h estimate, now reduced by the Phase 1
foundation (ISA selector + unified dispatch + executable conformance gate).
The single highest-value follow-up is Phase 6's cutover + Phase 3's A2A
conformance coverage, which together retire issue #7.
