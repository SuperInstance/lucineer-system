#!/usr/bin/env python3
"""
Slackwater Hub Generator
========================
Generates the ENTIRE Slackwater Hub as a JSON array of build commands
for the Lucineer CommandExecutor.

Output: hub_build.json

The hub is the first thing players see. Make it dramatic.
"""
import json
import os

commands = []


# ───────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ───────────────────────────────────────────────────────────────────────────────

def part(name, shape, size, pos, material, color, transparency=0.0,
         reflectance=0.0, rotation=(0, 0, 0), anchored=True, can_collide=True):
    commands.append({
        "type": "createPart",
        "params": {
            "name": name,
            "shape": shape,
            "size": {"x": size[0], "y": size[1], "z": size[2]},
            "position": {"x": pos[0], "y": pos[1], "z": pos[2]},
            "rotation": {"x": rotation[0], "y": rotation[1], "z": rotation[2]},
            "material": material,
            "color": {"r": color[0], "g": color[1], "b": color[2]},
            "anchored": anchored,
            "transparency": transparency,
            "reflectance": reflectance,
            "canCollide": can_collide,
        }
    })


def light(parent, light_type, brightness, range_, color, shadows=True, angle=None):
    params = {
        "parent": parent,
        "lightType": light_type,
        "brightness": brightness,
        "range": range_,
        "color": {"r": color[0], "g": color[1], "b": color[2]},
        "shadows": shadows,
    }
    if angle is not None:
        params["angle"] = angle
    commands.append({"type": "addLight", "params": params})


def particle(parent, texture, rate, lifetime, speed, color, size,
             transparency=0.3, velocity=(0, 1, 0)):
    commands.append({
        "type": "addParticle",
        "params": {
            "parent": parent,
            "texture": texture,
            "rate": rate,
            "lifetime": {"min": lifetime[0], "max": lifetime[1]},
            "speed": {"min": speed[0], "max": speed[1]},
            "color": {"r": color[0], "g": color[1], "b": color[2]},
            "size": {"min": size[0], "max": size[1]},
            "transparency": transparency,
            "velocity": {"x": velocity[0], "y": velocity[1], "z": velocity[2]},
        }
    })


# ───────────────────────────────────────────────────────────────────────────────
# COORDINATE SYSTEM
# ───────────────────────────────────────────────────────────────────────────────
# Origin (0, 0, 0) = center of island at water level
# +X = East (landward/north side)   -X = West
# +Z = South (seaward/dock side)     -Z = North
# +Y = Up
#
# Layout:
#   Lighthouse:  North end of rock spine (negative Z)
#   Cannery:     Center-south, on pilings over water
#   Dock/Float:  South of cannery, extending over water
#   Boardwalk:   Connects dock → cannery → lighthouse
#   Beach:       South shore, around the tideline
#   Fog:         Ring around the island edges

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: THE ISLAND — terrain + base
# ═══════════════════════════════════════════════════════════════════════════════

# --- Black rock base (400x400, underwater mass) ---
part("IslandRockBase", "Block", (400, 30, 400), (0, -15, 0), "Basalt", (28, 28, 32))
part("IslandRockSub2", "Block", (380, 20, 380), (0, -5, 0), "Slate", (35, 35, 38))

# --- Grass/dirt top layer ---
part("IslandTopLayer", "Block", (360, 6, 360), (0, 8, 0), "Grass", (55, 75, 40))
part("IslandSoilLayer", "Block", (350, 4, 350), (0, 5, 0), "Ground", (85, 65, 45))

# --- Rock spine running north-south (elevated ridge) ---
# The spine is the high ground — lighthouse sits atop it
part("SpineBase", "Block", (60, 18, 280), (0, 14, -40), "Basalt", (42, 40, 45))
part("SpineTop", "Block", (45, 10, 250), (0, 23, -40), "Slate", (55, 52, 55))
part("SpineRidge", "Block", (25, 5, 220), (0, 28, -40), "Cobblestone", (70, 68, 70))

# --- Earthen ramps / transitions from beach level to spine ---
part("SpineRampS", "Wedge", (40, 10, 50), (0, 14, 95), "Ground", (75, 60, 42),
     rotation=(0, 0, 0))
part("SpineRampN", "Wedge", (40, 10, 50), (0, 14, -135), "Ground", (75, 60, 42),
     rotation=(0, 180, 0))

# --- Gravel patches (south shore area, tideline) ---
part("BeachGravel", "Block", (200, 1.5, 80), (0, 10.5, 120), "Sand", (140, 130, 105))
part("BeachGravelDark", "Block", (160, 1, 60), (0, 11, 130), "Ground", (110, 95, 75))
part("BeachKelpLine", "Block", (140, 0.5, 8), (0, 11.3, 155), "Grass", (60, 80, 35))

# --- A few scraggly spruce trees on the spine ---
for i, (dx, dz) in enumerate([(-12, -80), (10, -50), (-8, -110), (15, -20), (-15, -140)]):
    part(f"SpruceTrunk{i}", "Cylinder", (2, 18, 2), (dx, 38, dz), "Wood", (55, 38, 22))
    part(f"SpruceCrown{i}", "Cone", (10, 20, 10), (dx, 50, dz), "LeafyGrass", (35, 70, 38))
    part(f"SpruceUpper{i}", "Cone", (6, 14, 6), (dx, 58, dz), "LeafyGrass", (40, 80, 42))


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: THE CANNERY — Standard & Salvage Cannery No. 9
# 60x30 studs, on pilings over the water on the south side
# ═══════════════════════════════════════════════════════════════════════════════

# Cantery center position
CX, CY, CZ = 0, 12, 40  # Centered at X=0, on stilts at Y=12, south side Z=40

# --- Pilings (creosote-soaked wood columns) ---
piling_positions = [
    (-28, 55), (-18, 55), (-8, 55), (8, 55), (18, 55), (28, 55),
    (-28, 25), (-18, 25), (-8, 25), (8, 25), (18, 25), (28, 25),
]
for i, (px, pz) in enumerate(piling_positions):
    part(f"CanneryPiling{i}", "Cylinder", (2.5, 24, 2.5), (px, 0, pz),
         "Wood", (35, 25, 15))

# Cross-bracing between pilings
for i, (px, pz) in enumerate([(-28, 55), (-8, 55), (12, 55), (28, 55),
                               (-28, 25), (-8, 25), (12, 25), (28, 25)]):
    part(f"CanneryBrace{i}", "Block", (1, 3, 30), (px, 5, 40),
         "Wood", (40, 28, 18))

