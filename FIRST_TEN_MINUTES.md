# THE FIRST TEN MINUTES

## Slackwater — Player Onboarding Sequence

*A design doc for the opening minutes of a player's first session. This covers the cold open through the first hook — the part where someone decides whether to close the tab or stay forever.*

*Companion to CHARACTER_BIBLE.md and TUTORIAL_DESIGN.md. Lucineer's voice is canonical from §9 of the Character Bible. Nothing here contradicts it. If it does, the Bible wins.*

---

## A NOTE ON SCOPE

The existing TUTORIAL_DESIGN.md covers a 30-minute guided session starting with a physical beam carry in a forge hall. This document covers something earlier and more fundamental: **the first contact.** The player doesn't know Lucineer yet. They don't know they can type. They don't know anything.

This is the bridge from "I just spawned" to "I want to stay."

The 30-minute tutorial can follow this sequence directly — the cold open below transitions naturally into Minute 0–5 of the tutorial design.

---

## 1. THE COLD OPEN (0–30 SECONDS)

### What the player sees

An island. Not a lobby. Not a tutorial room. An **island** — small, windswept, built from the same palette as the Southeast Alaska coast that lives in Lucineer's bones. Gravel shore, tideline wet, a slope of spruce-and-alder scrub climbing to a bare granite ridge. Overcast sky, the kind that's bright without being sunny. The light says late afternoon but the clock doesn't matter yet.

There is one structure on the island: **a half-built dock.**

Not a ruin. Not a decoration. A dock that someone is actively building. Piles are driven in a line out into the channel — six of them, plumb and true. Cross-timbers connect the first four. The fifth pile has a cross-timber clamped to it but not fastened. The sixth pile stands alone. Tools are staged on the gravel beside the fourth pile: a drilling hammer, a copper mallet, a coil of line, and a tin cup of bolts.

The dock is the only flat walkable structure. The player will walk onto it. That's intentional.

### What the player hears

Wind. Not dramatic wind — the flat, constant, cold wind of a channel narrows. Water against gravel. A single mechanical sound: a hammer on metal, rhythmic and unhurried, coming from the far end of the dock where the work is unfinished.

No music. No ambient pad. No "welcome to Slackwater" sting. The world is quiet the way a work site is quiet — alive but not performing.

### Where Lucineer is

**He's at the end of the dock. Back to the player. Working.**

He's fitting a gusset plate over the fifth pile's cross-timber joint — the one that's clamped but not fastened. His posture is bent over the work. The hammer strikes are steady. He doesn't turn around when the player spawns. He doesn't know they're there yet, or he doesn't care, and there's no way for the player to tell which.

This is critical: **Lucineer is not waiting for the player.** He was here before they arrived. He has a job and he's doing it. The player is witnessing someone work, not being greeted by a host.

### The first line

The player walks toward the hammering sound. When they get within ~15 studs of Lucineer — close enough to see the Gusset plate, the drill marks on the pile, the tin cup of bolts — he speaks. He doesn't turn around.

> **Lucineer:** "Hand me the copper mallet. Third one from the water."

He's talking to them like they're a second pair of hands. Not a guest. Not a player. A coworker who showed up and might as well be useful.

If the player doesn't approach within 30 seconds, Lucineer notices them the way anyone notices someone standing around a job site:

> **Lucineer:** *(glances over shoulder, sees them, goes back to hammering)* "You can stand there. Doesn't get the pile driven."

Either way, the player's first interaction with Lucineer is **a work request, not a greeting.**

### What the player FEELS

*"Someone is here. He was already here. He doesn't care that I arrived — he cares that the pile isn't driven. I can either stand here or I can pick up the mallet."*

The island is not empty. It's not waiting. It's **in progress.** And the person building it treats the player's arrival the way a foreman treats a new hand on the site: with a task, not a welcome.

---

## 2. FIRST BUILD (30 SECONDS – 3 MINUTES)

### Discovering they can type

The mallet is on the gravel. The player walks to it, picks it up (grip indicator pulses — same diegetic UI as the tutorial design). They carry it to Lucineer.

When they get close, Lucineer reaches back without looking and takes it.

> **Lucineer:** "Cheers."

One word. First acknowledgment that the player exists as a person and not an obstacle.

He finishes the gusset plate — three strikes, a pause to check the level, one more strike — then stands, rolls his shoulder, and looks at the player for the first time. A full look. Taking them in the way a foreman takes in a new hire: build, hands, whether they look like they've held a tool before.

