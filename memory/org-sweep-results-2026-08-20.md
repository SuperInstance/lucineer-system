# Org Sweep Results — 2026-08-20 (Phase 2 follow-up)

**Script:** `/home/eileen/.openclaw/workspace/org-sweep/link-repair.sh` (dry/apply modes) + `fixup-annotate.sh`
**Artifacts:** `org-sweep/dry-run.tsv`, `org-sweep/apply.log`, `org-sweep/fixup.log`, `org-sweep/final-hashes.tsv`

## Totals

- **88 repos committed** / 344 files changed / 0 commit failures
- **~1,700 replacements** (dry-run count: 1,718 across 360 candidate files)
- **Nothing pushed.** No `git push` was run anywhere.
- Commit message everywhere: `docs: org-wide link repair — repo renames + master→main (scout phase 2)`

## Important scope corrections vs. the scout report (verified via `git ls-remote`)

1. **master→main was almost entirely a false alarm.** The 359 `blob/master` links target only 6 repos. Remote defaults checked live:
   - `AI-Writings` (229 links): remote HEAD **is** master → links valid, left alone.
   - `plainsong` (104), `signal-chain` (8), `plato-fflearning` (1): remote default is master and **no `main` branch exists** → rewriting would have *created* ~113 dead links. Left alone.
   - `forgemaster` (16): both branches exist; repo is deprecated → dead-annotated instead of branch-fixed.
   - `plato-training` (1, in study-flux-lucid): default is main → **rewritten** (the only actual master→main edit).
2. **`openconstruct-` narrowed to `openconstruct-kernel` only.** There are many live sibling repos (`openconstruct-abi`, `-rust`, `-docs`, `-hub`, `-c`, `-go` …); a blanket `openconstruct-` rewrite would have been catastrophic. Only `openconstruct-kernel → OpenConstruct` was applied.
3. **All 5 "dead" repos still exist on GitHub** (ls-remote succeeds for the-living-minds, wesley-journal, forgemaster, compaction-teacher, flow-state). Links were annotated `(dead)` per instructions — the annotation reflects org deprecation status, not 404s.
4. **Protected from renaming** (false-positive classes found in dry run): `fleet-wiki.casey-digennaro.workers.dev` live deployment domain (58×), local clone paths `/home/eileen/projects/<oldname>` (19×), filename refs `mud-arena.cu`/`mud-arena.md`, hyphen compounds (`lau-tensor-midi` 106×, `flux-tensor-midi` 69×, `tensor-midi-core`, `zeroclaw-arena`, `zeroclaw-plato`, `study-luciddreamer-vision`, `officers-quarters-smp`, `forgemaster-shell` + 4 other live `forgemaster-*` repos, `EXOCORTEX-INSPIRATIONS-*` paths).

## Rules applied (tracked `*.md` only; excluding node_modules/.git/target/dist/build/vendor)

- Renames (strict boundaries): hermes-perception→hermes-avatar (179), officers-quarters→elephant (135), openconstruct-kernel→OpenConstruct (74), lucineer-brain→lucineer-system (98), ternary-tenforward→confidence-cascade (103), log-tensor→murmur (102), tensor-midi→fleet-jepa-midi (285), mud-arena→mud-engine (210), luciddreamer-vision→lucid-dreamer (66), fleet-wiki→lucineer-fleet-wiki (112)
- URL-scoped: `github.com/SuperInstance/EXOCORTEX`→exocortex-core (4), `/zeroclaw`→zeroclaw-dissertation (60)
- Dead-repo links annotated ` (dead)`: the-living-minds, wesley-journal, forgemaster, compaction-teacher, flow-state — annotate-over-delete per instructions. Final state: **250/250 inline dead links annotated, 0 misplaced**.

## Bug found and fixed during the run

First apply pass misplaced 22 `(dead)` annotations: GNU sed is POSIX **leftmost-longest**, and the annotate rule's `[^)]*` tail spanned multiple links on one line, parking the annotation after the *last* link (sometimes a live repo). Fix: paren-bounded `[^()]` groups; `fixup-annotate.sh` stripped all annotations (verified zero pre-existing `) (dead)` in every parent commit), re-annotated correctly, and **amended the 14 affected commits**. Rules verified idempotent.

## Skipped

| Repo | Why |
|------|-----|
| ai-writings | Per instructions (live repo, fleet writes constantly). Still 1,462 commits ahead of origin — uninvestigated, flagged in scout report. |
| researchlocal-backup | Backup/snapshot repo — editing it would falsify the backup (judgment call). Contains openconstruct-kernel + master refs. |
| researchlocal | Not a git repo → cannot commit. ~25 files with master refs left untouched. |
| quilt-rust | Matches were in `target/` build artifacts only — excluded by dir filter, no changes. |

