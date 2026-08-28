**Candidate (c): Clock aliasing between NMEA capture and keel tick — the shared-epoch blind spot.**

The convergence missed this: both NMEA parser and keel tick run off `esp_timer` (same clock, ✓), but *sampling phase differs*. NMEA captures the timestamp when a complete sentence arrives (data-dependent delay: 0–50ms variability in UART FIFO drain); keel samples GPIO state synchronously on `esp_timer` interrupt firing. If both ran in the same ISR context, zero drift. They don't.

**The leak:**

Call esp_timer_get_time() at T₀ (NMEA done). Keel's next tick fires at T₁ = (T₀ + 1MHz⁻¹ - phase). The position's timestamp T₀ and the blink's timestamp T₁ are **phase-locked to different events**—UART completion vs timer interrupt. Both are 1µs-grained, but their *sample skew* ≠ 0.

Worst case: NMEA idles 999µs waiting for keel's 1MHz tick to fire, then the GPS data itself is 100ms old (from sentence parse latency—UART buffering, checksum validation). Total skew: **~100ms**. That's sub-sample at 1Hz position update but *not* invisible at 10Hz.

**What matters:**

If downstream uses both timestamps to interpolate heading (e.g., `Δlat/Δt` between two positions), mixing NMEA's "packet arrival" timestamp with keel's "GPIO observation" timestamp produces systematic bias in heading estimate—not a crash, but 1–2° error in course if the vessel is turning. Smooth data → noisy gradient.

**Fix:** Timestamp NMEA *inside* the uart_event_t callback, not after the full sentence is assembled. Use the same `esp_timer_get_time()` call—zero skew to keel's next edge. Single line: `nmea_ts = esp_timer_get_time()` in ISR.

The repackaged framework didn't break this; it's a design trap the code walks into. Inert claim stands, but **implementation assumed sampling coherence the code doesn't provide**.

**Signed: claude-haiku-4-5**
