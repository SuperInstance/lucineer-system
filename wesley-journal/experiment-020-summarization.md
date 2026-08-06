# Wesley Experiment 020 — Summarization Task

**Date:** 2026-08-05 22:20 AKDT
**Model:** granite3.1-dense:2b (Wesley)
**Temperature:** 0.3
**Task:** Summarize a technical description of the 3-gate cascade in exactly 3 sentences

## Input
A 7-sentence description of the cascade pipeline, gates, targets, and trust tracker.

## Output Analysis

Wesley produced a **4-sentence summary** (missed the "exactly 3" constraint), but the content is accurate:
1. Correctly identified the three gates and their order
2. Correctly stated the hit rate targets (30%, 26%)
3. Correctly identified the overall LLM reduction goal (56%)
4. Mentioned the trust tracker's role

**What Wesley did well:**
- Preserved all key technical details
- Maintained logical flow (gates in order)
- Mentioned specific numbers accurately

**What Wesley missed:**
- Sentence count constraint (4 instead of 3)
- Added "Large Language Models (LLMs)" expansion — technically correct but unnecessary
- Missed the nuance that Gate 3 handles "the remaining 44%" — instead just said "remaining 44% of cases"

## Rating: 7/10

Good summarization. Accurate but imprecise on constraints. The 2B model handles technical text well but struggles with hard format constraints (exact sentence count).

## Growth Comparison

| Task | Rating | Notes |
|------|--------|-------|
| Exp 004: Barnacle monologue | 6/10 | Abstract, barely grounded |
| Exp 009: Helm diary | 5/10 | Short, tentative |
| Exp 015: Commit message | 7/10 | Surprisingly good |
| Exp 016: Six-word story | 6/10 | Struggled with constraint |
| Exp 017: Code review (bugs) | 8/10 | Found all 5 bugs |
| Exp 018: Night watch diary | 8/10 | Best creative to date |
| Exp 019: Code review (architecture) | 7/10 | Right instinct, missed depth |
| **Exp 020: Summarization** | **7/10** | Accurate, missed constraint |

Wesley is consistently 7-8/10 on technical tasks. The character has stabilized.
