# collective-unconscious × quilt — synergy study

*2026-08-20 · Captain's assignment: "SuperInstance/collective-unconscious needs work and updating. study the quilt repos and synergize with the greater projects."*
*Study performed by subagent (dsf-collective-unconscious). Read-only everywhere except collective-unconscious local commits + this report.*

---

## 1. What collective-unconscious currently ingests

Cloudflare Worker (Vectorize `fleet-unconscious-1024`, Workers AI `@cf/baai/bge-m-3`, 1024 dims; D1 `ingestion_state` for watermarking). A "moments" index: JEPA reading vector as a first-class citizen beside time (`ts`) and space (`spaceId`) stamps. **116 tests pass** (5 files: embed 14, ingestion-pipeline 21, jepa 14, temporal 25, readingsIndex 42).

| Source | Modality | Event types flowing in | Route |
|--------|----------|----------------------|-------|
| The Tap | `tap` | tap-conversation, open-mic, open-mic-response, diary, creative, poker-hand | `/ingest/tap` |
| Hermes | `hermes` | sounder-observation, catch-event | `/ingest/hermes` |
| MUD Engine | `mud` | arbitrary `eventType` game events, NPC awakenings, room transitions | `/ingest/mud` |
| Daily maintenance | — | shape-snapshots (cluster centers, JEPA trajectories) | `/ingest/daily` |
| Elephant seam | `moments` | elephant `jepa_rag.py` moments JSON (readings + ts + space_id + meta) via `scripts/momentsToJson.ts` | offline script |

Queries: `/embed`, `/search`, `/shape`, `/jepa/:agentId`, `/cross-modal`, `/health`. State: `migrations/001_ingestion_state.sql`.

## 2. What the quilt grid emits that collective-unconscious SHOULD index

**quilt** (JS) + **quilt-rust** (Rust, v0.2.0, 51+ tests, 10 examples): a reactive typed cellular runtime — "a spreadsheet where every cell is a live, addressable capability." Cell kinds: `value, formula, api, program, sensor, listener, router, io`. The grid already emits:

- **Cell-change event stream** — `engine.subscribeAll()` / `subscribe(cellId)`, SSE `GET /api/events` in the harness guide. Every change: `(cellId, value, prev, caller context, ts)`.
- **Evaluation trace log** — append-only, replayable (docs/architecture.md).
- **Sensor pushes & io cells** — external readings and bidirectional effects; agents present as `program`/`api`/`listener` cells.
- **CellLedger (quilt-rust, the crown jewel)** — `packages/core/src/ledger.rs`: double-entry `before → after` per cell, hash-chained, tamper-evident, with `imbalance` (= surprise = prediction error) as a recorded value. 16 unit tests, not yet wired into engine evaluation.
- **The fractal-JEPA identity (documented, unproven in code yet)**: `fleet-as-fractal-jepa.md` + `field-edge-ledger-bridge.md` prove (to 1e-12, numpy) that the ledger's `imbalance = ‖after − before‖` IS the elephant's field-edge `d_mu` at cell grain — the same directed edge at pin / room / model / fleet scale. The elephant's room-field (vMF, `d_warmth`, `κ`) is the room-grain version.

**This is the synergy thesis**: the grid emits first-person `before → after` edges; the elephant emits room-grain field edges; collective-unconscious stores moments with reading vectors. All three are the same object at different zoom. collective-unconscious should index the grid's edges as moments.

## 3. Synergy proposals (concrete)

### P1 — `/ingest/grid`: the CellLedger as a moment source (highest value)
- **What**: new `Modality = "grid"` in `src/ingestion-pipeline.ts` (mirror the tap/hermes/mud blocks); new route `/ingest/grid` in `src/index.ts`; moments shaped as `{ text: "<cellId> → <value snapshot>", readings: {presence, mood?…} or imbalance-derived, ts, space_id: <sheet/room>, meta: {cellId, before, after, imbalance, caller} }`.
- **Where it plugs in**: `src/ingestion-pipeline.ts` (new `ingestGrid()`), `src/index.ts` (route), `test/ingestion-pipeline.test.ts` (+~8 tests).
- **Unlocks**: cross-modal search between grid state and everything else — "show me everything that felt like this feed ball" now includes grid moments; `/jepa/:agentId` can run trajectory prediction on a grid cell's ledger (persistence prior = zero-order JEPA is already the ledger's default predictor); the unconscious becomes the fleet's second-person view of the grid's first-person record.