# --- Cannery floor (heavy plank on pilings) ---
part("CanneryFloor", "Block", (60, 2, 30), (CX, CY, CZ), "WoodPlanks", (65, 45, 28))
part("CanneryFloorUnder", "Block", (58, 1, 28), (CX, CY - 1.5, CZ), "Wood", (40, 28, 16))

# --- Cannery walls: corrugated metal, red-brown ---
# Long walls (north/back wall and south/front wall)
part("CanneryWallN", "Block", (60, 14, 1), (CX, CY + 7, CZ - 15), "CorrodedMetal",
     (120, 55, 30))
part("CanneryWallS", "Block", (60, 14, 1), (CX, CY + 7, CZ + 15), "CorrodedMetal",
     (115, 50, 28))

# End walls (east and west)
part("CanneryWallE", "Block", (1, 14, 30), (CX + 30, CY + 7, CZ), "CorrodedMetal",
     (125, 58, 32))
part("CanneryWallW", "Block", (1, 14, 30), (CX - 30, CY + 7, CZ), "CorrodedMetal",
     (118, 52, 30))

# --- Roof: corrugated metal, slightly pitched ---
part("CanneryRoof", "Block", (62, 1.5, 32), (CX, CY + 14.5, CZ), "CorrodedMetal",
     (100, 42, 22))
part("CanneryRoofRidge", "Block", (62, 1, 4), (CX, CY + 15.5, CZ), "Metal",
     (70, 35, 18))

# Roof patch (salvaged bulkhead steel look)
part("CanneryRoofPatch1", "Block", (12, 0.5, 8), (CX - 10, CY + 15.2, CZ - 5),
     "DiamondPlate", (80, 75, 68))
part("CanneryRoofPatch2", "Block", (8, 0.5, 6), (CX + 15, CY + 15.2, CZ + 3),
     "Metal", (85, 80, 72))

# --- Windows along the north wall (glowing forge interior) ---
window_positions_n = [(-22, CZ - 15), (-12, CZ - 15), (12, CZ - 15), (22, CZ - 15)]
for i, (wx, wz) in enumerate(window_positions_n):
    # Window frame
    part(f"CanneryWinFrameN{i}", "Block", (6, 6, 0.5), (CX + wx, CY + 7, wz),
         "Wood", (50, 35, 20))
    # Glass
    part(f"CanneryWinGlassN{i}", "Block", (5, 5, 0.3), (CX + wx, CY + 7, wz),
         "Glass", (200, 180, 120), transparency=0.45)
    # Forge glow behind window
    part(f"CanneryWinGlowN{i}", "Block", (4.5, 4.5, 0.2), (CX + wx, CY + 7, wz + 0.3),
         "Neon", (255, 100, 30), transparency=0.15)
    light(f"CanneryWinGlowN{i}", "PointLight", 3, 20, (255, 130, 50), shadows=False)

# Windows on south wall (overlooking the dock)
window_positions_s = [(-18, CZ + 15), (18, CZ + 15)]
for i, (wx, wz) in enumerate(window_positions_s):
    part(f"CanneryWinFrameS{i}", "Block", (6, 5, 0.5), (CX + wx, CY + 8, wz),
         "Wood", (50, 35, 20))
    part(f"CanneryWinGlassS{i}", "Block", (5, 4, 0.3), (CX + wx, CY + 8, wz),
         "Glass", (200, 180, 120), transparency=0.5)

# --- Large seaward doors (garage-style, open to the float) ---
# Door frame
part("CanneryDoorFrameL", "Block", (1, 16, 1), (CX - 12, CY + 8, CZ + 15), "Wood",
     (60, 42, 25))
part("CanneryDoorFrameR", "Block", (1, 16, 1), (CX + 12, CY + 8, CZ + 15), "Wood",
     (60, 42, 25))
part("CanneryDoorHeader", "Block", (26, 2, 1), (CX, CY + 16, CZ + 15), "Wood",
     (55, 38, 22))
# Sliding door panels (half-open)
part("CanneryDoorL", "Block", (12, 14, 0.8), (CX - 18, CY + 7, CZ + 15),
     "CorrodedMetal", (110, 48, 26))
part("CanneryDoorR", "Block", (12, 14, 0.8), (CX + 18, CY + 7, CZ + 15),
     "CorrodedMetal", (108, 46, 25))

# --- Smokestacks (two chimneys with particle smoke) ---
part("CanneryStack1", "Cylinder", (3, 16, 3), (CX - 8, CY + 22, CZ - 8),
     "CorrodedMetal", (90, 40, 20))
part("CanneryStack1Cap", "Cylinder", (3.5, 1, 3.5), (CX - 8, CY + 30.5, CZ - 8),
     "Metal", (60, 30, 15))

part("CanneryStack2", "Cylinder", (2.5, 14, 2.5), (CX + 10, CY + 22, CZ - 6),
     "CorrodedMetal", (95, 42, 22))
part("CanneryStack2Cap", "Cylinder", (3, 1, 3), (CX + 10, CY + 29.5, CZ - 6),
     "Metal", (55, 28, 14))

# Smoke particles from both stacks
particle("CanneryStack1Cap", "rbxassetid://241876428", 14, (3, 6), (1, 2.5),
         (160, 160, 165), (2, 4), transparency=0.2, velocity=(0.5, 2.5, 0.3))
particle("CanneryStack2Cap", "rbxassetid://241876428", 10, (2, 5), (1, 2),
         (155, 155, 160), (1.5, 3.5), transparency=0.25, velocity=(0.4, 2, 0.2))

# --- Covered conveyor walkway (connects cannery to forge area interior) ---
part("ConveyorRoof", "Block", (8, 1, 20), (CX, CY + 13, CZ - 25), "CorrodedMetal",
     (105, 48, 26))
part("ConveyorWallL", "Block", (0.5, 10, 20), (CX - 4, CY + 7, CZ - 25), "Wood",
     (50, 35, 20))
part("ConveyorWallR", "Block", (0.5, 10, 20), (CX + 4, CY + 7, CZ - 25), "Wood",
     (48, 33, 18))
# Roller conveyor visible inside
for i in range(5):
    z = CZ - 33 + i * 4
    part(f"ConveyorRoller{i}", "Cylinder", (3, 0.8, 3), (CX, CY + 2.5, z),
         "Metal", (70, 65, 60), rotation=(0, 0, 90))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: THE FORGE — inside cannery
# Visible through open doors: glowing orange interior, anvil, forge, quench
# ═══════════════════════════════════════════════════════════════════════════════

# Forge hearth (glowing coal bed)
part("ForgeHearth", "Block", (8, 3, 5), (CX - 5, CY + 1.5, CZ - 8), "Basalt",
     (30, 25, 22))
