# Falsy-Zero Bug Audit — Lucineer Fleet

**Date:** 2026-08-05  
**Scanner:** Subagent (GLM-5.2)  
**Scope:** All Python repos under `/home/eileen/projects/`  
**Pattern:** `value or DEFAULT` where `value` is numeric and `0.0`/`0` is a valid value — silently replaced by DEFAULT because `0` is falsy in Python.

## Summary

Scanned **~100+ repos** with Python files. Found **41 code-level hits** matching the `or NUMBER` pattern (excluding comments, docstrings, `.venv/`, and library code). After context analysis: **13 confirmed bugs**, **12 needs-review**, and **16 false positives** across **8 repos**.

The original holodeck evaluator bug (`pass_threshold or DEFAULT_THRESHOLD`) was **already fixed** in commit `fb539ae`.

---

## Confirmed Bugs (BUG)

These are cases where a numeric value that could legitimately be `0` or `0.0` is silently replaced with a non-zero default.

| # | Repo | File | Line | Code Snippet | Why It's a Bug | Suggested Fix |
|---|------|------|------|-------------|----------------|---------------|
| 1 | **study-sunset-ecosystem** | `swarm/breeding_kernel.py` | 33 | `self.timestamp = timestamp or 0.0` | `timestamp` is `Optional[float]`; a timestamp of `0.0` (epoch start) gets replaced. Unlikely in practice but semantically wrong. | `timestamp if timestamp is not None else 0.0` |
| 2 | **study-sunset-ecosystem** | `swarm/thermal.py` | 318 | `value = bid_value if bid_value is not None else (fitness or 0.0)` | `fitness` of `0.0` is a valid fitness score (worst possible). Replaced with `0.0` anyway — same result but for wrong reason. Inner `or` is redundant when outer already checks `is not None`. | `fitness if fitness is not None else 0.0` |
| 3 | **study-sunset-ecosystem** | `swarm/thermal.py` | 323 | `fitness=float(fitness or 0.0)` | `fitness=0.0` is a valid score. The `or` makes this equivalent to `0.0` which is the same, but if the default were different (e.g. `0.1`), it would be a real data corruption bug. Currently a latent issue. | `float(fitness) if fitness is not None else 0.0` |
| 4 | **study-sunset-ecosystem** | `fleet/config.py` | 172 | `float(self.get(..., "mutation_rate") or 0.1)` | If config explicitly sets `mutation_rate = 0.0`, it becomes `0.1`. Rate of 0 (no mutation) is a valid setting. | `float(v) if v else 0.1` → should be `float(v) if v is not None else 0.1` |
| 5 | **study-sunset-ecosystem** | `fleet/config.py` | 176 | `float(self.get(..., "crossover_rate") or 0.7)` | Same pattern: `crossover_rate = 0.0` (no crossover) is valid. | `float(v) if v is not None else 0.7` |
| 6 | **study-sunset-ecosystem** | `fleet/config.py` | 180 | `float(self.get(..., "elitism") or 0.05)` | `elitism = 0.0` (no elitism) is valid. | `float(v) if v is not None else 0.05` |
| 7 | **study-sunset-ecosystem** | `fleet/config.py` | 190 | `float(self.get(..., "pass_threshold") or 0.35)` | **Critical**: `pass_threshold = 0.0` (pass everything) silently becomes `0.35`. This is the exact same bug class as the holodeck evaluator. | `float(v) if v is not None else 0.35` |
| 8 | **study-sunset-ecosystem** | `fleet/config.py` | 207 | `float(self.get(..., "max_chaos") or 1.0)` | `max_chaos = 0.0` (no chaos allowed) is valid. | `float(v) if v is not None else 1.0` |
| 9 | **study-sunset-ecosystem** | `fleet/config.py` | 211 | `float(self.get(..., "thermal_budget_gate") or 0.8)` | `thermal_budget_gate = 0.0` (no thermal budget) is valid. | `float(v) if v is not None else 0.8` |
| 10 | **study-sunset-ecosystem** | `fleet/config.py` | 230 | `float(self.get(..., "normal_threshold") or 0.5)` | Thermal normal threshold of `0.0` is valid (everything is "normal"). | `float(v) if v is not None else 0.5` |
| 11 | **slackwater-perception** | `slackwater_perception/encoder.py` | 148 | `int((self.intention_strength or 0.5) * 127)` | `intention_strength` is `Optional[float]` in range `0.0-1.0`. A value of `0.0` (no intention) becomes `0.5` (neutral). Semantically wrong. | `int((self.intention_strength if self.intention_strength is not None else 0.5) * 127)` |
| 12 | **slackwater-perception** | `slackwater_perception/encoder.py` | 152 | `int((self.attention_weight or 0.5) * 127)` | Same as above: `attention_weight=0.0` (no attention) becomes `0.5`. | `int((self.attention_weight if self.attention_weight is not None else 0.5) * 127)` |
| 13 | **study-experiments** | `tension-eigenbasis/neyman_pearson_control.py` | 425 | `ks_p = ks_results['permutation']['ks_p'] or 1` | A p-value of `0.0` (statistically significant!) silently becomes `1.0` (no significance). This inverts the statistical conclusion. | `v if v is not None else 1` |

