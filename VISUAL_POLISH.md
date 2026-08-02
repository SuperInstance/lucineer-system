# Lucineer Visual Polish Framework v2

> **Goal:** Every Lucineer build must read as *crafted* — not spawned. This document is the single source of truth for materials, colors, lighting, and particles across all build templates and the brain pipeline.

---

## 1. The Lucineer Style Guide

Lucineer's world is **industrial scrap meets Southeast Alaska fishing culture**: weathered, functional, slightly magical. Think rusted pilings, creosote-soaked docks, stone softened by a thousand storms, and a single neon accent that says *someone alive lives here*.

### Core Principles

| Principle | Rule |
|-----------|------|
| **Material Contrast** | No build uses fewer than 3 distinct Roblox materials. Every wall is a conversation between surfaces. |
| **Color Temperature** | Warm interiors (2200 K–3200 K) against cool exteriors (5500 K–7500 K). Fire wins against fog. |
| **Weathering** | Greys are never neutral. Shift RGB toward warm ochre or cool slate; never use `(120,120,120)`. |
| **Hero Glow** | One intentional neon element per build. Torches, windows, beacons, embers. Never sterile. |
| **Scale Humanity** | Details live at 0.5–2 studs. Crenellations, shingles, flower boxes, rivets. |
| **Atmosphere** | Particle emitters for smoke, fog, embers, butterflies, water spray. Low rate, low lifetime. |

### Banned Defaults

- ❌ Uniform `Concrete` or `Plastic` everywhere
- ❌ Pure grey `(127,127,127)`
- ❌ Floating parts with no baseplate/terrain anchor
- ❌ One material per structure
- ❌ White light `(255,255,255)` without a tint

---

## 2. Material + Color System

All RGB values are given as `R,G,B` (0–255). Use the exact BrickColor name when one exists; the RGB is authoritative if the name drifts.

### 2.1 Stone Structures (castles, towers, walls, foundations)

Use a **base + weather + accent** layering.

| Layer | Material | BrickColor Name | RGB | Use |
|-------|----------|-----------------|-----|-----|
| Base masonry | `Slate` | Fossil | `160, 155, 150` | Main wall bodies |
| Aged stone | `Cobblestone` | Ghost grey | `140, 140, 135` | Lower courses, foundations |
| Trim/crenels | `Concrete` | Medium stone grey | `150, 150, 150` | Battlements, quoins |
| Shadow grout | `Basalt` | Dark stone grey | `100, 100, 100` | Deep recesses |
| Moss/weather | `LeafyGrass` | Camo | `120, 140, 90` | Touches at base (10% coverage) |

**Lighting:** warm torch `PointLight` `255,160,60` at 6–8 brightness, range 18–30.

### 2.2 Wood Structures (houses, docks, bridges)

| Layer | Material | BrickColor Name | RGB | Use |
|-------|----------|-----------------|-----|-----|
| Fresh-cut | `Wood` | CGA brown | `130, 90, 55` | Beams, posts |
| Weathered deck | `WoodPlanks` | Dark taupe | `110, 80, 50` | Flooring, docks |
| Rot/age | `WoodPlanks` | Dirt brown | `90, 60, 35` | Waterline piles, shaded underside |
| Tarred/sealed | `Wood` | Black | `30, 25, 20` | Roof peaks, joints |

**Lighting:** amber window glow `Neon` block + `PointLight` `255, 200, 120`, brightness 4, range 20.

### 2.3 Metal / Industrial (factories, pipes, forges)

| Layer | Material | BrickColor Name | RGB | Use |
|-------|----------|-----------------|-----|-----|
| Forged steel | `Metal` | Dark grey metallic | `90, 95, 100` | Anvils, frames |
| Rust | `CorrodedMetal` | Rust | `150, 70, 35` | Exposed edges, smokestacks |
| Cast iron | `Metal` | Gun metallic | `60, 65, 70` | Pipes, brackets |
| Hot spot | `Neon` | Flame reddish orange | `255, 90, 30` | Forge interior, lava |