## Anomalies / notes

- Untracked files were never touched (scope = git-tracked), e.g. `luciddreamer-ai/public/compass-head/profiles/**` still contains old names.
- Pre-existing uncommitted work left alone: `si-readme/plato-portal/README.md`, `elephant/SLOPE-REGRESSION-2026-08-20.md` (a fleet agent was mid-write), `fleet-radio/episodes/2026-08-19.html`. None of these were in our commits.
- Residual old-name occurrences after the sweep are all intentional: ai-writings (skipped), researchlocal-backup (skipped), protected local paths/filenames/domains, hyphen compounds, untracked files.
- Display text of renamed links was left as-is (e.g. `[EXOCORTEX](.../exocortex-core)`); only the targets were repaired.

## Commits (repo → short hash, post-amend)

| Repo | Hash |
|------|------|
| ACE-Step-1.5 | 1d9b22c |
| EXOCORTEX | ae40f14 |
| INTEGRATION_GUIDES | ca29e31 |
| SuperInstance-papers | 93aafa9 |
| base60-lattice | 1ff5842 |
| cns-bridge | 02ab195 |
| cocapn-dashboard | e9dd884 |
| collective-unconscious | 2065a2d |
| compaction-teacher | 0a36361 |
| confidence-cascade | cdc6973 |
| covers | 0b5a13c |
| dual-band-guard | e088e64 |
| elephant | ba67482 |
| emergence-engine | 59f2d9f |
| fleet-connections | 0668cbb |
| fleet-dashboard | f165653 |
| fleet-envelope | 2b15415 |
| fleet-inventory | 6dcb3e8 |
| fleet-jepa-midi | 6852750 |
| fleet-memory | 1b68f68 |
| fleet-radio | 3230239 |
| fleet-wiki | 36c80b3 |
| forgemaster | e3f1a12 |
| gossip-ping | 754226e |
| hermes-cloudflare | e8e238d |
| hermes-nmi | fa7d3d2 |
| hermes-perception | 3210b4b |
| hermes-reader | 05e983f |
| luciddreamer-ai | a7f126a |
| luciddreamer-prototype | 1fb10bc |
| luciddreamer-research | 54dea6c |
| lucineer-brain | 141eefb |
| lucineer-creative | e67c178 |
| lucineer-memory | b608500 |
| lucineer-roblox | 0703643 |
| lucineer-system | 9fc441c |
| lucineer-vector | ff5d102 |
| lucineer-worker | 3f26dde |
| mud-arena | 9c3bf5f |
| mud-engine | 9ec0ca6 |
| mud2scummvm | ffde672 |
| officers-quarters | aa1144f |
| plainsong | 1105f13 |
| plato-portal | 79ac73d |
| plato-vision-jepa | 4b8f790 |
| platonic-creative-suite | 35156c0 |
| platos-shell | 0828566 |
| platos-shell-ide | 076688b |
| roblox-beatclock | 37cdeac |
| roblox-bond-system | e2b9ca9 |
| roblox-filtergate | c370bc2 |
| room-render | e64633b |
| screen-agent | 2858338 |
| scummvm-arcade | 63b83ba |
| scummvm-gui-design | 50788da |
| scummvm-prototype | f7298fa |
| si-main | 5dd3d27 |
| si-readme | 33f3363 |
| silence-map | e500f96 |
| spatial-registry | 346dd32 |
| stigmergy | dedbb8c |
| study-constraint-papers | 0a4c390 |
| study-fleet-yaw | b412202 |
| study-flux-lucid | 0122ebd |
| study-luciddreamer-vision | 225c77b |
| study-oracle1 | 4e341e1 |
| study-si-papers | 47799c2 |
| study-spreader-tool | 24b1111 |
| study-superz | d517b76 |
| superinstance-profile | b5ff526 |
| tap-frontend | 14bc3ff |
| tapscript-studio | 21cf3bb |
| technician | a852131 |
| tensor-midi | 3faadce |
| ternary-tenforward | 35a0b80 |
| terrain | 3404433 |
| the-living-minds | 5a46d9a |
| the-tap | 7a3703f |
| vessel-agent-system | 9fdecdb |
| vessel-room-navigator | 37d93aa |
| vibe-protocol | 4a7edc2 |
| voxel-logic | 670acfe |
| wesley-curriculum | 97a5ee8 |
| wesley-holodeck | 5936951 |
| wesley-journal | f0baf34 |
| wesleys-imagination | a527e97 |
| zeroclaw | 21bc2c7 |
| zeroclaw-dissertation | d686a63 |
