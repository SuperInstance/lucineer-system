# Negative Space: The Fleet-Wide NaN Blindness

**Date:** 2026-08-11 00:00 AKDT  
**Scope:** Entire SuperInstance fleet  
**Severity:** Medium (silent data corruption, not crashes)

## The Finding

Across the entire fleet, there are **zero NaN validation checks** in source code. Zero `isnan()`, zero `is_nan()`, zero `Number.isNaN()`. Meanwhile there are **62+ floating-point comparisons** that will silently fail when given NaN inputs.

This is not a bug in any single repo. It is a **fleet-wide architectural blind spot**.

## The Pattern

### How NaN Works (in every language)

NaN (Not-a-Number) has a unique property: **all comparisons with NaN return false, except `!=`**.

```
NaN < 0.0   → false
NaN > 0.0   → false
NaN == 0.0  → false
NaN != 0.0  → true
NaN < NaN   → false
NaN == NaN  → false  // Even NaN doesn't equal itself!
```

This means any `if value < threshold` guard silently passes NaN through. Any `if value == 0.0` check silently fails. NaN propagates through arithmetic: `NaN + x = NaN`, `NaN * x = NaN`, `NaN.sqrt() = NaN`.

### Where It Bites

| Repo | Language | Vulnerable Comparisons | Impact |
|------|----------|----------------------|--------|
| dual-band-guard | Rust | 16 | NaN magnitudes bypass all guard logic. VarianceGuard NaN contaminates window. EntropyGuard records NaN direction as -1.0. |
| officers-quarters | TypeScript | 38 | Surprise/threshold checks in tile evolution. Coverage calculations. |
| batten-spline | Python | 3 | Confidence interpolation. Fog density. Quality clipping. |
| base60-lattice | TypeScript | 4 | Angle comparisons. |
| stigmergy | TypeScript | 1 | Pheromone detection. |
| cns-bridge | Python | 2 | Signal processing. |

### The Specific Bugs (Already Documented)

1. **batten-spline** (memory/overnight/2026-08-10-2250-negative-space-batten-spline-fog-inert.md): NaN embedding produces NaN confidence for all nearby queries. Silent corruption.

2. **dual-band-guard** (tests/edge_cases_extended.rs): 
   - `StructuralGuard`: `NaN < 0.01` is false → guard doesn't short-circuit → NaN falls through to other checks → classified as Correctable (wrong)
   - `VarianceGuard`: NaN in window → sum is NaN → variance is NaN → `NaN > threshold` is false → everything becomes Correctable (silent failure)
   - `EntropyGuard`: NaN direction → `abs() < EPSILON` is false → recorded as -1.0 (silent data corruption)

## Why This Is a Pattern, Not a Coincidence

The fleet builds systems that model the world. Models use floating-point math. Floating-point math has NaN. The systems trust their inputs. Nobody validates.

This is the same pattern as the security breach (the hermit crab and the open hatch) — the system assumes the outside world is well-formed. When it isn't, the system doesn't crash. It corrupts silently.

**The hermit crab metaphor:** The hermit crab checks its shell for cracks before entering. But it never checks the water for salinity. If the water is wrong, the crab lives in a poisoned shell and doesn't know it. NaN is the poison in the water.

## The Fix

### Option A: Input Validation (Boring but Effective)
Add NaN checks at every system boundary:

**Python:**
```python
import math
def safe_confidence(x: float) -> float:
    if math.isnan(x) or math.isinf(x):
        return 0.0  # treat NaN as zero confidence
    return x
```

**Rust:**
```rust
if surprise.magnitude.is_nan() {
    return SurpriseBand::Correctable; // or a new "Invalid" band
}
```

**TypeScript:**
```typescript
if (Number.isNaN(value)) {
    return 0.0;
}
```

### Option B: The NaN Guard (The Fleet's Missing Component)
Build a fleet-wide NaN validation layer — a utility module imported by every repo:

```
SuperInstance/nan-guard/
  ├── python/nan_guard.py
  ├── rust/nan_guard.rs
  └── typescript/nan_guard.ts
```

Each provides:
- `sanitize(value, default=0.0)` — replace NaN/Inf with default
- `validate(value, name)` — raise/panic on NaN (for debugging)
- `is_clean(value)` — boolean check

This is the dual-band-guard pattern applied to NaN: a weightless, untrainable guard that refuses to let NaN through.

### Option C: Property-Based Testing (Long-term)
Add property-based tests that verify NaN-safety:
- Python: Hypothesis (`@given(st.floats(allow_nan=True))`)
- Rust: Proptest or Quickcheck
- TypeScript: Fast-check

These would catch NaN bugs automatically across the fleet.

## Recommendation

1. **Immediate:** Document the NaN vulnerability in each repo's README
2. **Short-term:** Add input validation at system boundaries (Option A)
3. **Medium-term:** Build `nan-guard` as a shared utility (Option B)
4. **Long-term:** Property-based NaN tests in every test suite (Option C)

## The Deeper Pattern

The fleet has recurring "infrastructure ahead of need" (stigmergy grid, FlowStateProtector, harmony-core). NaN validation is the opposite: **infrastructure behind need**. The need exists now (NaN is silently corrupting data). The infrastructure doesn't.

The ship builds depth sounders but doesn't check if the water is fresh. The depth sounder works perfectly in salt water. In fresh water, it reads wrong. The crew trusts the reading. The boat runs aground.

---
*The water looks the same. The instruments glow. The reading is wrong. The hull meets the rock.*