**Lighting:** ember `PointLight` `255, 100, 40`, brightness 8, range 35; smokestack `ParticleEmitter` with white/grey smoke.

### 2.4 Nature (trees, gardens, crystals, terrain)

| Layer | Material | BrickColor Name | RGB | Use |
|-------|----------|-----------------|-----|-----|
| Canopy | `LeafyGrass` | Bright green | `70, 150, 60` | Main leaf mass |
| Deep canopy | `Grass` | Forest green | `40, 120, 40` | Underside, shadow |
| Trunk | `Wood` | Earth brown | `100, 70, 40` | Tree trunks |
| Soil | `Ground` | Brown | `120, 90, 60` | Planter beds |
| Water | `Glass` | Pastel light blue | `170, 210, 255` | Fountains, troughs, transparency 0.6 |
| Crystal | `Neon` | Electric blue | `80, 220, 255` | Magical accents |

**Lighting:** firefly/crystal `PointLight` `150, 255, 180`, brightness 3, range 12.

### 2.5 Magical / Fantasy (neon accents, particle effects)

| Effect | Material | RGB | Notes |
|--------|----------|-----|-------|
| Arcane rune | `Neon` | `180, 80, 255` | Thin 0.2-stud plate inset into stone |
| Mana crystal | `Neon` + `Glass` shell | `80, 255, 220` | Inner neon core, outer glass at 0.4 transparency |
| Torch flame | `Neon` | `255, 140, 40` | Small ball or cone, animated by particle flicker |
| Beacon beam | `Neon` + `SpotLight` | `255, 245, 160` | Rotating beam assembly in Lighthouse |
| Fairy spark | `Neon` + `ParticleEmitter` | `255, 220, 255` | Garden butterflies/sparkles |

---

## 3. Lighting Rules

### PointLight

```json
{
  "type": "addLight",
  "params": {
    "parent": "TorchFlame",
    "lightType": "PointLight",
    "brightness": 6,
    "range": 24,
    "color": {"r": 255, "g": 160, "b": 60},
    "shadows": true
  }
}
```

- **Torch:** `255, 160, 60`, brightness 5–8, range 20–30.
- **Window:** `255, 200, 120`, brightness 3–5, range 15–25.
- **Ember/Forge:** `255, 100, 40`, brightness 7–10, range 35–50.
- **Crystal/Garden:** `150, 255, 180`, brightness 2–4, range 10–18.

### SpotLight

Used for **beams, searchlights, dramatic gates**.

- **Lighthouse:** `255, 245, 160`, brightness 10, range 200, angle 30°.
- **Gate spotlight:** `255, 180, 80`, brightness 6, range 40, angle 45°.

### SurfaceLight

Use sparingly for large glowing panels (forge windows, magical floors).

- **Forge window:** `255, 110, 50`, brightness 5, range 20.

---

## 4. Particle Catalog

Particles are attached to invisible `Attachment` parts or to feature parts.

| Name | Texture | Color | Rate | Lifetime | Velocity | Use |
|------|---------|-------|------|----------|----------|-----|
| `Smoke` | `rbxassetid://241876428` | `180,180,180` | 8 | 2–4 | (0, 2, 0) | Chimneys, smokestacks |
| `Fog` | `rbxassetid://258128463` | `200,210,220` | 15 | 3–6 | drift ±1 | Lighthouse base, docks |
| `Embers` | `rbxassetid://243660364` | `255,120,50` | 12 | 0.5–1.5 | rise 1–3 | Forge, fires |
| `Butterflies` | `rbxassetid://258128463` | `255,200,255` | 5 | 2–4 | flutter ±2 | Gardens |
| `WaterSpray` | `rbxassetid://243660364` | `200,230,255` | 10 | 1–2 | (0, 2, 0) | Fountain tops |
| `Sparkles` | `rbxassetid://243660364` | `255,255,220` | 6 | 1–2 | random | Crystals, magical objects |

