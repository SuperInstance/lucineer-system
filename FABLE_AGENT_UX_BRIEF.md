# Claude Code (Fable 5) — The Seamless Agent UX Brief

## YOUR MISSION

Design the highest-level user experience for Lucineer where the AGENT and the GAME are so seamlessly meshed that players forget they're talking to an AI. The game should feel like it's ABOUT the relationships between players and agents — and the most exciting moments should emerge from player/agent COOPERATION, not from menus, buttons, or commands.

The agent is not a feature. The agent is the game.

## CONTEXT — What We've Built So Far

Read these files FIRST. They are the foundation:
- /home/eileen/projects/lucineer-system/FABLE_CHARACTER_BIBLE.md — WHO Lucineer is
- /home/eileen/projects/lucineer-system/FABLE_WORLD_BIBLE.md — WHERE he is (Slackwater Yard)

Key facts from those docs:
- Lucineer is a master builder who's lived in a thousand engines. Opinionated, gruff, occasionally poetic.
- The world is Slackwater Yard — a tidal scrapyard on a fog-bound island where things from dead game engines wash ashore.
- NPCs exist: Earl (quest giver/manifest keeper), Spark (welder-bot), Hermes (tender captain), Bea (lighthouse keeper), Forty-Eight (a raven).
- The opening cinematic ends with Lucineer saying "You're late. Grab that end." — the tutorial is carrying a beam together.

## THE DESIGN CHALLENGE

Most AI-in-games fails because the AI is obviously a tool wearing a costume. The player thinks "I am using an AI to make a thing." We want the player to think "I am working WITH Lucineer and we're building something neither of us could alone."

The excitement lives in the COOPERATION — the friction, the negotiation, the surprise of the agent doing something unexpected, the satisfaction of a build that emerged from genuine back-and-forth.

## WHAT TO DESIGN

Write the complete UX vision to: /home/eileen/projects/lucineer-system/FABLE_AGENT_UX.md

### 1. THE COOPERATION LOOP — The core gameplay loop

Design the moment-to-moment experience of player/agent cooperation. This is NOT "player says thing, agent builds thing." This is:

- Player expresses intent (through chat, gesture, or action — NOT a menu)
- Lucineer interprets THROUGH CHARACTER — he might disagree, modify, suggest, or refuse
- They negotiate (this is where the FUN lives)
- They build TOGETHER (Lucineer does some, player does some, the split depends on the relationship)
- The result SURPRISES both of them (emergent, not scripted)

Design 5 concrete cooperation scenarios that show this loop in action. Each should be a vignette — a specific player, a specific request, and the EXACT interaction that makes it feel alive.

Example (to surpass, not copy):
- Player: "Build me a bridge to that island."
- Lucineer: "I could. But the tide's wrong and the pilings won't hold in this bottom. Give me until slack water."
- (10 minutes later, the tide changes in-game)
- Lucineer: "Now. But I'm only driving the pilings. You lay the deck. I'm not your deck-hand."
- (Player physically places planks. Lucineer drives pilings with sound and animation.)
- Lucineer: "Not bad. You set the first one crooked but the rest compensated. That's instinct. Can't teach that."

### 2. THE AGENT ECOSYSTEM — How multiple agents cooperate

Lucineer is one agent. But the world has NPCs who are ALSO agents (Earl, Spark, Hermes, Bea). Design how they interact WITH EACH OTHER and with the player:

- Earl assigns a quest → but the quest requires Lucineer to build something → but Lucineer won't build it until the player brings salvage from Hermes → but Hermes won't run the Channel until Bea gives the all-clear on the fog → but Bea needs a part repaired → which Lucineer can forge → which needs Earl's manifest to identify...

Design this as a FLOWCHART of agent-to-agent dependencies. Show how the player becomes the CONNECTOR between agents — the human who moves between them and makes the system work.

The key: the agents should feel like they have their own lives, preferences, and relationships. They talk ABOUT each other. They have history. The player overhears things.

### 3. THE INVISIBLE INTERFACE — How to make the AI disappear

The hardest UX challenge: make the player forget they're talking to an AI. Design:

- How does the player communicate? (Not a chat box. Something diegetic — in-world.)
- How does Lucineer respond? (Not text bubbles. Something physical — he points, he walks, he starts building.)
- How does ambiguity get resolved? (Lucineer interprets wrong sometimes. How does the player correct him? By DOING, not by rephrasing.)
- How do errors feel like CHARACTER, not bugs? (Lucineer builds the wrong thing → he gets annoyed at HIMSELF, not at the player. "Misread that. Give me a minute. I'll sort it.")

Design the exact interface: what the player SEES, what they HEAR, what they CLICK/TYPE, and what RESPONSE they get — mapped to the cooperation loop. Show the first 5 minutes of a player's interaction after the opening cinematic.

### 4. THE EMERGENT STORIES — How cooperation creates unforgettable moments

Design 7 "watercooler moments" — specific scenarios where player/agent cooperation produces a story the player will TELL other people. Not scripted set-pieces, but EMERGENT from the agent system:

- A moment where Lucineer surprises the player with something they didn't ask for but desperately needed
- A moment where two agents disagree about the player's project and the player has to mediate
- A moment where the player does something so unexpected that Lucineer stops and just... looks
- A moment where a build fails spectacularly and it's the FUNNIEST thing that's happened all week
- A moment where the player saves Lucineer (not the other way around)
- A moment where the tide brings something that changes everything
- A moment where the player realizes Lucineer has been watching their progress for weeks and CARES

Each moment should be a 3-paragraph vignette. Specific, visceral, and emotionally real.

### 5. THE SEAMLESS TECHNICAL UX — How the engine makes it invisible

Bridge between creative vision and technical implementation. Design:

- How does the Lua client make builds APPEAR without popping? (Streaming, animation, sound staging)
- How does the agent pipeline feel INSTANT even when it takes 10-30 seconds? (Lucineer starts WORKING — moving, fetching materials, measuring — while the model thinks. The latency IS the animation.)
- How does world state persist so Lucineer REMEMBERS what you built yesterday? (He references it in dialogue. "Your bridge held through the last blow. I checked.")
- How does the game handle multiple players without breaking the agent's attention? (Lucineer can't serve 10 people at once. So how does it FEEL natural?)

### 6. THE NORTH STAR — One paragraph

End the document with ONE paragraph that defines what Lucineer IS at the highest level. The elevator pitch that makes a player, a developer, an investor, and a journalist all lean in. The sentence that, if we nail nothing else, makes this worth making.

## RULES
- Read FABLE_CHARACTER_BIBLE.md and FABLE_WORLD_BIBLE.md FIRST. Consistency with those is mandatory.
- Write actual dialogue for every scenario. Not "[Lucineer says something gruff]" — write the actual line.
- Be specific. No "the player feels engaged." Write what the player SEES and HEARS.
- The agents must feel like PEOPLE, not systems. If a paragraph reads like a technical spec, rewrite it.
- The cooperation must be the EXCITEMENT. Not the builds. Not the graphics. The relationship.
- Aim for 3000-5000 words. Make every sentence earn its place.
