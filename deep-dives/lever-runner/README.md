# Lever Runner — Project README

> **A deep-dive study as part of the Slackwater Cognition Architecture research.**

## What This Is

Analysis of [SuperInstance/lever-runner](https://github.com/SuperInstance/lever-runner) — a post-inference command executor that runs pre-approved shell commands by intent, not by tool schemas.

## Key Findings

- **Token-lean execution:** ~70 tokens per query (vs 2,000-5,000 for Copilot CLI / Warp / Cursor)
- **Three-gate architecture:** Rust fastloop (50µs) → Python cache (200µs, 44% hit) → LLM intent extraction (500ms)
- **Structural security:** LLM cannot inject commands — it outputs a 3-8 word phrase, not shell syntax
- **Trust scoring:** Self-improving action selection (+1.5 success / -4.0 failure, auto-promote at 20+ successes)
- **Production-ready:** 160 tests, MIT license, multiple deployment surfaces (CLI, Telegram bot, HTTP API)

## Documents

| File | Contents |
|------|----------|
| `analysis.md` | Full architecture analysis, code quality assessment, integration opportunities |
| `LEARN.md` | Extracted patterns and lessons applicable to cognition architecture |
| `integration-plan.md` | Concrete phased plan for integrating Lever Runner patterns |
| `README.md` | This file |

## Relevance to Slackwater

Lever Runner's intent → action pipeline is isomorphic to the cognition architecture's perception → action selection pipeline. The three-gate cascade, trust scoring, and token-lean operation patterns are directly transferable.

## Repository

- **Upstream:** https://github.com/SuperInstance/lever-runner
- **Cloned to:** `/home/eileen/projects/study-lever-runner`
- **Version studied:** v1.0.0 (commit: main branch, 2026-08-03)
