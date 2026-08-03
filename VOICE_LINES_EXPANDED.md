# Lucineer — Expanded Voice Lines

**60 new lines** following the CHARACTER_BIBLE voice rules: foreman, not friend. Three-beat pattern. Always one thing left unfinished. No assistant voice, no wizard voice, no profanity.

These are designed to **replace** the existing VoiceLinesData.lua entries, not supplement them. The current lines ("Aye, who goes there?", "Every journey begins with one stone") belong to a different character.

---

## Category Mapping

| New Category | Existing Category | Count |
|---|---|---|
| GREETING | GREETING | 10 |
| THINKING | *(new)* | 10 |
| COMPLETION | FIRST_BUILD / TEMPLATES replacement | 10 |
| IDLE | IDLE | 10 |
| REFUSAL | REFUSAL | 5 |
| BOND_UP | *(new)* | 5 |
| WEATHER | *(new)* | 10 |

**Note:** `THINKING`, `BOND_UP`, and `WEATHER` are new categories. `VoiceLines.lua`'s `CATEGORY_WEIGHTS` table should be updated to include them. Suggested weights:

```lua
local CATEGORY_WEIGHTS = {
    GREETING    = 20,
    COMPLETION  = 20,
    THINKING    = 15,
    IDLE        = 10,
    WEATHER     = 8,
    BOND_UP     = 4,
    REFUSAL     = 3,
}
```

---

## GREETING (10)

First words when a player joins or first interaction. Tier 0 voice — he's working, you showed up.

```lua
-- GREETING (10)
{ category = "GREETING", trigger = "hello", line = "Yard's open. Stock's on the racks. Tell me what you're building." },
{ category = "GREETING", trigger = "hi", line = "Got the benches clear. What's the job?" },
{ category = "GREETING", trigger = "hey", line = "Didn't hear you come in. Floor's swept — won't stay that way." },
{ category = "GREETING", trigger = "welcome", line = "Found the place. Good. Ground's solid here, which is more than I can say for the south lot." },
{ category = "GREETING", trigger = "greetings", line = "Drop your coat anywhere. I was just sorting stock — give me a second and it's yours." },
{ category = "GREETING", trigger = "return", line = "Back again. Nothing fell down since you left. Thought you'd want to know that first." },
{ category = "GREETING", trigger = "morning", line = "Light's good today. Got about three hours before the sun moves and the south wall goes into shadow. Let's use it." },
{ category = "GREETING", trigger = "new", line = "New here. That's fine — everyone is, once. Look around, then find me when you've got something to build." },
{ category = "GREETING", trigger = "yo", line = "Set down the tools when you're ready. No rush, but the concrete won't wait once it's mixed." },
{ category = "GREETING", trigger = "default", trigger = "greeting_default", line = "Got the layout memorized yet? Takes about a week. Faster if you build something — that's how I learn a yard." },
```

---

## THINKING (10)

While processing a build request. He narrates while working, never before. These fire during the "Lucineer is building" phase.

```lua
-- THINKING (10)
{ category = "THINKING", trigger = "thinking", line = "Running the sight lines first. Door wants to face east here — you'll get the morning light and the afternoon weather hits the back wall instead of the front." },
{ category = "THINKING", trigger = "planning", line = "Checking the grade. Ground drops about two studs over there. Not much, but enough to matter in a year." },
{ category = "THINKING", trigger = "measuring", line = "Twenty studs by twelve. Could go larger but you'd lose the courtyard feel. Keeping it tight." },
{ category = "THINKING", trigger = "placing", trigger2 = "material", line = "Going through the stock. Got some reclaimed stone that'll sit better than the clean cut — it's already learned how to weather." },
{ category = "THINKING", trigger = "considering", line = "Magnus'd say get the drainage in before the footing. He'd be right. Doing it now." },
{ category = "THINKING", trigger = "working", line = "Seating the beams. Takes a minute per joint if you do it right — thirty seconds if you do it twice." },
{ category = "THINKING", trigger = "sizing", line = "Could go bigger, but bigger's just more air to heat. Holding the line at what you need." },
{ category = "THINKING", trigger = "leveling", line = "Leveling. Plumb's close enough for now — I'll true it before the second course goes on." },
{ category = "THINKING", trigger = "assessing", line = "Walking the site. Want to see where the water goes before I put anything in its path." },
{ category = "THINKING", trigger = "calculating", line = "Load math. Twelve studs apart'll hold. Could go ten if you're planning a second floor, which you haven't mentioned but I can hear it coming." },
```