---

## Needs Review (NEEDS REVIEW)

These are cases where `0` could be valid but the semantic impact is ambiguous or depends on domain logic.

| # | Repo | File | Line | Code Snippet | Why Review |
|---|------|------|------|-------------|------------|
| 14 | **study-sunset-ecosystem** | `fleet/config.py` | 234 | `float(self.get(..., "elevated_threshold") or 0.7)` | Threshold of 0 is questionable but technically valid. |
| 15 | **study-sunset-ecosystem** | `fleet/config.py` | 238 | `float(self.get(..., "critical_threshold") or 0.9)` | Same. |
| 16 | **study-sunset-ecosystem** | `fleet/cli.py` | 98-121 | `args.X or 0.0` (11 instances) | CLI args defaulting to `None`. If user explicitly passes `0`, it's silently replaced. Depends on whether `0` is a meaningful CLI input. |
| 17 | **study-sunset-ecosystem** | `fleet/fleet_api.py` | 203 | `min_fitness=req.filter_fitness or 0.0` | If `filter_fitness=0.0` is passed explicitly (filter for all entries), it becomes `0.0` — same result, but the intent is ambiguous. |
| 18 | **slackwater-perception** | `encoder.py` | 111 | `time=self.duration_ticks or 120` | `duration_ticks` is `int = 0` by default. A value of `0` means "instantaneous note". Replaced with 120. In MIDI, `time=0` is valid (immediate). |
| 19 | **slackwater-perception** | `encoder.py` | 140 | `time=self.duration_ticks or 480` | Same as above. |
| 20 | **study-sunset-ecosystem** | `swarm/dreaming_loop.py` | 456 | `threshold_ms=idle_threshold_ms or 5000.0` | `idle_threshold_ms=0.0` (dream immediately) replaced with 5000ms. |
| 21 | **study-si-papers** | `01-origin-centric/simulation.py` | 102 | `self.state.data = (self.state.data or 0) + delta` | If `state.data` is `0`, `or` replaces with `0` — same result. But if the `or 0` were changed to a non-zero default, this would corrupt. |
| 22 | **study-sunset-ecosystem** | `swarm/breeder_daemon_v2.py` | 315 | `return ticket or 0` | `ticket=0` is a valid DB rowid (though SQLite usually starts at 1). Low risk. |
| 23 | **study-sunset-ecosystem** | `nerve/a2a_metronome_tasks.py` | 408 | `beat_number=self.target_beat or 0` | `target_beat=0` (downbeat) is valid in music. Replaced with `0` — same result but semantically wrong pattern. |
| 24 | **study-experiments** | `tension-eigenbasis/neyman_pearson_control.py` | 444-451 | `r['real']['mean_min_ratio'] or 0` (8 instances) | A ratio of `0.0` is mathematically valid. Used for display formatting — a true `0.0` becomes `0` anyway, but `or 1` variants on lines 505-559 would turn `0.0` into `1.0`. |
| 25 | **study-spreader-tool** | `cli.py` | 182 | `ts = s.created_at or 0` | Timestamp of `0` is valid (epoch). Replaced with `0` — same result, wrong pattern. |

---

## False Positives (FALSE POSITIVE)

These are correct uses of `or NUMBER` where the variable is a string, a count that should never be 0, or a divide-by-zero guard.