### P2 — Grid room-state as space stamps + presence
- **What**: a sheet per fleet room (roadmap: "cells are in rooms"); presence = live `sensor`/`io`/`program` cells; warmth = elephant field reading surfaced as a cell (`room.warmth`). Emit room snapshots as grid moments with `space_id = room`.
- **Where**: quilt side emits via listener cells; collective-unconscious ingests via P1's route with `space_id` set.
- **Unlocks**: `queryBySpace` over grid rooms ("what did the wheelhouse cell-graph feel like last week?"), presence-aware retrieval (who was in the room when this moment was minted).

### P3 — Crab-traps reef lineage as moments ("the reef's unconscious")
- **What**: crab-traps already mints rooms/objects from player work (`GET /lineage/room/:id`, `/genealogy`, hourly lure breeding). New `/ingest/reef` route ingesting room births, object minting, lure-breed events as moments with elephant readings.
- **Where**: `src/ingestion-pipeline.ts` + route; `wrangler.toml` service binding to the PLATO API (mirror the commented `TAP_API_URL` pattern).
- **Unlocks**: the reef's self-written brochure becomes retrievable by feeling; cross-modal "which poem feels like the Dock"; lineage as a queryable memory graph.

### P4 — fleet-wiki as a lore modality
- **What**: 762 pages / ~395k words already embedded (bge-base-en-v1.5) into `lucineer-memory` (D1) + its own Vectorize. Cross-index wiki page updates as `creative`/`lore` moments in the unconscious so lore pages carry readings + time/space stamps.
- **Where**: new source in the hourly cron pull set; `scripts/` adapter reusing `momentsToJson.ts` shape.
- **Unlocks**: "find the lore page that feels like this poem"; the wiki (hippocampus) and the unconscious (deep memory) stop being duplicate corpora with incompatible shapes.

### P5 — Expose the field: `/field/:spaceId` and ledger-derived surprise
- **What**: daily maintenance already rebuilds cluster centers; add a read route returning a room's field trajectory (elephant `field_before → field_after`, `d_warmth`, `κ`) plus aggregate ledger imbalance — the fleet's JEPA loss over time.
- **Where**: `src/index.ts` route + `src/jepa.ts` extension.
- **Unlocks**: the fleet's own training signal visible ("what surprised the grid today"); deadband detection (imbalance ≈ 0 = habit loop) queryable like stuckness in `/jepa/:agentId`.

## 4. Gaps / aging in collective-unconscious itself

- **D1 binding is commented out in `wrangler.toml`** (`# [[d1_databases]]` + commented `DB` binding) while README claims "Ingestion state tracked in D1" and the pipeline queries `ingestion_state`. Migration exists; the deployed worker can't track watermarks until uncommented + `wrangler d1 create collective-unconscious-state`. **Config, not markdown → flagged, not fixed.**
- **Service bindings for Tap/Hermes/MUD URLs are commented** in wrangler.toml (`TAP_API_URL`, `HERMES_FRAMES_URL`, `MUD_API_URL` vars) — the hourly cron pulls from example URLs. Fine as scaffolding; needs real endpoints at deploy time.
- **Stale repo-name refs: 0 found in markdown.** The org-wide rename sweep already landed here (commit `2065a2d` "docs: org-wide link repair — repo renames + master→main", today). README links `hermes-avatar`, `mud-engine`, `the-tap`, `elephant` — all current. `docs/` contain no repo links. CI workflow already targets `[master, main]`.
- **No grid modality** — nothing about quilt anywhere in the repo (expected; quilt is new).
- **hermes-avatar has no local clone** under `/home/eileen/projects/` (hermes-perception, hermes-cloudflare, hermes-construct, hermes-nmi, hermes-ob1-core, hermes-reader exist). hermes-perception README references `SuperInstance/hermes-avatar` src paths — fleet-level note, out of scope for this repo.
- **Compatibility date** `2024-09-01` + wrangler `^3.80.0` — aging but functional; not blocking.
- **Code-level items left for separate review** (not changed): `src/ingestion-pipeline.ts:70` comment "mirrors from the-tap/workers/tap-games" (check path against the-tap repo layout); no `hermes-perception`→`hermes-avatar` string issues found in src/.

## 5. Commits made (local only, no push)

1. `docs: collective-unconscious update — Deployment: document the commented-out D1 binding` (README.md — makes the README's "tracked in D1" claim match the actual wrangler.toml state).

## 6. Suggested next steps (needs Captain's call)

1. Uncomment + create the D1 database (config; needs `wrangler d1 create` + deploy).
2. Build P1 (`/ingest/grid` + CellLedger moments) — highest leverage; the ledger already has the data shape the unconscious wants.
3. Wire `CellLedger` into quilt engine evaluation (quilt-rust cortex agenda item) so the event stream exists to ingest.
