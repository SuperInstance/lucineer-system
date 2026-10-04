# Audit Round 20 — lucineer-relay

Repo: SuperInstance/lucineer-relay · default branch: **main** · Audit date: 2026-09-04 · Commit: **5f7e3c8**

## 1. Link check

- All 5 sibling-repo links (lucineer-system, lucineer-memory, lucineer-vector, lucineer-roblox, casting-call) verified live via `gh api` ✓.
- Live worker `https://lucineer-relay.casey-digennaro.workers.dev/api/health` → 200 `{"status":"ok"}` ✓.
- CI workflows (ci.yml, tests.yml) reference main+master and run pytest — live, not dead refs ✓. Default branch is main (repo has no master).
- No "18/18" quilt-verilog citations anywhere in the repo (grep clean) ✓.

## 2. r10 fixes re-verified — ALL HOLD

- Lease claim: 3-min `LEASE_MS = 3 * 60 * 1000` (src/do/LucineerSession.ts:13) + `/api/job/:jobId/renew` documented ✓ (dated 2026-09-03 note intact).
- Schema: `claimed_by` / `lease_expires_at` present in README schema block, mirroring source ✓.
- Previously-undocumented endpoints section present (renew, batch claim, chat, generate-build, quick, world, cache DELETE) ✓.
- Duplicate related-repo row: merged, removal noted in HTML comment ✓.

## 3. Claims verified by re-run

- **pytest re-run fresh: 301 passed, 7 skipped (0.26s)** ✓ — matches r10 exactly.
- Constants re-read from source: `MAX_ATTEMPTS = 3` (:15), `RATE_LIMIT_MAX = 10` (:17), `RATE_LIMIT_WINDOW_MS = 60_000` (:19) ✓.
- 3-tier auth still in place (LUCINEER_INTERNAL_KEY / LUCINEER_KEY / LUCINEER_SHARED_SECRET) ✓.
- **Still true (flagged, not fixed):** `test/logic.test.ts` remains unwired — package.json has only deploy/dev/types scripts, no `test` script, vitest-pool-workers present but unused by CI. Carried forward from r10.

## 4. Stale claim FIXED

- **lucineer-roblox size:** README said "16 Lua modules". Actual: **86 modules / ~47.5k lines** (lucineer-system r12 re-count, commit 7f6bdc1). Independent r20 count via `gh api git/trees` returned **91 `.lua` blobs** (includes tests/specs beyond the module count). Corrected with dated 2026-09-04 note citing both counts (honest-boundary: two sources, two numbers, both stated).

## 5. Cross-pollination applied

- Honest-boundary booking (quilt-verilog discipline): the fix note states both evidence sources (r12 count 86 modules vs r20 blob count 91 files) rather than collapsing to one number.
- Verification-by-rerun: pytest + constants + live health endpoint all re-executed fresh, not trusted from docs.
- No history rewritten; r10 dated notes preserved verbatim.

## 6. Result

Commit **5f7e3c8** pushed to main (ff, no force). 1 stale claim fixed; all r10 fixes hold; tests 301/308 green; worker live.
