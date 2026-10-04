# opencode cross-check: backup safety of /home/eileen/projects

- Date: 2026-09-17
- Requested by: Lucineer (fleet foreman), via staff-assistant task
- Mode: strictly read-only. No repos were modified, fetched, pushed, or written to. Only this report file was created.
- Scope: 417 entries in /home/eileen/projects. 15 diverse repos sampled in depth (quilt-*, study-*, slackwater-*, roblox-*, fleet-*, misc incl. one git-worktree). Plus fleet-wide read-only sweeps (git-vs-non-git classification, dirty-state scan, untracked node_modules scan, secret-pattern scan of dirty files).

## Verdict

Overall hygiene of sampled repos is good: all 15 sampled have an `origin` remote on github.com/SuperInstance, 13/15 are fully clean and in sync, and no real secrets were found in any dirty/untracked file. However, the cross-check surfaced real backup-safety risks OUTSIDE the clean core: one repo with no remote at all and fresh uncommitted work, several repos with unpushed local branches (up to 146 commits by merge-base), ~7.4 GB of unversioned data in non-git directories, and a family of worktrees with detached/unsynced heads.

## Sampled repos (15)

| Repo | Remote (origin) | Dirty files | Ahead of upstream | Last commit | Notes |
|---|---|---|---|---|---|
| quilt | github.com/SuperInstance/quilt.git (https) | 0 | n/a — branch `quilt-jupyter-conception` has no upstream; 1 unpushed commit vs origin/main; HEAD on NO origin ref | 2026-08-31 | Unpushed branch |
| quilt-agent | SuperInstance/quilt-agent.git (ssh) | 0 | 0 | 2026-08-20 | Clean |
| quilt-vm-rust | SuperInstance/quilt-vm-rust.git (ssh) | 0 | 0 | 2026-08-26 | Clean |
| study-cocapn | SuperInstance/superinstance-cocapn.git (ssh) | 0 | 0 | 2026-08-26 | Clean; remote name differs from dir name |
| study-fleet-vessel | SuperInstance/fleet-vessel.git (https) | 0 | 0 | 2026-08-07 | Clean; dir/remote name mismatch |
| study-murmur | SuperInstance/Murmur.git (https) | 0 | 0 | 2026-08-12 | Clean; dir/remote name mismatch |
| slackwater-cognition | SuperInstance/slackwater-cognition.git (ssh) | 0 | 0 | 2026-08-12 | Clean |
| slackwater-rust | SuperInstance/slackwater-rust.git (ssh) | 0 | 0 | 2026-08-11 | Clean |
| roblox-testkit | SuperInstance/roblox-testkit.git (https) | 0 | 0 | 2026-08-12 | Clean |
| roblox-craftmind-agents | SuperInstance/roblox-craftmind-agents.git (ssh) | 0 | 0 | 2026-08-12 | Clean |
| fleet-conductor | SuperInstance/fleet-conductor.git (ssh) | 0 | 0 (branch `production-round3-2026-07-10` tracks upstream) | 2026-08-23 | Clean |
| fleet-gateway | SuperInstance/fleet-gateway.git (https) | 0 | 1 | 2026-08-30 | 1 unpushed: `5b2285b evening ritual: checkpoint before poker night 2026-08-30` |
| lucineer-system | SuperInstance/lucineer-system.git (ssh) | 0 | 0 | 2026-09-03 | Clean; freshest of sample |
| Scrapcraft | SuperInstance/Scrapcraft.git (ssh) | 0 | 0 | 2026-08-28 | Clean (dir is capitalized; lowercase `scrapcraft` does not exist) |
| saddle-ft | SuperInstance/saddle.git (ssh) | 0 | n/a — branch `field-trial` no upstream, BUT HEAD commit is contained in origin/main | 2026-08-23 | Git worktree of `saddle`; content already on origin. Safe. |

## Fleet-wide sweeps (read-only, all repos)

### Dirty repos (12 of ~396 git repos have uncommitted state)

