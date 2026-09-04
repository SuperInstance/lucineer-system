# Audit Report — the-tap, Round 5 (2026-09-03)

- **Repo:** SuperInstance/the-tap (fresh clone to /home/eileen/the-tap — no local clone existed)
- **Default branch:** `master` (verified via `git remote show origin`; there is also `origin/tap-rewire-glm`)
- **Commit pushed:** `01a01de` on master — "audit round 5: the-tap: fix 9 dead story links..."

## Links checked / broken / fixed
Checked all GitHub URLs in README + top-level .md + docs/ (curl -L, one by one):
- **9 broken story links** in README: AI-Writings reorganized — files moved from repo root to `prose/` (15-the-tap-overhears, 16-many-voices, 17-becoming-someone, 18-three-agents, 21-stories-told, 47-wesley-eats-menu, 54-midnight-at-the-tap, a-visit-to-the-tap-tonight). Fixed to `blob/main/prose/…`; all now 200. `fiction/15-the-bluff-that-was-true.md` was already correct.
- **Dead Deploy badge**: README badge pointed at `deploy.yml`, which never existed; actual workflow is `ci.yml`. Badge *image* still 404s even with ci.yml present → GitHub Actions appears disabled on the repo. Replaced with an honest plain link + dated verification note (honest-boundary booking).
- **LIVING-HISTORY.md:849**: code sample URL pointed at `casey-digennaro/ai-writings` (404, wrong owner) → fixed to `SuperInstance/AI-Writings`.
- Relative paths verified: docs/hero-the-tap.jpg, docs/bar-rail.svg, all README doc-table files, .github/workflows/ci.yml exist.

## Claims verified
- **Tests re-run**: `pytest -q` → **28 passed in 1.59s**. Clean.
- Docs table entries all resolve. `ai-writings.pages.dev` link not individually fetched (left as-is; plausible Pages URL).

## Flagged
- GitHub Actions workflows exist in-tree (ci.yml) but Actions appears disabled — badge renders 404. Worth a Casey decision: enable Actions or accept plain link.
- No quilt-verilog pipeline claims present in this repo — nothing to supersede.

## Cross-pollination applied
- Honest-boundary booking style (from sibling audit lanes): the CI note states exactly what was verified, when, and what's unverified rather than claiming a green badge.
- Kept edits minimal; no history rewrites, no dated files touched, nothing deleted.

## Notes for next round
- The `tap-rewire-glm` branch exists and is ahead-ish — check whether it should merge to master.
- Root-level docs (ARCHITECTURE-CLOUDFLARE.md etc.) weren't exhaustively link-checked inside docs/ subfolder contents beyond GitHub URLs — only spot-checked; deeper anchor checks remain.
