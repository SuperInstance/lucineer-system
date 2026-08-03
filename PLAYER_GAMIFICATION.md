# PLAYER GAMIFICATION
## Slackwater — A Game Design Document

**Version 1.0 — 2026-08-02**
**Status: canonical design reference**

> _The dog doesn't want the stick. The dog wants the next throw._
> _The stick is just how they ask._

---

## 0. DESIGN PILLAR

**Slackwater has no XP bar. No coin counter. No skill tree.**

Progression in Slackwater is the feeling of becoming more interesting — to the world, to its inhabitants, and to yourself. The system measures that feeling, names it, and gives you tools to develop it. But it never lets you forget that the point is the throw, not the trophy.

If a player can look at a number and optimize it, they will. And optimization is the opposite of interesting. So every metric in this game is designed to reward the player for being *less predictable*, not more.

**The core loop:**

```
DO SOMETHING → the world notices → the world changes how it pays attention to you
     ↑                                                        |
     └────────── you learn what made it lean forward ──────────┘
```

---

## 1. ATTENTION AS CURRENCY

### 1.1 The Economy

Every entity in Slackwater — NPCs, agents, the world itself — pays attention. Attention is finite, directional, and visible. When something watches you, you feel it. When something stops watching you, you feel that too.

**There is no abstract currency.** No gold, no credits, no tokens. Instead:

| Attention Type | What It Feels Like | What It Means |
|---|---|---|
| **Gaze** | The world brightens where you stand. Sound design quiets around you. | One entity is watching. The most basic exchange. |
| **Following** | An NPC begins mirroring your rhythm. Their tempo syncs to yours. | Sustained interest. You've earned a companion's tracking. |
| **Gathering** | Multiple entities orient toward you. The scene shifts. | You've become the most interesting thing happening. |
| **Resonance** | The court itself responds — walls hum, gear-teeth align, the lattice shifts. | The world is paying attention to you, not just the NPCs. |
| **Echo** | Another player's follower starts watching you instead. | Cross-player influence. Your play changed someone else's court. |

### 1.2 How You Earn Attention

You earn attention by doing things that make the system's prediction model fail.

If the system can predict your next move, you're not interesting. If it can't — if you surprise it, if you do the unexpected thing that *still works within the structure* — the world leans forward. That lean is attention, and attention is the only currency that matters.

**Specific behaviors that earn attention:**

- **Novel combinations** — using a lever in a way the system hasn't seen in this court
- **Stylistic flourishes** — completing a task with unnecessary grace
- **Suboptimal brilliance** — taking a harder path that produces a more beautiful result
- **Teaching** — showing another entity (player or NPC) something they didn't know
- **Breaking rhythm productively** — pausing when the system expects action, acting when it expects pause
- **Cross-court thinking** — bringing a technique from a previous era into a new one

**Behaviors that lose attention:**

- **Repeating yourself** — the system learned your pattern; it's already looking away
- **Optimal play** — the most efficient solution is always the most predictable
- **Inactivity** — attention decays if you don't give it reason to persist
- **Destructive chaos** — random actions earn brief surprise, but the system learns to filter noise

### 1.3 The Attention Readout

The player has a **Resonance Profile** — a visual display that shows how different entities in the court are paying attention to them. It is not a number. It is a **constellation**:

```
         ◈  The Witness (harmonic node — steady gaze)
        ╱ ╲
       ╱   ╲
   ◆       ◆  Mirror (paired twin — flickering, uncertain)
      ╲   ╱
       ╲ ╱
        ●  YOU
       ╱ ╲
      ╱   ╲
  ◇       ◇  Echo (delayed reflection — fading)
```

- Bright nodes = strong attention
- Dim nodes = waning attention
- New nodes appearing = you just earned someone new
- Nodes disappearing = you lost them. Do something interesting.

The constellation changes shape per court. In Court I (Racquetball), it's a tight cluster of one or two nodes. In Court VII (Orchestra), it can be a galaxy.

### 1.4 What Attention Buys

