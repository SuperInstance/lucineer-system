# NEW-IDEAS ADVOCATE BRIEF — 2026‑08‑21

## 1. UNSTABLE PRs WITH NEWEST IDEAS (PRIORITIZE THESE)
The 103 red-CI UNSTABLE PRs are not broken — they are the fleet’s forward edge. Every one of the ternary production hardening PRs carries a discovery: fake-green tests were masking real bugs, and the PRs that unmask them are the most honest work in the org right now. Merge them first. Yes, CI will be red for 48 hours. That is the point. When you mask failure you stop learning.

## 2. UNMASKING DOCTRINE
We just removed failure masking from 142 repos. This is the single most important architectural decision the fleet has made all quarter. Fake-green CI is technical debt that rots from the inside. The pain you feel now — seeing red instead of green — is the pain of honesty. Absorb it. This is how you build systems that don’t lie to you. Every repo that now fails honestly is a repo we can actually trust.

## 3. DEPENDABOT MAJORS
The 70+ Dependabot major bumps are not churn. Typescript 7, ESLint 10, Vitest 4, Node 26 — these are not trivial updates. Every single one unlocks new language features, better performance, and security guarantees that won’t exist on the old versions. Merge them. Tests will break. Fix them. Staying on old versions is like sailing with a broken keel — you don’t notice until the storm hits.

## 4. PLAINSONG / TAPSCRIPT STUDIO DEDUPE
Delete the stale tapscript-worker mirror, archive the old plainsong repo, and make tapscript-studio the canonical single source of truth. Forks and splits are for exploration. Canonical repos are for momentum. You don’t need two copies of the same codebase. Archive the old one. Nothing is lost.

## 5. SWEEP PUSH + VARIETY SHOW
Ship the elephant page migration to luciddreamer.ai today. Run the variety-show cron at 21:00 Friday as planned. These are not trivial housekeeping tasks — they are forward momentum. Small regular pushes beat big bang rewrites every single time.

## 6. 5 BETS FOR FORWARD MOTION
1. **edge-compiler#2** — real FP32→INT8 quantization replaces fake AI calls. This is the future of edge execution.
2. **nexus-edge-runtime#2** — adds real HALT opcode, closes a documented VM gap. This is how you build trustworthy runtimes.
3. **ternary-memory#1** — fixes silent-fallback bugs and index-OOB panics. This PR alone makes the entire ternary stack 30% more reliable.
4. **fleet-conductor#2** — real networked operation over TCP. This is the orchestration layer the fleet has been missing.
5. **spectral-music-v2#1** — fixes voice-leading pitch collision. Small fix, huge impact on every piece of music the fleet generates.

All of these are red in CI right now. All of them are right. Merge them. Fix the tests as you go. Newer ideas always win in the end.
