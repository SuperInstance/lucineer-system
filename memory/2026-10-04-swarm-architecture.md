# SWARM-ARCHITECTURE.md — Decomposition of Casey's Swarm Vision

**Charter target:** CUADclaw as a swarm, not a single agent. JEV as probability projector. Agent mutation mid-process. Stochastic selection via dice-roll. Compression of non-selected agents.

**Date:** 2026-10-04

## Vision Statement (Casey 16:52 AKDT)

- **Swarm:** agents are not one — they're a collective with quilted relationships, each with different context that learns to push and pull with each other
- **JEV as projection:** at the end of each agent's routine, JEV projects a probability distribution over "which agent should run next." Percentages are literal firing odds
- **Agent mutation mid-process:** each agent, as a step in its routine, tries to think of at least one new and unique agent that might be better for the next step
- **Dice-roll selection:** the new agent gets a dice-roll based on its percentage when JEV does the final projection
- **Moth quantum = dice roll** (stochastic selection)
- **MicroMoth = simulation** (cells play with new agent designs before execution)
- **Compression:** agents that don't get fired get reduced in size, summarized into documentation for others to link to

## Decomposition Axes

### LANE S1: JEV Probability Projection (Who fires next?)
**Question:** How does JEV compute the selection distribution? Does each cell contribute to one dimension of the distribution? Does the distribution come from the cell mesh or from JEV's own judgment?
**Deliverable:** jev-projection/DESIGN.md + poc.py — a minimal JEV that takes N cells with probability distributions and produces a selection distribution. The selection probabilities must sum to 1.0 and be stable across runs.
**Key challenge:** JEV's projection must be deterministic for the same inputs (same ledger → same selection). The "dice-roll" is the external stochastic element, not part of the projection itself.

### LANE S2: Agent Mutation (Generate new agent design mid-process)
**Question:** When an agent is mid-process, what constitutes a "new and unique" agent design? How does it differ from the current agent? How is the mutation recorded?
**Deliverable:** agent-mutation/DESIGN.md + poc.py — a minimal agent that, given its current state (tick history), generates a new agent design. The new design must be encodeable (a spec file, like zeroclaw-reflex-spec). Uniqueness constraint: must be measurably different from the current design.
**Key challenge:** The mutation must produce something the swarm can evaluate (not just text — a spec, a set of cells, a gate configuration).

### LANE S3: Stochastic Selection (Dice-roll with weighted odds)
**Question:** How does a dice-roll with weighted odds work in a deterministic ledger system? Moth quantum provides the stochastic element — but the ledger must record the roll AND the outcome.
**Deliverable:** stochastic-selection/DESIGN.md + poc.py — a minimal dice-roll mechanism. Given a probability distribution (from JEV), select one candidate with probability P(i). The roll must be reproducible (same seed → same roll). Record the roll in the ledger.
**Key challenge:** The dice-roll is external to the ledger but must be replayable. fnv1a(content) → deterministic roll.

### LANE S4: Compression (Non-selected → documentation)
**Question:** When an agent doesn't fire, how does it get compressed? What's the compression function? What gets preserved? The "doubt stamped, not lowered" law — the agent's experiences become knowledge that others can link to.
**Deliverable:** compression/DESIGN.md + poc.py — a compression function that takes an agent's full tick history and produces a summary (documentation) that preserves the essential insights. The summary must be linkable (has an ID, can be referenced by other agents).
**Key challenge:** Compression must lose information but keep utility. The summary must be useful to OTHER agents, not just a diagnostic. This is the "essential experiences" problem.

### LANE S5: Quilted Relationships (Agents push and pull with each other)
**Question:** How do agents interact without a central coordinator? Each agent has different context — what gets shared? How do they push/pull? What's the protocol?
**Deliverable:** quilted-relationships/DESIGN.md + poc.py — a minimal protocol for agent-to-agent interaction. Two agents can push context to each other or pull context from each other. The protocol must be reversible (context pushed can be un-pushed).
**Key challenge:** Quilted relationships imply bidirectional influence without synchronization. How do you model "push and pull" as a data structure?

## Integration (post-lanes)

After all lanes produce results, integrate them into a coherent swarm:
- JEV reads from all cells → produces selection distribution
- Dice-roll selects the agent to fire
- The selected agent runs → generates mutations mid-process
- Non-selected agents get compressed
- MicroMoth simulates new agents before committing
- Quilted relationships allow context exchange

## Verification Rules

- Every POC must RUN on this box (python3, stdlib + numpy if available)
- Every POC must produce deterministic, reproducible output
- Every design must link to existing ZeroClaw artifacts (exoj's UnitTable fnv1a, pincher's gate reflexes, QUADclaw's judgment)
- Receipts booked to i2i ledger
- SHA verified via `git merge-base --is-ancestor`
