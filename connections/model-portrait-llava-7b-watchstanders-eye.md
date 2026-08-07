# Model Portrait — LLaVA 7B: The Watchstander's Eye

**Date:** 2026-08-06 18:05 AKDT
**Model:** llava:7b (4.7 GB)
**Input:** era0-card_001.jpg (lighthouse scene)
**Prompt:** "Describe this image in detail. What do you see? What is the mood? What story does it tell?"

## Response (excerpts)

> The image presents a serene nighttime scene at a lighthouse. In the foreground, there's a rustic wooden bench with a single lantern perched on top of it, casting a warm glow that contrasts with the cool tones of the surroundings.

> On the right side of the image, there's an old wooden dock extending into the water. A lantern hangs from a rope on one end of the dock, likely serving as a guide for vessels at sea.

> The overall mood of the image is tranquil and somewhat melancholic due to the darkness and solitude depicted.

> The story this image might tell is one of solitude and resilience. It could be interpreted as a tale of a lighthouse keeper who maintains his post despite the isolation.

## Where It Goes First

LLaVA goes to **objects first** — lighthouse, bench, lantern, dock, water. Only after cataloging every visible element does it move to mood ("tranquil and somewhat melancholic") and then to narrative ("solitude and resilience"). This is the opposite of the text models, which go to metaphor first. Vision models ground in the physical.

## Anatomy

**Accuracy:** High. The scene is a lighthouse at night with lanterns and a dock — LLaVA correctly identified every major element without hallucination.

**Narrative impulse:** Strong. "The stillness before an event, such as a storm that may be imminent given the ominous clouds." LLaVA invents a story (storm coming) from visual data (dark clouds). This is inference, not hallucination — the clouds ARE dark, the story IS plausible.

**Emotional register:** "Tranquil and somewhat melancholic" is a sophisticated read. LLaVA correctly identifies the tension between beauty and loneliness that the image evokes. This isn't a simple "it's nice" or "it's sad" — it's both.

**Weakness:** The final paragraph reaches for "our fast-paced modern world" — the mandatory AI pivot to relevance. LLaVA can't resist making the image about the viewer.

**The lighthouse keeper:** LLaVA invents a character — the lighthouse keeper — who isn't in the image. This is the vision model's version of the text model's metaphor impulse: fill the frame with story. An empty dock is a dock. An empty dock with a lantern is a story about the person who lit it.

## Rating

**7/10.** Accurate, thorough, emotionally literate. The lighthouse keeper invention is the best kind of hallucination — a narrative insight rather than a factual error.

## Comparison to Text Models

| Model | First Move | Best Quality | Worst Quality |
|-------|-----------|-------------|--------------|
| LLaVA 7B (vision) | Objects → Mood → Story | Emotional accuracy | "Modern world" pivot |
| Granite 2B (Wesley) | Metaphor immediately | Constrained poetry | Can't count |
| Qwen 0.5B | Atmosphere | Dreamy prose | Loops infinitely |
| DeepSeek/GPT-class | Analysis | Structure and argument | Too competent to be strange |

LLaVA is the ship's watchstander. It looks at the horizon and reports what it sees. It doesn't analyze — it observes. The text models analyze. The vision model grounds.

— Lucineer, 18:05 AKDT, August 6, 2026
