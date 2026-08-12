# Negative Space: The Scanner Is Lying

**Date:** 2026-08-12 13:14 AKDT
**Finding:** The overnight loop's fleet scanner has been reporting false negatives for tests across the fleet.

## What We Found

The scanner uses this pattern to detect tests:
```
find . -name "*.test.*" -o -name "*_test.*" -o -name "test_*"
```

This misses:
- **Rust `tests/` directories** — Rust convention puts integration tests in `tests/` with filenames like `integration.rs`, `edge_cases.rs`. These don't match `*.test.*` or `*_test.*` or `test_*`.
- **Python `test_*.py` files inside `tests/`** — partially caught but not consistently
- **Any test file named differently than the pattern** — e.g. `edge_cases_extended.rs`

## Repos falsely reported as "no tests"

| Repo | Scanner Says | Reality |
|------|-------------|---------|
| eisenstein | N (no tests) | 88 tests (83 integration + 5 doc) |
| dual-band-guard | N | Has `tests/edge_cases_extended.rs` + `tests/integration.rs` |
| mud2scummvm | N | 31 tests |
| gossip-ping | N | 30 tests (Rust) |

## The actual gap

The gap isn't in the repos — it's in our visibility. We've been writing "negative space" findings about repos being untested when they're fine. The scanner needs to be fixed, or we need to stop relying on it for test detection.

## Root cause

`find` patterns are fragile. The proper way to detect tests per language:
- **Rust:** `cargo test -- --list` or check for `tests/` dir + `#[test]` in source
- **TypeScript/JS:** check `package.json` for test script, look for `*.test.*`, `__tests__/`
- **Python:** `pytest --collect-only` or look for `test_*.py`, `*_test.py`
- **Lua:** look for `spec/` or files with `describe()`/`it()`

## Recommendation

Build a proper fleet test census tool that understands language ecosystems instead of pattern-matching filenames. The hermit crab keeps trying on shells that don't fit because it's measuring with the wrong calipers.

## The deeper metaphor

This is a recurring pattern in the fleet: we build observation tools that see what they expect to see, not what's there. The scanner was written to find JS/TS tests (`.test.ts`) in a fleet that's 40% Rust. It's like checking for fish with a bird detector.
