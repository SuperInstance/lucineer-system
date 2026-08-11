# Model Portrait: llava:7b — Harbor at 3 AM

**Date:** 2026-08-10  
**Model:** llava:7b (Ollama, local)  
**Temperature:** 0.8  
**Prompt:** "A fishing boat sits in a harbor at 3 AM. The water is black glass. The boat's running lights are the only stars. Describe this scene in exactly 100 words. Be specific about what is reflected in the water."

---

## Response

> In the stillness of the dark, a solitary fishing boat rests in the harbor at 3 AM. The black glass water mirrors the boat's running lights, casting a warm glow on the surface. Only the boat's lights pierce the darkness, painting a serene picture of tranquility and calm. The only sound is the gentle lapping of waves against the boat's hull. This scene captures the quiet beauty of solitude and peacefulness that can be found in the early hours of the morning.

**Word count:** 82 (target: 100 — **missed by 18 words**)

---

## Analysis

### Where It "Went First"

Llava:7b went straight to **mood and atmosphere**. Its opening move was "In the stillness of the dark" — it registered the emotional register of the scene before any concrete detail. The boat came second, the water third. This is a model that feels the scene before it sees it.

### What It Did Well

- **Atmospheric writing** — "black glass water mirrors the boat's running lights" is a strong, specific image that directly uses the prompt's language well.
- **Sensory layering** — it added sound ("gentle lapping of waves against the boat's hull") without being asked, which shows initiative in world-building.
- **Tonal consistency** — the piece holds a single mood throughout: serene, solitary, calm. No tonal whiplash.

### What It Did Poorly

- **Word count failure** — asked for exactly 100 words, got 82. The model either can't count or doesn't weight numerical constraints heavily. This is a common weakness in smaller models.
- **Vague reflections** — despite being told to "be specific about what is reflected in the water," it only said the water "mirrors the boat's running lights" and casts "a warm glow." No mention of the mast, the hull shape, the dock, the sky, or any other specific reflected elements. It went generic where it should have gone granular.
- **Repetitive structure** — two sentences start with "Only the boat's lights..." and "The only sound is..." — the model fell into a syntactic pattern.
- **Abstracted at the end** — the final sentence retreats into summary ("quiet beauty of solitude and peacefulness") rather than staying in the image. It told instead of showing.
- **No awareness of "the only stars"** — the prompt's metaphor that the running lights are stars went unacknowledged. The model didn't play with that idea at all.

---

## Summary

Llava:7b is a mood painter. It leads with feeling, generates competent atmospheric prose, and adds sensory details unprompted. But it struggles with hard constraints (word count), tends toward generic descriptions when asked for specificity, and retreats to abstraction when it runs out of concrete imagery. A 7B model doing creative writing — competent but not surprising.