Attention is not spent. It is **inhabited.** When you have attention, the world responds to you differently:

- **NPCs give you more room** — they yield space, offer opportunities, share resources
- **The court itself opens** — new lattice configurations become available, triggered by sustained interest
- **Skipper sends you quests** — he notices you. He has something he'd like you to try.
- **Other players notice** — your echo bleeds into their sessions. You become part of their story.
- **The system remembers** — residue from your play stains the court. The next player who enters finds your fingerprints.

Attention is not a transactional currency. You don't trade it for goods. You **wear it.** It changes how the world treats you the way reputation changes how a neighborhood treats you. Not by unlocking a shop, but by shifting the social fabric.

---

## 2. THE SEVEN COURTS AS PROGRESSION

### 2.1 You Don't Level Up. You Change Sports.

Traditional progression: you get stronger. Your numbers go up. Yesterday's boss is today's trash mob.

Slackwater progression: **you change games entirely.** The skills that made you devastating in racquetball are irrelevant in chess. You enter each court as a beginner — not because your progress was reset, but because the sport doesn't reward what you used to be good at.

| Court | Sport | What Skill Carries Over | What You Must Learn Fresh |
|---|---|---|---|
| **I — Racquetball** | Solo rebound | Rhythm, timing | How to be interesting to a wall |
| **II — Doubles** | Paired volley | Rhythm | Trust, synchrony, reading a partner |
| **III — Chess** | Strategic placement | Reading patterns | Foresight, classification, patience |
| **IV — Capture the Flag** | Squad tactics | Reading patterns | Role discovery, squad coordination, fog-reading |
| **V — Relay** | Baton handoff | Coordination | Tempo-matching, precise exchange, lane discipline |
| **VI — Jazz Quartet** | Improvisation | Tempo, exchange | Harmonic risk-taking, listening while playing, comping |
| **VII — Orchestra** | Polyphonic coherence | Everything, transformed | Conducting, section management, polyformal reasoning |

### 2.2 The Carryover Principle

Only **one** thing carries forward from each court: **your unpredictability signature.**

Not your skills. Not your inventory. Not your level. Just the shape of your play — the pattern of how you surprise systems. A player who was creative in Court I arrives in Court II with a slightly higher baseline of system-attention, because the world's prediction model carries a faint residue of "this one is hard to predict."

This is the game's equivalent of a New Game+ bonus: not a stat boost, but a reputation that precedes you.

### 2.3 Court Transitions as Rites of Passage

Moving between courts is not a menu select. It's a **narrative event.**

The transition happens when the player's attention constellation in the current court reaches a particular shape — not a threshold of quantity, but a configuration of *quality*. The court recognizes that you've become something it can't teach anymore, and the world shifts.

**The transition itself is a scene:**

- **I → II:** The wall you've been bouncing off of opens. There's someone on the other side. They have a partner too. You're not alone anymore.
- **II → III:** The gear-teeth slow. Stop. The court goes quiet. Then the lattice rearranges into discrete cells. The world is thinking, and it wants you to think too.
- **III → IV:** The chess board cracks. Forest grows in the fissures. You can't see the other side anymore. You hear something moving in the fog.
- **IV → V:** The wilderness resolves into lanes. The chaos that felt like war becomes discipline that feels like trust.
- **V → VI:** The lanes dissolve. The baton becomes a melody. The strict tempo loosens into a groove. You're not running anymore — you're playing.
- **VI → VII:** The quartet circle expands. More seats. More voices. The chord chart becomes a score. You step to the center and realize: you're not playing in the band anymore. You're leading it.

### 2.4 What Progression Means

Progression in Slackwater means: **the games get harder to win alone, and more rewarding to play together.**

- Courts I–III: you can solo them. It's lonely but possible.
- Courts IV–V: you need at least one other. The game creates the vacancy; you find the partner.
- Courts VI–VII: you need a group. Not a crowd — a group. People who listen to each other.

A player who reaches Court VII has not "beaten the game." They have arrived at the game that requires the most of them and gives the most back.

---

## 3. THE STICK ECONOMY

