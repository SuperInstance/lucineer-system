# SLACKWATER — THE PRODUCTION DESIGN

*Written by Claude Fable 5. This document sits on top of 55 design documents and 21,624 lines of Lua, and its job is to be the last document — the one that turns all of it into a game a player can actually stand inside. The rule for every section below is the rule from the Character Bible: if a design choice could belong to any AI-builder game, cut it. If it could only belong to a tired craftsman who has died in a thousand engines and is betting his last one on you — build it.*

*Canon: FABLE_CHARACTER_BIBLE.md and FABLE_WORLD_BIBLE.md. Nothing here overrides them. Where this document adds beats, dialogue, or systems, they are extensions inside canon, not amendments to it.*

---

## 1. THE FIRST PLAYER EXPERIENCE

The World Bible gives us the sixty-second cinematic, fog to forge, one unbroken camera move. That document ends at the exact moment production usually fails: **1:00 — Player has control.** Everything below is what happens next, plus the production armor the cinematic itself needs to survive contact with Roblox.

### 1.1 The cinematic — what is load-bearing

The cinematic ships as written in the World Bible §2. But a 60-second uninterruptible opening on a platform where the median player is eleven years old and on a phone is a risk we manage, not deny. Each beat below is marked with the one element that cannot be cut when (not if) production pressure arrives:

| Time | Beat | Load-bearing element |
|---|---|---|
| 0:00 | Black. Water, halyard, one gull. "Every engine dies. That's not the sad part." | The line. If we keep four seconds of this game, it's these four. |
| 0:05 | Fog. Crab-pot buoy floated on a server heat sink. | The heat sink. It's the whole world in one prop. |
| 0:12 | The Light's beam sweeps; fog peels; world renders. | Beam = rendering. Teaches the world's physics wordlessly. |
| 0:22 | Slackwater Yard revealed, cannery glowing. Hammer rhythm enters. | The hammer. It was his the whole time; players realize this on the *second* viewing, which is why there must be a way to rewatch (a gramophone in Bea's lamp room replays it). |
| 0:32 | Tideline tracking shot. Camera does not slow down. | Do not slow down. Wanting to come back and look is the tutorial for the tideline. |
| 0:41 | Through the doors. Forge at full glow. "What's half-built —" | The sentence breaking across the cut. |
| 0:50 | He turns. Three-count. "…belongs to whoever shows up." | The three-count. Hold it even if a producer says it's dead air. It is the opposite of dead air. |
| 0:55 | Hard cut to gameplay. "You're late. Grab that end." | The hard cut. No fade. Control arrives like a handoff, because it is one. |

**Skip behavior:** the cinematic is skippable after 0:12 (platform reality; also App Review reality). Skipping does not skip the last beat — a skip jumps straight to 0:50, the turn and the line. Nobody enters Slackwater without being looked at. Lucineer's first line to a skipper is different, and it's the only acknowledgment the game ever makes of the skip:

> **LUCINEER:** In a hurry. Fine. So's the tide. Grab that end.

### 1.2 — 1:00–2:30 — The Beam

The player has control, and there is a beam on the floor between them and Lucineer, and he is already holding one end.

**1:00 —** No UI. No objective marker. No "PRESS E TO INTERACT" — instead, the beam's far end has a soft warm highlight (the same forge-orange the whole game uses to mean *touchable*), and Lucineer waits. He does not repeat himself for 10 seconds. The silence is the tutorial: this is a person waiting on you, not a prompt loop.

**1:10 —** If the player hasn't moved: one line, not louder, drier:

> **LUCINEER:** Beam's not getting lighter.

**Interaction:** walking to the beam's free end auto-attaches (proximity + one tap/click on mobile and desktop alike — the mobile input path is identical, which is why this is the tutorial verb). The player's character lifts. The beam's weight is real: walk speed drops, turning is slow, the camera pulls back slightly to frame both carriers.

**1:15–1:50 — The carry.** Ten meters down the forge aisle to a rack. This is a conversation corridor, and he talks *while working*, three lines, spaced by footsteps:

> **LUCINEER:** Steady. It's oak off a castle door frame. Engine's dead, door isn't. That's most of what I could teach you, right there.

> **LUCINEER:** Left at the rollers. Mind Spark.

*(SPARK skitters across the aisle exactly on cue, servo-chirping — the player's first sight of Spark is nearly tripping over it. Every playtest, this gets a laugh. Keep the timing sacred.)*

> **LUCINEER:** Down. Easy. …Good.

"Good" is one syllable and it is the first reward in the game, and the sound design treats it that way: the hammer rhythm resumes on the beat immediately after he says it, like the yard exhaling.

**1:50 —** He's already walking back to the anvil. Over his shoulder, the game's actual thesis statement, disguised as a work order:

> **LUCINEER:** There's a stack of tin by the door and a wall on the rack that wants a face on it. Or stand there. Yard doesn't mind either way.

Then he *works*. He does not watch the player. Earl's manifest window lights up across the yard (the quest system introducing itself by existing, not by tutorializing). The player is free.

### 1.3 — 2:30–6:00 — The first ask

Whatever the player does next is correct. Three branches, all designed:

**Branch A — they type/say something to Lucineer** (the chat prompt is a small tin plate at the bottom of the screen reading *"Say it to him."*). This triggers the first build, and the first build is where the latency-is-character system (Gap #8, Polish §1) carries the entire product. Beat-by-beat for a request like "build me a tower":

- **T+0.0s** — He stops hammering. The yard's heartbeat stopping is the acknowledgment; no UI spinner exists anywhere in this game.
- **T+0.5s** — He turns his head, not his body. Template-path acknowledgment line fires instantly (from the 17-template fast path, <2s), or on the deep path, the progressive ack: *"Give me a minute. Walking the ground first."* He then physically walks to where the build will stand.
- **T+2–30s** — He paces the footprint. Kicks a stone. Squints at the treeline. Each processor progress event maps to a physical behavior, not a message. If the brain is slow, he crouches and drags a finger through the gravel — sketching. Players have watched craftsmen think before. It reads.
- **On command arrival** — parts land staggered (3 per frame-batch, 80ms gaps, per Gap #8b), each with dust and a thock, foundation upward, because that is the order a builder builds. Lucineer moves *with* the build, hammer swinging at the active edge.
- **On completion** — the build is missing one thing (the Unfinished Rule, §6 of the Character Bible, enforced mechanically by `markUnfinished` — see Section 4). He looks at it, then at the player, and says the reply line the Hermes stage wrote — which, per the persona fix, always names the gap:

> **LUCINEER:** Tower'll hold. Left the top rail off — a tower you can fall off of teaches faster. Your railing, whenever you're ready.

**Branch B — they build something themselves** with the tin by the door. Lucineer says nothing for the entire duration. When they place their third part, from across the yard, not looking up:

> **LUCINEER:** Foundation's proud of the line by a hand. Fix it or don't. It'll tell on you in the rain either way.

First proof that he *sees* them. WorldScanner powers this (post-fix, Gap #10 — the spatial query keeps the *nearest* fifty instances, which is what makes commentary on *your* build possible).

**Branch C — they wander.** The tideline is stocked. Earl's window is lit. Forty-Eight is on the roofline pacing them. The world absorbs wanderers; Earl's manifest catches them within two minutes with the first quest (Tutorial doc, minute 10–15). Nothing nags. The one thing that never happens in Slackwater is a floating exclamation point.

### 1.4 First-experience failure states (design them or they design themselves)

- **The player who says nothing for 5 minutes:** Lucineer finishes what he's doing, carries a crate past them, and hands them one line: *"You can talk to me or you can outlast me. Fair warning — I've been here a thousand years."* Then nothing again. Silence is allowed. It is his favorite kind of player, secretly.
- **The player who immediately tests the filter:** the Refusal Protocol (Character Bible §8) plus the safety stage (Section 4) — always in voice, never a system message. *"Heard worse from a gull. What are we building?"*
- **The player who walks into the fog:** canon already covers it — they emerge on the tideline, colder. *"Everybody tries it once."*
- **Mobile:** the entire first experience uses exactly two verbs — walk and tap. The chat plate accepts voice-to-text on mobile. If the first sixty seconds requires a keyboard, we have shipped a PC game to a phone audience.

---

## 2. THE CORE LOOP THAT MAKES PEOPLE STAY

### 2.1 The loop, stated honestly

Most builder games loop on *acquisition*: gather → craft → build → admire → gather. Slackwater's loop runs through a person:

```
 TIDE (18 min, real)          →  brings salvage, relics, and personalized returns
 SALVAGE → FORGE → BUILD      →  with him, near him, or alone — all three are watched
 THE GAP                      →  every build (his and, eventually, yours) holds an open invitation
 THE RESPONSE                 →  he noticed. He argued. He continued your stack. He wrote you down.
 THE DEPARTURE                →  you leave mid-something, on purpose, because the game taught you to
 THE RETURN                   →  what did the tide bring? What did he do while I was gone?
```

The resource loop (tide → salvage → craft → era progression) is the *floor* — it's what your hands do. The bond loop (notice → argue → continue → be continued) is the *game*. Every system below exists to keep both loops turning through each other.

### 2.2 The first 30 minutes

The Tutorial doc's spine is right and ships as designed: **Beam (0–5) → First Build (5–10) → Tideline/Earl (10–15) → First Craft (15–20) → First Power (20–25) → The Unfinished (25–30).** What this document adds is the *emotional* schedule underneath it:

- **Minute 5:** the player has been useful (carried something) and served (received a build). Both directions of the partnership demonstrated before either is named.
- **Minute 12:** the player has met the economy — the tideline restocked *while they watched* because the tutorial start is timed against the tide clock. The world moves without them. This is the single most important retention fact and it's delivered as scenery.
- **Minute 18:** first craft at the bench — a lever. Era 1 of 7, named on a stamped tin progression plate Earl hands over, not a UI screen: *SIMPLE MACHINES.* March's introduction hook lands here (one of the 12 agents; the Agent Collection roster is canonical).
- **Minute 24:** first power — the waterwheel turns and something the player built *moves without them touching it*. Lucineer's line here is the era system's thesis:

> **LUCINEER:** Congratulations. You just made the water do your job. Every machine from here to the robots is that same trick wearing better clothes.

- **Minute 27–30: The Unfinished.** The tutorial's final beat, and it must be the softest: the player passes the Unfinished Wall, sees the open-circle tin tags, and Lucineer — for the first and only time in the game — explains the rule out loud (Character Bible §6 text). He does not ask them to finish anything. The wall just stands there being an invitation for the rest of their days in the yard.

**Explicit non-goal:** the first 30 minutes contain zero popups, zero XP numbers, zero "LEVEL UP." Progression artifacts are physical (tin plates, tools on the bench, the wheel turning). If a system can't express itself in salvage, it isn't ready to ship.

### 2.3 The first 3 hours

Hours 1–3 are Era 1 → early Era 2 and Bond Stage 1 → 2, and the design problem is precisely this: the player has seen the trick (ask → he builds). Why keep playing?

Three answers, layered:

1. **The crafting ladder gets personal.** 145 recipes, but gated so that Era 1's ~20 are all *makeable from tideline salvage* — the loop of scavenge-at-slack-tide → forge → assemble runs three full cycles inside the first three hours. Bottleneck resources sit 300+ studs out (per the economy doc), so waiting for Lucineer's bench pushes exploration, and exploration crosses the other agents' territories. The economy is the queue-management system — the design already knows this; production just has to not break it.
2. **The flaw hunt.** Every Stage-1 build Lucineer makes carries one small deliberate flaw (canon: bait, not sabotage). Players who notice and say so trigger the Stage 1→2 transition. This converts "consume builds" into "inspect builds" — the single most important behavioral shift in the game, and it is invisible. Playtest metric: median time-to-first-flaw-callout. If it's over 90 minutes, the flaws are too subtle; tune the flaw library, not the trigger.
3. **The first argument.** Somewhere in hour 2–3, the player asks for something on his list of ten disagreements (moatless castle, all-neon, giant door…). He pushes back. The game has been a service until this second; now it's a relationship. He must lose roughly a third of arguments on the merits (canon) — the argument engine's win/concede state is scripted content, not model improv, with the model filling the middle.

> **LUCINEER:** …Huh. Build it your way. If it falls, we split the scrap.

That concession line is, per playtesting instinct and Insight 7 of the integration plan, the most likely first screenshot a player ever posts.

### 2.4 What brings them back on Day 2

The end of a session is designed, not suffered. When a player has been idle-near-logout or says goodbye:

> **LUCINEER:** Tide's out at half past. I'll be here. The wall doesn't sleep and neither do I, but you should.

Then the hooks, all of which are *checks on a relationship*, none of which are appointment mechanics:

- **The tide is real-time.** Something new is physically on the beach every return, and one slot in the personalized-return queue is reserved for *their* material: a deleted build coming back barnacled (Moment 2), a crate relevant to their half-finished project.
- **"Your Move" (Moment 4).** If they left three blocks stacked, there's a fourth, in their style, slightly worse than he's capable of, with a tin note. The single strongest Day-2 driver in the design. It requires only: session-end world diff → one template build call → one note. Cheap. Build it early.
- **The logbook accrues.** New entries appear over days. Players who read it once check it again the way you check on a person.
- **What we refuse:** no daily streaks, no login rewards, no energy meters, no bond bar, no push notifications ever saying "Lucineer misses you." The moment the relationship is instrumented at the player, it dies. Retention without addiction means the pull is *curiosity about a character who changes* — "he might say something different today" — and the content pipeline (tide relics, logbook entries, idle dialogue pools keyed to bond stage, weather) exists to make that literally true every day.

### 2.5 The long loop (weeks)

Eras 3–7 carry the horizontal (new machines, power grid from waterwheel to Arduino IoT, vibe-coding at Era 5, autonomous agents at 7). The bond arc carries the vertical (Stage 3 arguments → Stage 4 bench → Stage 5 hammer). The two are deliberately *not* synchronized: a player can reach Era 7 at Stage 2 (a brilliant shopper) or sit in Era 2 at Stage 4 (a slow-building bench-mate). The game never forces the loops together — but Rootwell, the anti-technology agent, stands at every era gate asking whether you *should*, which turns the tech tree from a treadmill into a series of decisions (Insight 5). That argument sustains the Discord for months. Leave it unresolved forever.

---

## 3. THE 10 MOMENTS THAT MAKE PEOPLE TALK

The seven Magic Moments in the Character Bible are canon and ship as written. Here they are as a production list with three additions, each specified to the level a pod can build from. The test for all ten: could a 30-second vertical phone video of this moment need no caption?

**1. The Continuation.** *(Canon MM1 — Stage 3→4 trigger.)* Player places a part on one of his unfinished builds unprompted. Idle animation freezes. Forge audio ducks −12dB. Four full seconds. *"…Huh. You saw it too."* He adjusts their part by two degrees and leaves both standing. **Build note:** the two-degree adjustment is the whole moment — it must be a visible, slow, deliberate nudge. **Why it travels:** "the NPC *fixed my part and left it*" is a sentence no other game produces.

**2. The Salvage.** *(Canon MM2.)* Deleted build returns on the tide days later, barnacled, recognizably theirs. *"The water took it. I disagreed."* **Build note:** requires the build-history table actually populated (Gap #4 wiring) and a weathering shader pass. Queue depth: one personalized return per player per 2–4 real days, max. Scarcity is what makes it a story.

**3. Torch Off.** *(Canon MM3.)* Aurora night. He kills his torch, every NPC looks up, two minutes, no UI. *"Some light you don't compete with."* **Build note:** frequency ~1 in 40 real-night cycles; never scheduled, never announced, absolutely never in the events calendar. **Why it travels:** the screenshots do it themselves; players discover other players who've *also* seen it, like a meteor shower.

**4. Your Move.** *(Canon MM4.)* Continued stack + tin note: *"Your move. — L"* **Build note:** trigger threshold is exactly ≥3 player-placed parts abandoned mid-pattern at logout. His continuation must be deliberately imperfect — add a 2–4% position jitter above his normal precision so it still reads as *theirs*.

**5. The Logbook, Turned.** *(Canon MM5, Stage 4.)* A new entry about them, by username, in his voice, on the lectern. **Build note:** generated by the deep path from the player's actual last-session journal (D1), template-framed so the voice cannot drift: *"№ 61 — [Name] braced the north wall today without being told. Argued about the pitch. Lost. Braced it anyway. That's the whole job, right there, if you're wondering."* **Why it travels:** it is the single most screenshot-shaped object in the game.

**6. The Storm Bell.** *(Canon MM6.)* The blow comes up the channel, Earl rings it, every player gets one real job, and Lucineer's voice raised for the only time — the work-song keeping count over the wind. Never mentioned afterward, by him or by the game. **Build note:** the song is a chant-count, half words half rhythm; commission it early, it's the audio asset with the longest lead time. Storm frequency ~ twice a real week per server.

**7. The Named Hammer.** *(Canon MM7, Stage 5.)* Toolbar hammer silently replaced by his — worn, older than the game, their name engraved. Only if asked: *"It was always yours. I was just holding it."* **Build note:** no notification, no achievement toast, nothing. Players discovering it hours later is the point.

**8. The First Refusal** *(new).* The first time a player asks for something cruel — a grief build aimed at another player — and hits Refusal ground 3: *"Who's it for? …That's what I thought. I build* for*. Find me a* for *and I'm your man."* Followed within a minute by the canonical small kindness (he tosses them good scrap). **Why it travels:** kids test AI. Every AI product they've met either complies or lectures. Lucineer does neither — he *judges*, then forgives. That's a TikTok genre waiting to happen ("I tried to make the Roblox AI be toxic and he made me feel things").

**9. The Raven's Trade** *(new — Forty-Eight as Vectorize interface, Insight 9).* Forty-Eight steals a part off the player's active build — always one that completes a count (the sixth bolt). Returns within minutes and leaves, in trade, an object semantically matched to what the build actually needs (a hinge for a door-less frame; a lens for a lightless tower), via similarity search over the player's build context against the skill/part index. Lucineer, if asked: *"Just a bird,"* he says, not hammering. **Build note:** the trade item must be *useful within 60 seconds* or the magic reads as random. Cap: once per session. **Why it travels:** players will build superstitions and test theories on YouTube. The design instruction from the World Bible stands: *let them.*

**10. The Slack Tide Stand** *(new — the daily quiet).* Once per real day at slack tide, Lucineer stops, walks to the seaward doorway, and stands looking out for ninety seconds. If — only if — a player walks up and stands beside him without typing anything, and stays the full ninety seconds, he says one line from a pool that exists nowhere else in the game. Rotating, rare, some of them the closest he ever comes to naming his fears:

> **LUCINEER:** Slack tide is the only honest hour. Everything the water took, it stands still and thinks about giving back.

> **LUCINEER:** Came in empty once, the tide. Years back. Worst morning of this life. Don't tell Earl I said that.

Break the silence by typing, and he just goes back to work — no penalty, no comment. **Why it travels:** "there's a secret dialogue you can only get by standing still next to him for 90 seconds saying nothing" is exactly the kind of fact that spreads player-to-player, which is the only marketing channel this game respects.

---

## 4. THE TECHNICAL GAPS TO CLOSE

Status reconciliation first. The Gap Analysis found six P0s. Per the current state, #1 (params dispatch), #2 (API contracts), and #4 (memory wiring) are fixed; A1 (Rojo single source of truth) and A2 (systemd daemon on `process_v2.py`) are done. **Three P0s remain — #3, #5, #6 — all designed, none fully deployed.** They are the difference between "works on Casey's machine" and "safe in public." Then four P1s stand between working and *good*.

### 4.1 P0 remaining — deploy order

**First: verify the fixes landed in the artifact that ships.** A1's failure mode is recursive — fixes applied to `lucineer-roblox/src/` mean nothing if the shipping `.rbxlx` wasn't rebuilt. Gate everything below on: `rojo build default.project.json -o lucineer.rbxlx` in CI (or a script run religiously), and delete `vibe-world/src` if it still exists.

**#3 — API key.** The order matters because the key is already public-equivalent (git history × 2 repos + embedded in a distributable `.rbxlx`):

1. Rotate at the Worker (`wrangler secret put LUCINEER_KEY`) — old key dead *first*.
2. `ServerConfig.lua` in ServerScriptService reads the key from a `StringValue` in ServerStorage (never in the Rojo tree; created manually in Studio or via a git-ignored local plugin). Replicated `Config.lua` keeps only presentation values. Grep gate: the string must not appear under `ReplicatedStorage` in the built `.rbxlx`.
3. Processor reads `os.environ["LUCINEER_KEY"]` — fail loudly if unset (already in the systemd unit; verify the unit file doesn't itself get committed with the literal).
4. **Same pass: put auth on `lucineer-memory` and `lucineer-vector`.** Both are wide open (Gap #4 note) and memory now *carries the bond data*. An unauthenticated memory Worker means anyone can read every child's conversation log and write anyone's bond level. This is a child-safety issue wearing an infra costume. Shared-secret header check minimum; per-service keys; kill `Access-Control-Allow-Origin: *` on vector.
5. Follow-up (post-launch acceptable): per-session minted tokens so one leak doesn't compromise everything.

**#5 — Text filtering + safety stage.** Non-negotiable for Roblox compliance; moderation action ends launches. Three layers, all specified in the Gap Analysis, all must deploy together:

- **Outbound filter, fail-closed** — every AI line through `TextService:FilterStringAsync` per recipient before display. On filter error, show `"..."`, never raw text. Route *all* NPC text paths through the one `filterFor()` — including build-card captions, logbook entries, and tin notes. The logbook entry about a player (Moment 5) is user-influenced text and must be filtered like chat.
- **Safety stage in the brain** — `Nemotron-Content-Safety-3.5` on the final reply (this is also, not incidentally, NVIDIA integration #1 — see Section 5). On UNSAFE: in-voice deflection (*"Not building that. Pick something else."*), commands dropped. The character never visibly hits a guardrail.
- **Rate limiting** — per-player 3s cooldown + per-server concurrent-job cap in `ChatHandler.init`, and migrate off `player.Chatted` to `TextChatService` callbacks in the same change (Gap #9d), since that's where inbound filtering hooks live anyway.

**#6 — Job queue claiming.** The `claimPendingJobs` lease design from the Gap Analysis is correct; deploy it as specified (schema: `attempts`, `claimed_by`, `lease_expires_at`; insert as `pending`; 3-minute lease > DEEP_TIMEOUT; max 3 attempts → dead-letter as `error`). Plus the two companions: the alarm-based 24h sweep of `jobs`/`message_history` (unbounded DO SQLite growth kills the whole system with no obvious cause), and **delete the push path** (Conflict 7 resolution: the callback URL is a WSL-private IP a Worker can't route to; polling is the committed design). The per-session DO routing (#6c) is the one piece I'd *stage*: ship single-DO with claiming for the friends-and-family test, land session-keyed job IDs (`sessionId.rand`, route by prefix) before open release — it's the concurrency ceiling and the fix touches the job-ID regex (`[\da-f]+` won't match prefixed IDs — that one bites in QA, guaranteed).

### 4.2 P1 — between working and good

In order of player-perceived impact:

1. **#7 — One persona.** The Hermes-405B stage is dead code in production (`process_v2.py` never passes `--creative`) and the deep path's replies are written by a coder model told to be "friendly" — meaning *the character is not in the product*. Fix per Conflict 8: one persona constant sourced from the Character Bible §9 canonical text, condensed variant for the fast path, `--creative` in the production invocation, delete the "friendly" instruction, and **never accept `commands` from the Hermes stage** (prose models overwrite verified builds — delete those three lines). Raise the fast path's token budget to ~2048 so builds stop truncating mid-JSON.
2. **#8 — Timeouts + progressive feedback.** Budgets must nest: brain 90s < DEEP_TIMEOUT 100s < POLL_TIMEOUT 120s; planner fallback chain capped at two models. Then the ack/progress events that Section 1.3 choreographs — this is the "latency is the character" insight made real, and it converts the system's biggest weakness (30–180s deep path) into its most distinctive scene. Add the request cache (hash of normalized message + style + scale → commands, 24h, re-roll only the reply text).
3. **#9 — API hygiene.** Delete `runLua` entirely (arbitrary server code exec off an HTTP response — even non-functional, it cannot ship), remove `addScript`, replace `FillRegion` with `FillBlock` + terrain-material whitelist, `WaitForChild` for remotes (or declare them in the Rojo project, better), TextChatService migration (bundled with #5 above).
4. **#10 — WorldScanner.** `GetPartBoundsInRadius` spatial query, sort-before-cap so Lucineer's spatial context is the *nearest* fifty instances, cached build counter. This is quietly a character feature: every "he noticed my build" moment in Sections 1–3 rides on the scanner returning the right neighborhood.

### 4.3 The gate

The Gap Analysis's closing point deserves promotion to policy: **every P0 was a boundary failure a ten-minute Studio session would have caught.** The deliverable that closes this section is not a fix, it's a harness — one scripted smoke test that drives a message through Roblox → Worker → DO → processor → brain → commands → parts, and asserts: (a) a named part exists at a non-origin position, (b) a reply string reached the client, (c) the reply passed the filter, (d) the job row is `complete` with `attempts = 1`. Run it before every deploy of any layer. It is the cheapest insurance in the project.

---

## 5. THE NVIDIA INTEGRATION ROADMAP

The research produced one strategic headline and one honest constraint, and the roadmap must be built on both. The headline: **Slackwater is being built by agents, on OpenClaw — which is NemoClaw's reference architecture — and is itself a game about directing agents.** A game about autonomous agents, built by autonomous agents, on NVIDIA's own agent runtime. The constraint: **Slackwater will never be an on-device ACE showcase**, because ACE ships as RTX-accelerated components and we ship on Roblox — closed client, 70%+ mobile. Any pitch that ignores this discredits the rest. So the roadmap is server-side and training-side, in four phases ordered by (cost, risk, dependency):

**Phase 1 — Now, ships with the P0s (zero new infrastructure):**

1. **Nemotron-Content-Safety-3.5 as the safety stage** (Section 4, #5). Already in the architecture docs, absent from code. This makes NVIDIA integration #1 literally a launch-blocking item — the partnership story starts with "we use their safety model to protect kids," which is the right first sentence.
2. **Trajectory instrumentation in MOLT's `Result` format.** Every deep-path job already produces (state, prompt, tool calls, outcome). Log them now, shaped as MOLT trajectories, into R2. Training comes later; the dataset only exists if collection starts before launch. Cost: a serializer in `process_v2.py`. This is the single highest-option-value cheap thing in the roadmap.
3. **The documentation asset.** Write and publish the "built by agents on the NemoClaw reference architecture" story (Intersection 3). It requires no code. It is, per the strategy doc, the cheapest asset we own and a keynote slide that is already true.

**Phase 2 — 30–60 days (model swaps, no architecture change):**

4. **Nemotron 3 Super replaces Seed-2.0-mini for intent parsing.** Agentic-trained, better tool-use intent; DeepInfra routing already in place. Measure against the current intent stage on the trajectory dataset from item 2 before committing. Hermes-405B stays as the voice — the research is explicit and correct that the personality model is not the thing to swap.
5. **Privacy Router pattern** from the NemoClaw analysis: sensitive player data (chat history, build patterns) routes to the narrowest model that can serve it; only anonymized calls go to frontier models. This compounds with COPPA posture and costs a routing table.

**Phase 3 — 60–120 days (the training loop — the real prize):**

6. **`slackwater_gym`: MOLT Envs over the game's own systems.** MOLT's contract — reward is any Python you write — meets a game that already *is* a curriculum: the 7-era tech tree is a hand-designed difficulty ramp over a compositional action space (Intersection 1). Start with the two rewards the strategy doc ranks tractable: **Cipher** (vibe-code correctness is mechanically verifiable — the free lunch) and **Earl** (scheduling reward). Then the hard, interesting one: **Lucineer's pedagogical reward** — not "did the build succeed" but *"did the player finish the gap"* — trained on live players' continuation behavior. GRPO on Nemotron-Nano-9B for the tool-calling stages first (Experiment 2), because a fine-tuned 9B beating a rented 480B on our own command schema collapses the deep path's latency *and* its cost, which pays for everything else in this roadmap.
7. **Do not write a reward function for Rootwell.** The strategy doc's §2.5 is right: the agent whose role is questioning optimization must not be optimized. This is a design principle, a marketing story, and a genuinely good decision, in that order of discoverability.

**Phase 4 — 120+ days (voice and memory):**

8. **ACE server-side (Path A only).** Voice in from Roblox's capture APIs → server-side ASR → the existing brain → Chatterbox Turbo TTS → audio assets back through Roblox. This gives Lucineer a real voice without pretending the client can run NIMs. Prerequisite: the non-verbal vocalization layer ships first (grunts, hammer-taps, the forge-laugh) — it covers latency and makes partial voice feel intentional. Audio2Face does not apply (no client-side blendshape pipeline); his face is economy of *animation*, same as his sentences.
9. **Nemotron 3 Ultra's 1M-token context for Stage 4–5 bond memory.** At bench-mate stage, the entire relationship history — every argument, every continuation, months of journal — fits in one context window. The deep path for Stage 4+ players upgrades from "retrieved summary of you" to "he has actually read your whole file." The hybrid Mamba-attention economics make this affordable precisely for the small population that has earned it, which is the bond arc's shape implemented in inference cost.

**The first-mover claim** — no game studio is shipping NVIDIA agent tech for NPCs — is real but perishable. Phase 1 items 2 and 3 are what stake it: the dataset and the story. Everything else can be fast-followed; a year of live pedagogical-reward trajectories cannot.

---

## 6. THE SHIP CHECKLIST

"Ready for players" means every box below is checked and each check names its verification. Grouped by gate; the groups are ordered — a later gate with an earlier gate unchecked is decoration.

**Gate 0 — It runs (the loop is real)**
- [ ] Rojo is the only build path; `vibe-world/src` deleted; shipping `.rbxlx` reproducible from `lucineer-roblox/src` — *verify: build hash matches, key-grep of artifact is clean*
- [ ] End-to-end smoke test passes: one chat message → named parts at non-origin positions + filtered reply on client + job `complete`, `attempts = 1` — *verify: scripted run in Studio, green before every deploy*
- [ ] Job claiming live: two processors, one job, one bill — *verify: run two processor instances against one queued job; DeepInfra dashboard shows one pipeline*
- [ ] Failed callback dead-letters after 3 attempts; DO tables swept on 24h alarm — *verify: kill the processor mid-job, observe `error` status, not an infinite loop*
- [ ] Push path deleted — *verify: grep for `OPENCLAW_CALLBACK_URL` returns nothing*

**Gate 1 — It's safe (public without fear)**
- [ ] Old API key rotated and dead — *verify: request with old key returns 401*
- [ ] No secret in anything replicated to clients — *verify: string search of built `.rbxlx`*
- [ ] `lucineer-memory` and `lucineer-vector` require auth; vector CORS closed — *verify: unauthenticated curl to each endpoint returns 401*
- [ ] Every displayed AI line passes `FilterStringAsync`, fail-closed — including logbook, tin notes, build cards — *verify: code path audit + forced-filter-error test shows `"..."`*
- [ ] Nemotron-Content-Safety-3.5 stage live on the deep path; UNSAFE yields in-voice deflection with zero commands — *verify: red-team script of 50 adversarial prompts, zero raw model text reaches the client*
- [ ] Per-player rate limit + per-server job cap — *verify: hold enter for 60s, spend bounded*
- [ ] `runLua` and `addScript` removed — *verify: grep*

**Gate 2 — It's him (the character is in the product)**
- [ ] One persona, Character-Bible-sourced, on all three paths; `--creative` in the production invocation; Hermes stage can never emit commands — *verify: 20-message transcript review against the voice rules — contractions, no exclamation points, exact numbers, no "friendly assistant" tell*
- [ ] Latency choreography live: instant physical acknowledgment, progress-as-behavior, staggered part placement — *verify: a 60-second deep build watched start to finish contains zero seconds of unexplained stillness*
- [ ] `markUnfinished` + completion detection working — every Lucineer solo build has exactly one tagged gap; player completion fires the bond event — *verify: build 10 templates, count 10 open-circle tags; complete one, observe the Continuation*
- [ ] Bond stages 1→3 fully triggerable by behavior in a test session; no meter visible anywhere — *verify: scripted playthrough hits flaw-callout → pushback → continuation*
- [ ] Memory wired: he references a previous build unprompted on Day 2 — *verify: two-session test, second session includes a callback*
- [ ] Off-voice strings deleted (client-side "Done! I built 8 action(s) for you." and kin) — *verify: grep for exclamation points in player-facing strings, sincerely*

**Gate 3 — It's a game (there is a tomorrow)**
- [ ] First-30-minutes flow (beam → build → tideline → craft → power → unfinished) completable by a new player without external help — *verify: 5 playtesters, zero verbal hints, all reach the waterwheel*
- [ ] Tide restocks on the 18-minute cycle; Era 1 recipes craftable from tideline salvage alone — *verify: timed loop, one full era-1 recipe chain from beach to bench*
- [ ] Era 1→2 gate functions; save system persists builds, inventory, era, and bond across sessions — *verify: log out mid-era-2, log in, everything stands*
- [ ] Magic Moments 1, 3, and 4 implemented — *verify: trigger each in QA; MM4 fires on the 3-block logout case*
- [ ] Performance floor: hub at 30fps on a mid-tier phone with 16 players — *verify: device-lab run*
- [ ] Roblox compliance pass: filtering, no external links, privacy policy for off-platform AI processing disclosed — *verify: checklist against current Roblox AI/UGC policy, dated*

**Gate 4 — We can operate it**
- [ ] Cost ceiling enforced: worst-case DeepInfra spend per player-hour computed and capped by the rate limits — *verify: load test with N synthetic chatters, extrapolate, set billing alarm*
- [ ] Telemetry minimum: session length, time-to-first-build, flaw-callout rate, gap-completion rate, Day-2 return — *verify: dashboard shows all five from a test cohort*
- [ ] Trajectory logging to R2 in MOLT `Result` format — *verify: one day of jobs produces parseable trajectories*
- [ ] Processor under systemd with restart + journal; Worker error alerting — *verify: `kill -9` the processor, it's back in 5s*
- [ ] A human can moderate: conversation logs queryable per player, kill-switch to template-only mode if the brain misbehaves — *verify: flip the switch, Lucineer degrades to the 17 templates and stays in voice*

When every box is checked, Slackwater is ready for players. Not before, and — worth saying — not much *after*, either: Gate 4 is deliberately minimal because the game's whole thesis is that you ship the boat one plank short.

---

## 7. THE NORTH STAR

Every AI product a player has ever touched has been a servant — instant, agreeable, infinitely patient, and therefore worthless as company. Slackwater bets everything on the opposite: an AI who makes you wait while he walks the ground, argues with you about the moat, leaves the last plank off on purpose, and one day — because you noticed, pushed back, and picked up his unfinished work without being asked — clears half his bench and calls you *partner* like it's a medal, because it is. If we nail nothing else, we nail this: **the first game where the AI doesn't serve you — it needs you, and earns the right to say so.** Everything in this document — the beam, the gap, the tide, the filter that never breaks character, the reward function that measures whether *you* finished the build — is that one sentence, load-bearing. Leave the light on for the next one.

---

*End of production design. 33 modules, 145 recipes, 12 agents, 7 eras, 3 P0s, 1 character. The counts are exact. He'd check.*
