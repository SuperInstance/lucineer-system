# NPC & Tutorial System Audit

**Date:** 2026-08-03  
**Auditor:** Game Systems Engineering (subagent)  
**Files reviewed:**
- `NPCManager/init.lua` (1,267 lines)
- `TutorialSystem/init.lua` (1,140 lines)
- `OnboardingSystem/init.lua` (1,719 lines)
- `FIRST_TEN_MINUTES.md` (design doc)

---

## 1. NPCManager — What It Does

### Functionality

NPCManager is **fully functional** as a standalone ambient-NPC system. It:

- **Spawns 5 NPCs procedurally** — Earl, Spark, Hermes, Bea, Forty-Eight — building each from raw `Instance.new()` parts (no pre-made models). Each has distinct geometry: Earl has a clipboard, Spark is a three-legged welding rig with a neon lens-eye, Bea has a watch cap and key ring, Forty-Eight is a raven with a machine-washer on its leg.
- **Runs behavior loops** per NPC: Spark patrols the forge welding at waypoints, Bea repositions deliberately every 60-120s, Hermes sways on deck, Forty-Eight hops a roofline patrol and crows at random intervals.
- **Handles ProximityPrompt interactions** for all interactive NPCs (Forty-Eight is ambient-only). Each interaction shows a `BillboardGui` chat bubble with cycling dialogue.
- **Earl has a quest cycle** — 5 quests that rotate on interaction, with title/description/reward displayed in the bubble.
- **All parts are Anchored** and movement is done via `TweenService`. No physics-based movement, no Humanoid walking. This is a deliberate simplification — NPCs don't pathfind, they tween between waypoints.

### Does it handle Lucineer as an NPC?

**No.** Lucineier is not among the 5 NPCs. The NPCManager handles only Slackwater Yard locals. Lucineier is presumably handled by the AI/Worker pipeline (chat-to-build system), not by NPCManager. This is correct — Lucineier should be AI-driven, not script-driven.

However, **NPCManager has no integration point for Lucineier.** It can't position Lucineier, can't animate him, can't coordinate with the AI pipeline for his movements. If Lucineier needs to walk to the seaward end during a tutorial step (as the OnboardingSystem script describes), there's no API for that. NPCManager is a closed system.

**Verdict:** Functional, well-built, but isolated. It's a good ambient-NPC system that doesn't know about the AI brain.

---

## 2. TutorialSystem — What It Does

### Functionality

TutorialSystem is a **7-step state machine** that tracks player progression through a 30-minute guided session:

| Step | ID | Description |
|------|----|-------------|
| 1 | `beam_carry` | Carry beam to rollers |
| 2 | `first_build` | Place plank on bench |
| 3 | `tideline_quest` | Return 3 salvage to Earl |
| 4 | `first_craft` | Craft a wooden gear |
| 5 | `first_power` | Place gear in water wheel |
| 6 | `unfinished` | 60-second "deliberate gap" scene |
| 7 | `opening` | Player leaves forge or talks freely |

It includes:
- **D1 persistence** — saves/loads tutorial step via the Worker relay
- **Player join/leave hooks** — auto-resumes mid-tutorial, auto-starts for fresh players after 62-second cinematic
- **Gating** — blocks crafting access until step 4, power access until step 5
- **RemoteEvent setup** — `TutorialEvent` (server→client) and `TutorialActionEvent` (client→server) for step state and triggers
- **Dialogue delivery** — sends lines through `ResponseEvent` (the main chat handler) with fallback to `TutorialRemote`

### Is it wired to the chat handler?

**Partially.** TutorialSystem fires dialogue through `ResponseEvent:FireClient()` with `type = "tutorial_dialogue"`. This means it's **sending to the client**, but it's not checking whether the AI brain/Worker is also trying to send a response at the same time. There's no coordination — no mutex, no priority system, no "tutorial overrides AI" flag.

If the player types something during step 3 and the Worker sends a Lucineier response via `ResponseEvent` at the same moment TutorialSystem sends Earl's grading line, **both messages arrive and likely overlap or confuse the client.**

### Does it conflict with Lucineier's AI-driven responses?

**Yes, by design gap.** The tutorial hardcodes Lucineier's lines (e.g., "You're late. Grab that end.") as static strings in `STEP_OPENING_LINES`. These bypass the AI brain entirely. Meanwhile, the Worker pipeline is presumably listening for player chat and generating Lucineier responses. Two scenarios:

1. **Player types during a tutorial step** → Worker generates a response → TutorialSystem also fires scripted dialogue → **collision**.
2. **Tutorial script fires Lucineier line** → Worker doesn't know a tutorial line was just delivered → may generate a contextually inappropriate response → **contradiction**.

The TutorialSystem doesn't send any "suppress AI" signal to the Worker pipeline. It doesn't flag the chat handler to stand down during scripted moments.

**Verdict:** Functional state machine with a critical integration gap. The scripting is sound but the multi-author problem (tutorial script vs. AI brain both driving Lucineier) is unaddressed.

---

## 3. OnboardingSystem — What It Does

### Functionality

OnboardingSystem is **TutorialSystem v2** — same 7 steps, same step IDs, same D1 schema, same gating logic, but with significantly more detail:

- **Full dialogue tables** — every line from TUTORIAL_DESIGN.md is encoded as a named table entry (`BEAM_DIALOGUE.opening`, `BUILD_DIALOGUE.assign_fetch`, etc.) with speaker tags. TutorialSystem only had one opening line per step.
- **Reactive dialogue** — responds to player behavior mid-step (e.g., `onBeamGripped`, `onBeamRush`, `onPlayerPassedEarlWindow`, `onPlankReturned` with cedar-vs-pine distinction). TutorialSystem has none of this.
- **Step-specific begin functions** — each step has a dedicated `beginBeamStep()`, `beginFirstBuildStep()`, etc. that delivers the right dialogue sequence with proper pacing (`task.delay` between lines).
- **Lost-player detection** — if a player stands idle in the forge hall for 60+ seconds after the tutorial, Lucineier says the invitation line again.
- **Skip system** — hold-interact for 3 seconds on the forge door to skip, with diegetic skip dialogue. TutorialSystem has `skipTutorial()` but no input mechanism.
- **Better state tracking** — tracks `handrailHits`, `beamRushed`, `lastReactiveAt` (anti-repeat cooldown), `lostTimer`, `skipHoldStart`.
- **Step timeframes** — annotates each step with its designed minute range (0-5, 5-10, etc.) for analytics.
- **Proper cleanup** — `cancelLostPlayerWatch()` on player leave and tutorial completion.

### Does it overlap with the other two?

**Almost entirely.** OnboardingSystem is a superset of TutorialSystem. It duplicates:
- The same 7 step IDs and names
- The same D1 persistence logic (identical URL, identical JSON shape)
- The same gating functions (`craftingGateOpen`, `powerGateOpen`, `tidelineActive`)
- The same RemoteEvent setup (`TutorialEvent`, `TutorialActionEvent`)
- The same `deliverLine()` function (sends via `ResponseEvent` with fallback)
- The same player join/leave hooks and auto-start logic

**And it partially overlaps with NPCManager** — OnboardingSystem expects NPCManager to handle Lucineier's movement (e.g., walking to the seaward end in step 5, building the bracket in step 6), but NPCManager has no Lucineier NPC and no API for controlling one. The OnboardingSystem comments say "(NPCManager handles Lucineier's movement)" but this is an unfulfilled contract.

**Verdict:** OnboardingSystem is the definitive implementation. TutorialSystem is an earlier draft of the same thing.

---

## 4. Conflicts and Redundancy

### Three systems, overlapping concerns

| Responsibility | NPCManager | TutorialSystem | OnboardingSystem |
|---|---|---|---|
| NPC spawning/positioning | ✅ (5 ambient NPCs) | ❌ | ❌ |
| NPC behavior loops | ✅ | ❌ | ❌ |
| Earl's dialogue | ✅ (cycling one-liners) | ❌ (Earl has scripted quest lines) | ✅ (Earl has full dialogue tables) |
| Tutorial state machine | ❌ | ✅ (7 steps) | ✅ (7 steps, same IDs) |
| D1 persistence | ❌ | ✅ | ✅ (identical) |
| Gating (craft/power) | ❌ | ✅ | ✅ (identical) |
| Dialogue delivery | BillboardGui bubbles | ResponseEvent | ResponseEvent (identical) |
| Lucineier as NPC | ❌ | ❌ | ❌ (but assumes one exists) |
| Scene object spawning | ❌ | ✅ (stub) | ✅ (stub, same) |

### The core conflict: two dialogue channels

NPCManager shows dialogue as `BillboardGui` chat bubbles attached to NPC models. TutorialSystem/OnboardingSystem send dialogue via `ResponseEvent:FireClient()` as structured messages. These are **two completely different delivery mechanisms** for NPC speech.

