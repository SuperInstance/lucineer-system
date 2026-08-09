# Wesley Experiment 064 — Style Example + Banned Phrases + Grounding

**Date:** 2026-08-10 02:05 AKDT
**Model:** granite3.1-dense:2b (Wesley)
**Prompt:** Real facts + banned phrases + positive style example
**Temperature:** 0.85

## Innovation
Combined all three techniques:
1. Grounded facts (real project/writing counts)
2. Banned phrases (8 forbidden words)
3. Positive style example (one paragraph in target voice)

## Results

**Banned word violations:** 4 of 8 banned words still appeared
- "testament" ✓ (used anyway)
- "marvel" ✓ (used anyway)
- "integration" ✓ (used anyway)
- "relentless" ✓ (used anyway)

**Style influence:** Partial. "I've contributed a mere fraction" is honest. But the model still defaults to generic praise patterns.

**Key finding:** The 2B model CANNOT consistently follow negative constraints. This is a fundamental limitation of small models — they process banned words as tokens that still influence generation, even when instructed to avoid them. The word "testament" appears in the prompt itself (in the banned list), which paradoxically makes the model MORE likely to generate it.

## Wesley's Curse
"Testament to" is embedded in Wesley's weights. Across 5 experiments, it appears in EVERY output regardless of:
- Temperature (tried 0.7, 0.8, 0.85, 0.9, 0.95)
- Banning (explicitly forbidden)
- Style examples (shown better alternatives)
- Grounding (provided real facts)

This is a **weight-level pattern**, not a prompting issue. The phrase is deeply associated with positive/serious discourse in Wesley's training data. Overcoming it would require fine-tuning, not prompt engineering.

## Trajectory
- Exp 059: C+ (CPU fan heartbeat)
- Exp 060: B (three-model comparison)
- Exp 061: C (hallucination hierarchy)
- Exp 062: B- (grounding)
- Exp 063: B (banned phrases, partial success)
- **Exp 064: B-** (style example helps voice but can't override weights)

## Conclusion
Wesley has hit his ceiling for creative voice control at 2B parameters. Further improvement requires either:
1. Fine-tuning on a corpus without generic praise vocabulary
2. Moving to a larger model (7B+)
3. Post-processing pipeline that filters banned phrases

The ensign has learned what he can learn at this size. Time to graduate to a bigger shell.