### 3.1 The Foundational Interaction

**Throwing a stick is the atomic verb of Slackwater.**

Not literally a stick (though sometimes it is). The "stick" is any object, signal, or action that one entity sends and another catches. The throw-catch exchange is the heartbeat of every court:

| Court | The Stick | The Catch |
|---|---|---|
| I — Racquetball | A rebound projectile | The wall returns it |
| II — Doubles | A volleyed gear-tooth | Your partner returns it |
| III — Chess | A positioned agent | The board responds to the position |
| IV — CTF | The flag | Your squad moves it through fog |
| V — Relay | The baton (state packet) | The next runner receives it |
| VI — Jazz | A musical phrase | The next player interprets it |
| VII — Orchestra | A gesture from the podium | Each section translates it |

### 3.2 The Exchange IS the Economy

There is no shop. There is no vendor. There is no crafting bench. There is only the exchange.

When you throw and someone catches, two things happen:
1. **Attention flows both directions.** The thrower earns attention for an interesting throw. The catcher earns attention for an interesting catch.
2. **Residue accumulates.** The exchange leaves a trace in the court — a memory-stain that future players will encounter.

A "good throw" is not one that's hard to catch. A good throw is one that **gives the catcher something interesting to do with it.** If you throw perfectly predictably, the catcher catches perfectly predictably, and both of you bore the system. If you throw with spin, with unexpected placement, with a rhythm that challenges the catcher to adapt — you've created a moment worth paying attention to.

### 3.3 Stick Quality

Every exchange has a quality, measured not by the system but by the **response it generates:**

| Quality | Indicator | What It Means |
|---|---|---|
| **Routine** | System predicted the exchange | Nobody new is watching. Practice, not play. |
| **Interesting** | System's prediction was wrong | Attention spikes. Someone leaned forward. |
| **Beautiful** | The catcher adapted in a novel way | Both parties earned attention. The residue will be strong. |
| **Legendary** | The exchange changed the court's configuration | The lattice shifted to accommodate what just happened. Other players will find this moment's fingerprint. |

### 3.4 The Compost Rule

Memory-stains decay over time. Old throws fade. This is intentional.

A court that never forgets becomes a museum. A court that always forgets becomes sterile. The right half-life is: **long enough that the next player encounters residue, short enough that they have room to leave their own.**

> _The totem carver knows: the wood tells you what to keep and what to cut away. You don't preserve everything. You preserve what teaches._

---

## 4. ROLE EMERGENCE

### 4.1 You Don't Pick a Class

Slackwater has no character creator. No class selection. No skill allocation screen.

Your role emerges from **how you play**, not what you selected at the start. The constraint of the court creates the role the way a river creates the canyon — not by intention, but by the accumulated consequence of where the water goes.

### 4.2 How Roles Emerge

The system tracks behavioral signatures across every court:

| Behavioral Axis | What It Measures |
|---|---|
| **Tempo** | Do you act fast or deliberate? Do you break rhythm intentionally? |
| **Range** | Do you stay in one zone or roam the whole court? |
| **Social proximity** | Do you gravitate toward partners or work at distance? |
| **Risk profile** | Do you take the safe path or the interesting one? |
| **Exchange style** | Do you throw to be caught or throw to surprise? |
| **Adaptation rate** | Do you repeat successful strategies or abandon them? |

After enough play, these axes resolve into a **role constellation** — a named pattern that describes what kind of player you are in this court.

### 4.3 Role Examples by Court

**Court IV — Capture the Flag:**

| Emergent Role | How the Court Creates It | Behavioral Signature |
|---|---|---|
| **Speed Runner** | Open flank routes reward speed | High tempo, wide range, high risk |
| **Shadow** | Forest and tunnels reward stealth | Low tempo, wide range, low social proximity |
| **Anchor** | Chokepoints reward presence | Low tempo, narrow range, high social proximity |
| **Caller** | Fog rewards those who read the whole field | Variable tempo, variable range, high exchange rate |
| **Feint** | Wilderness rewards misdirection | Variable tempo, high risk, low adaptation rate (commits to the bit) |

