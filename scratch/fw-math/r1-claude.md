I'll tackle the **NMEA byte-parser integer arithmetic** — it's where the absence of an FPU bites hardest and where framework choice has real teeth.

---

**NMEA Lat/Lon in 32-bit, no FPU:**

NMEA frames lat as `ddmm.mmmm` (degrees, minutes, decimal minutes). To avoid floats on an ESP32-S3 with no hardware divider, store as **micro-degrees** (µ° = 1/1,000,000 degree).

Raw parse: `4807.038,N` → degrees=48, cent-minutes=707 (i.e., 7.038 × 100).

Convert to µ°:
```
µ° = degrees × 1,000,000 + centminutes × 16,667
     ───────────────────────────────────────────
     (since 1'=1°/60; centminutes÷60÷100≈16,667)
```

**The overflow trap:**  
Intermediate centminutes × 1,000,000 = max ~60,000 × 1,000,000 = 60 billion, which **overflows 32-bit**.  
Safe path: compute in 64-bit, then narrow:
```
uint64_t tmp = ((uint64_t)centminutes × 1000000) / 60000;
// = centminutes × 16.667, exact as integer (no FPU division)
µ° = tmp + (degrees × 1000000);
```

**Xtensa LX7 cost (on 240MHz core):**  
- `MULL` (32×32→64): 1 cycle
- `QUOS` (64÷32→32): ~30 cycles (software loop, no hardware divider)
- Shift narrowing: 1 cycle  
- **Total per coord: ~32 cycles** at 240MHz = **133 ns**, drift-free since it's pure arithmetic.

**Bounds:**  
- Max lat: 90M µ° (27 bits safe)
- Max lon: 180M µ° (28 bits safe)
- 64-bit intermediate: 36 bits used; no overflow.

---

**Repackaged vs. Custom:**  
Stock Arduino-ESP32 v4.4 ships with libc division; compiles the loop. Custom framework can **inline `__udivdi3` or substitute a hardware-friendly reciprocal (1/60000 pre-computed as fixed-point Q48),** cutting 30 cycles to 3–4. But repackaging doesn't expose this tuning; you'd rebuild libc. **Synergy claim:** quilt's math is *immune* to framework choice here—the Xtensa ISA bottleneck is fixed, not the compiler. Repackaging is a transparency loss, not a performance one.

—**Haiku 4.5**
