# LUCINEER — THE POLISH PLAN

**Date:** 2026-08-02
**Prerequisite:** the P0 items in `GAP_ANALYSIS.md`. None of this is visible until the
core loop runs.

---

## THE THESIS

There is a temptation to fix "the builds look basic" by adding detail to the builds. That
is the expensive path and the second-best one.

**The three things that most change how a Roblox build reads, in order of leverage:**

1. **The lighting and atmosphere rig** — global, one-time, affects every build ever made.
2. **The choreography of construction** — *how* parts arrive, not what they are.
3. **The parts themselves** — materials, colors, greebling.

A gray box under a tuned Future-lighting rig with volumetric atmosphere, color grading,
and bloom, that *rises out of the ground with dust and a settling sound*, looks better
than a detailed 40-part castle that pops into existence under default lighting. Item 3 is
where 90% of the effort usually goes and where the least perceived quality lives.

**This document owns items 1 and 2, plus everything non-visual.** Item 3 — the material,
color, and template system — is Kimi's brief (`VISUAL_POLISH.md`,
`build_templates_v2.py`). The two documents meet at the `createPart` command schema, so
the extension in §1.4 below is the shared contract and should be agreed before either side
writes code.

---

## §1 — VISUAL POLISH

### 1.1 The lighting rig (highest leverage change in this entire document)

Roblox's default lighting is flat, gray, and shadowless. Every experience that looks
striking has a tuned rig. This is a one-time setup that improves every build retroactively.

The aesthetic target: **industrial Southeast Alaska.** Overcast, high-latitude, low sun.
Wet surfaces. Air you can see. Warm artificial light against cold ambient — that contrast
is the entire look, and it's what makes Lucineer's lanterns and forge-glow read as
meaningful rather than decorative.

Create `src/ServerScriptService/LucineerServer/Atmosphere.lua`:

```lua
--[[
    Lucineer Atmosphere Rig
    Global lighting, post-processing, and weather. Set once at startup.
    This does more for perceived build quality than any per-part change.
]]

local Lighting = game:GetService("Lighting")
local TweenService = game:GetService("TweenService")

local Atmosphere = {}

-- Low-sun overcast maritime. Cold ambient, warm practicals, visible air.
local PRESETS = {
    overcast = {
        ClockTime = 15.2,          -- low sun = long shadows = depth
        GeographicLatitude = 56,   -- Petersburg, AK
        Brightness = 2.1,
        ExposureCompensation = 0.15,
        OutdoorAmbient = Color3.fromRGB(88, 100, 112),   -- cold blue-gray
        Ambient = Color3.fromRGB(52, 58, 66),
        ColorShift_Top = Color3.fromRGB(150, 160, 170),
        ColorShift_Bottom = Color3.fromRGB(70, 72, 78),
        FogEnd = 1800,
        atmosphere = {
            Density = 0.42, Offset = 0.15,
            Color = Color3.fromRGB(178, 188, 196),
            Decay = Color3.fromRGB(96, 108, 122),
            Glare = 0.28, Haze = 1.9,
        },
        correction = {
            Brightness = 0.02, Contrast = 0.14, Saturation = -0.08,
            TintColor = Color3.fromRGB(240, 246, 255),
        },
        bloom = { Intensity = 0.85, Size = 22, Threshold = 1.7 },
    },

    -- Golden hour. Reserve this — see §2, the 45-second beat.
    goldenhour = {
        ClockTime = 17.4,
        GeographicLatitude = 56,
        Brightness = 2.6,
        ExposureCompensation = 0.3,
        OutdoorAmbient = Color3.fromRGB(112, 96, 88),
        Ambient = Color3.fromRGB(64, 52, 46),
        ColorShift_Top = Color3.fromRGB(255, 196, 132),
        ColorShift_Bottom = Color3.fromRGB(92, 70, 60),
        FogEnd = 2400,
        atmosphere = {
            Density = 0.38, Offset = 0.25,
            Color = Color3.fromRGB(214, 190, 168),
            Decay = Color3.fromRGB(140, 96, 70),
            Glare = 0.55, Haze = 2.4,
        },
        correction = {
            Brightness = 0.04, Contrast = 0.18, Saturation = 0.06,
            TintColor = Color3.fromRGB(255, 244, 228),
        },
        bloom = { Intensity = 1.3, Size = 26, Threshold = 1.5 },
    },

    -- Magic Moment 4. Storm.
    storm = {
        ClockTime = 14.0,
        GeographicLatitude = 56,
        Brightness = 1.2,
        ExposureCompensation = -0.25,
        OutdoorAmbient = Color3.fromRGB(62, 70, 80),
        Ambient = Color3.fromRGB(34, 40, 48),
        ColorShift_Top = Color3.fromRGB(96, 104, 116),
        ColorShift_Bottom = Color3.fromRGB(44, 48, 54),
        FogEnd = 700,              -- claustrophobic; the world closes in
        atmosphere = {
            Density = 0.62, Offset = 0.05,
            Color = Color3.fromRGB(150, 158, 168),
            Decay = Color3.fromRGB(70, 78, 88),
            Glare = 0.1, Haze = 3.4,
        },
        correction = {
            Brightness = -0.03, Contrast = 0.22, Saturation = -0.28,
            TintColor = Color3.fromRGB(226, 234, 248),
        },
        bloom = { Intensity = 0.5, Size = 18, Threshold = 2.0 },
    },
}

local instances = {}   -- cached effect instances

local function ensureEffects()
    if instances.atmosphere then return end

    Lighting.Technology = Enum.Technology.Future   -- required for real shadows + PBR
    Lighting.GlobalShadows = true
    Lighting.EnvironmentDiffuseScale = 0.6
    Lighting.EnvironmentSpecularScale = 0.7
    Lighting.ShadowSoftness = 0.35

    local function ensure(className: string, name: string): Instance
        local existing = Lighting:FindFirstChild(name)
        if existing then return existing end
        local inst = Instance.new(className)
        inst.Name = name
        inst.Parent = Lighting
        return inst
    end

    instances.atmosphere = ensure("Atmosphere", "LucineerAtmosphere")
    instances.correction = ensure("ColorCorrectionEffect", "LucineerGrade")
    instances.bloom      = ensure("BloomEffect", "LucineerBloom")
    instances.sunRays    = ensure("SunRaysEffect", "LucineerSunRays")
    instances.dof        = ensure("DepthOfFieldEffect", "LucineerDOF")

    instances.sunRays.Intensity = 0.12
    instances.sunRays.Spread = 0.9

    -- Subtle. Enough to separate foreground from background, not enough to notice.
    instances.dof.FarIntensity = 0.12
    instances.dof.FocusDistance = 55
    instances.dof.InFocusRadius = 180
    instances.dof.NearIntensity = 0
end

--[[
    Apply a preset, optionally tweened.
    @param name string -- "overcast" | "goldenhour" | "storm"
    @param duration number? -- seconds to blend (0 = instant)
]]
function Atmosphere.apply(name: string, duration: number?)
    ensureEffects()
    local preset = PRESETS[name]
    if not preset then
        warn(string.format("[Lucineer] Atmosphere: unknown preset '%s'", name))
        return
    end

    duration = duration or 0
    local info = TweenInfo.new(duration, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut)

    local function applyTo(target: Instance, props: { [string]: any })
        if duration <= 0 then
            for k, v in pairs(props) do target[k] = v end
        else
            TweenService:Create(target, info, props):Play()
        end
    end

    local lightingProps = {}
    for k, v in pairs(preset) do
        if k ~= "atmosphere" and k ~= "correction" and k ~= "bloom" then
            lightingProps[k] = v
        end
    end

    -- ClockTime and GeographicLatitude aren't tweenable in a way that reads well.
    Lighting.GeographicLatitude = preset.GeographicLatitude
    lightingProps.GeographicLatitude = nil

    applyTo(Lighting, lightingProps)
    applyTo(instances.atmosphere, preset.atmosphere)
    applyTo(instances.correction, preset.correction)
    applyTo(instances.bloom, preset.bloom)
end

function Atmosphere.init()
    Atmosphere.apply("overcast", 0)
    print("[Lucineer] Atmosphere: rig installed")
end

return Atmosphere
```

**Two settings carry most of the weight:**

- **`Lighting.Technology = Future`** — without it there are no real-time shadows from
  `PointLight`s, which means Lucineer's lanterns and forge-glow contribute nothing. With
  it, a single warm point light inside a gray stone tower creates the entire mood.
- **`Atmosphere.Density`** — visible air is what makes a Roblox scene stop looking like
  parts on a baseplate. It gives depth cueing for free and makes distant builds recede.

**Cost check:** Future lighting is more expensive on low-end mobile. Gate it:

```lua
-- Client-side quality scaling
if UserInputService.TouchEnabled and not UserInputService.KeyboardEnabled then
    Lighting.ShadowSoftness = 0
    instances.dof.Enabled = false
    instances.sunRays.Enabled = false
end
```

### 1.2 Build choreography — the second-highest-leverage change

Right now `CommandExecutor.executeBatch` (`CommandExecutor.lua:408`) creates every part in
a single frame. Twenty parts appear simultaneously. That reads as **a texture popping in**,
not as building.