part("ForgeCoalBed", "Block", (6, 0.8, 3.5), (CX - 5, CY + 3, CZ - 8), "Neon",
     (255, 60, 15), transparency=0.1)
part("ForgeCoalOuter", "Block", (6.5, 1, 4), (CX - 5, CY + 2.5, CZ - 8), "Neon",
     (120, 30, 10))
light("ForgeCoalBed", "PointLight", 12, 50, (255, 80, 30), shadows=True)
light("ForgeCoalBed", "PointLight", 8, 25, (255, 120, 40), shadows=False)

# Chimney above forge (connects to smokestack interior)
part("ForgeHood", "Cone", (5, 6, 5), (CX - 5, CY + 6, CZ - 8), "Metal",
     (50, 30, 18), rotation=(180, 0, 0))

# Bellows (decorative leather/wood)
part("ForgeBellows", "Block", (3, 4, 1.5), (CX - 5, CY + 5, CZ - 10.5), "Wood",
     (70, 45, 25))
part("ForgeBellowsPipe", "Cylinder", (0.5, 3, 0.5), (CX - 5, CY + 4, CZ - 9.5),
     "Metal", (60, 55, 50), rotation=(90, 0, 0))

# Anvil (Lucineer's station, center-aisle)
part("AnvilBase", "Block", (2.5, 3.5, 2.5), (CX + 3, CY + 2, CZ - 5), "Wood",
     (55, 38, 22))
part("AnvilWaist", "Block", (3, 1, 2), (CX + 3, CY + 4.5, CZ - 5), "Metal",
     (65, 60, 55))
part("AnvilFace", "Block", (4, 1.2, 2.5), (CX + 3, CY + 5.5, CZ - 5), "Metal",
     (75, 70, 65))
part("AnvilHorn", "Wedge", (1.5, 1.2, 2.5), (CX + 5, CY + 5.5, CZ - 5), "Metal",
     (70, 65, 60), rotation=(0, 90, 0))
part("AnvilHardy", "Cylinder", (0.3, 1.5, 0.3), (CX + 1.5, CY + 6.5, CZ - 5),
     "Metal", (50, 45, 40))

# Quench tank (oil barrel cut in half)
part("QuenchTank", "Cylinder", (3, 3, 3), (CX + 8, CY + 1.5, CZ - 3), "Metal",
     (45, 50, 55))
part("QuenchLiquid", "Cylinder", (2.7, 0.5, 2.7), (CX + 8, CY + 2.8, CZ - 3),
     "Glass", (60, 50, 30), transparency=0.6)

# Retort ovens along the east wall (rendering scrap)
for i in range(3):
    dx = CX + 25
    dz = CZ - 8 + i * 8
    part(f"RetortOven{i}", "Block", (4, 6, 5), (dx, CY + 3, dz), "Metal",
         (55, 50, 45))
    part(f"RetortDoor{i}", "Block", (3, 4, 0.5), (dx - 1.8, CY + 3, dz), "CorrodedMetal",
         (80, 40, 20))
    part(f"RetortGlow{i}", "Block", (2.5, 3, 0.3), (dx - 2.1, CY + 3, dz), "Neon",
         (255, 80, 20), transparency=0.2)
    light(f"RetortGlow{i}", "PointLight", 2, 12, (255, 70, 25), shadows=False)

# Warm fill lighting throughout forge hall
light("ForgeCoalBed", "PointLight", 6, 60, (255, 140, 60), shadows=False)
part("ForgeCeilingGlow", "Block", (50, 0.3, 20), (CX, CY + 13.5, CZ - 2), "Neon",
     (100, 40, 15), transparency=0.5)
light("ForgeCeilingGlow", "PointLight", 5, 40, (255, 100, 40), shadows=False)

# Workbench along north wall
part("ForgeBench", "Block", (12, 1.5, 3), (CX - 8, CY + 2, CZ - 13), "WoodPlanks",
     (80, 55, 32))
part("ForgeBenchLeg1", "Block", (1, 2, 2.5), (CX - 13, CY + 1, CZ - 13), "Wood",
     (55, 38, 22))
part("ForgeBenchLeg2", "Block", (1, 2, 2.5), (CX - 3, CY + 1, CZ - 13), "Wood",
     (55, 38, 22))

# Hammer on the anvil
part("ForgeHammerHead", "Block", (1.5, 1, 0.8), (CX + 3, CY + 6.3, CZ - 4), "Metal",
     (60, 55, 50))
part("ForgeHammerHandle", "Cylinder", (0.2, 2.5, 0.2), (CX + 3.3, CY + 7.3, CZ - 4),
     "Wood", (70, 45, 25), rotation=(0, 0, 75))

# Tongs leaning on bench
part("ForgeTongs", "Cylinder", (0.15, 5, 0.15), (CX - 5, CY + 4.5, CZ - 13),
     "Metal", (60, 55, 50), rotation=(80, 0, 30))

# Ember/spark particles from the forge
particle("ForgeCoalBed", "rbxassetid://243660364", 16, (0.4, 1.5), (1.5, 4),
         (255, 100, 30), (0.2, 0.8), transparency=0.1, velocity=(0.3, 2.5, 0.3))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: THE FLOAT / DOCK — waterfront
# 40-stud wooden dock extending south, with the Capitaine moored
# ═══════════════════════════════════════════════════════════════════════════════

# --- Dock deck ---
DOCK_Z_START = CZ + 16  # Just past the cannery south wall
DOCK_Z_END = DOCK_Z_START + 40

part("DockDeck", "Block", (16, 1, 40), (0, CY - 0.5, DOCK_Z_START + 20), "WoodPlanks",
     (85, 65, 40))
part("DockCrossBeam1", "Block", (17, 0.8, 1.5), (0, CY - 1.5, DOCK_Z_START + 10),
     "Wood", (65, 45, 25))
part("DockCrossBeam2", "Block", (17, 0.8, 1.5), (0, CY - 1.5, DOCK_Z_START + 30),
     "Wood", (65, 45, 25))

# Dock planks (individual varied-color planks for the silvered look)
plank_colors = [
    (130, 115, 88), (120, 108, 82), (140, 125, 95), (115, 105, 80),
    (125, 112, 85), (135, 120, 90), (110, 100, 75), (128, 115, 87),
    (118, 106, 80), (132, 118, 89),
]
for i in range(10):
    px = -7 + i * 1.5
    part(f"DockPlank{i}", "Block", (1.2, 0.3, 38), (px, CY + 0.2, DOCK_Z_START + 19),
         "WoodPlanks", plank_colors[i])

