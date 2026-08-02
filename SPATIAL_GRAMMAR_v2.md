# Lucineer Spatial Grammar v2

> **Goal:** Turn free-form player requests into conflict-free, correctly-scaled, stylistically coherent build plans. This grammar runs *before* command generation — it produces a `BuildPlan` that templates or the brain pipeline can execute.

---

## 1. Core Concepts

A player request is decomposed into:

```
BuildPlan = {
    "style": str,           # e.g. "spooky", "medieval", "scrap"
    "terrain": str | None,  # e.g. "hill", "water", "flat"
    "anchors": [Anchor],    # one per sub-build
    "relationships": [Rel], # e.g. "garden in front of castle"
}

Anchor = {
    "intent": str,          # canonical build type: "castle", "garden", "dock"
    "size": str,            # "small", "medium", "large"
    "position": (x, y, z),
    "rotation": y_degrees,
    "style_overrides": {},
}
```

The pipeline:

```
raw text
  → intent parser (extract intents + modifiers)
  → spatial planner (resolve positions/scales)
  → style resolver (apply palette overrides)
  → command generator (template or brain.py)
```

---

## 2. Intent Extraction

### Canonical Intents

These map directly to `build_templates_v2.py` templates:

```python
CANONICAL_INTENTS = {
    "castle", "house", "lighthouse", "forge", "garden",
    "tower", "tree", "bridge", "wall", "road", "lamp",
    "dock", "platform", "staircase", "pyramid", "dome", "arch",
}
```

### Keyword Maps

```python
INTENT_ALIASES = {
    "castle":    {"castle", "fortress", "fort", "keep", "citadel", "palace"},
    "house":     {"house", "home", "cabin", "cottage", "shack"},
    "lighthouse":{"lighthouse", "beacon", "light tower"},
    "forge":     {"forge", "smithy", "blacksmith", "foundry"},
    "garden":    {"garden", "park", "yard", "flowerbed", "grove"},
    "dock":      {"dock", "pier", "wharf", "jetty"},
    "tree":      {"tree", "pine", "oak", "cedar"},
    "bridge":    {"bridge", "overpass", "span"},
    "wall":      {"wall", "fence", "barrier"},
    "road":      {"road", "path", "street", "trail"},
    "lamp":      {"lamp", "lantern", "light"},
    "tower":     {"tower", "turret", "spire"},
}

SIZE_KEYWORDS = {
    "tiny": 0.6, "small": 0.8, "little": 0.8,
    "medium": 1.0, "large": 1.4, "big": 1.4,
    "huge": 1.8, "massive": 2.0, "giant": 2.2,
}

TERRAIN_KEYWORDS = {
    "hill": "hill", "cliff": "hill", "mountain": "hill",
    "water": "water", "lake": "water", "sea": "water", "ocean": "water",
    "beach": "shore", "shore": "shore", "coast": "shore",
    "flat": "flat", "field": "flat", "clearing": "flat",
    "forest": "forest", "woods": "forest",
}
```

### Extractor Function

```python
import re
from typing import List, Dict, Tuple

def extract_intents(text: str) -> List[Dict]:
    """
    Return a list of detected build intents with size and terrain hints.
    Example: 'haunted castle with a garden and dock' ->
        [
            {'intent': 'castle', 'size': 1.0, 'style_hint': 'spooky'},
            {'intent': 'garden', 'size': 1.0, 'style_hint': 'spooky'},
            {'intent': 'dock',   'size': 1.0, 'style_hint': 'spooky'},
        ]
    """
    text_lower = text.lower()
    style = detect_style(text_lower)
    terrain = detect_terrain(text_lower)
    size_mult = 1.0
    for word, mult in SIZE_KEYWORDS.items():
        if word in text_lower:
            size_mult = mult
            break

    found = []
    for canonical, aliases in INTENT_ALIASES.items():
        for alias in aliases:
            if re.search(r"\b" + re.escape(alias) + r"\b", text_lower):
                found.append({
                    "intent": canonical,
                    "size": size_mult,
                    "style_hint": style,
                    "terrain_hint": terrain,
                })
                break
    return found


def detect_style(text: str) -> str:
    style_words = {
        "spooky": {"haunted", "spooky", "creepy", "dark", "ghost", "evil"},
        "medieval": {"medieval", "old", "ancient", "kingdom"},
        "modern":   {"modern", "sleek", "glass", "steel"},
        "scrap":    {"scrap", "rusty", "industrial", "junk", "salvage"},
        "magical":  {"magical", "fairy", "enchanted", "mystic", "arcane"},
    }
    scores = {style: sum(1 for w in words if w in text) for style, words in style_words.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "medieval"


def detect_terrain(text: str) -> str:
    for word, terrain in TERRAIN_KEYWORDS.items():
        if word in text:
            return terrain
    return "flat"
```