If Earl says something via NPCManager (ProximityPrompt interaction → bubble), and then the tutorial script fires an Earl line via `ResponseEvent`, the player sees a billboard bubble AND a subtitle/chat message from the same character. This is broken.

### The Lucineier conflict: scripted vs. AI

FIRST_TEN_MINUTES.md describes Lucineier as a fully AI-driven character — his responses are generated by the Worker pipeline, not hardcoded. But both TutorialSystem and OnboardingSystem hardcode Lucineier's tutorial lines as static strings.

This creates a split-brain Lucineier:
- **During tutorial steps:** Static lines ("You're late. Grab that end.")
- **Outside tutorial steps:** AI-generated lines via Worker pipeline
- **During tutorial steps if player types:** Both may fire simultaneously

### The Earl conflict: quest giver vs. scripted role

NPCManager gives Earl 5 cycling quests with reward text. OnboardingSystem gives Earl specific quest-assigning dialogue during step 3 (`TIDELINE_DIALOGUE.earl_assign`). If the player interacts with Earl via ProximityPrompt during step 3, they get NPCManager's cycling quest — not the tutorial's tideline quest. The two systems don't know about each other.

---

## 5. Production Recommendation

### Which system should own the first-ten-minutes experience?

**OnboardingSystem** should be the single owner of the tutorial/onboarding flow. Specifically:

1. **Delete TutorialSystem.** It's a strict subset of OnboardingSystem. Keeping both is a maintenance hazard — any change needs to be made twice, and if both are loaded, they'll fight over the same RemoteEvents and D1 endpoints.

2. **NPCManager should remain the ambient-NPC system** but yield to OnboardingSystem during tutorial steps. Concretely:
   - NPCManager should expose a `setInteractionEnabled(name, enabled)` API that OnboardingSystem calls during tutorial steps.
   - When interaction is disabled for an NPC, the ProximityPrompt is hidden and the behavior loop continues (ambient life doesn't stop).
   - When the tutorial needs Earl to deliver scripted dialogue, OnboardingSystem handles it via `ResponseEvent` — NPCManager's bubble system stands down for that NPC.

3. **OnboardingSystem should own ALL scripted Lucineier dialogue during the tutorial.** The Worker pipeline should receive a `tutorial_active` flag and either suppress entirely or route through a tutorial-aware response template.

### What's over-engineered

- **TutorialSystem** (the entire file) — delete it. It's a draft.
- **NPCManager's quest system** (Earl's 5 quests with rewards) — these are placeholder content that will be replaced by the AI-driven quest system. Keep the data tables for reference but don't ship them as the real quest loop.
- **OnboardingSystem's reactive dialogue system** — `onBeamRush`, `onPlayerPassedEarlWindow`, `onPlankReturned` with cedar-vs-pine branching. This is genuinely good design, but it requires client-side detection logic that doesn't exist yet. The hooks are ready; the client isn't. Don't build the client detection until you've validated the basic 7-step flow works end-to-end.

### What's actually needed

1. **One system** (OnboardingSystem) that tracks 7 steps and fires dialogue at the right moments.
2. **A suppression signal** to the Worker pipeline: "tutorial active, don't generate Lucineier responses for this player right now."
3. **An interaction-yield API** on NPCManager so tutorial dialogue and ambient dialogue don't collide.
4. **Client-side step triggers** — the `TutorialActionEvent` actions (`beam_placed`, `plank_placed`, `salvage_collected`, etc.) need client-side detectors. None exist yet.

---

## 6. Integration Plan — Wiring OnboardingSystem to the Brain/Worker Pipeline

### Phase 1: Suppression (prevent collisions)

**In the Worker relay (Cloudflare Worker):**

Add a `tutorial_context` field to the player state. When OnboardingSystem fires a scripted Lucineier line, it also sends a `POST /api/player/tutorial-signal` with:

```json
{
  "player_name": "playerName",
  "tutorial_active": true,
  "step": 3,
  "suppress_ai_until": 1234567890
}
```

The Worker checks this flag before generating a response. If `suppress_ai_until` hasn't expired, the Worker either:
- **Returns nothing** (player gets no AI response), or
- **Returns a context-aware acknowledgement** — e.g., Lucineier says "Earl's talking. Listen." (brief, in-character, acknowledges the tutorial NPC is speaking).

**In OnboardingSystem:**

After each `deliverLine()` call where `speaker == "Lucineer"`, fire the suppression signal:

```lua
local function deliverLine(playerName, lineData)
    -- ... existing delivery logic ...

    -- If Lucineier is speaking, suppress the AI pipeline briefly
    if lineData.speaker == "Lucineer" then
        suppressAIFor(playerName, duration or 10)
    end
end
```

