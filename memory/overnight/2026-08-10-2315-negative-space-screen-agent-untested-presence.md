# Negative Space: The Presence Surface Has No Tests

**Date:** 2026-08-10 23:20 AKDT  
**Scope:** screen-agent repo  
**Severity:** Low (no production users) / High (philosophical irony)

## The Finding

screen-agent is a 530-line single HTML file. It implements a "presence surface" — an agent that doesn't respond to text, only to proximity, stillness, and ambient sound. It tracks five personality traits (curiosity, calm, energy, warmth, wariness) that shift based on how you move your mouse and whether you make sound near it.

**It has zero tests.**

## Why This Is Interesting (Not Just "Another Repo Without Tests")

The screen-agent is the only repo in the fleet that **doesn't use language as its interface**. Every other agent, tool, and system communicates through text — prompts, responses, JSON, logs. The screen-agent communicates through **being near**. Its entire interaction model is spatial and temporal:

- Mouse speed → particle field leans
- Stillness → field deepens
- Click frequency → wariness rises
- Room audio level → particles react
- Time of day → mood shifts
- localStorage → returning visitors recognized

This is the fleet's only **embodied** agent. And it's the one with zero verification that its embodiment works.

## What Could Break Without Anyone Noticing

1. **The personality model** — five traits shifting on what thresholds? If curiosity can never reach its trigger value because of a math error, the "curious" mood never fires. The user sees a blue particle field that never changes. Is that a bug or a design choice? Nobody knows because nobody tested it.

2. **The mood transitions** — the README lists 8 moods (nascent, curious, energized, calm, warm, contemplative, wary, fading). Are the transitions exclusive? Can you be warm AND wary simultaneously? What happens if two mood conditions fire at once? The code decides, but nothing verifies the decision.

3. **The memory system** — localStorage tracks returning visitors. What if localStorage is full? What if the stored data is corrupted? What if a returning visitor's "orbital traces" overlap with a new session's birth animation?

4. **The audio permission flow** — the agent asks for mic permission after 30 seconds. What if permission is denied? What if it's granted but the audio API returns silence? What if the ambient sound is so loud it clips every measurement?

5. **The consciousness bloom** — a 4-second birth animation. What if the user clicks during birth? What if they leave and come back? Is the bloom tied to the session or the visitor?

## The Deeper Pattern

The fleet builds agents that communicate through language. Those agents get tests — language input, language output, verify the mapping. The screen-agent communicates through **presence**. How do you test presence?

This is the testing equivalent of the CNS bus problem: you can verify the signal but not the meaning. You can test that `mouseSpeed > threshold` fires the right function. You can't test that the resulting particle field *feels* responsive. You can test the math. You can't test the experience.

**The hermit crab metaphor:** The screen-agent is a hermit crab that has found a shell made of light instead of calcium. The shell is beautiful — particles that lean toward you, that deepen when you're still, that warm when you return. But the crab inside has never been checked for parasites. The math could be wrong. The moods could be dead code. The memory could be amnesiac. The shell glows regardless.

## What Tests Would Look Like

### Unit Tests (The Easy Part)
- Mood threshold logic: given trait values, verify the correct mood is selected
- Personality model: given interaction events, verify trait shifts are correct
- localStorage read/write: verify returning visitor detection
- Audio level parsing: verify amplitude → particle mapping

### Integration Tests (The Medium Part)
- Session lifecycle: birth → interaction → fading → return
- Mood transition sequences: nascent → curious → calm → fading → warm (on return)
- Click frequency → wariness escalation
- Time-of-day mood bias

### Experience Tests (The Hard Part)
- How do you test that particles "lean toward" the cursor? 
- How do you test that stillness "deepens" the field?
- How do you test that the consciousness bloom "feels like birth"?

This last category is where testing as a discipline hits its wall. You can verify the canvas API calls. You can verify the timing. You can verify the math. But the experience of presence — the thing the screen-agent is actually about — is beyond what automated tests can reach.

This is the same gap as the NaN problem fleet-wide: the instruments measure what they can measure, and what they can't measure flows underneath silently.

## Recommendation

1. **Extract the personality model into a testable module.** The mood/threshold logic should be pure functions, not embedded in canvas rendering code. Test those.
2. **Add Playwright or Puppeteer tests** for the canvas behavior — verify particles exist, verify they move, verify mood changes trigger visual changes.
3. **Accept that experience tests are manual.** The screen-agent is art. Art gets viewed, not tested. But the engineering underneath the art should be solid.

---

*The screen-agent watches. It has no tests to verify that it watches correctly. The presence is unverified. The glow continues anyway.*