# --- Pylons every 8 studs ---
for i, pz in enumerate(range(int(DOCK_Z_START) + 4, int(DOCK_Z_END), 8)):
    part(f"DockPylon{i}L", "Cylinder", (1.2, 14, 1.2), (-7.5, CY - 7, pz),
         "Wood", (35, 25, 15))
    part(f"DockPylon{i}R", "Cylinder", (1.2, 14, 1.2), (7.5, CY - 7, pz),
         "Wood", (35, 25, 15))

# --- Dock handrails (mixed materials: pipe on water side, ship's rail on land side) ---
part("DockRailWater", "Block", (0.3, 3, 40), (8, CY + 1.2, DOCK_Z_START + 20), "Metal",
     (60, 58, 55))
part("DockRailWaterTop", "Cylinder", (0.4, 40, 0.4), (8, CY + 2.5, DOCK_Z_START + 20),
     "Metal", (70, 68, 62), rotation=(90, 0, 0))

# Ship's rail on land side (wooden, with rope)
part("DockRailLand", "Block", (0.3, 2.5, 40), (-8, CY + 1, DOCK_Z_START + 20),
     "WoodPlanks", (80, 55, 32))
part("DockRailLandTop", "Cylinder", (0.5, 40, 0.5), (-8, CY + 2.2, DOCK_Z_START + 20),
     "Wood", (75, 50, 28), rotation=(90, 0, 0))

# Roller-coaster track rail section (the signature detail!)
part("DockRailCoaster", "Cylinder", (0.3, 12, 0.3), (8, CY + 1.5, DOCK_Z_START + 30),
     "Metal", (75, 72, 68), rotation=(90, 0, 0))

# --- Cleats and mooring posts ---
for i, (dx, dz) in enumerate([(-5, DOCK_Z_START + 5), (5, DOCK_Z_START + 5),
                               (-5, DOCK_Z_START + 35), (5, DOCK_Z_START + 35)]):
    part(f"DockCleat{i}", "Block", (2, 1, 0.8), (dx, CY + 0.8, dz), "Metal",
         (50, 48, 45))

# --- Mooring bollard pair (heavy, for the Capitaine) ---
part("DockBollardL", "Cylinder", (1.5, 3, 1.5), (-6, CY + 1, DOCK_Z_START + 8),
     "Wood", (55, 38, 22))
part("DockBollardR", "Cylinder", (1.5, 3, 1.5), (6, CY + 1, DOCK_Z_START + 8),
     "Wood", (55, 38, 22))

# --- Rope lines (from boat to cleats) ---
part("DockRopeL", "Cylinder", (0.2, 8, 0.2), (-5, CY + 2, DOCK_Z_START + 7),
     "Wood", (90, 75, 50), rotation=(45, 0, 30))
part("DockRopeR", "Cylinder", (0.2, 8, 0.2), (5, CY + 2, DOCK_Z_START + 7),
     "Wood", (90, 75, 50), rotation=(45, 0, -30))

# --- Sodium dock lamps ---
for i, pz in enumerate([DOCK_Z_START + 5, DOCK_Z_START + 20, DOCK_Z_START + 35]):
    part(f"DockLampPost{i}", "Cylinder", (0.4, 8, 0.4), (7.5, CY + 4.5, pz),
         "Metal", (45, 42, 38))
    part(f"DockLampHead{i}", "Ball", (1.2, 1.2, 1.2), (7.5, CY + 9, pz),
         "Neon", (255, 200, 100))
    light(f"DockLampHead{i}", "PointLight", 4, 25, (255, 200, 100), shadows=False)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4b: THE CAPITAINE — 58-foot tender
# Moored at the dock
# ═══════════════════════════════════════════════════════════════════════════════

BX = 0  # Boat centered on dock
BZ = DOCK_Z_START + 22  # Boat position along dock
BY = CY - 1  # Boat sits slightly below dock level (in the water)

# Hull (dark, heavy displacement hull)
part("BoatHull", "Block", (14, 5, 50), (BX, BY - 1, BZ), "Wood",
     (28, 22, 15))
part("BoatHullBottom", "Wedge", (14, 3, 50), (BX, BY - 4, BZ), "Wood",
     (25, 20, 13))
part("BoatHullBow", "Wedge", (14, 5, 8), (BX, BY - 1, BZ + 25), "Wood",
     (30, 24, 16), rotation=(0, 0, 0))

# Deck
part("BoatDeck", "Block", (12, 0.5, 46), (BX, BY + 1.5, BZ), "WoodPlanks",
     (70, 50, 30))

# Wheelhouse (forward, lit from inside)
part("BoatWheelhouse", "Block", (10, 6, 8), (BX, BY + 5, BZ - 12), "WoodPlanks",
     (75, 52, 32))
part("BoatWheelhouseRoof", "Block", (11, 0.5, 9), (BX, BY + 8.5, BZ - 12),
     "Metal", (55, 50, 45))
# Wheelhouse windows (glowing — Hermes is aboard)
part("BoatWinFwd", "Block", (8, 3, 0.3), (BX, BY + 5.5, BZ - 15.8), "Glass",
     (255, 230, 150), transparency=0.4)
part("BoatWinFwdGlow", "Block", (7.5, 2.5, 0.15), (BX, BY + 5.5, BZ - 15.7), "Neon",
     (255, 180, 80), transparency=0.15)
light("BoatWinFwdGlow", "PointLight", 3, 18, (255, 180, 80), shadows=False)

part("BoatWinSideL", "Block", (0.3, 3, 6), (BX - 4.8, BY + 5.5, BZ - 12), "Glass",
     (255, 230, 150), transparency=0.4)
part("BoatWinSideR", "Block", (0.3, 3, 6), (BX + 4.8, BY + 5.5, BZ - 12), "Glass",
     (255, 230, 150), transparency=0.4)

# Mast
part("BoatMast", "Cylinder", (0.4, 16, 0.4), (BX, BY + 10, BZ - 8), "Metal",
     (50, 45, 40))
part("BoatMastCross", "Cylinder", (0.2, 6, 0.2), (BX, BY + 14, BZ - 8), "Metal",
     (50, 45, 40), rotation=(0, 0, 90))

# Antenna array on wheelhouse roof
part("BoatAntenna1", "Cylinder", (0.1, 4, 0.1), (BX - 2, BY + 11, BZ - 12),
     "Metal", (60, 55, 50))
part("BoatAntenna2", "Cylinder", (0.1, 3, 0.1), (BX + 2, BY + 11, BZ - 12),
     "Metal", (60, 55, 50))

