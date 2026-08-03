# ERA BUILDING SYSTEM
## Slackwater — The Five Eras of Maritime Construction

*Reference document for Lua engineers. Every value, material ID, and build type in this document is designed to map to the EraSystem, Recipes, and CraftingSystem modules. Where a direct field mapping exists, it is called out in code blocks.*

---

## 0. DESIGN PHILOSOPHY

The existing EraSystem tracks seven technology eras (0–6) from Simple Machines to Autonomous Agents. This document defines a parallel **building progression** of five eras that describes what players *build with* and *what those builds look like*, rather than what components they can wire together. The two systems interlock:

| Building Era | Tech Era Equivalent | What Changes |
|---|---|---|
| Era 1: Driftwood and Salvage | Tech Era 0 (Simple Machines) | What you can place, what it's made of |
| Era 2: Frame and Plank | Tech Era 1 (Power Transmission) | Structural integrity, multi-story |
| Era 3: Stone and Mortar | Tech Era 2 (Electricity) | Permanence, load-bearing, foundations |
| Era 4: Metal and Machine | Tech Eras 3–4 (Control + Programmable) | Prefabrication, mechanical systems |
| Era 5: Light and Signal | Tech Eras 5–6 (Networked + Autonomous) | Illumination, communication, automation |

The building era is derived from — but not identical to — the tech era. A player who rushes the electrical tech tree without building anything substantial still lives in a driftwood shack. Lucineer cares about what you've built, not just what you can wire.

### The Golden Rule

**Attention is the only currency** (per the Integrated Architecture). There is no XP bar for building eras. Advancement happens through **building milestones** — specific constructions that demonstrate mastery of the current era's materials — and **Lucineer's assessment**, which is narrative, not numeric. The era system tracks what you've built; Lucineer decides what it means.

### Lua Implementation Contract

```lua
-- Building eras layer on top of the existing EraSystem.
-- Add these fields to each ERAS entry in EraSystem/init.lua:

BUILDING_ERAS = {
    [1] = {
        name = "Driftwood and Salvage",
        requiredBuilds = { "fire_pit", "workbench_scrap" },
        minimumDistinctBuilds = 4,
        materials = { "driftwood", "salvage_plank", "rawhide", ... },
        buildTypes = { "lean_to", "debris_hut", "tideline_fence", ... },
    },
    -- ... etc
}

-- Era advancement check (replaces XP-based gating):
function checkBuildingEraAdvancement(playerName)
    local built = playerBuildCounts[playerName]  -- { [buildType] = count }
    local currentEra = playerBuildingEra[playerName]
    local eraDef = BUILDING_ERAS[currentEra]
    
    -- Must have built all required types
    for _, buildType in ipairs(eraDef.requiredBuilds) do
        if not (built[buildType] and built[buildType] > 0) then
            return false  -- Not yet
        end
    end
    
    -- Must have built minimum distinct types
    local distinctCount = 0
    for buildType, count in pairs(built) do
        if count > 0 and eraDef.buildTypes[buildType] then
            distinctCount = distinctCount + 1
        end
    end
    
    return distinctCount >= eraDef.minimumDistinctBuilds
end
```

---

## 1. THE FIVE ERAS

### Era 1: DRIFTWOOD AND SALVAGE

> *"You work with what the tide brings you. It's not much. It's enough."*

**Aesthetic:** Beachcomber vernacular. Walls made of salt-bleached planks pulled from wrecks. Roofs of layered bark, canvas scraps, and salvaged cloth. Structures are small, single-room, impermanent — a storm can take them. Everything smells of salt and tar. The visual language is *organic irregularity*: no two planks are the same width, walls lean slightly, doorways are rough-cut. Builds sit on the sand without foundations. It looks like someone's first week on an island, because it is.

**Lucineer calls it:** "the salvage years" or "before you had standards"

**Materials:**

| ID | Name | Found Where | Properties | Personality |
|---|---|---|---|---|
| `driftwood` | Driftwood | Tideline, wreckage | Light, soft, salt-cured. Easy to work, weak structurally. | The friendly drunk — cheerful, undemanding, falls over if you push it. Always there when you need something, anything, to stack. |
| `salvage_plank` | Salvaged Plank | Wrecks, debris fields | Variable hardwood/softwood. May have fasteners embedded. | The retiree with stories — been through things, has metal in it, will surprise you with what it remembers. Works hard when you let it. |
| `rawhide` | Rawhide | Small catches, beach finds | Flexible when wet, rigid when dry. Shrinks as it cures. | The clingy friend — holds everything together when wet, then becomes inflexible. You learn to time your lashing with the tide schedule. |
| `palm_fiber` | Palm Fiber | Palm trees, shoreline | Strong when twisted, weak when straight. Absorbs water. | The introvert — useless alone, strong in a group. Twist three together and it becomes rope. Twist a dozen and it becomes a structural element. |
| `kelp_dried` | Dried Kelp | Shoreline harvesting | Flexible, water-resistant, moderately strong woven. Burns well. | The survivor — grows back every week, asks nothing, feeds the fire and the bed equally. You underestimate it until the night you have nothing else. |
| `sea_rope` | Sea Rope | Crafted (palm_fiber ×3) | Tension load only. Degraded by fresh water, salt-stable. | The dependable middle child — not glamorous, not special, but you reach for it every single time. Everything in Era 1 is tied together. Literally. |
| `beach_stone` | Beach Stone | Shoreline collecting | Hard, heavy, irregular. Good for weight, bad for structure. | The quiet one — doesn't say much, but when you need something to not move, you put a stone on it. Patient. Eternal. Doesn't care about your plans. |
| `canvas_scrap` | Canvas Scrap | Wreckage, washed-up cargo | Water-resistant woven fabric. Tears at existing holes. | The hand-me-down — was somebody else's sail, somebody else's tent. Still has life in it. Holes are character, not failure. |
| `pitch` | Pitch (Tar) | Natural seeps, boiled pine | Sticky, water-resistant, flammable. Sealant and adhesive. | The messy one — gets on everything, ruins clothes, but it's the only thing between dry and wet. You learn to love the smell. Lucineer loves the smell. |
| `shell` | Shell | Shell beds, tidal pools | Hard, brittle, beautiful. Decorative + minor structural. | The vain one — pretty, sharp, and fragile. You use it for detail work, inlays, the knob on a door. It's the first material that's *chosen*, not just *used*. |
| `bone` | Bone | Beach finds, large fish | Hard, workable, dense. Tools, pegs, decorative. | The solemn one — it was alive. You honor it by making it useful. Bone pegs hold better than wood. Bone needles sew straighter than thorn. |

**Build Types:**

| Build Type | Cost | Unlocks | Description |
|---|---|---|---|
| `lean_to` | driftwood×3, canvas_scrap×2 | First structure | A one-sided shelter leaning against a rock or tree. Keeps rain off. Barely. |
| `debris_hut` | driftwood×5, sea_rope×2, palm_fiber×3 | Sleeping spot | A framework of driftwood covered in fiber and canvas. Small, warm, ugly. |
| `tideline_fence` | driftwood×4, sea_rope×2 | Perimeter marking | Low post-and-rope fence. Defines "yours." Won't stop anything determined. |
| `salvage_rack` | salvage_plank×3, driftwood×2 | Material drying | A raised rack for drying kelp, hide, fiber. First step toward processing. |
| `fire_pit` | beach_stone×6, driftwood×2 | Cooking, warmth, light | Ringed stones with a fire. The heart of the camp. |
| `driftwood_platform` | driftwood×8, sea_rope×4 | Raised building surface | A low platform above the sand. First step toward real foundations. |
| `workbench_scrap` | salvage_plank×4, driftwood×3, beach_stone×2 | Basic crafting | A crude workbench. Unlocks crafting table UI. |

**Era Gate — Advancement Requirement:**
Player must have built at least **4 distinct build types** from Era 1, including `fire_pit` and `workbench_scrap`. When these conditions are met, Lucineer walks the camp, assesses, and delivers his verdict.

**Lucineer Transition Dialogue (Era 1 → Era 2):**

> *[Lucineer sets down the adze. He walks the perimeter of the camp — the leaning debris hut, the smoking fire pit, the rack of drying kelp. He kicks the driftwood platform lightly, testing it. He nods once.]*

> **LUCINEER:** You've stopped sleeping in the sand. Good. That's the first thing a builder does — they get off the ground. The ground doesn't care about you. Get above it.

> *[He picks up a salvage plank, runs his thumb along the grain.]*

> **LUCINEER:** This plank came from somebody else's boat. Somebody who probably built it right, and it still wasn't enough. But the wood remembers what it was supposed to be. You've been stacking things on top of each other and hoping. Tomorrow, we frame. A frame is a decision that stays decided. Go look at your platform and tell me where the posts meet — *really* meet, not just lean. That's where we start.

> *[He flips the plank, examining the cross-section.]*

> **LUCINEER:** I'll bring the adze. You bring patience.

---

### Era 2: FRAME AND PLANK

> *"First real carpentry. Posts carry beams. Beams carry floors. The structure has opinions about where it wants to stand."*

