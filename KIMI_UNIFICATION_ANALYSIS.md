# KIMI UNIFICATION ANALYSIS — Spatial Architect's Notes

> Source: [`UNIFICATION_VISION.md`](UNIFICATION_VISION.md) + [SuperInstance/snapkit-v2](https://github.com/SuperInstance/snapkit-v2) + [SuperInstance/tminus-ecosystem-review](https://github.com/SuperInstance/tminus-ecosystem-review)

The vision is clear: **T-Minus** gives Lucineer temporal awareness, **Tensor-MIDI** gives it spatial/harmonic coordination, and **Snapkit-v2** gives it cognitive self-monitoring. This doc answers three concrete questions with code patterns that could drop into the existing Slackwater stack.

---

## 1. Builds on an Eisenstein A₂ Hexagonal Lattice

### Current state

Today Lucineer builds at arbitrary `Vector3` coordinates. `BuildAnimator.lua` tweens parts into float positions, and `CommandExecutor` spawns parts wherever the model decides. There is no conservation law for placement — a spiral tower and a snapping dock can drift into one another, and the AI has no compact "address" for a build.

### Proposed change

Treat the horizontal build plane as the Eisenstein A₂ lattice. Every placement snaps to an Eisenstein integer `a + bω` where `ω = -½ + (√3/2)i`. The vertical axis stays an ordinary integer stud axis. A part's world address becomes:

```
address = (EisensteinInteger(a, b), y_studs)
```

This gives Slackwater three things it doesn't have today:

1. **Exact placement** — `eisenstein_snap_voronoi` returns the true nearest lattice point, not a rounded float.
2. **Spatial constraints as tokens** — `CleverToken` anchors build styles to lattice points; a "spiral tower" token means "allowed deviations within `snap_radius`".
3. **Natural zoning** — Voronoi cells around tokens become build regions; collisions reduce to lattice-cell occupancy.

### Code patterns

#### Python: wrap `snapkit.eisenstein` into a build lattice

```python
# lucineer_system/build_lattice.py
import math
from dataclasses import dataclass
from snapkit.eisenstein import EisensteinInteger, eisenstein_snap

SQRT3 = math.sqrt(3)
E1 = complex(1, 0)
E2 = complex(-0.5, SQRT3 / 2)  # ω

@dataclass(frozen=True, slots=True)
class BuildAddress:
    """World address: hex lattice (a,b) + vertical stud height."""
    a: int
    b: int
    y: int

    @property
    def world_x(self) -> float:
        return self.a - 0.5 * self.b

    @property
    def world_z(self) -> float:
        return self.b * (SQRT3 / 2)

class BuildLattice:
    """Snap arbitrary Roblox Vector3(x, y, z) to the A₂ lattice."""

    def __init__(self, stud_spacing: float = 4.0):
        self.stud_spacing = stud_spacing  # one lattice step in studs

    def snap(self, x: float, y: float, z: float, tolerance: float = 0.5):
        # Normalize world coords to the lattice basis scale
        z_norm = z / self.stud_spacing
        x_norm = x / self.stud_spacing
        z_lattice = 2.0 * z_norm / SQRT3
        a_float = x_norm + z_lattice * 0.5
        b_float = z_lattice

        # Use snapkit's true Voronoi snap
        ei, distance, is_snap = eisenstein_snap(complex(a_float, b_float), tolerance)
        y_studs = int(round(y / self.stud_spacing))

        return BuildAddress(ei.a, ei.b, y_studs), distance, is_snap

    def address_to_vector3(self, addr: BuildAddress):
        return (
            addr.world_x * self.stud_spacing,
            addr.y * self.stud_spacing,
            addr.world_z * self.stud_spacing,
        )
```

The `eisenstein_snap` call is the same primitive used by Snapkit's `TokenLattice` to snap behavioral states to constraint tokens ([`snapkit/eisenstein.py`](https://github.com/SuperInstance/snapkit-v2/blob/main/snapkit/eisenstein.py)).

#### Luau: port inside `CommandExecutor` / `BuildAnimator`

```lua
-- src/ReplicatedStorage/Lucineer/BuildLattice.lua
local BuildLattice = {}

local SQRT3 = math.sqrt(3)
local HALF_SQRT3 = SQRT3 * 0.5

function BuildLattice.snap(x: number, z: number, spacing: number)
    local zNorm = z / spacing
    local xNorm = x / spacing
    local bFloat = 2 * zNorm / SQRT3
    local aFloat = xNorm + bFloat * 0.5

    local a = math.round(aFloat)
    local b = math.round(bFloat)

    -- Voronoi refinement: check the 3x3 neighborhood for true nearest
    local bestA, bestB, bestDist = a, b, math.huge
    for da = -1, 1 do
        for db = -1, 1 do
            local ca, cb = a + da, b + db
            local wx = ca - cb * 0.5
            local wz = cb * HALF_SQRT3
            local dist = (xNorm - wx)^2 + (zNorm - wz)^2
            if dist < bestDist then
                bestDist = dist
                bestA, bestB = ca, cb
            end
        end
    end

    return {
        a = bestA,
        b = bestB,
        worldX = (bestA - bestB * 0.5) * spacing,
        worldZ = bestB * HALF_SQRT3 * spacing,
        residual = math.sqrt(bestDist) * spacing,
    }
end

return BuildLattice
```

Usage in `BuildAnimator.animatePart`:

```lua
local lattice = require(game.ReplicatedStorage.Lucineer.BuildLattice)
local snapped = lattice.snap(part.Position.X, part.Position.Z, 4.0)
part.Position = Vector3.new(snapped.worldX, part.Position.Y, snapped.worldZ)
```

#### Constraint tokens for build styles

Snapkit's `CleverToken` already maps `(entropy, hurst)` behavioral signatures to lattice points. The same mechanism can anchor build styles:

```python
from snapkit.clever_tokens import TokenLattice, ConstraintType

lattice = TokenLattice()
lattice.register_token(
    "build:spiral_tower",
    lattice_coord=(3, 1),
    constraint_type=ConstraintType.PERIODIC,
    snap_radius=0.3,
    expected_entropy=0.4,
    expected_hurst=0.6,
    metadata="Tower must grow in ring-1 hex neighbors each tier",
)

# In the prompt to Qwen3-Coder, inject the active constraint block:
system_prompt += lattice.render_prompt(["build:spiral_tower"])
```

This collapses the model's degrees of freedom: instead of asking "place a part anywhere," the prompt now says "choose one of the six ring-1 neighbors of the previous address." The lattice becomes the conservation law for builds.

### What changes

| Today | With A₂ lattice |
|-------|-----------------|
| `Vector3` floats | `BuildAddress(a, b, y)` |
| Collision via Region3 overlap | Collision via lattice-cell occupancy |
| Build style in prose prompt | Build style as anchored `CleverToken` |
| Drift allowed | `residual` and `snap_radius` enforce a hard boundary |
| Arbitrary curves | Sequences of lattice deltas (six primary directions) |

---

## 2. The 5-Model Brain Pipeline via Tensor-MIDI Events

### Current state

`cross_model_synthesis.py` and `roundtable.py` call the five models through DeepInfra/MiniMax chat completions and pass JSON/text back and forth. The coordination is sequential and textual. There is no shared clock and no compact binary bus.

### Proposed change

Replace the JSON message bus with [FluxTensorMIDI](https://github.com/SuperInstance/snapkit-v2/blob/main/snapkit/midi.py). Each model is a `Room` on its own MIDI channel. A "thought" becomes a `MIDIEvent`:

- `channel` = model id (0=Seed, 1=Hermes, 2=Qwen, 3=Gemini, 4=Nemotron/DeepSeek)
- `tick` = turn/step in the roundtable
- `note` = decision token or conclusion category
- `velocity` = confidence (0–127)
- `control_change` = metadata (cost, era, priority)

The roundtable conductor schedules events, renders a sorted score, and the aggregator decodes the score into the final synthesis.

### Code patterns

#### Python: `BrainConductor`

```python
# lucineer_system/brain_conductor.py
from dataclasses import dataclass
from snapkit.midi import FluxTensorMIDI, MIDIEventType, TempoMap

MODEL_CHANNELS = {
    "seed": 0,
    "hermes": 1,
    "qwen": 2,
    "gemini": 3,
    "nemotron": 4,
}

@dataclass(frozen=True)
class ModelSignal:
    model: str
    tick: int
    token_id: int       # mapped to MIDI note 0-127
    confidence: float   # 0.0-1.0, mapped to velocity
    cost_cents: int     # encoded as control_change value
    era: int = 0

class BrainConductor:
    """Run the 5-model roundtable as a Tensor-MIDI score."""

    def __init__(self, ticks_per_beat: int = 480, bpm: float = 120.0):
        self.flux = FluxTensorMIDI(TempoMap(ticks_per_beat, bpm))
        for name, ch in MODEL_CHANNELS.items():
            self.flux.add_room(name, channel=ch)

    def emit(self, signal: ModelSignal):
        note = max(0, min(127, signal.token_id))
        velocity = max(1, min(127, int(signal.confidence * 127)))

        self.flux.note_on(
            signal.model,
            tick=signal.tick,
            note=note,
            velocity=velocity,
        )

        # Metadata as control changes
        self.flux._events.append(MIDIEvent(
            tick=signal.tick,
            channel=MODEL_CHANNELS[signal.model],
            event_type=MIDIEventType.CONTROL_CHANGE,
            value=0,               # controller 0 = era
            velocity=max(0, min(127, signal.era)),
        ))

        self.flux._events.append(MIDIEvent(
            tick=signal.tick,
            channel=MODEL_CHANNELS[signal.model],
            event_type=MIDIEventType.CONTROL_CHANGE,
            value=1,               # controller 1 = cost bucket
            velocity=max(0, min(127, signal.cost_cents)),
        ))

    def render(self):
        return self.flux.render()

    def decode(self, events):
        by_model = {name: [] for name in MODEL_CHANNELS}
        for e in events:
            model = next(n for n, c in MODEL_CHANNELS.items() if c == e.channel)
            if e.event_type == MIDIEventType.NOTE_ON:
                by_model[model].append({
                    "tick": e.tick,
                    "token_id": e.value,
                    "confidence": e.velocity / 127.0,
                })
        return by_model
```

This mirrors Snapkit's own `FluxTensorMIDI` usage in `HarmonyGovernor`, where per-channel observations are encoded as `note_on` events with `note = sensor value` and `velocity = 1 - φ` ([`snapkit/governor.py`](https://github.com/SuperInstance/snapkit-v2/blob/main/snapkit/governor.py)).

#### Replacing the roundtable call site

Instead of this from `cross_model_synthesis.py`:

```python
r1a = di("nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B", system, user, ...)
```

The pipeline becomes:

```python
conductor = BrainConductor()

# Each model emits a signal at tick 0
for model_name, model_id in [("nemotron", "nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B"), ...]:
    response = di(model_id, system, user)          # still textual under the hood
    token_id = vocab.encode(response)              # compress to a vocabulary index
    confidence = estimate_confidence(response)
    conductor.emit(ModelSignal(
        model=model_name,
        tick=0,
        token_id=token_id,
        confidence=confidence,
        cost_cents=estimate_cost(response),
        era=current_era,
    ))

# The synthesis model reads the rendered score, not five walls of text
score = conductor.render()
synthesis = qwen_synthesizer.decode_score(score)
```

### What changes

| Today | With Tensor-MIDI |
|-------|------------------|
| JSON chat payloads | `MIDIEvent(tick, channel, note, velocity)` |
| Sequential model calls | Parallel "rooms" in a shared score |
| Confidence in prose | `velocity` normalized 0–127 |
| No shared time axis | `TempoMap` gives a global tick grid |
| Cost is after-the-fact | `CONTROL_CHANGE` embeds cost in the event |

### Caveat: the 7-bit bottleneck

MIDI notes and velocities are 7-bit. For a large decision vocabulary, map tokens to notes and use `PROGRAM_CHANGE` events to switch "banks" (one bank per conclusion type). Do not try to stuff raw token IDs > 127 into a single note.

---

## 3. Agents via T-Minus Predict-and-Confirm

### Current state

The perception system polls:

```lua
-- PerceptionSystem/init.lua
RunService.Heartbeat:Connect(function()
    local now = tick()
    local interval = (now - lastActiveCheck > 10) and 30 or 5
    if now % interval < 0.1 then
        sendPerceptionData(serializeGameState())
    end
end)
```

And `perception_agent.py` polls a queue:

```python
async def listen_for_perception_queue():
    while True:
        async with session.get(PERCEPTION_QUEUE_URL) as resp:
            if resp.status == 200:
                await process_perception_data(await resp.json())
            elif resp.status == 204:
                await asyncio.sleep(1)
```

Autonomous agents also run `while True` loops in `autonomous_agents.md`. Every tick is a poll.

### Proposed change

Adopt the T-Minus pattern from [tminus-music](https://github.com/SuperInstance/tminus-ecosystem-review/blob/main/tminus-music-DOCS.md) and [lau-tminus](https://github.com/SuperInstance/tminus-ecosystem-review/blob/main/lau-tminus-DOCS.md):

1. **Declare the future** — agent predicts an event (`player_will_need_hardwood_at_beat_64`).
2. **Subscribe once** — agent attaches a `PrecompiledScript` to the prediction.
3. **Shared clock** — `TickSchedule`/`TickClock` advances beats; BPM adapts to world energy.
4. **Confirm or miss** — when the actual event matches, the precompiled script executes with zero latency; on a miss, the prediction is discarded and confidence is penalized.

### Code patterns

#### Python: `TMinusAgent` inspired by lau-tminus

```python
# lucineer_system/tminus_agent.py
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional
import uuid

@dataclass
class PrecompiledScript:
    name: str
    action: Callable[[], None]
    energy_cost: float

@dataclass
class Prediction:
    id: str
    agent_id: str
    event_type: str
    predicted_beat: float
    confidence: float
    script: Optional[PrecompiledScript] = None
    confirmed: bool = False

class TMinusAgent:
    def __init__(self, agent_id: str, clock):
        self.agent_id = agent_id
        self.clock = clock
        self.predictions: List[Prediction] = []
        self.history: List[tuple] = []

    def predict(self, event_type: str, beats_ahead: float,
                confidence: float, script: Optional[PrecompiledScript] = None) -> str:
        pred = Prediction(
            id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            event_type=event_type,
            predicted_beat=self.clock.current_beat + beats_ahead,
            confidence=confidence,
            script=script,
        )
        self.predictions.append(pred)
        return pred.id

    def observe(self, actual_event: dict) -> List[PrecompiledScript]:
        """Returns scripts whose predictions matched the actual event."""
        executed = []
        for p in list(self.predictions):
            if self.matches(p, actual_event):
                p.confirmed = True
                if p.script:
                    executed.append(p.script)
                    p.script.action()
                self.history.append((p, True))
                self.predictions.remove(p)
            elif self.clock.current_beat > p.predicted_beat + 1:
                # Prediction window closed — miss
                self.history.append((p, False))
                self.learn_from_miss(p)
                self.predictions.remove(p)
        return executed

    def matches(self, prediction: Prediction, actual: dict) -> bool:
        # Fuzzy typed matching, e.g. "resource_need" with tolerance
        if prediction.event_type != actual.get("event_type"):
            return False
        beat_ok = abs(prediction.predicted_beat - actual.get("beat", 0)) <= 1.0
        return beat_ok

    def learn_from_miss(self, prediction: Prediction):
        # Penalize similar active predictions
        for p in self.predictions:
            if p.event_type == prediction.event_type:
                p.confidence *= 0.8
```

This is a direct port of the `TMinusEngine::predict → observe → execute` pipeline described in the lau-tminus docs.

#### Lua: replace polling heartbeat with a BPM clock

```lua
-- src/ServerScriptService/TMinusClock.lua
local TMinusClock = {}
TMinusClock.__index = TMinusClock

function TMinusClock.new(bpm: number, swing: number)
    local self = setmetatable({}, TMinusClock)
    self.bpm = bpm
    self.swing = math.clamp(swing, 0, 1)
    self.next_tick = 0
    self.current_beat = 0
    return self
end

function TMinusClock:tick_interval()
    return 60.0 / self.bpm
end

function TMinusClock:swing_offset(tick_id: number)
    if tick_id % 2 == 0 then
        return 0
    end
    return self:tick_interval() * self.swing * 0.33
end

function TMinusClock:next_tick()
    local id = self.next_tick
    local interval = self:tick_interval()
    local delta = interval + self:swing_offset(id)
    self.next_tick += 1
    self.current_beat += (1 / 4) -- assuming 4 ticks per beat
    return { id = id, delta = delta }
end

function TMinusClock:adapt(energy: number)
    -- tick-engine formula: factor = 1 + (energy - 0.5) * 0.4
    local factor = 1.0 + (math.clamp(energy, 0, 1) - 0.5) * 0.4
    self.bpm = math.clamp(self.bpm * factor, 30, 300)
end

return TMinusClock
```

Usage in the agent runtime:

```lua
local clock = TMinusClock.new(120, 0.2)
local lastTick = tick()

RunService.Heartbeat:Connect(function()
    local now = tick()
    if now - lastTick >= clock:tick_interval() + clock:swing_offset(clock.next_tick) then
        lastTick = now
        local t = clock:next_tick()
        agent:advance(t.delta)

        -- Adapt BPM to world energy (active builds, agent count, etc.)
        local energy = WorldScanner:get_energy_signal()
        clock:adapt(energy)
    end
end)
```

This matches the `tick-engine` design: `TickSchedule.next_tick()` returns ticks, `Tempo.adapt(energy)` scales BPM, and swing adds off-beat delay ([tick-engine docs](https://github.com/SuperInstance/tminus-ecosystem-review/blob/main/tick-engine-DOCS.md)).

#### Concrete example: resource prefetch

Instead of polling "does the player need hardwood?" every 5 seconds:

```python
agent.predict(
    event_type="player_will_need_hardwood",
    beats_ahead=16.0,
    confidence=0.75,
    script=PrecompiledScript(
        name="fetch_hardwood",
        action=lambda: fleet.send("Earl", "deliver", "hardwood", 20),
        energy_cost=0.3,
    ),
)
```

When the player actually opens the build menu and selects a hardwood recipe at the predicted beat, `agent.observe({"event_type": "player_will_need_hardwood", "beat": 64.1})` fires the precompiled script instantly. No polling.

### What changes

| Today | With T-Minus |
|-------|--------------|
| `while True` + `asyncio.sleep(1)` | `TickClock.next_tick()` |
| Query state every 5–30 s | Predict once, confirm once |
| Reaction latency = poll interval | Reaction latency = 0 on match |
| Fixed cadence | BPM adapts to world energy |
| No accuracy metric | `accuracy()` over sliding window |

The tminus-music docs note this is roughly **10× fewer messages** than polling for the same coverage.

---

## 4. The Unified Substrate (All Three Together)

When the three changes are combined, Slackwater stops being a game with AI helpers and becomes a **musical-spatial-temporal organism**:

1. A player places a foundation → `BuildLattice.snap` turns it into an Eisenstein address.
2. The build address emits a `MIDIEvent` on the "build" channel with the lattice encoded in control changes.
3. Agents predict the next build event (`foundation_complete_at_beat_32`).
4. At `t-minus-0`, the predicted beat arrives; if the foundation is complete, the agent confirms and executes a precompiled script (e.g., Lucineer starts the next tier).
5. If the build drifts off-lattice or the agent misses its prediction, `HarmonyGovernor` measures friction Φ and wakes `ExecutiveAgent` to rekey, rewire, or inject novelty.

### Mini integration sketch

```python
from snapkit.governor import HarmonyGovernor
from snapkit.midi import FluxTensorMIDI
from lucineer_system.build_lattice import BuildLattice
from lucineer_system.tminus_agent import TMinusAgent

lattice = BuildLattice(stud_spacing=4.0)
flux = FluxTensorMIDI()
flux.add_room("build", channel=0)
flux.add_room("agent_earl", channel=1)

governor = HarmonyGovernor(beat_period=1.0)
governor.register_channel("build", channel=0, deadband=1.5)

agent = TMinusAgent("Earl", clock)

# Player builds at a world position
addr, distance, is_snap = lattice.snap(x, y, z, tolerance=0.5)
flux.note_on("build", tick=clock.current_beat,
             note=addr.a + 64, velocity=127 - int(distance * 50))

# Earl predicts the next resource need
agent.predict("need_hardwood", beats_ahead=8, confidence=0.8,
              script=PrecompiledScript("fetch_hardwood", ...))

# Governor watches build friction
phi = governor.record_observation("build",
    prediction=lattice_expected_distance,
    actual=distance)
if phi > governor.channel_state("build").deadband:
    executive.handle_alarms()
```

---

## 5. Risks and First Steps

| Risk | Mitigation |
|------|------------|
| Players lose free-form placement | Make snapping optional in creative mode; enforce only in structured builds |
| MIDI 7-bit limit | Use `PROGRAM_CHANGE` banks and controller pairs for larger vocabularies |
| Prediction misses feel worse than polling | Keep a slow fallback poll (e.g., every 8 beats) as a safety net |
| Clock desync across distributed workers | Use `TempoMap` as authoritative server clock; clients interpolate |
| Eisenstein exact arithmetic cost | It's integer math plus one sqrt per snap; negligible vs. LLM latency |

### Suggested first commit

1. Port `eisenstein_snap_voronoi` to a Luau module and snap the first build template (e.g., `tower`) to the lattice.
2. Add a `BrainConductor` that logs the roundtable as MIDI to `/tmp/lucineer_brain.mid` for inspection.
3. Replace one polling agent (Earl's resource monitor) with a `TMinusAgent` and measure message count.

---

*"The hull sets the beat. The agents sync to the ocean."*