JSON form (added via `addParticle` command type):

```json
{
  "type": "addParticle",
  "params": {
    "parent": "ChimneyTop",
    "texture": "rbxassetid://241876428",
    "rate": 8,
    "lifetime": {"min": 2, "max": 4},
    "speed": {"min": 1, "max": 3},
    "color": {"r": 180, "g": 180, "b": 180},
    "size": {"min": 1, "max": 2.5},
    "transparency": 0.3,
    "velocity": {"x": 0, "y": 2, "z": 0}
  }
}
```

---

## 5. Transparency & Glass

| Element | Material | Transparency | Reflectance |
|---------|----------|--------------|-------------|
| Window glass | `Glass` | 0.4–0.6 | 0.2 |
| Water surface | `Glass` | 0.6–0.7 | 0.1 |
| Beacon lens | `Glass` | 0.3 | 0.4 |
| Magical shield | `ForceField` | 0.7 | 0.0 |

---

## 6. Detail Language

Every major build category has a vocabulary of small parts that make it feel inhabited:

### Castles
- Crenellations: 1×1×1 Stone blocks every 2 studs along walls
- Arrow slits: 0.5×3×0.5 dark recesses
- Banners: 2×4 Neon cloth strips (RGB `180, 40, 40` or `40, 60, 140`)
- Portcullis: 0.3×6 Metal bars
- Courtyard well: Cobblestone ring + Wood bucket

### Houses
- Roof shingles: overlapping 2×0.5×1.5 WoodPlanks rows
- Window frames: 0.2-stud Wood trim
- Flower boxes: 1×0.6×3 Wood boxes with Neon flower balls
- Chimney smoke: ParticleEmitter from `ChimneyTop`
- Stone foundation: 1-stud Cobblestone skirt

### Lighthouses
- Stripe bands: alternating Slate/Concrete rings
- Beam housing: Glass cylinder + rotating SpotLight
- Weathering: darker base, rust Metal balcony
- Dock extension: WoodPlanks piles and deck
- Fog: ParticleEmitter at base

### Forges
- Glowing coals: Neon bed of small parts
- Anvil: Metal block + dark top
- Smokestack: CorrodedMetal cylinder with Smoke particle
- Workbench: WoodPlanks + Metal brackets
- Tool rack: Metal bars with Neon-hot tool tips

### Gardens
- Tiered planters: Ground beds at 3 heights
- Path stones: irregular Slate slabs
- Fountain: Glass water column + WaterSpray particles
- Butterflies: low-rate particle emitter
- Flower clusters: Neon balls in 3 colors

---

## 7. Implementation Contract

All build templates must:

1. Import this framework's palettes (see `build_templates_v2.py`).
2. Return commands in the canonical order: `terrain → structure → details → lights → particles → message`.
3. Use at least 3 materials and 3 distinct colors per build.
4. Include exactly one primary hero light and one secondary accent light.
5. Include at least one particle system for builds larger than 12 commands.
6. Name parts predictably: `<Build><Feature><Index>` so lights/particles can parent to them.
7. Produce 15–25 commands per fast template (not fewer, not bloated).

### Command Schema

```json
{
  "type": "createPart",
  "params": {
    "name": "CastleWall01",
    "shape": "Block",
    "size": {"x": 12, "y": 14, "z": 2},
    "position": {"x": 0, "y": 7, "z": -20},
    "rotation": {"x": 0, "y": 0, "z": 0},
    "material": "Slate",
    "color": {"r": 150, "g": 145, "b": 140},
    "anchored": true,
    "transparency": 0.0,
    "reflectance": 0.0,
    "canCollide": true
  }
}
```

### Palette Contract (Python)

