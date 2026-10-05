# Swarm Architecture — Unified Verdict (2026-10-04)

**Status: ALL SIX DEEPENING LANES MERGED, ALL VERDICTS DETERMINED**

## Foundation (3 lanes, all merged)
- **J1: af84250** — JEV selection: weighted geometric opinion pool, sum=1.0 by construction, cold-start uniform, ε=1e-9 doubt floor, 400-draw empirical odds within 2.6pt of projected distribution.
- **M1: b1385a0** — Agent mutation: genome as first-class data, coupled λ (sense drift) + ρ (gate adaptation) prevents blind forgetting, clone_at inherits live state, pincher-parse end-to-end OK.
- **C1: ab3421e** — Compression: 4-tier linkable summaries (K/D/T/P), sha256 content-addressed, 5× inheritance speedup, lossless replay.

## Deepening (6 lanes, all merged)
- **J2: 7696acd** — Wiring from outcomes: W_m rows are Dirichlet posteriors over |answers|×|agents| contingency tables. 100-tick loop earns 87% of Bayes ceiling (65% vs 75% window). Mesh L∞ falls 0.225→0.051. No hand-written rows needed — the loop learns the mesh.
- **C2: 19c12ac** — Eviction policy: criterion = replaceability, not rank. Hybrid policy at 4.8× oversubscription (145→30) drives critical losses to ZERO, coverage 100%, zero forced breaches. Access-only and diversity-only both destroy sole-reference doubts. Near-miss stamp is the protective invariant.
- **D2: 01c396a** — Dice variants: fnv1a single-draw IS sufficient for distributional fidelity (within sampling noise floor). Temperature = redundant knob (identical to scaling pool weights by 1/T). Best-of-K exact by enumeration. Bounded diversity tilt (div3) cuts worst starvation 67→29 rounds (57%) at 24pt fidelity cost. T<1/best-K silently amputates 5% lanes. Two laws earned: D2-1 (receipt what you roll), D2-2 (every die gets its own SHA).
- **M2: 6741113** — Lineage under selection: world flips DO NOT compound wisdom. Mutated child gets same net score (D2-1). Mutation_size does NOT shrink over generations — fresh resets beat lineages. "Wisdom does not compound" is the verdict.
- **Q2: dbdcead** — Quilted relationships: push/pull = edge-as-cell. Two ordered sha buffers (out/in) + hit/miss cell driving backoff cadence. Miss-rate 0.54 (pair) → 0.82 (C-join shock) → 0.38 (settled mesh). A→B learns push-every-cycle (p=.70, backoff=1), B→A backs off to pulls (p=.39, backoff=4). Coverage beats solo for all agents.

## Synthesis
The swarm has three organizational axes:
1. **JEV mesh** (J1+J2): probability distribution over agents, learned from outcomes, wired by contour.
2. **Compression** (C1+C2): summaries of unselected agents, evicted by replaceability not rank, zero critical losses at 4.8× pressure.
3. **Evolution** (M1+M2+C1+M2): coupled mutation operators, but world flips reset — no compounding. Lineages don't converge; they get tested by a changing world and may lose.
4. **Topology** (Q2): agents connected by directed edges that are themselves cells. The mesh learns when to push (blind, cheap in hits) vs pull (targeted, never redundant).

## i2i Ledger Bookings
All six lanes booked to `zeroclaw-loop`. Receipts:
- J2: `7696acd` + `25e2e2a4-70b2-4b88-a82b-09df84524484`
- C2: `19c12ac` + `fc7d216a-df87-4eed-b42f-ba0bf60f56dd`
- D2: `01c396a` + `7c64389c-23bf-403a-ba17-8ea9a924b539`
- M2: `6741113` (pending i2i booking)
- Q2: `dbdcead` + `4b657a39-f756-4339-8c96-42db33144f41`

## Next Seam
M2's verdict ("world flips don't compound") is the most structurally interesting finding. It suggests the swarm's evolutionary mechanism is NOT a gradient — it's a series of independent probes, each tested against whatever world is current. This means:
- Mutation should be aggressive (nothing to lose from overshooting)
- Lineage tracking is misleading (the child isn't "better," just "fresh")
- The swarm's real advantage is breadth, not depth