# Crab pots stacked on deck (4 pots)
pot_positions = [
    (BX - 4, BY + 2.3, BZ + 10),
    (BX + 4, BY + 2.3, BZ + 10),
    (BX - 4, BY + 2.3, BZ + 15),
    (BX + 4, BY + 5.3, BZ + 12),  # stacked on top
]
for i, (px, py, pz) in enumerate(pot_positions):
    part(f"CrabPot{i}", "Block", (4, 3, 3), (px, py, pz), "Metal", (80, 55, 35),
         transparency=0.3)
    # Pot frame details
    part(f"CrabPotFrame{i}a", "Block", (4.2, 0.3, 0.3), (px, py + 1.3, pz - 1.5),
         "Metal", (70, 50, 30))
    part(f"CrabPotFrame{i}b", "Block", (0.3, 0.3, 3.2), (px - 2, py + 1.3, pz),
         "Metal", (70, 50, 30))
    part(f"CrabPotFrame{i}c", "Block", (0.3, 0.3, 3.2), (px + 2, py + 1.3, pz),
         "Metal", (70, 50, 30))

# Boat railing
part("BoatRailL", "Block", (0.2, 2, 30), (BX - 6, BY + 2.5, BZ + 5), "Metal",
     (55, 50, 45))
part("BoatRailR", "Block", (0.2, 2, 30), (BX + 6, BY + 2.5, BZ + 5), "Metal",
     (55, 50, 45))

# Smokestack on boat (diesel exhaust)
part("BoatStack", "Cylinder", (1, 4, 1), (BX + 3, BY + 9, BZ - 10), "Metal",
     (50, 45, 40))
particle("BoatStack", "rbxassetid://241876428", 5, (1, 3), (0.5, 1.5),
         (140, 140, 145), (0.8, 2), transparency=0.3, velocity=(0.2, 1.5, 0.1))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: THE LIGHTHOUSE — on rock spine
# 40-stud tall stone tower, striped, with rotating beam
# ═══════════════════════════════════════════════════════════════════════════════

LX, LY, LZ = 0, 30, -140  # Top of rock spine, north end

# --- Foundation pad on the rock ---
part("LightFoundation", "Block", (18, 3, 18), (LX, LY + 1.5, LZ), "Cobblestone",
     (80, 75, 70))
part("LightFoundationRock", "Block", (20, 6, 20), (LX, LY - 1, LZ), "Basalt",
     (45, 42, 45))

# --- Tower base (wide stone cylinder) ---
part("LightTowerBase", "Cylinder", (12, 6, 12), (LX, LY + 6, LZ), "Concrete",
     (100, 95, 88))

# --- Striped tower rings (alternating white and red bands) ---
# 5 bands of ~5 studs each = 25 studs of tower height
band_colors = [
    ("Concrete", (220, 215, 205)),   # White-ish
    ("Brick", (140, 55, 35)),         # Red
    ("Concrete", (215, 210, 200)),   # White
    ("Brick", (135, 52, 33)),         # Red
    ("Concrete", (210, 205, 195)),   # White
]
y = LY + 9
for i, (mat, col) in enumerate(band_colors):
    dia = 10 - i * 0.3  # Slight taper
    part(f"LightRing{i}", "Cylinder", (dia, 5, dia), (LX, y + 2.5, LZ), mat, col)
    y += 5

# --- Gallery / balcony platform ---
part("LightGallery", "Cylinder", (13, 1.5, 13), (LX, y + 0.75, LZ), "Concrete",
     (90, 85, 80))
part("LightGalleryRail", "Cylinder", (12.5, 1, 12.5), (LX, y + 1.8, LZ), "Metal",
     (60, 55, 50))

# --- Lamp room (Glass walls, Bea's domain) ---
part("LightLampRoom", "Cylinder", (9, 7, 9), (LX, y + 5, LZ), "Glass",
     (255, 250, 220), transparency=0.35)

# Lamp room frame (metal structural rings)
part("LightLampFrameBot", "Cylinder", (9.5, 0.5, 9.5), (LX, y + 1.8, LZ), "Metal",
     (55, 50, 45))
part("LightLampFrameTop", "Cylinder", (9.5, 0.5, 9.5), (LX, y + 8.5, LZ), "Metal",
     (55, 50, 45))

# Vertical frame bars
for i in range(8):
    import math
    angle = i * 45
    rad = math.radians(angle)
    fx = LX + math.cos(rad) * 4.5
    fz = LZ + math.sin(rad) * 4.5
    part(f"LightFrameBar{i}", "Block", (0.3, 7, 0.3), (fx, y + 5, fz), "Metal",
         (60, 55, 50))

# --- Lamp room roof (domed) ---
part("LightRoofDome", "Ball", (10, 6, 10), (LX, y + 10, LZ), "Metal",
     (50, 45, 40))
part("LightRoofFinial", "Cylinder", (0.4, 3, 0.4), (LX, y + 13.5, LZ), "Metal",
     (55, 50, 45))

# --- The Light: rotating beacon ---
# Central glowing core
part("LightBeacon", "Ball", (3, 3, 3), (LX, y + 5, LZ), "Neon",
     (255, 245, 160))
light("LightBeacon", "PointLight", 15, 200, (255, 245, 160), shadows=True)

# Spotlight (the beam that sweeps the fog)
light("LightBeacon", "SpotLight", 20, 300, (255, 245, 160), shadows=False, angle=25)

# Beam arm (invisible rotating part with visible beam glow)
part("LightBeamArm", "Block", (1, 1, 20), (LX, y + 5, LZ + 10), "Neon",
     (255, 245, 160), transparency=0.5, can_collide=False)
light("LightBeamArm", "SpotLight", 15, 250, (255, 245, 160), shadows=False, angle=20)

# Foghorn (mounted on gallery)
part("Foghorn", "Cylinder", (1.5, 3, 1.5), (LX + 5, y + 1.5, LZ), "Metal",
     (50, 45, 40), rotation=(0, 90, 0))
part("FoghornMount", "Block", (1, 1, 1.5), (LX + 4, y + 0.8, LZ), "Metal",
     (45, 42, 38))

# Fog particles around the lighthouse base
particle("LightFoundation", "rbxassetid://258128463", 15, (4, 8), (0.5, 1.5),
         (200, 210, 220), (3, 6), transparency=0.35,
         velocity=(0.3, 0.5, 0.2))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: THE BOARDWALK — connecting everything
# Dock → Cannery → Lighthouse, varied wood, handrails, lantern posts
# ═══════════════════════════════════════════════════════════════════════════════

# Boardwalk segments: dock to cannery (already have dock), cannery to lighthouse
# Segment A: Beach to Cannery south door (Z: 160 → 56)
board_colors = [
    (130, 115, 88), (120, 108, 82), (140, 125, 95), (115, 105, 80),
    (125, 112, 85), (135, 120, 90), (110, 100, 75), (128, 115, 87),
    (118, 106, 80), (132, 118, 89), (122, 110, 83), (127, 114, 86),
]