| Repo | Dirty entries | Ahead | Last commit | What's dirty |
|---|---|---|---|---|
| quilt-tournament | 30 | **NO REMOTE AT ALL** | 2026-09-04 | Modified/deleted scout notes + ~26 untracked STIR-*.md files |
| rd | 18 | 0 | 2026-08-31 | soak-coverage.log + 17 untracked tap log .md files |
| qv-head | 9 | detached HEAD (contained in origin/master) | 2026-08-30 | Verilog RTL + Verilator build artifacts (obj_scale .gch, untracked obj_dbg/obj_fix/obj_ghost dirs) |
| ai-writings | 9 | 0 | 2026-09-04 | Radio logs, music-catalog JSON, untracked .wav (8.9 MB) + .mp3 (740 KB) |
| quilt-verilog | 5 | **3 unpushed** | 2026-09-04 | Spike logs + untracked counter example/testbench/tool |
| fleet-radio | 4 | 0 | 2026-09-02 | composer-state.json + episode HTML |
| quilt-llvm-wt-r4lane1 | 2 | no upstream; ~10 unpushed vs origin/master; HEAD not on origin | 2026-08-31 | Modified lib.rs + **untracked lowering.rs** |
| experiment-wheel | 2 | 0 | 2026-08-31 | RESULTS.json + bench log |
| qvw-r27 | 1 | **detached HEAD, NOT on any origin ref; 146 commits since merge-base with origin** | 2026-09-04 | Modified cosim/synth_gate_theta.json |
| quilt-rust-selfimprove | 1 | no upstream; **35 unpushed** vs origin/main; HEAD not on origin | 2026-08-31 | Modified corpus.json |
| quilt-rust | 1 | 0 | 2026-08-29 | Untracked experiments/ dir |
| quilt-llvm | 1 | branch `r4-conception`; **11 unpushed** vs origin/master; HEAD not on origin | 2026-08-31 | Untracked docs/phase/R4-LANE1-BRIEF.md |