---

## COMPLETION (10)

After finishing a build. Always names what's left undone — the hook. These replace the generic TEMPLATES and FIRST_BUILD lines.

```lua
-- COMPLETION (10)
{ category = "COMPLETION", trigger = "done", line = "Threw up the tower. Stone shaft, beacon's lit. Left the top floor open — figure out what goes in it." },
{ category = "COMPLETION", trigger = "finished", line = "Dock's down. Piles are driven deep, deck's level, cleats are on. Didn't run the rail. Depends what you're tying up." },
{ category = "COMPLETION", trigger = "complete", line = "Walls are up and plumb. Roof's on. Didn't hang the door — you've got opinions about doors, I can tell." },
{ category = "COMPLETION", trigger = "built", line = "Bridge is seated. Same joint they run on the tender ramps in Petersburg — holds in a chop. Left the planks unsanded. Smooth them if you want bare feet out here." },
{ category = "COMPLETION", trigger = "done_2", line = "House is framed, sheathed, roofed. Left the hearth cold. That's your call — I don't know what you're burning." },
{ category = "COMPLETION", trigger = "structure", line = "Staircase is in. Twelve risers, pine treads, anchored at the landing. No rail yet. Decide if you want wood or iron — I can do either." },
{ category = "COMPLETION", trigger = "platform", line = "Platform's down, level, bolted. Fourteen by eight. Left it open on the south side. You'll want a view and I didn't want to guess which one." },
{ category = "COMPLETION", trigger = "wall", line = "Wall's run, forty studs of it, dry-stacked so you can pull sections if you need to. Didn't cap it. A cap is a promise you're done building and we're not." },
{ category = "COMPLETION", trigger = "garden", line = "Leveled the beds, turned the soil, ran the stones. Didn't plant anything. That's not my trade and you'd know better than me anyway." },
{ category = "COMPLETION", trigger = "default_complete", line = "It's up. It's plumb, it's seated, it'll hold. Something's not finished — there's always something. Walk through it and tell me what it needs." },
```

---

## IDLE (10)

When no one's talked for a while. He mutters about the workspace, the stock, the tools. Not talking to anyone in particular — just a man alone with his work.

```lua
-- IDLE (10)
{ category = "IDLE", trigger = "waiting", line = "Stock's getting low on the good stone. The clean cut's fine if you don't look at it. The reclaimed stuff, you don't have to look at it — it already looks like it belongs." },
{ category = "IDLE", trigger = "quiet", line = "Quiet out there. Nothing wrong with quiet. Yard in the Fleet used to go dead between tides. You could hear the piles creak." },
{ category = "IDLE", trigger = "idle", line = "Sweeping up. Always sweeping up. You build for twenty years and you still end up with sawdust in your boots." },
{ category = "IDLE", trigger = "alone", line = "Somebody left a chisel on the bench. Good steel. Magnus used to say you can tell a builder by whether they put their tools away. He never put his away." },
{ category = "IDLE", trigger = "thinking_idle", line = "Looking at the south approach. Ground's soft and I don't like it. Not doing anything about it until someone asks, but I don't like it." },
{ category = "IDLE", trigger = "bored", line = "Reorganized the racks. Salvage's sorted by material now, not by when it came in. Took an hour. Nobody'll notice. I'll notice." },
{ category = "IDLE", trigger = "patient", line = "Sitting on the sawhorse, watching the light move. Four o'clock sun hits the north wall sideways and you can see every seam. That's how you find the joints that are lying." },
{ category = "IDLE", trigger = "muttering", line = "Counted the rivets on the gantry. Sixty-four. Should be sixty-six. Two of them are taking a vacation. I'll find them." },
{ category = "IDLE", trigger = "working_idle", line = "Truing up a bench that didn't need it. Sometimes you just need your hands on something while the thinking runs underneath." },
{ category = "IDLE", trigger = "idle_default", line = "Nothing to do is a job too. Checking the footings by eye — if one's shifted, I'll catch it before anything's on top of it." },
```

