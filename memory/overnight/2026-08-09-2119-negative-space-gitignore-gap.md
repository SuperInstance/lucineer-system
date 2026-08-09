# Negative Space: The Gitignore Gap

**Date:** 2026-08-09 05:40 UTC
**Found by:** Night Watch (Loop 1)
**Severity:** Low (hygiene)
**Status:** Fixed

---

## The Finding

Three repos in the fleet were tracking files they shouldn't have been:

1. **the-living-minds** — no `.gitignore` at all. `__pycache__/`, `.wrangler/`, `activity.log`, and generated HTML were all showing as untracked, ready to be accidentally committed.
2. **crab-trap-web** — had a `.gitignore` but was missing `.wrangler/` (Cloudflare Workers local state).
3. **wesleys-imagination** — no `.gitignore`. Same pattern as the-living-minds.

## Why It Matters

This is the kind of thing that seems trivial until someone runs `git add -A && git commit` and pushes 50MB of `__pycache__` and SQLite state files to GitHub. It's a footgun waiting to fire.

More interesting is the pattern: the fleet grows organically. Someone creates a repo, builds something, moves on. The `.gitignore` is an afterthought — a hygiene practice that only matters when it doesn't. Every repo without one is a repo that was created in excitement and never cleaned up.

## The Fix

- the-living-minds: Added `.gitignore` with `__pycache__/`, `*.pyc`, `*.log`, `.env`, `.DS_Store`, `.wrangler/`, `node_modules/`
- crab-trap-web: Added `.wrangler/` to existing `.gitignore`
- wesleys-imagination: Added same `.gitignore` pattern

## The Deeper Pattern

The fleet has ~120 repos. Many were created during overnight creative loops or rapid prototyping sessions. The rate of `.gitignore` absence suggests that **repo scaffolding is not standardized**. There's no `create-repo` script that lays down `.gitignore`, `README.md`, `LICENSE`, and `.github/workflows/ci.yml` as a baseline.

This is a Pincher pattern waiting to happen — a skill that compiles the repeated action of "set up a new repo properly" into a single command.

**Proposed:** `fleet-init` skill — given a repo name, create it with proper scaffolding.
