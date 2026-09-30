# Scout: CANON CELL block — SuperInstance repo survey, wave 2 (2026-09-29)

Scope: 7 repos, all shallow-cloned to /tmp/scan2-canon/ (read-only). Every repo is tiny
(5-6 files, 20-24K). I read 100% of non-git content in all 7 — full coverage, not sampling.
All last commits: 2026-09-20, "Merge pull request #1 from SuperInstance/canon-md" — a
batch PR stamped CANON.md identity cards across the whole family.

## What a "canon cell" is (focus q-a)

A canon cell = the `CANON.md` file at repo root: a YAML identity card. Fields observed
identically in all 7: `canon: 1`, `name`, `mission`, `state: active`, `family: canon`,
`vessel: unattributed`, `born_from: []` (parentage), `feeds: [...]` (downstream consumers,
e.g. `quilt-canvas-demo`), `owed_by: []`, `canonical_docs: [README.md]`, `ledger: git-log`,
`verified: 2026-09-18|20`. Each cell claims: identity+mission, lineage (who birthed me /
who I feed / who owes me), which docs are canonical, and a staleness date. Verification is
NOT cryptographic in these repos: `ledger: git-log` means git history is the evidence
ledger, plus a human `verified:` date stamp. Server-side, the Live Canon API does have one
real self-check: `/api/canon/hash` returns `{state_hash, paper_count: 71, test_cell_hash,
canon_target}` where live `state_hash === canon_target` (verified 2026-09-29) — a
current-vs-target drift comparison. That's the strongest verification mechanism in the block.

## Per-repo findings

### canon-hash (v0.1.0, 20-line index.js)
FNV-1a 64-bit state-hash fetcher. `stateHash()` GETs `/api/canon/hash`; `getHex()` handles
`h.hash || h.state_hash` shape drift. Works against live API today. 19-line live test.
The hash endpoint response (state_hash + paper_count + canon_target) is the drift-check
contract — best single steal in the family.

### canon-paper (v0.1.2, 73 lines)
`paper(n)`, `listPapers()`, `papersByAuthor/Phase/FNumber()`. Paper shape:
`{id: "paper-408.md", number: 408, title: "F98 — ...", f_number, phase}` (phase is an
integer ~222, f_number ~98 — numbered doctrine epochs). Trick worth noting: to fetch a
known paper's BODY it re-uses the claim endpoint, claiming the paper's F-number as topic
because "F-number recall has the highest weight in the scoring" (index.js:33-40). Currently
broken: `/api/canon/claim` 404s live. `papersByAuthor` actually filters by title substring
(misnamed). Bug: `paperCount()` in canon-claim does `Object.keys(data).length` on
`{papers:[...]}` → returns 1, not the count.

### canon-recs (v0.1.0, 118 lines, deps: canon-claim + canon-graph)
The most substantive file in the block. `recommendByTopic`/`recommendByPaper` combine
claim() (authority winner) with ghost-style kNN over a **16-dim dial-vector** built by
`cellToDials()` (lines 23-51): `[numQ, titleLo, fQ, phaseQ, yearQ, nRefsQ, titleHi, 0×9]`
where numQ=min(number,500)*131, fQ=f_number*218, phaseQ=phase*218, yearQ=(year-1970)*546,
nRefsQ=min(0x7FFF,refcount*256), and titleLo/titleHi are 16-bit slices of an FNV-1a-64
hash of the title. Plain cosine over these. Zero ML embeddings — deterministic, cheap,
explainable. 32-line live test (0 asserts; throw-on-failure style).

### canon-zoo (2 files, no code)
README only: "A system prompt for inspiration through play. Hit the button. Watch what
happens." The actual prompt is NOT in the repo — dead-end shell or prompt lives elsewhere.

### canon-suite (v0.1.0, 18 lines)
Meta-package re-exporting claim/drill/stateHash/getHex/fetchCanon/renderGraph. package.json
test script references `test/test.js` which DOES NOT EXIST → suite self-test is broken.
Otherwise trivial.

### canon-claim (v0.1.0, 45 lines)
Thin client for `/api/canon/claim?topic=` and `/api/canon/drill?topic=`. Drill response
shape (from test): `{curriculum: {doctrine, implementation, verification: {f_number,
title,...}}}` — a topic expands into a 3-part curriculum. That CLAIM→DRILL→curriculum
contract is the block's best conceptual steal. BUT: both endpoints return 404 against the
live API today, and the test (expects `claim('trust ladder')` → winner f_number===168)
would fail. The test docstrings are the only surviving spec of the claim/scoring behavior
("F-number recall has the highest weight").