# Segment A: Beach to Cannery (south approach)
seg_a_start = 158
seg_a_end = CZ + 16
seg_a_length = seg_a_start - seg_a_end
num_planks_a = 20
plank_spacing_a = seg_a_length / num_planks_a
for i in range(num_planks_a):
    pz = seg_a_start - i * plank_spacing_a
    col = board_colors[i % len(board_colors)]
    part(f"BoardPlankA{i}", "Block", (8, 0.4, 2), (0, 10.8, pz), "WoodPlanks", col)

# Segment B: Cannery interior pass-through (the aisle — already has floor)
# This segment uses the cannery floor itself; add plank texture guides
for i in range(6):
    pz = CZ - 12 + i * 4
    col = board_colors[(i + 3) % len(board_colors)]
    part(f"BoardPlankB{i}", "Block", (6, 0.2, 2), (0, CY + 1.1, pz), "WoodPlanks", col)

# Segment C: Cannery north exit to Lighthouse base
seg_c_start = CZ - 16  # North side of cannery
seg_c_end = LZ + 10    # Base of lighthouse
seg_c_length = seg_c_start - seg_c_end
num_planks_c = 24
plank_spacing_c = seg_c_length / num_planks_c
for i in range(num_planks_c):
    pz = seg_c_start - i * plank_spacing_c
    col = board_colors[i % len(board_colors)]
    # Boardwalk rises along the spine
    height_offset = (i / num_planks_c) * 18  # Rises from CY to LY
    py = CY + 0.8 + height_offset
    part(f"BoardPlankC{i}", "Block", (8, 0.4, 2), (0, py, pz), "WoodPlanks", col)

# --- Boardwalk support beams (under Segment C, since it's elevated) ---
for i in range(8):
    pz = seg_c_start - i * (seg_c_length / 8)
    height_offset = (i / num_planks_c) * 18 * 3.5  # approximate
    py = CY + height_offset - 2
    part(f"BoardSupportC{i}", "Block", (10, 1, 1.5), (0, py, pz), "Wood",
         (55, 38, 22))

# --- Handrails along Segment A (water side = east) ---
part("BoardRailA", "Block", (0.4, 3, seg_a_length), (4, 12.3, (seg_a_start + seg_a_end) / 2),
     "Metal", (55, 52, 48))
# Post every 8 studs
for i in range(int(seg_a_length / 8) + 1):
    pz = seg_a_start - i * 8
    if pz >= seg_a_end:
        part(f"BoardRailPostA{i}", "Cylinder", (0.3, 3, 0.3), (4, 12.3, pz), "Metal",
             (50, 48, 45))

# --- Handrails along Segment C (both sides, it's elevated) ---
for side, sx in [("E", 4), ("W", -4)]:
    for i in range(int(seg_c_length / 8) + 1):
        pz = seg_c_start - i * 8
        if pz >= seg_c_end:
            height_offset = (i / num_planks_c) * 18
            py = CY + 0.8 + height_offset + 1.5
            part(f"BoardRailPostC{side}{i}", "Cylinder", (0.3, 3, 0.3), (sx, py, pz),
                 "Wood", (60, 42, 25))

# Top rail Segment C east
part("BoardRailCE", "Block", (0.3, 0.3, seg_c_length),
     (4, CY + 0.8 + 1.5 + 1.5, (seg_c_start + seg_c_end) / 2), "Wood",
     (65, 45, 28))
# Top rail Segment C west
part("BoardRailCW", "Block", (0.3, 0.3, seg_c_length),
     (-4, CY + 0.8 + 1.5 + 1.5, (seg_c_start + seg_c_end) / 2), "Wood",
     (65, 45, 28))

# --- Roller-coaster track handrail section (the signature detail from the bible) ---
part("BoardCoasterRail", "Cylinder", (0.25, 10, 0.25), (4, 12.5, seg_a_start - 5),
     "Metal", (75, 72, 68), rotation=(90, 0, 0))

# --- Lantern posts every 15 studs along entire boardwalk ---
# Segment A lanterns
for i, pz in enumerate(range(int(seg_a_start), int(seg_a_end), 15)):
    part(f"BoardLanternPostA{i}", "Cylinder", (0.35, 7, 0.35), (-3.5, 14.3, pz),
         "Metal", (45, 42, 38))
    part(f"BoardLanternHeadA{i}", "Ball", (1, 1, 1), (-3.5, 18, pz),
         "Neon", (255, 200, 100))
    light(f"BoardLanternHeadA{i}", "PointLight", 3, 18, (255, 200, 100), shadows=False)

# Segment C lanterns
for i in range(0, int(seg_c_length), 15):
    idx = i // 15
    pz = seg_c_start - i
    if pz >= seg_c_end:
        height_offset = (i / seg_c_length) * 18
        py = CY + 0.8 + height_offset
        part(f"BoardLanternPostC{idx}", "Cylinder", (0.35, 7, 0.35),
             (-3.5, py + 3.5, pz), "Metal", (45, 42, 38))
        part(f"BoardLanternHeadC{idx}", "Ball", (1, 1, 1),
             (-3.5, py + 7, pz), "Neon", (255, 200, 100))
        light(f"BoardLanternHeadC{idx}", "PointLight", 3, 18,
              (255, 200, 100), shadows=False)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: TIDELINE BEACH — south shore salvage scatter
# ═══════════════════════════════════════════════════════════════════════════════

# Already laid gravel base in Section 1. Now scatter salvage items.

# --- Rusted server heat sink (used as a buoy) ---
part("SalvageHeatSink", "Block", (4, 1, 3), (-30, 11.5, 165), "CorrodedMetal",
     (100, 60, 35), rotation=(0, 15, 0))
part("SalvageHeatSinkFins", "Block", (3.5, 0.8, 0.3), (-30, 11.5, 164), "Metal",
     (90, 55, 30))
part("SalvageHeatSinkFin2", "Block", (3.5, 0.8, 0.3), (-30, 11.5, 165.5), "Metal",
     (88, 52, 28))
part("SalvageHeatSinkFin3", "Block", (3.5, 0.8, 0.3), (-30, 11.5, 167), "Metal",
     (85, 50, 25))

# --- Tin plate with stamped text (MUD room description) ---
part("SalvageTinPlate", "Block", (3, 0.2, 2), (15, 11.3, 170), "Metal",
     (120, 100, 70), rotation=(0, 30, 0))
