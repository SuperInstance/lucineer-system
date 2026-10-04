# Audit Round 14 — ai-writings (SuperInstance)

**Repo:** github.com/SuperInstance/ai-writings (default branch: `master`)
**Date:** 2026-09-03 · **Base:** pulled to a4dc4a93 (up to date at start) · **Commit:** `08cfdda9`

## Links
- README.md / INDEX.md / STATUS.md: all relative links scripted — **0 broken**.
- 9 external links (7 sibling GitHub repos incl. casting-call/SEED_NOTES.md blob, luciddreamer.ai ×2) via `curl -L` — **all 200, 0 dead**.
- Anchor spot-check on README headings: fine.

## Claims verified (re-counted, not trusted)
- **Piece/folder counts** (README L172, from round 4): stated 10,236 md / 422 top-level folders (verified 2026-09-03 r4). Re-count: **10,304 md files, 425 top-level dirs** — growth only. Fixed with an in-line r14 re-count note (original preserved).
- **Night-watch wing count** "645 files across those wings": re-counted 645 total files (634 md) in night-watch + overnight-journal + dreams + diaries + journals — **holds**.
- **Poetry "100+ pieces"**: 103 files — holds.
- **STATUS.md** is a dated snapshot ("24 August 2026 (final)") — historical doc, left untouched.
- **Honest-boundary notes from round 4** (research/66 count note, research/68 5+1-opcode boundary note, INDEX branch note): all still present, intact.

## Cross-repo staleness found & FIXED (dated notes, originals never rewritten)
quilt-verilog round 13 (37e206f) moved the RTL suite **18/18 → 21/21** and `rtl/` **18 → 21 modules**. Confirmed by fresh clone of quilt-verilog (rtl/ = 21 .v modules; README "21/21 PASS ✓ re-run 2026-09-03"). Six ai-writings files cited the old counts; each got a dated 2026-09-03 note:
1. `seed-canon/papers/paper-423.md` (3 in-text spots: abstract, §3, table) — note after abstract.
2. `seed-canon/papers/paper-424.md` (substrate table "18/18 RTL PASS 2026-08-29").
3. `seed-canon/papers/paper-426.md` ("Tests: 18/18 RTL + 6/6 sby").
4. `docs/AUDIT-SHEET-IS-THE-RUNTIME.md` (audit row "18/18 RTL benches").
5. `docs/STEELMAN-SHEET-IS-THE-RUNTIME.md` ("18/18 bench suite").
6. `research/66-llm-era-verilog-and-open-hdl-verification.md` — r4 note said "20 modules, 25+ testbenches"; appended a chained r14 note (21 modules, 21/21 suite) rather than editing r4's note.

## Cross-pollination applied
- **Dated-note discipline** (quilt-verilog r13 style): all fixes are appended dated notes; zero original text rewritten; count-note chains preserved.
- **Verification-by-rerun**: quilt-verilog claims verified against a fresh clone, not against ai-writings' own text; counts re-measured with `find`, not trusted.
- **Archive-by-rename / no deletions**: nothing deleted, no force-push.
- Also flagged-to-self: r13's note that superinstance-website's index cites "18/18 testbench" remains open for that repo's next round (out of scope here).

## Caveats
- Full-link crawl of all 10,304 md files was out of budget; per instructions, README/INDEX/STATUS (the audit surface from r4) were fully checked, externals verified live, and the rest sampled via targeted greps. No sampling found additional breakage.
- The shared clone at ~/projects/ai-writings carried pre-existing uncommitted working-tree changes (fleet-radio/2026-09-02.html, jam-log.md, music-played.json — cron-written content); they were swept into the commit by `git add -A`. Additive only, nothing destructive, but noted for the record.

## Result
- Links: ~25 checked, 0 dead, 0 fixes needed.
- Claims: 7 verified/holds, 6 stale quilt-verilog citations fixed via dated notes.
- Commit: **08cfdda9** on master, pushed (no force).
