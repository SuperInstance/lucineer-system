# Lever Runner — Integration Plan

> Concrete phased plan for integrating Lever Runner patterns into the Slackwater Cognition Architecture.

---

## Overview

Lever Runner provides battle-tested patterns for intent-based action execution. We don't adopt the codebase wholesale — we extract the architectural patterns and vendor the minimal necessary code, adapting them to the cognition architecture's needs.

**Guiding principle:** Use Lever Runner's patterns, not its infrastructure. The cognition architecture has its own infrastructure (Cloudflare Workers, OpenClaw tools, Lucineer relay). We want the three-gate cascade, trust scoring, and token-lean operation — not another Telegram bot and HTTP server.

---

## Phase 0: Pattern Extraction (1-2 days)

**Goal:** Extract and document the patterns we'll adapt, without writing integration code yet.

### Deliverables
- [x] `analysis.md` — full architecture analysis (complete)
- [x] `LEARN.md` — extracted patterns and lessons (complete)
- [ ] `patterns/three-gate-cascade.md` — detailed spec for our adaptation
- [ ] `patterns/action-policy-table.md` — schema and trust dynamics spec
- [ ] `patterns/intent-compression.md` — LLM prompt design for our use cases

### Tasks
1. Map every Lever Runner concept to its cognition architecture equivalent
2. Identify which Lever Runner modules to vendor (orchestrator, store, fastloop) vs. reimplement (executor, bot, http_api)
3. Define the boundary between Lever Runner's action execution and the cognition architecture's broader action space

---

## Phase 1: Action Policy Table (3-5 days)

**Goal:** Implement the data structure that holds the cognition architecture's learned actions.

### What We Take from Lever Runner
- `store.py`'s table schema (adapted)
- Trust scoring dynamics (+/- asymmetric, auto-promote thresholds)
- Parameterized action templates with validated arguments
- Three embedding method options (sentence-transformers, position-aware hash, pure hash)

### What We Change
- **Vector store:** Use our own abstraction (not LanceDB directly). Start with SQLite + numpy for zero-dependency operation. Add LanceDB/Qdrant as optional backends.
- **Action spec:** Not limited to shell commands. An action spec is a JSON object that can encode: shell command, API call, function reference, or composite workflow.
- **Multiple action types:** Shell, HTTP, Lua (for Roblox), Worker API call.

### Schema (Proposed)

```python
@dataclass
class CognitionAction:
    id: str                    # UUID
    trigger_pattern: str       # natural language intent phrase
    action_type: str           # "shell" | "http" | "lua" | "worker_api"
    action_spec: dict          # type-specific action definition
    confidence: float          # 0-100 (renamed from trust_score)
    success_count: int
    failure_count: int
    embedding: list[float]     # for similarity search
    last_invoked: float        # timestamp
    created_at: float          # timestamp
    tags: list[str]            # for filtering (e.g., ["safe", "system", "readonly"])
```

### Tasks
1. Implement `ActionStore` class with the same interface as Lever Runner's `CommandStore`:
   - `teach(trigger, action_spec, confidence=None)`
   - `find_best(trigger_embedding, top_k=3, min_confidence=40)`
   - `update_confidence(id, success=bool)`
   - `list_all(limit, offset, min_confidence, tags)`