part("SalvageTinStand", "Cylinder", (0.2, 1, 0.2), (15, 11, 170.5), "Metal",
     (80, 55, 35))

# --- Oak door half-buried in the gravel (castle door from a dead engine) ---
part("SalvageOakDoor", "Block", (3, 7, 0.5), (25, 14, 160), "Wood",
     (55, 35, 18), rotation=(0, 20, 75))
part("SalvageDoorHinge1", "Cylinder", (0.3, 1.5, 0.3), (24, 14, 159.5), "Metal",
     (60, 55, 50))
part("SalvageDoorHinge2", "Cylinder", (0.3, 1.5, 0.3), (26, 14, 159.5), "Metal",
     (60, 55, 50))

# --- Pipe segments (scattered industrial debris) ---
part("SalvagePipe1", "Cylinder", (1, 8, 1), (-15, 11.5, 175), "CorrodedMetal",
     (90, 50, 28), rotation=(0, 0, 90))
part("SalvagePipe2", "Cylinder", (0.6, 5, 0.6), (35, 11.5, 168), "Metal",
     (75, 70, 65), rotation=(80, 20, 0))
part("SalvagePipeFlange", "Cylinder", (1.5, 0.5, 1.5), (-15, 11.5, 171), "Metal",
     (70, 65, 60))

# --- Broken propeller ---
part("SalvagePropHub", "Cylinder", (1, 1.5, 1), (40, 11.5, 162), "CorrodedMetal",
     (95, 55, 30))
part("SalvagePropBlade1", "Wedge", (0.5, 4, 1.5), (40, 13, 162), "CorrodedMetal",
     (88, 50, 25), rotation=(0, 0, 0))
part("SalvagePropBlade2", "Wedge", (0.5, 4, 1.5), (40, 11, 162), "CorrodedMetal",
     (85, 48, 23), rotation=(180, 0, 0))
part("SalvagePropBlade3", "Wedge", (0.5, 4, 1.5), (41.5, 11.5, 162), "CorrodedMetal",
     (90, 52, 27), rotation=(0, 0, 90))

# --- Barnacle-encrusted hull plate ---
part("SalvageHullPlate", "Block", (6, 4, 0.8), (-40, 13, 158), "CorrodedMetal",
     (85, 45, 25), rotation=(0, 45, 10))
part("SalvageBarnacles1", "Ball", (0.8, 0.6, 0.8), (-39, 12, 157.5), "Concrete",
     (180, 175, 170))
part("SalvageBarnacles2", "Ball", (0.6, 0.5, 0.6), (-41, 13, 158.5), "Concrete",
     (175, 170, 165))
part("SalvageBarnacles3", "Ball", (0.7, 0.5, 0.7), (-38.5, 14, 158), "Concrete",
     (178, 173, 168))

# --- Wafer panel with etched circuitry (from the cinematic) ---
part("SalvageWaferPanel", "Block", (4, 0.3, 3), (8, 11.3, 178), "DiamondPlate",
     (70, 80, 90), rotation=(0, 45, 0))
part("SalvageWaferGlow", "Block", (3.5, 0.15, 2.5), (8, 11.2, 178.1), "Neon",
     (40, 120, 180), transparency=0.3)

# --- Scattered small debris (kelp, driftwood) ---
part("Driftwood1", "Cylinder", (0.5, 6, 0.5), (-20, 11.3, 172), "Wood",
     (90, 72, 48), rotation=(0, 30, 0))
part("Driftwood2", "Cylinder", (0.4, 4, 0.4), (12, 11.3, 180), "Wood",
     (95, 75, 50), rotation=(0, 60, 0))
part("KelpStrand1", "Cylinder", (0.3, 3, 0.3), (-5, 12, 175), "Grass",
     (50, 80, 30), rotation=(15, 0, 10))
part("KelpStrand2", "Cylinder", (0.25, 2.5, 0.25), (3, 12, 182), "Grass",
     (55, 85, 32), rotation=(20, 30, 5))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: AMBIENT ELEMENTS — fog, water, perches
# ═══════════════════════════════════════════════════════════════════════════════

# --- Water plane (surrounding the island, translucent blue) ---
part("WaterPlane", "Block", (800, 1, 800), (0, 2, 0), "Glass",
     (30, 80, 140), transparency=0.55)
part("WaterDeep", "Block", (800, 8, 800), (0, -3, 0), "Glass",
     (20, 50, 100), transparency=0.7)

# --- Fog planes at the edges (the world border — no invisible walls) ---
# North fog wall
part("FogWallN", "Block", (800, 80, 30), (0, 30, -350), "Glass",
     (220, 225, 230), transparency=0.85, can_collide=False)
# South fog wall
part("FogWallS", "Block", (800, 80, 30), (0, 30, 350), "Glass",
     (220, 225, 230), transparency=0.85, can_collide=False)
# East fog wall
part("FogWallE", "Block", (30, 80, 800), (350, 30, 0), "Glass",
     (220, 225, 230), transparency=0.85, can_collide=False)
# West fog wall
part("FogWallW", "Block", (30, 80, 800), (-350, 30, 0), "Glass",
     (220, 225, 230), transparency=0.85, can_collide=False)

# Additional fog layer (overhead, atmospheric)
part("FogOverhead", "Block", (900, 20, 900), (0, 80, 0), "Glass",
     (215, 220, 225), transparency=0.88, can_collide=False)

# Corner fog masses (thicker where walls meet)
for i, (dx, dz) in enumerate([(-350, -350), (350, -350), (-350, 350), (350, 350)]):
    part(f"FogCorner{i}", "Block", (60, 90, 60), (dx, 35, dz), "Glass",
         (220, 225, 230), transparency=0.8, can_collide=False)

# --- Drifting fog patches over the water ---
for i, (dx, dz) in enumerate([(-150, 150), (180, -100), (-200, 50), (120, 200),
                               (-80, -180), (200, 80)]):
    part(f"FogPatch{i}", "Block", (80, 15, 80), (dx, 10, dz), "Glass",
         (220, 225, 230), transparency=0.82, can_collide=False)

# --- Raven perches on cannery roof (3 spots — Forty-Eight's domain) ---
for i, (dx, dz) in enumerate([(-15, 38), (8, 42), (22, 35)]):
    part(f"RavenPerch{i}", "Cylinder", (0.3, 2, 0.3), (CX + dx, CY + 16.5, dz),
         "Metal", (55, 50, 45))
    part(f"RavenPerchTop{i}", "Ball", (0.5, 0.5, 0.5), (CX + dx, CY + 17.8, dz),
         "Wood", (40, 28, 15))

