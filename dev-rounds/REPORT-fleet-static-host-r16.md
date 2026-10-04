# Audit Report — fleet-static-host, Round 16 (2026-09-04)

Fresh clone `gh repo clone SuperInstance/fleet-static-host` → default branch **master** (also has `lobby-tapestry` branch, untouched).

## ⚠️ Topology note
At clone time master HEAD was already **a83548c** — a commit titled *"audit round 16: fleet-static-host: re-verified tests/vendoring/live endpoints; booked 5th D1 sheet (telemetry/uscp) as dated note"* (SuperInstance <fleet@superinstance.dev>, Sep 3 22:45 −0800 ≈ 1.5 h before this run). A prior/partial r16 run appears to have already landed. Per round-3 discipline (quilt-verilog lane commit 7e923c5), I **independently re-verified every claim in that note rather than assuming it**. All of its claims check out (details below). This round therefore made **no new commit** — nothing further was broken.

## Links (~20 checked, 0 dead)
- Live workers.dev: `/`, `/papers/`, `/writings/`, `/scrap/`, `/mist/`, `/ternary/`, `/api/quilt/health`, `/canon/search`, `/forest/search` — all 200. `POST /mcp` → 401 (auth challenge, as designed). `POST /ai/tts` with JSON body → 200. `GET /ai/tts` → 500 (falls past the POST-only route; minor routing nit, not a doc claim — **flagged, not fixed**, code changes out of audit scope).
- KaTeX CDN (jsdelivr 0.16.11 css/js/auto-render) — 200.
- `SuperInstance/quilt-cloudflare` @ `3c293f6` — repo + commit reachable via `gh api` (date 2026-08-20T17:15:46Z, matches README).
- Scripted relative-link check across all in-tree `*.md` (README, tools/MCP-BRIDGE.md, tools/FOREST-HEBBIAN.md, public/quilt/docs/*, public/demos/zkcanvas/context/*) — 0 dead. README's `../quilt-cloudflare` renders as the GitHub sibling-repo link on the repo root; verified live via gh api.

## Claims verified (by re-run, not trust)
- **`npm test` → 34/34 PASS** (fresh clone).
- **Vendored `src/quilt.ts` vs upstream `src/worker.ts` @ 3c293f6**: diff = attribution header only (12 added lines) + pure removals (185 lines: upstream entrypoint/MCP demo). Matches README claim exactly.
- **Live D1 vs committed sheets**: 5 sheets (lobby, papers, writings, trails, **telemetry**), 55 cells. `paper.*` = 7 ✓ README "7 papers"; `writing.*` = 24 ✓ "24 verbatim pieces"; trails 8 entries + index + note ✓; 5th sheet `telemetry` (`uscp.block_mined`) — exactly as booked by a83548c's dated note.
- **wrangler.jsonc `run_worker_first`** matches the r6-dated note (`/ai/embed`, `/ai/tts`, `/canon/search`, `/forest/search`, `/mcp`, `/.well-known/mcp` all present).
- **r6 fixes hold**: both dated notes (r16 telemetry note, r6 expanded-layout note) present in README; Layout section covers mcp.ts/uscp.ts/tools/migrations.

## Cross-pollination
- **No quilt-verilog citations anywhere in this repo** (grep across md/ts/jsonc) — the r13/r14 stale-citation class (18/18→21/21) is **absent**; nothing to fix.
- r14/r15 dated-correction-chain style: already exemplified by this repo's own r6/a83548c notes — consistent, no changes needed.

## Outcome
Nothing broken → **no commit** (per rules). Prior r16 commit a83548c independently verified true in full.
