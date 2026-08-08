# EXOCORTEX Overnight Audit — 2026-08-07 19:30 AKDT

## Summary

Audited the EXOCORTEX repo at `/home/eileen/projects/EXOCORTEX/`.
Found and fixed 1 production bug, wrote 103 new tests covering previously untested modules.

## Repo Overview

EXOCORTEX is a persistent cognitive substrate for multi-agent systems — tiered in-memory store with optional SurrealDB backend, shadow rendering, tiered compute, ESP32-friendly TAP protocol. Part of the SuperInstance fleet.

**Stack:** Python 3.10+, FastAPI, Textual TUI, asyncio, pure-Python ML (MicroNN, k-means)

**Modules:**
- `src/core/types.py` — Core data models (CortexEvent, MemoryEntry, Provenance, etc.)
- `src/core/resonance.py` — Cross-agent knowledge overlap detection
- `src/config/__init__.py` — TOML config loader
- `src/bus/__init__.py` — Async pub/sub Cortical Bus with priority + backpressure
- `src/compute/__init__.py` — MicroNN neural net + tiered compute dispatch + reflex arc
- `src/compute/dream.py` — Dream cycle (k-means memory consolidation)
- `src/memory/__init__.py` — 3-tier memory (hot/warm/cold) with half-life decay
- `src/memory/surrealdb_backend.py` — SurrealDB backend with in-memory fallback
- `src/shadows/__init__.py` — Shadow rendering pipeline (machine events → human stories)
- `src/tui/__init__.py` — Textual TUI ("Plato's Cave")
- `src/protocols/__init__.py` — FastAPI REST + TAP protocol endpoints
- `src/main.py` — Entry point wiring everything together
- `mentis-thinker-adapter/` — Subproject: mental world model adapter (separate pyproject)

## Bugs Found

### BUG-1: CortexEvent.new() trace_id collision (FIXED)

**Severity:** High — crashes `/api/v1/embed` and `/api/v1/remember` endpoints

**Root cause:** `CortexEvent.new()` sets `trace_id=uuid.uuid4().hex[:12]` as an explicit kwarg, then spreads `**kwargs`. If a caller passes `trace_id` in kwargs (which `protocols/__init__.py` does on lines 96 and 116), Python raises `TypeError: got multiple values for keyword argument 'trace_id'`.

**Impact:** Both `/api/v1/embed` and `/api/v1/remember` HTTP endpoints crash with 500 errors. The endpoints pass `trace_id=entry.id[:12]` to `bus.emit()`, which passes it to `CortexEvent.new()`.

**Fix:** Changed `CortexEvent.new()` to use `kwargs.setdefault("trace_id", ...)` instead of explicit kwarg:

```python
# Before (broken):
@staticmethod
def new(event_type, source, **kwargs):
    return CortexEvent(
        event_type=event_type, source=source,
        trace_id=uuid.uuid4().hex[:12],
        **kwargs,  # 💥 collision if kwargs has trace_id
    )

# After (fixed):
@staticmethod
def new(event_type, source, **kwargs):
    kwargs.setdefault("trace_id", uuid.uuid4().hex[:12])
    return CortexEvent(
        event_type=event_type, source=source,
        **kwargs,
    )
```

**File:** `src/core/types.py` line 78

**Regression test added:** `tests/test_protocols.py::TestRememberEndpoint::test_remember_trace_id_bug_regression`

## Test Coverage Improvements

### Before: 315 tests (7 test files)
### After: 418 tests (9 test files, +103 new tests)

### New file: `tests/test_protocols.py` (49 tests)
Previously **zero** tests for the FastAPI HTTP layer. Added comprehensive coverage:
- App creation, CORS middleware, route verification
- `GET /api/v1/capabilities` — all operations, protocols, tiers
- `GET /api/v1/stats` — empty and populated states
- `GET /api/v1/query` — tag-based queries, multiple tags, no match
- `POST /api/v1/embed` — basic embed, custom dims, default agent, memory storage
- `POST /api/v1/remember` — basic, default agent, empty tags, trace_id bug regression
- `POST /api/v1/recall` — basic, empty memory, top_k, result structure
- `POST /api/v1/predict` — untrained vs trained model
- `POST /api/v1/train` — basic, custom dims, model overwrite
- `GET /tap/recall` — basic, empty, 200-byte limit, no query param
- `POST /tap/remember` — basic, memory storage verification
- `GET /tap/predict` — normal, invalid reading, missing reading, anomaly detection
- `POST /tap/sense` — basic, memory storage, invalid values, empty data, anomaly detection

### New file: `tests/test_compute_engine.py` (54 tests)
Previously **zero** tests for MicroNN and only minimal coverage of ComputeEngine. Added:
- `MicroNN` init, dimensions, weight shapes, Xavier initialization scale
- `MicroNN` forward pass: output size, zero input, different inputs, valid floats
- `MicroNN` predict: class/confidence return, softmax sums to 1, single class, argmax correctness
- Compute tier dispatch: all 8 operations mapped to correct tiers (HOT/WARM/BATCH)
- Operation results: embed normalization, custom dims, remember, recall, analyze, transform, train, predict
- Reflex arc: first reading, baseline accumulation, n<5 threshold, extreme anomaly, counter increment, normal value passthrough, multi-sensor independence, negative values, stats update after anomaly, detail string format
- Stats tracking: initial state, per-tier call counting, models count, baselines count
- Edge cases: zero-dim embed, empty input predict, multiple models, model overwrite

## Observations (not bugs, but noted)

1. **`reflex_check` is async but contains no awaits** — it's purely synchronous computation marked `async`. Not a bug (callers use `await`), but a minor design smell.

2. **Embedding is random unit vectors** — documented in README as a placeholder. Recall works by random-vector cosine similarity. This is intentional and acknowledged.

3. **MicroNN training is simulated** — `accuracy = random.uniform(0.85, 0.96)`. Also documented in README.

4. **`get_recent_memories` in MemoryLayer only checks warm tier** — doesn't scan hot or cold tiers. This means recently reheated memories (promoted from cold to hot) won't appear in recent queries. Documented behavior, not a bug.

5. **SurrealDB backend schema uses SCHEMAFULL with DEFINE ANALYZER** — may fail on SurrealDB < 2.0. The fallback logic handles this gracefully.

6. **TAP endpoints return plain strings** — FastAPI wraps these as JSON (`"remembered"` with quotes). For true ESP32 plain-text responses, the endpoints should use `Response(content="remembered", media_type="text/plain")`. Low priority since the current behavior works, just adds quotes.

## Files Changed

| File | Change |
|------|--------|
| `src/core/types.py` | Fixed CortexEvent.new() trace_id collision bug |
| `tests/test_protocols.py` | **NEW** — 49 tests for FastAPI REST + TAP endpoints |
| `tests/test_compute_engine.py` | **NEW** — 54 tests for MicroNN + ComputeEngine |

## Conclusion

The repo is well-structured with clean separation of concerns. The one production bug (trace_id collision) was silently breaking two HTTP endpoints. With 103 new tests covering the previously untested HTTP layer and compute engine, test coverage went from 315 → 418 tests. The ship sails tighter.
