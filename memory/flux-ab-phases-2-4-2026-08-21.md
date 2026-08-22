# FLUX A/B Reconciliation — Phases 2–4 Executed (2026-08-21)

**Executor:** subagent (FLUX A/B phases 2–4) · **Repo:** `/home/eileen/projects/flux-runtime`
**Branch:** `reconcile/isa-unified-interpreter` (PR #28, OPEN) · Continues `memory/flux-ab-truth-2026-08-21.md` + `memory/flux-ab-plan-2026-08-21.md`

## Commits (all pushed to PR #28)

| Phase | SHA | Summary |
|-------|-----|---------|
| 1 (prior) | `802bead` | unified interpreter path + selector (2676 tests) |
| 2 | `5849eb4` | toolchain System B modes + 3 spec landmines resolved (2695) |
| 3 | `3641715` | dual-mode executable conformance, compiler-side semantics (2721) |
| 4 | `4473413` | dual-mode equivalence suite + legacy annotations (2739) |

Full suite final: **2739 passed** (was 2676 at start).

## The three landmines — resolutions

1. **JZ = Format F (op, rd, imm16), NOT Format E.** Evidence: signal_compiler
   back-patches a big-endian imm16 (parallel to JMP 0x43 F); asm-text vectors use
   two-operand `JNZ R2, done`; no concrete JZ vector contradicts. Fixed:
   `isa_unified.py:171-174` (spec relabeled F + comment), `interpreter.py`
   `_step_unified` JZ/JNZ/JLT/JGT now decode `rd + _fetch_i16_be`.
2. **imm16 = BIG-endian in System B.** Compiler `_emit_format_f` + MOVI16 vector
   `[0x40, rd, 0x10, 0x00]`=4096 + formats.py all agreed; spec header's
   "little-endian" claim was wrong — corrected in `isa_unified.py` header.
   Cross-assembler unified target packs BE; System A mode stays LE, unchanged.
3. **A2A registers now populated.** Converged spec (TELL "Send rs2 to agent rs1,
   tag rd"; ASK "resp→rd") requires operand registers to carry values.
   signal_compiler loads tag/agent/data before each A2A op (names interned via
   `zlib.crc32 & 0x7FFF`); BCAST's rs1 = never-loaded reg (agent field 0 =
   fleet); `_dispatch_a2a(..., rd=rd)` writes ASK responses to rd (System A
   R0 convention preserved when rd=None).

## Phase 2 toolchain changes

- `SignalCompiler(isa="unified")` default (historical emission preserved);
  "system_b" alias; "system_a" rejected (Signal is System B-native — no
  invented Format-G mapping).
- `CrossAssembler(target="system_a"|"unified")`; `opcodes_compat.UNIFIED_OPCODE_DEFS`
  derived from `build_unified_isa()` (258 mnemonics + aliases); unified emitters
  for formats A–G with BE imm16 + PC-relative jumps.

## Bugs found & fixed during phases

- **LOOP off-by-instruction-size** (pre-existing, invisible until a VM-executed
  vector existed): `_compile_loop` omitted the +4 in the back-offset → body ran
  once regardless of count. Caught by Phase 3 loop vector, fixed in 3641715.
- **BCAST agent-field aliasing**: rs1=0 pointed at R0 (which holds the tag) →
  payload agent field leaked the tag id. Now rs1 = dedicated zero register.

## Phase 4 annotations (retained-as-is rule)

Annotated with pointers to unified equivalents: `tests/conftest.py`,
`test_vm.py`, `test_vm_complete.py`, `test_cross_assembler.py`,
`test_formats.py`, `test_debugger.py`, `test_security.py`,
`test_bytecode_verifier.py`. New unified twins:
`tests/test_toolchain_unified.py` (19), `test_dual_mode_equivalence.py` (18),
extended `test_conformance_unified.py` (+26).

## Remaining (Phases 5–6, NOT executed)

Phase 5 (docs: `OPCODE-TABLE-RECONCILED.md`, mark old doc superseded) and
Phase 6 (cutover: flip default to unified + tag `pre-isa-cutover`) are
untouched. PR #28 still OPEN on `main` @ `20afa5e`.