**Aesthetic:** Timber-frame vernacular. Upright posts planted in notched sill beams, horizontal girts, diagonal braces. Walls are plank-on-frame — sawn boards fastened to a skeleton of load-bearing timber. Roofs gain actual pitch and overlap. Structures can be two stories. The visual language is *intentional geometry*: right angles exist, spans are deliberate, and the building's skeleton is visible and proud. Joints are pegged, not nailed — treenails and wedges. It looks like a shipwright built a house, because one did.

**Lucineer calls it:** "the honest years" or "when the wood learned to stand"

**Materials (Era 1 materials carry forward):**

| ID | Name | Found / Made | Properties | Personality |
|---|---|---|---|---|
| `timber` | Timber (Sawn) | Felling + sawing trees | Load-bearing, straight-grained, structural. Heavy. | The soldier — stands where you put it, carries what you give it, doesn't bend. Earns its position. You learn to read grain the way Lucineer reads weather: by feel. |
| `plank` | Plank (Sawn) | Sawing timber into boards | Flat, uniform thickness, variable width. Weather-resistant when painted. | The practical one — does what timber does but flat. Walls, floors, shelves, doors. The shape of civilization is the plank. |
| `treenail` | Treenail | Carved from hardwood offcuts | Cylindrical peg, ~2cm diameter. Wedge-driven into mortises. | The quiet hero — two pieces of wood that want to separate are held together by a third, smaller piece of wood. No metal. No glue. Just compression and faith. |
| `tar_boiled` | Tar (Refined) | Pitch double-boiled | Thicker, darker, stickier than raw pitch. Caulking and preservative. | Pitch grew up. Went through fire twice and came out harder. This is what you seal the seams with when you're tired of bailing. |
| `oakum` | Oakum | palm_fiber picked loose + tar | Fibrous, tarry, water-tight when packed. The caulker's best friend. | The problem-solver — you hammer it into the gap between planks and the sea gives up. Oakum is what stands between dry wood and rot. |
| `nail_wrought` | Wrought Nail | Forge (requires bellows + metal_fragment) | Hand-forged, square-section, tapered. Holds better than cut nails. | The first metal fastener. A luxury in Era 2. You count them. You straighten and reuse bent ones. Lucineer hoards them like coins. |
| `hinge_iron` | Iron Hinge | Forge | Wrought iron strap hinge. Allows doors and shutters to swing. | The diplomat between wood and movement — holds the door firmly but lets it move. The first articulation in your structures. |
| `glass_crude` | Crude Glass | Sand + potash + high heat (requires bellows) | Imperfect, bubbly, wavy. Lets light in. Not perfectly clear. | The dreamer — you can see *through* it. Roughly. The world on the other side is softened, distorted, beautiful. Every pane is a little different. |
| `shingle` | Wood Shingle | Split from billets with froe | Thin, tapered, overlapping. Modular roofing unit. | The crowd — one shingle is nothing. A hundred shingles, overlapped four deep, will shed rain for a decade. They work as a team. |
| `mortise_peg` | Mortise Peg | Hardwood, tapered | Wedge-shaped, driven through protruding treenail to expand and lock the joint. | The lock — when you drive the peg, the joint goes from assembled to *permanent*. The sound it makes — that particular thock — is the sound of a decision being made. |
| `brace_timber` | Diagonal Brace | Timber, shaped at angles | Prevents racking. Transfers lateral load. Makes rectangles rigid. | The stubborn one — resists sideways force. Without braces, your rectangular frame is just a parallelogram waiting to collapse. The brace is the argument that wins. |
| `sill_beam` | Sill Beam | Timber, squared and leveled | The foundation of a timber frame. Everything sits on the sill. | The patriarch — the first piece. Leveled, squared, set on stone or post. Get the sill wrong and everything above it is wrong. Get it right and the frame builds itself. |
| `canvas_woven` | Canvas (Woven) | Loom (requires palm_fiber ×6) | Tight weave, water-resistant, durable. Better than scraps. | Grew up from scraps. This is cloth you made on purpose, to the size you needed. The first manufactured material. |

**Build Types:**

| Build Type | Cost | Unlocks | Description |
|---|---|---|---|
| `post_and_beam` | timber×4, treenail×6, brace_timber×2 | Structural framing | The skeleton. Vertical posts in sill beams with horizontal girts. Load-bearing. |
| `plank_wall` | plank×6, timber×2, treenail×4 | Vertical enclosure | Sawn planks fastened to frame. Weather-tight when caulked. |
| `shingled_roof` | shingle×8, timber×3, treenail×4 | Weatherproof roofing | Overlapping shingles on timber rafters. First real rain protection. |
| `framed_floor` | timber×5, plank×4, treenail×6 | Second story | Raised floor on joists. Opens verticality. |
| `caulked_seam` | oakum×2, tar_boiled×1 | Waterproofing | Sealed plank seams. Keeps the weather and the vermin out. |
| `hinged_door` | plank×4, hinge_iron×2, nail_wrought×4 | Security, privacy | A real door that latches. You can close it and it stays closed. |
| `glazed_window` | glass_crude×2, timber×2, plank×2 | Light, view | Imperfect glass in a wooden frame. Wavy, beautiful, functional. |
| `framed_workshop` | timber×12, plank×15, treenail×20, shingle×10 | Advanced crafting | Full workshop with bench, tool rack, storage. Unlocks Era 2+ recipes. |
| `storehouse` | timber×8, plank×10, treenail×12 | Material storage | Dry, secure storage. Materials inside don't degrade. |
| `pier_jetty` | timber×10, plank×6, treenail×8 | Water access | A walkway over water. Dock boats, stage materials, fish from it. |
| `saw_pit` | timber×6, plank×4, beach_stone×4 | Plank production | A pit for two-man rip-sawing. Doubles plank output from timber. |
| `crane_post` | timber×6, sea_rope×4, brace_timber×4 | Heavy lifting | A simple wooden crane. Lifts materials to upper stories. |

**Era Gate — Advancement Requirement:**
Player must have built `post_and_beam` AND `framed_workshop`, plus at least **3 other distinct Era 2 build types**. Lucineer inspects the workshop specifically — its construction quality determines his assessment.

**Lucineer Transition Dialogue (Era 2 → Era 3):**

