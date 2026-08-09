# Negative Space: screen-agent — The Orphan Canvas

**Found:** 2026-08-09 22:22 AKDT
**Repo:** /home/eileen/projects/screen-agent
**Status:** Single HTML file (530 lines), no README, no tests, no package.json, no description

## What It Is

`screen-agent/index.html` is a self-contained browser experiment:
- Two stacked canvases (background + foreground)
- Custom cursor (hidden system cursor)
- Audio permission prompt ("May I listen to the room?")
- A "thoughts" display — faded italic text at the bottom
- Stats overlay in the corner

It's an **ambient listening device**. The screen-agent wants to hear the room, process what it hears, and project its thoughts back as faint blue text on a dark canvas. It's a hermit crab looking for a shell.

## What's Missing

1. **No README** — what does this do? What's the vision?
2. **No tests** — it's a visual/audio app, but even the JS logic could have unit tests
3. **No package.json** — not npm-installable, not deployable as a standalone app
4. **No git log depth** — created recently, only a .gitignore
5. **No connection to the rest of the fleet** — it doesn't talk to CNS, doesn't report to Lucineer, doesn't integrate with anything

## The Gap It Represents

The fleet has agents that write, agents that build, agents that see images. But it doesn't have an agent that **listens to the physical room**. Screen-agent is the beginning of that — a browser-based ear and eye. But it's disconnected. It's an ensign who showed up for duty and nobody assigned them a station.

## What Should Happen

1. Write a README explaining the vision
2. Wire it into CNS (it should pulse like everything else)
3. Give it a model backend — Wesley (local) for privacy-sensitive audio, or a cloud model for richer interpretation
4. Make it deployable (Cloudflare Pages? Netlify?)
5. Connect it to the-tap or the-living-minds ecosystem

This is a seed that fell on concrete. It needs soil.