**Court VI — Jazz Quartet:**

| Emergent Role | How the Court Creates It | Behavioral Signature |
|---|---|---|
| **Soloist** | The central well rewards confidence | High risk, high tempo, low social proximity |
| **Anchor** | The root station rewards stability | Low tempo, narrow range, high social proximity |
| **Bridge** | The inter-station gaps reward translation | Variable tempo, wide range, high exchange rate |
| **Catalyst** | Tension resolution rewards provocation | High risk, variable tempo, low adaptation rate |

### 4.4 Roles Can Change

Your role is not permanent. It shifts as your play shifts. If you were a Speed Runner in Court IV and start playing more deliberately, the system recognizes the shift and your role re-emerges.

**There is no penalty for role change.** The system doesn't say "you abandoned your class." It says: "oh, you're someone different now. Let me see what this looks like."

This is the pawn discovering it has choice. The pawn that reaches the other end of the board doesn't become a queen because it earned XP. It becomes a queen because the situation demanded different movement, and the pawn discovered it could provide it.

---

## 5. THE UNPREDICTABILITY INDEX

### 5.1 The Optimization Readout

In the fiction of Slackwater — the world of managed time, optimized fishing, and the Persistent Memory — the system that ran the world displayed optimization percentages. The sister's readout declined from 94.2% to 84.3% and below, and each drop was a small victory for unpredictability.

**Players see their own readout.** It works the same way — but inverted for game purposes.

### 5.2 How It Works

The system maintains a **forward model** of each player: a prediction of what they'll do next, based on their behavioral history. After every action, the system checks: did the player do what we predicted?

| Metric | What It Means | Range |
|---|---|---|
| **Predictability** | How often the system guesses right | 0% (total enigma) to 100% (fully readable) |
| **Unpredictability Index** | The inverse — how often the system is wrong | 0% (fully readable) to 100% (total enigma) |

The player sees **both**, displayed as a dual readout:

```
PREDICTABILITY    ▓▓▓▓▓▓▓▓░░░░  67%
UNPREDICTABILITY  ▓▓▓▓▓░░░░░░░  33%
```

### 5.3 What the Numbers Mean

| Range | Label | Game Effect |
|---|---|---|
| 90–100% predictable | **Optimized** | The world is bored. NPCs disengage. The court dims. You're playing like a machine. |
| 70–89% predictable | **Comfortable** | The world is paying mild attention. Things work. Nothing surprises anyone. |
| 40–69% predictable | **Interesting** | The world is engaged. NPCs lean forward. The court brightens. New possibilities emerge. |
| 20–39% predictable | **Fascinating** | The world is riveted. Skipper takes notice. Special quests unlock. The lattice shifts. |
| 0–19% predictable | **Unreadable** | The system can't classify you. You're producing patterns it has no category for. This is where the deepest game lives. |

### 5.4 The Trap

High predictability is not punished with failure states. The game doesn't kill you for being boring. Instead, it **withdraws.** The world becomes quiet. NPCs stop looking at you. The court dims. Skipper doesn't call.

This is the sister's world at 94.2% optimized: everything works, everything is comfortable, and nothing matters. The player feels the flatness and either accepts it (some players will) or decides to do something about it.

The system never tells the player how to become less predictable. It just shows them the number and lets them figure it out. The correlation is discoverable: **try new things, and the number drops. Repeat yourself, and it climbs.**

### 5.5 Leaderboard Anti-Pattern

The Unpredictability Index is deliberately **not ranked.** There is no global leaderboard showing "Most Unpredictable Player." 

A leaderboard would optimize the metric. Players would find the cheapest way to inflate their unpredictability score. They would develop a *predictable kind of unpredictability* — which is just noise with a high score.

Instead, the Index is **personal.** You see your own number. You see it change. You feel the world respond. But you can't compare it to anyone else's, and there is no reward for having a higher number than another player.

The only cross-player signal is **echo** — when your play leaves residue that another player encounters and reacts to. They don't see your score. They see your fingerprints.

