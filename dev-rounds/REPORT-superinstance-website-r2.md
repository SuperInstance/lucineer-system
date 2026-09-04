# Dev Round 2 Report — superinstance-website

**Date:** 2026-09-03 (07:38 AKDT start) · **Repo:** SuperInstance/superinstance-website · **Default branch:** `master` (clone at ~/projects/superinstance-website, was up to date; pulled clean before work)

## Commit
`41c899fa070bfb457a71f59047a08cbc50ad852d` — "audit round 2: superinstance-website: fix 8 dead footer/card links …" (pushed to origin/master, no force, no deletions)

## Links checked
- **Live-site link check** (superinstance.dev, actual deployed state): confirmed `/specs`, `/essays`, `/studio`, `/tap`, `/calendar.html`, `/pomodoro.html` return **404**, `/docs` and `/bridges` 301→404 (directories with no index.html). Footer (index.html + feature.html) and two app cards pointed at all of these.
- All external links verified 200: quilt-verilog repo + CHIP-MATRIX/NOVEL-ENHANCEMENTS/EXPLAINER, quilt-scratch + 90s-MACHINES, ai-writings papers 225/226, all 5 fleet-static-host paths, mist/scrap-quilt workers, luciddreamer.ai, zeroclaw-dissertation.

## Fixed
1. Footer links (index.html + feature.html): `/specs`→`/spec-explorer.html`, `/essays`→`https://ai-writings.pages.dev/`, `/studio`→`/studio-v2.html`, `/tap`→`/tap-tavern.html`, `/docs`→GitHub docs dir, `/bridges`→GitHub bridges dir.
2. Cards: `/calendar.html`→`/family-calendar.html`, `/pomodoro.html`→`/pomodoro-quilt.html` (both files).
3. **Wrong evidence link:** headline card "📊 Chip matrix — three families, measured" pointed at quilt-verilog's `docs/CHIP-MATRIX.md`, which is actually an edge-inference benchmark doc (RTX 4050 vs CPU), *not* the FPGA evidence. Replaced with `docs/SYNTHESIS-RESULTS.md` and relabeled.
4. **README fact fixes:** build-pipeline diagram claimed build-domains.sh reads ecosystem-data.json + quality-report.json — it reads only `domains.json` + `templates/base.html` and writes `dist/<domain>/`. Also corrected the page table (ecosystem.html = live Workers APIs, search.html = fleet-vector-api /search, not client-side JSON) and the API table (ecosystem-data.json is a fleet inventory snapshot, not a crate-dependency registry).

## Claims
- ✅ Verified against quilt-verilog ground truth: 2B model beat human hand-tune by 10 points (EXPLAINER.md), biggest models produced no valid design, ratchet caught regressions, Variety Ledger calm-regime specialist, T1–T8 program, 5+1 opcode model.
- ⚠️ **Flagged + corrected:** headline "5+1 opcodes now **run on** iCE40, UP5K and ECP5" overstated — SYNTHESIS-RESULTS.md states plainly "Nothing on this page is tested on hardware … a bitstream that packs is not a bitstream that boots." Reworded to "close synthesis … bitstreams packed, not yet booted on hardware."
- ⚠️ Flagged, not rewritten: README "Adding a New Crate" says to hand-edit ecosystem-data.json — that file is a generated snapshot (2026-06-11, counts stale vs fleet). Left for owner decision.
- ℹ️ ecosystem.html polls superinstance-vectorize.worker.dev (currently 404) but fails gracefully by design (status page) — no fix needed.

## Cross-pollination
- Applied quilt-verilog's **honest-boundary discipline** to the public headline: keep the achievement, state the boundary (synthesis vs boot) in place — same pattern as round 1's lucineer-system note. No history rewritten, nothing deleted.

## Counts
Links checked: ~60 (24 site paths live-verified + ~30 external + README refs) · dead-and-fixed: 9 (8 nav/card + 1 evidence) · claims verified: 6 ✅ · flagged: 2 ⚠️ + 1 ℹ️
