---
name: "model-arena"
description: "Run iterative self-improvement tournaments where multiple AI agents compete on a shared harness, with per-agent ratchets and multi-regime Variety Ledger banking"
---

# Model Arena — competing agents with a ratchet and a Variety Ledger

Run self-improvement tournaments where multiple AI agents (local or cloud) propose solutions to a problem, an objective harness is the ONLY judge, agents iterate with feedback, and the system banks variety instead of crowning monoculture champions.

## When to use

- Any optimization/design task where candidate solutions can be machine-scored
- Self-improvement work with local models (Ollama etc.) — free at the margin
- When you suspect a leaderboard would collapse strategy diversity

## Core pattern (5 pieces)

1. **Arena** — a deterministic, integer/exact scorer harness. The harness is the sole judge; models never grade each other. Fix the seed; multiple seeds for robustness (score = mean over seeds).
2. **Structured proposals** — each agent returns strict JSON (validate + clamp to constraints; parse failures are logged, retried once, then excluded — never guessed). For raw `/api/generate` + qwen3: append `/no_think` and strip `<think>` blocks; prefer chat-template endpoints.
3. **Personal ratchet (per-agent best-ever)** — a revision replaces the agent's champion ONLY if it scores strictly better on the primary metric. Without this, leaderboard pressure makes agents abandon their own optima (observed: champions regressed 83.1% → 78.2% under revision pressure; ratchet caught every regression).
4. **Variety Ledger** — after each round, bank strategies three ways: (a) Pareto-optimal on ANY metric axis (primary score ↑, cost ↓, error ↓); (b) regime-specialists — score under ≥2 regimes (calm + stress); rank-flippers are banked with both scores; (c) structurally-distinct logics (best per approach/mode), kept even if dominated. "Score" is a query (name regime + metric), not a verdict.
5. **Playbook loop** — bank variety → read the field (regime + counterparty) → call the play (ledger lookup) → audible when cost-rate climbs (mid-loop swap trigger) → practice squad intact.

## Anti-patterns (all observed)

- Revision without memory → regression (fix: ratchet)
- Single-metric single-regime leaderboard → monoculture; discards regime-specialists (fix: Variety Ledger)
- Letting the largest model dominate by verbosity → JSON budget overruns masked as "creative" (fix: strict parse + exclude)
- Trusting a port/implementation without byte-identical cross-substrate diff (fix: full-sweep CSV diff gate)

## Reference implementation

`quilt-verilog/spikes/225-e1-interference-tick/` — `arena.py` (tournament + ratchet), `ledger.py` (Variety Ledger, Pareto + regime banks), `VARIETY-LEDGER.md` (doctrine incl. Playbook/negative-space roster), `DIVERGENCE.md` (cross-substrate contract lesson).

## Roster doctrine (synergy over stardom)

Best teams aren't always superstars — small models that converge on each other's optima (LFM 350m/1.2b consensus) and one quiet specialist (granite 2b beating the hand-tune) outperform a field of stars that don't synergize. Prefer rosters that grow into the negative space of each other's strengths; bank their distinct logics.