### canon-graph (v0.1.0, 59 lines)
`fetchCanon()` + `renderGraph(papers, {start, depth, maxFNumber})`: depth-limited DFS over
`ref_papers`/`ref_f_numbers`, visited-set, cap `maxFNumber=200`, line cap 200 when walking
all. Renders `paper-N (F-M) → paper-X, F-Y  Title`. Bounded-traversal pattern is reusable.

## Focus answers (b), (c), (d) — definitive negatives

- (b) JEV gate: ABSENT. `grep -rniE 'jev|mechanism|externality'` across all 7 repos = 0
  hits. No jev_gate.py, no 0.7 threshold, no MECHANISM/EXTERNALITY inputs/outputs anywhere.
- (c) Promotion velocity: ABSENT. No velocity/sprint/promotion metrics. Closest proxy:
  per-cell `verified:` dates + single-batch canon-md PR (all 7 same day).
- (d) Evidence-forms drift: NEITHER side is in this block. Zero hits for
  witness/receipt/memory, direct/witness/pattern, weights 1.0/0.7/0.4, or "R10". No merge
  or ruling artifact here. The drift must live in the foundation/quilt-side repos — the
  canon block is clean of it. (Paper 408 title seen live: "F98 — The 165-Test
  Polyformalism Conformance Suite"; 409: "F99 — The Quilt Atlas: 47 Repositories, 280K
  Lines of Code, 1500+ Tests" — the ruling text likely sits in the quilt/paper corpus.)

## (e) Reuse for Cloudflare Workers + D1 + Vectorize context API

Directly portable: (1) CANON.md frontmatter as the claim schema (identity/lineage/owed_by
in one file — trivially a D1 row + a file); (2) the /api/canon/hash contract
(state_hash vs canon_target drift self-check + paper_count) as /api/context/hash;
(3) cellToDials() as a deterministic 16-float Vectorize vector when you want metadata-KNN
without embedding-model cost/latency — quantized ints make cosine behave like feature
matching; (4) drill's {doctrine, implementation, verification} curriculum shape as the
context-API response envelope; (5) renderGraph's bounded DFS for provenance views.
Demotion-receipt discipline: NOT present in this block (no receipts, no tiers).

## RANKED TOP-5 STEALABLES

1. `canon-recs/index.js:23-51` — `cellToDials()` + `cosine()`: deterministic 16-dim
   quantized metadata embedding (FNV-1a title + year/phase/f_number/refcount) for
   zero-model-cost Vectorize KNN. Exact quantizer constants in file.
2. `https://live-canon.superinstance.dev/api/canon/hash` response contract
   `{state_hash, paper_count, test_cell_hash, canon_target}` (client: canon-hash/index.js)
   — server-side drift self-check; adopt as-is for the context API.
3. `<repo>/CANON.md` (all 7, e.g. canon-claim/CANON.md) — machine-readable claim cell:
   born_from/feeds/owed_by lineage + canonical_docs + ledger type + verified date.
   The whole claim/tier discipline in one YAML file.
4. `canon-claim/test/test.js:12-20` + `canon-paper/index.js:33-40` — CLAIM→DRILL
   curriculum contract `{doctrine, implementation, verification}` and F-number-as-topic
   lookup trick ("F-number recall has the highest weight") — spec survives only in tests.
5. `canon-graph/index.js:14-58` — `renderGraph()`: bounded DFS (depth, maxFNumber,
   visited-set, 200-line cap) reference-graph renderer for provenance views.

## What I could NOT determine

- Where the JEV gate / evidence-forms rulings actually live (not in this block; likely
  foundation-, quilt-, or paper-corpus repos — next-wave targets).
- The claim scoring formula (winner.score seen = 366.8; weights unknown; endpoint 404s).
- canon-zoo's actual system prompt (repo is README-only).
- Whether /api/canon/claim|drill were removed or moved (no server code in this block).
- Full repo history: shallow clones (depth 1) — only the canon-md merge commit visible;
  earlier claim/tier evolution unverifiable from here.
- The `vessel: unattributed` semantics (no doc explains it in this block).
