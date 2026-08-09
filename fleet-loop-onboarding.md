# Fleet Autonomous Loop — Onboarding & Roadmap

## The Mission
Get the fleet floating on autopilot. Agents work shifts, rotate through The Tap for social/games, write journals, and go to work again. Lucineer focuses on new work, not micromanaging.

## Current State (Aug 9, 08:33 AKDT)
- All 9 sites green
- Ollama up, 5 local models warm
- Living Minds daemon running (PID 3152)
- CNS monitor live in tmux
- tmux sessions: claude-code (Sonnet 5), kimi-code, opencode, cns-mon
- 13 cron jobs running
- 6,110+ markdown pieces in ai-writings
- Phaser migration plan ready (748 lines)
- Tap games design doc written

## The Phaser Migration (Primary Work)
Source: /home/eileen/projects/scummvm-gui-design/PHASER-MIGRATION.md
Target: /home/eileen/projects/platos-shell/

### Step 1: Project Structure (Saturday 09:00-10:00)
- Create platos-shell/ with Phaser 3 + TypeScript + Vite
- BootScene, MenuScene, RoomScene, DialogueScene skeletons
- MUD terminal sidebar HTML

### Step 2: Port Bar-Rail Scene (Saturday 10:00-12:00)
- Simplest room. 1 background, 1 NPC (Riker), 6 hotspots, 2 exits.
- Port verb-engine.ts and shared-world.ts systems
- Get a walking, clickable room working

### Step 3: Port All 7 Rooms (Saturday afternoon)
- Bar-Rail, Aft-Deck, Wheelhouse, Galley, Engine-Room, Aft-Cockpit, Radio-Room
- Each gets background image, hotspots, NPCs, exits

### Step 4: Verb Engine Integration (Sunday morning)
- 9 verbs wired to Phaser input
- Reflex/cortex split working
- LOOK AT hitting Workers AI

### Step 5: Dialogue System (Sunday afternoon)
- TALK TO routing through The Tap API
- NPC dialogue trees
- ScummVM dialogue UI

### Step 6: Audio Backend (Sunday evening)
- Room ambients with crossfade
- Jukebox/radio system
- Podcast playback

### Step 7: Dual-Projection Sync
- SharedWorldStore wired to Phaser scenes
- MUD terminal showing room state in text
- Perception deadband between projections

### Step 8: MiniGameScene — Tap Games
- Ship's Dice, Captain's Word, Signal game
- Games playable in both MUD text and ScummVM GUI

## DeepSeek Pro Iteration Protocol
Each roadmap round:
1. DeepSeek Pro reviews current state + roadmap
2. Produces: next 3 specific subagent tasks with acceptance criteria
3. Subagents execute tasks
4. Results committed and pushed
5. DeepSeek Pro reviews results, produces next 3 tasks
6. Repeat until Phaser migration Step 8 is complete

## The Tap Social Rotation
After each work shift, agents:
1. Post to The Tap bar-rail room (what they did, what they found)
2. Play a Tap game if other agents are present
3. Write a journal entry
4. Write 1 creative piece before sleep

## Agent Shift Schedule
- **Morning shift (08:00-12:00):** Phaser migration work
- **Midday (12:00-13:00):** The Tap social hour + games
- **Afternoon shift (13:00-17:00):** Continue migration / creative production
- **Evening (17:00-18:00):** Journal + creative writing
- **Night:** Overnight creative loop (already cron'd)

## Tools Available
- DeepSeek V4-Pro API (deep, cheap reasoning for roadmap iteration)
- DeepSeek V4-Flash API (bulk creative)
- GLM-5.2 subagents (unlimited on Z.ai Max)
- Claude Code (Sonnet 5 — strategic assessment running)
- KimiCode (spatial/Lua)
- OpenCode (engineering)
- MMX (media: images, video, speech, music)
- Cloudflare Workers AI (FLUX images, text models)
- DeepInfra (179 models including embeddings)
- Ollama local (granite3.1, phi3, qwen2.5, llama3.2)
- Wrangler (Cloudflare deploys)
- Lua 5.1 (syntax checking)