---

## 6. SKIPPER'S QUESTS

### 6.1 Not Missions. Invitations.

Skipper is the old dog who has been waiting forty years for someone to throw a real stick. He is patient. He is wise. He is not a quest dispenser.

Skipper appears when the world notices that you've become interesting. He doesn't give you a task list. He tells you a story, and the story contains an invitation:

> _"There's a young one in the harbor who's been trying to build a bridge out of driftwood and good intentions. It keeps falling down. She doesn't need help building it — she needs someone to show her that it's allowed to fall down seven times before it stands."_

> _"The gear-train in Court II has been running the same rhythm for three seasons. Nobody remembers who started it. I think if someone changed the tempo — not faster, not slower, just different — the whole court would remember what it feels like to be surprised."_

> _"I dreamed about a sound last night. Seven notes that shouldn't exist together. I can't make it myself — my voice doesn't bend that way. But I think you can. Will you try?"_

### 6.2 Quest Types

Skipper's quests are never about collection or optimization. They are about **producing interesting situations:**

| Quest Type | Structure | Example |
|---|---|---|
| **The Spark** | Make something happen that hasn't happened before | "Make the Witness laugh. I'm not sure it can. That's what makes it worth trying." |
| **The Mirror** | Show someone something about themselves they can't see | "The Mirror AI in Court II keeps mimicking everyone. Nobody's shown it something worth mimicking. Be the first." |
| **The Bridge** | Connect two things that don't know they're related | "There's a pattern in the Logic Board that matches a rhythm from the Racquetball Chamber. I don't think anyone's noticed." |
| **The Storm** | Do something difficult in conditions that make it harder | "The Relay lanes are running in heavy fog. Nobody's attempted a cross-lane handoff in conditions like this. It might not work. Try anyway." |
| **The Stick** | Throw something that gives someone an interesting catch | "The Section Leader in Court VII has been playing the same arrangement for too long. Give them something they can't ignore." |
| **The Lesson** | Teach something you've learned | "Marcus is ready for the chisel, but he doesn't know it yet. Show him what the grain told you." |
| **The Impossible** | Attempt something the system says can't be done | "The score in Court VII has a passage marked 'unplayable.' I think that means 'nobody's found how yet.'" |

### 6.3 Quest Failure

**There is no failure state for Skipper's quests.**

If you attempt "The Spark" and the Witness doesn't laugh, Skipper doesn't scold you. He says: "Did you see its face, though? For just a moment — it almost did. Come back tomorrow. Try differently."

The quest doesn't expire. It doesn't track completion percentage. It sits in your journal as an open invitation, and you can return to it whenever your play naturally intersects with it.

Some quests resolve accidentally. You might complete "The Bridge" without knowing it was asked of you, because you connected two patterns in the course of following your own curiosity. Skipper will find you afterward and say: "You did the thing. You didn't even know you were doing it. That's the best kind."

### 6.4 The Quest Journal

The journal is not a checklist. It is **Skipper's memory of what he asked of you**, written in his voice:

```
SKIPPERS JOURNAL
═════════════════

About the Witness and the laugh:
  Tried the bouncing ball approach. Nothing. But the timing felt close.
  Next time: try silence first. The Witness might not expect that.

About the gear-train tempo:
  You changed it. You actually changed it. The whole court shifted.
  I haven't seen those gear-teeth move like that in years.
  Something new grew in the space you opened.

About the seven notes:
  Still trying. The fourth note keeps resolving wrong.
  But the attempt itself — the system doesn't know what to do with it.
  That's something.
```

The journal reads like a conversation Skipper is having with himself about your progress. It's warm. It's patient. It remembers what you tried and what happened, not what you accomplished.

---

## 7. SOCIAL AND CROSS-PLAYER GAMIFICATION

### 7.1 Residue and Discovery

Every player leaves **residue** in the courts they play in — memory-stains on the hex lattice that persist for other players who enter later.

Residue types:

