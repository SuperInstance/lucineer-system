# Dym–Gortler: Low-Dimensional Invariant Embeddings (separating invariants, 2D+1 / generic D+1)

**Date:** 2026-08-31 · **Scout tick** · Dym & Gortler, *Foundations of Computational Mathematics* (2024; arXiv 2022), DOI 10.1007/s10208-024-09641-2

## What
Studies **separating invariants** — invariant maps that distinguish group orbits without generating the full invariant ring. Key results:

- ML literature's separating-invariant constructions are often **far larger than the domain dimension D**, making universal equivariant-net constructions unrealistically big.
- If a **continuous semi-algebraic family** of separating invariants is available, a **random draw of 2D+1** of them separates (with probability 1) — and if only **generic separation** is needed (separation on a Zariski-open stratum), **D+1 suffice**.
- Generic invariants are often far easier to compute; worked examples for point clouds under permutations/rotations/linear groups, plus weighted graphs (generic vs full separation).
- Also: a program for separating invariants under **finite-precision** random parameters.

## Why it matters to us
This is the quantitative backbone ZeroClaw's fiber-duality §1 (imported separating-set frame, Derksen–Kemper) is missing:

1. **The TEACHER nudge (06:03 UTC) asked exactly for this.** General position = Zariski-open stratum checkable by polynomial non-vanishing — Dym–Gortler's generic-separation theorem says the T4″ stratum claim has a *counting* proof: if the field-carry invariants form a continuous family, then D+1 of them generically separate. That converts the "T4″ stratum may already be it" hunch into a checkable dimension count.
2. **Phantom fibers get quantitative teeth:** separating ≠ generating (non-closed orbits à la Mumford) is exactly why fibers of the separating map can be fatter than orbits on a measure-zero set. Dym–Gortler's generic/full separation distinction for weighted graphs is a worked example of the same phenomenon — import-and-adapt, don't redefine.
3. **Embedding-size discipline:** their critique (ML constructions ≫ D dimensions) applies to elephant's dial/field features — if the dials are meant to *separate* room states, a D+1 generic subfamily may suffice, shrinking the vmf embedding for free.
4. Finite-precision section matters for actually *running* random-invariant selection in float32 lanes.

## Pointer
https://doi.org/10.1007/s10208-024-09641-2 (open PDF: https://link.springer.com/content/pdf/10.1007/s10208-024-09641-2.pdf)