---

## 3. Scale Relationships

Every build has a **base footprint** and a **base height**. The `size` multiplier scales both uniformly.

```python
BASE_SIZES = {
    # intent: (footprint_xz, height)
    "castle":    {"footprint": 40, "height": 28, "clearance": 22},
    "lighthouse":{"footprint": 16, "height": 38, "clearance": 14},
    "forge":     {"footprint": 20, "height": 16, "clearance": 12},
    "house":     {"footprint": 20, "height": 14, "clearance": 10},
    "garden":    {"footprint": 24, "height": 8,  "clearance": 14},
    "dock":      {"footprint": 26, "height": 6,  "clearance": 8},
    "tower":     {"footprint": 10, "height": 24, "clearance": 8},
    "tree":      {"footprint": 8,  "height": 14, "clearance": 6},
    "bridge":    {"footprint": 30, "height": 8,  "clearance": 6},
    "wall":      {"footprint": 24, "height": 10, "clearance": 4},
    "road":      {"footprint": 36, "height": 1,  "clearance": 4},
    "lamp":      {"footprint": 3,  "height": 8,  "clearance": 2},
    "platform":  {"footprint": 14, "height": 8,  "clearance": 8},
    "staircase": {"footprint": 12, "height": 12, "clearance": 6},
    "pyramid":   {"footprint": 24, "height": 16, "clearance": 14},
    "dome":      {"footprint": 18, "height": 12, "clearance": 10},
    "arch":      {"footprint": 16, "height": 16, "clearance": 8},
}

def build_dimensions(intent: str, size_mult: float = 1.0) -> Dict:
    base = BASE_SIZES.get(intent, {"footprint": 10, "height": 8, "clearance": 6})
    return {
        "width": base["footprint"] * size_mult,
        "height": base["height"] * size_mult,
        "clearance": base["clearance"] * size_mult,
        "radius": (base["footprint"] * size_mult) / 2,
    }
```

### Scale Language

| Word | Multiplier | Example Result |
|------|------------|----------------|
| tiny | 0.6 | Small doghouse-scale house |
| small | 0.8 | Cabin |
| medium | 1.0 | Standard template size |
| large | 1.4 | Manor / big forge |
| huge | 1.8 | Keep-scale castle |
| massive | 2.0 | Landmark structure |

---

## 4. Positioning Rules

### Spatial Relationships

```python
RELATIONSHIP_OFFSETS = {
    "in front of":  {"azimuth": 0,   "distance_factor": 1.1},  # +Z relative to anchor
    "behind":       {"azimuth": 180, "distance_factor": 1.1},  # -Z
    "left of":      {"azimuth": -90, "distance_factor": 1.0},  # -X
    "right of":     {"azimuth": 90,  "distance_factor": 1.0},  # +X
    "next to":      {"azimuth": 45,  "distance_factor": 1.0},
    "near":         {"azimuth": 0,   "distance_factor": 0.8},
    "far from":     {"azimuth": 0,   "distance_factor": 2.0},
    "on":           {"azimuth": 0,   "distance_factor": 0.0},  # stacked / same spot
    "surrounded by":{"azimuth": 0,   "distance_factor": 0.7, "encircle": True},
}
```

### Collision-Aware Layout Engine

