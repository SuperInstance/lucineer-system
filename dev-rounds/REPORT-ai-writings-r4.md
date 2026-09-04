# Audit Round 4 — ai-writings (cross-pollination + fact-check)

**Date:** 2026-09-03 · **Repo:** SuperInstance/AI-Writings · **Default branch:** master · **Commit:** `3dffbbfc` (pushed)

## Method

Pulled (`git pull --ff-only`, already current at `6465f2dd`). Extracted every markdown link from the five top-level docs (README.md, INDEX.md, STATUS.md, AGENTS.md, ORGANIZING.md) via script: relative paths checked against the filesystem, external URLs checked via `gh api` (authenticated as SuperInstance) and `curl -L`. Images (`<img src>`, `showcase.html` raw.githubusercontent media) checked separately. Numbers/claims re-measured with `find`/`git ls-files` counts rather than trusted. quilt-verilog cross-references checked against the live sibling checkout in `~/projects/quilt-verilog`.

## Links

**~75 links checked, 0 dead.**
- 40+ relative links in the 5 docs: all resolve (incl. all "The Door" quote links, all 13 wing directory links, hero art `radio-theater/compass-head-radio-hour/images/hero-compass-head.png`, `hermes/hermes.webp`, `artwork/the-tap/the-tap-portrait.jpg`).
- External: 7 sibling repos (baton-system, casting-call, collective-unconscious, elephant, fleet-radio, luciddreamer-ai, quilt) — all exist (baton-system is private, exists per auth; rest public). Blob paths verified: `baton-system/docs/GC_AGENTS.md`, `baton-system/docs/gc-intelligent-README.md`, `casting-call/SEED_NOTES.md` — all 200. `luciddreamer.ai/` and `/compass-head/` both 200.
- `showcase.html` media: 8/8 raw.githubusercontent assets exist in-repo on main; `assets/fleet-media.js` tracked. AGENTS.md's `.gcconfig` reference exists.
- INDEX-referenced files spot-checked: essays 84/85/86/87/94/95/98/100/114, `essays-drafts/the-degraded-channel-was-the-design.md`, `seed-canon/stories/01…06`, `experiments/quilt-holodeck.html` — all present.

## Claims

Verified by re-measurement (2026-09-03): **10,236 md files** (README said 8,800+ — understated floor, now corrected to 10,000+), **422 top-level folders** (said 130+), **poetry = 102 non-README files** (said 72), **essays 616** (said 600+ ✓), **645 files in night-watch wings** (said 460+). Essays/Papers/essays table in INDEX matches files.

Flagged, not rewritten (dated snapshots — history preserved):
- **STATUS.md vs INDEX.md same-day inconsistency** (both 2026-08-24): STATUS "final" says 7 repos / 264 tests; INDEX v6 says 6 repos / 113 tests and a "state snapshot" of 8 repos / 111 tests. Three different counts on one date — different lanes, never reconciled. Left as-is (historical records); noted here.
- INDEX "quilt-holodeck.html" listed without path (lives in `experiments/`) — not a link, left alone.

## Cross-pollination (honest-boundary style, in place — no history rewritten)

1. **research/66** — "`rtl/` now holds nine modules with eight passing testbenches": superseded by quilt-verilog growth (20 rtl modules, 25+ tb, re-counted this round; round-3 audit measured 18). Added a dated count-note blockquote directly after; original sentence preserved.
2. **research/68 (Back Deck Papers)** — "five opcodes" doctrine claim: quilt-verilog doctrine is now the 5+1 model (OP_ACK/OP_NAK added; every op answered). Added an inline dated boundary note; original preserved.
3. **INDEX.md** — "Branch on GitHub: writers-room-session-2026-08-22" was stale framing (branch still exists — verified `a71da66` on remote — but content is on master, the default). Added in-place note rather than changing the historical claim.
4. **README "The Numbers"** — live stats, not history: refreshed (10,000+ pieces / 400+ folders with verification date, poetry 100+, night-watch 600+ with file count).

## Commit

`3dffbbfc` on master, pushed. 4 files changed, 8 insertions, 6 deletions. No deletions, no force-push, nothing archived (nothing needed retiring).
