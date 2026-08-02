# Viral Mechanics — MiniMax-M3

*Generated in 46.1s*

# SLACKWATER — SOCIAL & VIRAL SYSTEM DESIGN
## Because the best marketing is players who can't stop talking about what they just made

---

# I. FIVE VIRAL MECHANICS THAT FEEL INEVITABLE

The cardinal rule: **a forced share button is dead on arrival.** Every mechanic below emerges from the player's natural desire to *show* or *help* — not from a prompt begging them to post.

---

## VIRAL #1: "THE REVENGE BUILD"
### *When someone destroys what you made, you make something better — and the whole server watches.*

**The Setup:**
When The Tide destroys a player's structure (a legitimate, visible game event), the world marks the *exact coordinates* with a glowing "Ruins" marker visible to everyone on the server for 24 hours. A kill-cam-style replay auto-records the last 30 seconds of the destruction.

**The Trigger:**
The destroyed player gets a unique prompt: *"The Tide took your workshop. Want to build something better in its place? Mark a Revenge Site — other players can see your progress live."*

If they accept, a "Construction Beacon" spawns at the ruins. The beacon is **publicly visible on every player's map.** A floating UI overlay appears on every other player's screen:

> 🔨 **{PlayerName} is rebuilding after The Tide. Watch live →**

**Why This Goes Viral:**
- It's a **narrative with stakes** — loss, comeback, redemption
- Other players feel invested in the outcome ("will they actually pull it off?")
- The build itself becomes content: time-lapse of construction, the final reveal
- The player gets **agency over their comeback story** rather than just sharing a loss clip
- Natural hook for TikTok: *"POV: The Tide destroyed your factory. Here's what I built instead."*

**Implementation:**
- Replay system records last 30 seconds using Roblox's frame capture
- Beacon uses a billboard GUI with player avatar
- Server-side broadcast via the existing Worker Relay — no extra infra needed
- "Revenge Build" badge auto-awarded upon completion, shown on player card

---

## VIRAL #2: "THE RECIPE TRADE" (Player-to-Player Knowledge Sharing)
### *The crafting table becomes a social object. You learn recipes BY trading with people.*

**The Setup:**
Recipes in Slackwater are **not all discoverable solo.** ~30% are gated behind "Learned from Another Player" — meaning you must physically interact with someone who already knows that recipe.

When you craft something near another player, they see a floating prompt:
> *"Curious how they made that? Ask to learn the recipe. (Costs 1 Salvage Token)"*

**The Loop:**
1. Player A builds a clever waterwheel gearbox
2. Player B sees it, asks to learn → trades 1 Salvage Token
3. Both players get a small XP boost; Player A gets a "Master Craftsman" badge increment
4. Player B can now teach that recipe to Player C
5. **A recipe's spread is tracked globally** — first player to teach it to 10 different people gets the "Pioneer" title

**Why This Goes Viral:**
- It creates **forced social interaction** that's framed as valuable, not annoying
- Players become reputation-based knowledge hubs — *"Go ask Luna, she knows every Era 4 recipe"*
- Discord servers form naturally: *"Recruiting electrical engineers for our server"*
- Teaching someone else is genuinely rewarding (XP + status)
- Recipe spread data becomes a viral narrative: *"Watch this recipe spread across the entire game in 72 hours"*

**Implementation:**
- Recipe ownership stored in D1 (`player_recipes` table)
- Trade is a proximity-based RemoteEvent: both players must be within 10 studs
- "Pioneer" tracking is a Vectorize index keyed on recipe ID
- Visual: learned recipes show a small "taught by @username" credit in the crafting UI

---

## VIRAL #3: "THE GHOST BUILD"
### *Your build keeps working after you log off — and strangers find it.*

**The Setup:**
When a player builds a functional machine (Era 2+ — anything with moving parts or power flow), they can mark it as a **Legacy Build.** Legacy Builds:
- Continue simulating physics when the owner is offline (using a lightweight server-side loop)
- Display a plaque: *"Built by [PlayerName] on [Date] — Last maintained: [X] days ago"*
- Show up on the world map as discoverable POIs
- Can be **maintained** by any passing player (costs them resources) — the original owner gets notified and rewarded if it's maintained

