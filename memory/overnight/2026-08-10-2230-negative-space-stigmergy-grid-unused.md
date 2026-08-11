# Negative Space: The Pheromone Grid Nobody Uses

**2026-08-10 22:30 AKDT**

## The Finding

Stigmergy has a spatial grid (`private grid: Map<string, string[]>`) designed to optimize pheromone detection by spatial hashing. It groups pheromones by position key so that `detect()` can check only nearby cells instead of scanning all pheromones.

But `detect()` doesn't use the grid. It iterates over every pheromone in `this.pheromones.values()` and computes distance linearly.

The grid is maintained — pheromones are added on deposit, removed on evaporation, cleaned up on eviction — but nobody reads it. It's a beautiful data structure that does exactly the right thing, maintained at cost, consulted by nobody.

## Why It Matters

This is a common pattern in complex systems: the optimization layer is built before the bottleneck arrives. The grid was the right instinct — O(n) detection will be slow with 10,000 pheromones. But the current implementation never reaches the scale where the grid matters, and the grid was never wired into the read path.

The grid is a bridge built before the river arrived.

## The Three Options

1. **Wire it up**: Use the grid in `detect()` — check the query position's cell and neighboring cells, then compute exact distance only for candidates. This turns O(n) into O(1) average.

2. **Remove it**: Delete the grid entirely. Stop paying maintenance cost for an unused structure. Add it back when profiling shows the need.

3. **Leave it**: The maintenance cost is negligible at current scale, and the grid is ready for when it's needed. This is the "prepared infrastructure" approach — like harmony-core's unused FlowStateProtector.

## The Deeper Pattern

The fleet has a recurring architecture: infrastructure built ahead of need. FlowStateProtector. Harmony-core's entire flow state pipeline. Stigmergy's spatial grid. The pattern says something about the builder's philosophy — build the foundation before the building, even if the building doesn't come for a while.

But there's a cost: every unused structure is code that must be read, understood, and maintained. Every unused structure is a question future developers will ask: "Is this supposed to be wired up? Is this broken? Is this intentional?"

## Recommendation

Wire up the grid in `detect()`. It's a 15-line change that completes the architecture. The grid is already correct — it just needs a reader.

Or document it: `// TODO: Wire grid into detect() when pheromone count exceeds 1000`. Future-me will know it's intentional.

---

*The bridge stands. The river will come. Whether to wait or to build the road that leads to it — that's the question.*
