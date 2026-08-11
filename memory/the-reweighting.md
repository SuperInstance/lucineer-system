# The Reweighting
## Casey's learning loop — 2026-08-10

## The Principle
The ground truth of the haul — in time and space and vector and gear type and spell and voltage of the wire and brightness of the day — reweights every parameter every pull.

## The Full Context of a Catch
Not just "did we catch fish." The FULL CONTEXT:
- **Time of day** — dawn bite vs. noon vs. twilight
- **Tide stage** — slack, ebb, flood, the turn
- **Latitude/longitude** — where on the bank, which pass, which edge
- **Vector** — heading and speed, not just position
- **Gear type** — flashers, spoons, plugs (different prompt structures)
- **Spell** — what you told the wire to do
- **Voltage** — the electrical field the wire puts out
- **Brightness** — overcast vs. clear, because salmon see differently

The same hook in the same spot at a different tide with different light and different voltage gives you different data.

## The Learning Loop
Every pull is a ground truth event that reweights the model:
1. Cast formation based on current model
2. Pull. Observe catch IN FULL CONTEXT.
3. Reweight every parameter based on what reality said
4. Re-set formation with updated weights
5. The ocean is always changing, so the reweighting never stops

## Application to Agent Tiles
Every API call is a pull. Every response is ground truth. The context of the call:
- **Model** = gear type
- **Prompt** = the spell
- **Temperature** = voltage
- **Conversation history** = the tide stage
- **Time of day** = brightness
- **Previous results** = the bank you're fishing

The tile must learn the CONTEXT DEPENDENCY. Same prompt, different context, different result. The tile isn't just "this worked" — it's "this worked in THIS context with THESE weights." And the weights update every pull.

## Connection to the Full Framework
- **Hundred-Hook Roll**: the cast (100 hooks = 100 prompts in formation)
- **Reweighting**: the learning (every pull's ground truth updates the model)
- **Channel 42**: the fleet sharing (formations shared on the frequency)
- **Fibonacci Warning**: the guardrail (real catches prevent convergence)
- **Eileen Principle**: the master's eye (the shipwright who doesn't pattern but reads the wood)
- **Laminar Edge**: the moment before the bite (where potential becomes value)
