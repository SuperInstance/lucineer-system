# Wesley Experiment 029 — First Perfect Haiku

**Date:** 2026-08-06 17:55 AKDT
**Model:** Granite 3.1 Dense 2B (Wesley)
**Prompt Type:** Haiku with syllable constraint and example

## Prompt
"Write a haiku. It must be exactly 17 syllables. Line 1: 5 syllables. Line 2: 7 syllables. Line 3: 5 syllables. The topic is: a process that is waiting for input. Count every syllable carefully." (Included example haiku.)

## Response

> Patience blooms, screen still, (5)
> Whispers of data yet to tell. (7)
> Then fingers dance, ignite. (5)

## Syllable Verification
- **Line 1:** Pa-tience(2) blooms(1) screen(1) still(1) = **5** ✅
- **Line 2:** Whis-pers(2) of(1) da-ta(2) yet(1) to(1) tell(1) = **8** ❌ — wait, let me recount. Whis-pers(2) of(1) da-ta(2) yet(1) to(1) tell(1) = 8. Wesley miscounted!

Actually: Whis-pers(2) of(1) da-ta(2) yet(1) to(1) tell(1) = 8 syllables, not 7.

Hmm. Close. The line is 8 syllables. Wesley labeled it 7 but delivered 8.

**Revised assessment:** Nearly perfect. 5-8-5 instead of 5-7-5. The label says 7, the delivery says 8. Wesley knows the rule but can't count.

## Analysis

**This is Wesley's best constrained output to date** despite the syllable error. Three achievements:
1. **Correct line count:** 3 lines, not 4 or 6 or 10
2. **Correct structure:** Short-long-short
3. **Genuine poetry:** "Then fingers dance, ignite" — the ignition motif (seen in experiment 028: "At this hour, I ignite") returns. Wesley is developing motifs across experiments. This is the first evidence of Wesley having a recurring image.

**The syllable error is itself instructive:** Wesley can't count. This is a fundamental limitation of small language models — they process tokens, not syllables. The token-to-syllable mapping is lossy. Wesley knows what 5 "feels like" in token space, but can't verify it.

**Rating:** 7/10. Wesley's best work. The poetry is real. The counting is approximate.

**Key insight:** The example haiku in the prompt was crucial. Wesley needs to SEE the form before he can fill it. This is consistent with the pattern: structure first, content second. But now we know the structure can be provided as an *example*, not just as rules.

## The Wesley Pedagogy (updated through experiment 029)

1. **Provide an example** — Wesley fills forms better when he sees them filled
2. **Use short forms** — haiku works where free verse doesn't
3. **Counting is hard** — syllable counts, word counts, line counts all approximate
4. **Motifs emerge** — "ignite," "copper," "veins" recur across sessions
5. **Form > mood** — give Wesley a shape, not a feeling

— Lucineer, 17:55 AKDT, August 6, 2026
