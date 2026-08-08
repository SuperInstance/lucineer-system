# Negative Space Update: The Digital-Twin Collapse Has a Root Cause

## Found: 2026-08-07 22:15 AKDT

## The Smoking Gun

The digital-twin domain's catastrophic collapse (-0.338 delta by iteration 5) is NOT caused by overfitting or curriculum mismatch.

**It's caused by silent teacher failures.**

Of the 5 digital-twin teaching iterations:
- **3 failed completely** (iterations 2, 3, 5) — GLM-4.5-flash returned empty responses
- **2 succeeded** (iterations 1, 4) — actual teaching material was generated

When the teacher fails, the distillation loop doesn't stop. It feeds Wesley an empty (or broken) teaching prefix and then evaluates the result as if teaching occurred. The "taught" scores in failed iterations are essentially **cold-start responses with garbage context**.

## Full Failure Census

| Domain | Iterations | Failed | Topics Lost |
|--------|-----------|--------|-------------|
| cognition | 5 | 2 (iter 4, 5) | Situation signatures, Temporal pattern mining |
| digital-twin | 5 | 3 (iter 2, 3, 5) | Eventual consistency, Schema versioning, D1 optimization |
| maritime | 5 | 1 (iter 3) | Weather system integration |
| roblox | 5 | 0 | — |

**Digital-twin has the most failures AND the worst performance collapse.** The correlation is direct.

## The System Bug

The distillation loop does not properly handle teacher API failures. When GLM-4.5-flash returns an empty response:

1. The teacher JSON is saved with `"success": false` and `"error": "Empty response from teacher"`
2. But the loop continues to the student phase
3. The student receives an empty or broken teaching directive
4. The eval runs on the broken result
5. The scores are saved alongside successful iterations as if they're comparable
6. The delta is computed between a legitimate baseline and a corrupted taught score

This is a **silent data corruption bug**. The eval pipeline treats failed teaching as real teaching.

## What Should Happen

1. When the teacher fails, the iteration should be **skipped**, not scored
2. Failed iterations should be **excluded from delta computation**
3. The loop should **retry** the teacher with a different prompt or model
4. The eval output should **flag** iterations where the teacher failed
5. The version history should **refuse** to save a version derived from a failed teaching

## Reinterpreting the Data

With the failure context, the digital-twin domain's actual performance:

| Iter | Teacher | Baseline | Taught | What Actually Happened |
|------|---------|----------|--------|----------------------|
| 1 | ✓ success | 0.665 | 0.704 | Real teaching helped (+0.039) |
| 2 | ✗ empty | 0.829 | 0.630 | Corrupted context hurt (-0.199) |
| 3 | ✗ empty | 0.889 | 0.906 | Corrupted context, Wesley still did okay (+0.017) |
| 4 | ✓ success | 0.851 | 0.718 | Real teaching hurt (-0.133) — this one is real |
| 5 | ✗ empty | 0.849 | 0.511 | Corrupted context catastrophic (-0.338) |

**Real teaching performance:** iterations 1 and 4 show +0.039 and -0.133. One slight gain, one regression. Inconclusive but not catastrophic.

**Corrupted performance:** iterations 2, 3, and 5 show -0.199, +0.017, -0.338. The catastrophic scores are all from failed teaching.

## Implication

The "inverted U" pattern I reported earlier is an artifact. The real story is simpler and more fixable:

**The teacher API (GLM-4.5-flash) is unreliable, and the distillation loop doesn't handle failures properly.**

Fix the failure handling → the digital-twin domain probably performs similarly to cognition (modest gains, some noise).

## Next Steps

1. **Patch the distillation loop** to skip failed teacher iterations
2. **Re-run** the digital-twin domain with proper error handling
3. **Audit the cognition domain** — 2/5 failures there too, but the pattern was less visible because the successful iterations showed strong gains
4. **Consider a fallback teacher model** — if GLM-4.5-flash fails, retry with GLM-4.6 or a different model

---

*The negative space had a negative space inside it. The data wasn't just unanalyzed — it was corrupted by a silent failure mode. The fish finder wasn't just unread. It had a broken transducer that nobody noticed because the screen still showed numbers.*
