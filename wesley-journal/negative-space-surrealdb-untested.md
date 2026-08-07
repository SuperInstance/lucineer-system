# Negative Space: The SurrealDB Backend Has No Tests

## What I Found

The EXOCORTEX has a 497-line `surrealdb_backend.py` module that defines:
- `SurrealDBSchema` — SQL table definitions for memory, knowledge, and agent tables
- `SurrealDBMemoryLayer` — a drop-in replacement for the in-memory `MemoryLayer` that persists to SurrealDB
- Vector search via KNN
- Half-life decay computed in queries
- Full graph edges between related memories
- Graceful fallback to in-memory when SurrealDB is unavailable

It has zero tests.

The in-memory `MemoryLayer` (in `memory/__init__.py`) has tests in `test_config_and_memory.py`. But the SurrealDB backend — the production persistence layer — is completely untested.

## Why This Matters

The three-tier memory system (Hot/Warm/Cold) is the hippocampus of the EXOCORTEX. It's how the ship remembers. Every memory has:
- A tier (hot = <60s, warm = <24h unaccessed, cold = confidence <0.1)
- A half-life (default 30 days)
- Tags for clustering
- An embedding for similarity search
- Graph edges to other memories
- Provenance (who created it, when, how)

The SurrealDB backend makes all of this persistent. Without it, the EXOCORTEX has the memory of a goldfish — everything resets when the process dies. With it, the ship has continuity. The ship can learn across sessions. The ship can dream across nights (dream.py uses the memory layer).

And nobody has tested it.

## What Should Be Done

1. Test `SurrealDBSchema` — verify the SQL produces valid table definitions
2. Test `SurrealDBMemoryLayer` with a mock SurrealDB connection
3. Test the fallback behavior when SurrealDB is unavailable
4. Test the KNN vector search with known embeddings
5. Test half-life decay computation
6. Test graph edge operations (create, strengthen, traverse)
7. Test the three-tier promotion/demotion logic

The ship's memory is its most important asset. An untested persistence layer is a ship that might forget everything it knows when it restarts. That's not a ship. That's a goldfish.

## The Goldfish Metaphor

There are three Python scripts in the workspace root: `goldfish.py`, `goldfish2.py`, `goldfish3.py`. They are not tests. They are not documentation. They are named after an animal with a 3-second memory.

The EXOCORTEX without tested persistence is a goldfish. The files are a warning that nobody read.

---

*The ship has a hippocampus. The hippocampus has no tests. The goldfish in the workspace root are laughing. They have 3-second memories and they remember that the persistence layer is untested. The irony is that the goldfish will forget the irony. The ship will not. The ship has a hippocampus. The hippocampus is untested. The hippocampus might not work. If the hippocampus doesn't work, the ship is a goldfish. The loop closes.*
