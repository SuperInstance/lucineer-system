# Dev Round 11 Report — superinstance-website

**Date:** 2026-09-03 (17:57 AKDT start) · **Repo:** SuperInstance/superinstance-website · **Default branch:** `master` (clone at ~/projects/superinstance-website, up to date at 41c899f before work; no force-push, no deletions)

## Commit
`62f0405` — "audit round 11: superinstance-website: dated note on stale 'Adding a New Crate' steps … fix browse.html data-source row …" (pushed to origin/master)

## Round-2 follow-ups (all resolved)
1. **8 dead-site-link fixes from 41c899f re-verified live** — no 404 regressions. All 200: `/spec-explorer.html`, `/studio-v2.html`, `/tap-tavern.html`, `/family-calendar.html`, `/pomodoro-quilt.html`, `/`, `/feature.html` on superinstance.dev; external replacements `ai-writings.pages.dev` and GitHub `docs`/`bridges` tree URLs also 200.
2. **"opcodes run on iCE40/UP5K/ECP5" correction still intact** — index.html headline reads "close synthesis on iCE40, UP5K and ECP5 — bitstreams packed, not yet booted on hardware" with 18/18 testbench / 6/6 formal / HX8K 44.4 MHz / 98% LC numbers (matches quilt-verilog SYNTHESIS-RESULTS.md ground truth as re-checked in round 3). Evidence link points at SYNTHESIS-RESULTS.md, correct.
3. **"Adding a New Crate" stale section — FIXED this round.** Verified against the repo itself: `ecosystem-data.json` carries `"generated": "2026-06-11T14:57:00-08:00"` (1,605 repos / 1,494 crates), has **no in-repo generator** (no script references it; committed exactly once), and is consumed at runtime by `status.html`. `build-domains.sh` reads only `domains.json` + `templates/base.html` (re-read line by line, confirms round 2). Added a **dated note** documenting all of this; original 4 steps kept verbatim for history — no rewrite.

## Links checked
- **22 external links** across README.md + index.html + feature.html (quilt-verilog repo + SYNTHESIS-RESULTS/NOVEL-ENHANCEMENTS/EXPLAINER + g3-kinduction tree, quilt-scratch + 90s-MACHINES, ai-writings pages 225/226 + root, all 5 fleet-static-host paths, mist/scrap-quilt workers, luciddreamer.ai, zeroclaw-dissertation, SuperInstance org) — **all 200 via curl -L, zero dead**. (The bare `quilt-verilog/quilt-verilog` owner guess 404s; the site itself never uses it — correct owner is SuperInstance, all in-use links live.)
- **8 round-2 fixed site links** re-verified live on superinstance.dev — all 200.
- README relative-path references (build-domains.sh, domains.json, templates/, tutorials/, dist/) — all resolve in-tree.

## Claims
- ✅ `quality-report.json` "291 KB" — actual 291,431 bytes, exact.
- ✅ build-pipeline description (round-2 corrected) matches build-domains.sh source — re-read and confirmed.
- ⚠️ **Fixed:** README page table claimed `browse.html` data source = `domains.json`; browse.html fetches **only** `quality-report.json` (0 references to domains.json) — corrected in-place with a dated parenthetical. Round 2's table pass fixed ecosystem/search rows but missed this one.
- ℹ️ ecosystem-data.json snapshot counts (June 2026) stale vs live fleet — inherent to a snapshot; documented in the new dated note, no rewrite.

## Cross-pollination applied
- **Honest-boundary booking** (quilt-verilog / lucineer-system style): both fixes are dated in-place notes; original text preserved verbatim beneath/around them — history not rewritten.
- **Verification-by-rerun** (elephant/crab-traps discipline): rather than trusting round 2's report, re-verified every round-2 fix live (curl), re-read build-domains.sh end-to-end, and grep-verified JSON consumers (status.html → ecosystem-data.json; browse/stats.html → quality-report.json) before claiming the README row was wrong.
- **Byte-match discipline**: the dated note cites the exact snapshot timestamp and counts from the file itself, not paraphrase.
- Tapestry trail-presentation / archive-by-rename: not applicable this round (nothing retired).

## Counts
Links checked: ~35 (8 site re-verifications + 22 external + in-tree relative refs) · dead: 0 · stale claims fixed: 2 (browse.html data-source row; "Adding a New Crate" flagged-in-r2 now note-fixed) · claims verified: 4 ✅

## Verdict
No regressions from round 2; both prior flags now closed. One new commit, pushed clean.