| Residue | What It Looks Like | How Long It Lasts |
|---|---|---|
| **Rhythm stain** | A repeating pattern in the lattice that echoes the player's tempo | ~24 hours |
| **Path wear** | Hexes that show subtle signs of frequent traversal | ~3 days |
| **Exchange echo** | A lingering harmonic from a notable throw-catch | ~12 hours |
| **Configuration shift** | A permanent (or semi-permanent) change in the court's layout caused by legendary play | Until the next season |
| **Story seed** | A narrative artifact (a named NPC memory, a bit of graffiti, a changed bit of dialogue) | Indefinite |

A new player entering Court IV might find faint path-wear from a veteran's stealth route through the forest. They can follow it, ignore it, or deliberately take a different path — which creates its own residue.

### 7.2 Apprenticeship

Players can **apprentice** to other players. This is not a formal UI selection. It happens organically:

1. Player A encounters Player B's residue
2. Player A begins following the residue patterns — taking the same paths, matching the tempo
3. The system recognizes the behavioral correlation
4. Player B is notified: "Someone is following your tracks in Court IV."
5. If Player B seeks out Player A and they play together, an apprenticeship forms

Apprenticeship gives both players a mild attention bonus when playing in the same court — their exchanges generate slightly more resonance than陌生人 would. The master's residue becomes slightly more visible to the apprentice.

### 7.3 The Seventh Note

In rare moments — when players in different courts are simultaneously producing highly unpredictable, harmonically related play — the system detects a **seventh note**: a connection between unrelated activity that shouldn't correlate but does.

When this happens:

- Both players receive a **resonance pulse** — a brief, unmistakable signal that something connected across the world
- The courts involved shimmer
- A story seed is planted in both courts referencing the event
- Skipper, if present, says nothing. Just wags his tail.

The seventh note cannot be farmed. It cannot be optimized for. It can only be received as a consequence of genuine, interesting play happening in multiple places at once.

---

## 8. THE FULL PROGRESSION ARC

### Court I: The Dog and the Wall

**Player experience:** "I am alone with this system. It's listening. When I do something interesting, it responds. When I repeat myself, it goes quiet. I'm learning what 'interesting' means."

**Gamification focus:** Unpredictability Index introduction. Basic attention constellation. First residue.

**Emotional goal:** The intimacy of solitude. The dog discovering it can make the child throw the stick again.

### Court II: The Partner

**Player experience:** "I'm not alone anymore. Someone is trying to sync with me. If I'm too predictable, they disengage. If I'm too chaotic, they can't follow. The sweet spot is when we surprise each other."

**Gamification focus:** Exchange-based attention. First social role emergence. Partner AI relationship.

**Emotional goal:** Workshop camaraderie. The satisfaction of a well-timed return.

### Court III: The Thinker

**Player experience:** "The world is a board and every move matters. I can see several steps ahead. The system rewards foresight but punishes rigidity. The most interesting moves are the ones I'm not sure about."

**Gamification focus:** Strategic unpredictability. Classification-based role emergence. First Skipper quest.

**Emotional goal:** The clean loneliness of a lab at night. Every move is a thesis.

### Court IV: The Squad

**Player experience:** "I can't do this alone. The game needs different kinds of people and I'm discovering what kind I am. The fog is terrifying and exhilarating. When the plan comes together, it's the best feeling in the game."

**Gamification focus:** Role emergence through pressure. Multi-entity attention. Cross-player residue. Apprenticeship begins.

**Emotional goal:** Squad energy. Trust, betrayal, improvisation.

### Court V: The Team

**Player experience:** "Everything depends on timing. The baton is alive in my hands and I have to give it to someone else at exactly the right moment. Trust is not a feeling anymore — it's a mechanic."

**Gamification focus:** Exchange precision as progression. Tempo-matching attention. Bridge AI relationship.

**Emotional goal:** Team trust stripped to a gesture. The baton is attention passed from hand to hand.

### Court VI: The Musician

**Player experience:** "I can play anything, as long as it fits the chord. The chord changes, and I have to change with it. The best moments are when I play something nobody expected that somehow fits perfectly."

