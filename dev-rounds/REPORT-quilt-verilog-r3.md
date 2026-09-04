# Audit Round 3 — quilt-verilog (SuperInstance)

**Date:** 2026-09-03 · **Auditor:** cross-pollination + fact-check subagent (GLM-5.3)

## Repo state
- **Location:** `~/projects/quilt-verilog` (local clone of `git@github.com:SuperInstance/quilt-verilog.git`)
- **Default branch:** `master` (origin/HEAD → master); local master was 39 commits behind → fast-forwarded before audit (no force ops, no deletions)
- Note: work-in-progress branches (`g3-kinduction`, `audit-r3`, `cosim-scaleup`) exist and were left untouched. Untracked local scratch file `tb/scratch_snaplog_probe.v` left alone.

## Link check
- **82 markdown files** scanned (README + docs/ tree, recursively).
- **145 relative links checked — 0 broken.** All docs-map targets (THE-TICK, FORMAL-PROOFS, SYNTHESIS-RESULTS, academic/ tree, annals-1905, review-*.md, proposals/*) resolve. An earlier false-positive pass (naive root-relative resolution) was discarded; per-file relative resolution is the correct method.
- **External GitHub sibling links verified live via `gh`:** quilt-c (main), quilt-rust (main), quilt-timesfm (master), quf-vhdl (main) — all exist; quf-vhdl's `docs/VERILOG_VS_VHDL.md` cross-link target exists in that repo. ai-writings references resolve to `SuperInstance/AI-Writings` (GitHub is case-insensitive for repo names; papers 66/67/68/70 cited by name as external companions, not links — fine as-is).

## Claims verified
- **18/18 RTL testbench suite:** run_suite.sh registers exactly 18 benches ✓ (README's 18/18 claim matches).
- **34/34 behavioral sim:** re-ran `make sim` live during audit — `Ran 34 tests … OK` ✓.
- **6 SymbiYosys proofs:** Makefile FORMAL_SBY pins exactly 6 (5 BMC + 1 k-induction) ✓.
- **Synthesis numbers:** iCE40 HX8K 7,596/7,680 LC 98%, UP5K 80.1%, ECP5 ladder — README table matches docs/SYNTHESIS-RESULTS.md, which itself records the fmax corrections (post-placement estimates once quoted as final) — honest-boundary discipline intact.
- **5+1 opcode model:** consistent across README/RTL (OP_BIND..OP_NAK); matches superinstance-website's corrected framing.
- **"Synthesis only, nothing booted" overstatement check:** CLEAN. README's "Honest limitations" states "The bitstream has never met a board; no PCF exists"; SYNTHESIS-RESULTS.md repeats "Nothing on this page has met a board." No doc claims opcodes "run on" hardware. superinstance-website's corrected headline ("bitstreams packed, not yet booted on hardware") is consistent with — not contradicted by — this repo.
- **lucineer-system pipeline claims:** no cross-references from quilt-verilog to lucineer-system found; nothing to contradict.
- **superinstance-website corrected headline (2B-beats-hand-tune / T1–T8):** no "2B/hand-tune" claim exists in this repo. T1–T8 lives in docs/NOVEL-ENHANCEMENTS.md (present on master) and the website links to it correctly, including g3-kinduction branch spike links (spikes/225-e1-interference-tick/{EXPLAINER,DIVERGENCE,PORTING-NOTES}.md all exist on that branch).

## Claims flagged & fixed
- **Stale module count (fixed):** README said `rtl/ — 17 modules`. Phase 251 (a07bff0, 2026-09-03) added `rtl/live_canon.v`, making 18. Fixed to "18 modules (17 fabric + `live_canon.v`, the Phase 251 Live Canon)". Only stale item found.

## Cross-pollination
- **Byte-match control discipline (source repo):** kept intact — no rewording of verification claims, no retroactive result edits.
- **Honest-boundary booking:** already native here (limitations section, failed prove-mode documented) — reinforced, not rewritten.
- **Arch-by-rename:** confirmed intact (`README.archived-20260830.md` preserved).
- **Tapestry doctrine trail-presentation:** declined — README's map-style index (docs/INDEX.md) already serves that role well; a rewrite would be churn without evidence of benefit.

## Result
- **Commit:** `7e923c5` on `master` — `audit round 3: quilt-verilog: fix stale rtl/ module count (17→18) after Phase 251 live_canon.v; all README/doc links + headline claims re-verified (18-bench suite, 34/34 sim re-run, 6 sby, synth tables, sister repos live)`
- Links: 145 checked / 0 broken / 0 link fixes. Claims: 7 verified, 1 stale (fixed). Cross-pollination: 1 applied (count-honesty fix in source's own style), 1 declined with reason.
