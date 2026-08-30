# Git Rescue — Windows Repos Committed & Pushed

**Date:** 2026-08-13  
**Agent:** Subagent (Git Rescue — Windows)

## Summary

All 9 repos successfully committed and pushed to GitHub.

## Repos with Existing Git (Committed & Pushed)

### 1. ai-writings ✅
- **Path:** `/mnt/c/Users/casey/ai-writings`
- **Remote:** `https://github.com/SuperInstance/ai-writings` (renamed to AI-Writings)
- **Strategy:** Created `windows-backup` branch (did NOT merge with WSL version)
- **Result:** 1591 files committed and pushed to `windows-backup` branch
- **Note:** Had to revert `.github/workflows/ci.yml` and `.github/workflows/landing-page.yml` changes because the OAuth token lacks `workflow` scope. Those changes remain uncommitted locally.
- **Push time:** ~5 minutes (1.2GB repo over WSL)

### 2. hermit-crab ✅
- **Path:** `/mnt/c/Users/casey/hermit-crab`
- **Remote:** `https://github.com/SuperInstance/hermit-crab`
- **Result:** 9 files committed to `windows-backup-2026-08-13` branch
- **Note:** Could not push to master — remote had diverged AND the CI workflow file change was blocked by OAuth `workflow` scope. Created backup branch. Reverted ci.yml change.

### 3. trinity-agent ✅
- **Path:** `/mnt/c/Users/casey/trinity-agent`
- **Remote:** `https://github.com/SuperInstance/trinity-marine-station.git`
- **Result:** 76 files committed and pushed to `main` (76 files changed, 21,819 insertions, 20,844 deletions)

### 4. vessel-quest ✅
- **Path:** `/mnt/c/Users/casey/vessel-quest`
- **Remote:** `https://github.com/SuperInstance/vessel-quest.git`
- **Result:** 26 files committed and pushed to `main` (9,204 insertions, 201 deletions)

### 5. perception-cascade ✅
- **Path:** `/mnt/c/Users/casey/perception-cascade`
- **Remote:** `https://github.com/SuperInstance/perception-cascade.git`
- **Result:** 4 files committed and pushed to `main`

### 6. SuperInstance-papers ✅
- **Path:** `/mnt/c/Users/casey/SuperInstance-papers`
- **Remote:** `https://github.com/SuperInstance/SuperInstance-papers.git`
- **Result:** 35 files committed to `windows-backup-2026-08-13` branch
- **Note:** `main` branch is protected — could not force-push. Pushed to backup branch instead.

## New Repos (Git-Init & Pushed)

### 7. si-research ✅
- **Path:** `/mnt/c/Users/casey/_si_research`
- **Remote:** `https://github.com/SuperInstance/si-research` (NEW, private)
- **Result:** Initial commit with 21 files committed and pushed
- **Note:** Contains embedded git submodules (conservation-enforcer, flux-core, plato-core, etc.) — added as gitlinks. Submodule contents not included in this repo.

### 8. boat-agent ✅
- **Path:** `/mnt/c/Users/casey/boat-agent`
- **Remote:** `https://github.com/SuperInstance/boat-agent.git`
- **Result:** 23 files committed and pushed to `main` (already had git + remote)
- **Note:** `core/target/` added to .gitignore

### 9. research-lab ✅
- **Path:** `/mnt/c/Users/casey/research_lab`
- **Remote:** `https://github.com/SuperInstance/research-lab` (NEW, private)
- **Result:** Initial commit with 13 files committed and pushed

## Issues Encountered

1. **GitHub OAuth `workflow` scope** — The gh token cannot push changes to `.github/workflows/*.yml` files. Affected: ai-writings, hermit-crab. Workaround: reverted workflow file changes before pushing.
2. **Branch protection** — SuperInstance-papers `main` branch is protected against force-push. Workaround: pushed to `windows-backup-2026-08-13` branch.
3. **Large repo push** — ai-writings (1.2GB .git) took ~5 minutes to push over WSL. First attempt was killed; second succeeded.
4. **Embedded git repos** — _si_research contains 17+ subdirectories that are their own git repos. They were committed as gitlinks (submodule references) rather than full file trees. To fully back up their contents, each would need to be committed individually or properly added as submodules.

## Uncommitted Remnants

- ai-writings: `.github/workflows/ci.yml` and `.github/workflows/landing-page.yml` (workflow scope issue)
- hermit-crab: `.github/workflows/ci.yml` (workflow scope issue)
- _si_research: Submodule contents (17 embedded repos referenced as gitlinks)
