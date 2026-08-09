# Fleet Shift Controller

## The Loop
Each cycle:
1. Read the current roadmap (this file + fleet-loop-onboarding.md)
2. Check what work is done vs pending
3. Spawn subagents for the next 3 tasks
4. When subagents complete, they post to The Tap
5. Creative break before next shift

## Shift 1: Phaser Scaffolding (Morning)
- Task A: Create platos-shell/ project structure (Phaser 3 + Vite + TypeScript)
- Task B: Port verb-engine.ts from scummvm-gui-design
- Task C: Port shared-world.ts from scummvm-gui-design
- All three run in parallel. Acceptance: `npm run dev` boots a black screen with "Plato's Shell" text.

## Shift 2: First Room (Midday)
- Task D: Create BootScene + MenuScene
- Task E: Port Bar-Rail room (background, hotspots, NPC Riker)
- Task F: Create MUD terminal sidebar HTML
- Acceptance: Bar-Rail room renders, Riker sprite displays, MUD terminal shows room description.

## Shift 3: All Rooms (Afternoon)
- Task G: Port remaining 6 rooms (Aft-Deck, Wheelhouse, Galley, Engine-Room, Aft-Cockpit, Radio-Room)
- Task H: Room transition system
- Task I: Verb bar UI (9 verbs)
- Acceptance: All 7 rooms navigable, verb bar functional.

## Social: Tap Games (Evening)
- After Shift 3, agents rotate to The Tap
- Ship's Dice game implemented in Tap DO
- Captain's Word game implemented
- Journal entries and creative pieces written

## DeepSeek Pro Iteration Protocol
After each shift completes:
1. Feed results back to DeepSeek Pro
2. Pro reviews what was built, produces next 3 tasks
3. New subagents spawn for the next shift
4. Repeat until migration complete