> *[Lucineer stands in the workshop doorway, one hand on the frame. He's been watching the player square a timber for the better part of an hour. He waits until the adze is set down.]*

> **LUCINEER:** This frame is good. I mean it — the joinery is honest, the braces are where they should be, and you pegged every mortise instead of cheating with nails. This building will stand through weather that strips paint off hulls.

> *[He steps inside, knocks a post with his knuckle. The sound is solid.]*

> **LUCINEER:** But wood is still wood. It rots. It burns. It warps when the season turns enough times. You've learned to shape it — now learn to outlast it. There's limestone in the cliff face and clay in the riverbed, and I'm going to show you what fire does to rock when you ask it properly.

> *[He picks up a lump of beach stone, turns it over.]*

> **LUCINEER:** Your great-grandfather's lighthouse stood for ninety years after he died. Wooden frame, stone skin. The frame held. The skin is what made it permanent. We're going to build something the sea can't take.

> *[He puts the stone in the player's hand.]*

> **LUCINEER:** Carry one of these to the workshop. Just one. We start with weight.

---

### Era 3: STONE AND MORTAR

> *"Permanence arrives. Walls have mass. Foundations go below the frost line. The building outlasts the builder."*

**Aesthetic:** Masonry vernacular. Dressed stone walls with lime-mortar joints, or fieldstone laid in courses. Brick appears where clay is fired. Foundations are trenched and laid with rubble and mortar. Roofs can be stone slab or tile. Structures gain real height — two and three stories, towers, thick walls that insulate against storm and cold. Arches and lintels span openings. The visual language is *deliberate weight*: buildings look grounded, immovable, permanent. Mortar lines are visible and proud. It looks like it was built to outlast you, because it was.

**Lucineer calls it:** "the permanent years" or "when the island agreed to keep us"

**Materials (Era 1–2 carry forward):**

| ID | Name | Found / Made | Properties | Personality |
|---|---|---|---|---|
| `limestone` | Limestone | Quarry face, cliff cuts | Soft enough to dress with hand tools, hard enough to last centuries. White to grey. | The agreeable one — lets you shape it, then hardens in place. Limestone doesn't fight you. It's the patient student that becomes the master. |
| `sandstone` | Sandstone | Cliff strata | Warm tones (buff, rust, red). Carves beautifully. Softer than limestone. | The artist — it *wants* to be carved. Given a chisel, it offers shapes. The colors are the island's painting. |
| `fieldstone` | Fieldstone | Surface collecting | Irregular shapes and sizes. Laid by eye, not by rule. | The wild one — every stone is a different problem. No two courses are the same. The waller who can read fieldstone is an artist working in a medium that has opinions. |
| `granite` | Granite | Deep quarry (requires effort) | Hardest structural stone. Premium. Resists everything. Hard to work. | The old god — it doesn't want to be shaped. You persuade it, with patience and steel, to accept the form you need. In return, it lasts forever. Forever is a long time. Respect it. |
| `brick_fire` | Fired Brick | Clay + kiln (requires fire_pit + fuel) | Uniform, modular, 2:1:4 proportion. Structural and modular. | The soldier's soldier — every brick is identical, every brick does its job, every brick trusts the brick next to it. The first mass-produced material. Democracy in clay. |
| `mortar_lime` | Lime Mortar | Limestone (burned) + sand + water | The binder. Without it, stone is just a pile. Cures by carbonation. | The glue with opinions — mortar is softer than the stone, which is correct. The mortar sacrifices itself so the stone can move with temperature and season. It's the first material whose job is to *fail* gracefully. |
| `concrete_crude` | Crude Concrete | Aggregate + lime + water | Poured, cast, structural. Sets by chemical reaction. | The shapeshifter — it starts as a liquid and ends as a rock. You pour it into a form, and when you remove the form, the form remains. It's the closest thing to magic in the material world. |
| `clay_raw` | Raw Clay | Riverbed, deposits | Plastic when wet, rigid when dry, ceramic when fired. Versatile. | The child — it takes whatever shape you give it. Leave it alone and it cracks. Fire it and it becomes permanent. Clay is the material that grows up. |
| `sand_fine` | Fine Sand | River, beach (sieved) | Fine aggregate for mortar and concrete. Clean, uniform. | The supporting cast — never the star, always necessary. Without sand, mortar cracks. Without sand, concrete fails. It's the most boring material in the encyclopedia and one of the most important. |
| `tile_roof` | Roof Tile | Fired clay, molded | Modular roofing. Overlapping. Red-orange to grey. | The reliable one — click, click, click, they interlock. Each tile covers the edge of the last. The roof that builds itself from repetition. |
| `slate` | Slate | Cliff strata (deep) | Splits into flat sheets. Dense, impermeable. Roofing and flooring. | The flake — hit it right and it splits perfectly. Hit it wrong and it shatters. Reading slate is a skill. Once you learn it, you have the best roofing material on the island. |
| `lead_sheet` | Lead Sheet | Smelted galena | Malleable, heavy, toxic. Waterproofing, flashing, pipes. | The necessary evil — it's poisonous, it's ugly, and nothing else works as well for flashing and waterproofing. You handle it carefully, wash your hands, and appreciate that it exists. |
| `rebar_crude` | Crude Iron Rod | Forge, drawn iron | Ribbed or rough iron rod for concrete reinforcement. Tension member. | The skeleton inside the body — concrete is strong in compression, weak in tension. Iron is the opposite. Together, they cover each other's weaknesses. The first composite material. The beginning of a new way of thinking. |

**Build Types:**

| Build Type | Cost | Unlocks | Description |
|---|---|---|---|
| `stone_foundation` | fieldstone×8, mortar_lime×4, sand_fine×4 | All Era 3 structures | Trenched and laid rubble foundation. Everything permanent sits on this. |
| `stone_wall` | limestone×10 (or fieldstone×12), mortar_lime×6 | Permanent enclosure | Dressed stone and mortar. Load-bearing, weatherproof, fireproof. |
| `brick_wall` | brick_fire×12, mortar_lime×4 | Modular enclosure | Fired brick in mortar. Faster than stone, very strong. |
| `arch_stone` | limestone×8, mortar_lime×3, timber×4 (formwork) | Wide spans | A stone arch. Spans openings no timber beam can match. |
| `stone_tower` | limestone×30, mortar_lime×15, timber×10, rebar_crude×4 | Height, signal platform | Circular or square tower, 3+ stories. The landmark structure. |
| `vaulted_ceiling` | brick_fire×15, mortar_lime×6, timber×8 (formwork) | Masonry roofing | Brick vault overhead. Permanent, fireproof, beautiful. |
| `tiled_roof` | tile_roof×12, timber×4, mortar_lime×2 | Premium roofing | Overlapping fired tiles on timber rafters. Lasts a century. |
| `slate_floor` | slate×6, mortar_lime×2 | Interior flooring | Flat slate tiles in mortar. Clean, durable, waterproof. |
| `stone_chimney` | brick_fire×8, mortar_lime×3, fieldstone×4 | Indoor heating | Full chimney with flue. Heats without filling the room with smoke. |
| `root_cellar` | fieldstone×10, mortar_lime×4, timber×3 | Cold storage | Below-grade stone chamber. Cool year-round. Food preservation. |
| `cistern` | brick_fire×10, mortar_lime×6, lead_sheet×2 | Water storage | Lined cistern collects rainwater. Independent water supply. |
| `lime_kiln` | limestone×8, brick_fire×6, timber×10 | Mortar production | Fires limestone into quicklime. The key to all masonry. |
| `forge_hearth` | brick_fire×10, mortar_lime×4, fieldstone×6, tar_boiled×2 | Metalworking | A proper forge. Unlocks iron and steel production. |
| `bridge_stone` | limestone×15, mortar_lime×8, timber×6 (formwork) | Permanent crossing | Stone arch bridge over water. Won't wash out. |

**Era Gate — Advancement Requirement:**
Player must have built `stone_foundation`, `stone_wall` (or `brick_wall`), `lime_kiln`, and at least **2 other distinct Era 3 build types**. Additionally, the player must have built at least one structure with a `vaulted_ceiling` or `stone_tower` — demonstrating they can work at height with masonry.

**Lucineer Transition Dialogue (Era 3 → Era 4):**

> *[Lucineer is on the catwalk of the stone tower, looking out over the bay. He heard the player coming up the spiral stairs — the echo in stone is different from wood. Wood absorbs. Stone reports. He speaks without turning.]*

> **LUCINEER:** You can hear yourself think in here. That's what stone does — it holds everything. Sound, heat, cold, and time. Your great-grandfather understood that. He built his workshop in timber and his lighthouse in stone, and the workshop burned down in 1953 and the lighthouse is still standing.

> *[He turns, leaning on the parapet.]*

> **LUCINEER:** You've learned weight. Now learn force. Stone holds still — it carries load, it endures, it waits. But what if the wall could *move*? What if the structure could *do* something — lift, pivot, pump — and do it every day, the same way, without tiring? That's not carpentry and it's not masonry. That's mechanism.

> *[He pulls folded drawings from his coat — gears, linkages, a water-driven arm.]*

> **LUCINEER:** I've been watching the river for a year. There's enough flow to turn a wheel that turns a shaft that turns a gear that lifts a hammer that shapes the iron that reinforces the concrete that holds the wheel. You see? It's a *circuit*. Not wire — not yet — but a circuit of stone and iron and water, and it runs itself.

> *[He hands the drawings over.]*

> **LUCINEER:** Bring me iron. Not fragments — *worked* iron. We're going to build the first machine this island has seen since the old light went dark.

---

### Era 4: METAL AND MACHINE

> *"Iron becomes steel. The structure stops sitting passively and starts working. Pumps pump. Cranes lift themselves. The building is a machine with a roof."*

**Aesthetic:** Industrial maritime. Iron-frame structures with riveted plates, exposed mechanism, and functional pipe runs. Stone and brick still form the base — but now they house boilers, turbines, line shafts. Steel beams span distances timber can't. Walls incorporate iron grilles, copper sheeting, brass fittings. The visual language is *honest mechanism*: gears, belts, pipes, and valves are visible and celebrated, not hidden behind cladding. Steam and smoke are present. It looks like a shipyard workshop crossed with a Victorian pumping station, because that's what it is.

**Lucineer calls it:** "the iron years" or "when the island learned to breathe steam"

**Materials (Era 1–3 carry forward):**

| ID | Name | Found / Made | Properties | Personality |
|---|---|---|---|---|
| `iron_bar` | Iron Bar (Worked) | Forge, reheated and drawn | Ductile, forgeable, strong in tension and compression. Rusts. | The former beachcomber that grew up — iron ore sat in the dirt for millennia. You found it, fed it fire, and it became the backbone of everything that followed. But it rusts. It always rusts. You paint it, oil it, embed it in concrete. You fight. |
| `steel_bar` | Steel Bar | Forge + carbon process (requires precise heat) | Iron with discipline. Harder, springier, holds an edge. Doesn't yield. | The graduate — iron went to school. Carbon taught it structure. Steel is iron that has learned to be exactly what you need: hard where it should be, flexible where it must be. |
| `steel_plate` | Steel Plate | Rolling mill (requires power) | Flat sheet steel. Walls, tanks, hulls. Can be cut and welded. | The skin of the new world — flat, uniform, strong. The first material that comes in exactly the shape you need. No carving, no splitting. Cut and fasten. |
| `steel_beam` | Steel I-Beam | Rolling mill | Long-span structural member. Replaces timber girts entirely. | The bridge between eras — a shape designed by mathematics. The I-beam puts material only where stress lives: flanges top and bottom, web between. It's the first material that was *calculated* before it was made. |
| `rivet_iron` | Iron Rivet | Forge, headed and shanked | Red-hot driven, contracts as it cools, clamps permanently. | The newborn fastener — placed while hot, it shrinks as it cools, pulling the joint tight. Every rivet is a tiny embrace that strengthens as it settles. Millions of them held the ships and bridges of the industrial world together. |
| `copper_sheet` | Copper Sheet | Smelted copper, rolled | Malleable, corrosion-resistant. Starts salmon-pink, goes green. | The patina philosopher — it changes color as it ages, and the change *protects* it. The verdigris isn't decay; it's armor. Copper is the material that turns aging into a feature. |
| `brass_fitting` | Brass Fitting | Copper + zinc, cast | Gold-colored, corrosion-proof, machinable. Valves, connectors. | The diplomat — brass gets along with everything. Doesn't corrode in iron. Doesn't corrode in copper. Doesn't corrode in salt water. It's the material you use at the boundary between metals that hate each other. |
| `pipe_iron` | Iron Pipe | Cast or drawn | Pressurized fluid transport. Threaded or flanged joints. | The circulatory system — fluid goes where the pipe goes. Unlike wood or clay, iron pipe holds pressure. Steam, water, oil — it carries the fluids that make machines work. |
| `boiler_plate` | Boiler Plate | Thick steel plate, riveted or welded | Pressure vessel grade. Holds steam pressure without rupturing. | The responsible one — when this fails, people die. Boiler plate is treated with respect from smelting to installation. Every rivet is inspected. Every seam is tested. It carries the weight of trust. |
| `glass_sheet` | Sheet Glass | Improved furnace (requires flat-cast process) | Flat, clear, uniform panes. Real windows, finally. | Glass grew up — the bubbles and waves of crude glass are gone (or at least minimized). Sheet glass is transparency you can count on. The world outside looks the way it actually looks. |
| `cable_steel` | Steel Cable | Drawn wire, spun into rope | Extreme tensile strength. Flexible. Heavy lifting and tension. | The muscle — spun from wire thinner than hair into cables thicker than your wrist. Steel cable bends where steel beam cannot, and carries almost as much load. The crane, the bridge, the elevator all depend on it. |
| `girder_riveted` | Riveted Girder | Steel plate + angles + rivets | Built-up structural beam. Custom depth and profile. | The tailored suit — when a standard I-beam isn't deep enough or strong enough, you build a girder from plates and angles and rivets. It's bespoke engineering. Each one is designed for its specific load. |
| `concrete_reinforced` | Reinforced Concrete | Concrete + steel rebar grid | Strong in compression AND tension. Cast in forms. | The partnership that changed construction forever — concrete resists crushing, steel resists stretching. Together, they're complete. This is the material of the twentieth century: dams, bridges, skyscrapers, highways. It starts as mud and becomes a mountain. |

**Build Types:**

| Build Type | Cost | Unlocks | Description |
|---|---|---|---|
| `iron_frame` | steel_beam×6, rivet_iron×12, iron_bar×4 | Steel structural skeleton | Riveted steel frame. Replaces timber framing. Spans further, carries more. |
| `steel_wall` | steel_plate×8, rivet_iron×8, iron_bar×2 | Metal enclosure | Riveted steel plate walls. Fireproof, storm-proof. |
| `boiler_house` | boiler_plate×8, pipe_iron×4, valve×2, brick_fire×6 | Steam power | Boiler house with feedwater system. Produces pressurized steam. |
| `engine_house` | steel_beam×8, steel_plate×6, rivet_iron×10, pipe_iron×4 | Mechanical power | Houses steam engine or turbine. Drives line shafts. |
| `line_shaft_system` | iron_bar×6, steel_bar×4, bearing×4, belt_drive×2 | Power distribution | Overhead shafts carrying rotational power to workstations. |
| `powered_hammer` | steel_beam×4, iron_bar×6, cable_steel×2, gear×4 | Automated forging | Steam-powered trip hammer. Forges what muscle cannot. |
| `powered_crane` | steel_beam×8, cable_steel×4, gear×6, pipe_iron×2 | Heavy lift | Powered overhead crane. Lifts entire frames into place. |
| `pumping_station` | brick_fire×10, pipe_iron×6, valve×3, boiler_plate×4 | Water management | Pumps water from mines, cisterns, low ground. Civil engineering. |
| `copper_roof` | copper_sheet×8, timber×3 | Premium roofing | Copper sheet roofing. Bright, then green, then centuries-old. |
| `glass_wall` | glass_sheet×8, steel_beam×4, iron_bar×4 | Curtain wall | Wall of glass in steel frame. Light floods in. The future. |
| `workshop_industrial` | steel_beam×15, steel_plate×10, rivet_iron×20, pipe_iron×6, brick_fire×8 | Advanced crafting | Full industrial workshop. Line-shaft powered. Unlocks Era 4+ recipes. |
| `concrete_struct` | concrete_reinforced×8, rebar_crude×6 | Poured structures | Reinforced concrete walls, floors, platforms. Cast in forms. |
| `gantry_rail` | steel_beam×4, iron_bar×4, rivet_iron×6 | Crane mobility | Overhead rail system. Crane moves along it. Covers the whole yard. |
| `wind_turbine_mech` | steel_plate×6, steel_beam×4, gear×4, cable_steel×2 | Wind power | Mechanical wind turbine. Drives shafts when the steam is off. |

**Era Gate — Advancement Requirement:**
Player must have built `boiler_house` or `engine_house` AND `workshop_industrial`, plus at least **3 other distinct Era 4 build types**. The player must also demonstrate a working **power transmission chain** — a powered machine connected via line shaft or belt to a power source. Lucineer tests this by asking the player to run the workshop from a single prime mover.

**Lucineer Transition Dialogue (Era 4 → Era 5):**

> *[The industrial workshop hums with shaft power. Lucineer is standing at the far end, where the line shaft terminates in a dead pulley. He's been staring at it. The pulley spins, connected to nothing, uselessly turning. He puts his hand on it — gently, feeling the rotation.]*

> **LUCINEER:** Everything in this room moves because of that shaft. One wheel, and the whole building works. One fire, and the whole island moves. We took the river and the wind and the coal and we made them *turn* — and that was the hardest thing humans ever learned to do.

> *[He stops the pulley with his palm. The shaft keeps spinning elsewhere — the workshop doesn't care about one stopped wheel.]*

> **LUCINEER:** But it's dark in here. Not the light — I mean the mechanism. The shaft turns, and we can see it turn. The belt moves, and we can watch it move. But the *reason* it moves — the decision to send power here instead of there — that's still made by a person pulling a lever. The machines are strong but they're stupid. They do exactly what you tell them and they never ask why.

> *[He reaches into his coat and produces something small. A wire. A filament. He holds it up to the window light.]*

> **LUCINEER:** I found this in the lighthouse ruins. It's the last filament from the old light. Glass cracked, brass corroded, but the wire — the wire is intact. Somebody, a hundred years ago, pushed a current through this and it *glowed*. Not burned. Not flickered. Glowed. Steady. Clean. A small sun that lived in a glass bottle and asked nothing of the world except to be connected.

> *[He turns to the player.]*

> **LUCINEER:** You've built the muscle. Now build the nerve. I want you to coil a thousand turns of copper around an iron core and spin it until the wire glows. Then I want you to climb that stone tower and hang the light where the old one hung. The ships aren't coming anymore — but the light was never just for them. It was for *us*. Proof that we're here. Proof that someone is home.

> *[He puts the filament in the player's hand.]*

> **LUCINEER:** Don't break it. It survived a century in the dark for you.

---

### Era 5: LIGHT AND SIGNAL

> *"Electricity transforms everything. Buildings speak to each other across the water. The lighthouse works again. The island is no longer alone."*

**Aesthetic:** Electrified maritime. The stone and steel buildings of Era 3–4 now carry wire, lamps, switchboxes, and antennas. The lighthouse — the emotional anchor of the entire game — is restored and operational. Copper wire runs along ceiling joists and through conduit. Lamps glow steady in windows for the first time. Telegraph wires cross between buildings. The visual language is *connection*: every structure is a node, every wire is a link, every lamp is a statement. At night, the island glows. From the tower, signal lamps can reach the horizon. It looks like a coast that has rejoined the world.

**Lucineer calls it:** "the year the light came back" or "when the island remembered it had a voice"

**Materials (Era 1–4 carry forward):**

| ID | Name | Found / Made | Properties | Personality |
|---|---|---|---|---|
| `copper_wire` | Copper Wire | Refined copper, drawn through dies | Excellent conductor, ductile, oxidation-resistant. The bloodstream of electricity. | The messenger — copper wire carries the invisible. You can't see electricity. You can see the wire. Every lamp, every motor, every signal is copper reaching out to copper. The island's nervous system, spun by hand. |
| `magnet` | Permanent Magnet | Iron + lodestone, or electromagnetized steel | Produces a persistent magnetic field. The heart of every generator and motor. | The invisible force — you can't see the field, can't feel it, can't weigh it. But put iron near it and the iron *jumps*. The magnet is the first material that does something without being touched. |
| `filament` | Lamp Filament | Tungsten or carbon, coiled | Heats to incandescence in vacuum. Produces light from electricity. | The fragile miracle — a wire so thin it's almost invisible, sealed in a glass vacuum, heated to 3000 degrees. It glows. It's the most human material in the encyclopedia: fragile, brilliant, and it burns out eventually. Everything about it is a metaphor for being alive. |
| `bulb_glass` | Bulb Glass (Envelope) | Glass blown/cast to precise shape | Vacuum-tight enclosure for filament. Transparent to visible light. | The cradle — it holds the filament in vacuum so it doesn't burn. The glass doesn't produce light; it *protects* the light. The most important invisible job in the system. |
| `insulator_porc` | Porcelain Insulator | Fired ceramic, glazed | Non-conductive. Prevents current leakage at wire terminations. | The boundary — electricity goes where copper tells it and nowhere else. The insulator is the material that says *no*. Without it, current leaks everywhere and nothing works. Freedom requires boundaries. |
| `brass_contact` | Brass Contact | Brass, machined | Spring-loaded electrical contact. Switches, sockets, connectors. | The handshake — the point where current passes from one body to another. Every switch click is brass touching brass. Every socket is brass embracing brass. The mechanical poetry of connection. |
| `antenna_wire` | Antenna (Wire) | Copper or brass, long span | Radiates and receives electromagnetic waves. The bridge across distance. | The voice that carries — string a wire between two high points and suddenly information crosses water faster than a boat. The antenna doesn't carry electricity; it carries *meaning*. Every message it sends is a prayer that someone is listening. |
| `lens_fresnel` | Fresnel Lens | Cast glass, concentric rings | Focuses light into a parallel beam visible at extreme distance. | The visionary — a flat-ish lens that does the work of a thick one. Concentric rings step the glass down, focusing light into a beam that reaches the horizon. It's the most beautiful piece of glass ever designed, and every lighthouse on earth owes its reach to it. |
| `circuit_board` | Circuit Board | Copper-clad board, etched | Substrate for mounting and connecting electronic components. | The map — copper traces on insulation, drawing the circuit in two dimensions. The board is the geography of a machine. Every line is a road, every pad is a destination, every component is a building. The circuit board is where engineering became architecture. |
| `semiconductor` | Semiconductor | Purified silicon or germanium | The basis of diodes, transistors, and all modern electronics. | The alchemist's stone — sand, purified beyond imagining, becomes a material that can *decide*. The semiconductor is the last material in the encyclopedia and the first one that thinks. Everything before it was passive. This one amplifies, switches, and controls. It's the brain of the final era. |
| `fiber_optic` | Fiber Optic Strand | Drawn glass, ultra-pure | Transmits light signals over long distances with minimal loss. | The final material — a thread of glass finer than hair that carries light around corners, across water, through walls. It's copper wire's successor: faster, lighter, immune to the elements. A single strand carries more information than every telegraph wire on the island combined. |

**Build Types:**

| Build Type | Cost | Unlocks | Description |
|---|---|---|---|
| `wire_run` | copper_wire×4, insulator_porc×4, timber×2 | Power distribution | Run wire between buildings. First electrical infrastructure. |
| `lamp_post` | copper_wire×2, filament×1, bulb_glass×1, iron_bar×2 | Exterior lighting | A lamp on a post. The yard is lit at night. Transformative. |
| `switch_box` | copper_wire×3, brass_contact×2, iron_bar×1, circuit_board×1 | Power control | A switch panel. Control power to different circuits. |
| `generator_house` | steel_beam×6, steel_plate×4, brick_fire×8, copper_wire×6, pipe_iron×4 | Power generation | A proper generator house. Mechanical power becomes electricity. |
| `battery_bank` | copper_wire×4, iron_bar×4, lead_sheet×4, brick_fire×4 | Power storage | Banks of batteries. Electricity available when the generator isn't running. |
| `lighthouse_restored` | stone_tower×1, lens_fresnel×1, filament×4, bulb_glass×4, copper_wire×8, brass_contact×4, circuit_board×2 | THE landmark | The lighthouse, fully restored. The emotional climax of the building game. Light reaches the horizon. |
| `telegraph_station` | copper_wire×4, brass_contact×2, iron_bar×2, circuit_board×1 | Communication | Send and receive Morse code messages. Text communication across wire. |
| `signal_tower` | steel_beam×8, antenna_wire×4, copper_wire×6, circuit_board×2 | Long-range signal | A radio signal tower. Communicate beyond the island's shores. |
| `workshop_electrical` | workshop_industrial×1, wire_run×4, switch_box×2, lamp_post×4, generator_house×1 | Electrical crafting | Full electrified workshop. Power tools. Unlocks Era 5+ recipes. |
| `grid_system` | wire_run×8, switch_box×4, transformer×2, copper_wire×10 | Island power grid | A complete electrical grid connecting all structures. Every building has power. |
| `intercom_system` | copper_wire×6, brass_contact×4, circuit_board×2, speaker×2 | Building communication | Wired communication between buildings. Talk across the island. |
| `automated_gate` | steel_plate×4, iron_bar×4, solenoid×2, copper_wire×3, circuit_board×1 | Remote access | A gate that opens and closes electrically. Security with convenience. |
| `beacon_light` | filament×2, bulb_glass×2, copper_wire×3, lens_fresnel×1, steel_beam×2 | Navigation aid | A secondary beacon. Guides boats, marks channels. Multiple beacons = safe passage. |
| `workshop_automation` | circuit_board×4, semiconductor×4, copper_wire×8, sensor×4, steel_beam×4 | Automated production | Machines that run themselves based on sensor input. The threshold of autonomy. |

**Era Gate — Final Era.**
There is no Era 6 in the building system. Era 5 is the capstone. The lighthouse restored is the game's emotional endpoint — not a "you win" screen, but a moment of profound quiet. The light is on. The island is visible again. Ships that passed in the dark now see something on the horizon.

**Lucineer Final Dialogue (Lighthouse Restored):**

> *[Dusk. The filament warms — not all at once, but gradually, the way a candle settles into its flame. The Fresnel lens catches the glow and throws it outward, a horizontal fan of light that sweeps the bay and reaches for the horizon. Lucineer stands at the parapet, both hands on the rail, watching the beam find the dark water.]*

> **LUCINEER:** There.

> *[Long silence. The beam rotates. The island, for the first time in decades, casts light beyond its own shore.]*

> **LUCINEER:** Your great-grandfather stood here. Different light, same lens, same stone, same view. He hung the lamp because he couldn't stand the dark. Not the dark on the island — the dark *out there*. The empty water where nobody knows you're alive. The light doesn't bring ships. The light says: *someone is here. Someone built something. Someone stayed.*

> *[He turns to the player. His face is lit from below by the beam's scatter.]*

> **LUCINEER:** You learned salvage. Then carpentry. Then stone. Then iron. Then this — a wire that glows because you asked it to. Five lessons. Each one harder, each one more permanent, each one less about *you* and more about *what comes after you*. That's what building is. It's not the structure. It's the conversation between your hands and the people who will stand here when your hands are gone.

> *[He puts his hand on the lens housing — the same housing, refurbished, that held the original light.]*

> **LUCINEER:** The light's yours now. Keep it burning. That's all anyone can do.

> *[He looks out. The beam sweeps the bay. Somewhere on the water, far out, a boat that has been navigating by stars alone for hours adjusts its heading by two degrees toward the light.]*

> **LUCINEER:** *(quietly)* There's always someone out there.

---

## 2. MATERIAL ENCYCLOPEDIA — MASTER INDEX

*All 40 materials, sorted by first appearance. Lucineer's name for each material appears in parentheses where it differs from the formal name.*

### Era 1 Materials (11)

| # | ID | Name (Lucineer's Name) | Era | Category | Density | Workability | Durability | Water Resist |
|---|---|---|---|---|---|---|---|---|
| 1 | `driftwood` | Driftwood ("sea-bone") | 1 | Organic | Low | High | Low | Poor |
| 2 | `salvage_plank` | Salvaged Plank | 1 | Reclaimed | Medium | Medium | Medium | Fair |
| 3 | `rawhide` | Rawhide | 1 | Organic | Medium | Medium | Medium (dry) | Poor (wet) |
| 4 | `palm_fiber` | Palm Fiber | 1 | Organic | Low | High | Low | Poor |
| 5 | `kelp_dried` | Dried Kelp | 1 | Organic | Low | High | Low | Good |
| 6 | `sea_rope` | Sea Rope | 1 | Manufactured | Low | — | Low | Good |
| 7 | `beach_stone` | Beach Stone ("patience") | 1 | Mineral | High | Low (hard) | Very High | Excellent |
| 8 | `canvas_scrap` | Canvas Scrap | 1 | Reclaimed | Low | Medium | Low | Fair |
| 9 | `pitch` | Pitch | 1 | Hydrocarbon | Medium | — (adhesive) | Medium | Good |
| 10 | `shell` | Shell | 1 | Organic (CaCO₃) | Medium | Low (brittle) | High | Excellent |
| 11 | `bone` | Bone | 1 | Organic | Medium | Medium (carvable) | High | Good |

### Era 2 Materials (13 new, 11 carry forward = 24 total)

| # | ID | Name (Lucineer's Name) | Era | Category | Density | Workability | Durability | Water Resist |
|---|---|---|---|---|---|---|---|---|
| 12 | `timber` | Timber ("the backbone") | 2 | Wood | High | Medium | Medium | Fair (treated) |
| 13 | `plank` | Plank | 2 | Wood | Medium | High | Medium | Fair (treated) |
| 14 | `treenail` | Treenail ("trust peg") | 2 | Wood (hardwood) | Medium | — (finished) | High | Good |
| 15 | `tar_boiled` | Refined Tar | 2 | Hydrocarbon | Medium | — (sealant) | Medium | Excellent |
| 16 | `oakum` | Oakum | 2 | Composite (fiber+tar) | Low | — (caulking) | Medium | Excellent |
| 17 | `nail_wrought` | Wrought Nail | 2 | Metal | High | — (finished) | Very High | Poor (rusts) |
| 18 | `hinge_iron` | Iron Hinge | 2 | Metal | High | — (finished) | Very High | Poor (rusts) |
| 19 | `glass_crude` | Crude Glass ("dream-glass") | 2 | Glass | Medium | Low (brittle) | High (if unbroken) | Excellent |
| 20 | `shingle` | Wood Shingle | 2 | Wood | Low | High | Medium | Fair |
| 21 | `mortise_peg` | Mortise Peg ("the lock") | 2 | Wood (hardwood) | Medium | — (finished) | High | Good |
| 22 | `brace_timber` | Diagonal Brace ("the argument") | 2 | Wood | Medium | Medium | High | Fair |
| 23 | `sill_beam` | Sill Beam ("the patriarch") | 2 | Wood | High | Medium | High | Fair (treated) |
| 24 | `canvas_woven` | Woven Canvas | 2 | Manufactured | Low | Medium | Medium | Good |

### Era 3 Materials (13 new, 24 carry forward = 37 total)

| # | ID | Name (Lucineer's Name) | Era | Category | Density | Workability | Durability | Water Resist |
|---|---|---|---|---|---|---|---|---|
| 25 | `limestone` | Limestone ("the student") | 3 | Stone | High | Medium (dressable) | Very High | Good |
| 26 | `sandstone` | Sandstone ("the artist") | 3 | Stone | High | High (carvable) | High | Fair (porous) |
| 27 | `fieldstone` | Fieldstone ("the wild one") | 3 | Stone | High | Low (irregular) | Very High | Good |
| 28 | `granite` | Granite ("the old god") | 3 | Stone | Very High | Very Low (hard) | Exceptional | Excellent |
| 29 | `brick_fire` | Fired Brick | 3 | Ceramic | Medium | — (modular) | Very High | Excellent |
| 30 | `mortar_lime` | Lime Mortar ("the binder") | 3 | Composite | Medium | — (paste) | High (cures) | Good |
| 31 | `concrete_crude` | Crude Concrete ("the shapeshifter") | 3 | Composite | High | — (poured) | Very High | Good |
| 32 | `clay_raw` | Raw Clay ("the child") | 3 | Ceramic (raw) | High | Very High (plastic) | Low (wet) / High (fired) | Poor (wet) / Excellent (fired) |
| 33 | `sand_fine` | Fine Sand | 3 | Mineral | High | — (aggregate) | — (inert) | — (inert) |
| 34 | `tile_roof` | Roof Tile | 3 | Ceramic | Medium | — (modular) | Very High | Excellent |
| 35 | `slate` | Slate ("the flake") | 3 | Stone | High | Special (splits) | Very High | Excellent |
| 36 | `lead_sheet` | Lead Sheet | 3 | Metal (heavy) | Very High | Very High (malleable) | Exceptional | Excellent |
| 37 | `rebar_crude` | Crude Iron Rod ("the inner skeleton") | 3 | Metal | High | — (finished) | Very High | Poor (embeds in concrete) |

### Era 4 Materials (13 new, 37 carry forward = 50 total)

| # | ID | Name (Lucineer's Name) | Era | Category | Density | Workability | Durability | Water Resist |
|---|---|---|---|---|---|---|---|---|
| 38 | `iron_bar` | Iron Bar | 4 | Metal | High | Medium (forgeable) | Very High | Poor (rusts) |
| 39 | `steel_bar` | Steel Bar ("the graduate") | 4 | Metal | High | Medium (forgeable) | Exceptional | Poor (rusts) |
| 40 | `steel_plate` | Steel Plate | 4 | Metal | High | Medium (cuttable) | Exceptional | Poor (needs coating) |
| 41 | `steel_beam` | Steel I-Beam | 4 | Metal | High | — (finished) | Exceptional | Poor (needs coating) |
| 42 | `rivet_iron` | Iron Rivet | 4 | Metal | High | — (hot-driven) | Very High | Poor (rusts) |
| 43 | `copper_sheet` | Copper Sheet | 4 | Metal | Medium | Very High (malleable) | Exceptional (patina) | Excellent |
| 44 | `brass_fitting` | Brass Fitting | 4 | Metal (alloy) | Medium | High (machinable) | Exceptional | Excellent |
| 45 | `pipe_iron` | Iron Pipe | 4 | Metal | High | — (finished) | Very High | Fair (rusts slowly) |
| 46 | `boiler_plate` | Boiler Plate | 4 | Metal (heavy) | Very High | — (specialized) | Exceptional | Good |
| 47 | `glass_sheet` | Sheet Glass | 4 | Glass | Medium | Low (brittle) | High | Excellent |
| 48 | `cable_steel` | Steel Cable ("the muscle") | 4 | Metal (composite) | High | — (flexible) | Very High | Fair (greased) |
| 49 | `girder_riveted` | Riveted Girder | 4 | Metal (built-up) | Very High | — (bespoke) | Exceptional | Poor (needs coating) |
| 50 | `concrete_reinforced` | Reinforced Concrete | 4 | Composite | Very High | — (cast in form) | Exceptional | Excellent |

### Era 5 Materials (11 new, 50 carry forward = 61 total)

| # | ID | Name (Lucineer's Name) | Era | Category | Density | Workability | Durability | Water Resist |
|---|---|---|---|---|---|---|---|---|
| 51 | `copper_wire` | Copper Wire ("the messenger") | 5 | Metal (conductor) | Low | — (drawn) | High | Good (insulated) |
| 52 | `magnet` | Permanent Magnet | 5 | Metal (magnetic) | High | — (finished) | Permanent | Excellent |
| 53 | `filament` | Lamp Filament ("the fragile miracle") | 5 | Metal (refractory) | Very Low | — (specialized) | Low (burns out) | N/A (vacuum) |
| 54 | `bulb_glass` | Bulb Glass ("the cradle") | 5 | Glass | Low | Special (blown) | Medium (fragile) | Excellent |
| 55 | `insulator_porc` | Porcelain Insulator | 5 | Ceramic | Medium | — (finished) | Very High | Excellent |
| 56 | `brass_contact` | Brass Contact ("the handshake") | 5 | Metal (alloy) | Medium | High (machinable) | Very High | Excellent |
| 57 | `antenna_wire` | Antenna Wire | 5 | Metal (conductor) | Low | — (spanned) | High | Good |
| 58 | `lens_fresnel` | Fresnel Lens ("the visionary") | 5 | Glass (precision) | Medium | — (cast/rings) | Very High | Excellent |
| 59 | `circuit_board` | Circuit Board ("the map") | 5 | Composite | Low | — (etched) | High | Good (coated) |
| 60 | `semiconductor` | Semiconductor ("the thinking stone") | 5 | Semiconductor | Low | — (cleanroom) | Very High | Excellent (sealed) |
| 61 | `fiber_optic` | Fiber Optic Strand | 5 | Glass (ultra-pure) | Very Low | — (drawn) | High (in sheath) | Good (sheathed) |

---

## 3. ERA TRANSITION MECHANICS

### 3.1 No XP, No Grinding

Per the Integrated Architecture: **Attention is the only currency.** There is no XP bar. There is no "level up." Era advancement is driven by **building milestones** — physical evidence of mastery — assessed by Lucineer in narrative dialogue.

The mechanic is simple:

1. **Build qualifying structures.** Each era defines required builds and a minimum number of distinct builds from that era's catalog.
2. **The game silently tracks these.** No progress bar is shown. No "3 of 4 required builds" notification appears. The player builds because they want or need the structure, not because a bar is filling.
3. **When conditions are met, Lucineer arrives.** He walks the site. He inspects. He delivers his verdict — the transition dialogue. Then the next era's materials and build types unlock.
4. **The player can refuse.** If the player says "not yet" or ignores Lucineer, nothing bad happens. The era gate remains open. There is no penalty for waiting. The next era is ready when the player is.

### 3.2 Qualification Logic

```lua
-- In EraSystem/init.lua, add building era tracking:

local BUILDING_ERA_REQUIREMENTS = {
    [1] = {  -- Era 1 → 2
        requiredBuilds = { "fire_pit", "workbench_scrap" },
        minDistinctBuilds = 4,
        validBuilds = {
            "lean_to", "debris_hut", "tideline_fence", "salvage_rack",
            "fire_pit", "driftwood_platform", "workbench_scrap",
        },
    },
    [2] = {  -- Era 2 → 3
        requiredBuilds = { "post_and_beam", "framed_workshop" },
        minDistinctBuilds = 5,
        validBuilds = {
            "post_and_beam", "plank_wall", "shingled_roof", "framed_floor",
            "caulked_seam", "hinged_door", "glazed_window", "framed_workshop",
            "storehouse", "pier_jetty", "saw_pit", "crane_post",
        },
    },
    [3] = {  -- Era 3 → 4
        requiredBuilds = { "stone_foundation", "lime_kiln" },
        minDistinctBuilds = 6,
        requiresHeightBuild = true,  -- vaulted_ceiling OR stone_tower
        validBuilds = {
            "stone_foundation", "stone_wall", "brick_wall", "arch_stone",
            "stone_tower", "vaulted_ceiling", "tiled_roof", "slate_floor",
            "stone_chimney", "root_cellar", "cistern", "lime_kiln",
            "forge_hearth", "bridge_stone",
        },
        heightBuilds = { "vaulted_ceiling", "stone_tower" },
    },
    [4] = {  -- Era 4 → 5
        requiredBuilds = { "workshop_industrial" },
        requiresPowerChain = true,  -- power source → line shaft → powered machine
        minDistinctBuilds = 5,
        validBuilds = {
            "iron_frame", "steel_wall", "boiler_house", "engine_house",
            "line_shaft_system", "powered_hammer", "powered_crane",
            "pumping_station", "copper_roof", "glass_wall",
            "workshop_industrial", "concrete_struct", "gantry_rail",
            "wind_turbine_mech",
        },
        powerChainBuilds = {
            sources = { "boiler_house", "engine_house", "wind_turbine_mech" },
            distribution = { "line_shaft_system" },
            consumers = { "powered_hammer", "powered_crane", "pumping_station" },
        },
    },
    -- Era 5 is the final era. No advancement check.
}

function EraSystem.checkBuildingEraAdvancement(playerName)
    local currentEra = EraSystem.getCurrentEra(playerName)
    local req = BUILDING_ERA_REQUIREMENTS[currentEra]
    if not req then return false end  -- Final era or invalid

    local counts = playerBuildCounts[playerName] or {}
    local distinctCount = 0
    local hasAllRequired = true

    -- Check required builds
    for _, buildType in ipairs(req.requiredBuilds) do
        if not (counts[buildType] and counts[buildType] > 0) then
            hasAllRequired = false
        end
    end

    -- Count distinct valid builds
    for _, buildType in ipairs(req.validBuilds) do
        if counts[buildType] and counts[buildType] > 0 then
            distinctCount = distinctCount + 1
        end
    end

    if not hasAllRequired then return false end
    if distinctCount < req.minDistinctBuilds then return false end

    -- Check special requirements
    if req.requiresHeightBuild then
        local hasHeight = false
        for _, buildType in ipairs(req.heightBuilds or {}) do
            if counts[buildType] and counts[buildType] > 0 then
                hasHeight = true
                break
            end
        end
        if not hasHeight then return false end
    end

    if req.requiresPowerChain then
        -- Check that player has at least one source, one distribution, and one consumer
        local hasSource = checkAnyBuilt(req.powerChainBuilds.sources, counts)
        local hasDist = checkAnyBuilt(req.powerChainBuilds.distribution, counts)
        local hasConsumer = checkAnyBuilt(req.powerChainBuilds.consumers, counts)
        if not (hasSource and hasDist and hasConsumer) then return false end
    end

    return true  -- Ready for advancement
end
```

### 3.3 Lucineer's Assessment — The Narrative Layer

The milestone check is mechanical. Lucineer's assessment is narrative. When the check returns `true`, the system triggers a **Lucineer visit event**:

1. Lucineer walks to the player's primary build site (highest-investment structure).
2. He performs a slow inspection animation — pacing, examining joints, testing beams.
3. He delivers the era transition dialogue (as written above).
4. The dialogue ends with an implicit invitation — he doesn't say "Era 3 unlocked." He says "bring me iron" or "carry one of these to the workshop." The game unlocks new materials and build types silently. The player discovers them by trying.
5. A brief musical shift — the BeatClock tempo map eases into the next era's default tempo (Era 1: Largo 40, Era 2: Andante 70, Era 3: Moderato 85, Era 4: Allegro 110, Era 5: Adagio 55 — slower because the work is more precise).

### 3.4 The Refusal State

If the player does not engage with Lucineer's visit (walks away, ignores the dialogue), the era gate remains open. Lucineer may return on the next session with a shorter, different prompt:

> **LUCINEER:** You've built enough to move on. Whenever you're ready. No rush. The stone isn't going anywhere.

This can repeat. There is no penalty for delayed advancement. Some players will want to build extensively within an era before moving on — building a complete Era 2 village before touching stone. This is valid and encouraged. The system does not rush.

---

## 4. VISUAL PROGRESSION — HOW THE ISLAND CHANGES

### 4.1 Environmental Changes Per Era

The island itself responds to the player's progression. These changes are applied via the existing `worldChanges` table in the EraSystem definitions, extended for building eras:

**Era 1: Driftwood and Salvage**
- **Sky:** Dawn coastal — warm, hazy, low contrast. Everything feels tentative and new.
- **Ambient sound:** Wind and waves only. Bird calls. No mechanical sound.
- **Vegetation:** Sparse, wind-bent. Grass on sand. No gardens.
- **Lighting:** Natural only. Fire pit glow at night. Stars are very bright (no light pollution).
- **Atmosphere:** Sea mist, light fog in mornings. The world feels large and empty.
- **Particle density:** 0.3 — drifting sea foam, occasional pollen.
- **Water color:** Deep blue-grey. Untouched.

**Era 2: Frame and Plank**
- **Sky:** Morning — clearer, higher contrast. The haze lifts.
- **Ambient sound:** Add sawing, hammering, wood-splitting. The sounds of work.
- **Vegetation:** Planted trees appear (if player has planted). Gardens possible.
- **Lighting:** Lamp light from windows (oil lamps). Warm interior glow.
- **Atmosphere:** Sawdust haze near workshop. Wood smoke from chimneys.
- **Particle density:** 0.4 — sawdust motes, smoke wisps.
- **Water color:** Same blue-grey, but a small dock changes the shoreline feel.

**Era 3: Stone and Mortar**
- **Sky:** Midday — full clarity, strong shadows. The world feels permanent and solid.
- **Ambient sound:** Add stone-cutting, mortar-mixing, the rhythmic clang of the forge.
- **Vegetation:** Mature trees (time has passed). Stone walls define property. Gardens are established.
- **Lighting:** Lamp light steadier. Glowing windows in stone walls. Forge fire visible through workshop openings.
- **Atmosphere:** Dust from the quarry. Steam from the lime kiln. The air smells of minerals.
- **Particle density:** 0.6 — stone dust, forge smoke, lime mist.
- **Water color:** Slightly greenish near shore (quarry runoff, lime).

**Era 4: Metal and Machine**
- **Sky:** Late afternoon — industrial amber. Smoke on the horizon from the boiler stack.
- **Ambient sound:** Add the constant hum of the line shaft, the hiss of steam, the rhythmic clang of the powered hammer. The island has a mechanical heartbeat.
- **Vegetation:** Trees pushed back by industry. Gardens still tended but the yard is dominated by iron and stone.
- **Lighting:** Electric arc light in the workshop (if generator is running). Brighter, whiter, harsher than oil lamps.
- **Atmosphere:** Coal smoke, steam plumes, machine oil smell. The air is warmer near the engine house.
- **Particle density:** 0.8 — steam clouds, coal smoke, iron filings.
- **Water color:** Slightly murky near the pier (industrial runoff). The player may need the pumping station to manage this.

**Era 5: Light and Signal**
- **Sky:** Evening into night — the critical transition. The lighthouse beam sweeps the sky. Stars are present but the beam dominates. Aurora-like effect from signal towers (if built).
- **Ambient sound:** The mechanical hum is quieter now (electric motors are quieter than steam). Add the soft buzz of lamps, the occasional crackle of the telegraph. At night, the rotating beam of the lighthouse has a faint mechanical sweep sound.
- **Vegetation:** Returning — the player has stopped burning everything. Managed woodland. Gardens mature.
- **Lighting:** Electric lamps along paths and in windows. The lighthouse. Signal beacons. The island is visible from far away at night. Warm light in windows, white light from the tower, green from the signal towers.
- **Atmosphere:** Clean air. The coal smoke is gone (electric heating). Ozone faint near the generator. The air smells of the sea again, for the first time since Era 3.
- **Particle density:** 0.5 — fewer particles than Era 4, but more deliberate: lamp-lit dust motes, signal-tower light scatter, the beam's visible cone in mist.
- **Water color:** Clear again. Clean. The reflection of the lighthouse on the water at night is the game's signature image.

### 4.2 The Build Landscape

The most visible progression is the build landscape itself — the accumulated evidence of five eras of construction:

| Era | What the Landscape Looks Like |
|---|---|
| 1 | A camp. One or two rough shelters, a fire pit, drying racks. Materials stacked on the sand. Everything temporary. |
| 2 | A homestead. Timber-frame workshop, storehouse, pier. Fenced garden. The beginning of a permanent settlement. The old Era 1 camp may still stand as a "memory structure." |
| 3 | A village. Stone tower(s), stone walls, bridge, kiln, forge. The silhouette is dominated by masonry. Trees are managed, not wild. Paths are paved in slate or flagstone. |
| 4 | A shipyard. Industrial structures, crane gantry, boiler stack, pipe runs. Steel and iron are visible everywhere. The workshop is the largest building. The pier is extended for industrial loading. |
| 5 | A coast guard station. The lighthouse dominates. Electric lights line the paths. Telegraph/antenna wires cross between buildings. The island looks inhabited, maintained, and *connected*. From offshore, it looks like a small port. |

### 4.3 World Change Implementation

```lua
-- Extend EraSystem ERAS table with building-era worldChanges:

local BUILDING_WORLD_CHANGES = {
    [1] = {
        skyPreset = "dawn_coastal",
        ambientSound = "wind_and_waves",
        particleDensity = 0.3,
        vegetationState = "sparse_wild",
        waterTint = Color3.fromRGB(40, 60, 80),  -- deep blue-grey
        nightLighting = "fire_only",
    },
    [2] = {
        skyPreset = "morning_clear",
        ambientSound = "wind_and_waves_plus_hammering",
        particleDensity = 0.4,
        vegetationState = "planted_managed",
        waterTint = Color3.fromRGB(40, 60, 80),
        nightLighting = "oil_lamps",
    },
    [3] = {
        skyPreset = "midday_solid",
        ambientSound = "quarry_and_forge",
        particleDensity = 0.6,
        vegetationState = "mature_managed",
        waterTint = Color3.fromRGB(45, 70, 70),  -- slightly green near shore
        nightLighting = "oil_lamps_and_forge_glow",
    },
    [4] = {
        skyPreset = "afternoon_industrial",
        ambientSound = "mechanical_hum_steam",
        particleDensity = 0.8,
        vegetationState = "industrial_clearance",
        waterTint = Color3.fromRGB(50, 60, 55),  -- murky near pier
        nightLighting = "electric_arc_workshop",
    },
    [5] = {
        skyPreset = "evening_lighthouse",
        ambientSound = "electric_buzz_and_beam",
        particleDensity = 0.5,
        vegetationState = "restored_managed",
        waterTint = Color3.fromRGB(35, 65, 85),  -- clear, clean
        nightLighting = "full_electric_plus_lighthouse",
        specialEffect = "lighthouse_beam",
    },
}

-- Applied via existing EraSystem.getWorldChanges() + AtmosphereRig module
```

---

## 5. IMPLEMENTATION NOTES FOR LUA ENGINEERS

### 5.1 Integration with Existing EraSystem

The building era system layers **on top of** the existing tech era system. Do not replace the tech eras — extend them. The mapping is:

```lua
-- Derive building era from tech era (with building milestone override)
function EraSystem.getBuildingEra(playerName)
    local techEra = EraSystem.getCurrentEra(playerName)
    local buildingReady = EraSystem.checkBuildingEraAdvancement(playerName)

    -- Building era is the LOWER of:
    --   a) what the player's builds qualify them for
    --   b) what their tech era supports
    -- This prevents a player from being Era 5 builder while still in tech Era 1.
    
    if techEra == 0 then return 1 end  -- Always at least Era 1
    if techEra == 1 then
        return buildingReady and 2 or 1
    end
    if techEra == 2 then
        return buildingReady and 3 or 2
    end
    if techEra == 3 or techEra == 4 then
        return buildingReady and 4 or 3
    end
    if techEra == 5 or techEra == 6 then
        return buildingReady and 5 or 4
    end
    return 1
end
```

### 5.2 Recipe Registration

Add building-type recipes to the existing Recipes.lua registry. Each build type becomes a recipe with `category = "building"`:

```lua
r{
    id = "lean_to",
    era = 0,  -- tech era (existing system)
    buildingEra = 1,  -- NEW FIELD: which building era this belongs to
    name = "Lean-To Shelter",
    category = "building",
    ingredients = { driftwood = 3, canvas_scrap = 2 },
    output = { type = "structure", buildType = "lean_to" },
    description = "A one-sided shelter. Keeps rain off. Barely.",
    footprint = { width = 3, depth = 2 },  -- in lattice cells
    placementType = "surface",  -- sits on ground, no foundation needed
    agentTip = "Lucineer says: everybody's first build. It won't last. That's the point.",
}
```

### 5.3 Material Registration

Add raw materials to the CraftingSystem inventory as gatherable/harvestable items:

```lua
-- Materials are gathered, not crafted. Add to CraftingSystem as inventory items.
-- Harvesting nodes exist in the world and produce materials on interaction.

local HARVEST_NODES = {
    tideline = {
        produces = { "driftwood", "beach_stone", "shell", "kelp_dried", "bone" },
        respawnHours = 6,  -- tide cycle
        minYield = 1,
        maxYield = 3,
    },
    wreckage = {
        produces = { "salvage_plank", "canvas_scrap", "nail_wrought" },
        respawnHours = 24,
        minYield = 2,
        maxYield = 5,
        depleted = true,  -- wrecks don't respawn — finite resource
    },
    cliff_face = {
        produces = { "limestone", "sandstone", "slate" },
        requires = { tool = "chisel" },
        respawnHours = 0,  -- infinite, but slow per-node
    },
    -- etc.
}
```

### 5.4 Build Placement

Building types use the existing Eisenstein A₂ lattice (per the Grand Plan, Layer 4):

- Era 1 builds: 1–2 lattice cells. No foundation. `placementType = "surface"`.
- Era 2 builds: 2–4 lattice cells. Optional sill beam foundation. `placementType = "surface_or_foundation"`.
- Era 3 builds: 4–9 lattice cells. Requires `stone_foundation` first. `placementType = "foundation_required"`.
- Era 4 builds: 4–12 lattice cells. Requires `stone_foundation` or `concrete_struct`. `placementType = "foundation_required"`.
- Era 5 builds: Variable. The lighthouse is a special placement — it occupies the existing stone tower location and adds the lens/filament/electrical components.

### 5.5 The Lighthouse — Special Case

The lighthouse restoration is a multi-era build. The tower itself is an Era 3 build (`stone_tower`). The lens and light are Era 5 additions. The lighthouse is not a single recipe — it is a **composite structure** that accumulates across eras:

```lua
-- Lighthouse is built in stages across eras:
-- Era 3: stone_tower (the shell)
-- Era 4: iron framework for lens housing (inside the tower top)
-- Era 5: lens_fresnel + filament + bulb_glass + copper_wire = lighthouse_restored

-- When all components are present in the tower top, trigger the restoration event.
function checkLighthouseComplete(buildPosition)
    local hasTower = findBuildNear(buildPosition, "stone_tower", 5)
    local hasLens = findBuildNear(buildPosition, "lens_fresnel", 5)
    local hasLight = findBuildNear(buildPosition, "filament", 5)
    local hasWire = findBuildNear(buildPosition, "copper_wire", 5)
    
    if hasTower and hasLens and hasLight and hasWire then
        triggerLighthouseRestoration()
    end
end
```

### 5.6 Material Degradation (Optional — Phase 2)

Some materials degrade over time, adding a maintenance layer:

| Material | Degradation | Rate | Mitigation |
|---|---|---|---|
| `driftwood` | Rot | 7 days exposed | Keep dry, paint with pitch |
| `canvas_scrap` | UV decay | 14 days exposed | Store indoors |
| `rawhide` | Breakdown if wet | 3 days wet | Cure fully before use |
| `timber` | Rot (untreated) | 30 days exposed | Paint with tar_boiled |
| `iron_bar` | Rust | 7 days if wet | Paint, oil, or embed |
| `steel_beam` | Rust | 14 days if wet | Paint or copper-sheet clad |
| `copper_sheet` | Patina (cosmetic only) | 30 days | None needed — patina protects |

Stone, brick, mortar, concrete, glass, and ceramics do not degrade within gameplay timescales.

---

## 6. QUICK REFERENCE — ERA SUMMARY TABLE

| | Era 1 | Era 2 | Era 3 | Era 4 | Era 5 |
|---|---|---|---|---|---|
| **Name** | Driftwood & Salvage | Frame & Plank | Stone & Mortar | Metal & Machine | Light & Signal |
| **Lucineer's Name** | "salvage years" | "honest years" | "permanent years" | "iron years" | "year the light came back" |
| **New Materials** | 11 | +13 | +13 | +13 | +11 |
| **Cumulative Materials** | 11 | 24 | 37 | 50 | 61 |
| **Build Types** | 7 | 12 | 14 | 14 | 14 |
| **Required Builds** | fire_pit, workbench_scrap | post_and_beam, framed_workshop | stone_foundation, lime_kiln | workshop_industrial | — (final era) |
| **Min Distinct Builds** | 4 | 5 | 6 (+ height) | 5 (+ power chain) | — |
| **Sky** | Dawn coastal | Morning clear | Midday solid | Afternoon industrial | Evening lighthouse |
| **Tempo (BPM)** | 40 (Largo) | 70 (Andante) | 85 (Moderato) | 110 (Allegro) | 55 (Adagio) |
| **Night Light** | Fire only | Oil lamps | Forge glow | Electric arc | Lighthouse + grid |
| **Emotional Beat** | Survival | Craftsmanship | Permanence | Industry | Connection |

---

*End of Era Building System. 5 eras, 61 materials, 61 build types, 5 Lucineer dialogues. Every value in this document is designed to be directly implementable in the existing EraSystem, Recipes, and CraftingSystem Lua modules.*