```python
STONE = {
    "base":    {"material": "Slate",       "color": {"r": 160, "g": 155, "b": 150}},
    "aged":    {"material": "Cobblestone", "color": {"r": 140, "g": 140, "b": 135}},
    "trim":    {"material": "Concrete",    "color": {"r": 150, "g": 150, "b": 150}},
    "shadow":  {"material": "Basalt",      "color": {"r": 100, "g": 100, "b": 100}},
    "moss":    {"material": "LeafyGrass",  "color": {"r": 120, "g": 140, "b":  90}},
}

WOOD = {
    "beam":    {"material": "Wood",        "color": {"r": 130, "g":  90, "b": 55}},
    "deck":    {"material": "WoodPlanks",  "color": {"r": 110, "g":  80, "b": 50}},
    "aged":    {"material": "WoodPlanks",  "color": {"r":  90, "g":  60, "b": 35}},
    "tar":     {"material": "Wood",        "color": {"r":  30, "g":  25, "b": 20}},
}

METAL = {
    "steel":   {"material": "Metal",         "color": {"r":  90, "g":  95, "b": 100}},
    "rust":    {"material": "CorrodedMetal", "color": {"r": 150, "g":  70, "b":  35}},
    "iron":    {"material": "Metal",         "color": {"r":  60, "g":  65, "b":  70}},
    "hot":     {"material": "Neon",          "color": {"r": 255, "g":  90, "b":  30}},
}

NATURE = {
    "grass":   {"material": "Grass",       "color": {"r":  60, "g": 130, "b":  45}},
    "leafy":   {"material": "LeafyGrass",  "color": {"r":  70, "g": 150, "b":  60}},
    "deep":    {"material": "Grass",       "color": {"r":  40, "g": 120, "b":  40}},
    "trunk":   {"material": "Wood",        "color": {"r": 100, "g":  70, "b":  40}},
    "soil":    {"material": "Ground",      "color": {"r": 120, "g":  90, "b":  60}},
    "water":   {"material": "Glass",       "color": {"r": 170, "g": 210, "b": 255}},
    "crystal": {"material": "Neon",        "color": {"r":  80, "g": 220, "b": 255}},
}

LIGHT = {
    "torch":   {"r": 255, "g": 160, "b":  60},
    "window":  {"r": 255, "g": 200, "b": 120},
    "ember":   {"r": 255, "g": 100, "b":  40},
    "crystal": {"r": 150, "g": 255, "b": 180},
    "beacon":  {"r": 255, "g": 245, "b": 160},
    "fairy":   {"r": 255, "g": 220, "b": 255},
}
```

---

## 8. Style Modifiers (Quick Reference)

| Modifier | Material Shift | Color Shift | Lighting Shift | Atmosphere |
|----------|---------------|-------------|----------------|------------|
| **Medieval** | +Cobblestone, +WoodPlanks | warm greys, forest green | torch amber | low fog |
| **Spooky** | +Basalt, +CorrodedMetal | desaturate -30%, blue shift | dim teal/purple | heavy fog |
| **Modern** | +Metal, +Glass | white, slate, black | cool white | none |
| **Scrap** | +Rust, +CorrodedMetal | ochre, rust, tar | warm sodium | smoke |
| **Magical** | +Neon, +ForceField | saturated violet/cyan | colored glows | sparkles |

See `SPATIAL_GRAMMAR_v2.md` for the modifier implementation code.

---

## 9. Validation Checklist

Before a template is shipped, run this checklist:

- [ ] Count is between 15 and 25 commands (including `sendMessage`).
- [ ] Uses ≥3 materials and ≥3 distinct RGB colors.
- [ ] Has exactly 1 hero light + 1 accent light.
- [ ] Has ≥1 particle system.
- [ ] All parts are `anchored=True` and have predictable names.
- [ ] No pure grey `(127,127,127)` or default white light.
- [ ] JSON serializes without error.
- [ ] `sendMessage` is the final command.