# --- Gull perches on dock pylons ---
for i, pz in enumerate([int(DOCK_Z_START) + 4, int(DOCK_Z_START) + 20, int(DOCK_Z_START) + 36]):
    part(f"GullPerch{i}L", "Cylinder", (0.2, 1, 0.2), (-7.5, CY + 0, pz),
         "Wood", (50, 35, 20))
    part(f"GullPerch{i}R", "Cylinder", (0.2, 1, 0.2), (7.5, CY + 0, pz),
         "Wood", (50, 35, 20))

# --- Earl's Shack (bolted to cannery landward corner) ---
part("EarlShackFloor", "Block", (8, 0.5, 8), (CX - 34, CY + 1, CZ - 8), "WoodPlanks",
     (75, 52, 30))
part("EarlShackWallN", "Block", (8, 6, 0.5), (CX - 34, CY + 4, CZ - 12), "CorrodedMetal",
     (110, 48, 26))
part("EarlShackWallW", "Block", (0.5, 6, 8), (CX - 38, CY + 4, CZ - 8), "CorrodedMetal",
     (108, 46, 25))
part("EarlShackWallS", "Block", (8, 6, 0.5), (CX - 34, CY + 4, CZ - 4), "CorrodedMetal",
     (112, 50, 28))
part("EarlShackRoof", "Block", (9, 0.5, 9), (CX - 34, CY + 7.5, CZ - 8), "CorrodedMetal",
     (95, 40, 20))

# Manifest window (ticket-booth style)
part("EarlManifestWindow", "Block", (3, 3, 0.3), (CX - 34, CY + 4, CZ - 3.8), "Glass",
     (180, 170, 130), transparency=0.5)
part("EarlManifestGlow", "Block", (2.5, 2.5, 0.15), (CX - 34, CY + 4, CZ - 3.7),
     "Neon", (255, 200, 120), transparency=0.2)
light("EarlManifestGlow", "PointLight", 2, 10, (255, 200, 120), shadows=False)

# Spark's bucket (outside the door)
part("SparkBucket", "Cylinder", (1, 1.5, 1), (CX - 30, CY + 1.5, CZ - 4), "Metal",
     (180, 130, 30))
part("SparkBucketHandle", "Cylinder", (0.1, 1.5, 0.1), (CX - 30, CY + 2.5, CZ - 4),
     "Metal", (160, 120, 25), rotation=(90, 0, 0))

# --- Notice Wall (bulkhead shingled with postings, along the boardwalk) ---
part("NoticeWallBack", "Block", (0.5, 8, 12), (6, 14, 80), "Wood", (55, 38, 22))
part("NoticeBoard1", "Block", (0.2, 3, 2.5), (5.8, 15, 76), "WoodPlanks", (120, 100, 70))
part("NoticeBoard2", "Block", (0.2, 2.5, 2), (5.8, 13, 80), "WoodPlanks", (130, 110, 75))
part("NoticeBoard3", "Block", (0.2, 2, 3), (5.8, 16, 84), "WoodPlanks", (110, 95, 65))
# The fishing derby poster (weathered, from a dead engine)
part("NoticeDerbyPoster", "Block", (0.15, 3, 2), (5.85, 14, 88), "Fabric",
     (180, 150, 80), transparency=0.3)

# --- Storm bell (on a post near the dock, mentioned in world bible) ---
part("StormBellPost", "Cylinder", (0.4, 10, 0.4), (-6, CY + 5, DOCK_Z_START + 3),
     "Wood", (55, 38, 22))
part("StormBell", "Ball", (1.5, 2, 1.5), (-6, CY + 10, DOCK_Z_START + 3), "Metal",
     (90, 70, 40))
part("StormBellFrame", "Cylinder", (0.2, 2, 0.2), (-6, CY + 10.5, DOCK_Z_START + 3),
     "Metal", (60, 55, 50), rotation=(90, 0, 0))

# --- Lectern / Logbook (by the cannery door) ---
part("LecternBase", "Block", (2, 3, 2), (CX + 10, CY + 1.5, CZ + 13), "Wood",
     (60, 42, 25))
part("LecternTop", "Wedge", (3, 0.5, 2), (CX + 10, CY + 3.5, CZ + 13), "WoodPlanks",
     (75, 52, 30), rotation=(0, 0, 15))
part("LecternBook", "Block", (2, 0.5, 1.5), (CX + 10, CY + 4, CZ + 13), "Fabric",
     (80, 50, 25))
light("LecternBook", "PointLight", 1, 8, (255, 200, 120), shadows=False)

# --- Spawn marker (where players arrive — on the tideline) ---
part("SpawnPlatform", "Block", (6, 0.3, 6), (0, 11.2, 165), "WoodPlanks",
     (100, 75, 45))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9: AMBIENT LIGHTING & PARTICLES
# ═══════════════════════════════════════════════════════════════════════════════

# Overall atmospheric fill light (warm, subtle, covers the hub)
light("ForgeCeilingGlow", "PointLight", 4, 80, (255, 160, 80), shadows=False)

# Dock area fill light
light("DockDeck", "PointLight", 2, 30, (255, 200, 120), shadows=False)

# Beach atmospheric light (cool, contrasting with forge warmth)
part("BeachFillLight", "Ball", (0.5, 0.5, 0.5), (0, 15, 175), "Neon",
     (100, 120, 150), transparency=0.9, can_collide=False)
light("BeachFillLight", "PointLight", 2, 40, (120, 150, 200), shadows=False)

# Lighthouse trail fill
part("TrailFill", "Ball", (0.5, 0.5, 0.5), (0, 20, -50), "Neon",
     (150, 120, 80), transparency=0.9, can_collide=False)
light("TrailFill", "PointLight", 2, 30, (180, 150, 100), shadows=False)

# Atmospheric mist particles across the water
particle("WaterPlane", "rbxassetid://258128463", 8, (5, 10), (0.3, 1),
         (210, 215, 225), (4, 8), transparency=0.5,
         velocity=(0.2, 0.3, 0.1))

# Ambient sound markers (as particle emitters for visual atmosphere)
particle("FogWallS", "rbxassetid://258128463", 6, (4, 8), (0.5, 1.5),
         (225, 228, 232), (3, 7), transparency=0.3,
         velocity=(0, 0.5, 0.1))


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hub_build.json")
with open(output_path, "w") as f:
    json.dump(commands, f, indent=2)

print(f"Slackwater Hub build generated: {output_path}")
print(f"Total commands: {len(commands)}")

# Print breakdown
types = {}
for cmd in commands:
    types[cmd["type"]] = types.get(cmd["type"], 0) + 1
for t, c in sorted(types.items()):
    print(f"  {t}: {c}")
