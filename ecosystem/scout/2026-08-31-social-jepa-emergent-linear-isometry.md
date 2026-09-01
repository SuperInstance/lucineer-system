# Social-JEPA: Emergent Geometric Isomorphism Between Independently Trained World Models

**Date:** 2026-08-31 · **Scout tick** · arXiv:2603.02263 (v1 Feb 28 2026, v2 Apr 17 2026)

## What
Two agents train JEPA-style world models from **distinct viewpoints of the same environment** — no parameter sharing, no coordination, no shared latent space. After training, their latent spaces turn out to be related by an **approximate linear isometry**: you can translate one agent's representation into the other's with a linear map.

Consequences demonstrated:
- Alignment survives large viewpoint shifts and minimal pixel overlap.
- A classifier trained on one agent ports to the other **zero-shot** (no gradient steps).
- Distillation-style migration between agents accelerates later learning and cuts total compute.

Claim: predictive learning objectives (JEPA's) impose strong regularities on representation *geometry* — independent learners converge on mutually translatable spaces.

## Why it matters to us
This is a big one for the elephant/ZeroClaw program:

1. **Reader-delta gets a mechanism.** ZeroClaw's Reading 2 (reader-delta: a known model's drift as retrieval key) currently assumes a reader's embedding space stays comparable over time. Social-JEPA shows independent observers of the same room should be related by an (approximate) *linear* isometry — meaning reader-delta comparison may be cheap: estimate one linear map instead of a full re-alignment. Also suggests a validity test for vmf.py's μ̂ comparisons across readers: if the residual after best linear map is small, the readers agree structurally even when coordinates differ.
2. **"Room as the unit of perception" gets outside support.** Independent agents watching the same room converge on translatable geometry — the room is the shared invariant, not the observation stream. That's the elephant's founding claim, now with external evidence.
3. **The Tap / fleet angle:** agents trained separately (different models, different yards) could interoperate at the embedding layer via a learned linear bridge rather than shared protocols — a lightweight A2A alternative to the wire-standard work filed 08-30.
4. **Wesley/Liquid lane:** zero-shot classifier porting = the local GPU model can borrow a cloud-trained classifier with no local gradient steps — relevant to growing Wesley on cheap hardware.

## Pointer
https://arxiv.org/abs/2603.02263 (code linked from paper page)
