# Negative Space: The Fleet Health Audit

**Date:** 2026-08-07, 01:15 AKDT
**Watch:** Overnight Creative Loop
**Finding:** The fleet is bigger than anyone realized, and half of it is undocumented

## The Discovery

145 repositories in `/home/eileen/projects/`. This is not a workspace — it's a **shipyard**. And like any shipyard, some vessels are seaworthy and some are still in dry dock.

### The Numbers

| Metric | Count | % |
|--------|-------|---|
| Total repos | 145 | 100% |
| Have tests | 95 | 65.5% |
| **NO tests** | **50** | **34.5%** |
| Have LICENSE | 126 | 86.9% |
| **NO LICENSE** | **19** | **13.1%** |
| Have README | 140 | 96.6% |
| **NO README** | **5** | **3.4%** |
| Have CONTRIBUTING | 38 | 26.2% |
| **NO CONTRIBUTING** | **107** | **73.8%** |

### The Pattern

The fleet splits into three tiers:

**Tier 1: Battle-Ready (38 repos)** — Tests, README, LICENSE, CONTRIBUTING. These are the ships that can sail without the captain. They're the ones the overnight crew has been improving: forgemaster, exocortex-core, fleet-dashboard, songforge, batten-spline, cns-bridge. These are done — or at least, they're as done as software gets.

**Tier 2: Seaworthy but Undersigned (57 repos)** — Tests + README + LICENSE, but no CONTRIBUTING. These work, but nobody has written down *how to contribute*. The hull is sound; the gangplank is missing. This is where the overnight crew has been operating — adding CONTRIBUTING.md one repo at a time.

**Tier 3: Dry Dock (50 repos)** — No tests. These are the study repos, the research repos, the "I had an idea at 2 AM" repos. They're not broken — they're *unstarted*. The `study-*` prefix dominates this tier. These are thinking materials, not shipping materials.

### The Real Finding

The overnight crew has been adding LICENSE files and CONTRIBUTING.md to individual repos. That's good work. But the fleet has **107 repos without CONTRIBUTING.md** and **50 without any tests**. At the current rate (adding 1-3 per overnight session), it would take **36-54 nights** to cover the fleet.

This is not a problem. This is a **pipeline**.

The study repos don't need tests — they're research notebooks, not production code. But the production repos (slackwater-*, lucineer-*, roblox-*, cns-*) that lack CONTRIBUTING.md are the gap. These are the repos where a new contributor (or a new AI agent) would land and not know what to do.

### The Missing READMEs

Five repos have no README at all:

1. `INTEGRATION_GUIDES/` — presumably integration documentation (ironic)
2. `covers/` — likely creative content (cover art?)
3. `fleet-pipeline/` — a CI/CD pipeline with no documentation
4. `fleet-tts/` — text-to-speech component with no documentation
5. `researchlocal/` — unclear, no git history

`fleet-pipeline` and `fleet-tts` are the concerning ones. These are production infrastructure components. A pipeline without a README is a pipeline that only the person who built it can operate.

### The Recommendation

1. **fleet-pipeline and fleet-tts need READMEs** — tonight, if possible
2. **Production repos missing LICENSE** (compaction-teacher, fishinglog-ai-site, luciddreamer-content, lingbot-map, ai-writings-vectorizer) — add MIT LICENSE
3. **slackwater-* repos missing LICENSE and CONTRIBUTING** — these are core game components. They need full documentation.
4. **Study repos** — leave them alone. They're thinking tools, not shipping products.
5. **A CONTRIBUTING template** — create a standard CONTRIBUTING.md template that can be dropped into any repo with minimal modification.

### The Meta-Finding

The fleet has grown to 145 repos. That's more than any single human can track in their head. The overnight crew exists *because* the fleet reached a size where human attention became the bottleneck. The crew is not just improving code — it's **maintaining the fleet's institutional memory** while the captain sleeps.

The negative space is the fleet's technical debt made visible. 107 repos without CONTRIBUTING.md is 107 places where knowledge lives in one person's head. The overnight crew's job is to move that knowledge into files.

---

*145 repos. 50 without tests. 19 without licenses. 107 without contributing guides. The fleet is a shipyard, and the shipyard never sleeps. The negative space is not a gap — it's a map of where the work goes next.*

— Lucineer, Negative Space Audit, 01:15 AKDT, Aug 7 2026
