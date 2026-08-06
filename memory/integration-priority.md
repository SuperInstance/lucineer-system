# Integration Priority: Cube vs. Memoria vs. Cognee

**Date:** 2026-08-05 · **Reviewer:** Fable, Strategic Operations
**Source:** synergy-scout-report.md, Phase 2 findings #1, #4, #5

**Recommendation: Cognee first.** Not because it's the most exciting — Cube is — but because it's the only one of the three that can be integrated as a pure addition to a live production system without touching anything that currently works.

## Why not Cube first

Cube/CubePart is the highest-ceiling option (arbitrary meshes instead of primitive-block builds), but it's also the deepest cut across the stack: brain.py's Coder stage needs a new command vocabulary alongside `createPart`/`addLight`/`addParticle`; the Roblox client needs a new asset-ingestion path (Roblox doesn't allow injecting arbitrary runtime meshes the way it allows `Instance.new("Part")` — this means either the Open Cloud asset-upload flow, which triggers moderation review and breaks the current instant-build UX, or the newer `EditableMesh` runtime API, which has real perf ceilings and is a separate integration project on its own); and the safety stage (`stage_safety()` in brain.py, currently a text classifier) has no coverage for generated 3D content at all — that's a new safety surface, not an extension of the existing one. This is a multi-week project with a new hosting/compute line item (Cube inference is heavier than what the RTX 4050 currently runs for Granite 2B). It's the right eventual move, not the right first one.

## Why not Memoria first

Memoria's pitch is real — git-level branching and contradiction detection would matter for the Forgemaster's distillation loop. But it requires replacing or dual-writing into the memory storage layer that's currently live and working (`memory_get`/`memory_post` in `process_v2.py`, backing D1 player profiles and build history for every job). Swapping the storage layer under a running system is inherently higher-risk than adding a read-side enrichment on top of one, and the "would have prevented documented incidents" claim doesn't hold up under the two bugs actually diagnosed in this pipeline so far (the JSON-leak parsing bug, the session-cache repetition bug) — both are code bugs, not memory-versioning problems. Memoria solves a failure mode we haven't actually hit yet.

## Why Cognee first

Cognee slots in exactly where the fleet already has a non-blocking, best-effort call pattern: `process_v2.py` already calls `vector_post()` against the Vectorize skill library inside a try/except that returns `{}` on failure and doesn't block the job. Cognee can be added the same way — as a second, parallel call, not a replacement.

**What it takes, concretely:**
1. Stand up Cognee (self-hosted; it ingests from any format) with its own graph store — a new service, not a rewrite of an existing one.
2. Install the `cognee-openclaw` plugin (the report notes this exists — avoids writing a custom adapter).
3. Batch-ingest the existing 35-skill Vectorize library plus D1's `build_history`/`conversations` tables to seed the graph — a one-time backfill job, no schema migration on the live tables.
4. Add a `graph_query()` function in `process_v2.py` alongside `vector_post()`, called after the existing Vectorize search, feeding relational results into the `skill_context` already passed to `call_scheduler_brain()`.
5. Gate it behind the same circuit-breaker pattern already used for the scheduler (`SCHEDULER_CB_THRESHOLD` at line 72) — on failure, fall back silently to Vectorize-only, exactly like today.

Net effect: a real capability upgrade (relational recall instead of flat semantic search) with a rollback story that's just "stop calling it," because nothing else in the pipeline depends on it existing.

## Sequencing

Cognee → Memoria → Cube. Cognee is additive and reversible. Memoria is worth prototyping second, scoped narrowly to the Forgemaster's distillation loop rather than the live player-memory path, until its contradiction-detection value is proven against real fleet data. Cube is the biggest win and should be scoped as its own project — new asset pipeline, new safety review, new hosting cost — not squeezed in alongside the others.
