# Audit Round 17 — SuperInstance/elephant (FACT-CHECK + CROSS-POLLINATE)

Date: 2026-09-04 (01:0x AKDT) · Auditor: r17 subagent · Scratch: /tmp/lane-r17
Default branch: `main` · Commit: `d63a9f9` (normal push after rebase, no force).

## ⚠️ Topology note: CONCURRENT r17 lane

While this lane was mid-flight, a **second round-17 commit appeared on `main`**
(`a777b0a`, ~same mandate: "module-count phrasing clarified… round-7 fixes
re-verified… re-run date booked"). This lane independently re-verified everything
rather than trusting it, resolved the resulting rebase conflict by **merging both
lanes' findings** into the PROVEN booking ("re-verified by two independent
round-17 lanes"), and preserved the sibling lane's module-count phrasing fix
(31 `.py` files under `elephant/`, root has no `.py`). Casey may want to check
why two r17 lanes were dispatched to the same repo.

## Prior-fix verification (r7: 79dcd98 + the second r7 commit bf7380d)

All prior fixes verified to hold by re-run, not by trust:

| Prior claim | r17 re-verification |
|---|---|
| 393 tests / 31 files | ✅ fresh clone: **393 passed in 33.84s**; `tests/test_*.py` = 31 exactly |
| Modules 31 + 10 dials = 41 | ✅ `ls elephant/*.py` = 31, `elephant/dials/*.py` = 10 |
| DEFAULT_DIALS = 9 dial bank (bf7380d) | ✅ `len(DEFAULT_DIALS)` = 9 |
| Quickstart numbers (+0.29/κ2.04, −0.05/κ1.96, 0.83, +0.34) | ✅ re-ran README snippet: +0.29/κ2.04, −0.05/κ1.96, distance 0.8288, gap +0.3389 — exact |
| tapnight divergence 0.389 → 0.859 | ✅ re-ran `examples/tapnight_cycles.py`: "initial 0.389 → final 0.859" — exact |
| radasound "gate 1" audit note (bf7380d) | ✅ present at docs/radasound-crossover-2026-08-22.md:205 |
| r7 README corrections (dated notes) | ✅ all intact, no regressions |

## Links checked (scripted)

- **39 relative markdown links** across README + docs/ + top-level *.md — **0 dead**.
  (One regex false positive: `docs/fleet-field-math.md` math text `(t−t1)(t−t2)` parsed
  as a link; verified line 109 is prose, not a link.)
- **0 internal anchors** to check (no `#foo` cross-refs).
- **7 sibling repos verified live via gh api**: collective-unconscious, crab-traps,
  fleet-radio, AI-Writings, mud-arena, quilt, quilt-verilog — all exist.
- No blob/deep links to AI-Writings `prose/` in this repo (the r5/r15 dead-link
  class is absent).

## Stale quilt-verilog citations (r13 change: 18/18 → 21/21)

- Grep for `18/18`, `18 rtl`, `18 module(s)`, `quilt-verilog` across all md:
  **only one quilt-verilog mention exists** (README cross-pollination section,
  no numeric citation). The stale-citation class from r14 (ai-writings) is
  **absent here** — nothing to fix. The two "21/21" hits in STAGE2-*.md are
  unrelated (visited-room sets).

## Cross-pollination / sibling-repo contradictions checked

- ai-writings r14 fixes: n/a — no quilt-verilog numbers cited here.
- superinstance-website r11/r13-note: elephant not cited by number; the website's
  own "18/18" staleness is that repo's problem, not elephant's.
- the-tap r15 classes (pytest 28/28, prose/ links, "1313 files", /api/tide):
  no such claims made in elephant docs — absent.

## Fixes applied (this lane)

Minimal — this was a near-null round:

1. README PROVEN booking: appended dated r17 re-verification note, merged with the
   sibling lane's note → "Re-verified 2026-09-04 by two independent round-17 lanes…".
2. README pytest command: appended "r17 fresh-clone re-run 2026-09-04: 393 passed in ~34s".

Nothing broken was found; both edits are additive dated notes (archive-by-rename /
honest-boundary discipline). No deletions, no force-push, no archived files.

## Commit

`d63a9f9` on `main` (rebased cleanly onto the sibling lane's `a777b0a`; README
conflict resolved by merge, sibling's module-phrasing fix preserved).
