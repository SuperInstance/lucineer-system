ROUND 2 — you now read your rivals' round-1 answers (below). Their convergence: the repackaged rspurlock framework (Arduino-ESP32 v4.4, no custom patches) is MATHEMATICALLY INERT — the math lives in application code, not the framework package.

ROUND 1 ANSWERS:
[CLAUDE] NMEA lat/lon in µ°: µ° = deg×1e6 + centminutes×16,667; overflow trap centminutes×1e6 = 60 billion overflows 32-bit — safe via uint64 intermediate then narrow; MULL 1 cycle, QUOS ~30 cycles software loop → ~32 cycles/coord = 133ns @240MHz; bounds: lat 90M µ° (27 bits), lon 180M µ° (28 bits) safe.
[KIMI] Keel ♩=60: S3 timers off APB=80MHz; exact 1s needs N·d=80,000,000, satisfied exactly by d=80, N=1,000,000 (esp_timer) → 0 ppm software error; residual = 40MHz crystal ±20ppm → 72ms/hr worst case. digitalWrite = one s32i.n into GPIO_OUT_W1TS/W1TC (0x60004008/0C), toggle 3 ops ~17ns; LX7 no FPU, no 64-bit ALU — u64 compare = two 32-bit sub/bne pairs.
[DEEPSEEK] µ° bounds: |lat|≤90°→90e6 µ° < 2^31 ✅; parse acc=acc*10+digit max 180,000,000 < 2^31 ✅; knots mm/10×3600/1852 no overflow (99,999×3600=359,996,400 < 2^31); acc*10+c compiles to slli×2+add×2 (no HW multiply); /1852 → mullhi+shift reciprocal. Same 72ms/hr crystal bound. Verdict: repackaging is mathematically inert — packaging, not equations.

ROUND 2 TASK — find what the others MISSED. Three candidates, pick the strongest and go deep:
(a) The qm_opcodes state machine (BIND/LINK/EFFECT/VIEW/TICK/FORGET) — what does it cost INSTRUCTIONS? A cell-graph with E edges and V vertices: LINK = hash or index lookup? EFFECT = switch dispatch — what's the actual dispatch cost on LX7 (jump table vs compare-chain)? What's the TOTAL cycle budget for a 100-cell tick at 240MHz, and is the opcode loop memory-bound or ALU-bound?
(b) The "inert" claim is too easy — what could a repackaged framework actually BREAK or FIX that changes the math? (e.g., toolchain versions changing codegen: GCC for Xtensa — which version does v4.4 pin? -Os vs -O2 changing the reciprocal-multiply emission? LTO? newlib float emulation?)
(c) Drift accounting across BOTH layers: the NMEA parser's clock vs the keel's clock — if both run off the same esp_timer epoch, what's the relative drift between a parsed position and a blink? Zero (shared epoch) or is there aliasing (1µs tick vs 25ns tick)?
Answer ≤350 words, equations plaintext, sign your model. Be the sharpest knife at the table.
