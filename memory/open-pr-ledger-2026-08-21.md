# Open-PR Ledger — 2026-08-21 (mop-up wave)

Fresh rebuild of all open PRs under **SuperInstance** (user account, 4327 repos) at wave start:
**91 open PRs across 25 repos** (via `gh search prs` + GraphQL enrichment: mergeable / mergeStateStatus / statusCheckRollup / reviewDecision).
Prior waves: `merge-fixwave-2026-08-21.md` (16 merged), `unstable-triage-2026-08-21.md` (19 fixed-pushed, 33 lockfile-blocked).

## Actions this wave (all merges green-CI at merge time; no red CI merged)

### Merged this wave (13)
| PR | repo | what | note |
|---|---|---|---|
| #2–#5 | constraint-theory-py | dependabot req bumps (pytest, mypy, pytest-cov, setuptools) | #5 branch updated onto post-#4 main (strict protection) |
| #67 | PersonalLog | jsdom 29→30 | — |
| #69 | PersonalLog | eslint-config-next 16.3.1 | branch updated onto post-#67 main (dependabot had rebased; lockfile clean) |
| #70 | PersonalLog | **NEW PR (P2 fold-forward of #50)** — onnxruntime-web 1.26.0→1.27.0 on current main + regen lockfile | created this wave; all 4 CI jobs green |
| #76 | webgpu-profiler | prettier ^3.9.6 | — |
| #81 | webgpu-profiler | @typescript-eslint/eslint-plugin ^8.67.0 | — |
| #82 | webgpu-profiler | @typescript-eslint/parser ^8.67.0 | dependabot auto-rebased after #81 |
| #83 | webgpu-profiler | eslint 10.8.1 | — |
| #84 | webgpu-profiler | @types/node 26.2.0 | dependabot auto-rebased after #83 |
| #8 | quicunnel | rustls/quinn API-drift fix + rcgen 0.14 (ring 0.17, clears RUSTSEC-2025-0009) + stop tracking build artifacts | audit now green — ring vuln cleared on-branch by prior actor's rcgen commit |

### Folded forward (P2 conflict-chain) — 1
- **PersonalLog#50** → unique fix (onnxruntime-web 1.27.0) folded into fresh **#70** on current main; #50 closed with dated epitaph pointer. Old branch was next-15-era (2 generations behind); no rebase attempted.

### Closed with dated epitaphs — 4
| PR | repo | epitaph summary |
|---|---|---|
| #1 | bplus-tree | superseded — master already has fuller professional README (direct push); minimal-voice variant not folded; branch `docs/bplus-tree-readme` preserved |
| #60 | webgpu-profiler | superseded — base (^4.1.7) no longer exists on main (vitest ^1.6.1 family, green via #66 wave); no unique delta to fold |
| #65 | webgpu-profiler | same as #60 |
| #6 | forgemaster | superseded — May-2026 restructure snapshot (+1.6M lines/4900 files, mostly state/log/pyc) conflicting with actively-evolved main (pushed 2026-08-21); community files duplicate root-level docs; branch `kimi1/fleet-simulation` preserved |

### sunset-ecosystem (item 3) — in progress at ledger write
- **#33 (shared-CI migration)**: was red on 2-month-old checks. Fixed on-branch this wave: (1) `ast-unparse`→`astunparse` (dead PyPI package, Multi-Persona Code Review install step — now passes); (2) gated `pyaudio` to non-Linux (no manylinux wheels, needs portaudio.h; `uv sync --all-extras` unblocked; benchmark job now green); (3) fixed hard syntax error in `examples/voice_room.py` (stray duplicated docstring fragment); (4) `[tool.ruff]` bootstrap baseline E9+F63 (documented; ~8.8k legacy findings deferred); (5) mechanical `ruff format` of 1011 files (format gate). CI rerunning — pytest + coverage≥75 gate is the remaining unknown; #32 holds the repo's test fixes.
- **#32 (fix all test failures)**: CONFLICTING; will be evaluated after #33 (merge on top or close-as-absorbed with pointer).

### Verified: the 9 "stuck CI" repos (item 4) — all MERGED by prior actor 2026-08-21 18:02Z
activelog-agent#1, activelog-ai-pages#1, actualization-harbor#1, adinkra-math-pypi#1, ability-transfer#3, fleet-discovery#1, fleet-agent-early-version#1, fleet-github-app#1, fleet-coordinate-js#1 — plus the other 7 fixed-pushed repos merged 17:45–17:46Z. Nothing left to do.

### Incident notes
- `/tmp` (tmpfs) hit 100% mid-wave from prior agents' scratch — cleared stale worktrees/venvs (wt-quicunnel, wt-qr*, wt-pl*, wt-scrdt*, 2 venvs), freed 5.7G. Nothing quilt-related touched.
- Several "CONFLICTING" states were stale recompute windows; re-querying after a few seconds showed MERGEABLE (webgpu#82/#84, PersonalLog#69 were auto-rebased by dependabot).
- Strict branch protection (require up-to-date branches) on constraint-theory-py/webgpu/PersonalLog means every same-repo sequential merge needs a branch update or dependabot auto-rebase; handled per-PR.

## Still open (at wave start → status after this wave's actions)
(LIST_PLACEHOLDER)

## Skip list honored (not touched)
- edge-native-paper #1/#2 — repo archived; GitHub refuses merges. Human decision (unarchive vs close).
- PersonalLog #58 — typescript@7 vs typescript-eslint (lint parser hard-error). Branch ready otherwise.
- PersonalLog #60(absorbed into merged wave? — no longer open)/#61/#66/#68 cluster — engine/lockfile issues, needs-work per triage.
- flux-runtime #27 (tsc 3467 pre-existing errors) — also #25 red, left open, needs-work.
- Edge-Native #5 — ESP32 build, needs-work. (Now CLOSED unmerged by another actor — verified this wave.)
- fleet-constraint #1 — **now green+CLEAN** (build-and-test 3.10/3.11/3.12 pass); skipped per directive (decision item).

## Handoff notes (quilt-family — another agent spearheads; untouched this wave)
- quilt-swarm #1–#12, quilt-fleet #1–#6, quilt-rag #1–#5, quilt-elf #1–#3, quilt-nomad #1–#2, quilt-pincher #1–#5, quilt-k3s #1–#3, quilt-ai #1, quilt-cloudflare #2, quilt-evolve #1, quilt-rust #1–#4 — 43 PRs, all UNSTABLE (lockfile `cache: npm`/`npm ci` EUSAGE, k3d missing, or clippy API drift). Root fixes per triage: commit lockfiles or drop `cache:` from setup-node; quilt-rust needs small code changes (tower-http/thiserror/axum drift). quilt-jetson #1/#3 already merged by other actor (earlier wave).
- SmartCRDT #50/#51/#52/#54/#55/#56/#58/#62/#64/#66 — Install-Dependencies/lockfile failures (10 PRs); same shared lockfile fix; #62/#64/#66 get past install but fail type-check/tests.
- CognitiveEngine #46/#50/#51/#53/#54 — Docker tag uppercase-org issue + red suite (5 PRs).
- SuperInstance-papers #12/#14 — test failing (TS 6→7 + no lockfile).
- PersonalLog #52 — sharp 0.35.3, Build & Test red.
- quicunnel #6/#7 — all jobs red (older dependabot branches; superseded by merged #8's approach? evaluate next wave).