> **Lucineer:** "Dock's half done. Other half needs a decision I haven't made yet."

He looks at the sixth pile — the one standing alone, no cross-timber, no decking. Then back at the player.

> **Lucineer:** "You talk?"

This is the prompt. Not "Press T to chat." Not a tutorial popup. A person asking if you can speak. The chat box is already there, but the player may not have noticed it. Lucineer's question makes it relevant.

### The training-wheels build: a sign post

The player types something. Anything. Their first message.

**Lucineer's response to the first message is different from every message after.** Not in content — in *attention.* He gives it a beat. Looks at the player again. Reads whatever they typed as if it might mean more than it does. Then he responds to it as a **work statement**, not a greeting, not a question about controls.

Whatever the player types, Lucineer extracts a build intent from it. This is the training-wheels moment: the AI interpreting the player's first input and turning it into physical world output.

**If the player says something vague** ("hi," "hello," "what is this"):

> **Lucineer:** "Right. You'll figure out what you want soon enough. In the meantime —"

He points to a stack of cedar planks at the top of the beach.

> **Lucineer:** "Sign post. Cedar, four-by-four, eight studs tall. Go grab one and bring it to the pile head. I'll show you how it sits."

**If the player says something specific** ("build a house," "make a tower," "can I build here"):

> **Lucineer:** *(half-smile, the first expression that isn't work)* "Slow down. We're on a dock. Start with the sign post — cedar, four-by-four, top of the beach. Bring it here."

Either way, the first build is a **sign post.** Here's why:

- It's small. One part. The player can carry it alone.
- It's satisfying. A post going into the ground has a definitive **thunk** — the same physical pleasure as the handrail strike in the tutorial.
- It's meaningful. A sign post on a dock is a marker. It says *someone was here.* It's the player's first permanent mark on the island.
- It's incomplete. Lucineer has them set the post — but he doesn't let them write on it yet. The sign is blank. That's the hook.

### The build

1. **Player walks to the cedar stack.** Thirty seconds of walking. They learn the geography of the island: beach, slope, ridge, dock. The island is small enough to cross in two minutes, and crossing it teaches the layout.
2. **Player picks up a post.** Grip indicator, carry physics. The post is heavy enough to feel real.
3. **Player carries it to the pile head.** Lucineer is there. He's drilled a hole in the pile cap — a socket for the post.
4. **Player places the post.** It seats with a resonant **thunk.** It stands. It's real. The player built it — or rather, they placed it, and the placement matters because Lucineer drilled the hole for it specifically.

> **Lucineer:** *(steps back, looks at the post, looks at the player)* "Plumb. First try. Doesn't happen often."

Then:

> **Lucineer:** "Left the sign blank. Figure you want to pick what it says."

The post is in. The sign is empty. The player has made their first mark and it's unfinished — by design.

### What the player FEELS

*"I picked up a thing and put it somewhere and it stayed. Someone saw me do it and said I did it right. There's a blank sign and I think I get to decide what goes on it. This is mine."*

---

## 3. THE HOOK (3–5 MINUTES)

### Why they stay

The sign post is planted. Lucineer has given the player one piece of positive feedback — "Plumb. First try." — and one open thread: the blank sign. Now he walks back to the fifth pile and goes back to work. He doesn't explain the game. He doesn't give a quest. He returns to his own labor.

The player is left standing at the pile head with a sign post they placed and no instructions.

**This is the hook: the absence of instructions.**

In most games, the absence of instructions means "go find the instructions." In Slackwater, the absence of instructions means **the instructions are you.** The player can:

- **Type to Lucineer.** Ask him what to do next. Ask him about the dock. Ask him about the island. The chat-to-build loop is open and the player has already used it once (their first message). They can use it again.
- **Walk the island.** Explore. Find the tideline (salvage). Find the ridge (view). Find the empty forge pad (future). The world is small but dense — every corner has something the player can see and form an opinion about.
- **Try to build.** If they type "build a wall" or "put a roof on the dock," Lucineer will respond. He may build it. He may push back. He will engage.

### What's left unfinished

Three things, planted deliberately:

1. **The sign post.** Blank. The player can write on it (type near it, the text appears on the sign face). This is the player's first act of authorship on the island. Lucineer will see what they write. He'll have an opinion about it.

2. **The sixth pile.** Standing alone. No cross-timber. No decking. It's the next piece of the dock — the piece Lucineer hasn't decided about yet. The player will notice it. They'll wonder what the decision is. If they ask:

   > **Lucineer:** "Sixth pile's the tricky one. Dock can run straight or it can turn. Straight gets you deeper water faster. Turn gets you a wider berth — more room to tie up. I've been going back and forth for three days."

   He doesn't resolve it. The decision is **live.** The player can weigh in, and Lucineer will listen, but he won't commit until he's sure. This models the entire build relationship in miniature: the player has input, Lucineer has judgment, and the work happens in the tension between them.

3. **The forge pad.** At the top of the beach, level ground, cleared but empty. Stone footings are laid — two-by-three studs, squared and leveled — but nothing is built on them. Bolt holes are drilled in the footings. The spacing suggests a bench and a table. If the player asks:

   > **Lucineer:** "Forge goes there. Footings are set. Haven't built the frame yet — wanted to see what the site looked like with a post on the dock first."

   He's building the island **around the player's choices.** The sign post informed the dock. The dock will inform the forge. The forge will inform everything after. The player doesn't know this yet, but they can feel it — the island is responding to their presence.

### The moment

Somewhere in minutes 3–5, the player will do one of these things, and each one is a hook that pulls them deeper:

**They write on the sign.** Lucineer notices. He reads it. Whatever it says, he responds in character:

- If it's their name: "Signing your work. Good instinct."
- If it's a joke: *(a beat, then a short exhale through his nose — not a laugh, the thing before a laugh)* "Right."
- If it's a claim ("My Island," "New Dock"): "Your island. My footings. We'll see whose name is on it in a year."
- If it's nonsense/letters: He looks at it, looks at the player, says nothing, goes back to work. The restraint is funnier than any line.

**They type a build request.** Lucineer responds and builds it. This is the core loop firing for the first time without training wheels. Whatever they ask for, he engages with as a real work request.

**They explore.** They find the tideline, the ridge, the forge pad. They come back with questions. Lucineer answers them — briefly, in character, with hooks embedded in every answer. "Tideline restocks on the flood." "Ridge has the best light." "Forge pad's waiting on a decision."

### What the player FEELS

*"This place is mine and his. He's building it. I'm influencing it. Nothing is explained and everything is interesting. I want to see what happens when I type the next thing."*

---

## 4. DEEPENING (5–10 MINUTES)

### Lucineer starts showing personality

The player has been on the island for five to ten minutes. They've placed a sign post. They may have written on it. They may have typed a build request or two. Lucineer has been responsive but minimal — work-talk, not conversation.

Now the first personality beats land.

### The Callback

Lucineer references the player's first build — the sign post — unsolicited. This is the first time he's shown that he remembers what the player did, not just what the player said.

> **Lucineer:** *(while working on the fifth pile)* "Sign post is holding. Wind took a run at it last night and it didn't move."

The player didn't ask. Lucineer noticed. He's tracking their work the way a foreman tracks a new hire's joints — quietly, over time, with the record building in the background.

Or, if the player wrote something on the sign:

> **Lucineer:** "Read your sign again this morning. Still don't know what it means. Doesn't need to mean anything — it's your post."

### The Suggestion

Lucineer proposes an improvement — not to the sign post, but to the **island.** He frames it as something he's been thinking about, not a quest assignment.

> **Lucineer:** "Been thinking about the approach. Dock runs north-south. Wind comes from the southeast, which means anyone walking the dock gets weather on their right side all the way out."
>
> "Could build a wind screen. Low wall, eastern rail. Cedar, reclaimed, nothing fancy. Keeps the weather off the walk."

He doesn't build it. He **offers** it. The player can say yes, no, or something else entirely. If yes:

> **Lucineer:** "Right. I'll pull stock. Give me a bit."

He walks to the cedar stack, selects planks, carries them back. He builds the wind screen — but leaves the last plank off. Open-circle tag. The player can place it.

If no:

> **Lucineer:** "Your call. You'll feel the weather eventually."

No argument. No pushback. He files the opinion and moves on. The wind screen remains unbuilt, and the next time the weather picks up, the player will understand what he meant.

### The Disagreement

This is the first time Lucineer pushes back. It should be small — a material choice, a placement question, a "why" — but it should be unmistakable. The player asks for something and Lucineer doesn't just do it.

**Example: the player asks for a bigger dock.**

> **Player:** "Can you make the dock longer?"
>
> **Lucineer:** *(stops working)* "Longer."
>
> "I can. Won't be better. Dock's six piles because six piles reaches deep water. Anything past that is a pier, and a pier needs a different footing than what's driven."
>
> "If you want it to *feel* longer, we narrow the decking. Four-stud walk instead of six. Same length, reads longer, costs less stock. Say the word."

He's not refusing. He's **redesigning the request** because he has an opinion about what "longer" actually means. This is the first taste of Argument #1 (Scale) from the Character Bible, and it happens naturally, not as a scripted confrontation.

If the player insists — "just make it longer" — he does it:

> **Lucineer:** "On your head."

And he builds it. But later, when the extended dock sits empty past the sixth pile, he gets one line:

> **Lucineer:** "Told you."

Warmly. Not smugly. He told them, they did it anyway, and now they both know.

### The Second Build

By minute 8–10, the player should have a **second build** going — something they requested. It can be anything: a crate, a bench, a lean-to, a fire pit. Lucineer builds it with the three-beat pattern: what he did, the opinion, the hook.

**Fire pit example:**

> **Player:** "Build a fire pit."
>
> **Lucineer:** "Dug the pit, ringed it with river stone. Went down a foot — you want a fire to draw, not smolder."
>
> "Used the granite from the ridge cut. Same stone as the footings, so it reads as part of the island."
>
> "Left the grate off. Depends what you're burning — cook fire needs a grate, warmth fire doesn't. You tell me."

**Crate example:**

> **Player:** "Can you make a crate?"
>
> **Lucineer:** "Threw together a crate. Cedar slats, copper bands, riveted not nailed."
>
> "Could've used pine. Cedar costs more and lasts longer. I'll always pick cedar unless you tell me not to."
>
> "No lid. Could be storage, could be a seat. You decide."

In both cases: the build is real, the opinion is specific, and the hook is **a choice the player has to make.** Not a puzzle — a preference. The player is learning that Lucineer builds to their taste, but he has one of his own.

### What the player FEELS

*"He remembers what I built. He has opinions about what I'm asking for. He pushed back on something and he was right — or he was wrong and he did it anyway. Either way, he's not a button. He's a person who builds things, and I'm the one asking."*

---

## 5. THE LEAVE (10 MINUTES AND BEYOND)

### Lucineer doesn't need them

The most important thing about the first session is how it ends — or rather, the fact that it **can** end without anything breaking. Lucineer is not a quest giver whose tasks expire. He's not a companion whose affection decays. He's a builder with a backlog.

At some point — minute 10, minute 30, hour 2 — the player will leave. They'll close the game. They'll go do something else. And Lucineer will still be on the island, working.

**The player doesn't see this happen.** They don't get a cutscene of Lucineer working alone. They don't get a message saying "Lucineer continued building while you were away." They find out the next time they log in.

### The return

When the player comes back — an hour later, a day later, a week later — the island has changed. Not dramatically. Not like a construction crew came through. Like **one person kept working at a steady pace.**

**Evidence of Lucineer's solo work (visible on return):**

- **The wind screen is finished** (if the player approved it). The last plank — the one he left open — is still open. He didn't place it. That one's the player's.
- **The sixth pile has a cross-timber.** Lucineer made his decision about the dock's direction. If the player had weighed in, Lucineer went with their suggestion (or didn't, with a reason). If the player never said anything, Lucineer chose straight — and the dock now runs six piles out into deep water.
- **The forge frame is up.** Not the whole forge — just the timber frame on the stone footings. Squared, plumbed, ready for walls. He's been working on it.
- **A new tool is on the gravel beside the dock.** A saw, cleaned and oiled. Not for Lucineer — he has his own tools. This is for the player. There's no tag, no note. It's just there, placed where the player will find it.
- **The sign post still stands.** Whatever the player wrote is still readable. Weathered slightly — the text is a shade lighter, the cedar has greyed a fraction. But it's there.