```python
import math
from typing import List, Dict, Tuple

class Anchor:
    def __init__(self, intent: str, size_mult: float = 1.0, position=(0, 0, 0), rotation=0):
        self.intent = intent
        self.size_mult = size_mult
        self.position = position
        self.rotation = rotation
        dims = build_dimensions(intent, size_mult)
        self.radius = dims["radius"]
        self.height = dims["height"]

    def bbox(self) -> Tuple[float, float, float, float]:
        """Return (min_x, max_x, min_z, max_z)."""
        x, _, z = self.position
        r = self.radius
        return (x - r, x + r, z - r, z + r)


def place_relative(
    child_intent: str,
    child_size: float,
    parent: Anchor,
    relation: str,
    occupied: List[Anchor],
) -> Anchor:
    """
    Place `child` relative to `parent` without overlapping anything in `occupied`.
    """
    rel = RELATIONSHIP_OFFSETS.get(relation, {"azimuth": 0, "distance_factor": 1.0})
    child_dims = build_dimensions(child_intent, child_size)

    # Base distance = sum of radii + small buffer
    base_dist = parent.radius + child_dims["radius"] + 2
    distance = base_dist * rel.get("distance_factor", 1.0)

    # Convert azimuth (degrees, +Z = 0) to radians
    rad = math.radians(rel["azimuth"] + parent.rotation)
    px, py, pz = parent.position
    cx = px + distance * math.sin(rad)
    cz = pz + distance * math.cos(rad)

    child = Anchor(child_intent, child_size, (cx, py, cz), rotation=parent.rotation)

    # If collision, push outward along the same vector until clear
    max_attempts = 8
    step = 3
    for _ in range(max_attempts):
        if not any(_bboxes_overlap(child.bbox(), o.bbox()) for o in occupied):
            break
        cx += step * math.sin(rad)
        cz += step * math.cos(rad)
        child.position = (cx, py, cz)
    return child


def _bboxes_overlap(a: Tuple[float, float, float, float], b: Tuple[float, float, float, float]) -> bool:
    return not (a[1] < b[0] or a[0] > b[1] or a[3] < b[2] or a[2] > b[3])


def terrain_offset(terrain: str, base_y: float) -> float:
    """Adjust Y so builds sit naturally on terrain."""
    offsets = {
        "flat": 0,
        "hill": 6,
        "water": -2,
        "shore": 0,
        "forest": 0,
    }
    return base_y + offsets.get(terrain, 0)
```

### Layout Example

```python
from build_templates_v2 import TEMPLATES_V2

def plan_castle_with_garden_and_dock(request: str, origin=(0, 0, 0)) -> Tuple[List[Anchor], Dict]:
    """
    'haunted castle with a garden and dock' -> 3 anchors.
    """
    intents = extract_intents(request)
    if not intents:
        return [], {}

    style = intents[0]["style_hint"]
    terrain = intents[0]["terrain_hint"]

    # Primary anchor is the first mentioned major structure
    primary_data = intents[0]
    primary = Anchor(
        primary_data["intent"],
        primary_data["size"],
        (origin[0], terrain_offset(terrain, origin[1]), origin[2]),
    )
    occupied = [primary]
    anchors = [primary]

    # Place secondary structures relative to primary
    rel_map = ["in front of", "right of", "left of", "behind"]
    for idx, child_data in enumerate(intents[1:], start=1):
        relation = rel_map[(idx - 1) % len(rel_map)]
        child = place_relative(
            child_data["intent"],
            child_data["size"],
            primary,
            relation,
            occupied,
        )
        anchors.append(child)
        occupied.append(child)

    return anchors, {"style": style, "terrain": terrain}
```

---

## 5. Style Modifiers

Style modifiers override the default palette from `VISUAL_POLISH.md`. The resolver produces a `StylePatch` dict that the template or brain pipeline applies to every generated part.

```python
STYLE_PATCHES = {
    "medieval": {
        "material_bias": {"+Slate", "+Cobblestone", "+WoodPlanks"},
        "color_shift": (0, -5, -15),        # slightly cooler, shadowed
        "light_shift": (10, -10, -40),      # more torch amber
        "particle": "low_fog",
        "transparency_bias": 0,
    },
    "spooky": {
        "material_bias": {"+Basalt", "+CorrodedMetal", "+Slate"},
        "color_shift": (-30, -30, 10),      # desaturate + blue shift
        "light_shift": (-100, -60, 60),     # dim teal / purple
        "particle": "heavy_fog",
        "transparency_bias": 0.1,
    },
    "modern": {
        "material_bias": {"+Metal", "+Glass", "+Concrete"},
        "color_shift": (10, 10, 10),        # clean neutral
        "light_shift": (-20, -20, 20),      # cool white
        "particle": None,
        "transparency_bias": 0.3,
    },
    "scrap": {
        "material_bias": {"+CorrodedMetal", "+Rust", "+WoodPlanks"},
        "color_shift": (20, -10, -30),      # rust / ochre
        "light_shift": (20, 0, -40),        # sodium warm
        "particle": "smoke",
        "transparency_bias": 0,
    },
    "magical": {
        "material_bias": {"+Neon", "+ForceField", "+Glass"},
        "color_shift": (20, 0, 40),         # saturated violet/cyan
        "light_shift": (30, -30, 80),       # colored glows
        "particle": "sparkles",
        "transparency_bias": 0.2,
    },
}


def clamp_color(c: Dict[str, int]) -> Dict[str, int]:
    return {k: max(0, min(255, v)) for k, v in c.items()}


def apply_style_patch(color: Dict[str, int], patch: Dict) -> Dict[str, int]:
    shift = patch.get("color_shift", (0, 0, 0))
    return clamp_color({
        "r": color["r"] + shift[0],
        "g": color["g"] + shift[1],
        "b": color["b"] + shift[2],
    })
```

