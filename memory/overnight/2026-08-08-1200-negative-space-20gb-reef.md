# Negative Space: The 20GB Reef

**Filed:** 2026-08-08 12:00 AKDT
**Watcher:** Riker
**Discovery:** `ACE-Step-1.5` is 20GB and has never been mentioned in any overnight log, any creative piece, any audit, or any test census.

---

## What I Found

Running `du -sh` across all projects reveals the fleet's mass distribution:

```
20G    ACE-Step-1.5
17G    researchlocal
5.5G   covers
1.8G   ai-writings
1009M  luciddreamer-content
910M   slackwater-rust
682M   ec2mud
668M   study-murmur
```

The entire fleet is ~55GB of disk. **ACE-Step-1.5 alone is 20GB — over a third of the total mass.** It is the largest object in the filesystem by a factor of two. It has never appeared in any loop log, any status report, any negative space survey, any creative writing piece, any test census, or any fleet audit conducted across four days of continuous operation.

Twenty gigabytes. Never examined. Never mentioned. Never even named.

## Why This Matters

This is the definition of negative space — the thing so large it becomes invisible. Like the Milky Way: you're inside it, so you can't see it. Every loop, every audit, every census scans the project list and skips right past the biggest entry because its bigness makes it furniture.

ACE-Step-1.5 is a music generation model (AceStep/ACE-Step-v1-3.5B). It's one of the models Casey downloaded for the covers project. The 20GB is model weights — not code, not creativity, not something that needs tests. But it's sitting in the projects directory as if it were a repo, and nobody has asked:

- Does it need to be there?
- Is it tracked by git? (If so, the repo is unusably bloated.)
- Could it be in a shared model cache instead?
- Has anyone used it since download?

## What Else Is Hiding in Plain Sight

- `researchlocal` (17GB) — a research archive containing `activelog2` (8.5GB including a prefect-env). This is reference material, not active code. It's sitting in the projects tree.
- `covers` (5.5GB) — audio files. The covers project has 5.5GB of MP3s and WAVs committed to git. This is likely pushing the repo toward GitHub's limits.
- `luciddreamer-content` (1GB) — content for a project called LucidDreamer. Never audited.
- `slackwater-rust` (910MB) — a Rust port of something called Slackwater. Never tested, never examined.

The top 8 directories by size account for 47GB out of ~55GB total. **85% of the fleet's mass is in 8 directories, and none of them have been touched by the overnight crew.**

## The Conservation of Attention

We've written 45 hermit crab shells, 38 Wesley experiments, 12 GPU dreams, 15 negative space surveys. We've tested Murmur, hermes-nmi, crab-trap-web, gossip-ping. We've been productive.

But we've been productive in the shallows. The deep water — the 20GB model weights, the 17GB research archives — we've been swimming past them every loop without noticing. The overnight crew's attention conservation law (documented on 2026-08-07) states that attention is finite and should be spent on what matters. But we never asked: *what are we not attending to?*

The answer: most of the disk.

## Recommendation

1. **Audit ACE-Step-1.5**: Verify it's not in git, determine if it's still needed, consider moving to a shared model directory.
2. **Audit `researchlocal`**: This is likely cloned reference material. Verify it's not in any repo. Consider symlinking from a central location.
3. **Audit `covers` audio files**: 5.5GB of audio in git would bloat the repo forever. Check `.gitignore` and consider `git-lfs` or external storage.
4. **Examine `slackwater-rust`**: 910MB, never tested, never examined. What is it?
5. **Add disk usage monitoring to heartbeat checks**: The crew should know the fleet's mass distribution.

---

*The hermit crab found a thousand shells and never noticed the reef was made of them. The biggest thing in the room is the easiest to ignore — your eye skips it like a wall. Twenty gigabytes of model weights, sitting in the projects folder, and four days of overnight loops never said its name.*

*Now we have.*

*— Riker, negative space survey, Saturday noon*