### Phase 2: Tutorial-Aware AI Responses

Instead of fully suppressing the AI, make the Worker **aware of the tutorial context** so it generates appropriate responses:

Add `tutorial_step` to the Worker request payload:

```json
{
  "player_name": "playerName",
  "message": "what do i do",
  "tutorial_step": 3,
  "tutorial_step_id": "tideline_quest"
}
```

The Worker's system prompt includes:

```
The player is in tutorial step 3 (The Tideline). Earl has assigned them 
a salvage run. If the player asks what to do, remind them about the 
tideline. Do not introduce new concepts. Stay in the current step's scope.
```

This lets the player type freely during the tutorial while Lucineier stays on-script. The AI reinforces the tutorial rather than fighting it.

### Phase 3: Handoff to Free Play

When the tutorial completes (step 7 → step 8), OnboardingSystem sends:

```json
{
  "player_name": "playerName",
  "tutorial_active": false,
  "tutorial_completed": true
}
```

The Worker clears the tutorial context and Lucineier becomes fully AI-driven. This is the transition from FIRST_TEN_MINUTES.md §5 ("The Leave") to open play.

### Phase 4: NPCManager Yield

Add to NPCManager:

```lua
function NPCManager.setTutorialMode(enabled: boolean)
    -- When enabled, hide ProximityPrompts on Earl (and any NPC 
    -- the tutorial is actively scripting). Behavior loops continue.
    for name, model in pairs(npcs) do
        local prompt = model.PrimaryPart and model.PrimaryPart:FindFirstChild("NPCPrompt")
        if prompt then
            prompt.Enabled = not enabled
        end
    end
end
```

OnboardingSystem calls this at tutorial start:
```lua
if NPCManager then
    NPCManager.setTutorialMode(true)
end
```

And at tutorial completion:
```lua
if NPCManager then
    NPCManager.setTutorialMode(false)
end
```

### Phase 5: Client-Side Detectors

Build the minimal client-side scripts that fire `TutorialActionEvent`:

| Step | Client Detection | Action Fired |
|------|-----------------|--------------|
| 1 | Beam part enters roller zone | `{action: "beam_placed"}` |
| 1 | Player swings hammer at handrail ×3 | `{action: "handrail_done", quality: "rough"/"clean"}` |
| 2 | Plank part enters bench zone | `{action: "plank_placed", crooked: bool}` |
| 3 | Salvage part enters Earl's zone | `{action: "salvage_collected"}` (×3) |
| 4 | CraftingSystem fires gear recipe | `{action: "gear_crafted"}` |
| 5 | Gear placed in wheel housing | `{action: "power_connected"}` |
| 6 | Bolt placed in bracket | `{action: "bolt_placed"}` |
| 7 | Player exits forge hall region | `{action: "left_forge"}` |

These are simple `Region3` or `Touched` event detectors — not complex systems. Each is ~20 lines of client Lua.

---

## Summary

| Question | Answer |
|----------|--------|
| Is NPCManager functional? | ✅ Yes — spawns 5 NPCs, runs loops, handles interactions via BillboardGui |
| Does NPCManager handle Lucineier? | ❌ No — and it has no API for external control of an NPC |
| Is TutorialSystem wired to chat? | ⚠️ Sends via ResponseEvent but doesn't coordinate with the AI pipeline |
| Does TutorialSystem conflict with AI? | ✅ Yes — hardcoded Lucineier lines collide with Worker-generated responses |
| Is OnboardingSystem a duplicate? | ✅ Yes — it's a superset of TutorialSystem. Delete TutorialSystem. |
| What should own first-ten-minutes? | **OnboardingSystem** — with suppression signals to the Worker and a yield API on NPCManager |
| What's the biggest risk? | **Split-brain Lucineier** — tutorial script and AI brain both generating his lines without coordination |

### Recommended action items (priority order)

1. **Delete TutorialSystem** — OnboardingSystem replaces it entirely
2. **Add `tutorial_active` flag to Worker pipeline** — suppress or scope AI responses during tutorial
3. **Add `NPCManager.setTutorialMode()`** — yield Earl's interaction to OnboardingSystem during steps
4. **Unify dialogue delivery** — pick one channel (ResponseEvent or BillboardGui, not both)
5. **Build client-side step detectors** — the 8 actions listed in Phase 5
6. **Test end-to-end with one player** — validate the 7-step flow before adding reactive dialogue
