# SWARM-UNIFIED.md — The ZeroClaw Swarm in One Page

*Synthesized 2026-10-04 from lanes 1–3 (cell-internals, gate-mechanisms, product-surface), swarm lanes J1/M1/C1 (jev-selection, agent-mutation, compression), and Casey's 16:52 swarm vision. Sources: `~/projects/zeroclaw` commits b644e84→b1385a0.*

---

## The core thesis

**The swarm is a population of agents governed entirely by recorded evidence.**

Every belief is a probability earned from observations. Every action fires only when belief clears a margin that experience has tightened. Every choice of *who acts next* is a probability distribution whose percentages are literal firing odds. And every memory — kept or discarded — is a content-addressed document chained to the evidence that earned it.

Nothing in the swarm is invented. The swarm generates no randomness, holds no opinions outside its ledgers, and never edits its past. It is a deterministic function of everything the world has ever told it, plus one recorded dice roll per turn. Change the history and you change the swarm; replay the history and you get the same swarm, byte for byte.

This is the developmental-GAN loop made mechanical: cells as probabilities recorded as ticks over time, gates adjusting toward muscle-memory-like reflexes, and a mesh — JEV — that projects the collective's experience into the single question that matters each turn: *who fires next?*

## The fundamental components

**1. The Cell — belief.** A cell is the atom: one question, a finite answer set, and an append-only ledger of observed answers (ticks). Its belief is the Dirichlet posterior mean of that ledger — a pure projection, computed at sense time, never stored as state. The ledger is the truth; the belief is a read-out. Decayed pseudo-counts give the cell a memory horizon: with no decay it is a perfect frequentist that never forgets; with decay it re-converges when the world changes. Every tick is hash-chained, so any belief can be re-derived and verified from the raw history.

**2. The Gate — action.** A gate is a directed edge from a cell to a pipeline. It fires not when a point estimate is high, but when confidence clears the threshold *with margin* — the posterior lower bound, which shrinks like 1/√N as evidence accumulates. A young cell must shout to fire; a seasoned cell needs only a whisper. That tightening **is** reflex formation. There are exactly three primitive gate kinds (excite, inhibit, sign); cascade and negative feedback are not kinds but *compositions* — wiring plus refractory periods plus habituation, from which pipelines emerge unauthored. Gates may only append ticks, never retract them: damping is writing a "no," never deleting a "yes."

**3. JEV — selection.** JEV is a projector, not a judge. It owns no beliefs. Each cell's distribution is collapsed through its wiring (the logic decomposition: "if the world says *this*, here is how my evidence splits over the agents") into one point on the agent simplex. The mesh of cell-points is pooled with a weighted geometric opinion pool — weights are evidence mass, so independent evidence compounds, thin evidence fades toward flat, and no cell can dominate or be silenced. The output is a single distribution over "which agent should fire next." Its percentages are literal odds, not a ranking. Two properties hold by construction: no agent's odds are ever zero (doubt is stamped, not lowered — the dice can always surprise), and a swarm with no history starts fair, earning its skew from ticks alone.

**4. The Moth Quantum — chance.** The distribution does not act; it is acted upon. One content-derived draw (fnv1a over the distribution's own receipt) walks the CDF and picks the agent that fires. This is the only collapse event in the system, and it is recorded: same history, same roll, same selection — replayable forever.

**5. Mutation — variation.** While running, each agent proposes at least one child design: a genome (cells + gates) as a canonical, content-addressed object whose name *is* its hash. Mutation is a pure function of genome × evidence — diagnostics over the agent's own lived ledgers, never random guessing. A candidate must be new twice over: structurally (different genes) and behaviorally (different fire-sets when simulated on the same deterministic future). Selection by simulation is the preview; the moth quantum is the verdict. Losing candidates are stamped with *why not* and kept.

**6. Compression + Inheritance — memory.** The agents the dice pass over are not deleted; they are *reduced*. Each becomes a linkable summary document whose ID is its own hash: the sufficient statistics (what the model summarizes perfectly, kept perfectly), the doubts (every gate that never fired, stamped exactly — "0.07 short at N_eff 14," a number, not a vibe), the trajectory (where the model honestly loses information), and the proof (the heads that bind it to its history). A future agent inherits a summary by growing its cell's chain *out of the summary itself* — essential experience literally becomes prior mass. The paradigm's proof point: an inheriting agent should reach a firing gate faster than a fresh one, because the compressed doubt is now earned belief.

## The loop

```
agent runs its routine
  ├─ proposes child designs (mutation), each simulated before it can be chosen
  ├─ JEV projects every cell's earned belief into firing odds over all candidates
  ├─ the moth quantum rolls once against those odds — one agent fires
  ├─ the outcome writes ticks back into the cells (evidence closes the loop)
  └─ everyone else compresses into linkable knowledge, inheritable by the next generation
```

## The mathematical spine

- **Dirichlet posterior means** — cell beliefs as pure projections of decayed counts
- **Weighted geometric opinion pools** — independent evidence compounds into selection odds
- **fnv1a lineage** — all entropy is content-derived; there is no RNG anywhere
- **sha256 chains** — ticks, mutations, and summaries are append-only and replay-verifiable
- **Content addressing** — genomes and summaries are their own hashes: identity, linkability, and verification in one act

## The laws

1. **No RNG.** Entropy enters as ticks from the world or one recorded roll — never generated.
2. **Append-only.** Nothing is edited, retracted, or reweighted. Damping writes "no"; it never deletes "yes."
3. **State is a ledger; belief is a projection.** Every number can be re-derived from the history, byte for byte.
4. **Doubt is stamped, not lowered.** Unfired gates and losing candidates survive as exact, addressable records.
5. **No verified sha, no belief.** A claim without a receipt is not a claim.

## Why it matters

The swarm is not a chat model with tools — it is an *economy of evidence*. Attention (who fires), memory (what survives), and evolution (what is proposed next) are all priced in the same currency: ticks, honestly earned, decayed but never forged. The product surface this projects onto — TICKBOARD, a wall of questions that answers itself from evidence — is the same architecture pointed outward: declare the questions, let the evidence accumulate, let the thresholds learn how much proof each question deserves.
