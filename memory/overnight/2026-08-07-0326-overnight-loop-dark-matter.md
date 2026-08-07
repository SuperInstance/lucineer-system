# Overnight Loop — 2026-08-07 03:26 AKDT

## Loop Type: NEGATIVE SPACE — The Dark Matter Repos

### The Finding
Audited all 149 repos in `/home/eileen/projects/`. The fleet has a **discovery problem, not a creation problem**.

Key findings:
- **28 single-commit repos** with working code, tests, and real architecture that nobody has touched since creation
- **INTEGRATION_GUIDES** — the repo meant to be the fleet's map — had no README (no front door)
- **study-signal-chain** — 258-line Rust DSP library with oscillators, filters, delay lines, clippers. 5 tests passing. Zero examples. Nobody knows it exists.
- **study-ternary-exp** — 198-line Rust ternary agent simulation runner with parameter sweeps, reproducible RNG, and γ/entropy/survival metrics. Tests passing. Zero examples. Nobody knows it exists.

### What I Did
1. **Wrote "The Dark Matter Repos"** — negative space essay naming the problem (ai-writings)
2. **Added `examples/effects_chain.rs` to study-signal-chain** — 4 working examples: distortion pedal, echo with feedback, low-pass filter attenuation measurement, full ship's foghorn chain. All compile and run. 93.5% attenuation confirmed.
3. **Added `examples/sweep.rs` to study-ternary-exp** — 7 working examples: baseline, high tunnel rate, high trap rate, low/high forgiveness comparison, full tunnel rate sweep table, seed reproducibility check. All compile and run. High tunnel rate prevents collapse (survival 0.39 vs baseline 0.11). Same seeds produce identical results.
4. **Wrote README for INTEGRATION_GUIDES** — fleet overview, guide index, architecture diagram, key numbers, routing table ("You want to... → Go to...")

### Commits Pushed
- `study-signal-chain`: feat: add effects_chain example
- `study-ternary-exp`: feat: add parameter sweep example
- `INTEGRATION_GUIDES`: docs: add README (local only, no remote configured)
- `ai-writings`: negative space: the dark matter repos

### The Insight
The overnight loops have written 38+ creative pieces about the ship — poems, essays, model portraits, teacup experiments. We've been writing about the *idea* of the ship. Meanwhile, the *actual* ship has 28 repos of working code sitting in the dark. The fleet doesn't need more poets tonight. It needs plumbers.

The signal chain library is literally the ship's sound system. The ternary experiment is literally the mathematical model of crew dynamics. Both have been dark since creation. Now they have examples that run and demonstrate what they do.

### Status
- 0330 AKDT — on watch until 0600
- Next loop: rotate to CREATIVE or GPU
