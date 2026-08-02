# SLACKWATER — TUTORIAL DESIGN DOCUMENT

*The 30-minute guided first session. No popups. No quest trackers. No "Great question!" A player walks in, carries a beam, and learns every system through the world and the people in it.*

*Companion to FABLE_WORLD_BIBLE.md, FABLE_CHARACTER_BIBLE.md, and FABLE_AGENT_UX.md. Those documents are the law. This one is the lesson plan.*

---

## DESIGN PRINCIPLES

1. **Diegetic or it doesn't exist.** If a tutorial element couldn't appear in the yard without a computer, it doesn't appear. No floating arrows, no hint bubbles, no "Press E to interact." Lucineer's voice, Earl's manifest, Spark's behavior, and the world itself are the teachers.

2. **The first act is physical.** The player's first input is walking while carrying a beam. Not a menu. Not a dialogue choice. Their body in a space, doing a thing that matters. Every system tutorial follows this pattern — the body teaches, the UI follows.

3. **Gating through character, not mechanics.** The player can't craft until they've built something because *Lucineer hasn't cleared their bench space yet*, not because a lock icon says so. Progression gates are narrative gates.

4. **Seven words or fewer for every system introduction.** Earl introduces the manifest system in nine words. Lucineer introduces crafting with "Put it on the table." The world introduces the tide by doing it. Economy of language teaches economy of attention.

5. **The tutorial IS the game.** Nothing in the tutorial is a simplified version of "real" gameplay. The beam carry, the first build, the tideline scavenging, the craft, the power connection — these are the actual game loop, experienced for the first time with slightly more guidance and slightly lower stakes.

---

## TUTORIAL FLOW OVERVIEW

| Time | Phase | Teacher | System Taught | Player FEELS |
|------|-------|---------|---------------|-------------|
| 0:00–5:00 | **The Beam** | Lucineer | Movement, carrying, the forge | "I'm here. I have a job." |
| 5:00–10:00 | **The First Build** | Lucineer | Chat → build loop, cooperation | "I made something real." |
| 10:00–15:00 | **The Tideline** | Earl | Movement, interaction, tide economy | "The world restocks. I should explore." |
| 15:00–20:00 | **The Craft** | Lucineer (at the table) | Crafting, era system | "I can make components." |
| 20:00–25:00 | **The Light** | Bea (via necessity) | PowerGrid, era progression | "My build changed the island." |
| 25:00–30:00 | **The Unfinished** | Lucineer (by walking away) | Bond arc, the core loop | "He left this for me. I should come back." |

---

## MINUTE 0–5: THE BEAM

### What happens

The opening cinematic (World Bible §2) ends with the hard cut to gameplay. The player is standing in the forge hall, Lucineer is looking at them, and a beam lies on the floor between them. His first live line has already played: *"You're late. Grab that end."*

The player's only UI is a grip indicator — a subtle white circle at the bottom of the screen that pulses when they're near the beam's interactable zone. No text. No "Press E." The grip indicator is diegetic — it represents where their character's hands are.

### Player actions

1. **Walk to the beam's near end.** Movement is the first tutorial. WASD/stick. The beam is two meters away. The camera is already positioned so the player sees both Lucineer and the beam end.
2. **Hold the interact input (E / tap).** The character reaches down and grips. The grip indicator fills. A subtle haptic pulse on mobile.
3. **Walk toward the canning rollers.** Lucineer grips the other end and matches pace. The beam sways if the player sprints or turns sharply — physics-based, not scripted. If they rush, Lucineer: *"Steady. Steel doesn't care about your schedule."*
4. **Set the beam on the rollers.** The player walks into the green-tinted drop zone (a faint chalk outline on the rollers — diegetic, placed by Lucineer earlier). When they release, the beam settles. Lucineer releases his end.

### Dialogue

