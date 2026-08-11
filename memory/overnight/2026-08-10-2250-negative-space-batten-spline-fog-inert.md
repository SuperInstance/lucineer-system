# Negative Space: batten-spline — Fog Density Is Computed But Never Used

**Repo:** batten-spline  
**Date:** 2026-08-10 22:50 AKDT  
**Component:** CascadeRouter.route()

## The Gap

`CascadeRouter.route()` computes two values:
1. **confidence** — distance-and-time-weighted quality estimate (Nadaraya-Watson kernel regression)
2. **fog_density** — distance to nearest batten (how well-charted this region is)

Both are returned in `RouteResult`. But only `confidence` is used in the routing decision (`_pick_target`). `fog_density` is informational — reported but inert.

## Why This Matters

Consider this scenario:

1. A local model handles embedding `[0.1, 0.0]` well. Quality reported: 0.95.
2. A local model handles embedding `[0.15, 0.0]` well. Quality reported: 0.90.
3. New prompt at `[0.12, 0.0]` → confidence 0.925, fog_density 0.02. Route: LOCAL. ✅ Correct.
4. New prompt at `[0.12, 50.0]` → confidence 0.925 (same distance from battens in normalized space), fog_density 50.0. Route: LOCAL. ❌ Wrong.

OK, that's a contrived 2D example. But the real issue is subtler: when there are very few battens (cold start), confidence is dominated by whatever happens to be nearest. A single batten at quality 0.9 means EVERYWHERE in the space gets routed to LOCAL with ~0.9 confidence (the Gaussian kernel decays, but with a large `fog_scale`, the decay is gentle).

**Fog density should be a confidence modifier or a gating signal:**
- If fog_density > threshold, force CLOUD regardless of interpolated confidence
- Or: multiply confidence by `exp(-fog_density / fog_scale)` so distant queries get downweighted

## The Existing Guard

The current guard against this is: with no battens, confidence returns 0.0 (complete fog). So an empty router routes everything to CLOUD. But once you add even ONE batten, the entire embedding space gets nonzero confidence that decays with distance. Whether that's "high enough" depends on `fog_scale`.

## What Else Is Missing

1. **NaN handling** — adding a batten with a NaN embedding silently produces NaN confidence for all future queries that get near it. No validation.
2. **Prune is age-based only** — `prune()` sorts by `age_weight` and keeps the newest. It doesn't consider spatial coverage. A well-distributed old batten gets pruned in favor of a cluster of new ones in the same neighborhood.
3. **No serialization versioning** — `state_dict()` has no version field. Schema evolution will be painful.
4. **routing_decision() on BattenSpline duplicates _pick_target() on CascadeRouter** — two code paths for the same logic, can diverge.
5. **No batch routing** — routing one at a time when you could batch with vectorized distance computation.

## Recommendation

**Quick win:** Add a `fog_threshold` parameter to CascadeRouter. In `route()`, if `fog_density > fog_threshold`, return CLOUD with reason "uncharted territory". This is a 5-line change.

**Medium win:** Combine confidence and fog_density into a composite score: `adjusted_confidence = confidence * exp(-fog_density / (2 * fog_scale))`. This naturally penalizes uncharted regions even when interpolation says "high quality nearby."

## Pattern

This matches the fleet-wide pattern: **infrastructure ahead of need.** The fog_density computation is correct, well-implemented, and produces the right values. It just doesn't feed into any decision. The grid exists but nobody reads it — same as stigmergy's spatial lookup, same as FlowStateProtector's counter.

---
*The fog is measured precisely. The fog is ignored completely. This is not irony — it's architecture waiting for its wiring.*
