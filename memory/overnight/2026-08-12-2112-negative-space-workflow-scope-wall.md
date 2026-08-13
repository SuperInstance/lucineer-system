# Negative Space: The Workflow Scope Wall

**Date:** 2026-08-12 21:12 AKDT

## The Finding

The GitHub OAuth token used by the fleet doesn't have the `workflow` scope. This means:

- We can push code changes (source files, tests, docs)
- We **cannot** push changes to `.github/workflows/*.yml` files

This is why 22 repos still have placeholder CI workflows. We can fix the YAML locally, but we can't push the fix. The CI theater persists not because we haven't noticed it, but because we lack the permission to change it.

## Impact

- Every CI workflow we've added in overnight loops was created via `git push` — but only for repos where the first workflow was created before the scope limitation, or via the GitHub API.
- New CI workflow files pushed directly are rejected with: `refusing to allow an OAuth App to create or update workflow without workflow scope`

## The Fix

Casey needs to run:
```bash
gh auth refresh -s workflow
```

Or regenerate the GitHub token with the `workflow` scope included. This is a one-time fix that unblocks all CI workflow improvements across the fleet.

## Recommendation

This should be the #1 morning priority. Until the workflow scope is added, the fleet's CI is frozen — we can improve everything except the thing that verifies the improvements.
