# TUTOR Translation: Three Layers, One 60-Bit Machine

**NMEA Conversion (µ-Degree Safe Integer)**

TUTOR integer on 60-bit word, maxint ≈ 1.15e18. The conversion is direct:

```
U = IP * 1000000 + FR * 1000000 / SCALE
```

No 64-bit intermediates needed—a 60-bit word **swallows the overflow trap entirely**. Worst case: 180°×1e6 = 1.8e8, trivial. This is why PLATO chose 60 bits: large enough that naive arithmetic stays safe, small enough to fit CDC 6600 registers. The ESP32's dance (`u = ip*1000000LL + fr*1000000LL/scale` with 64-bit temporaries) is defensive; TUTOR makes it unnecessary. What vanishes: the fixed-point multiplier library (×3048/10000). TUTOR had no floats early; you'd hard-code scale factors as integer ratios, checked once at init.

**Keel Timer (80M Counter as 1 kHz Discipline)**

The ESP32 requires N·d = 80,000,000 ticks (80 MHz, 1 second exact). PLATO IV refreshes at 1 kHz—so a 1 Hz keel is simply:

```
KEELPHASE = MOD(TICKCOUNT, 1000)
IF KEELPHASE = 0 THEN LIGHT_PIXEL(256, 256)
```

One modulo, one conditional per refresh. But here's the trade-off: PLATO's clock drifts ±100 ppm (72 ms/hr). The ESP32's ±20 ppm crystal is 5× tighter—needed for NMEA navigation. TUTOR's real-time design (1 kHz plasma panel refresh, touch input) could *tolerate* that drift; it was CAI, not dead-reckoning. The keel on PLATO would blink, just not at UTC precision.

**Opcode Dispatch (100-Cell Loom)**

State machine with 100 states, 200 edges:

```
DISPATCH(STATE, EDGE) = LOOKUP[STATE][EDGE]
NEWSTATE = DISPATCH(CURRENT, INPUT)
```

On CDC 6600 (PLATO's engine): one table dereference from core memory ≈ 1–2 µs. 100×200 = 20,000 entries ≈ 160 KB. PLATO systems had ~1 MB core—this fits. The "2,200 cycles @240MHz ≈ 9.2µs" on ESP32 is **surprisingly close** to CDC 6600 timing: a state transition is a state transition, whether the display is plasma or SPI.

**What Survives:**

Integer semantics (perfect). The state topology (identical). Real-time discipline (1 kHz ≈ 80 MHz / 80k, both are *heartbeats*).

**What Vanishes:**

The precision arms race. TUTOR encoded the same math at looser tolerance, trusting that interactivity (touch, immediate feedback) was more important than drift. The ESP32 stack tightens the loop; PLATO loosened it, intentionally.

---

Claude Haiku 4.5