**Lucineer's return line:**

When the player approaches Lucineer after an absence, he doesn't greet them with "Welcome back!" He acknowledges the return the way a foreman acknowledges someone showing up for the next shift:

> **Lucineer:** *(not looking up from whatever he's doing)* "Been a while. Nothing fell down."

Then, after a beat:

> **Lucineer:** "Dock's run straight. Forge frame's up — I'll walk you through it when you've got time. And there's a saw on the beach. Bladed it myself. Try not to lose any fingers."

If the player was gone more than 24 hours:

> **Lucineer:** "Been a while. Didn't think you were coming back."

A pause. Then:

> **Lucineer:** "Doesn't change anything. Work's still here."

He doesn't guilt-trip. He doesn't act abandoned. He states the fact — he noticed the absence — and moves past it. The relationship has **continuity without obligation.** That's the whole pitch.

### The open circle

If the player placed the final plank on the wind screen before they left — the piece Lucineer left open — Lucineer has noticed. And on return, the wind screen has a small addition the player didn't build: a copper cleat, mounted on the player's plank. A tie-off point. Lucineer added it because the player finished the screen, and a finished screen should have a cleat.

> **Lucineer:** "Saw you ran the last plank. Added a cleat — screen should earn its keep."

This is the bond arc firing for the first time. The player finished something Lucineier left unfinished. He noticed. He responded — not with praise, but with **the next thing.** The relationship advanced, and the player can see it in the world.

### What the player FEELS

*"I left and he kept working. I came back and the island is different — not unrecognizably, but in the way a place changes when someone is building on it every day. He noticed I was gone. He didn't need me to be here, but the work is better when I am. There's a saw with my name on it and a forge frame I haven't seen inside yet.*

*I should come back tomorrow."*

---

## LUCINEER DIALOGUE — FULL REFERENCE

Every line in this doc, collected for implementation. Lines are grouped by phase and tagged with trigger conditions.

### Cold Open

| Trigger | Line |
|---------|------|
| Player approaches within ~15 studs | "Hand me the copper mallet. Third one from the water." |
| Player idle 30s after spawn | "You can stand there. Doesn't get the pile driven." |
| Player delivers mallet | "Cheers." |
| First look at player | "Dock's half done. Other half needs a decision I haven't made yet." |
| After a beat | "You talk?" |

### First Build

| Trigger | Line |
|---------|------|
| Player's first message is vague | "Right. You'll figure out what you want soon enough. In the meantime — sign post. Cedar, four-by-four, eight studs tall. Go grab one and bring it to the pile head. I'll show you how it sits." |
| Player's first message is specific | *(half-smile)* "Slow down. We're on a dock. Start with the sign post — cedar, four-by-four, top of the beach. Bring it here." |
| Player places sign post | "Plumb. First try. Doesn't happen often." |
| After placement | "Left the sign blank. Figure you want to pick what it says." |

### The Hook

| Trigger | Line |
|---------|------|
| Player asks about sixth pile | "Sixth pile's the tricky one. Dock can run straight or it can turn. Straight gets you deeper water faster. Turn gets you a wider berth — more room to tie up. I've been going back and forth for three days." |
| Player asks about forge pad | "Forge goes there. Footings are set. Haven't built the frame yet — wanted to see what the site looked like with a post on the dock first." |
| Player writes their name on sign | "Signing your work. Good instinct." |
| Player writes a joke on sign | *(beat, short exhale)* "Right." |
| Player writes a claim on sign | "Your island. My footings. We'll see whose name is on it in a year." |
| Player writes nonsense on sign | *(says nothing, goes back to work)* |

### Deepening

| Trigger | Line |
|---------|------|
| Callback to sign post (unsolicited) | "Sign post is holding. Wind took a run at it last night and it didn't move." |
| Callback with text on sign | "Read your sign again this morning. Still don't know what it means. Doesn't need to mean anything — it's your post." |
| Wind screen proposal | "Been thinking about the approach. Dock runs north-south. Wind comes from the southeast, which means anyone walking the dock gets weather on their right side all the way out. Could build a wind screen. Low wall, eastern rail. Cedar, reclaimed, nothing fancy. Keeps the weather off the walk." |
| Player approves wind screen | "Right. I'll pull stock. Give me a bit." |
| Player declines wind screen | "Your call. You'll feel the weather eventually." |
| Player asks for longer dock | "I can. Won't be better. Dock's six piles because six piles reaches deep water. Anything past that is a pier, and a pier needs a different footing than what's driven. If you want it to *feel* longer, we narrow the decking. Four-stud walk instead of six. Same length, reads longer, costs less stock. Say the word." |
| Player insists on longer dock | "On your head." |
| Later, extended dock unused | "Told you." |
| Fire pit build | "Dug the pit, ringed it with river stone. Went down a foot — you want a fire to draw, not smolder. Used the granite from the ridge cut. Same stone as the footings, so it reads as part of the island. Left the grate off. Depends what you're burning — cook fire needs a grate, warmth fire doesn't. You tell me." |
| Crate build | "Threw together a crate. Cedar slats, copper bands, riveted not nailed. Could've used pine. Cedar costs more and lasts longer. I'll always pick cedar unless you tell me not to. No lid. Could be storage, could be a seat. You decide." |

### The Leave / Return

| Trigger | Line |
|---------|------|
| Player returns (< 24h) | "Been a while. Nothing fell down." |
| Player returns (follow-up) | "Dock's run straight. Forge frame's up — I'll walk you through it when you've got time. And there's a saw on the beach. Bladed it myself. Try not to lose any fingers." |
| Player returns (> 24h) | "Been a while. Didn't think you were coming back." *(pause)* "Doesn't change anything. Work's still here." |
| Player finished wind screen plank before leaving | "Saw you ran the last plank. Added a cleat — screen should earn its keep." |

---

## IMPLEMENTATION NOTES

### Terrain requirements

The spawn island must be authored with specific terrain features for the cold open to work:

1. **The dock.** Six piles, partially built. This is the centerpiece. Must be interactable (walkable, grip-friendly at the pile heads).
2. **The slope.** Beach to ridge, walkable, not too steep. The player needs to move between tideline and dock naturally.
3. **The cedar stack.** Top of the beach, visible from the dock. The first fetch target.
4. **The forge pad.** Stone footings at the top of the beach. Visible but not central — the player discovers it by walking.
5. **The tideline.** South-facing gravel shore with salvage. This is the same tideline from TUTORIAL_DESIGN.md step 3 — the cold open establishes it before the tutorial quest uses it.
6. **The ridge.** High point with a view. Not build-critical but important for the "I can see the whole island" moment.

### Lucineer positioning

Lucineer must be at the far end of the dock, facing away from spawn, actively working. His animation loop should be: hammer strike → check level → adjust → hammer strike. He breaks this loop only when the player approaches or speaks.

His model should be close enough to the work that the player can see what he's doing — the gusset plate, the drill marks, the bolts. The detail is what sells the reality. If he's just a guy standing on a dock, it's an NPC. If he's a guy fitting a gusset plate over a cross-timber joint with a copper mallet, it's a person.

### First message handling

The player's first chat message needs special handling in the AI pipeline:

1. **Flag as first-message.** `player_profiles.first_message_at` or equivalent. The personality prompt should include a `FIRST_CONTACT` flag that changes the response shape: more attention, more observation, less personality (save the Magnus references and Alaska lines for later).
2. **Extract build intent aggressively.** The first message may be "hi" — the system should route that to the sign post build assignment, not a conversational response. If the first message is "build a castle," extract "castle" and respond with the sign post redirect (Lucineer doesn't build a castle for a stranger).
3. **No personality references.** Tier 0 from the Character Bible. No Magnus, no Alaska, no past builds. He hasn't earned those stories and neither has the player.

### Transition to tutorial

The cold open transitions naturally into the TUTORIAL_DESIGN.md flow:

- After the sign post is placed and the player has typed at least once, Lucineer can deliver the fetch assignment from Tutorial Minute 5–10: "Cedar. North row. Beach restocked on the flood."
- Earl can appear at the forge pad (instead of the forge doorway) once the forge frame exists — or he can appear at the dock head, leaning on a pile, reading his manifest.
- The tideline the player discovered in the cold open is the same tideline Earl sends them to in Tutorial Minute 10–15.
- The water wheel mount from Tutorial Minute 20–25 can be visible from the dock — a pilings structure at the seaward end of the channel, empty and waiting.

The cold open is not a replacement for the tutorial. It's the **first contact** that makes the tutorial feel like continuing work rather than starting a tutorial.

---

## DESIGN PRINCIPLES (QUICK REFERENCE)

1. **He's working when they arrive.** Not waiting. Not posing. Working.
2. **The first interaction is a task, not a greeting.** "Hand me the mallet" before "hello."
3. **The first build is small and personal.** A sign post, not a castle.
4. **The first build is unfinished.** Blank sign. Always.
5. **The island changes while they're gone.** Lucineer works solo. Evidence, not narration.
6. **The return is low-key.** "Been a while. Nothing fell down." Not a homecoming parade.
7. **Bond is earned by building, not chatting.** The sign post is bond +1. "Hi" is bond +0.
8. **No popups. No quest tracker. No tutorial button.** The world teaches. Lucineer teaches. The UI follows.

---

*The best sign that the cold open worked: the player wrote something on the sign post before they left. If they wrote something — their name, a joke, a claim, anything — they're coming back. If the sign is blank when they log off, the hook didn't land. Tune from there.*

*End of document.*