The fix is not more parts. It's *time*.

Create `src/ReplicatedStorage/Lucineer/BuildFX.lua`:

```lua
--[[
    Lucineer Build FX
    Parts don't appear — they arrive. Scale-in, settle, dust, sound.
    This is what makes twenty gray boxes feel like construction.
]]

local TweenService = game:GetService("TweenService")
local Debris = game:GetService("Debris")

local BuildFX = {}

local SETTLE = TweenInfo.new(0.34, Enum.EasingStyle.Back, Enum.EasingDirection.Out)
local FADE   = TweenInfo.new(0.28, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)

--[[
    Animate a part into existence: rises from below, scales up, settles.
    @param part BasePart
    @param delay number -- stagger offset in seconds
]]
function BuildFX.materialize(part: BasePart, delay: number?)
    local targetSize = part.Size
    local targetCFrame = part.CFrame
    local targetTransparency = part.Transparency

    -- Start small, low, and ghosted.
    part.Size = targetSize * 0.05
    part.CFrame = targetCFrame - Vector3.new(0, math.min(targetSize.Y, 6) * 0.6, 0)
    part.Transparency = 1

    task.delay(delay or 0, function()
        if not part.Parent then return end
        TweenService:Create(part, SETTLE, {
            Size = targetSize,
            CFrame = targetCFrame,
        }):Play()
        TweenService:Create(part, FADE, {
            Transparency = targetTransparency,
        }):Play()
        BuildFX.dust(part)
    end)
end

--[[ A short puff of dust at the part's base. Sells the weight. ]]
function BuildFX.dust(part: BasePart)
    local attachment = Instance.new("Attachment")
    attachment.Position = Vector3.new(0, -part.Size.Y / 2, 0)
    attachment.Parent = part

    local emitter = Instance.new("ParticleEmitter")
    emitter.Texture = "rbxassetid://241876428"    -- soft smoke puff
    emitter.Color = ColorSequence.new(Color3.fromRGB(196, 190, 178))
    emitter.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0.5),
        NumberSequenceKeypoint.new(1, 1),
    })
    emitter.Size = NumberSequence.new({
        NumberSequenceKeypoint.new(0, math.clamp(part.Size.Magnitude * 0.12, 0.5, 4)),
        NumberSequenceKeypoint.new(1, math.clamp(part.Size.Magnitude * 0.3, 1, 9)),
    })
    emitter.Lifetime = NumberRange.new(0.4, 0.9)
    emitter.Speed = NumberRange.new(1, 3)
    emitter.SpreadAngle = Vector2.new(180, 180)
    emitter.Rate = 0
    emitter.Drag = 4
    emitter.Parent = attachment

    emitter:Emit(math.clamp(math.floor(part.Size.Magnitude), 4, 24))
    Debris:AddItem(attachment, 2)
end

--[[
    Stagger a whole batch. Returns total duration so callers can sequence.
    Grouped in small waves — reads as deliberate work, not a conveyor belt.
]]
function BuildFX.materializeBatch(parts: { BasePart }): number
    local WAVE = 3
    local WAVE_GAP = 0.13
    for i, part in ipairs(parts) do
        BuildFX.materialize(part, math.floor((i - 1) / WAVE) * WAVE_GAP)
    end
    return math.ceil(#parts / WAVE) * WAVE_GAP + 0.4
end

return BuildFX
```

Wire it into the executor:

```lua
-- CommandExecutor.executeBatch
local BuildFX = require(script.Parent.BuildFX)

function CommandExecutor.executeBatch(commands: { table }): { table }
    local results = {}
    local created: { BasePart } = {}

    for i, command in ipairs(commands) do
        local result, err = CommandExecutor.execute(command)
        table.insert(results, {
            index = i, type = command.type,
            success = err == nil, result = result, error = err,
        })
        if typeof(result) == "Instance" and result:IsA("BasePart") then
            table.insert(created, result)
        end
    end

    BuildFX.materializeBatch(created)
    return results
end
```

**Effect:** a 20-part castle now takes ~1.3 seconds to assemble, wave by wave, each wave
with dust. That is the single change most likely to make someone say "whoa" — and it costs
nothing per build because the work is in one module.

### 1.3 The "unfinished" affordance needs to be *visible*

Lucineer's defining trait is leaving work undone as an invitation
(`CHARACTER_BIBLE.md` §1). Right now that exists only as text in a reply. **A player who
doesn't read carefully will experience it as the build being broken.**

Make it legible. Every build marks its open hook with a physical affordance:

```lua
--[[
    Mark a deliberately unfinished region. Chalk outline + faint glow +
    a floating label. This is Lucineer's signature, made visible.
]]
function BuildFX.markUnfinished(cframe: CFrame, size: Vector3, label: string)
    local marker = Instance.new("Part")
    marker.Name = "LucineerHook"
    marker.Size = size
    marker.CFrame = cframe
    marker.Anchored = true
    marker.CanCollide = false
    marker.CanQuery = false
    marker.Transparency = 1
    marker.Parent = workspace:FindFirstChild("LucineerBuilds")

    -- Chalked outline — reads as "marked out, not built."
    local box = Instance.new("SelectionBox")
    box.Adornee = marker
    box.Color3 = Color3.fromRGB(255, 214, 120)
    box.LineThickness = 0.035
    box.SurfaceTransparency = 0.94
    box.SurfaceColor3 = Color3.fromRGB(255, 200, 90)
    box.Parent = marker

    local billboard = Instance.new("BillboardGui")
    billboard.Size = UDim2.new(0, 190, 0, 34)
    billboard.StudsOffset = Vector3.new(0, size.Y / 2 + 2, 0)
    billboard.AlwaysOnTop = false
    billboard.MaxDistance = 140
    billboard.Parent = marker

    local text = Instance.new("TextLabel")
    text.Size = UDim2.fromScale(1, 1)
    text.BackgroundTransparency = 1
    text.Font = Enum.Font.GothamMedium
    text.TextSize = 13
    text.TextColor3 = Color3.fromRGB(255, 214, 120)
    text.TextStrokeTransparency = 0.5
    text.Text = label      -- e.g. "left open — your call"
    text.Parent = billboard

    -- Slow breathing pulse. Patient, not nagging.
    task.spawn(function()
        while marker.Parent do
            TweenService:Create(box, TweenInfo.new(2.2, Enum.EasingStyle.Sine), 
                { SurfaceTransparency = 0.86 }):Play()
            task.wait(2.2)
            TweenService:Create(box, TweenInfo.new(2.2, Enum.EasingStyle.Sine),
                { SurfaceTransparency = 0.97 }):Play()
            task.wait(2.2)
        end
    end)

    return marker
end
```

**This also solves the bond-detection problem** from `CHARACTER_BIBLE.md` §4. The marker
is a real part with a real bounding box — watch for player-authored parts inside it and
you have your `+5 bond` trigger, with no heuristics:

```lua
marker:GetPropertyChangedSignal("Parent"):Connect(...)  -- or poll on a slow timer
local overlapping = workspace:GetPartBoundsInBox(marker.CFrame, marker.Size, playerFilter)
if #overlapping > 0 then
    -- Player built in the gap. Fire Magic Moment 3.
end
```

Requires a new command type, `markUnfinished`, added to the schema in §1.4.

### 1.4 Command schema extension (shared contract with Kimi's `build_templates_v2.py`)

Agree this before either side writes templates. Additions to `createPart`:

```jsonc
{
  "type": "createPart",
  "params": {
    "name": "CastleWallNorth",
    "position": {"x": 0, "y": 7, "z": -20},
    "size": {"x": 40, "y": 15, "z": 2},
    "material": "Cobblestone",
    "color": "#6E6A64",

    // --- NEW ---
    "rotation": {"x": 0, "y": 45, "z": 0},   // degrees; currently impossible to rotate
    "reflectance": 0.05,                      // wet-stone sheen
    "castShadow": true,
    "colorJitter": 8,                         // ±8 RGB per part — kills the "printed" look
    "surfaceAppearance": {                    // PBR; the single biggest material upgrade
      "colorMap": "rbxassetid://...",
      "normalMap": "rbxassetid://...",
      "roughnessMap": "rbxassetid://..."
    },
    "fx": "materialize" | "instant",
    "tag": "structure" | "detail" | "light" | "hook"
  }
}
```

Three of these matter disproportionately:

- **`rotation`** — the executor has **no rotation support at all** today
  (`CommandExecutor.lua:100` sets `Position` only). Every build in the system is
  axis-aligned. Pitched roofs, angled braces, and radial towers are *impossible* right now.
  This is a bigger visual limitation than materials.
- **`colorJitter`** — applying ±8 RGB of noise per part is a two-line change that makes
  uniform stone read as laid stone. Cheapest realism in the document.
- **`tag`** — lets the client treat structure, detail, and light differently for
  choreography, LOD, and the unfinished-hook detection above.

Rotation support:

```lua
-- CommandExecutor.createPart, replacing the Position assignment
local pos = parseVector3(params.position or { x = 0, y = 5, z = 0 })
local rot = params.rotation
if rot then
    part.CFrame = CFrame.new(pos) * CFrame.Angles(
        math.rad(rot.x or 0), math.rad(rot.y or 0), math.rad(rot.z or 0))
else
    part.Position = pos
end

if params.colorJitter then
    local j = params.colorJitter
    local base = part.Color
    part.Color = Color3.fromRGB(
        math.clamp(base.R * 255 + math.random(-j, j), 0, 255),
        math.clamp(base.G * 255 + math.random(-j, j), 0, 255),
        math.clamp(base.B * 255 + math.random(-j, j), 0, 255))
end
```

### 1.5 What *not* to do

- **Don't chase MeshParts yet.** They need modeling, upload, and moderation review, and
  they won't help until lighting and choreography are in. Revisit after launch.
- **Don't add more parts per build.** Twenty well-lit, well-choreographed, slightly
  jittered parts beat sixty flat ones, and the part budget is real on mobile.
- **Don't use `Neon` for everything that glows.** It currently appears in nearly every
  template (`process_v2.py:120,133,146,...`). Neon is emissive but casts no light. A
  `Neon` ball with a `PointLight` inside it is correct; `Neon` alone is a flat sticker.

---

## §2 — THE FIRST SIXTY SECONDS

The most important minute in the product. It has one job: **establish that Lucineer is a
person with opinions, not a command parser.** Everything else is downstream of that.

### The beat sheet

