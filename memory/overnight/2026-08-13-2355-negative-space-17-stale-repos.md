# Negative Space: 17 Study Repos Gone Stale

**Date:** 2026-08-13 23:55 AKDT
**Finding:** 17 repositories in the fleet haven't had a commit since before August 2026.

## The Stale Repos

| Repo | Last Commit | Days Silent |
|------|-------------|-------------|
| study-claude-code | 2026-06-08 | 66 days |
| study-cudaclaw-bridge | 2026-06-09 | 65 days |
| study-oxide-flux-runtime | 2026-06-09 | 65 days |
| study-vessel-template | 2026-05-16 | 89 days |
| study-flux-papers | 2026-05-08 | 97 days |
| study-cocapn-health | 2026-07-12 | 32 days |
| study-lucid-tutor | 2026-07-12 | 32 days |
| study-lucid-tutor-c | 2026-07-12 | 32 days |
| study-luciddreamer-ai-pages | 2026-07-12 | 32 days |
| study-luciddreamer-vision | 2026-07-12 | 32 days |
| study-multi-model-adversarial-testing | 2026-07-12 | 32 days |
| study-murmur-protocol-v2 | 2026-07-12 | 32 days |
| study-nebula-docs | 2026-07-12 | 32 days |
| study-si-bench | 2026-07-12 | 32 days |
| study-vessel-constellation | 2026-07-12 | 32 days |
| study-vessel-tech | 2026-07-12 | 32 days |
| study-zeroclaw-arena | 2026-07-12 | 32 days |

## Analysis

**Two waves of stagnation:**
1. **May-June cohort (5 repos)** — these are from the early fleet build-out. Vessel templates, flux runtime, Claude Code studies. The ship outgrew them.
2. **July 12 cohort (12 repos)** — mass stagnation on a single date. This suggests a pivot happened around July 12 where these study repos were abandoned en masse for production work.

**Plus 2 empty repos:** study-intent-directed-compilation and study-lucid-tutor-c both have empty src/ directories. Ideas that never shipped.

**Plus 1 missing README:** fleet-embed has code but no README. A repo that doesn't explain itself.

## The Pattern

The fleet creates study repos like a fishing boat sets pots — mark a location, drop a line, move on. Some pots are pulled full. Some are never pulled at all. The 17 stale repos are the pots still in the water from earlier fishing grounds.

## Recommendation

1. **Archive the May-June cohort** — they're from a different era of the fleet
2. **Assess the July 12 cohort** — some may have been superseded by production repos (e.g., study-vessel-template → vessel-agent-system)
3. **Fill or delete the empty repos** — they're ghost rooms
4. **Write README for fleet-embed** — it does work but doesn't explain itself

The fleet's negative space is the history of what it tried and stopped trying. That's not failure — it's the track in the water. But 17 silent repos is a lot of ballast.
