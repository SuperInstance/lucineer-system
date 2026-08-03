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

---

## 1. THE FIVE ERAS

### Era 1: DRIFTWOOD AND SALVAGE

> *"You work with what the tide brings you. It's not much. It's enough."*

**Aesthetic:** Beachcomber vernacular. Walls made of salt-bleached planks pulled from wrecks. Roofs of layered bark, canvas scraps, and salvaged cloth. Structures are small, single-room, impermanent — a storm can take them. Everything smells of salt and tar. The visual language is *organic irregularity*: no two planks are the same width, walls lean slightly, doorways are rough-cut. Builds sit on the sand without foundations. It looks like someone's first week on an island, because it is.

**Materials Available:**

| Material ID | Name | Source |
|---|---|---|
| `driftwood` | Driftwood | Tideline, wreckage |
| `salvage_plank` | Salvaged Plank | Wrecks, debris fields |
| `rawhide` | Rawhide | Tanning small catches |
| `palm_fiber` | Palm Fiber | Palm trees (if present) |
| `kelp_dried` | Dried Kelp | Shoreline harvesting |
| `sea_rope` | Sea Rope | Palm fiber twisted |
| `beach_stone` | Beach Stone | Shoreline collecting |
| `canvas_scrap` | Canvas Scrap | Wreckage, washed-up cargo |
| `pitch` | Pitch (Tar) | Natural seeps, boiled pine |
| `shell` | Shell | Shell beds, tidal pools |
| `bone` | Bone | Beach finds, large fish |

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

**Materials Available (Era 1 materials carry forward):**

| Material ID | Name | Source | Era 1 Equivalent |
|---|---|---|---|
| `timber` | Timber (Sawn) | Felling + sawing trees | — |
| `plank` | Plank (Sawn) | Sawing timber | salvage_plank refined |
| `treenail` | Treenail | Carved hardwood pegs | — |
| `tar` | Tar (Boiled) | Pitch refined | pitch refined |
| `oakum` | Oakum | Fiber picked and tarred | palm_fiber + tar |
| `nail_wrought` | Wrought Nail | Forge (requires bellows) | — |
| `hinge_iron` | Iron Hinge | Forge | — |
| `glass_crude` | Crude Glass | Sand + fire (imperfect) | — |
| `shingle` | Wood Shingle | Split from billets | — |
| `mortise_peg` | Mortise Peg | Hardwood | — |
| `brace_timber` | Diagonal Brace | Timber, shaped | — |
| `sill_beam` | Sill Beam | Timber, squared | — |
| `canvas_new` | Canvas (Woven) | Loom (requires fiber) | canvas_scrap refined |

**Build Types:**

| Build Type | Cost | Unlocks | Description |
|---|---|---|---|
| `post_and_beam` | timber×4, treenail×6, brace_timber×2 | Structural framing | The skeleton. Vertical posts in sill beams with horizontal girts. Load-bearing. |
| `plank_wall` | plank×6, timber×2, treenail×4 | Vertical enclosure | Sawn planks fastened to frame. Weather-tight when caulked. |
| `shingled_roof` | shingle×8, timber×3, treenail×4 | Weatherproof roofing | Overlapping shingles on timber rafters. First real rain protection. |
| `framed_floor` | timber×5, plank×4, treenail×6 | Second story | Raised floor on joists. Opens verticality. |
| `caulked_seam` | oakum×2, tar×1 | Waterproofing | Sealed plank seams. Keeps the weather and the vermin out. |
| `hinged_door` | plank×4, hinge_iron×2, nail_wrought×4 | Security, privacy | A real door that latches. You can close it and it stays closed. |
| `glazed_window` | glass_crude×2, timber×2, plank×2 | Light, view | Imperfect glass in a wooden frame. Wavy, beautiful, functional. |
| `framed_workshop` | timber×12, plank×15, treenail×20, shingle×10 | Advanced crafting | Full workshop with bench, tool rack, and storage. Unlocks Era 2+ recipes. |
| `storehouse` | timber×8, plank×10, treenail×12 | Material storage | Dry, secure storage. Materials inside don't degrade. |
| `pier_jetty` | timber×10, plank×6, treenail×8 | Water access | A walkway over water. Dock boats, stage materials, fish from it. |
| `saw_pit` | timber×6, plank×4, beach_stone×4 | Plank production | A pit for two-man rip-sawing. Doubles plank output from timber. |
| `crane_post` | timber×6, sea_rope×4, brace_timber×4 | Heavy lifting | A simple wooden crane. Lifts materials to upper stories. |

