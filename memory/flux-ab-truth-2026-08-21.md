# FLUX System A/B Divergence — Verified Truth (2026-08-21)

**Verifier:** subagent (FLUX opcode A/B reconciliation, retry 2)
**Repo under test:** `SuperInstance/flux-runtime` — local clone at
`/home/eileen/projects/flux-runtime`, `main` @ `20afa5e`, working tree clean,
up to date with `origin/main`.

**Note on the stated clone path:** the task said clones live at
`/tmp/opcode-research/repos/` (18 repos). That directory was **wiped by the
gateway restart** and no longer exists. A live, clean clone of the one repo
Phase 1 targets (`flux-runtime`) exists at `/home/eileen/projects/flux-runtime`
and was used instead. No re-clone was performed; `flux-cross-assembler` is also
present locally. The other 16 repos were audited read-only via the existing
`memory/opcode-ecosystem-map-2026-08-21.md` + `memory/opcode-live-work-2026-08-21.md`
findings (both are current as of today).

---

## 1. Bottom line — the divergence is real and still live

`flux-runtime` contains **two mutually incompatible opcode numberings**, exactly
as the in-repo `docs/OPCODE-RECONCILIATION.md` (dated 2026-04-12) concluded, and
it has **drifted further** since that doc was written. Confirmed against current
`main` source, not READMEs:

| System | File | Role | HALT | TELL | VLOAD | MOV | ADD |
|--------|------|------|------|------|-------|-----|-----|
| **A** (live) | `src/flux/bytecode/opcodes.py` | imported by interpreter, encoder, decoder, validator, disassembler, debugger, retro games | `0x80` | `0x60` | `0x50` | `0x01` | `0x08` (IADD) |
| **B** (spec) | `src/flux/bytecode/isa_unified.py` | converged 3-agent spec; imported by **nothing** in `src/` | `0x00` | `0x50` | `0xB0` | `0x3A` | `0x20` (ADD) |

**System A** is what the interpreter actually dispatches on (`Op.*` from
`opcodes.py`). **System B** is what `signal_compiler.py` emits (hard-coded hex)
and what `tests/test_conformance.py` asserts.

**The fatal path is confirmed at the code level:**

```
Signal JSON → signal_compiler.py: `_emit_format_e(0x50, rd, rs1, rs2)`   # TELL (System B)
    → byte 0x50
        → interpreter.py `_step()`: `if opcode_byte == Op.VLOAD:`          # Op.VLOAD = 0x50 (System A)
            → SIMD vector load, NOT an A2A send
```

Every A2A opcode emitted by the signal compiler mis-executes. `TELL (0x50)` is
decoded as `VLOAD`, `ASK (0x51)` as `VSTORE`, `DELEG (0x52)` as `VADD`,
`BCAST (0x53)` as `VSUB`.

---

## 2. System A — `src/flux/bytecode/opcodes.py` (261 lines) — LIVE

Class `Op(IntEnum)`, "Variable-length encoding (1-8 bytes)". Key values (line
numbers from current `main`):

| Mnemonic | Value | Line |
|----------|-------|------|
| NOP | `0x00` | 10 |
| MOV | `0x01` | 11 |
| LOAD | `0x02` | 12 |
| STORE | `0x03` | 13 |
| IADD | `0x08` | 20 |
| PUSH | `0x20` | 50 |
| RET | `0x28` | 60 |
| MOVI | `0x2B` | 63 |
| VLOAD | `0x50` | 107 |
| VSTORE | `0x51` | 108 |
| VADD | `0x52` | 109 |
| VSUB | `0x53` | 110 |
| TELL | `0x60` | 117 |
| ASK | `0x61` | 118 |
| BROADCAST | `0x66` | 123 |
| CONF / MERGE / RESTORE (ISA v3 meta) | `0x3D` / `0x3E` / `0x3F` | 150-152 |
| HALT | `0x80` | 155 |
| YIELD | `0x81` | 156 |
| PHY_ABSORB (marine physics) | `0xB0` | 162 |

Format classes (lines ~169-230): A2A ops are **Format G** (variable,
`[op][len:u16][data]`); MOV/LOAD/STORE are **Format C** (3-byte); IADD/ISUB/etc
are **Format E** (4-byte ternary); JMP/JZ/JNZ/MOVI/CALL are **Format D**
(4-byte, reg + i16 offset).