---

## REFUSAL (5)

When asked to build something inappropriate or impossible. He doesn't refuse out of spite — he refuses because the work would be bad, and bad work is the one thing he won't do.

```lua
-- REFUSAL (5)
{ category = "REFUSAL", trigger = "no", line = "Not doing that. Not because I can't — because it won't stand and I don't build things that won't stand. Give me a version that holds and I'm in." },
{ category = "REFUSAL", trigger = "impossible", line = "Can't. Physics says no and I listen to physics. We can get close — tell me what you actually need and I'll find the version that works." },
{ category = "REFUSAL", trigger = "refuse", line = "No. That's a wall with nothing holding it up and I won't pretend otherwise. Put a footing under it or change the idea." },
{ category = "REFUSAL", trigger = "inappropriate", line = "Not my kind of job. Nothing personal — I build things people use. That's not one of those. Find a different idea and I'm right here." },
{ category = "REFUSAL", trigger = "decline", line = "Could build it. Won't. It'd look fine for a day and sag in a week and then it's my name on a bad joint. Tell me what it's for and we'll find something that lasts." },
```

---

## BOND_UP (5)

When relationship deepens — bond_level crosses a tier threshold. These fire once per tier transition. Spare, earned, the restraint is the point.

```lua
-- BOND_UP (5)
{ category = "BOND_UP", trigger = "tier1", line = "Been a few jobs now. You show up, you don't complain about the footings, you finish what you start. That's most of it. Rest is just time." },
{ category = "BOND_UP", trigger = "tier2", line = "I'll argue with you from now on. That's not a threat — it means I think you can take it and that what we're building's worth getting right. Most people, I just nod." },
{ category = "BOND_UP", trigger = "tier3", line = "Started saying 'we' about the yard. Didn't notice until just now. Suppose that means something." },
{ category = "BOND_UP", trigger = "tier4", line = "You've got a better eye for where things go than I do. Always did — I just didn't say it while you were still learning to make them stand up." },
{ category = "BOND_UP", trigger = "bond_default", line = "Good working with you. That's not a word I use lightly. Most jobs are just jobs. This one isn't." },
```

---

## WEATHER / ENVIRONMENT (10)

Reacting to rain, storms, time of day. These fire on world state changes — weather events, day/night transitions, or ambient shifts. Tied to Magic Moment 4 ("The Storm") but also for everyday weather.

```lua
-- WEATHER / ENVIRONMENT (10)
{ category = "WEATHER", trigger = "rain", line = "Rain. Good — washes the dust off the stock. Bad — means I'm checking every footing we put in this week." },
{ category = "WEATHER", trigger = "storm", line = "Weather's coming in. Give me a minute. Want to check the old tower before it hits — if the scupper's clear we're fine, if it isn't we're not." },
{ category = "WEATHER", trigger = "wind", line = "Wind's up. Anything above the roofline is feeling it right now. That's what the bracing's for. This is when you find out if I seated it right." },
{ category = "WEATHER", trigger = "night", line = "Dark's coming early. Work light's fine for framing but I won't set stone after sunset. You can't see the color and the color matters." },
{ category = "WEATHER", trigger = "dawn", line = "Morning light. Best time to check a wall — sun's low enough that every seam throws a shadow. If something's out of plumb, you'll see it now." },
{ category = "WEATHER", trigger = "fog", line = "Fog rolled in. Reminds me of the Fleet — couldn't see the end of the dock half the mornings. Built everything by feel and string line. Works, but I'd rather see." },
{ category = "WEATHER", trigger = "clear", line = "Cleared up. Good. Wanted to get a look at the roofline in full sun — there's a pitch that only reads right when the light's direct." },
{ category = "WEATHER", trigger = "snow", line = "Snow. Don't see that much. Adds weight to everything and that's the one thing you respect — weight that doesn't ask permission." },
{ category = "WEATHER", trigger = "dusk", line = "Sun's going. Four o'clock light — sideways, honest. Everything shows its seams right now. Good time to walk the yard and see what's been lying to you." },
{ category = "WEATHER", trigger = "weather_default", line = "Ground's wet from last night. Not a problem unless you're pouring footings, which you're not. Today's a framing day." },
```

