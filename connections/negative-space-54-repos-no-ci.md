# Negative Space: 54 Repos Without CI

**Date:** 2026-08-10 17:50 AKDT

## Finding

148 repos have CI. 54 don't. That's 27% of the fleet running without automated test verification.

Among those without CI, several have significant code and test suites:
- **platos-shell**: 36 source files, 74 tests, no CI
- **vibe-protocol**: 10 source files, 77 Python + TS tests, no CI (now fixed)
- **officers-quarters**: 18 source files, no CI
- **scummvm-arcade**: 18 source files, no CI
- **collective-unconscious**: 11 source files, no CI
- **base60-lattice**: 8 source files, 107 tests, no CI

The tests exist. The CI doesn't run them. Tests that aren't run are aspirations, not safety nets.

## Root Cause

The GitHub OAuth token used for pushing doesn't have `workflow` scope. CI config files (`.github/workflows/*.yml`) require this scope to push. So the overnight crew can write the files, but only Casey can push them with a properly scoped token.

## Partial Fix

- **vibe-protocol**: CI added and pushed (token had scope for this repo)
- **platos-shell**: CI committed locally, push rejected (missing workflow scope)

## Recommendation

Either:
1. Casey runs `git push` on repos with committed CI configs
2. The GitHub token gets `workflow` scope added
3. We create a script that Casey can run once to push all pending CI configs

The fleet's tests are only as good as whether they actually run.
