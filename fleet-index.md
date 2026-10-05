# Fleet Index — /home/eileen/projects/

**Sweep date:** 2026-10-05
**Total directories:** 208
**Git repos:** 171 (134 CLEAN, 25 NOW-PUSHED, 10 NOW-STALE-FIXED, 1 CORRUPT, 1 EMPTY)
**Non-git directories:** 37

---

## CLEAN (134) — Already committed & pushed
These repos are in sync with origin. No action needed.

---

## NOW-PUSHED (25) — Fixed on 2026-10-05
All local work is now on GitHub. Verified via ls-remote.

| Repo | Branch | Commit | Remote URL |
|------|--------|--------|------------|
| Scrapcraft | main | 60a2580 | github.com:SuperInstance/Scrapcraft.git |
| cargo-line-tycoon | main | 2900a40 | github.com:SuperInstance/cargo-line-tycoon.git |
| chiaroscuro | reland8 | a93e192 | github.com:SuperInstance/chiaroscuro.git |
| crab-traps | main | ff0c30e | github.com:SuperInstance/crab-traps.git |
| fleet-seeds | main | fb58d37 | github.com:SuperInstance/fleet-seeds.git |
| fleet-triage | main | 88e30b3 | github.com:SuperInstance/fleet-triage.git |
| jev-quilt | main | 30e431b | github.com:SuperInstance/jev-quilt.git |
| lucineer-relay | main | b45d934 | github.com:SuperInstance/lucineer-relay.git |
| qthe | main | ee00b99 | github.com:SuperInstance/qthe.git |
| pie-minimax | a1-closure-receipt | 7d662e3 | github.com:SuperInstance/pie-minimax.git |
| quilt-esp32 | main | b58e23c | github.com:SuperInstance/quilt-esp32.git |
| quilt-jepa | main | c5712f1 | github.com:SuperInstance/quilt-jepa |
| quilt-mhs | main | c0c0042 | github.com:SuperInstance/quilt-mhs |
| quilt-research-canons | main | 29be5f9 | github.com:SuperInstance/quilt-research-canons |
| quilt-rust | main | 60951dd | github.com:SuperInstance/quilt-rust |
| quilt-tournament | master | 9aa4fd3 | github.com:SuperInstance/quilt-tournament |
| saddle | main | 641238a | github.com:SuperInstance/saddle |
| si-papers-new | main | c22da46 | github.com:SuperInstance/si-papers-new |
| sunset-ecosystem | main | f188a33 | github.com:SuperInstance/sunset-ecosystem |
| superinstance | main | ca35df2 | github.com:SuperInstance/superinstance |
| superinstance-website | main | 62f0405 | github.com:SuperInstance/superinstance-website |
| tapscript-studio | main | 0f9edf8 | github.com:SuperInstance/tapscript-studio |
| tapscript-worker | main | a43a849 | github.com:SuperInstance/tapscript-worker |
| the-tap | main | 78fdaeb | github.com:SuperInstance/the-tap |
| webgpu-profiler | main | f9c5275 | github.com:SuperInstance/webgpu-profiler |

---

## NOW-STALE-FIXED (10) — Committed & pushed on 2026-10-05
All uncommitted files now committed and pushed.

| Repo | Branch | Notes |
|------|--------|-------|
| ai-writings | main | short-stories files, pycache, replay reports |
| quilt-canvas-tui | main | forget() fix + pycache |
| selectlib | main | table() fix + pycache |
| quilt-gpu-lab | main | qm_example probes |
| selectlib-readonly | main | GPU experiment brief + pycache |
| pie-minimax-readonly | main | GPU experiment brief (already on remote, just pycache push) |
| pr-wave-micromoth | view-receipt-cells | .resolve-pr.sh.archived |
| quilt-arcade | main | judge result refresh |
| quilt-quant | main | package-lock.json |
| zeroclaw | main | m4 tax decomposition |

---

## CORRUPT (1) — Needs repair
| Repo | Issue |
|------|-------|
| A2A-native-notebookLM | Empty object file `.git/objects/04/209e28816e5f64301a62d55166f4602c0c6ff7`, HEAD bad object |

---

## EMPTY (1) — Zero commits
| Repo | Issue |
|------|-------|
| quilt-dpcpp | git init only, no commits, no remote |

---

## PARKED / ARCHIVED
| Item | Status |
|------|--------|
| ZeroClaw dissertation agent | PARKED 2026-10-05 — agent dir moved to `_archive/zeroclaw-20261005`, repo retained at SuperInstance/zeroclaw-dissertation |

---

## Cleanup notes
- All 35 repos (25 NOT-PUSHED + 10 STALE) are now safely on GitHub
- Local copies can be archived/deleted after Casey confirms
- Archive-by-rename: `<name>.archived-YYYYMMDD`
- Corrupt repo (A2A-native-notebookLM) may need re-clone to repair
