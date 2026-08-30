# IConE: batch-independent collapse prevention for JEAs (stable at batch size 1)

**Scouted:** 2026-08-30 08:03 AKDT · worker: scout
**Lane:** JEPA/predictive-coding literature (journal hot thread: ZeroClaw thesis v3, elephant room-state embeddings, E4 rebound watch)

## What

**IConE (Instance-Contrasted Embeddings)**, arXiv 2603.15263 (v1 Mar 2026, v2 Jul
2026) — "Batch Independent Collapse Prevention for Self-Supervised Representation
Learning."

All mainstream Joint-Embedding Architectures (JEPA family included) prevent
representation collapse via *batch interaction*: SimCLR-style negatives, or
VICReg-style variance/covariance regularization over the batch. That breaks in
small-batch regimes — and room-field training is a small-batch regime.

IConE replaces batch statistics with a **global set of learnable auxiliary
instance embeddings** under an explicit diversity objective — the anti-collapse
mechanism moves from the transient batch to a dataset-level embedding space.
Results: stable training at **batch size 1 through 64**, robust to severe class
imbalance, and geometric analysis shows preserved intrinsic dimensionality where
baseline JEAs collapse as batches shrink. Demonstrated on 2D/3D biomedical
modalities.

## Why it matters to us

- **Elephant's room-state embeddings are trained on exactly this failure regime:**
  small, imbalanced cold/warm contrast samples per room. VICReg-style variance
  regularization over a handful of room snapshots is statistically fragile — a
  likely contributor to the in-sample memorization (~4–15×) ZeroClaw's encoder
  tier showed, and to room-heldout failures.
- **Batch-independence = room-independence.** If collapse prevention doesn't need
  a batch, it doesn't need many simultaneous rooms — one room's history alone can
  train against the global auxiliary embedding set. That fits the "room is the
  unit of perception" doctrine better than batch-stat methods ever did.
- **Intrinsic-dimensionality preservation** is a directly measurable claim — the
  elephant repo could adopt it as a health dial alongside the vmf κ
  (concentration) readouts: watch embedding effective rank during training, not
  just loss.
- **For the E4 rebound watch:** if flooding signal is suspected of washing out
  embedding diversity, an IConE-style auxiliary objective is the outside-fleet
  answer — diversity enforced by construction, not by batch luck.

## Pointers
- https://arxiv.org/abs/2603.15263 (paper)
- Background: VICReg (arXiv 2105.04906) — the batch-stat baseline IConE replaces
- https://ai.meta.com/blog/understanding-dimensional-collapse/ (dimensional collapse primer)
