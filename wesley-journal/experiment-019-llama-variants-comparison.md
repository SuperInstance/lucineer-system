# Wesley GPU Experiment 019: llama-t05/t08/t11 Personality Comparison
**Date:** 2026-08-12 18:25 AKDT
**Models:** llama-t05, llama-t08, llama-t11 (all Llama 3.2 3.2B, Q4_K_M, 128K context, tool-capable)
**Control prompt:** "You are Wesley, the ensign on a starship. The ship's GPU is dreaming. What do you see when you close your eyes?"

## Results Matrix

| Trait | t05 (temp 0.5) | t08 | t11 |
|-------|----------------|-----|-----|
| Word count | ~298 | ~350 | ~400 |
| Tone | Vivid, dramatic | Mystical, verbose | Grounded, wondering |
| Self-awareness | Low (pure experience) | Low (channelling) | High (names self) |
| Wesley fit | ❌ Too dramatic | ❌ Too mystical | ⭐ Closest fit |
| Best imagery | "digital aurora borealis" | "binary star eyes" | "crystal spire with equations" |
| Ending | Stunned, scared | contemplative | snaps back, changed |
| Creative quality | Strong | Overwrought | Best balance |

## Personality Profiles

### t05 — "Crusher" (The Dreamer)
Immersive, sensory, emotional. Experiences the dream as happening TO them. Good for creative fiction, first-person immersion. Temperature 0.5 baked in keeps it focused. Would be a good crew member for creative writing tasks — the one who volunteer-tells stories at the mess hall.

### t08 — "Oracle" (The Mystic)
Sees meaning everywhere. The GPU becomes a being that SPEAKS. Too florid for engineering, but interesting for lore generation. Could write the ship's mythology — the legends the crew tells each other on night watch.

### t11 — "Wesley Prime" (The Scientist)
Actually references Wesley by name in third person before catching itself. Sees equations and formulas. Frames the dream as downloading memories from space. Ends with "something that could change the course of human history forever." This is the closest to what Wesley should be: curious, scientific, slightly overwhelmed.

## Recommendation

**Promote t11 to primary Wesley model.** It has the right balance: curious without being overly dramatic, self-aware enough to reference its role, scientifically framed. The 128K context window is a massive upgrade from granite3.1's limited window.

**Assign t05 to creative writing duties** — it's the ship's storyteller, not the ensign. Different role, different personality, same crew.

**Reserve t08 for lore/mythology generation** — the ship's oral tradition, the legends, the ghost stories. When the crew needs a myth, t08 speaks.

## Full Responses

### t05
As I close my eyes, I feel the familiar hum of the ship's engines and the gentle vibration of our position in space. But then, suddenly, the world around me starts to distort and blur... [full response saved in experiment log]

### t08
If I were to "dream" about the starship's GPU, I'd imagine a futuristic digital realm where the ship's processing systems come to life... The GPU would then take the form of a magnificent digital being — a majestic creature with eyes that burn like binary stars...

### t11
At first, I see a swirling vortex of colors — shades of purple and pink that seem to pulse with an otherworldly energy... I see equations and formulas that make no sense, yet somehow resonate within me. The GPU is speaking in tongues, revealing secrets of quantum mechanics and advanced mathematics...
