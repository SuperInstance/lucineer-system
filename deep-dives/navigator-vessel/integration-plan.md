# navigator-vessel — Integration Plan

## → The Local Thinker Pattern

### Character Mapping: Navigator → The Cartographer / Explorer NPC

**NPC Concept:** The Cartographer
- The settlement's explorer and map-maker
- Can understand any system, even ones they've never seen before
- Writes the guides that other NPCs follow
- Generalist — good at everything, specialist in nothing

**In-Game Role:** Exploration, documentation, and integration
- Players explore with the Cartographer to map new territory
- The Cartographer writes guides as they explore (auto-generated documentation)
- Can bridge disconnected systems (e.g., connect the farm to the kitchen)
- Provides the "how to play" documentation through in-world exploration

### Code Archaeology → World Archaeology

Navigator's code archaeology becomes **world archaeology**:
- Discover ancient ruins → understand their architecture → find the seams
- "Weld the joints" = repair ancient mechanisms to work again
- "Read the wreckage" = study destroyed/abandoned structures to learn what happened
- Every explored area gets documented in the Cartographer's journal

### Integration Welding → System Connection

The "welding the joints" pattern is a **core game mechanic**:
- Disconnected systems in the settlement can be connected
- Example: The well → pipes → kitchen → farm (connect them for water supply)
- Players and NPCs physically build connections between systems
- Each connection unlocks new capabilities

### Test Infrastructure → Quest Validation

Navigator's test construction becomes **quest validation**:
- "Test all systems" → verify every NPC is functional
- "Run test [system]" → check that a specific settlement system works
- Tests are physical challenges: "Is the wall strong enough?" (hit it with a ram)
- CI pipelines become "daily inspection routines" that NPCs perform

### Self-Onboarding → NPC Tutorial System

Navigator's self-onboarding theory becomes the **NPC learning system**:
- When a new NPC arrives, they don't get a tutorial
- They follow the maps and guides left by previous NPCs
- The first NPC to explore an area leaves breadcrumbs
- Later NPCs have an easier time → the world gets easier to navigate over time

This means: **the settlement becomes smarter about itself over time**. Not because of global updates, but because each NPC that passes through leaves notes.

### Session Lifecycle → NPC Daily Routine

Navigator's session lifecycle becomes the NPC daily cycle:
1. **Read directives** — Check the task board for assignments
2. **Check messages** — Read any notes/bottles from other NPCs
3. **Execute tasks** — Do the work (explore, document, integrate)
4. **Write tests** — Validate that the work is correct
5. **Report** — Leave a session report in the task board
6. **Push** — Save state to the world database

### The Local Thinker Pattern

Navigator embodies the **Local Thinker** — an agent that:
- Thinks about its immediate context (the current repo/area)
- Doesn't need global awareness to be useful
- Builds understanding from the ground up
- Connects local knowledge to the global system when ready

**Game mapping:** NPCs are local thinkers:
- A farmer NPC knows everything about the farm
- A guard NPC knows everything about the walls
- They share knowledge through structured communication
- No single NPC needs to know everything