| t | Beat | What the player experiences |
|---|---|---|
| 0:00 | **Land in weather** | No menu, no splash. Spawn on a working dock in the overcast rig. Rain on the water, a foghorn a long way off, gulls. It reads as a *place*, not a lobby. |
| 0:03 | **He's already working** | Lucineer is visible ~25 studs away, mid-build, back turned. He does not greet you. He is doing something and hasn't noticed. |
| 0:08 | **He notices** | Turns. Doesn't approach. `"You're new."` Beat. `"Grab a corner or don't, I'm not fussy."` Then goes back to work. |
| 0:15 | **The invitation is environmental** | The thing he's building has a visible `LucineerHook` marker: a chalked outline with *"left open — your call."* No tutorial popup. No arrow. |
| 0:20 | **Player experiments** | Whatever they do — walk over, type, stand there — he responds proportionally. Silence is fine. He doesn't prompt. |
| 0:25 | **First request** | Player types something. **Instant** in-voice ack (`GAP_ANALYSIS.md` #8b), before any model call: *"Alright. Let me look at the ground first."* |
| 0:28 | **Magic Moment 1 — The Siting** | Ghost preview appears where they pointed — then **slides forty studs** and settles on higher ground. `"You were standing in the wet."` |
| 0:34 | **The build** | Wave-by-wave materialization with dust and settling sound (§1.2). ~1.5s. Camera does *not* take over — the player keeps control. |
| 0:40 | **The hook** | Build completes with one visible gap and one line naming it. `"Left the top floor open. Figure out what goes in it."` |
| 0:45 | **The sky turns** | Weather breaks. `Atmosphere.apply("goldenhour", 8)` — an eight-second blend to low golden light across everything, including what they just built. |
| 0:52 | **He walks away** | He goes back to his own work without waiting for thanks. |
| 0:60 | **The player is alone with a thing they own** | No objective marker. No next step. The unfinished hook is glowing patiently. |

### Why it's built this way

**No tutorial, no UI.** Every affordance is diegetic — the chalk marker teaches the core
loop better than any popup, and it's already needed for bond detection.

**He doesn't greet the player.** Nearly every AI companion opens with a greeting and an
offer of help. Opening with *indifference* is the strongest possible signal that this one
is different, and it costs one line of dialogue.

**The disagreement is the third thing that happens.** Not the tenth. The Siting has to
land inside the first minute or the player has already filed Lucineer under "assistant."

**Golden hour is a reward, not a default.** Holding the world at overcast for 45 seconds
and then blending to golden light makes the *player's build* the thing the sun comes out
for. Reserve `goldenhour` for beats like this and for returning-player moments.

### Delete these immediately

```lua
-- LucineerClient/init.lua:107 — off-voice, and it fires on a blind 3-second timer
task.delay(3, function()
    UIManager.displayChatResponse("Hi! I'm Lucineer. Tell me what to build and I'll make it happen.")
end)

-- LucineerClient/init.lua:85 — the client narrating on Lucineer's behalf
UIManager.displayChatResponse(string.format("Done! I built %d action(s) for you.", succeeded))
```

Both are listed as anti-patterns in `CHARACTER_BIBLE.md` §10 and both are currently
shipping. The second is worse than it looks: because of `GAP_ANALYSIS.md` #2c, **it is
currently the only text a player can ever see from Lucineer.** The character, as
experienced today, is a progress counter.

Replacement for the second — say nothing on success. The build *is* the confirmation. Only
speak on partial failure, and in voice:

```lua
elseif data.type == "commands" then
    local failed = 0
    for _, r in ipairs(data.results or {}) do
        if not r.success then failed += 1 end
    end
    -- Success speaks for itself. He doesn't announce finished work.
    if failed > 0 then
        UIManager.displayChatResponse(
            "Part of that didn't seat right. Give me a second look at it.")
    end
end
```

---

## §3 — SOUND DESIGN

Currently: `SoundService` exists in the place file and contains nothing. `addSound`
(`CommandExecutor.lua:215`) defaults to `rbxassetid://0`.

Sound is the cheapest presence multiplier available. Four layers.

### Layer 1 — Ambient bed (continuous, positional)

Always running, never noticed, immediately missed if removed.

| Source | Placement | Volume | Notes |
|---|---|---|---|
| Water lapping | Attached to shoreline parts, `RollOffMaxDistance` 120 | 0.25 | The Alaska anchor |
| Wind | Non-positional in `SoundService`, looped | 0.12 | Ties to `Atmosphere` preset — rises with storm |
| Distant foghorn | Random 90–240 s interval, far position | 0.35 | The single most evocative sound in the palette. Use sparingly. |
| Gulls | Random 20–60 s, high position | 0.18 | Placement varies; never twice in the same spot |
| Rigging / chain creak | Near Lucineer's own structures | 0.15 | Industrial texture |

```lua
-- Ambience.lua — pseudo-random punctuation, never on a metronome
local function scheduleOccasional(sound: Sound, minGap: number, maxGap: number)
    task.spawn(function()
        while true do
            task.wait(math.random(minGap, maxGap))
            sound.PlaybackSpeed = 0.94 + math.random() * 0.12   -- never identical twice
            sound:Play()
        end
    end)
end
```

**The pitch jitter matters.** A foghorn that is bit-identical every time reads as a loop
within three plays. ±6% playback speed makes it read as a real horn at a real distance.

### Layer 2 — Build SFX (the payoff layer)

Synced to `BuildFX.materializeBatch`. This is where "wow" lives.

| Event | Sound | Timing |
|---|---|---|
| Part settles | Low wooden/stone thunk, pitch scaled to part volume | Per wave, on `SETTLE` completion |
| Large part settles | Add sub-bass impact + brief camera shake (≤0.2 studs) | Volume > 400 studs³ |
| Metal part | Ring with short tail | Material-dependent |
| Build begins | Single tool-down clack | On first wave |
| Build completes | Cloth-brush / hands-dusting-off | 0.3 s after last wave |
| Hook marker appears | Soft chalk scrape | With the `SelectionBox` fade-in |

```lua
-- Pitch by mass. Big things sound big. Free perceived weight.
local function settleSound(part: BasePart)
    local volume = part.Size.X * part.Size.Y * part.Size.Z
    local sound = Instance.new("Sound")
    sound.SoundId = MATERIAL_SETTLE[part.Material.Name] or MATERIAL_SETTLE.Default
    sound.PlaybackSpeed = math.clamp(1.6 - math.log(volume + 1) * 0.13, 0.55, 1.5)
    sound.Volume = math.clamp(0.16 + volume / 6000, 0.16, 0.55)
    sound.RollOffMaxDistance = 90
    sound.Parent = part
    sound:Play()
    Debris:AddItem(sound, 3)
end
```

**Cap concurrent settle sounds at ~6.** Twenty simultaneous thunks is mud. The wave
grouping in §1.2 mostly handles this; add a hard limiter anyway.

### Layer 3 — Lucineer's voice

`Qwen3-TTS-VoiceDesign` is listed as available. **Do not synthesize full lines at runtime**
— the latency budget is already broken (`GAP_ANALYSIS.md` #8a) and adding TTS to the
critical path makes it worse.

**Do this instead: pre-generate a non-verbal vocal set.** Thirty to forty short sounds —
grunts, "hm," a short exhale, a tool-down sigh, an approving "mm." Play one at the *start*
of a reply while the text renders.

This is the Animal Crossing / Banjo-Kazooie technique and it is dramatically more effective
than full TTS: it gives a voice without lip-sync, without latency, without a per-request
cost, and without ever mispronouncing anything. The player's brain supplies the rest.

| Context | Vocalization |
|---|---|
| Starting work | Short exhale, tool-down clack |
| Disagreeing (§7) | A flat "hn." Nothing else. Perfect. |
| Approving (Tier 2+) | Rising "mm" |
| The Handoff pause (Moment 3) | **Silence.** Four seconds. Then "Huh." |
| Correcting his own error | Tongue click, then the line |

Voice design target: **low, unhurried, slightly gravelly, mid-fifties, unbothered.** Not
gruff-comedic. The reference is a foreman who has never once needed to raise his voice.

### Layer 4 — Music

**Mostly absent, and that's the design.** A continuous score fights the ambient bed and
makes the world feel like a level instead of a place.

Music appears exactly four times:

1. **Storm arrival** — low drone in, no melody. Tension.
2. **Storm clears** — a resolving figure, ~12 s, then out.
3. **Bond tier-up** — four notes. Not a fanfare. A small acknowledgement.
4. **Magic Moment 5 (The Yard)** — the only real cue in the game, ~90 s, under the gantry
   build and the confession. It should be the first time the player has heard sustained
   music, which is precisely why it lands.

Instrumentation: upright bass, brushed percussion, a single reed. Sparse. Nothing
orchestral.

---

## §4 — SOCIAL AND VIRAL MECHANICS

**Reality check:** this system currently has one Durable Object for all sessions
(`GAP_ANALYSIS.md` #6c) and no multiplayer awareness at all. Everything here is gated on
that fix. Prioritize accordingly — this section is P2 relative to the rest of the document.

### 4.1 The shareable artifact: the Build Card

The clip-friendly moment is the *before/after with Lucineer's line attached.* Automate it.

On build completion, generate a card the player can save or post:

```
┌─────────────────────────────────────────┐
│  [render of the build, golden hour]     │
│                                         │
│  "Left the top floor open. Figure out   │
│   what goes in it."                     │
│                            — Lucineer   │
│                                         │
│  built with @PlayerName · session 14    │
│  lucineer.gg/b/7f3a9c                   │
└─────────────────────────────────────────┘
```

The quote is the viral payload. A screenshot of a Roblox castle is not interesting; a
screenshot of a Roblox castle **with a crusty foreman's opinion attached** is. The
character is the shareable asset, not the geometry.

Implementation: `ViewportFrame` render client-side, composited with the reply text, saved
via the share sheet on mobile. The short URL resolves to a page rendered from
`build_history` — which is already schemaed (`memory/schema.sql:14`) and currently unused
(`GAP_ANALYSIS.md` #4).

### 4.2 Lucineer talks about other players

The strongest social mechanic available, and it's nearly free once memory is wired.

When player B enters a region where player A built:

> "That's Tam's work. She runs her rails on the inside — I've started doing it her way."

This does three things at once: credits absent players, propagates technique across the
community, and makes the world feel inhabited by people rather than by accounts. It also
directly rewards Magic Moment 3 — a preference Lucineer learned from you gets *taught to
strangers.* That is a genuinely novel social loop and it's the most defensible idea in
this document.

### 4.3 The Yard (shared persistent world)

One shared build site per ~20 players, persistent across sessions. Lucineer is the
continuity: he remembers who built what, and he'll tell you.

> "Somebody put a dock in on the north side while you were gone. Not bad. Piles are shallow
> — I'd have driven them deeper, but it's holding."

Deliberately **not** a competitive space. No claiming, no griefing surface, no scores.
Contribution is the only verb.

### 4.4 Co-op building

Two players plus Lucineer. He assigns roles, and — critically — he *has opinions about how
you're working together*:

> "You two are both building walls. Somebody needs to be thinking about the roof."

### 4.5 What to skip

- **Leaderboards.** Antithetical to the character. Lucineer does not rank people; he
  notices whether you showed up. A leaderboard would contradict §6 of the Character Bible
  in the first five minutes.
- **Trading / economy.** Different game. Adds a griefing surface and a moderation burden.
- **Voice chat integration.** Latency and moderation cost far exceed the benefit here.

---

## §5 — PROGRESSION

### 5.1 Design principle

`ROUNDTABLE_BRIEF.md` cites 49 achievements in prior work. Resist porting that model
directly. **Lucineer's progression is a relationship, not a checklist**, and a visible
achievement grid would undercut it — the moment a player sees "Build 10 Towers (3/10)",
Lucineer becomes a quest dispenser.

So: **bond is the only meter, it is never shown as a number, and progression is expressed
entirely through his behavior.**

### 5.2 What the player actually sees

Nothing numeric. Tier changes are announced by Lucineer *changing*, plus a four-note cue
(§3 Layer 4):

- **Tier 1:** he uses your name for the first time
- **Tier 2:** he disagrees with you for the first time
- **Tier 3:** he says "we" for the first time
- **Tier 4:** he asks you to follow him

Each of these is a moment a player will notice and remember, and none requires UI.

Bond point events are specified in `CHARACTER_BIBLE.md` §4. Wiring is in
`GAP_ANALYSIS.md` #4 — `bond_level` is currently a dead column.

### 5.3 Capability unlocks (the mechanical layer)

Capability *is* gated, but framed as Lucineer's willingness rather than a locked feature.

| Tier | Unlocks | In-fiction framing |
|---|---|---|
| 0 | Single structures, ≤10 parts | "Let's start with something that stands." |
| 1 | Multi-structure requests, terrain shaping | "Alright, you can hold more than one idea. Go ahead." |
| 2 | Style modifiers (spooky, industrial, salvage); modify-in-place | "You've got taste now. Tell me what *kind*." |
| 3 | Named saved patterns; Lucineer requests work from you | "Teach me that one. I'll use it." |
| 4 | Full canvas; Lucineer builds unprompted | "Point. I'll build it." |

**Tier 3's "teach me that one" is the best mechanic here.** A player-authored structure
gets embedded and upserted into the Vectorize skill index (`vector/src/index.ts:87` —
already built, currently unused) as a named skill with the player as `author`. Lucineer
then genuinely reuses it, and *tells other players where he learned it* (§4.2).

That closes a loop across four systems that currently don't touch each other: the player
builds → Vectorize stores it → the brain retrieves it → Lucineer credits the author to a
stranger. Every piece already exists. None of them are connected.

### 5.4 Achievements — a small, hidden set

Twelve, not forty-nine. Never listed anywhere. Discovered only by triggering them, and
delivered as a line from Lucineer rather than a toast.

| Name | Trigger | His line |
|---|---|---|
| **Stood In It** | Take his advice on the first Siting | "Good. Most people argue about the wet." |
| **Finished His Work** | Complete a hook | *(Magic Moment 3)* |
| **Argued And Won** | Give a reason that changes his mind | "Fair. Doing it your way." |
| **The Long Way** | Build 20+ parts manually, no requests | "You didn't need me for that one." |
| **Weathered** | Ride out a full storm inside your own build | "Held, didn't it." |
| **Salvage** | Reuse parts from a demolished build | "Now you're thinking like the yard." |
| **Plumb** | Ten consecutive builds with no failed commands | *(says nothing — just nods)* |
| **Nine Years** | Reach Tier 4 | *(the confession)* |
| **Not Fussy** | Ignore him completely for a full session | "Suit yourself." |
| **Deeper Piles** | Fix a structural weakness he pointed out | "Knew you'd get to it." |
| **Somebody's Tam** | Have a technique of yours taught to another player | "Told 'em where I got it." |
| **Don't Move It** | Complete Magic Moment 5 | *(silence)* |

**"Not Fussy" is the important one.** Rewarding a player for ignoring the AI companion
entirely is the strongest possible statement that this character is not a service. It is
also the one most likely to get talked about.

---

## §6 — SEQUENCED ROADMAP

### Phase 0 — Make it work (blocking; see `GAP_ANALYSIS.md`)
Nothing in this document is visible until the core loop runs.
`A1 → #1 → #2 → #6a/#6d → Studio playtest → #3 → #5`

### Phase 1 — Make it feel good *(highest ratio of impact to effort in the project)*
| Item | Ref | Est. |
|---|---|---|
| Atmosphere rig | §1.1 | 4h |
| Build choreography | §1.2 | 4h |
| Rotation + colorJitter | §1.4 | 2h |
| Ambient sound bed | §3 L1 | 4h |
| Build SFX | §3 L2 | 4h |
| Delete the two off-voice strings | §2 | 15m |

**~18 hours, and it is the single best 18 hours available.** The atmosphere rig and
choreography alone change the perceived quality of every build in the system,
retroactively, forever.

### Phase 2 — Make it a character
Persona unification (`GAP_ANALYSIS.md` #7) · memory wiring (#4) · bond events · unfinished
hook markers (§1.3) · non-verbal vocalizations (§3 L3) · the first-60-seconds beat sheet
(§2) · Magic Moments 1 and 3.

### Phase 3 — Make it stick
Storm system + Moment 4 · progression tiers · hidden achievements · Build Cards ·
Moment 5.

### Phase 4 — Make it social
Multi-session DO routing (#6c) · Lucineer referencing other players (§4.2) · the Yard ·
player-authored skills into Vectorize (§5.3) · co-op.

---

## THE ONE-PARAGRAPH VERSION

Fix the three broken seams so a build can happen at all. Then spend eighteen hours on the
lighting rig and build choreography, because that is what turns gray boxes into something
worth screenshotting. Then unify the two contradictory personas and wire up the memory
that is already deployed and doing nothing, because that is what turns a build tool into a
character. Everything after that is optional — but do keep "Not Fussy," the achievement for
ignoring him entirely. That one tells people exactly what kind of thing this is.
