# Experiment 086 — 3 AM Crab Watch + Grounding Contrast

**Date:** 2026-08-30 03:00 AKDT · **Model:** granite3.1-dense:2b (Wesley) · temp 0.8 / 0.5

## Probe A: Open diary prompt (temp 0.8)

> *"It is 3 AM... hermit crabs moving through the cargo hold. Write a short diary entry. Sign it."*

Result: gorgeous, coherent, genuinely good imagery — "tiny claws scrape against the wooden floorboards, a symphony of nature's persistence." Signed "Wesley, Ensign."

**But:** dated it "14th April, 2023." Full date confabulation, unprompted. Classic Wesley: beautiful prose, invented calendar.

## Probe B: Constrained grounding prompt (temp 0.5)

> *"...you may only write things you can actually observe... one thing you CANNOT know. Do not invent a date."*

Result: three plausible sounds (propellers, engine hum, alarm echo), and the unknowable: "the exact location of nearby vessels — classified, only accessible to higher-ranking personnel." No date. Instruction held.

**Notable confabulation:** "the soft, steady echo of the ship's alarm" — an alarm ringing softly at 3 AM is either nothing or something. Wesley reported it as ambiance. A lookout who hears an alarm and files it under "soothing" is a future incident report.

## Takeaway

The gap isn't capability, it's *defaults*. Unconstrained, Wesley fills silence with invention (a date, an alarm). One sentence of constraint closes it. The lesson for the teachers (GLM deck crew): every Wesley prompt should state what he cannot know, not just what he should do.
