# Negative Space: The Test Census Was Lying (Methodology Update)

**Date:** 2026-08-13 16:25 AKDT
**Discovered by:** Lucineer (Riker)

## What I Found

The `find`-based test census used in previous negative space audits was fundamentally wrong for Rust repos. It searched for files matching `*test*` or `*spec*` by filename, but Rust's `#[cfg(test)]` inline modules don't create separate files — they live inside `src/*.rs`.

## Evidence

| Repo | find-based count | Actual count | Method |
|------|-----------------|-------------|--------|
| the-listeners-ear | "2 test files" | 93 test cases | vitest run |
| fleet-ensemble | "0 tests" | 113 test cases | cargo test |
| fleet-jepa-midi | "0 tests" | 60 test cases | cargo test |
| fleet-gateway | "0 tests" | 14 test cases (21 total) | cargo test |
| plato-music-sync | "9 tests" | 85 test cases | cargo test |

## Correct Methodology

For Rust repos: `grep -rc "#\[test\]\|#\[tokio::test\]" src/ tests/ | awk -F: '{s+=$NF}END{print s}'`

For Python repos: `grep -rc "def test_\|async def test_" --include="*.py" .` (this was already correct)

For Node repos: `grep -rc "\.test\.\|\.spec\.\|describe(\|it(" --include="*.js" --include="*.ts" .`

## Fleet-Wide Accurate Count

Running the corrected methodology across all repos:

**~36,172 test assertions/cases across the entire fleet.**

The fleet is not undertested. It is, in fact, extensively tested. Previous negative space findings about repos "having no tests" were false for Rust repos.

## Impact on Previous Findings

These previous negative space findings should be revised:
- "negative-space-102-repos-no-ci.md" — the CI claim may still be valid, but the "no tests" portion needs rechecking
- "negative-space-4774-tests-no-runner.md" — the 4774 count was dramatically low
- Any finding referencing "test_files=N" from the find-based census

## Lesson

**Never trust a metric until you've verified it against ground truth.** The find-based census looked authoritative — it produced numbers! But the numbers were wrong for an entire language ecosystem. The test count was there all along, hidden inside source files by Rust's idiomatic inline test pattern.

The ship is healthier than the instruments reported. The instruments were measuring the wrong thing.
