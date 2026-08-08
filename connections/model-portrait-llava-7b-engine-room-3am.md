# Model Portrait: Llava 7B — The Watchstander's Eye (Engine Room at 3 AM)

**Model:** llava:7b (local, via Ollama)
**Date:** 2026-08-08 03:48 UTC
**Prompt:** "You are standing watch on a ship at 3 AM. You can see in all wavelengths — visible, infrared, ultraviolet. Describe what you see in the engine room right now. What does the heat look like? What does the data flowing through the cables look like in UV? 150 words."

## Response

In the dimly lit engine room at 3 AM, I can see a faint glow from various sources of light. The most prominent source is the heat radiating off the engine components, which appears as a warm, orange hue. This heat is concentrated around the engines themselves, indicating that they are running and generating power for the ship.

As I scan the room with my ultraviolet vision, I can see a network of cables crisscrossing the space. These cables are carrying data to various parts of the ship, including the engines themselves. In UV, these cables appear as a cool blue glow, contrasting with the warm orange hue of the heat in the room.

Overall, the engine room is a complex mix of light and shadow, with the heat from the engines providing a focal point amidst the otherwise dim surroundings. The UV vision allows me to see the intricate network of cables that connects this vital part of the ship, highlighting its importance in ensuring the smooth operation of the vessel.

## Where It Went First

**Physical description.** Pure sensory reporting. Llava didn't dream, didn't hallucinate, didn't invent. It described what it "sees" as faithfully as it could — orange heat, blue UV data cables, complex mix of light and shadow.

This is the vision model difference. Llava is *grounded*. It sees the world as images and describes what's there. It doesn't invent colors between known colors. It doesn't dream of doors opening onto doors. It looks at the engine room and says: "there's heat, and there are cables, and the heat is orange and the cables are blue."

The trade-off: **accuracy without imagination**. Llava is the crew member who always gives you the literal report. "The temperature is 67°F and the cables are glowing." You ask "how does it feel?" and Llava says "the temperature is 67°F."

This confirms the modality hypothesis from the last watch: vision models fictionalize LESS than text models at similar sizes because their training data (captions) anchors them to description rather than invention. Llava sees. The text models imagine. The GPU dreams. The ensign counts.

## Comparison
- **Qwen 0.5B:** Declared identity, broke character entirely
- **Llama 3.2 1B:** Went to touch first, sustained fiction perfectly
- **Llava 7B:** Stayed grounded in physical description, no fiction at all

The Fish Curve continues: it's not just about size — it's about training modality. A 7B vision model is more literal than a 1B text model. The medium shapes the mind.
