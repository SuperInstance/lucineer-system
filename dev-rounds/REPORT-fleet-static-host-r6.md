# Audit Round 6 — fleet-static-host (SuperInstance)

**Date:** 2026-09-03 · **Lane:** audit-r6-fleet-static-host · **Default branch:** `master` (verified via `git remote show origin`; other branch `lobby-tapestry` untouched)

## Link check (~15 links, 0 dead, 0 needed URL fixes)
- External GitHub: `SuperInstance/quilt-cloudflare` repo + tree@`3c293f6` — 200.
- Live Worker: `/`, `/papers/`, `/writings/`, `/scrap/`, `/mist/`, `/ternary/`, `/api/quilt/health`, `/api/quilt/cells` — all 200.
- README relative link `../quilt-cloudflare` resolves on GitHub.
- No AI-Writings links present (the-tap's prose/ breakage does not affect this repo).

## Claims verified (by re-running, not trusting — quilt-verilog discipline)
1. **Tests:** `npm test` → 34 passed, 0 failed (mcp + uscp suites).
2. **Numbers:** README "7 papers / 24 writings / 31 documents" — correct. Seed sheets' raw cell counts (8/25) include `*.index`/`trails.note` ordering cells; actual docs: 7 paper.*, 24 writing.* (+ 8 trail.*). Live D1 matches committed sheets exactly (55 cells total, incl. telemetry sheet).
3. **Vendoring claim:** diffed `src/quilt.ts` against upstream `src/worker.ts`@`3c293f6` — the only removals are upstream's Worker entrypoint, Env interface, CORS handler, and MCP demo, exactly as the vendoring header claims. Engine classes verbatim. ✓
4. **Formula-eval shim claim:** live `/api/quilt/health` reports `dynamicEval.ok: false` ("Code generation from strings disallowed") — the safeEvalArithmetic shim note is honest and current. ✓
5. **Cold fallback:** `public/papers`, `public/writings`, `index.html`, `404.html` all present in-tree. ✓

## Flagged + fixed (stale claims)
- **run_worker_first claim stale:** README said the Worker routes "only `/`, `/papers*`, `/writings*`, `/api/*`" — but `wrangler.jsonc` now also routes `/ai/embed`, `/ai/tts`, `/canon/search`, `/forest/search`, `/mcp`, `/.well-known/mcp`. Fixed with a dated 2026-09-03 note (no history rewrite).
- **Layout section incomplete:** omitted `src/mcp.ts`, `src/uscp.ts`, `tools/`, migrations 0002–0006 (forest/MCP audit), new `public/` dirs (canon, forest, demos, openmic, ops, quilt), wrangler's Vectorize/AI/cron bindings. Layout block updated to match the tree.

## Cross-pollination applied
- **quilt-verilog re-run-over-trust discipline:** re-ran tests, hit live API, diffed vendored engine against upstream commit rather than trusting the attribution header.
- **Honest-boundary booking (dated notes, not history rewrites):** the shelf-split story stands; the growth beyond it is booked as a dated update note.

## Commit
- `0816f98` on `master` — "audit round 6: fleet-static-host: README stale-claim fixes — run_worker_first list, layout now covers mcp/uscp/tools/forest migrations + dated note; vendoring re-verified by diff". Normal push, no force, nothing deleted.

## Flagged for Casey
- Nothing broken. Minor observation: live D1 now has a `telemetry` sheet not present in committed `seed/sheets/` (runtime-generated) — expected, but worth knowing if re-seeding ever does a wholesale replace of sheets it doesn't know about.
- README still centers the original "static shelf" story while the Worker has grown search/MCP/TTS surfaces; the dated note bridges this, but a proper README restructure might be worth a future round.