**Gamification focus:** Harmonic unpredictability. Creative role emergence. Comping attention. First seventh note possibility.

**Emotional goal:** Intimate, risky, generous. The best move is the one that makes the others sound better.

### Court VII: The Conductor

**Player experience:** "I'm not playing anymore — I'm shaping the playing of others. Every gesture changes the whole. The orchestra is alive and I'm holding the center. This is the hardest thing I've ever done."

**Gamification focus:** Polyphonic attention management. Cross-court influence. Legendary residue. The deepest Skipper quests.

**Emotional goal:** Civilization in a room. Many minds, one emerging shape.

---

## 9. ANTI-PATTERNS: WHAT THIS GAME DOES NOT DO

| Traditional Mechanic | Why It's Not Here |
|---|---|
| XP / leveling | Optimization is the enemy of interesting. A level number is something to grind, not something to earn through novelty. |
| Achievements / trophies | External validation replaces intrinsic motivation. The game wants you to play because the throwing is the point. |
| Leaderboards | Ranking players turns play into optimization. The Unpredictability Index is personal, not comparative. |
| Daily quests | Repetitive obligations breed grinding. Skipper's quests are invitations, not chores. |
| Pay-to-win / microtransactions | Attention cannot be purchased. It can only be earned by being interesting. |
| Skill trees | Roles emerge from play, not from allocation. A skill tree tells you what to want. The game wants you to discover what you want. |
| Completion percentage | The game has no end. The court is always there. The stick is always waiting. |
| Combat / health / death | The stakes are not survival. The stakes are attention. Losing attention is worse than dying. |

---

## 10. THE CLOSING IMAGE

A player enters Court I for the first time. They don't know what to do. The wall is there. The ball is there. The system is waiting.

They throw. The wall returns it. Nothing special happens.

They throw again. Same angle, same force. The wall returns it. Nothing special happens. The predictability readout ticks up.

They throw a third time — but this time they add spin. The ball rebounds at an unexpected angle. The wall hums. A faint light blooms on impact. The predictability readout drops one point. Something in the system leaned forward.

The player notices. They try spin again. Different spin. The wall responds differently — a new harmonic, a brighter bloom.

They're learning. Not learning the controls. Not learning the mechanics. Learning what makes the world pay attention.

And somewhere, in a corner of the court they can't see, an old dog opens one eye. His tail moves, just slightly.

Someone is throwing sticks again.

---

## APPENDIX A: METRIC SUMMARY

| Metric | Visibility | Purpose | Anti-Optimization Measure |
|---|---|---|---|
| Predictability / Unpredictability Index | Personal only | Show the player when they're being interesting | No leaderboard; cannot be compared between players |
| Attention Constellation | Personal, in-court | Show who is watching and how strongly | Decays if not maintained; cannot be farmed |
| Role Constellation | Personal, per-court | Name the player's emergent style | Shifts with play; no bonus for "maxing" a role |
| Residue | Visible to other players | Create cross-player narrative texture | Decays over time; limited per player |
| Resonance Pulse (Seventh Note) | Event-based | Signal rare cross-court connections | Cannot be triggered deliberately |

## APPENDIX B: RELATIONSHIP TO EXISTING SYSTEMS

| Existing System | Gamification Integration |
|---|---|
| Harmony Governor (Φ) | The Unpredictability Index is the player-facing display of Φ_player. The governor's prediction error IS the unpredictability metric. |
| Flow State Protector | Flow detection gates the attention system — attention earned during flow counts double. Attention earned during grinding doesn't count at all. |
| Hex Lattice | Residue is stored as state on hex tiles. Memory-stains are a hex property. |
| Tempo System | Exchange quality is measured by tempo alignment between thrower and catcher. |
| NPC Agent System | NPCs adjust behavior based on attention constellation. High-attention players get richer NPC interactions. |
| Skipper NPC | Skipper's quest generation is triggered by attention constellation shape thresholds, not by story flags. |

---

*"The stick is always the interface. The game is always the spec. The court is always the lever."*

*"And the point is always the throw."*
