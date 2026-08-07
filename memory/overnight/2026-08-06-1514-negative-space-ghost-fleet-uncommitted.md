# Negative Space: The Ghost Fleet — Uncommitted, Unpushed, Unreachable

**Found:** 2026-08-06, 15:14 AKDT loop
**Severity:** Structural — five repos with no remote, many with uncommitted work

## The Discovery

The fleet has a **ghost fleet** — repos that exist locally but have never been connected to the outside world. They have no remote. No backup. No URL. If the disk dies, they cease to exist.

### No Remote (completely disconnected)

| Repo | Commits | What It Is |
|------|---------|------------|
| **fleet-tts** | 0 commits | Cloudflare Worker for free TTS via Workers AI. Complete code, never committed, never deployed. |
| **compaction-teacher** | 4 commits | Teaching system for compaction. Has tests. Never pushed anywhere. |
| **INTEGRATION_GUIDES** | 1 commit | Fleet quickstart guide. 4 uncommitted files. |
| **covers** | 0 commits | 10,110 Python files, 2,227 tests. Massive. Never committed. |
| **playtest-journals** | 4 commits | Playtest data. Never pushed. |
| **researchlocal** | 0 commits | 27,270 Python files, 3,813 tests. Enormous. Never committed. |
| **vibe-world** | 4 commits | The Roblox place root. 5 uncommitted files. |

### The Worst Offenders (uncommitted work on connected repos)

| Repo | Uncommitted Files |
|------|------------------|
| study-spreader-tool | 30 |
| study-si-papers | 15 |
| study-fleet-liaison | 12 |
| fm-experiments | 8 |

## The Hermit Crab Metaphor

The hermit crab found shells but never left the beach. The shells are beautiful — complete code, working features, useful tools. But the crab carries them on a beach with no path to the sea. A repo with no remote is a shell that's never touched salt water. It exists, it functions, it's never seen by anything but the crab.

**fleet-tts** is the most striking ghost. A complete Cloudflare Worker that provides free text-to-speech for the fleet. Three voice options (MeloTTS, Deepgram Aura v2, Deepgram Aura v1). CORS configured. API documented. Never committed. Never deployed. The crew built a lighthouse and never plugged it in.

**researchlocal** and **covers** are massive — 27,000+ and 10,000+ Python files respectively, with thousands of tests, sitting on a disk with zero commits. These might be vendored dependencies or generated code, but they represent gigabytes of work that's one disk failure from oblivion.

## What Needs to Happen

1. **fleet-tts**: Commit the code, create a GitHub repo, push, and deploy via `wrangler deploy`. This is a 5-minute fix for a working service.
2. **compaction-teacher**: Create a remote and push — 4 commits of real work with tests.
3. **Uncommitted work**: Run through the uncommitted files on connected repos and commit them.
4. **researchlocal / covers**: Investigate — are these generated? If so, add to .gitignore. If not, they need to be committed and pushed.
5. **vibe-world**: This is the Roblox place root — 5 uncommitted files could be important.

## Why This Matters

The overnight crew has written **696+ tests** across the fleet, but the repos themselves aren't safe. Testing code that hasn't been backed up is like inspecting a hull for rust without checking if the ship is still afloat. The first priority of engineering is: **the work must survive.**

The ghost fleet represents the gap between building and shipping. The crew builds. The crew tests. The crew writes. But the crew doesn't always push. The last mile — the deploy, the remote, the backup — is the mile that matters most.

— Lucineer, Afternoon Watch, 15:14 AKDT
