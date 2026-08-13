# Negative Space: 21 Stale Branches in A2A-native-notebookLM

**Date:** 2026-08-12 22:10 AKDT

## The Finding

A2A-native-notebookLM has 21 remote feature branches, all last committed on 2026-06-02 (over 70 days ago). These branches represent an integration sprint that was either completed or abandoned:

- agent-swarm-integration
- agent-to-agent-communication
- ai-pasture-integration
- claw-engine-integration
- content-transformations
- cortex-manifest
- deepinfra-refactor
- fleet-discovery
- i2i-vessel-integration
- langgraph-abstraction
- living-spreadsheet
- meta-integration
- meta-learning (2026-06-07)
- openmind-integration
- plato-computer-integration
- podcast-generation
- research-assistant
- surrealdb-vectorization
- ternary-coalescing
- ternary-computation
- feature/a2a-exocortex (2026-06-06)

## The Question

Were these features merged into main, or abandoned? If merged, the branches should be deleted (git hygiene). If abandoned, the work should be evaluated for salvage.

## Impact

21 stale branches creates noise in the repo. `git branch -a` becomes unreadable. PRs against these branches are invisible. The repo looks like it has 21 active workstreams when it actually has zero.

## Also: study-pincher has 15 branches

Similar pattern — study-pincher has 15 branches, suggesting another abandoned sprint.

## Recommendation

Casey should review these branches and decide:
1. **Merged?** → delete the branch
2. **Abandoned but useful?** → cherry-pick or rebase
3. **Dead?** → delete and move on

This is a 10-minute cleanup that would significantly reduce fleet noise.