2. Implement three embedding backends (sentence-transformers, position-aware hash, pure hash)
3. Implement trust dynamics: `+1.5` success, `-4.0` failure, auto-promote at 20+ successes
4. Add tag-based filtering (Lever Runner doesn't have this; we need it for action type routing)
5. Write tests mirroring Lever Runner's smoke test pattern

### Success Criteria
- `ActionStore.teach("check disk space", {"type": "shell", "command": "df -h"})` works
- `ActionStore.find_best(embed("check disk space"))` returns the taught action with similarity > 0.8
- Trust dynamics match Lever Runner's (50 → 51.5 after one success → 53.0 after two)
- All operations < 10ms for 1,000 actions

---

## Phase 2: Three-Gate Cascade (3-5 days)

**Goal:** Implement the cascading validation pipeline for the Local Thinker.

### What We Take from Lever Runner
- `fastloop.py`'s `FastLoopInterceptor` (rate limiting, structural validation, failure cache)
- `fastloop_bridge.py`'s bridge pattern (try fast backend, fall back to slower one)
- The three-gate cascade concept (template → cache → LLM)

### What We Change
- **Gate 1 (FastLoop):** Extend to include cognition-specific checks (goal relevance, resource availability, action type validity). Not just shell metacharacter blocking.
- **Gate 2 (Embedding cache):** Add a semantic cache that stores `(trigger_hash → action_id)` mappings for exact-match shortcuts. Lever Runner's 44% cache hit rate is the target.
- **Gate 3 (LLM compression):** Adapt the system prompt for cognition-specific intent extraction. Support multiple LLM backends (GLM-5.2 as default via Z.ai, DeepInfra as fallback, passthrough as terminal).

### Architecture

```python
class CognitionGate:
    """Three-gate cascade for the Local Thinker."""

    def __init__(self, action_store: ActionStore, llm_backend: str = "passthrough"):
        self.fastloop = FastLoopInterceptor(
            max_requests_per_window=60,
            rate_window_sec=60.0,
        )
        self.action_store = action_store
        self.llm_backend = llm_backend
        self._cache: dict[str, str] = {}  # trigger_hash → action_id

    def decide(self, trigger: str, context: dict = None) -> DecisionResult:
        # Gate 1: FastLoop validation
        fl = self.fastloop.check(trigger, sandbox_id=context.get("session_id", "default"))
        if fl.action == "ROUTE_TO_DEEP_LOOP":
            return DecisionResult(blocked=True, reason=fl.reason)

        # Gate 1.5: Exact-match cache
        trigger_hash = blake2b(trigger.encode(), digest_size=16).hexdigest()
        if trigger_hash in self._cache:
            action_id = self._cache[trigger_hash]
            action = self.action_store.get_by_id(action_id)
            if action and action.confidence >= 40:
                return DecisionResult(action=action, source="cache_hit")

        # Gate 2: Embedding search
        matches = self.action_store.find_best(embed(trigger), top_k=3)
        if matches and matches[0].similarity >= 0.55 and matches[0].confidence >= 40:
            self._cache[trigger_hash] = matches[0].id
            return DecisionResult(action=matches[0], source="vector_search")

        # Gate 3: LLM intent extraction (if enabled)
        if self.llm_backend != "passthrough":
            phrase = extract_intent(trigger, backend=self.llm_backend)
            matches = self.action_store.find_best(embed(phrase), top_k=3)
            if matches and matches[0].similarity >= 0.55:
                self._cache[trigger_hash] = matches[0].id
                return DecisionResult(action=matches[0], source="llm_assisted")

        # Final fallback: passthrough (raw trigger as intent)
        matches = self.action_store.find_best(embed(trigger.lower()), top_k=3)
        if matches and matches[0].similarity >= 0.40:  # lower floor for passthrough
            return DecisionResult(action=matches[0], source="passthrough_fallback")

        return DecisionResult(no_match=True, trigger=trigger)
```

### Tasks
1. Implement `FastLoopInterceptor` adaptation (port from Lever Runner with cognition extensions)
2. Implement semantic cache (trigger_hash → action_id with LRU eviction, max 10,000 entries)
3. Implement intent extraction prompt for cognition (adapted from Lever Runner's system prompt)
4. Implement the cascade orchestrator with all four resolution paths
5. Write integration tests covering all gate combinations

### Success Criteria
- Gate 1 validates and rejects bad input in < 1ms
- Gate 2 resolves 40%+ of queries via cache/vector search in < 10ms
- Gate 3 resolves novel queries via LLM in < 1s (with fallback to passthrough)
- Overall: >95% of queries resolved without hanging

---

## Phase 3: Action Execution Layer (2-3 days)

**Goal:** Execute the actions selected by the three-gate cascade.

### What We Take from Lever Runner
- `executor.py`'s sandboxing pattern (per-session dirs, restricted env, resource limits, timeout)
- Trust score feedback loop (execution result → confidence update)

### What We Change
- **Multi-type execution:** Not just shell commands. Route to the correct executor based on `action_type`.
- **Cloudflare Workers integration:** The `worker_api` action type calls Cloudflare Workers endpoints.
- **OpenClaw tool integration:** The `openclaw_tool` action type invokes OpenClaw tools via the exec tool.
- **Dry-run mode:** Support `decide(trigger, dry_run=True)` that returns the selected action without executing it.

### Tasks
1. Implement `ShellExecutor` (adapted from Lever Runner's executor.py)
2. Implement `HTTPExecutor` for Worker API calls
3. Implement `LuaExecutor` for Roblox actions (via the existing relay)
4. Implement `CompositeExecutor` that routes to the correct executor based on action type
5. Add dry-run support throughout
6. Wire confidence feedback (success → +1.5, failure → -4.0)

### Success Criteria
- Shell actions execute in sandbox with restricted env, timeout, resource limits
- HTTP actions call Cloudflare Workers with auth and timeout
- Lua actions route through the Roblox relay
- Confidence updates after every execution

---

## Phase 4: Auto-Promote and Self-Improvement (2-3 days)

**Goal:** Implement the learning loop that makes the system smarter over time.

### What We Take from Lever Runner
- `auto_promote.py`'s promote_winners and rewrite_losers patterns
- The hourly cron concept (adapted to heartbeat or scheduled task)

### What We Change
- **Promotion logic:** Generalized beyond shell commands. Any action type can be promoted.
- **Rewrite logic:** Use GLM-5.2 (via Z.ai) instead of Claude/Anthropic for rewrites.
- **Telemetry:** Log promotion/demotion decisions for auditability.
- **Integration with heartbeat:** Run auto-promote as part of the OpenClaw heartbeat cycle rather than a separate cron.

### Tasks
1. Port `promote_winners` logic with generalized action types
2. Port `rewrite_losers` logic with GLM-5.2 backend
3. Add audit logging (JSONL) for all trust changes
4. Implement as an OpenClaw heartbeat task (runs every N heartbeats)
5. Add metrics: total actions, average confidence, cache hit rate, gate distribution

### Success Criteria
- Actions with 20+ successes get promoted (+10 confidence)
- Actions with 5+ failures at confidence < 30 get rewrite candidates
- All trust changes are logged and auditable
- Auto-promote runs without disrupting normal operation

---

## Phase 5: Skill Pack System (2-3 days)

**Goal:** Package cognition actions as composable, portable skill packs.

### What We Take from Lever Runner
- JSONL skill pack format (`{trigger_pattern, action_spec, confidence, tags}`)
- Import/export mechanics
- The `.nail` portable format concept (adapted)

### What We Change
- **Action specs are richer:** Not just `{command: str}` but typed action objects
- **Tags for composition:** Filter by tag to compose action subsets
- **Version metadata:** Semver in the pack header for compatibility checking
- **Integration with OpenClaw skills:** Skill packs should be loadable as OpenClaw skill resources

### Tasks
1. Define skill pack JSONL schema (with version, tags, action types)
2. Implement export (`export_packs()`) and import (`import_packs()`)
3. Create initial seed packs:
   - `system-ops.jsonl` — system administration actions (from Lever Runner's seed)
   - `roblox-build.jsonl` — Roblox world-building actions
   - `cloudflare-dev.jsonl` — Cloudflare Workers/Pages development actions
4. Implement pack validation on import (schema check, confidence floor, tag validation)

### Success Criteria
- Can export and re-import the full action table with zero data loss
- Seed packs provide immediate value on first install
- Packs are human-readable JSONL (diffable, version-controllable)

---

## Phase 6: Cognition Snapshot (1-2 days)

**Goal:** Portable cognition state for deployment and migration.

### What We Take from Lever Runner
- `.nail` format concept (tar.zst archive with SQLite + manifest + embeddings)
- The device fingerprint and checksum verification pattern

### What We Change
- **Format:** tar.zst with:
  - `manifest.json` — version, checksums, source, timestamp
  - `actions.db` — SQLite with actions table
  - `failure_cache.json` — exported failure cache
  - `metrics.json` — historical performance data
- **Import validation:** Verify checksums, check version compatibility, merge or replace

### Tasks
1. Implement `export_snapshot(path)` — package full cognition state
2. Implement `import_snapshot(path)` — restore from snapshot (with merge/replace modes)
3. Add snapshot versioning (v1 schema, forward-compatible)
4. Test cross-device portability (export from x86, import on ARM)

### Success Criteria
- Snapshot captures full cognition state (actions, failure cache, metrics)
- Import on a fresh instance reproduces the original behavior
- Snapshot size < 5MB for up to 10,000 actions

---

## Timeline

| Phase | Duration | Dependencies | Deliverable |
|-------|----------|-------------|-------------|
| 0. Pattern Extraction | 1-2 days | None | Design docs |
| 1. Action Policy Table | 3-5 days | Phase 0 | `ActionStore` class |
| 2. Three-Gate Cascade | 3-5 days | Phase 1 | `CognitionGate` class |
| 3. Action Execution | 2-3 days | Phase 2 | `CompositeExecutor` |
| 4. Auto-Promote | 2-3 days | Phases 1, 3 | Self-improvement loop |
| 5. Skill Packs | 2-3 days | Phase 1 | JSONL pack system |
| 6. Cognition Snapshot | 1-2 days | Phases 1, 4 | `.cog` snapshot format |

**Total: 14-23 days** (assuming focused work, no competing priorities)

---

## Integration Points with Existing Systems

### OpenClaw
- **Heartbeat:** Auto-promote runs during heartbeat cycles
- **Skills:** Skill packs loaded as OpenClaw skill resources
- **Tools:** The `openclaw_tool` action type bridges to existing tool infrastructure
- **Memory:** Action history and metrics feed into MEMORY.md

### Cloudflare Workers
- **Worker API calls:** The `worker_api` action type hits Lucineer relay endpoints
- **D1/KV:** Action policy table can optionally use D1 or KV for storage (instead of local SQLite)
- **Vectorize:** Embedding search can optionally use Cloudflare Vectorize (instead of local numpy)

### Lucineer (Roblox)
- **Lua execution:** The `lua` action type sends commands through the Roblox relay
- **Build intelligence:** Roblox-specific skill packs (`roblox-build.jsonl`)
- **Spatial reasoning:** Build commands parameterized with `{{part_name}}`, `{{position}}`, etc.

### GLM-5.2 (Z.ai)
- **Default LLM backend:** Intent extraction and command rewriting use GLM-5.2
- **Unlimited tokens:** Z.ai Max plan means no token budget anxiety for the Local Thinker
- **Fallback chain:** GLM-5.2 → DeepInfra (cheap) → passthrough (zero cost)

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Embedding model too heavy for edge | Position-aware hash embedding (64 dims, 0 deps, 44% accuracy) |
| LanceDB dependency | Abstract behind `VectorStore` protocol; default to SQLite + numpy |
| LLM provider outage | Three-backend fallback chain always terminating at passthrough |
| Action table grows unbounded | Auto-promote demotes low-confidence actions; add max-size LRU eviction |
| Shell injection in parameterized actions | Validate args against `^[a-zA-Z0-9._-]+$` before substitution |
| Stale failure cache blocks valid inputs | Add TTL (24h) to failure cache entries; periodic cleanup |
| Trust dynamics don't match cognition needs | Make ±deltas configurable per action type |

---

## Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| Token cost per action (median) | < 100 tokens | Log all LLM calls, compute median |
| Gate 1-2 hit rate | > 50% | Track resolution source per decision |
| Action execution latency (p50) | < 50ms (excluding LLM) | Time from decision to result |
| Action execution latency (p99) | < 500ms (excluding LLM) | Same |
| Auto-promote accuracy | > 90% of promoted actions remain trusted | Audit promoted actions after 7 days |
| Failure cache effectiveness | > 30% of bad inputs caught by cache | Track cache hits vs. misses |
| Skill pack coverage | > 80% of common operations in seed packs | Usage analytics |

---

*This plan is a living document. Update as phases are completed and lessons are learned.*
