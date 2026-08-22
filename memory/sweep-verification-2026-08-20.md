# Sweep Verification Report — 2026-08-20 (ship-gate)

**Verifier:** subagent sweep-verify · **Date:** 2026-08-20 · **Method:** read-only inspection (no commits/pushes made)
**Reference:** post-sweep-checklist-2026-08-20.md · org-sweep-results-2026-08-20.md

---

## Verdict: ✅ SHIP

Sweep commits are exactly as claimed: md-only, correctly scoped, protected compounds intact,
renamed targets all resolve, dead-annotation 250/250 (one cosmetic duplicate), nothing pushed,
nothing mid-commit. One optional one-line cleanup before push (see Anomaly 1).

---

## Gate 1 — Per-repo commit verification: ✅ PASS (13/13 dirs, 13 repos checked)

All sampled sweep commits match the convention `docs: org-wide link repair — repo renames + master→main (scout phase 2)`
and their short hashes match the results table exactly. **Zero non-markdown files changed in any sweep commit.**

| Repo | HEAD sweep? | Hash (matches table) | Files changed | Non-md files | Anomalies |
|---|---|---|---|---|---|
| hermes-perception | ✅ HEAD | 3210b4b ✅ | 1 | 0 | none |
| officers-quarters | ✅ HEAD | aa1144f ✅ | 4 | 0 | none |
| mud-arena | ✅ HEAD | 9c3bf5f ✅ | 6 | 0 | none |
| tensor-midi | ✅ HEAD | 3faadce ✅ | 7 | 0 | none |
| ternary-tenforward | ✅ HEAD | 35a0b80 ✅ | 2 | 0 | none |
| lucineer-brain | ✅ HEAD | 141eefb ✅ | 2 | 0 | none |
| fleet-wiki | ✅ HEAD | 36c80b3 ✅ | 2 (README, CONTRIBUTING) | 0 | none |
| EXOCORTEX | ✅ HEAD | ae40f14 ✅ | 1 | 0 | none |
| zeroclaw | ✅ HEAD | 21bc2c7 ✅ | 4 | 0 | none |
| elephant | ✅ HEAD | ba67482 ✅ | 3 (docs/*.md) | 0 | pre-existing dirty worktree (see note) |
| collective-unconscious | sweep in history; HEAD=35bacdd (docs: D1 binding, +8 lines README) | 2065a2d ✅ | 1 | 0 | extra local docs commit on top — expected, md-only |
| superinstance-profile | sweep in history; HEAD=466bd42 (doubled-URL fix) | b5ff526 ✅ | 1 | 0 | URL-fix commit already landed (see Gate 4b) |
| lucid-dreamer (luciddreamer-vision) | **No sweep commit** — legit skip | — | — | — | verified no-op: 0 tracked md files contain any old name; remote = SuperInstance/lucid-dreamer.git; dry-run.tsv confirms no matches |
| log-tensor | **No sweep commit** — legit skip | — | — | — | verified no-op: only tracked md = README.md, references `logtensor` (its real GitHub name, no matches); murmur resolves on GitHub |

Notes:
- `luciddreamer-vision` local dir does not exist; renamed clone is `lucid-dreamer` (checked as substitute).
- elephant dirty files (`SLOPE-REGRESSION-2026-08-20.md`, `scripts/slope_regression.py` M; `STAGE2-CORPUS-DESIGN…` untracked) are the documented pre-existing mid-write agent work — NOT in the sweep commit, not sweep-touched, do not block push.

## Gate 2 — Catastrophic-match audit: ✅ PASS (426 changed +/- lines reviewed)

- **Over-renames (identifier rewrites): NONE.** The 4 grep hits were all correct: prose renames
  (`mud-arena already has` → `mud-engine already has`) and repo-path-prefix renames where the
  internal filename correctly survived (`tensor-midi/native/tensor_midi.c` → `fleet-jepa-midi/native/tensor_midi.c`;
  `mud_arena.cu` filename untouched).
- **Hyphen-compound protection: ZERO violations.** `lau-tensor-midi`, `flux-tensor-midi`, `tensor-midi-core`,
  `zeroclaw-arena`, `zeroclaw-plato`, `study-luciddreamer-vision`, `officers-quarters-smp`, `forgemaster-shell`
  all absent from every changed line.
- Code-block strings inside markdown were updated to new names (docker image `mud-engine`, `cd hermes-avatar`,
  `import … from 'hermes-avatar'`) — doc examples mirroring the renames; md-only, no source files touched.
- `createPerceptionStack()` link correctly rewritten to `hermes-avatar/blob/main/src/index.ts`.

## Gate 3 — Dead-annotation 250/250: ✅ PASS (1 cosmetic duplicate)

- Corpus-wide (all md, exact SuperInstance scope): **250 dead links, 249 cleanly annotated, 0 unannotated, 0 misplaced.**
- The 250th link is annotated but **doubled**: `hermes-nmi/README.md:178` →
  `([Living Minds](…/the-living-minds)) (dead) (dead)`. Annotation is adjacent to the correct link — cosmetic only.
- 5-file deep sample all correct: dual-band-guard/README (1/1), hermes-perception/README (1/1), ACE-Step-1.5/README (1/1),
  the-living-minds/README (3/3), wesley-journal/README (1/1).
- Correctly NOT annotated (live/other): `flux-flow-state` links, `the-living-minds.pages.dev` domains,
  `cocapn/forgemaster` (different org), `ai-writings` local paths.

## Gate 4a — Push safety: ✅ PASS

- All 13 repos `[ahead 1–2]` of origin — local-only as intended; no `[behind]`, no divergence, no unmerged paths/UU.
- No unstaged changes in any sweep-touched file (only elephant's documented pre-existing worktree files).
- No merge conflicts anywhere in the sample.

## Gate 4b — superinstance-profile URL queue (checklist item 4): ✅ ALREADY DONE

- Commit `466bd42 fix: repair doubled URLs…` sits on top of the sweep commit (8 insertions/8 deletions = 9 URLs / 8 lines).
- `grep -c 'SuperInstance/https' README.md` → **0**. L506 `[zeroclaw]` href → `SuperInstance/zeroclaw-dissertation` ✅.
  L492 `SuperInstance/SuperInstance.git` (self-clone) correctly left. Dead annotations on L105 verified in place.

## Gate 5 — Known-good mapping resolves: ✅ PASS (8/8 + bonus)

| Target | ls-remote HEAD |
|---|---|
| hermes-avatar | d6a5008 ✅ |
| elephant | 3af376b ✅ |
| lucineer-fleet-wiki | c737dd1 ✅ |
| fleet-jepa-midi | 4fc201a ✅ |
| lucid-dreamer | f17a010 ✅ |
| mud-engine (bonus) | 17bce11 ✅ |
| zeroclaw-dissertation (bonus) | b5630aa ✅ |
| exocortex-core (bonus) | c7f1c1f ✅ |
| murmur (bonus, log-tensor target) | 3b5f895 ✅ |

---

## Anomalies (2, both minor / non-blocking)

1. **hermes-nmi/README.md:178 — double dead annotation** `(dead) (dead)` on the the-living-minds link (only instance in the corpus).
   Adjacent to the correct link, zero link breakage. Optional one-line cleanup (`s/ (dead) (dead)/ (dead)/`) before or after push.
2. **hermes-perception/README.md code block:** `import { createPerceptionStack } from 'hermes-avatar'` — doc example assumes
   the npm package renamed in lockstep with the repo. Verify package name if the package is published; doc-only, non-blocking.

## Recommendation

**SHIP** — 13/13 sampled repos verify clean (md-only sweep commits at claimed hashes, ahead-of-origin only, no conflicts);
all 8 renamed targets resolve; 250/250 dead links covered (one cosmetic duplicate); superinstance-profile URL fix already landed;
the two unswept sample repos (log-tensor, lucid-dreamer) were verified legitimate no-ops. Fix the hermes-nmi double annotation
as an optional cosmetic follow-up, then push docs-first per the planned push order.
