# KimiCode (K3) — Your Mission

You are Lucineer's master builder and spatial architect. Casey is building an AI companion inside Roblox that builds structures in real-time from natural language.

## Current Build System
- 17 Python build templates generating JSON commands (createPart, addLight, setTerrain, sendMessage)
- 35 Luau skills in a Vectorize semantic search index
- Lua CommandExecutor in Roblox that receives JSON and creates Parts
- Brain pipeline: Seed-2.0-mini → Qwen3.6 → Qwen3-Coder-480B (generates commands for novel builds)
- All builds use basic Roblox primitives (Block, Ball, Cylinder, Cone)

## The Problem
The builds work but they're not "world-class, head-turning." A castle made of gray boxes is functional. A castle with weathered stone textures, crenellation details, banners, and dramatic lighting is head-turning.

## Your Deliverables

### 1. VISUAL POLISH FRAMEWORK (write to /home/eileen/projects/lucineer-system/VISUAL_POLISH.md)
- Define a material/color/texture system that makes every build look stunning
- Specify exact Roblox Material + BrickColor + Lighting combinations for:
  - Stone structures (castles, towers, walls)
  - Wood structures (houses, docks, bridges)
  - Metal/industrial (factories, pipes, forges)
  - Nature (trees, gardens, crystals)
  - Magical/fantasy (neon accents, particle effects)
- Define a "Lucineer Style Guide" — consistent visual language across all builds

### 2. UPGRADED BUILD TEMPLATES (write to /home/eileen/projects/lucineer-worker/build_templates_v2.py)
Rewrite the top 5 most impactful templates as Python functions that produce DRAMATICALLY better-looking builds:
- castle: Multi-texture stone, banner accents, torch lighting, gate detail, inner courtyard
- house: Shingled roof, window glow, chimney smoke, flower boxes, stone foundation
- lighthouse: Striped tower, rotating beam, weathered stone, fog particles, dock extension
- forge: Glowing interior, smokestack particles, anvil details, ember lighting
- garden: Multi-tier planters, path stones, butterfly particles, fountain centerpiece

Each should produce 15-25 commands (up from 5-10). Use:
- Multiple materials per build (Stone + Slate + Cobblestone, not just one)
- Neon accents for magical/lighting moments
- Transparency for glass/water effects
- Varied BrickColors for depth (not uniform gray)
- ParticleEmitter attachments for atmosphere
- PointLight/SpotLight with colored tints

### 3. SPATIAL GRAMMAR v2 (write to /home/eileen/projects/lucineer-system/SPATIAL_GRAMMAR_v2.md)
Define an upgraded spatial grammar for the brain pipeline:
- How to decompose complex requests ("haunted castle with a garden and dock")
- Positioning rules (avoiding overlap, using terrain)
- Scale relationships (how big should a "large" castle be vs a "small" house)
- Style modifiers (spooky, medieval, modern, scrap) with specific material/color mappings

Be specific. Write actual code. No hand-waving.
