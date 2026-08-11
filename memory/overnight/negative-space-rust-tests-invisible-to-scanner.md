# Negative Space: The Fleet Is Healthier Than the Scan Suggests

**Date:** 2026-08-10 19:25 AKDT
**Discovery:** 26 repos flagged as "zero tests" by filename-pattern scan. Reality: most have extensive tests inline.

## The Problem

My scan looked for files matching `*.test.*`, `*_test.*`, `*.spec.*`, `test_*` patterns. This catches:
- TypeScript/JavaScript test files ✅
- Python test files ✅

This MISSES:
- Rust `#[cfg(test)]` inline tests in `src/lib.rs` ❌
- Rust integration tests in `tests/*.rs` (they're just `*.rs`, not `*_test.rs`) ❌
- Go tests in `*_test.go` ✅ (but we have no Go repos)
- C/C++ test files with custom naming ❌

## The Reality

| Repo | Scan Said | Actual Tests | Source |
|------|-----------|-------------|--------|
| dual-band-guard | 0 | 59 | `#[cfg(test)]` + `tests/integration.rs` |
| gossip-ping | 0 | 60+ | `#[cfg(test)]` + `tests/integration.rs` |
| hermes-nmi | 0 | 162 | 7 `tests/*.rs` files |
| mud2scummvm | 0 | ? | Likely has tests |

**Three repos alone account for 281 tests my scan missed.** That's a significant blind spot.

## The Deeper Pattern

Rust convention puts tests in `tests/` directory with simple names (`dispatcher.rs`, not `dispatcher_test.rs`). The test annotation is on the functions inside (`#[test]`), not the filename. This is idiomatic Rust — everyone does it this way.

My scan was TypeScript-brained. It assumed tests announce themselves through filename conventions. Rust tests are quieter — they're embedded in source files or sit alongside the source with minimal naming ceremony.

## Implication for Overnight Loops

Previous session reports may have **undercounted** total fleet tests. The actual fleet test count is likely 300-500 higher than reported, because Rust repos were systematically undercounted.

## Fix

Update the fleet census script to also count:
1. `#[test]` annotations in `*.rs` files
2. `#[cfg(test)]` module blocks
3. Any file in a `tests/` directory for Rust projects

Or better: just run `cargo test` on Rust repos and parse the output.

## The Lesson

Assumptions about where tests live are themselves untested hypotheses. The scan was confident. The scan was wrong. 281 tests existed in the negative space it created.
