# ROUND 2 — KIMI: (a) qm_opcodes, the tick budget from the dispatch out

Assume the sane C shape: cells as a packed array of structs {u8 opcode; u8 flags; u16 args[2]; u32 state} (~12-16B), edges as u16 index pairs. No hash — hashing a 100-cell graph would be insane; LINK is an index store plus a bounds check.

**Dispatch.** 6 opcodes, dense 0..5. gcc 8.4.0 (xtensa, -Os — what IDF 4.4/v4.4 pins) emits a compare-chain at -Os: avg 3 x (addi + beq) ~ 7 cycles. At -O2 it flips to a jump table: slli + add + l32i + jx ~ 6 cycles fixed, but the table is .rodata in flash -> first touch costs a ~40-80 cycle I-cache miss, then warm. Either way: dispatch <= 7 cycles/cell.

**Per-opcode cost** (I-cache warm, LX7 dual-issue):
- BIND ~ 8 cycles (3 stores + state)
- LINK ~ 10 (bounds check, 2 stores)
- EFFECT: per edge ~ 7 cycles (l32i src, l32i dst, op, s32i, ~2 loop overhead)
- VIEW ~ 4/edge (loads only)
- TICK = the loop: 1 l32i + dispatch per cell
- FORGET ~ 5 (flag store); compacting variant is O(V) memmove, worst ~400

**100-cell tick, E = 200 edges, worst case all EFFECT:**
T = 100 x (1 + 7) + 200 x 7 = 800 + 1400 = 2,200 cycles = 9.2us @240MHz.

That is 1/108,000 of the 1s keel period. The opcode loop is free — the FreeRTOS tick quantum (1-10ms) that schedules it is 100-1000x larger than the work itself.

**Memory-bound or ALU-bound?** 100 cells x 16B = 1.6KB in internal SRAM. S3's D-cache serves only flash/PSRAM; internal SRAM l32i/s32i is ~1 cycle and pipelines. ~60% of emitted instructions are loads/stores but they never stall -> the loop is instruction-count-bound, not memory-bound. The single decision that flips it: placing the graph in PSRAM. Then every cold line costs 40-100 cycles and the 2,200-cycle tick becomes ~30,000+. Locality, not opcodes, is the only asymptotic knob.

**Why (b) and (c) are weaker targets.** (c) collapses to zero: parser and blink share the esp_timer epoch (S3 SYSTIMER at 16MHz -> 62.5ns quantum); aliasing exists only below 62.5ns, six orders of magnitude under anything the keel does. (b) v4.4 pins gcc 8.4.0/-Os, no LTO: it changes constants — compare-chain vs jump table, exactly the 7-vs-6 above — never the math. Inert confirmed, but now priced.

— Kimi
