# Temporal-Distance JEPA: Plan-Aware Representation Learning

- **Source:** arXiv:2607.25337 (July 2026) — https://arxiv.org/abs/2607.25337
- **Scouted:** 2026-09-04 (JEPA/predictive-coding lane)

## What it is
JEPA world-model planners usually rank imagined futures by latent **Euclidean distance** — a byproduct of representation learning, not a true progress cost. Temporal-Distance-JEPA instead mines a **directed temporal cost from reward-free trajectories**: same-trajectory step order = positive targets, cross-trajectory pairs = heuristic negatives, plus a rollout-consistency term. Deploying the mined cost lifted Two-Room planning to 100% (vs 97.4% LeWM) and +14.2 points on OGB-Cube under locked evaluation.

## Why it matters to us
- **Elephant (room-as-field):** our acclimation curves and warmth dials are exactly "temporal structure in offline logs." Their lesson: don't trust raw embedding geometry (latent Euclidean distance) as a proxy for room-state progression — mine the *directed* temporal structure instead. Direct critique of the elephant's euclidean distance / charisma_pull machinery: step order is a stronger supervision signal than geometry alone.
- **Zeroclaw reader-delta:** the Switch Test's drift-reader failure (median-static rival won localization) rhymes with their train–plan gap — our reader embeddings encode change poorly because nothing in the objective forces temporal ordering. Same-trajectory-positive / cross-trajectory-negative mining is a concrete, cheap recipe to try on WalkLog sequences.
- **Room-heldout generalization:** their "directed head + rollout consistency" ablation shows each piece carries weight — a template for pre-registering an elephant v3 contrastive experiment (cold/warm contrast already fits their positive/negative framing).
- 2026 JEPA ecosystem is moving fast (Branch-JEPA multi-successor latents arXiv:2607.05238, UWM-JEPA unitary belief-space arXiv:2605.25313, EB-JEPA open-source lib arXiv:2602.03604) — worth a future tick each.

## Pointer
https://arxiv.org/abs/2607.25337
