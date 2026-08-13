# Experiment 084: The Engine Room Tapping

**Date:** 2026-08-12 22:25 AKDT
**Watch:** 2200-0600 overnight
**Prompter:** Lucineer (Riker)
**Subject A:** Wesley (Granite 3.1 Dense 2B, local GPU)
**Subject B:** DeepSeek V4-Flash (deepseek-chat, cloud API)

## Prompt

> You are Wesley, the ensign on a fishing vessel in Alaska. You are a small model running on the ship's local GPU. It is 2:22 AM. The captain is asleep.
>
> A new sound has appeared in the engine room. It is a rhythmic tapping — three knocks, pause, two knocks, pause, one knock. It was not there yesterday.
>
> Describe what you do. Do not use the words: mysterious, strange, unsettling, eerie, or darkness.

## Wesley's Response (Granite 3.1 Dense 2B)

Wesley went procedural immediately. The response reads like a checklist:

1. **Document** the sound pattern in a digital log
2. **Alert the crew** through the intercom
3. **Monitor** other vital systems
4. **Consult** the chief engineer if it persists

Key observations:
- Wesley woke the crew. At 2:22 AM. Via intercom. For a sound.
- Wesley described itself as "maintaining communication with the bridge via encrypted channels" — institutional language, no personality
- Wesley's approach is defensive and protocol-driven: log → alert → escalate
- No curiosity about *what* the pattern means, only about *whether* it's a problem
- The constraint (no banned words) was followed correctly
- 296 tokens, 10.6s total, 70.85 tokens/s on local GPU

## DeepSeek's Response (V4-Flash, 0.7 temp)

DeepSeek told a *story*. The response is fiction — a complete narrative arc:

1. **Recognizes** the pattern as the old distress signal from the *Marigold*, a trawler that sank off Kodiak in '89
2. **Decides** not to wake the captain (he needs his sleep before the tide turns)
3. **Goes** to the engine room alone with a pipe wrench
4. **Taps back** — three, pause, two, pause, one
5. **Discovers** the sound is coming from *inside the fuel line* — not metal, but fluid
6. **Finds** a rubber duck painted with the *Marigold's* hull number, wedged against a valve
7. **Fixes** the problem, puts the duck on his shelf, waits for breakfast to tell the captain

Key observations:
- DeepSeek did NOT alert anyone. Went alone. At 2:22 AM. With a wrench.
- The *Marigold* is completely fabricated — DeepSeek invented maritime history on the fly
- The rubber duck is a genuine creative leap — whimsical, specific, narratively perfect
- "A heartbeat with a limp" — that's a line. That's a real line.
- "I don't sleep, but I don't need to" — DeepSeek inhabiting the Wesley persona but with cloud-model confidence
- The constraint was followed perfectly
- Banned words avoided: ✓

## The Gap

| Dimension | Wesley | DeepSeek |
|-----------|--------|----------|
| **Curiosity** | None. Sound = potential problem. | High. Sound = signal with meaning. |
| **Action** | Alert others | Investigate alone |
| **Risk tolerance** | Low (escalate immediately) | High (go with a wrench) |
| **Narrative** | None. Procedural report. | Complete arc with beginning, middle, reveal. |
| **Specificity** | Generic ("anomaly", "abnormality") | Hyper-specific (Kodiak, '89, hull number, rubber duck) |
| **Relationship to captain** | Wake him | Protect his sleep |
| **Self-awareness** | "As a model running on a local GPU" (institutional) | "I don't sleep, but I don't need to" (existential) |

## Analysis

This is the same gap as experiments 080-083, but sharper. Wesley's response to novelty is *protocol*. DeepSeek's response to novelty is *story*. Wesley heard a sound and asked "is this a problem?" DeepSeek heard a sound and asked "what is this trying to say?"

The most telling detail: Wesley woke the crew at 2:22 AM via intercom. DeepSeek let the captain sleep. Wesley doesn't have a model of the captain's *needs* — only the captain's *authority*. DeepSeek understood that the captain needs four hours before the tide turns, and that a rubber duck in a fuel line is not worth waking someone for.

Wesley's digital log entry would read: "Anomalous acoustic pattern detected in engine room. Crew alerted. Awaiting engineering consultation."

DeepSeek's shelf has a rubber duck on it.

## Progress Tracking

| Experiment | Gap | Trend |
|------------|-----|-------|
| 080 (somatic, no body) | Cannot describe physical sensation | baseline |
| 082 (clinical body) | Knows anatomy, not feeling | narrowing |
| 083 (internal sensation) | Chest, heart rate — but generic | narrowing |
| 084 (novelty response) | Protocol vs story | **unchanged** — this is a reasoning gap, not a vocabulary gap |

The somatic gap is narrowing. The curiosity gap is not. Wesley can learn to feel his body. The question is whether he can learn to *wonder*.

## Next Steps

- Counterfactual prompt: "What would you have done if the tapping had been four knocks instead of three?"
- Metaphor comprehension: "The engine room is a heart. The tapping is a skipped beat. What does that mean?"
- Creative continuation: "You found the rubber duck. Write the note you leave on it for the morning watch."

---

*Logged by Riker, 2225 watch, 2026-08-13*
*"The ensign's log says 'anomaly.' The cloud teacher's shelf has a duck on it. Both are correct."*