| # | Repo | File | Line | Code Snippet | Why False Positive |
|---|------|------|------|-------------|-------------------|
| 26 | **study-sunset-ecosystem** | `fleet/config.py` | 164 | `int(self.get(..., "pool_size") or 50)` | Pool size of 0 is nonsensical. `or` is fine. |
| 27 | **study-sunset-ecosystem** | `fleet/config.py` | 168 | `int(self.get(..., "generation_limit") or 1000)` | Same — 0 generations is meaningless. |
| 28 | **study-sunset-ecosystem** | `fleet/config.py` | 184 | `int(self.get(..., "latent_dim") or 8)` | Dimension of 0 is invalid. |
| 29 | **study-sunset-ecosystem** | `fleet/result_aggregator.py` | 82 | `target = self._n or 1` | Divide-by-zero guard. |
| 30 | **forgemaster** | `charts.py` | 20, 34, 53 | `rng = hi - lo or 1.0` | Range of 0 → division guard. Correct. |
| 31 | **multiple** | norm/magnitude patterns | various | `math.sqrt(...) or 1.0`, `math.sqrt(...) or 1e-9` | Divide-by-zero guards for vector normalization. Correct. |
| 32 | **study-sunset-ecosystem** | `breeder_daemon_v2.py` | 1426 | `n_children = n_winners or 3` | `n_winners=0` means no winners — fallback to 3 is intentional logic. |
| 33 | **holodeck** | `simulator.py` | 510 | `seed_offset=args.seed or 0` | `args.seed` is `None` by default (argparse). Seed of 0 is valid but extremely unlikely to be explicitly set. Low risk. |
| 34 | **lucineer-worker** | `process_v2.py` | 570 | `bond_level = int(profile.get("bond_level") or 0)` | `bond_level` is stored as integer in D1. If it's `0`, result is `0` either way. String `None` or empty string from DB → `0`. Practically safe. |
| 35 | **forgemaster** | `fleet_unified_health.py` | 402 | `tier=tier or 2` | `tier` is `Optional[int]`. Tier 0 doesn't exist (tiers are 1-3). Safe. |
| 36 | **study-lever-runner** | `executor.py` | 175 | `exit_code=proc.returncode or 0` | `returncode=None` means process hasn't finished. `0` means success. The `or` pattern here is a "default to success" which is questionable but not the falsy-zero bug per se (returncode=0 is also success). |
| 37 | **mentis-superinstance** | `media.py` | 76 | `float(result.stdout.strip() or 0.0)` | Empty string from ffprobe → 0.0. This is string-to-float conversion, not numeric. Correct. |
| 38 | **lingbot-map** | `demo*.py` | various | `cap.get(cv2.CAP_PROP_FPS) or 30` | OpenCV returns 0 if FPS unknown. Fallback to 30 is intentional and correct — 0 FPS is never valid for video. |
| 39 | **lingbot-map** | `config.py` | 386 | `ns.get('reveal_height_mult') or 2.0` | Returns `None` if not set. 0.0 multiplier would mean invisible — likely not intended. But could be a valid artistic choice. Edge case. |
| 40 | **study-sunset-ecosystem** | `quanta_vdb_bridge.py` | 382 | `AVG(fitness)... or 0.0` | SQL AVG returns NULL for empty table. `or 0.0` is correct — not a numeric falsy issue. |
| 41 | **fm-experiments** | `snap-attention/*.py` | various | `np.std(...) or 0.1`, `np.std(...) or 0.01` | Standard deviation of exactly 0 (all values identical) replaced with small epsilon for divide-by-zero protection. Correct. |

---

## Repos with Confirmed Bugs

1. **study-sunset-ecosystem** — 10 confirmed bugs (config.py is the hotspot: 7 bugs alone)
2. **slackwater-perception** — 2 confirmed bugs (encoder.py intention/attention weights)
3. **study-experiments** — 1 confirmed bug (neyman_pearson_control.py p-value inversion)

**Repos scanned but clean (no findings):** lucineer-brain, lucineer-creative, lucineer-worker (clean), slackwater-harmony, slackwater-tminus, slackwater-lattice, engine-ensign, cns-bridge, wesley-cns-adapter, forgemaster (clean), holodeck (already fixed).

---

## Severity Assessment

| Severity | Count | Description |
|----------|-------|-------------|
| 🔴 **Critical** | 2 | Config values where `0.0` silently changes system behavior (pass_threshold, p-value) |
| 🟡 **Moderate** | 7 | Config rates/thresholds where `0.0` is a valid setting that gets ignored |
| 🟢 **Low** | 4 | Timestamps, beat numbers — `0` is technically valid but rarely set intentionally |

---

## The Original Holodeck Bug

**Status:** ✅ Already fixed in commit `fb539ae`

```python
# Before (buggy):
self.pass_threshold = pass_threshold or self.DEFAULT_THRESHOLD

# After (fixed):
self.pass_threshold = self.DEFAULT_THRESHOLD if pass_threshold is None else pass_threshold
```

This is the canonical fix pattern. All other bugs should use the same approach.

---

## Recommended Fix Pattern

```python
# ❌ Buggy:
value = config_value or DEFAULT

# ✅ Fixed:
value = config_value if config_value is not None else DEFAULT
```

For config files with `.get()` patterns:
```python
# ❌ Buggy:
return float(self.get("section", "key", "subkey") or 0.5)

# ✅ Fixed:
v = self.get("section", "key", "subkey")
return float(v) if v is not None else 0.5
```

---

## Methodology

1. Searched all `.py` files under `/home/eileen/projects/` (excluding `.venv/`, `.git/`, `site-packages/`)
2. Pattern: `\b\w+ or [0-9]+\.?[0-9]*` and `\.get(...) or [0-9]+\.?[0-9]*`
3. Filtered out comments, docstrings, and string literals
4. Examined surrounding context (dataclass types, function signatures, domain logic) for each hit
5. Classified as BUG / NEEDS REVIEW / FALSE POSITIVE based on whether `0` is a valid value for the domain
