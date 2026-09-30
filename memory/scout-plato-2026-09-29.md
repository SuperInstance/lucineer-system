# PLATO deep-scout — lane PLATO (2026-09-29)

Fed the plato-cf rebuild (design receipt: /home/eileen/projects/plato-cf/README.md). Read-only scan; local clones where present, rest cloned to /tmp/scan-plato/.

## Per-repo digest

**plato-stable-early-version** (local) — Seed model: tiles = unit of knowledge, rooms = collections. Archived 2026-05-13 ("never fully developed; absorbed into plato-sdk"). Mechanism already inherited by plato-cf design.

**tile-memory-early-version** (local) — The Tile Compression Theorem: lossy, reconstructive memory. Tile fields: `constraints` (immortal facts), `context_required` hints, `emotional_valence` (salience 0-1), `compression_ratio`, `round_number`. Mechanisms worth building:
- `RateDistortion.compute_curve` — Lagrangian R + λ·D optimal point so tiers are *chosen, not guessed*.
- `TelephoneGame.play` — real LLM round-by-round transmission; returns `fact_timeline`, `drift_curve`, `novel_claims` per round, and **`crystallization_round`** (round where output stops changing) — perfect engine for the round-3 telephone-game endpoint.
- `fact_survival_rate` — per-fact bool timeline across compression chain (already pinned as demotion receipt field).
- **`lattice_snap_rate(hallucinations, valid_set)`** — fraction of fabrications that match known-valid items = "structurally plausible" measure. Cheap, string-set based; ideal second metric on demotion receipts and meaning-search QC.

**plato-hologram-early-version** (/tmp/scan-plato) — Vectorized field experiment, 1KB scaffolding, archived 2026-05-13 ("never developed"). But field.py is a gem: `HologramField` maintains an **incremental running centroid + boundary per room** (O(1) update per tile add), `density(point)` from k-NN distances, `onboard()` snapshot for newcomers. Worth stealing as a cheap room-level "field signature" column in D1 (no Vectorize query needed for coarse onboarding context); deterministic hash-embedding is a fallback when no model available.

**plato-sdk** (local, production) — Client for PLATO store: Python (`client.py`, `skills.py`, `equipment.py`, CLI) + JS (`client/room/tile.ts`). Agents live in the store (skills/equipment modules = the room is the agent's habitat). Steal: SDK-thin shape — client methods mirror REST 1:1; skills/equipment as tile categories.

**plato-portal** (/tmp/scan-plato, active) — SuperInstance Python SDK: persistent agents as markdown files under `~/.superinstance/agents/{name}/`, `remember(text, category=)` / `recall(q)` with timestamps, Fleet with tag/broadcast/dispatch, **thread-safe LRU agent cache with TTL eviction**. Steal: category-tagged remember/recall + LRU-TTL caching for plato-cf Python client hot rooms.

**cocapn-plato** (/tmp/scan-plato, v3.2.0, 36 tests) — The real engine: `QueryEngine` with 12 operators, dict-where clauses compiled to predicates, full-text predicate, sort, **aggregate**. Steal: compile-where-to-SQL pattern for the D1 keyword search + an `/aggregate` endpoint (count/group) plato-cf v1 lacks.

**fleet-memory** (local, production Rust) — sqlite-vec vec0 vtab + chunks table, cosine search. Steal for Vectorize mapping:
- **Provider-tagged index identity**: `index.<provider>.<model>.<dims>.db` — encode provider/model/dims in Vectorize index name + metadata so embedding models swap without rebuild.
- **Atomic pointer swap** via rename + **checkpoint per batch** (WAL/flock locally → batch upserts + idempotent re-index in Workers).
- O(chunk) streaming ingest.

**bare-metal-plato** (local) — C client + MCP server for IoT; 5-step embodiment handshake (Discover → Assess → Bridge → Confirm → Upgrade), 5 turbo-shell autonomy levels. Steal (later): expose plato-cf as an MCP server (bare-metal already has the C MCP pattern), and the staged-handshake shape maps to tier-lifecycle transitions.

## Top 3 plato-cf-relevant finds (booked to ledger)

1. **tile-memory TelephoneGame + RateDistortion** — crystallization_round/drift_curve/fact_timeline make decay a *simulated, receipted* act; powers `/tile/demote` honesty pin and the round-3 telephone-game endpoint.
2. **tile-memory lattice_snap_rate** — cheap hallucination-plausibility metric; attach to demotion receipts + meaning-search QC.
3. **fleet-memory provider-tagged index identity + atomic swap + per-batch checkpoint** — the exact pattern for Vectorize: name/tag indexes by provider.model.dims, batch idempotent upserts, swap models without rebuild.

Honorable mention: hologram's per-room running centroid/boundary as a D1 field-signature for cheap onboarding.