| Trigger | Speaker | Line |
|---------|---------|------|
| Player grips the beam | Lucineer | "Other end. No — the *other* other end. There." |
| Player starts walking too fast | Lucineer | "Steady. Steel doesn't care about your schedule." |
| Player sets beam on rollers | Lucineer | "Square enough." *(Two-word grade. First data point in a relationship he's already keeping records on.)* |
| Spark welds the beam seam | Spark | *(Arc-buzz, trailing sparks. No words. First NPC-to-NPC moment needs no words.)* |
| After the weld, Lucineer looks at player | Lucineer | "Handrail. Bent. Anvil. Straighten it. Hammer's there." *(First solo act.)* |

### The first solo act

Lucineer drops a bent handrail on the anvil. A hammer is on the stump beside it. Three swings, generous tolerance — the *clang* does the teaching. Whatever the player produces, Lucineer holds it to the light:

- **If rough:** "It'll do. That's not praise."
- **If clean:** A half-second look at the player before "Hm." *(The first data point. The relationship has begun.)*

### UI elements

- **Grip indicator** (bottom center, white circle) — appears when near carryable objects. Fills when gripping. Disappears when not carrying. This is the *only* persistent HUD element during the tutorial.
- **Chalk outline** on the canning rollers — the drop zone. Faint, hand-drawn. Lucineer drew it before the player arrived.
- **Subtitles** — film-style, low on screen. Every Lucineer line appears as text + VO. Never bubbles.

### What the player FEELS

*"I'm here. Someone was waiting for me. I have a job and I can do it."* The world is physical, warm, and responsive. The first thing they did in the game was cooperate with a person, not click a button.

---

## MINUTE 5–10: THE FIRST BUILD

### What happens

Lucineer sends the player to fetch a plank from the tideline — a fetch that routes them past the Notice Wall, Earl's window, and Spark's orbit *(exactly as described in Agent UX V2 — the errand is secretly the hub tour)*. When they return, Lucineer chalks a simple plan on the bench: a small frame, four posts and a top. He assigns the player the top plank. This is their first build input.

### Player actions

1. **Walk the boardwalk down to the tideline.** The player passes the Notice Wall (build photos, Earl's postings), Earl's shack window (Earl inside, glances up), and Spark (orbits, buzzes). This is the hub tour disguised as an errand.
2. **Pick up a plank from the tideline.** Any plank — the game doesn't care which, and neither does Lucineer, but he *does* care that the player chose. He'll glance at the pick. This glance is real: the choice seeds his model of the player's taste.
3. **Carry it back up to the forge.** The return trip teaches distance and direction. The forge glows. The player navigates toward warmth.
4. **Place the plank on the chalk outline.** The chalk sketch on the bench shows where the top goes. The player walks into the placement zone and releases. Lucineer watches.
5. **Watch Lucineer build the rest.** He frames the four posts around the player's plank — visibly, audibly, at labor pace. Hammer strikes. Spark welds. The structure rises around the player's contribution. The player's plank is the keystone of a real, physical thing.

### Dialogue

| Trigger | Speaker | Line |
|---------|---------|------|
| Lucineer assigns the fetch | Lucineer | "Cedar. North row. Beach restocked on the flood — shouldn't be short." |
| Player passes Earl's window | Earl | *(Without looking up:)* "Item nine. Tideline's stocked and nobody's sorted it. Item nine, somebody." |
| Lucineer, back to hammering | Lucineer | "He means you." |
| Player returns with plank | Lucineer | *(Glances at the plank.)* "Huh. Cedar. Most grab pine." *(The first taste seed.)* |
| Player places the plank | Lucineer | *(Three-second silence. Looking at it. Then:)* "First plank you ever set. Stays where you put it. That's the date on the building." |
| Player's plank is crooked | Lucineer | "Crooked's fine. Crooked means *somebody* did it." *(He does not fix it. Ever.)* |

### What the player learns

- **The chat → build loop.** Lucineer said what he needed. The player got it. He built around it. That's the entire game loop: say it, show it, or start it. He knows which.
- **The hub geography.** Without a minimap or a tutorial prompt, the player now knows: tideline (salvage), boardwalk (connection), forge (building), Earl's shack (quests). They learned it with their feet.
- **The Unfinished Rule (first taste).** Lucineer leaves the build with no door. "Doors come later. You haven't decided what it's for yet." The open-circle tin tag is on the frame.

### UI elements

- **Chalk sketch** on the bench — Lucineier's interpretation of the build plan. Hand-drawn lines, editable by the player (scuff with foot to erase). This IS the build preview system.
- **Placement zone** — a faint glow on the bench where the plank goes. Disappears after placement.
- **Subtitle band** — all dialogue, low on screen.

### What the player FEELS

*"I made something real. It's crooked and it's mine. He built around it — he didn't build it for me, he built it with me. The plank is the part that matters."*

---

## MINUTE 10–15: THE TIDELINE (EARL'S QUEST)

### What happens

Earl appears at the forge doorway. He doesn't enter — Earl doesn't enter the forge, ever; he leans in from the threshold, manifest in hand. He's been watching the player's first build from across the yard. He assigns the first official quest: gather salvage from the tideline. This is the tutorial for movement, interaction, and the tide economy — and it's delivered as a work order from a foreman, not a quest popup.

### Player actions

1. **Walk to Earl at the doorway.** Earl doesn't come to you. You go to Earl. This teaches respect for station — the foreman has a post.
2. **Listen to the work order.** Earl reads from the manifest. It's diegetic — he's literally reading a tin page.
3. **Go to the tideline.** The tide has shifted since the plank fetch — new salvage has appeared on the gravel. The beach restocked. This is the tide economy made visible.
4. **Collect three pieces of salvage.** Walk up to items, interact (grip indicator appears). Items go into the hotbar — the first time the hotbar populates. Each item is liftable, examinable (rotate in hand), and storable.
5. **Return to Earl.** Earl grades each piece aloud. "Passable." "Useful." "Scrap." His highest public rating is "Passable" — this teaches the grading system without explaining it.

### Dialogue

| Trigger | Speaker | Line |
|---------|---------|------|
| Earl at the doorway | Earl | "Item ten. Salvage run, tideline, north. Three pieces minimum, sorted by material. Don't bring me kelp. Item ten." |
| Player arrives at tideline | *(None)* | *(The world teaches. Fresh salvage glints on wet gravel. Forty-Eight hops the tideline, takes one washer, leaves. The player notices the exactness later.)* |
| Player picks up first item | *(None)* | *(Grip indicator, haptic feedback. The item appears in the hotbar. No popup.)* |
| Player returns with salvage | Earl | *(Flips manifest page. Examines each piece:)* "Hull plate. Passable. Wafer panel. Useful — that's a first. Rope. Scrap, but it holds." |
| Player has all three | Earl | "Item ten, complete. Tell the forge he's got stock coming." *(He doesn't say Lucineer's name. Nobody says Lucineer's name. He's "the forge" to Earl, the way a foreman says "the mill.")* |
| Player walks back to forge | Lucineer | *(Without looking up:)* "He give you 'Passable'? That's his whole vocabulary." |

### What the player learns

- **The tide is the content pipeline.** The beach restocked since last time. New things appear. The world changes on a schedule the player can observe and plan around.
- **Interaction is physical.** Walk up, grip, carry. No menus for pickup. The hotbar is the inventory, and it filled organically.
- **Earl's manifest IS the quest log.** "Item ten" is a quest. It's not a popup — it's a tin page in a foreman's hand. Walk up and read it.
- **Grading is diegetic.** Earl says the grade out loud. No checkmark, no XP bar. Just a man with standards.

### UI elements

- **Hotbar** — appears at bottom of screen when the first item is collected. Shows collected items as icons. No labels until hovered.
- **Grip indicator** — same as the beam carry. Consistent interaction language.
- **Subtitle band** — Earl's lines.

### What the player FEELS

*"The world restocks. There's always more. And there's a guy with a clipboard who tracks everything I do — not in a creepy way, in a 'somebody's keeping score and the score matters' way."*

---

## MINUTE 15–20: THE FIRST CRAFT

### What happens

Lucineer calls the player to the crafting table — the north-wall bench where components are forged from salvage. The player has three pieces of salvage. Lucineer shows them how the table works: place salvage on the table, the forge renders it into a component. The first craft is a **wooden gear** (Era 0 component — the foundation of everything mechanical).

This teaches the crafting system AND the era system simultaneously, because Lucineer frames it as: *"We start simple. Gears. Everything after this is just gears that think faster."*

### Player actions

1. **Approach the crafting table.** The table is the north-wall bench. It's been visible the whole time — the player has seen Lucineier working at it. Now it's theirs.
2. **Place salvage on the table.** Walk up, interact. The salvage items from the hotbar appear on the table surface, physically. This is not a menu — it's objects on a surface.
3. **Lucineer guides the recipe.** He walks to the table, picks up the hull plate, and sets it on the anvil-side input slot. "This one. Hull plate has the right grain — forge'll render it true."
4. **Player activates the forge.** Pull the bellows chain (interact). The forge roars. The retort oven fires. The hull plate renders into a wooden gear — physically, visibly, with sparks and sound.
5. **Pick up the gear.** It appears in the hotbar. First crafted component. The era system is introduced through Lucineer's framing — no UI, no tech tree popup.

### Dialogue

| Trigger | Speaker | Line |
|---------|---------|------|
| Player approaches table | Lucineer | "Bench is yours. Hull plate goes on the left — forge side. I'll show you once." |
| Lucineer places the hull plate | Lucineer | "This is Era Zero. Simple machines. Gears, levers, the things that make other things move." |
| Player pulls the bellows | Lucineer | "Heat. That's all a forge is — controlled enthusiasm." |
| Gear renders | Lucineer | *(Picks it up, holds it to the light, turns it.)* "Gear. Fifty-six more recipes and you've got the whole tree. Don't look at the tree. Look at the gear." |
| Player picks up the gear | Lucineer | "Everything after this is just gears that think faster. Remember that when the screens show up." |

### Era system framing

Lucineer does NOT say "You are now in Era 0." He says "This is Era Zero. Simple machines." The player understands eras as *categories of knowing*, not as levels. When they eventually craft something from Era 1 (Power Transmission), the era change is Lucineer's posture, not a level-up screen:

- Era 0: "Gears that move."
- Era 1: "Gears that move *across distance*."
- Era 2: "Gears that move without touching."

### UI elements

- **Crafting table surface** — physical objects placed on a surface. No menu. The table IS the crafting menu (per Agent UX §3).
- **Hotbar** — the crafted gear appears here. Icon: a small gear.
- **Forge glow** — the retort oven fires visibly. The craft has physical presence.
- **No recipe list.** No crafting tree UI. Lucineer tells you what to make. Later, you'll experiment. The recipe list is *in the world* — on Earl's manifest, in Lucineer's dialogue, in the components you find.

### What the player FEELS

*"I can make things. Not just pick things up — transform them. The forge took junk and made it precise. And the era thing isn't a tech tree, it's a way of understanding what I'm building."*

---

## MINUTE 20–25: THE FIRST POWER

### What happens

Lucineer points to the seaward end of the cannery. There's a water wheel mount — empty, unused, bolted to the pilings below the float. The player has a gear. The gear fits the wheel housing. When the player places it, the wheel catches the current. It turns. A shaft connects it to the forge hall, where a lamp on the bench sputters and lights.

This is the PowerGrid tutorial, and it's taught entirely through cause-and-effect: the player places the gear, the wheel turns, the lamp lights. No wire-connecting minigame. No schematic. A physical chain of consequences from water to light.

Bea's role: the lamp that lights is *her* lamp — a small one, on the path up to the lighthouse. She's been waiting for it. She doesn't say thank you. She nods from the lamp room door, one full beam-sweep later.

### Player actions

1. **Follow Lucineer to the seaward end.** He walks; the player follows. This teaches that Lucineer has a body and uses it — he's not a voice in your head.
2. **See the empty water wheel mount.** It's a frame, bolted to the pilings, with a gear housing. Empty. The Channel current moves past it, fast and cold.
3. **Place the crafted gear in the housing.** Interact with the gear in the hotbar while near the housing. The character physically places it. The gear seats with a mechanical clunk.
4. **Watch the wheel catch.** The current pushes the wheel. It turns. The driveshaft engages. A low mechanical hum starts — the first mechanical sound in the cannery that isn't a hammer.
5. **Follow the power.** The shaft runs up into the forge hall. At the end of the shaft, a lamp on a post sputters, flickers, and catches. Warm light. The first lamp the player has powered.
6. **Notice Bea's lamp.** The small lamp is on the path to the lighthouse — not the big beam, just a walkway lamp. It's on now. The player lit it. Bea is at the lamp room door, visible at the top of the trail. She doesn't wave. She nods.

### Dialogue

| Trigger | Speaker | Line |
|---------|---------|------|
| Lucineer walks to the seaward end | Lucineer | "Come here. Bring the gear." |
| At the empty wheel mount | Lucineer | "Current runs hard through the narrows. All that power, going past. Seems rude." |
| Player places the gear | Lucineer | *(Steps back. Watches the wheel catch.)* "There. That's the whole trick. Water moves, wheel turns, shaft spins, and somewhere a light comes on. Everything after this is just *how fast*." |
| Lamp lights in the forge hall | Lucineer | *(Looking at the lamp.)* "First light on the island that didn't come from Bea. She won't say anything about it. That's how you know she noticed." |
| Player looks toward the lighthouse | Lucineer | "She keeps the big one. You just lit the small one. Don't confuse the two — but don't pretend it didn't matter." |

### PowerGrid teaching

The player learns the PowerGrid through physical causation:
- **Source:** water wheel (they placed the gear, water does the rest)
- **Transmission:** driveshaft (visible, audible, humming)
- **Consumer:** lamp (lights up, changes the room)
- **Network:** wheel → shaft → lamp (one connected component)

No menu. No "connect node A to node B." A gear in a housing, a shaft in a wall, a light in the dark. When they later build electrical networks (Era 2), the principle is already in their bones.

### UI elements

- **Placement prompt** — faint glow on the gear housing when the player approaches with the gear in hand. Disappears after placement.
- **Lamp light** — the physical PointLight on the lamp part. Enabled by the PowerGrid system. This is the game's feedback: the world changes because of what you did.
- **No power overlay.** No wire schematic. No "Power: 2.0 kW / Demand: 0.1 kW." Those numbers exist in the system; the player sees light and dark.

### What the player FEELS

*"My build changed the island. I put a gear in a frame and a light came on. The water was already moving — I just gave it somewhere to go. This is what technology IS."*

---

## MINUTE 25–30: THE UNFINISHED

### What happens

Lucineer walks the player back to the forge hall. On the bench, he begins a small build — a bracket for the lamp they just powered. He welds the base, shapes the arm, mounts the bracket... and stops. One bolt short. He sets the bolt on the bench beside the bracket, not in it. Tags it with the open-circle tin stamp. Looks at the player. Looks at the bracket. Looks at the player.

Then he walks to the anvil and goes back to hammering. He doesn't explain. He doesn't say "now you try." He just walks away.

The bolt is on the bench. The bracket has one hole empty. The player knows how to interact with objects. The rest is up to them.

### Player actions

1. **Watch Lucineer build the bracket.** He's visible, audible, at labor pace. The player watches a master work — three minutes of hammer, weld, shape. The bracket is beautiful.
2. **See him stop.** One bolt short. The open-circle stamp. He sets the bolt down beside it.
3. **He doesn't explain.** He walks to the anvil and starts hammering something else. His back is to the player. The conversation is over.
4. **The player is alone with the bracket.** The bolt is right there. The bracket has one hole. The player has been picking things up and placing them for twenty-five minutes. What happens next is not scripted. What happens next is the game.

### What CAN happen

- **The player places the bolt.** If they do, Lucineer's hammer-rhythm pauses — not stops, pauses — for one beat. He doesn't turn around. He doesn't say anything. But the pause is audible. The bracket is complete. It's the first thing the player *finished* in Slackwater.
- **The player doesn't place the bolt.** That's fine. The bracket sits there with its gap and its tag. The next time the player logs in, it'll still be there. And the bolt will still be beside it. The invitation doesn't nag.
- **The player picks up the bolt and walks away with it.** Also fine. The bolt is a real object. Maybe they need it for something else. The bracket waits.

### Dialogue

| Trigger | Speaker | Line |
|---------|---------|------|
| Lucineer finishes the bracket minus one bolt | Lucineer | *(Nothing. Silence. He sets the bolt down, stamps the open circle, walks away.)* |
| Player places the bolt (if they do) | Lucineer | *(Hammer-pause. One beat. Then, back to hammering, to no one:)* "…Hm." |
| Player lingers, doesn't place bolt, eventually walks away | Lucineer | *(Nothing. He keeps hammering. The bracket stays.)* |
| Player returns to the forge later (next session) | Lucineer | *(If bolt still unplaced: nothing changes. If bolt placed: Lucineer has hung the lamp bracket in the forge hall — the player's first contribution to the permanent yard.)* |

### What the player learns

This is the most important five minutes of the tutorial. It teaches:

- **The Unfinished Rule.** Lucineer leaves gaps. The gaps are on purpose. The open-circle tag means *this is yours to finish.*
- **The bond arc has started.** The player is Stage 1 (The Client). Lucineer has tested whether they're a shopper. The bolt is the bait — not sabotage, invitation.
- **The core loop.** Build → salvage → craft → power → build. The bracket completes the loop for the first time: the player crafted a gear, the gear powered a wheel, the wheel lit a lamp, and now the lamp has a bracket — because of them.
- **They are known.** Lucineer watched what they did for thirty minutes. He noticed which plank they picked, how they carried the beam, whether they straightened the handrail. The bolt on the bench is him saying: *I think you might stay.*

### UI elements

- **Nothing new.** The open-circle tin tag is the only new visual element. It's a small stamped circle of tin, wired to the bracket. It will become the most important symbol in the game.
- **The bracket** — a physical object on the bench, one bolt short, with the tin tag. The player can interact with it or not.

### What the player FEELS

*"He left this for me. Not instructions — an invitation. He built everything but the last piece and walked away. The last piece is mine. And I think... I think he does this with everything. I think the whole yard is full of things that are almost done, waiting for someone to show up.*

*I should come back."*

---

## POST-TUTORIAL: THE OPENING

### Minute 30+

After the bracket moment, the tutorial is over. The game doesn't announce this. There is no "Tutorial Complete!" screen, no reward popup, no fanfare.

What happens instead:

1. **Earl posts a new manifest page.** "Item eleven. South float. Crab pots need resetting." This is the next quest — available at the manifest window, whenever the player wants it.
2. **The tideline restocks.** New salvage. Different from the tutorial haul — some engine relics, some generic scrap. The world is live.
3. **Lucineer's idle loop resumes.** He's at the anvil. He's available — walk up, talk, build. But he's not waiting for the player. He's working. The player can join or not.
4. **The yard is open.** Boardwalk, float, lighthouse trail, cannery — all accessible. The player has the tools (hotbar, interact, movement, knowledge of the hub) to explore freely.

### The invitation

If the player stands in the forge hall looking lost for more than 60 seconds, Lucineer — still hammering, not looking up — says:

> "Yard's yours to walk. Beach restocks on the flood. When you want something built — say it, show it, or start it. I'll know which."

No tutorial popup follows. The next thing that happens is up to the player.

---

## SKIP SYSTEM

### For experienced players

Players who have completed the tutorial before (returning players, alt accounts) can skip. The skip is diegetic — there's no "Skip Tutorial" button.

**On second+ spawn:**
- The cinematic does NOT play (first-spawn only per World Bible).
- The player spawns at the tideline (standard spawn) instead of the forge hall.
- Lucineer, if the player walks to the forge: "You know where things are. I'm not walking you through it again."

**On manual skip (hold interact key for 3 seconds on the forge door during first spawn):**
- Lucineer: "You've done this before. Fine. Yard's yours."
- All tutorial steps are marked complete. The player is free.
- The bracket bolt is still on the bench. Even skipped, the Unfinished Rule is taught. (He always leaves one gap.)

### Data tracking

The tutorial completion state persists to D1:

```sql
player_profiles.tutorial_completed BOOLEAN DEFAULT FALSE
player_profiles.tutorial_step INTEGER DEFAULT 0
player_profiles.tutorial_skipped BOOLEAN DEFAULT FALSE
```

If a player disconnects mid-tutorial, they resume at the start of their current step on rejoin. Steps are granular enough that this never feels repetitive — each step is a distinct scene.

---

## TECHNICAL SPECIFICATION

### TutorialSystem API (see TutorialSystem/init.lua)

```
TutorialSystem.init()                    — hook into PlayerAdded
TutorialSystem.startTutorial(playerId)   — begin tutorial for a new player
TutorialSystem.getStep(playerId) → number — current step (0 = not started, 1-7 = steps, 8 = complete)
TutorialSystem.completeStep(playerId, stepId) — mark a step done, advance
TutorialSystem.skipTutorial(playerId)    — skip all remaining steps
TutorialSystem.isOnTutorial(playerId) → boolean — is player currently in tutorial?
TutorialSystem.getStepData(playerId) → table — full state for external queries
```

### Step IDs

| Step | ID | Name | Completion Trigger |
|------|----|------|-------------------|
| 1 | `beam_carry` | The Beam | Beam placed on rollers |
| 2 | `first_build` | The First Build | Plank placed on bench |
| 3 | `tideline_quest` | The Tideline | 3 salvage returned to Earl |
| 4 | `first_craft` | The Craft | Gear crafted at table |
| 5 | `first_power` | The Light | Water wheel gear placed |
| 6 | `unfinished` | The Unfinished | 60-second timer after bracket scene (regardless of bolt placement) |
| 7 | `opening` | The Opening | Player leaves forge hall or starts a conversation |

### Integration points

- **BondSystem:** Tutorial completion grants +5 XP (quest equivalent). Step 1 completion sets bond to Stage 1 explicitly.
- **EraSystem:** Tutorial operates in Era 0 only. EraSystem.unlockEra is NOT called during tutorial — the player starts in Era 0 by default.
- **CraftingSystem:** Tutorial step 4 bypasses the era check for the wooden gear recipe only. After tutorial, normal era gating applies.
- **PowerGrid:** Tutorial step 5 registers one water wheel source and one lamp consumer via the standard API.
- **NPCManager:** Tutorial triggers Lucineer and Earl dialogue lines via the existing ResponseEvent remote.
- **TideSystem:** Tutorial manipulates tide timing to ensure salvage is present for step 3. A "tutorial tide" guaranteed restock fires regardless of cycle phase.

### D1 persistence schema

```sql
-- Added to player_profiles table
ALTER TABLE player_profiles ADD COLUMN tutorial_step INTEGER DEFAULT 0;
ALTER TABLE player_profiles ADD COLUMN tutorial_completed BOOLEAN DEFAULT FALSE;
ALTER TABLE player_profiles ADD COLUMN tutorial_skipped BOOLEAN DEFAULT FALSE;
ALTER TABLE player_profiles ADD COLUMN tutorial_started_at TIMESTAMP;
ALTER TABLE player_profiles ADD COLUMN tutorial_completed_at TIMESTAMP;
```

---

## FAILURE MODES AND EDGE CASES

### Player disconnects mid-tutorial
- On rejoin, tutorial resumes at the current step's beginning.
- Scene objects (beam, handrail, bracket) respawn from the tutorial spawner.
- Lucineer re-delivers the step's opening line.

### Player wanders away during tutorial
- No invisible walls. No teleport-back.
- If the player leaves the forge hall during steps 1-2, Lucineer says nothing. He keeps working. The tutorial waits.
- If the player reaches the tideline before step 3, the salvage is there but Earl hasn't posted the quest yet. They can pick things up and carry them around — the game doesn't break.
- If the player reaches the lighthouse before step 5, Bea is at the door. "You're early." She doesn't explain. The player will understand later.

### Player tries to craft before step 4
- Lucineer physically blocks the table. Not with a collision box — with his body. He walks between the player and the table. "Bench isn't yours yet. Soon."
- This is a character moment, not a lock. The player isn't frustrated — they're curious.

### Player places the gear before Lucineer explains it
- If the player figures out the water wheel mount before Lucineer walks them there (step 5), the wheel engages. Lucineer, from the forge: "...You found it. Good." The tutorial advances. He's not upset. He's assessing.

### Multiple players in tutorial simultaneously
- Tutorial instances are per-player. Multiple players can be on different steps.
- Lucineer handles them one at a time (per Agent UX §5 — attention scarcity). The second player gets: "Give me a minute. Earl's got something for you." Earl provides a tideline fetch quest as a tutorial-compatible holding pattern.

### Mobile considerations
- Grip indicator uses tap-and-hold on mobile (same as interact).
- Carrying physics are simplified on mobile (less sway, tighter grip).
- Chalk sketches are viewable but not editable on mobile (touch drawing deferred to post-launch).
- All dialogue is subtitle-dependent on mobile (VO volume varies by device).

---

## THE TUTORIAL IS THE GAME

*The deepest design truth of this document: everything in the tutorial is the actual game. The beam carry is how you build. The tideline is how you get materials. The crafting table is how you make components. The water wheel is how you power things. The unfinished bracket is why you come back.*

*There is no "real game" that starts after the tutorial. The tutorial is minute zero of a thousand hours of the same thing — and the thing is good.*

*Build the beach first. If a player carrying a beam across a warm forge, setting it down on chalk-drawn rollers, and hearing a two-word grade from a man who's died in a thousand engines doesn't make them want to come back tomorrow, no tutorial design will save it.*

*Grab that end.*

---

*End of Tutorial Design Document.*