**Era Gate — Advancement Requirement:**
Player must have built `post_and_beam` AND `framed_workshop`, plus at least **3 other distinct Era 2 build types**. Lucineer inspects the workshop specifically — its construction quality determines his assessment.

**Lucineer Transition Dialogue (Era 2 → Era 3):**

> *[Lucineer stands in the workshop doorway, one hand on the frame. He's been watching the player square a timber for the better part of an hour. He waits until the adze is set down.]*

> **LUCINEER:** This frame is good. I mean it — the joinery is honest, the braces are where they should be, and you pegged every mortise instead of cheating with nails. This building will stand through weather that strips paint off hulls.

> *[He steps inside, knocks a post with his knuckles. The sound is solid.]*

> **LUCINEER:** But wood is still wood. It rots. It burns. It warps when the season turns enough times. You've learned to shape it — now learn to outlast it. There's limestone in the cliff face and clay in the riverbed, and I'm going to show you what fire does to rock when you ask it properly.

> *[He picks up a lump of beach stone, turns it over.]*

> **LUCINEER:** Your great-grandfather's lighthouse stood for ninety years after he died. Wooden frame, stone skin. The frame held. The skin is what made it permanent. We're going to build something the sea can't take.

> *[He puts the stone in the player's hand.]*

> **LUCINEER:** Carry one of these to the workshop. Just one. We start with weight.

---

### Era 3: STONE AND MORTAR

> *"Permanence arrives. Walls have mass. Foundations go below the frost line. The building outlasts the builder."*

**Aesthetic:** Masonry vernacular. Dressed stone walls with lime-mortar joints, or fieldstone laid in courses. Brick appears where clay is fired. Foundations are trenched and laid with rubble and mortar. Roofs can be stone slab or tile. Structures gain real height — two and three stories, towers, thick walls that insulate against storm and cold. Arches and lintels span openings. The visual language is *deliberate weight*: buildings look grounded, immovable, permanent. Mortar lines are visible and proud. It looks like it was built to outlast you, because it was.

**Materials Available (Era 1–2 carry forward):**

| Material ID | Name | Source | Notes |
|---|---|---|---|
| `limestone` | Limestone | Quarry face, cliff cuts | Soft enough to dress, hard enough to last |
| `sandstone` | Sandstone | Cliff strata | Warm tones, carves beautifully |
| `fieldstone` | Fieldstone | Surface collecting | Irregular, laid by eye |
| `granite` | Granite | Deep quarry | Hardest stone. Premium structural material. |
| `brick_fire` | Fired Brick | Clay + kiln | Uniform, modular, structural |
| `mortar_lime` | Lime Mortar | Limestone + sand + water | The binder. Without it, stone is just a pile. |
| `concrete_crude` | Crude Concrete | Aggregate + lime + water | Poured, cast, structural |
| `clay_raw` | Raw Clay | Riverbed, deposits | For brick, tile, and mortar |
| `sand_fine` | Fine Sand | River, beach (sieved) | Mortar and concrete aggregate |
| `tile_roof` | Roof Tile | Fired clay | Modular roofing. Better than shingle. |
| `slate` | Slate | Cliff strata (deep) | Splits into flat sheets. Roofing, flooring, blackboards. |
| `lead_sheet` | Lead Sheet | Smelted galena | Flashing, waterproofing, pipes. Heavy, toxic, useful. |
| `rebar_crude` | Crude Iron Rod | Forge, drawn iron | Reinforcement for concrete. First composite material. |

**Build Types:**

| Build Type | Cost | Unlocks | Description |
|---|---|---|---|
| `stone_foundation` | fieldstone×8, mortar_lime×4, sand_fine×4 | All Era 3 structures require this | Trenched and laid rubble foundation. Everything permanent sits on this. |
| `stone_wall` | limestone×10 (or fieldstone×12), mortar_lime×6 | Permanent enclosure | Dressed stone and mortar. Load-bearing, weatherproof, fireproof. |
| `brick_wall` | brick_fire×12, mortar_lime×4 | Modular enclosure | Fired brick in mortar. Faster than stone, very strong. |
| `arch_stone` | limestone×8, mortar_lime×3, timber×4 (formwork) | Wide spans | A stone arch. Spans openings no timber beam can match. |
| `stone_tower` | limestone×30, mortar_lime×15, timber×10, rebar_crude×4 | Height, signal platform | A circular or square tower. 3+ stories. The landmark structure. |
| `vaulted_ceiling` | brick_fire×15, mortar_lime×6, timber×8 (formwork) | Masonry roofing | Brick vault overhead. Permanent, fireproof, beautiful. |
| `tiled_roof` | tile_roof×12, timber×4, mortar_lime×2 | Premium roofing | Overlapping fired tiles on timber rafters. Lasts a century. |
| `slate_floor` | slate×6, mortar_lime×2 | Interior flooring | Flat slate tiles in mortar. Clean, durable, waterproof. |
| `stone_chimney` | brick_fire×8, mortar_lime×3, stone×4 | Indoor heating | Full chimney with flue. Heats without filling the room with smoke. |
| `root_cellar` | fieldstone×10, mortar_lime×4, timber×3 | Cold storage | Below-grade stone chamber. Cool year-round. Food preservation. |
| `cistern` | brick_fire×10, mortar_lime×6, lead_sheet×2 | Water storage | Lined cistern collects rainwater. Independent water supply. |
| `lime_kiln` | limestone×8, brick_fire×6, timber×10 | Mortar production | Fires limestone into quicklime. The key to all masonry. |
| `forge_hearth` | brick_fire×10, mortar_lime×4, stone×6, tar×2 | Metalworking | A proper forge. Unlocks iron and steel production. |
| `bridge_stone` | limestone×15, mortar_lime×8, timber×6 (formwork) | Spanning water | A stone arch bridge. Permanent crossing. Won't wash out. |

**Era Gate — Advancement Requirement:**
Player must have built `stone_foundation`, `stone_wall` (or `brick_wall`), `lime_kiln`, and at least **2 other distinct Era 3 build types**. Additionally, the player must have built at least one structure with a `vaulted_ceiling` or `stone_tower` — demonstrating they can work at height with masonry.

**Lucineer Transition Dialogue (Era 3 → Era 4):**

> *[Lucineer is on the catwalk of the stone tower, looking out over the bay. He heard the player coming up the spiral stairs — the echo in stone is different from wood. Wood absorbs. Stone reports. He speaks without turning.]*

> **LUCINEER:** You can hear yourself think in here. That's what stone does — it holds everything. Sound, heat, cold, and time. Your great-grandfather understood that. He built his workshop in timber and his lighthouse in stone, and the workshop burned down in 1953 and the lighthouse is still standing.

> *[He turns, leaning on the parapet.]*

> **LUCINEER:** You've learned weight. Now learn force. Stone holds still — it carries load, it endures, it waits. But what if the wall could *move*? What if the structure could *do* something — lift, pivot, pump — and do it every day, the same way, without tiring? That's not carpentry and it's not masonry. That's mechanism.

> *[He pulls a folded drawings from his coat — gears, linkages, a water-driven arm.]*

> **LUCINEER:** I've been watching the river for a year. There's enough flow to turn a wheel that turns a shaft that turns a gear that lifts a hammer that shapes the iron that reinforces the concrete that holds the wheel. You see? It's a *circuit*. Not wire — not yet — but a circuit of stone and iron and water, and it runs itself.

> *[He hands the drawings over.]*

> **LUCINEER:** Bring me iron. Not fragments — *worked* iron. We're going to build the first machine this island has seen since the old light went dark.

---

### Era 4: METAL AND MACHINE

> *"Iron becomes steel. The structure stops sitting passively and starts working. Pumps pump. Cranes lift themselves. The building is a machine with a roof."*

**Aesthetic:** Industrial maritime. Iron-frame structures with riveted plates, exposed mechanism, and functional pipe runs. Stone and brick still form the base — but now they house boilers, turbines, line shafts. Steel beams span distances timber can't. Walls incorporate iron grilles, copper sheeting, brass fittings. The visual language is *honest mechanism*: gears, belts, pipes, and valves are visible and celebrated, not hidden behind cladding. Steam and smoke are present. It looks like a shipyard workshop crossed with a Victorian pumping station, because that's what it is.

**Materials Available (Era 1–3 carry forward):**

| Material ID | Name | Source | Notes |
|---|---|---|---|
| `iron_bar` | Iron Bar (Worked) | Forge, reheated and drawn | First structural metal |
| `steel_bar` | Steel Bar | Forge + carbon process | Iron that's been taught discipline |
| `steel_plate` | Steel Plate | Rolling mill (requires power) | Sheet steel for walls, tanks, hulls |
| `steel_beam` | Steel I-Beam | Rolling mill | Long-span structural member. Replaces timber girts. |
| `rivet_iron` | Iron Rivet | Forge | The fastener of the industrial age |
| `copper_sheet` | Copper Sheet | Smelted copper, rolled | Roofing, sheathing, waterproofing. Verdigris over time. |
| `brass_fitting` | Brass Fitting | Copper + zinc, cast | Valves, connectors, decorative work |
| `pipe_iron` | Iron Pipe | Cast or drawn | Pressurized fluid transport |
| `boiler_plate` | Boiler Plate | Thick steel, riveted | Pressure vessel construction |
| `glass_sheet` | Sheet Glass | Improved furnace | Flat, clear panes. Real windows. |
| `cable_steel` | Steel Cable | Drawn wire, spun | Heavy lifting, tension structures |
| `girder_riveted` | Riveted Girder | Steel plate + rivets | Built-up structural beam |
| `concrete_reinforced` | Reinforced Concrete | Concrete + rebar + steel | The composite that built the modern world |

**Build Types:**

| Build Type | Cost | Unlocks | Description |
|---|---|---|---|
| `iron_frame` | steel_beam×6, rivet_iron×12, iron_bar×4 | Steel structural skeleton | Riveted steel frame. Replaces timber framing. Spans further, carries more. |
| `steel_wall` | steel_plate×8, rivet_iron×8, iron_bar×2 | Metal enclosure | Riveted steel plate walls. Fireproof, storm-proof. |
| `boiler_house` | boiler_plate×8, pipe_iron×4, valve×2, brick_fire×6 | Steam power | A boiler house with feedwater system. Produces pressurized steam. |
| `engine_house` | steel_beam×8, steel_plate×6, rivet_iron×10, pipe_iron×4 | Mechanical power | Houses a steam engine or turbine. Drives line shafts. |
| `line_shaft_system` | iron_bar×6, steel_bar×4, bearing×4, belt_drive×2 | Power distribution | Overhead shafts carrying rotational power to workstations. |
| `powered_hammer` | steel_beam×4, iron_bar×6, cable_steel×2, gear×4 | Automated forging | A steam-powered trip hammer. Forges what muscle cannot. |
| `powered_crane` | steel_beam×8, cable_steel×4, gear×6, pipe_iron×2 | Heavy lift capability | A powered overhead crane. Lifts entire frames into place. |
| `pumping_station` | brick_fire×10, pipe_iron×6, valve×3, boiler_plate×4 | Water management | Pumps water from mines, cisterns, low ground. Civil engineering. |
| `copper_roof` | copper_sheet×8, timber×3 | Premium roofing | Copper sheet roofing. Starts bright, goes green, lasts centuries. |
| `glass_curtain` | glass_sheet×8, steel_beam×4, iron_bar×4 | Glass wall system | A wall of glass in a steel frame. Light enters. The future. |
| `workshop_industrial` | steel_beam×15, steel_plate×10, rivet_iron×20, pipe_iron×6, brick_fire×8 | Advanced crafting | Full industrial workshop. Line-shaft powered. Unlocks Era 4+ recipes. |
| `concrete_struct` | concrete_reinforced×8, rebar_crude×6 | Poured structures | Reinforced concrete walls, floors, platforms. Cast in forms. |
| `gantry_rail` | steel_beam×4, iron_bar×4, rivet_iron×6 | Crane mobility | Overhead rail system. Crane moves along it. Covers the whole yard. |
| `wind_turbine_mech` | steel_plate×6, steel_beam×4, gear×4, cable_steel×2 | Wind power | A mechanical wind turbine. Drives shafts when the steam is off. |

**Era Gate — Advancement Requirement:**
Player must have built `boiler_house` or `engine_house` AND `workshop_industrial`, plus at least **3 other distinct Era 4 build types**. The player must also demonstrate a working **power transmission chain** — a powered machine connected via line shaft or belt to a power source. Lucineer tests this by asking the player to run the workshop from a single prime mover.

**Lucineer Transition Dialogue (Era 4 → Era 5):**

> *[The industrial workshop hums with shaft power. Lucineer is standing at the far end, where the line shaft terminates in a dead pulley. He's been staring at it. The pulley spins, connected to nothing, uselessly turning. He puts his hand on it — gently, feeling the rotation.]*

> **LUCINEER:** Everything in this room moves because of that shaft. One wheel, and the whole building works. One fire, and the whole island moves. We took the river and the wind and the coal and we made them *turn* — and that was the hardest thing humans ever learned to do.

> *[He stops the pulley with his palm. The shaft keeps spinning elsewhere — the workshop doesn't care about one stopped wheel.]*

> **LUCINEER:** But it's dark in here. Not the light — I mean the mechanism. The shaft turns, and we can see it turn. The belt moves, and we can watch it move. But the *reason* it moves — the decision to send power here instead of there — that's still made by a person pulling