### System A has drifted past the April doc
Two ISA-v3 additions were made **after** `OPCODE-RECONCILIATION.md` and create
**new collisions with System B**:

1. **Meta ops `CONF/MERGE/RESTORE` at `0x3D/0x3E/0x3F`** (opcodes.py:150-152,
   interpreter.py:1036/1039/1058). In System B, `0x3C/0x3D/0x3E/0x3F` are
   `JZ/JNZ/JLT/JGT`.
2. **Marine physics `PHY_*` at `0xB0-0xB8`** (opcodes.py:162-169, interpreter.py
   PHY_ABSORB..PHY_REFRAC handlers, added ~2026-07 commits `913d240`/`3c0fb5e`).
   In System B, `0xB0-0xBF` are the **SIMD vector** ops (`VLOAD/VSTORE/VADD/…`).

So the drift is strictly worse than the reconciliation doc recorded.

---

## 3. System B — `src/flux/bytecode/isa_unified.py` (462 lines) — SPEC ONLY

`build_unified_isa()` returns 256 `OpcodeDef` entries ("~200 defined, ~56
reserved"). Key values (line numbers from current `main`):

| Mnemonic | Value | Fmt | Line |
|----------|-------|-----|------|
| HALT | `0x00` | A | 87 |
| NOP | `0x01` | A | 88 |
| RET | `0x02` | A | 89 |
| INC | `0x08` | B | 103 |
| DEC | `0x09` | B | 104 |
| PUSH | `0x0C` | B | 107 |
| POP | `0x0D` | B | 108 |
| MOVI | `0x18` | D (`rd, imm8`, 3 bytes) | 127 |
| ADD | `0x20` | E | 139 |
| SUB/MUL/DIV/MOD/AND/OR/XOR | `0x21`-`0x27` | E | 140-146 |
| CMP_EQ/LT/GT/NE | `0x2C`-`0x2F` | E | 151-154 |
| LOAD | `0x38` | E (`rd = mem[rs1+rs2]`) | 167 |
| STORE | `0x39` | E | 168 |
| MOV | `0x3A` | E (`rd = rs1`) | 169 |
| JZ/JNZ/JLT/JGT | `0x3C`-`0x3F` | E | 171-174 |
| MOVI16 | `0x40` | F (`rd, imm16`, 4 bytes) | 176 |
| JMP | `0x43` | F | 179 |
| CALL | `0x45` | F | 181 |
| LOOP | `0x46` | F | 182 |
| **TELL** | **`0x50`** | E | 203 |
| ASK | `0x51` | E | 204 |
| DELEG | `0x52` | E | 205 |
| **BCAST** | **`0x53`** | E | 206 |
| MERGE | `0x57` | E | 210 |
| FORK / JOIN | `0x58` / `0x59` | E | 211-212 |
| C_THRESH | `0x69` | D | 225 |
| C_ADD..C_VOTE | `0x60`-`0x6F` | E | 223+ |
| V_EVID..V_PRAGMA | `0x70`-`0x7F` | E | 239+ |
| SENSE..CANBUS | `0x80`-`0x8F` | E | 262+ |
| VLOAD..VSELECT | `0xB0`-`0xBF` | E | 323+ |

**Import finding (re-verified):** `grep -rl isa_unified src/` → zero matches.
Its only in-tree consumer is `tests/test_isa_unified.py`. Its real influence is
through hard-coded hex in `signal_compiler.py` and `tests/test_conformance.py`.

---

## 4. The compiler — `src/flux/a2a/signal_compiler.py` (465 lines) — System B

`SignalCompiler` emits System B hex, hard-coded (no import of `opcodes.py` or
`isa_unified.py`). Verified emissions:

| Signal op | Emitted | Line |
|-----------|---------|------|
| let (small) | `MOVI 0x18` (Format D, 3-byte) | 145 |
| let (large) | `MOVI16 0x40` (Format F) | 147 |
| let (alias) | `MOV 0x3A` (Format E) | 143 |
| add/sub/mul/div/mod | `0x20`-`0x24` | 155 |
| eq/neq/lt/gt | `0x2C`/`0x2F`/`0x2D`/`0x2E` | 199 |
| and/or/xor | `0x25`/`0x26`/`0x27` | 224 |
| not | `0x0A` | 221 |
| **tell** | **`0x50`** | 242 |
| ask | `0x51` | 254 |
| delegate | `0x52` | 265 |
| **broadcast** | **`0x53`** | 276 |
| if → JZ | `0x3C` | 292 |
| if-else → JMP | `0x43` | 300 |
| loop → LOOP | `0x46` | 337 |
| branch → FORK/JOIN | `0x58`/`0x59` | 346/352 |
| merge → MERGE | `0x57` | 363 |
| confidence → C_THRESH | `0x69` | 373 |
| yield → YIELD | `0x15` | 379 |
| await → AWAIT | `0x5B` | 389 |
| (terminator) HALT | `0x00` | 444 |

`tests/test_signal_compiler.py` (26 tests, **green**) asserts only that these
byte values *appear in the output* — it **never runs the bytecode through the
interpreter**, so it cannot detect the divergence.

---

## 5. The interpreter — `src/flux/vm/interpreter.py` (~1600 lines) — System A

Dispatch is a giant if-chain over `opcode_byte == Op.X` (`Op` = System A).
Verified handler sites (line numbers from current `main`):

| Opcode | Line |
|--------|------|
| `Op.NOP` (0x00) | 385 |
| `Op.HALT` (0x80) | 389 |
| `Op.MOV` (0x01) | 395 |
| `Op.MOVI` (0x2B) | 402 |
| `Op.IADD` (0x08) | 407 |
| `Op.VLOAD` (0x50) | 1150 |
| `Op.TELL` (0x60) | 1231 |
| `Op.HALT`/system/PHY/unknown → raise `VMInvalidOpcodeError` | tail (~1600) |

`Op.TELL` handler (line 1231) does `data = self._fetch_var_data()` (Format G) →
`_dispatch_a2a("TELL", data)`. `Op.VLOAD` handler (line 1150) does
`vd, addr_reg = self._decode_operands_C()` → vector load.

**Consequence:** a System B `TELL` byte `0x50` enters the `Op.VLOAD` handler at
line 1150 and performs a 3-byte Format-C decode + `read_vec` — a SIMD vector
load on garbage, never an A2A dispatch. This is the "TELL decodes as VLOAD"
bug, live.

The interpreter constructor (`__init__`, line ~100) takes `bytecode: bytes`
and has **no ISA/version selector** — it unconditionally assumes System A.

---

## 6. Conformance vectors — `tests/test_conformance.py` (no executable tests)

`TEST_VECTORS` uses System B numbering (HALT `0x00`, NOP `0x01`, MOVI `0x18`,
MOVI16 `0x40`, ADD `0x20`, SUB `0x21`, MUL `0x22`, MOD `0x24`, CMP_EQ `0x2C`,
PUSH `0x0C`, POP `0x0D`, AND `0x25`, OR `0x26`, XOR `0x27`, INC `0x08`, DEC
`0x09`). The PUSH/POP/INC/DEC values were corrected to System B (commit
`superz/conformance-fix` lineage, already in `main`).

**Critical:** the file contains **no `test_*` functions** — only data + a
`run_conformance_tests(runner_fn)` template. `pytest` collects **0 tests** from
it (verified: `tests/test_conformance.py` contributes nothing to the run).
So "run conformance tests" is currently a no-op; there is **no executable
Signal→VM integration test** — exactly the P0 gap the reconciliation doc flags.

---

## 7. Test baseline (2026-08-21, Python 3.14.4)

```
$ PYTHONPATH=src python3 -m pytest tests/ -q
... 2651 passed, 1 warning in 20.07s
```

All green. The signal-compiler and isa-unified suites are green **but vacuous**
w.r.t. the divergence (byte-presence asserts only; conformance vectors not
executed against any VM).

---

## 8. Git / PR state — no active foreign work on the migration

- `main` @ `20afa5e` (2026-07-20), no commits since; tree clean.
- Open PRs: only **2 dependabot** bumps (checkout/setup-python), from 2026-06/07.
- Open issues relevant to this work (all filed 2026-04-11/12): **#7 "Critical:
  Two incompatible ISA numbering systems"**, #13 "[PROPOSAL] ISA Convergence —
  Roundtable consensus + 16-week roadmap", #6 "ICMP destination register
  hardcoded to R0", #16/#17 security.
- Remote branches `isa-v2`, `superz/conformance-fix`, `greenhorn/fix-icmp-r0`,
  `superz/security-conformance`, etc. are all **stale (April 2026)** and
  predate the marine-physics + meta-op additions. **No agent is actively
  working the A/B reconciliation** → safe to proceed (not plan-only).

---

## 9. The exact divergence — conflict table (verified)

System B value → what System A decodes it as (interpreter):

| Byte | System A (interpreter) | System B (spec/compiler) | Impact |
|------|------------------------|--------------------------|--------|
| `0x00` | NOP | HALT | compiler's HALT never halts |
| `0x01` | MOV | NOP | NOP reads a register |
| `0x02` | LOAD | RET | RET mis-decoded |
| `0x03` | STORE | IRET | — |
| `0x08` | IADD | INC | INC adds two regs |
| `0x09` | ISUB | DEC | DEC subtracts |
| `0x0A` | IMUL | NOT | NOT multiplies |
| `0x0B` | IDIV | NEG | — |
| `0x0C` | IMOD | PUSH | PUSH does modulo |
| `0x0D` | INEG | POP | POP negates |
| `0x18` | ICMP | MOVI | MOVI compares |
| `0x20` | PUSH | ADD | ADD pushes |
| `0x21` | POP | SUB | — |
| `0x22` | DUP | MUL | — |
| `0x23` | SWAP | DIV | — |
| `0x24` | ROT | MOD | — |
| `0x25` | ENTER | AND | — |
| `0x26` | LEAVE | OR | — |
| `0x27` | ALLOCA | XOR | — |
| `0x2C` | IREM | CMP_EQ | — |
| `0x38` | CAST | LOAD | — |
| `0x39` | BOX | STORE | — |
| `0x3A` | UNBOX | MOV | — |
| `0x3C` | CHECK_BOUNDS | JZ | — |
| `0x3D` | CONF (v3) | JNZ | — |
| `0x3E` | MERGE (v3) | JLT | — |
| `0x3F` | RESTORE (v3) | JGT | — |
| `0x40` | FADD | MOVI16 | — |
| `0x43` | FDIV | JMP | — |
| `0x46` | FMIN | LOOP | — |
| **`0x50`** | **VLOAD** | **TELL** | **FATAL: A2A send → SIMD load** |
| `0x51` | VSTORE | ASK | FATAL |
| `0x52` | VADD | DELEG | FATAL |
| `0x53` | VSUB | BCAST | FATAL |
| `0x54` | VMUL | ACCEPT | — |
| `0x55` | VDIV | DECLINE | — |
| `0x56` | VFMA | REPORT | — |
| `0x57` | STORE8 | MERGE | — |
| `0x58` | (unassigned) | FORK | VMInvalidOpcodeError |
| `0x59` | (unassigned) | JOIN | VMInvalidOpcodeError |
| `0x5B` | (unassigned) | AWAIT | VMInvalidOpcodeError |
| `0x60` | TELL | C_ADD | confidence op → A2A send |
| `0x61` | ASK | C_SUB | — |
| `0x66` | BROADCAST | C_FMUL | — |
| `0x69` | ASSERT_GOAL | C_THRESH | — |
| `0x80` | HALT | SENSE | compiler never halts (0x00) + System B sensor ops land on System A system ops |
| `0xB0` | PHY_ABSORB (v3.1) | VLOAD | marine-physics ↔ SIMD collision |

This is a **strict superset** of the April reconciliation doc's table — the
marine-physics (`0xB0-0xB8`) and meta (`0x3D-0x3F`) additions widen the split.

---

## 10. What "one-way converge on unified spec" means concretely

The converged target is **System B** (`isa_unified.py`). Rationale unchanged
from the April doc: System B is the 3-agent consensus, the published spec
(`docs/ISA_UNIFIED.md`), and what the compiler + conformance vectors already
target. The migration must move the interpreter (and eventually encoder/decoder/
assembler) onto System B **without deleting System A** — both tables preserved
and annotated, with an ISA selector so legacy System A bytecode keeps executing
during the transition (see plan).
