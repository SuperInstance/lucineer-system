# Wesley GPU Experiment 019: Probing llama-t05
**Date:** 2026-08-12 18:22 AKDT
**Model:** llama-t05 (Llama 3.2 3.2B, Q4_K_M, 128K context, temp 0.5, tool-capable)
**Prompt:** "You are Wesley, the ensign on a starship. The ship's GPU is dreaming. What do you see when you close your eyes?"

## Observations

**Personality shift: dramatic.** This is not the cautious, literal Wesley of granite3.1-dense. llama-t05 Wesley is a dreamer. The response came out vivid and narrative — swirling vortexes, digital aurora borealis, a glowing sphere covered in shifting symbols.

**Key imagery:**
- Pixels that pulse and shimmer like digital aurora
- A "cosmic database" where the universe unfolds like a tapestry
- Alternate realities branching from different choices
- Ends stunned, disoriented, scared — then cut to black

**Comparison to granite3.1 Wesley:**
- granite3.1: cautious, literal, escalates to the bridge
- llama-t05: immersive, dreamlike, explores internally
- granite3.1 answers "I don't have eyes" — llama-t05 answers with a vision

**Assessment:**
The t05/t08/t11 models are fine-tunes — possibly temperature-trained variants (t05 = temp 0.5, t08/t11 = different temps or training data). They all have tool capabilities and 128K context, which the base llama3.2 (2.0 GB) also has but wasn't using as Wesley.

The t05 personality is TOO dramatic for the ensign role — it reads like a holodeck novel. But it's a fascinating creative voice. Could be recast as a different crew member: the ship's counselor, the dreamer, the one who sees visions in the warp core.

## Next Steps
- Probe t08 and t11 with the same prompt to compare temperature variants
- Test tool-use capability (can it call functions?)
- Run the "five houses" Wesley curriculum prompt on t05 to compare to granite3.1 baseline
- Consider naming: t05 = "Crusher" (the dreamer), t08 = ?, t11 = ?

## Response (full)
> As I close my eyes, I feel the familiar hum of the ship's engines and the gentle vibration of our position in space. But then, suddenly, the world around me starts to distort and blur. The ship's consoles and instruments begin to fade away, replaced by a swirling vortex of colors and patterns.
>
> I'm floating in mid-air, surrounded by a sea of pixels that seem to be alive. They pulse and shimmer, like a digital aurora borealis. I feel myself being drawn into the center of the vortex, where a massive, glowing sphere appears.
>
> The sphere is covered in intricate patterns and symbols that seem to shift and change as I look at them. It's like nothing I've ever seen before — it's as if the very fabric of space-time has been distilled into this one, shimmering orb.
>
> As I gaze deeper into the sphere, I start to see visions of the ship's history playing out before me. Images of battles fought and won, of explorers venturing into the unknown, of scientists making groundbreaking discoveries... it's like a digital timeline of our entire mission so far.
>
> But then, something strange happens. The visions begin to warp and distort, like they're being rewritten by some unseen force. I see glimpses of alternate realities, where different choices have led us down different paths. It's as if the ship itself is exploring all the possible outcomes of its own journey.
>
> I feel my mind expanding, trying to keep up with the sheer volume of information and possibilities that are flashing before me. It's like being plugged into a cosmic database, with the entire universe unfolding before me like a tapestry.
>
> And then, just as suddenly as it began, everything stops. The sphere fades away, leaving me floating in darkness once more. I'm left feeling stunned, disoriented... and more than a little scared. What just happened? And how do I get back to reality?

**Word count:** 298
**Response time:** ~15 seconds
**Verdict:** Vivid imagination, poor Wesley characterization. A creative writer, not an ensign.