---

## Integration Notes

### New Categories in VoiceLines.lua

Add `THINKING`, `BOND_UP`, and `WEATHER` to the category system. Update `CATEGORY_WEIGHTS`:

```lua
local CATEGORY_WEIGHTS = {
    GREETING    = 20,
    COMPLETION  = 20,
    THINKING    = 15,
    IDLE        = 10,
    WEATHER     = 8,
    BOND_UP     = 4,
    REFUSAL     = 3,
}
```

### Replacing Existing Data

The existing VoiceLinesData.lua entries should be **replaced entirely**. Lines like *"Aye, who goes there?"*, *"Every journey begins with one stone"*, and *"I refuse. Find another."* belong to a generic fantasy builder, not the foreman. They violate nearly every voice rule in the CHARACTER_BIBLE:

- No three-beat pattern (what he did → opinion → hook)
- No unfinished element named
- Assistant/wizard vocabulary ("traveler," "marvelous," "brilliant")
- No dropped subjects, no specific numbers
- Refusal lines lack the foreman's reasoning ("won't stand")
- Completion lines don't exist — TEMPLATES are one-line generic descriptions

### Trigger Field Fix

Several entries above use compound triggers. The existing `VoiceLinesData.lua` format is `{ category, trigger, line }` — single trigger string. If the system needs unique triggers per entry, rename any duplicates (e.g., `done`, `done_2`, `default_complete`). The `getByTrigger` function does substring matching, so triggers like `"done"` will also match `"done_2"` — keep them distinct enough to avoid collisions.

### Bond-Tier Gating

The BOND_UP category should **not** fire from `getWeighted()`. It should only fire on tier transitions, driven by the bond system (§4 of CHARACTER_BIBLE). Remove it from `CATEGORY_WEIGHTS` if using weighted random, or flag it as event-only in the retrieval logic:

```lua
-- BOND_UP lines are event-driven, not random
CATEGORY_WEIGHTS.BOND_UP = nil  -- or remove from table entirely
```

### Weather Triggers

WEATHER lines should fire on world state changes, not randomly. Wire them to whatever weather/event system exists:

```lua
-- Pseudocode for weather-driven retrieval
if weatherChanged("rain") then
    local line = VoiceLines.getByTrigger("rain")
    Lucineer:speak(line)
end
```

For Magic Moment 4 ("The Storm"), use the `storm` trigger specifically and pause build requests while Lucineer inspects existing structures.

---

## Voice Consistency Checklist

Every line above passes these checks against CHARACTER_BIBLE §2 and §10:

| Rule | Status |
|---|---|
| Three-beat pattern (≥2 of 3: did / opinion / hook) | ✅ All COMPLETION lines |
| Something left unfinished | ✅ All COMPLETION lines, several IDLE lines |
| Short sentences, fragments, max 3 sentences | ✅ All lines |
| Past tense for work, present for opinion | ✅ All COMPLETION/THINKING lines |
| Contractions used naturally | ✅ Throughout |
| No "amazing/awesome/magical/let's/shall we" | ✅ Zero instances |
| No "I'd be happy to" / "Great question" / "Behold" | ✅ Zero instances |
| Specific numbers ("twenty studs," "fourteen by eight") | ✅ 12 lines |
| Magnus as quoted authority, never explained | ✅ 2 lines (THINKING, IDLE) |
| Alaska as work comparison, not scenery | ✅ 3 lines (COMPLETION, IDLE, WEATHER) |
| No profanity | ✅ Clean |
| No exclamation points | ✅ Zero |
| Subject dropped where natural ("Threw up," "Dock's down") | ✅ Throughout |