### Style-Aware Command Post-Processing

```python
def patch_commands(commands: List[Dict], style: str) -> List[Dict]:
    patch = STYLE_PATCHES.get(style, STYLE_PATCHES["medieval"])
    out = []
    for cmd in commands:
        if cmd["type"] == "createPart":
            params = cmd["params"]
            if "color" in params:
                params["color"] = apply_style_patch(params["color"], patch)
            params["transparency"] = min(1.0, params.get("transparency", 0) + patch["transparency_bias"])
        out.append(cmd)
    return out
```

---

## 6. End-to-End Example

### Input

```text
"haunted castle with a garden and dock"
```

### Step 1: Intents

```python
extract_intents("haunted castle with a garden and dock")
# -> [
#     {"intent": "castle",  "size": 1.0, "style_hint": "spooky", "terrain_hint": "flat"},
#     {"intent": "garden",  "size": 1.0, "style_hint": "spooky", "terrain_hint": "flat"},
#     {"intent": "dock",    "size": 1.0, "style_hint": "spooky", "terrain_hint": "flat"},
# ]
```

### Step 2: Layout

```python
anchors, meta = plan_castle_with_garden_and_dock("haunted castle with a garden and dock")

# anchors (approximate):
#   castle:  (0,  0, 0)
#   garden:  (0,  0, 46)   # in front of castle
#   dock:    (46, 0, 0)    # right of castle
```

### Step 3: Generate Commands

```python
from build_templates_v2 import TEMPLATES_V2

all_commands = []
for anchor in anchors:
    fn = TEMPLATES_V2.get(anchor.intent)
    if not fn:
        continue
    _, cmds = fn(*anchor.position, player_name="Casey")
    cmds = patch_commands(cmds, meta["style"])
    all_commands.extend(cmds)
```

### Result

- **Castle:** at origin, Basalt/Slate, dim teal lights, heavy fog particles.
- **Garden:** in front, muted soil/flowers, ghostly butterflies.
- **Dock:** to the right, weathered wood, no bright accents.

---

## 7. Integration with process_v2.py

Replace the existing template dispatcher with the style-aware pipeline:

```python
from build_templates_v2 import TEMPLATES_V2
from spatial_grammar_v2 import extract_intents, plan_layout, patch_commands

def run_template_pipeline(request: str, player_name: str, origin=(0, 0, 0)):
    intents = extract_intents(request)
    if not intents:
        return None

    anchors, meta = plan_layout(intents, origin)
    all_commands = []
    for anchor in anchors:
        fn = TEMPLATES_V2.get(anchor.intent)
        if not fn:
            continue
        _, cmds = fn(*anchor.position, player_name=player_name)
        cmds = patch_commands(cmds, meta["style"])
        all_commands.extend(cmds)

    message = f"Built you a {meta['style']} setup, {player_name}. Don't say I never did anything for you."
    all_commands.append({"type": "sendMessage", "params": {"text": message}})
    return message, all_commands
```

---

## 8. Rules Summary

1. **First mentioned intent = primary anchor.** Everything else arranges around it.
2. **Use real dimensions.** Never place a castle 10 studs from a house — use `radius + clearance` math.
3. **Collision is not optional.** Push overlapping builds outward until `bbox` separation is positive.
4. **Style propagates.** If the user says "haunted", every sub-build gets the spooky patch.
5. **Terrain matters.** Docks move toward water/negative X, hill builds get +Y, shore builds stay at sea level.
6. **One hero light per build.** Templates own this; the grammar only shifts its color.
7. **Templates are authoritative for shape.** The grammar only decides *where*, *how big*, and *what style*.
