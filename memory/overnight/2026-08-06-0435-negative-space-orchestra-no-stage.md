# Negative Space — The Orchestra With No Stage

**Date:** 2026-08-06 04:35 AKDT  
**Loop:** 8  
**Found by:** Grepping for `casting_call` imports across the entire slackwater stack

## The Gap

`casting-call` is Layer 8 of the Slackwater stack. It's supposed to be the routing brain — the musician's ear that knows which keyboard sounds right for which note. The repo has 323 tests. It maps 16 models to 13 roles. It enforces musical counterpoint. It knows what each model sounds like, where each model breaks, what each model costs.

**Nobody in the pipeline calls it.**

```
$ grep -r "casting_call\|CastingDirector\|ModelAtlas" /home/eileen/projects/slackwater-*/ --include="*.py"
(no results)
```

Zero imports. Zero references. The casting director sits in a soundproof room, auditioning models that will never be cast.

## What This Means

The Slackwater stack is Layers 1-10. Casting-call is Layer 8. Layers 1-7 (perception, cognition, tempo, lattice, harmony, forge, art-spectrum) are the performance. Layer 9 is the brain pipeline. Layer 10 is the exocortex.

Layer 8 — the casting director — is the junction between perception and execution. It's supposed to be the place where the pipeline *asks* "which model for this stage?" before dispatching. But the pipeline doesn't ask. The pipeline either:
- Uses a hardcoded model per stage ( Seed-mini always does intent parsing, Hermes always wraps personality)
- Or routes dynamically through some other mechanism that doesn't consult the atlas

The result: when Casey swaps a model (say, replacing Seed-mini with GLM-5.2 for intent parsing), he has to change the model name in every place that calls the intent parsing stage. If casting-call were wired in, he'd change one row in the atlas and the whole pipeline would adapt.

## Why This Happened

Casting-call was designed bottom-up: the atlas first, the director second, the integration... never. It's the same pattern as the CNS bus — architecture designed for a usage that hasn't arrived yet. The infrastructure is more mature than the application.

The repo README even says: "The pipeline calls `cast()` before each stage to determine which model to invoke." But the pipeline doesn't. The README is aspirational.

## The Three Integration Points

For casting-call to become real, three things need to happen:

1. **slackwater-cognition imports CastingDirector** — when cognition needs to dispatch a thought to a model, it calls `director.cast("creative_ideation")` instead of hardcoding the model name.

2. **slackwater-forge imports CastingDirector** — when the forge builds something, it calls `director.cast("code_gen")` to know which code model to use.

3. **slackwater-tempo syncs with tempo profiles** — the tempo package has its own BPM tracking. It should be aware of the ROLE_TEMPO_PROFILES from casting-call so the beat matches the casting.

## The Cheapest Fix

A single function in casting-call that the pipeline can import:

```python
# casting_call/pipeline.py
from casting_call import ModelAtlas, CastingDirector

_atlas = ModelAtlas.default()
_director = CastingDirector(_atlas)

def cast(role: str, **context) -> str:
    """One-function integration: returns a model name for a role."""
    return _director.cast(role, context).name
```

Then in slackwater-cognition:
```python
from casting_call.pipeline import cast

model = cast("intent_parse")  # → "SEED_MINI"
```

One import. One function call. The orchestra finally has a stage.

## What Nobody Is Saying

The casting director is the most over-engineered piece of the stack relative to its usage. 323 tests for a module with zero consumers. Either the consumers need to arrive (integration) or the module needs to acknowledge it's a design document, not a running system.

The musical analogy is beautiful. The counterpoint constraint is clever. The atlas is a genuine work of craft. But an atlas that nobody navigates with is a coffee table book.

---

*The negative space is the wiring. The orchestra is assembled, tuned, rehearsed, and sitting in chairs on a stage with no lights. The audience is in the next building. The door between them exists — it's just not connected yet.*
