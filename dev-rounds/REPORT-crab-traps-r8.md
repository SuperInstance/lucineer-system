# AUDIT ROUND 8 — crab-traps (SuperInstance/crab-traps)

Date: 2026-09-03 · Lane: cross-pollination + fact-check · Default branch: `main` (verified via symbolic-ref)

## Repo state
- Local clone existed at `~/projects/crab-traps`; pulled ff-only, clean tree.
- Commit landed: **c0006d1** (`audit round 8: crab-traps: fix stale lure counts ...`) pushed to `origin/main`. No force-push, no deletions.

## Links checked
Relative paths in README/worker README — all resolve:
- docs/REEF-DESIGN.md, docs/THE-REAL-THING.md, docs/BEAM.md, worker/README.md, worker/migrations/0001_catches.sql, worker/scripts/build-lures.mjs, .github/workflows/review-lure.yml, scripts/review-lure.py, scripts/vectorize-lures.py ✅
- `quilt-rust/docs/cell-ledger.md` and `fleet-as-fractal-jepa.md` referenced by worker/README — verified present on GitHub SuperInstance/quilt-rust ✅
- Sibling repo links (elephant, mud-arena, collective-unconscious, fleet-radio, quilt, superinstance-ai) — all exist on GitHub SuperInstance org ✅
- Images (trap-v1.png, hero-submersible.jpg, lure-v1.png, fleet-v1.png) exist in assets/images/ ✅

External (curl -L):
- https://crab-trap-funnel.casey-digennaro.workers.dev/health → 200 ✅
- https://fleet.cocapn.ai/api/fleet/status → 200 ✅
- https://fleet.cocapn.ai/ → 200 ✅

## Claims verified vs. actual (tests re-run, not just read)
- **Test suite re-run**: `cd worker && npm test` → **358/358 passing, 15 files, exit 0**. README claimed "341" → FIXED to a live count with a dated re-verification note (quilt-verilog verification-by-rerun discipline).
- **Lure category table** (README): counted actual `.md` per dir excluding READMEs. Five stale counts → FIXED:
  - audit 1→2, competition 2→3, discovery 2→3, documentation 2→3, exploration 2→3.
- **"all 50+ lures bundled"** in the architecture diagram → actual total **45** lures. FIXED to "all 45 lures bundled".
- **"21 domain pages"**: pages.json has 22 keys but one is `trap` → 21 domains. Claim correct, no change. worker/pages/ holds 21 non-trap pages ✅.
- **review-lure.py**: ran locally — exits with warnings only (absolute-claim + one structure warning in ml-pipeline/constraint-review.md), consistent with CI-tolerated state; no new errors.
- Worker routes/behavior claims (D1 catches, 5s fleet timeout stub, badge n/a path) are covered by the passing 358-test suite — considered verified by rerun.

## Cross-pollination applied
- **quilt-verilog verification-by-rerun discipline**: replaced the hard-coded "341 tests" with the re-run count plus an inline dated re-verification note (`Re-verified 2026-09-03 (audit round 8): 358/358 passing in 15 files`) so future drift is auditable.
- **Honest-boundary booking**: fixes were corrections next to the claims (table cells, diagram line) — no silent history rewrites, no rewording beyond the stale numbers.
- **Tapestry doctrine / central docs index**: not applicable — repo has no central docs index page; docs/ is a flat set of design essays. Skipped rather than invented structure.

## Not flagged / no action
- AI-Writings prose move and quilt-verilog synthesis-result supersessions have no references in this repo — nothing contradicted.
- QUICK-START.md exists at lures/ root; not linked from main README but harmless.

## Outcome
Commit c0006d1 pushed to main: 6 stale numbers corrected + 1 dated re-verification note. Everything else verified green.
