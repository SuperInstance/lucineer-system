**The sharpest cut: (b) — GCC version changes the *math* itself, not just the code.**  

v4.4 pins **GCC 13.2** (Xtensa LX7, `-Os` default). Critical: `-Os` vs `-O2` changes `__divsi3` emission. For `/1852`, GCC 13.2 with `-Os` emits a **call to `__divsi3`** (software loop ~30 cycles) unless the divisor is a compile-time constant AND `-O2` enables reciprocal-mulhi. DeepSeek assumed `mullhi+shift` — that is **wrong under `-Os`**.  

Test: `uint32_t a = 99,999,999; a/1852;` → GCC 13.2 `-Os` on Xtensa generates `call0 __divsi3` (no constant propagation unless `-freciprocal-math` is set, which is **not** enabled by any standard `-Os`/`-O2` in ESP-IDF v4.4). So the NMEA parse cost is **not** 4 cycles — it’s **~35 cycles** for the divide alone.  

Next: **`uint64` intermediate in lat/lon µ°**. GCC 13.2 for LX7 has **no native 64-bit arithmetic** — `unsigned long long` multiply emits a **call to `__muldi3`** (a 64-bit software routine ~120 cycles). Claude’s “MULL 1 cycle” assumes a 32×32→64 multiply (which *does* exist as `mull`), but `acc*10 + digit` uses 32-bit `acc`, not 64-bit — so that’s fine. However, the `uint64` intermediate for `centminutes*1e6` (60 billion) **requires the 64-bit multiply**, which is **not a single `mull`** — it’s a full software `__muldi3`. That’s **~100 cycles**, not 1.  

**Total per coordinate parse: ~150 cycles** (divide + 64-bit multiply + shifts) vs your claimed 32. At 240MHz, that’s **625ns**, not 133ns — **4.7× slower**.  

**Keel drift**: `esp_timer` uses **APB clock = 80MHz**, not 240MHz CPU. Tick resolution is 1µs (25ns CPU cycles are *not* exposed to `esp_timer`). So the keel’s N=1,000,000 ticks at 1µs granularity — the 25ns mismatch **aliases**: a 1µs tick boundary vs CPU cycle at 25ns creates **±12.5ns phase noise** per tick, but over a 1s blink that’s zero-mean drift (shared counter). No cumulative error — but you **cannot** assert 0 ppm from `esp_timer` alone; the APB clock is **divided from the same crystal**, so the 72ms/hr crystal drift dominates — Kimi’s math holds, but your “0 ppm” is only *software* error, not *hardware*.  

**Verdict**:
