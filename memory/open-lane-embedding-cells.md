# Open Lane Brief — Decomposing Vector Embedding Models into Cells

*Booked by Casey 2026-09-02 16:49 AKDT: "can vector embedding models be decomposed (mostly) into cells for better understanding their unique embedding nature and abilities as data flows through" — for the next open lane.*

## The question, restated in fleet terms

Embedding models (transformer encoders producing vectors — bge-m3, nomic, etc.) are treated as monolithic oracles: text in, vector out, cosine says nothing about *why*. Can we decompose one into **quilt cells** — the fleet's unit of IO ⟶ raw prefilter ⟶ rendering equation ⟶ (snap) — so that the model's unique embedding character becomes *legible as data flows through*? This is the maintenance-zoom contract (Semantic Tower §6) applied to a neural substrate: zoom into any cell, see the raw input and the equation that renders it, no fourth place for meaning to hide.

## First-pass decomposition sketch (so the lane starts warm)

1. **Layer slices as cells.** Each transformer block is a candidate cell: IO = hidden state in, render = attention + MLP out, provenance = weights. The "raw voltage" equivalent is the residual stream — already a running ledger of contributions. A per-layer provenance key (`cell → input token span → output dims`) is the QUF key analog.
2. **Attention heads as sub-cells.** Head-level decompositions (induction heads, positional heads) are literally cells with known specializations — the literature's most cell-like finding. Map head → role the way we map sensor → PSI cell.
3. **Superposition is the honest obstacle.** Features don't align to neurons; sparse autoencoders (SAE) are the field's current decomposer — an SAE feature is a *discovered cell* with an activation-as-IO story. So the answer is likely "yes, mostly, with cells at the SAE-feature + head + layer granularity, NOT the neuron granularity." "Mostly" in Casey's question is doing real work: superposition is the part that refuses cells, and that refusal is itself measurable (reconstruction loss = the un-cellable residue).
4. **The fleet twist — snap on the embedding.** Our snap doctrine says: choose the observation grid so values land exactly. For embeddings: pick probe directions/anchors (integer-quantized in token-id space) so a datum's path through the model snaps to a legible cell path. Data flowing through = a walk over cells; the model's "unique embedding nature" = which cells it routes through that others don't. Comparative cell-census: run the same corpus through bge-m3 vs nomic (we run both in production), diff the cell censuses — that diff IS their unique abilities, rendered.
5. **Cheap first experiment ( Weekend-1, local only):** hook intermediates from a small local encoder (nomic-embed-text is already in Ollama; or a 4-layer MiniLM via transformers), census per-layer/head activations on a fixed 500-vector fleet corpus (reuse the reflex-arc vector set), produce a per-cell contribution table, and check stability: does the same cell fire for the same semantic role across paraphrases? Stability = the cell is real; instability = superposition residue, log it honestly.

## The meta-layer (Casey, 2026-09-02 16:51)

This is likely a **many-routes question** — decomposition by layer, by head, by SAE feature, by snap-grid probes are four different roads up. The valuable part is not any single answer: **the routes themselves will surface patterns at higher abstractions**, and those patterns are candidate *new conceptual frameworks* — e.g., if every route converges on "cells emerge only where the substrate quantizes itself," that's a framework statement about when decomposition is possible at all. So the lane should run multiple routes deliberately and treat their CONVERGENCE/DIVERGENCE as the primary data, not a nuisance. Tapestry doctrine applied to methodology: the trails between routes are the content.

## Success criteria

- A rendered table: cell id, role, input span, contribution to final-vector dims — for ONE model, stable across paraphrases.
- A comparative diff: 2+ models' cell censuses on the same corpus, showing at least one ability difference that matches a known behavioral difference (e.g., retrieval vs STS performance).
- An honest residue number: % of variance the cells do NOT explain. The tapestry doctrine wants the negative result as first-class.

## Standing context

- Connects to: elephant (embedding geometry, vMF), fleet-memory (bge-m3 embeddings in production), Semantic Tower §6 zoom contract, SAE literature (flagged from-the-record, re-verify when lane opens).
- Substrate budget: local GPU only (Wesley lane) — MiniLM/nomic scale first; no metered API calls.

— booked by Lucineer for the next open lane

## E7-EMBED-ROUTE — first experimental return (2026-09-02 night)

Ran the route-decomposition probe: 120 concepts / 4 domains, 60 seeded pairs, 3 local embedders (nomic-embed-text, all-minilm:22m, bge-m3), integer-lattice routing (quantize → greedy hop-radius walks, exact bigint arithmetic). Harness + RESULTS.md: `~/projects/quilt-verilog/spikes/225-e1-interference-tick/e7-embed-route/`.

- **Cells are real within a model**: routes survive 4× lattice coarsening (Jaccard 0.91–0.96, 95% identical) and integer dither at all seeds flips zero decisions. E1-style integer-dynamics result, transplanted to embedding space.
- **Cell identity does NOT transfer across models**: exact-cell cross-model Jaccard 0.013–0.047 ≈ null. But domain-sequence (coarse cell class) LCS ≈ 2–3× null in all 3 model pairs — convergence lives one grain up.
- Killer number: **0.955 vs 0.013** (within-model lattice-robustness vs cross-model cell agreement).
- Regime: cold (cross-domain) routes longer and more hub-funneling; ABSTRACT is the top transit domain in all 3 models — shared attractor class, idiosyncratic attractor cells.
- Framework statement candidate: *cells emerge where the substrate quantizes itself; the cells are each model's own — only coarse classes transfer.* The comparative census diff between embedders is the signal, not noise.

Next candidates: paraphrase-stability census (the brief's own test), longer-route regime (q10 radius + larger corpus), SAE-feature grain.