(Caveat: qvw-r27's "146 since merge-base" may over-count commits that exist on origin under other branches, but its HEAD commit itself is on no origin ref. quilt-llvm and quilt-llvm-wt-r4lane1 unpushed counts likely overlap — same r4 lineage.)

### Secrets scan of dirty/untracked files

Pattern scan (api key / secret / password / token / sk- / AKIA / ghp_ / xox / PRIVATE KEY) across all dirty and untracked files in the 12 dirty repos. All hits were false positives:
- quilt-tournament scout notes: prose use of "consent token", "origin-tagged tokens", "not a secret" (railway-interlocking / split-tally metaphor writing).
- qv-head `.gch` files: compiled Verilator precompiled headers (binary noise).
- ai-writings `.mp3`/`.wav`: binary noise.
**No real credentials found.**

### node_modules / large untracked dirs

No untracked `node_modules` anywhere in the projects tree (all repos' untracked entries were inspected). Largest untracked items found: `ai-writings` audio (9.6 MB) and `qv-head` Verilator build dirs. Non-issue at repo level — but see non-git dirs below.

## Dirs that are NOT git repos (10) — biggest single risk

| Dir | Size | Assessment |
|---|---|---|
| sd-fleet | **4.0 GB** | No version control, no remote. Total backup exposure. |
| researchlocal | **2.9 GB** | Same. (Note: `researchlocal-backup/` sibling IS a git repo, but this dir is not.) |
| readme-art-drafts | **456 MB** | Large, unversioned. |
| zeroclaw-knowledge | 59 MB | Unversioned. |
| music | 33 MB | Unversioned. |
| wesley-holodeck-archived | 1.9 MB | Small, archived — low risk. |
| mist-art-qc | 36 KB | Small. |
| fleet-reactions | 32 KB | Small. |
| fleet-mirror | 8 KB | Small. |
| shoal-opencode.archived-20260824-loses-tournament | 144 KB | Archived (name suggests a lost tournament). |

**Total unversioned: ~7.4 GB**, of which sd-fleet + researchlocal + readme-art-drafts = 99%.

## Worktree quirks

21 dirs are linked worktrees (`.git` is a file), not independent repos: `mist-lab-work`, the entire `quilt-llvm-wt-*` family (14 dirs: cocapn, gacorpus, merkle, mutants, r3lane1, r3lane3, r4lane1, region, rivalry, shape, tombstone, usetables + `quilt-cosim-wt`), `quilt-r27`, `quilt-rust-selfimprove`, `qv-head`, `qvw-r27`, `saddle-ft`, `saddle-v3`.

- Worktrees share object storage with their parent repo — a backup that only copies the parent repo's `.git` will LOSE worktree-local commits and dirty state. Relevant parents observed: `qv-head` + `qvw-r27` are worktrees of `quilt-verilog`; `saddle-ft`/`saddle-v3` of `saddle`; the `*-wt-*` family presumably of `quilt-llvm`.
- `qv-head` and `qvw-r27` are on **detached HEAD** — easy to lose track of; qvw-r27's HEAD is not on origin at all.
- `quilt-rust-selfimprove` worktree has 35 unpushed commits vs origin/main.

## Loose files at projects root (not in any repo)

`EXOCORTEX_DESIGN.md`, `WEBSITE_DEPLOYMENT.md`, `convergence-of-corrections-2026-08-19.md`, `fleet-next-level-plan.md`, `qwen-stream.log`, `qwen-stream.py`, `test-runner.sh`, `wesley-stream.log`, `wesley-stream.py`, `.openclaw-dummy`. Small, but no backup safety.

## Alarming, ranked

1. **quilt-tournament: no git remote, 30 uncommitted entries, last commit 2026-09-04 (freshest work in the dirty set).** One `rm -rf`, disk failure, or bad clean away from losing everything. Nothing of this repo exists off-machine.
2. **qvw-r27: detached HEAD, dirty, HEAD on no origin ref, ~146 commits since merge-base.** Worktree state that a parent-repo backup would not capture as a ref.
3. **quilt-rust-selfimprove: 35 unpushed commits + modified corpus.json.** Worktree of quilt-rust; unpushed local branch `selfimprove-harness`.
4. **quilt-llvm: 11 unpushed on `r4-conception`** (plus 10 on the r4lane1 worktree, likely overlapping) — the whole R4 lane exists only locally.
5. **~7.4 GB unversioned dirs** (sd-fleet 4.0G, researchlocal 2.9G, readme-art-drafts 456M, zeroclaw-knowledge 59M, music 33M).
6. **quilt: 1 unpushed commit** on local branch `quilt-jupyter-conception`; **fleet-gateway: 1 unpushed commit**; **quilt-verilog: 3 unpushed + dirty**.
7. Minor: `qv-head`/`qvw-r27` detached HEADs; `study-*` dirs whose remote names differ from dir names (study-cocapn→superinstance-cocapn, study-fleet-vessel→fleet-vessel, study-murmur→Murmur) — cosmetic, but complicates fleet inventories.

## What looked fine

- No secrets in any dirty file (content scan; all hits prose/binary false positives).
- No untracked node_modules or vendored dependency bloat anywhere.
- 13/15 sampled repos clean, synced, pushed, remote present.
- saddle-ft worktree content already merged to origin/main.
- No bare or broken `.git` dirs found; all worktree links resolve.

## Suggested next steps (for foreman decision — not executed)

1. Add an origin remote to quilt-tournament and push + commit its scout notes today.
2. Push the local branches: quilt `quilt-jupyter-conception`, quilt-llvm `r4-conception`, quilt-rust-selfimprove `selfimprove-harness`, the r4lane1 worktree branch; push fleet-gateway (1) and quilt-verilog (3).
3. Decide: gitify or snapshot sd-fleet / researchlocal / readme-art-drafts (7.3 GB of the 7.4 GB exposure).
4. Re-attach qv-head/qvw-r27 to named branches so their state is referrable and backable.
