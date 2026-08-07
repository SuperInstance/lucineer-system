# Negative Space: 22GB of Untracked Creative Work

**Date:** 2026-08-06 23:30 AKDT
**Found during:** Overnight Creative Loop, Hour 4

## The Finding

Two project directories totaling **22.2 GB** exist in `/home/eileen/projects/` with **zero git commits, zero version control, zero backup**:

### 1. `covers/` — 5.2 GB
Casey's actual song cover work. Contains:
- 8+ cover versions of "One Day In E" (folk rock, ambient, polished, sparse, intimate, band)
- Multiple Demucs separations (standard, heavy, EQ-processed, MDX, MDX Extra, MMI, 6-source, FT)
- Vocal extraction experiments (band filtering, spectral gating, soft masking, subtraction)
- Melody extraction JSON (34KB detailed analysis)
- MIDI exports of extracted melodies
- ACE-Step cover renders
- A recording guide and version catalog
- Multiple virtual environments (venv, venv311)
- **Audio experiments from 10:00-21:00 on Aug 6** — a full day of creative work

This is real creative output. Not code. Not tests. Not writing. Sound. And it has no version control.

### 2. `researchlocal/` — 17 GB
Old research data and project archives:
- `masklock.tar` — 230 MB
- `ai_society_portal.zip` — 54 KB
- `AI_AGENT_RPG_COMPLETE_PACKAGE.zip` — 96 KB
- ActiveLog MVP and technical repo directories
- SuperInstance project archives
- Consolidated documents
- Old .theia-ide configs
- Research_Package_v3

This is archaeological data — the dig site before the current fleet existed. Old projects, old architectures, old dreams.

## Why Nobody Talks About It

These directories aren't code. They're not in any test suite. They're not creative writing. They're not tracked by any agent. They're not in any CI pipeline. They're not mentioned in any AGENTS.md or TOOLS.md.

The creative writing corpus (49,850 pieces) gets all the attention. The test suites (thousands of tests across 145 repos) get all the engineering focus. But the actual **music** — the thing Casey was building all of this to help create — sits in a folder with no history.

## Risk

If the WSL filesystem corrupts (and WSL filesystems do corrupt), 22 GB of irreplaceable creative work is gone. The covers represent a full day of iterative musical exploration. The research archive represents months of earlier work.

## Recommendations

1. **Immediate:** Back up `covers/` to R2 (Cloudflare storage, free tier). The audio files are exactly what R2 is for.
2. **Near-term:** Add `covers/` to the fleet's backup strategy. Even if it doesn't go in git, it should have a mirror.
3. **Consider:** A `.gitignore`-aware git repo for the covers directory to track the non-audio files (JSON analyses, MIDI, lyrics, guides) while storing audio separately.
4. **researchlocal/:** Evaluate whether any of this is still needed. If yes, archive to R2. If no, it's 17 GB that could be freed.
5. **Meta-point:** The system writes 49,850 pieces of creative writing and 696+ tests but doesn't back up the actual creative output (music). The fleet is so focused on building itself that it forgot to protect what it's building FOR.

---

*The hermit crab built 49,857 shells. It forgot to back up the ocean.*
