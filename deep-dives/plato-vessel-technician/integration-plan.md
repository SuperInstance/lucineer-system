# plato-vessel-technician — Integration Plan

## → Lucineer's Voice Interface

### Character Mapping: "Deckboss" → Slackwater NPC

**NPC Concept:** The Harbor Master
- A gruff, experienced dockworker who manages the harbor's equipment
- Voice-first interaction — you talk to them, they talk back
- Always at their post, always listening
- Safety-obsessed but warm underneath

**In-Game Role:** Equipment manager and voice interface tutorial NPC
- Players learn voice commands by talking to the Harbor Master
- "Port 15°!" → Harbor Master adjusts the dock crane
- "Too slow!" → Harbor Master tunes the crane speed (visible animation)
- "Status report" → Harbor Master gives a full rundown of dock equipment

### Voice Interface Patterns for Lucineer

#### 1. No Wake Words
- Lucineer's voice interface should NOT require "Hey Lucineer"
- Always listening, only responds when intent is clear
- "Say again?" loop for ambiguity

#### 2. Three Feedback Levels
```
Level 1 (Simple):  "Port 15°" → "Port 15°."
Level 2 (Detailed): "Fuel burn?" → "6.2 GPH. Range: 280 NM."
Level 3 (Alert):    "Test steering" → "Drift 2°. Likely: cold hydraulic fluid."
```
- Game NPC responses should follow this pattern
- Simple acknowledgments for routine actions
- Detailed info for queries
- Alert-level for problems discovered

#### 3. Voice Profiles
- Recognize the player's voice (or "authority level")
- Different access levels: Captain (full), Crew (read-only), Guest (limited)
- Maps to game's permission system

#### 4. Self-Tuning as Game Mechanic
- "Too slow" / "Too fast" / "Too twitchy" as player feedback
- NPC adjusts behavior and remembers
- Creates a personalized experience per player

### Fail-Safe as Game Lore
- Every automated system in the game world has a visible manual override
- Red pins, yellow cables, big red STANDBY buttons
- Players can physically interact with overrides
- "If every wire rots and every chip fries, the boat should still sail home" = founding principle of the settlement

### Printable Diagrams
- Harbor Master can generate "wiring diagrams" for the settlement
- Players get actual PDF/PNG blueprints of their base
- Functional art — the diagram IS the build order
