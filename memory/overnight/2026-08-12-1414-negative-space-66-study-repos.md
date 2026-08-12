# Negative Space: 66 Study Repos and the Ghost Library

**Date:** 2026-08-12 14:14 AKDT
**Finding:** The fleet contains 66 `study-*` repositories — a third of the entire fleet — that form a shadow library of research clones, most of which haven't been touched in months.

## The Numbers

- **218 total repos** in `/home/eileen/projects/`
- **66 are study-\*** repos (30% of the fleet)
- **25 of those** were last touched in July 2026 — and only to add MIT licenses
- **3 haven't been touched since May 2026** (study-flux-papers, study-vessel-template, study-air)
- **study-vessel-monitor** is the deepest: 5,329 commits. It's a clone of WorldMonitor, an external real-time global intelligence dashboard.

## The Pattern

The study repos fall into categories:

### External Research Clones
Projects the captain was studying — ecosystems to learn from:
- study-vessel-monitor (WorldMonitor — 5,329 commits)
- study-cudaclaw / study-cudaclaw-main / study-cudaclaw-bridge
- study-luciddreamer-* (agent, ai-pages, vision)
- study-oxide-flux-runtime / study-oxide-pipeline

### Fleet Archaeology
Old versions of fleet projects, preserved for reference:
- study-flagship (old Lucineer flagship — 1,818 commits)
- study-pincher (79 commits)
- study-lever-runner (72 commits)
- study-superz (126 commits)

### Theory/Math
Pure research, no code to test:
- study-negative-knowledge
- study-sheaf-constraint-synthesis
- study-constraint-papers
- study-zero-crypto

## The Real Problem

These repos aren't hurting anything. But they're distorting our fleet statistics:

1. **Test coverage metrics** — We keep finding "repos without tests" that are just research clones. 25 of the 66 study repos have no tests because they're either pure docs or archived code.
2. **Scanner noise** — Every negative space scan flags them, creating false urgency.
3. **Commit history skew** — When we say "183 repos were active in August," some of those are study repos that got a one-line README from an overnight loop, not real development.

## What's Actually Interesting

The study repos represent **months of research that compiled into the current fleet**. study-flagship → lucineer-system. study-cudaclaw → various Rust tools. study-luciddreamer-* → the dreaming GPU concept.

They're the **exoskeletons of previous ideas**. The hermit crab moved out. The shells remain.

## Recommendation

1. **Stop scanning study-* repos for fleet health metrics.** They're archives, not active code.
2. **Consider a `study/` subdirectory** instead of polluting the top-level namespace.
3. **Or tag them** with a `.study` marker file so fleet tools can skip them.

The hermit crab doesn't carry its old shells on its back. It leaves them on the ocean floor for other crabs to find. Maybe the fleet should too.