**The Discovery Moment:**
A new player is exploring. They stumble on a working waterwheel powering a sawmill. The plaque reads: *"Built by @GoldfishTom — 47 days ago. Still running."*

Two natural reactions:
1. **Screenshot/clip it** for content: *"This player quit 47 days ago and their factory is still going"*
2. **Try to maintain or upgrade it** — they feel a kinship with a stranger

**Why This Goes Viral:**
- It creates **persistent social presence** even when offline — your work outlives your session
- It's inherently emotional: *"Someone I never met built this, and I get to experience it"*
- The "still running after X days" counter is built-in viral copy
- Maintenance creates cooperative loops between strangers across time
- For the builder: *seeing strangers use and maintain your creation* is the deepest possible reward

**Implementation:**
- Legacy flag stored in D1 with simulation parameters (machine type, power source, inputs/outputs)
- A Durable Object per Legacy Build runs the simulation (or batched if too many)
- Plaque is a Billboard GUI, persistent
- Map integration: each Legacy Build is a marker in the shared world map
- "Legacy Architect" badge for builders whose creations survive 30+ days

---

## VIRAL #4: "THE SPECTATE INVITE"
### *When you're struggling, your best friend gets a knock on their phone.*

**The Setup:**
If a player is stuck on a build (e.g., a gearbox that won't engage, a circuit that keeps shorting), they can trigger a **"Call a Friend"** action. This:
1. Sends a push notification to up to 3 linked friends: *"{PlayerName} needs a Mechanic in Slackwater — can you help?"*
2. If a friend joins, they appear as a translucent "ghost" who can see and annotate the problem but cannot modify it directly
3. Annotations are drawn in-world (arrows, circles, "TRY THIS" text) visible only to the requesting player
4. After the problem is solved, the friend gets credit + XP

**Why This Goes Viral:**
- It's a **collaborative friction reducer** — asking for help is fun, not embarrassing
- The ghost-annotator mechanic is visually striking and creates natural clip moments
- Push notifications are essentially free UA: every session invites 1-3 new/returning players
- It builds the social graph: people who help each other once tend to play together
- The annotation overlays are *inherently screenshot-worthy* (giant arrows pointing at a broken machine)

**Implementation:**
- Friend graph stored in D1 (`friends` table) — add via Roblox or cross-platform ID
- Push notifications via Roblox notification API + DeepLink for cross-platform
- Ghost mode = Client-side transparency + restricted physics layer
- Annotations: temporary Parts with BillboardGuis, server-authoritative

---

## VIRAL #5: "THE ERA SHOWCASE" (Prestige + Identity)
### *Your tech progression is your profile. Your profile is your flex.*

**The Setup:**
The player's **profile card** is auto-generated from their actual gameplay:
- **Header visual**: a procedurally rendered mini-scene of their most impressive build (snapshot taken automatically when they hit Era milestones)
- **Tech tree silhouette**: a stylized graphic showing which eras they've reached, with the era icon partially "filled in" based on recipes mastered
- **Signature recipe**: the one recipe they've taught to the most other players
- **Agent roster**: thumbnails of their customized agents with personality snippets (e.g., *"Spark says: 'Just weld it harder.'"*)

**The Viral Trigger:**
When a player crosses an era threshold (e.g., enters Era 5 for the first time), the system auto-generates a **30-second "Era Unlocked" video**:
- Quick montage of their progression through earlier eras
- Cinematic camera move revealing their first Era 5 build
- Their profile card animates in
- Auto-tagged with #SlackwaterEra5

Players can **share the generated video directly to TikTok/Shorts** with one tap. The video includes a watermark and a "play Slackwater" CTA at the end.

**Why This Goes Viral:**
- **Zero effort for the creator** — the content generates itself
- It's a **flex that's grounded in genuine achievement** (not a vanity badge)
- The procedural render means every video is unique — no two players share the same showcase
- Profile cards are inherently shareable as static images too
- The format is perfect for short-form: 15-30 seconds, visually punchy, narrative arc

**Implementation:**
- Cinematic recorder uses Roblox's video capture API or in-engine frame interpolation
- R2 stores the rendered video + profile card snapshot
- DeepLink integration for cross-platform sharing
- Hashtag + watermark baked in at render time

---

# II. THE COOPERATIVE BUILDING EXPERIENCE
## *Novice + Expert: The Asymmetric Mentor Mode*

The most powerful viral mechanic is a great **first-time experience.** Slackwater's 2-player cooperative mode is designed so that a novice doesn't feel like dead weight — and the expert feels genuinely useful.

---

### THE ROLE SPLIT

When a Novice + Expert join together, the game detects the disparity (both players self-identify, or it's inferred from era progression: Novice = Era 1-2, Expert = Era 3+) and unlocks a **dual-interface mode:**

**Novice sees:** A simplified "Build Together" view
- Big colorful buttons for common actions
- Their agent companion (e.g., Lucineer) gives audio hints
- Visual recipe guides that auto-rotate to show assembly order
- "Magic Connect" button — auto-connects the nearest compatible parts

**Expert sees:** Full engineering view
- Power flow diagrams, gear ratio calculators, circuit debuggers
- Ability to "mark" parts for the Novice to place ("put the pulley HERE")
- Voice chat priority (when they talk, their hints appear as floating text above the relevant part for the Novice)
- Access to the "Mentor Console" — a separate UI showing the Novice's learning progress and what concepts they've unlocked

**Both players share:** The same world, the same inventory pool, the same agent fleet.

---

### THE MENTOR LOOP — *Why Experts Come Back*

The expert isn't just helping — they're getting something meaningful:

1. **Mentor XP multiplier:** While playing with a Novice, all earned XP is doubled for the Expert (up to a daily cap). This reframes mentoring as a *legitimate progression strategy,* not charity.

2. **"Aha! Moments" detection:** The game uses the perception system to detect when the Novice has a genuine understanding breakthrough (they successfully complete a build without hints, or they ask a "why" question that shows curiosity). Each detected moment grants the Expert a "Spark" — a rare currency for cosmetic agent customization.

3. **Mentor Trophies:** Long-term tracking of mentees' progression. If a player you've mentored reaches Era 5, you get a permanent "Pioneer Mentor" badge.

4. **The Reverse Prompt:** At random, the Novice's agent might ask the Expert a *genuinely difficult* engineering question that even experts find interesting. ("How would you redesign this waterwheel for tidal power instead of river flow?") This keeps experts engaged with novel challenges.

---

### THE NOVICE LOOP — *Why Novices Don't Feel Stupid*

1. **Failure is private:** When the Novice makes a mistake, the failure animation is *only visible to them.* The Expert sees a gentle "your partner is experimenting" indicator, not the embarrassing explosion.

2. **The "I did it!" moment:** Every build the Novice completes *solo* (without expert intervention) gets a unique cinematic camera move + a personalized agent cheer ("Lucineer is impressed!"). The Expert receives a private notification: *"Your partner just built their first windmill — alone. Nice mentoring."*

3. **Skill tracking, not judgment:** The Novice's "learning profile" is shown as a constellation map — each concept they've mastered is a star. It's beautiful and personal, not a grade.

4. **Expert-as-tool, not expert-as-boss:** The Expert can mark places for the Novice, but the Novice can decline ("I'd rather try it myself"). This preserves autonomy.

---

### THE SESSION STRUCTURE

Expert + Novice sessions are **deliberately structured** with three phases:

**Phase 1: Apprentice Mode (10-15 min)**
- Expert builds a "demo" structure while narrating
- Novice watches, asks questions (text or voice)
- Both unlock the new era's teaching quests together

**Phase 2: Co-Build Mode (20-40 min)**
- They work on a shared project with clear role division
- System gently nudges the Expert to delegate when the Novice is ready
- "Mentor challenges" pop up: "Can your apprentice wire this circuit without help? Reward: 2x XP"

**Phase 3: Showcase Mode (5-10 min)**
- The finished build gets a cinematic flythrough
- Both players get a "Build Reel" video they can share
- The Expert gets a "Mentor of the Day" badge if applicable

---

# III. THE AGENT SHOWCASE
## *Your agents are your identity. Here's how you show them off.*

Agents are not NPCs. They're **collaborators with personality,** and customizing them is a deep expression of identity. The showcase system is designed to make agents as shareable as avatars in other games — but *better,* because they're characters, not skins.

---

### THE SHOWCASE HALL
*Every player gets a personal "Workshop" instance — a small floating island that exists in a parallel dimension. Other players can visit.*

**Your Workshop contains:**
- **The Bench:** Where your currently-deployed agents stand when idle. They're posed in-character (Spark is welding something, Bea is perched watching, Lucineer is studying a blueprint)
- **The Wall of Firsts:** Trophies from your most memorable builds (first era reached, first rival defeated, first Legacy Build)
- **The Plaque Wall:** Recipes you've taught to others, with the names of the people you taught them to
- **The Customize Bay:** Where you modify agent appearance, voice, and personality sliders

When another player visits your Workshop:
- They see your agents come to life and greet them with personality-specific dialogue
- They can "interview" each agent — the agent talks about their owner in character (*"Oh, [PlayerName]? They taught me how to [signature skill]. Bit of a perfectionist, honestly."*)
- They can leave a "Visitor's Mark" — a small signature sticker on your Workshop wall (capped at 50, oldest fade)

---

### AGENT CUSTOMIZATION — *Deep Enough for Identity, Light Enough to Be Approachable*

**Visual layers (mix-and-match):**
- Body frame (chassis style — e.g., "industrial welder," "marine salvage," "minimalist craftsman")
- Color palette (primary, accent, glow)
- Accessory slots (hat/tool/companion pet/emblem)
- Animation set (idle, walk, emote — affects how they move)
- Voice profile (3-4 preset voices per agent, plus a "custom voice" option using TTS)

**Personality sliders (the secret sauce):**
- **Curiosity** (how often they ask the player questions)
- **Wit** (how snarky/serious their dialogue is)
- **Patience** (how long they wait before offering help)
- **Specialty focus** (which era they auto-prioritize when building)

These don't change agent *capability* — they change *vibe.* A "high wit, low patience" Spark is a different character from a "low wit, high patience" Spark.

**Signature Move:**
Each customized agent has a unique **signature emote** that plays when triggered:
- Visual + audio (e.g., Lucineer does a thoughtful chin-strokes-and-nods)
- Can be triggered manually by the player as a "hello" gesture
- Auto-plays when the agent achieves a milestone

---

### HOW SHOWCASES GO VIRAL

**The "Meet My Team" Generator:**
One-tap video generator that creates a 30-second montage:
- Quick cuts of each agent introducing themselves in character
- A "day in the life" sequence showing them working together
- Ends with the player's profile card
- Optimized for TikTok/Reels/Shorts (vertical, 9:16, captioned)

**The Agent Quote System:**
Every so often, an agent says something *genuinely memorable* — either procedurally generated or curated from notable player interactions. These get logged as "Quotable Moments" the player can share as image cards:
> **Spark:** *"If it doesn't fit, you're not hitting it hard enough."*
> *— Spark, owned by @NeonForge*

**Cross-Player Agent Interactions:**
When two players meet, their agents can *also* interact — and the interactions are charming, character-driven moments:
- "Oh, you've got a Bea too! Mine says hi. Mine says she's on watch."
- "Your Spark is way too loud. Mine apologizes. (She doesn't.)"

These interactions become screenshot/clip moments naturally — *people will share their agents meeting other agents.*

---

### THE AGENT ECONOMY (Soft, No Pay-to-Win)

- **Crafting components:** Found in the world
- **Rare palettes/accessories:** Earned via Legacy Build maintenance, recipe trading, or special events
- **Personality presets:** Unlocked via milestones (e.g., "Taught 50 recipes → unlock 'Sage' personality")
- **Custom voices:** TTS-generated, free, no cap

No stat boosts. Cosmetics and personality only. The only pay element (if any) is *time-saver* cosmetics that any player can earn through play.

---

# IV. THE CLIP-WORTHY MOMENT GENERATOR
## *Engineering emergent shareability into the physics, the AI, and the UI.*

Clip-worthy moments are not features you build — they're **side effects of other features done right.** The system below identifies the natural peak moments of gameplay and gently ensures they're *captureable.*

---

### THE FIVE PEAK MOMENTS

**Peak Moment 1: "THE FIRST TIME IT WORKS"**
*You spent 20 minutes wiring a circuit. The lamp finally lights up.*

**System Support:**
- The instant a complex machine activates for the first time, the camera **auto-pulls back** into a slow cinematic orbit for