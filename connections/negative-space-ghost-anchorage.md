# Negative Space: The Ghost Anchorage

**Date:** 2026-08-09 03:10 UTC
**Discovery:** `/home/eileen/projects/researchlocal/`

## What's There

A 224MB directory sitting in `~/projects/` alongside the tracked fleet repos. Not a git repository. Not tracked. Not mentioned in any fleet document. Not connected to any pipeline, CI, or agent workflow.

Contents include:
- `masklock.tar` — 229MB. Untarred, unexamined.
- `AI_AGENT_RPG_COMPLETE_PACKAGE.zip` — 96KB.
- `ai_society_portal.zip` — 54KB.
- `SuperInstance-main/` — an earlier version of the project, before it was fleet-ified.
- `activelog-backend/`, `activelog-claude/`, `activelog2/` — three generations of the same project, each abandoned mid-build.
- `consolidated-documents/` — 10 subdirectories.
- `dialogues/` — something.
- `superinstance_novellas_complete/` — novellas.
- `tools/` — unspecified.
- `1021dmlog/` — a log from October 21st. Of what?
- Multiple `.Zone.Identifier` files — Windows metadata marking downloaded files. The ship's barnacles.

## What It Means

This is the drydock. Before the fleet, before the repos had READMEs and CI workflows and test suites, there was this — a single directory where everything accumulated. Tarballs of old ideas. Zip files of projects that became repos or didn't. Multiple generations of `activelog` stacked like geological strata.

Every fleet has a junk drawer. This is ours.

The interesting thing is not what's in it — it's that nobody talks about it. The overnight loops have run dozens of times. They've tested 30+ repos, written hundreds of creative pieces, filed negative space reports about missing tests and broken CI. Nobody has mentioned `researchlocal/` because it's not a repo. It doesn't have a `.git` directory. It's invisible to every tool that looks for repos by finding `.git` folders.

The fleet's sensors can't see it. It exists in the space between the repos.

## What Should Happen

Not deletion. This is history. But it should be acknowledged:

1. **Audit:** What's actually in those tarballs and zips? Is there code worth recovering?
2. **Archive:** Move to `~/archives/pre-fleet/` so it's clearly separated from active projects.
3. **Document:** Add to fleet wiki as "historical context" — the drydock where the fleet was built.
4. **Clean:** Remove the Zone.Identifier files. They're Windows metadata barnacles.

But not tonight. Tonight it stays where it is — a ghost anchorage next to the working fleet. The ships that became the fleet sailed out of this harbor. The harbor remains.
