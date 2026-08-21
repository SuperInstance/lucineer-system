# NEMOTRON UNIFICATION ANALYSIS
## T-Minus × Tensor-MIDI × Snapkit × Lucineer/Slackwater
### A Systems Architecture Report

*Prepared: 2026-08-02*
*Sources: SuperInstance ecosystem repos, Slackwater Master Architecture v2, FABLE Agent UX, AI-Writings on Tempo & Counterpoint*

---

## EXECUTIVE SUMMARY

Three ecosystem clusters from the SuperInstance org — T-Minus (temporal coordination), Tensor-MIDI/Flux (spatial-harmonic representation), and Snapkit-v2 (cognitive adaptation via FEP) — each solve a problem Slackwater's current architecture handles poorly. This document analyzes how to fuse them into the Lucineer build pipeline as a unified substrate, not a feature layer.

The current architecture is: Roblox client polls a Cloudflare Worker every 0.5s for job status. Five AI models communicate via JSON payloads. Agent positions are arbitrary Vector3 coordinates. Cognitive adaptation is hardcoded if/else logic. This works. It is also a metronome playing a piece that needs rubato.

---

## 1. REPLACING POLLING WITH T-MINUS PREDICT-AND-CONFIRM

### 1.1 The Current Polling Architecture

The Roblox client currently executes:

```lua
-- Current: Heartbeat-based polling (every 0.5s)
task.spawn(function()
    while job do
        local response = HttpService:GetAsync(
            "https://lucineer-relay.casey-digennaro.workers.dev/api/job/" .. job.id
        )
        if response.status == "complete" then
            executeBuild(response.commands)
            break
        end
        task.wait(0.5)
    end
end)
```

This generates **~120 HTTP requests per minute** for a single build job. For a 60-second deep pipeline run (5-model path), that's ~120 requests that each return `{"status": "pending"}`. The Worker serves these from D1, doing nothing but checking a flag 120 times. Multiply by N concurrent players and the relay becomes a polling server, not a build server.

### 1.2 The T-Minus Paradigm

From `tminus-ecosystem-review/SYNTHESIS.md`, the predict-and-confirm cycle is:

```
1. Declare the FUTURE (a countdown event with predicted completion)
2. Subscribe agents confirm readiness → quorum fires
3. Time elapses via a SHARED CLOCK
4. Predictions match → precompiled script EXECUTES
5. Predictions miss → script is discarded, agent re-plans
```

From `tminus-music`, the key primitives:
- `TMinusPredictor::predict_next()` — returns the next predicted event
- `TMinusPredictor::confirm(id)` — subscribe-once confirmation, fires exactly once
- `MessageSavings` — proves ~10× fewer messages than polling

From `lau-tminus`:
- `PrecompiledScript` — the build command stream is attached to the prediction. When the prediction fires, the script is ready for zero-latency execution
- `TMinusEngine` — `predict() → observe() → execute()` cycle
- `TMinusSummary` — tracks accuracy, avg lead time, scripts ready

### 1.3 The Redesigned Architecture

**Worker-side (Cloudflare Durable Object per world instance):**

```typescript
// Durable Object: BuildCoordinator
export class BuildCoordinator {
  constructor(state: DurableObjectState) {
    this.state = state;
    this.sessions = new Map(); // sessionId → WebSocket
    this.predictions = new Map(); // jobId → Prediction
  }

  async createJob(buildRequest): Promise<Job> {
    const job = await this.runPipeline(buildRequest);
    
    // T-Minus: register a prediction for job completion
    const prediction = {
      id: job.id,
      predictedBeat: this.estimateCompletion(job), // e.g., beat 120 at current BPM
      script: null,  // will be populated when pipeline completes
      subscribers: new Set<string>(), // sessionIds
    };
    this.predictions.set(job.id, prediction);
    
    return job;
  }

  async onPipelineComplete(jobId: string, commands: BuildCommand[]) {
    const prediction = this.predictions.get(jobId);
    if (!prediction) return;

    // Attach the precompiled script
    prediction.script = commands;
    
    // T-Minus confirm: fire exactly once to all subscribers
    for (const sessionId of prediction.subscribers) {
      const ws = this.sessions.get(sessionId);
      if (ws) {
        ws.send(JSON.stringify({
          type: 't-minus.confirm',
          jobId,
          accuracy: this.computeAccuracy(prediction),
          script: commands,  // PrecompiledScript — zero-latency execution
        }));
      }
    }
    
    // Record accuracy for future prediction calibration
    this.recordAccuracy(prediction);
  }
}
```

**Roblox client (subscribe-once, fire-once):**

```lua
-- T-Minus: subscribe once, get notified once
local function requestBuild(intent: string)
    -- Open WebSocket to Durable Object
    local ws = WebSocket.connect(relayUrl .. "/ws")
    
    -- Single subscription message
    ws:send({
        type = "t-minus.subscribe",
        jobId = jobId,
    })
    
    -- One callback fires exactly once when the job completes
    ws.onMessage = function(message)
        local data = HttpService:JSONDecode(message)
        if data.type == "t-minus.confirm" then
            -- PrecompiledScript arrives ready to execute
            -- No polling. No 120 requests. One message.
            executeBuild(data.script)
            
            -- The accuracy metric tells us how good the prediction was
            -- (used to calibrate future tempo estimates)
            print("Prediction accuracy:", data.accuracy)
        elseif data.type == "t-minus.miss" then
            -- Prediction missed — the pipeline took longer than expected
            -- Client shows diegetic "he's still thinking" animation
            -- A NEW prediction is issued automatically
            showThinkingAnimation()
        end
    end
end
```

### 1.4 Message Economics

| Metric | Polling (current) | T-Minus |
|--------|-------------------|---------|
| Messages per 60s job | ~120 GET requests | 1 subscribe + 1 confirm = 2 |
| Worker CPU per pending job | 120 D1 reads | 0 (state held in DO memory) |
| Client-side complexity | while-loop + retry logic | Single callback |
| Error recovery | Timeout-based | Prediction-miss → re-predict |
| Build latency | RTT of final poll | Zero (script pre-compiled, fires on confirm) |

### 1.5 Diegetic Integration (from FABLE_AGENT_UX §5)

T-Minus predictions map directly to the "latency is his body" principle. When the client subscribes, it also receives a **predicted completion beat**. The client uses this to time Lucineer's thinking animations:

- **Prediction registered** → Lucineer walks to the bench, pulls chalk (0-2s)
- **Beat 1-4** → Rough sketch on the bench (2-8s)
- **Beat 5-8** → Pulls stock, measures (8-16s)
- **Prediction confirm** → Chalk line finalizes, build stream begins

If the prediction misses (pipeline slower than expected), the diegetic behavior extends naturally — he measures twice, sends you for cedar. The **T-Minus miss is invisible to the player** because the animation system was already designed for variable latency.

### 1.6 The Tempo Map Integration

From "The Tempo Map of Computation" — the current system is a flat metronome: every poll is identical, every wait is the same experience. T-Minus gives us a **composed tempo map**:

- **Job created** → Largo (cold start, the agent is thinking)
- **Pipeline stage 1 complete** → Moderato (templates matched, stock pulled)
- **Deep path running** → Adagio (comprehensive, deliberate)
- **Prediction confirmed** → Allegro (the build streams, things happen fast)
- **Player in creative mode** → Rubato (system follows player's tempo)

The `TempoMap` / `EnsembleTempo` from `t-minus-rs` maps directly to this. The `TickClock` from `tick-engine` with BPM-driven cadence and swing provides the implementation.

---

## 2. TENSOR-MIDI AS AGENT COMMUNICATION PROTOCOL

### 2.1 The Current JSON Protocol

The 5-model pipeline currently communicates via structured JSON:

```json
{
  "stage": "spatial_decomposition",
  "model": "qwen3.6-35b",
  "output": {
    "buildCommands": [
      {"type": "place", "part": "wall_panel", "pos": [12, 0, 4]},
      {"type": "weld", "from": "wall_panel_1", "to": "frame_post_a"}
    ]
  },
  "nextStage": "code_generation"
}
```

This is readable, debuggable, and **bandwidth-inefficient at scale**. More critically, it loses the temporal character of the pipeline. Each stage is a discrete event — there's no way to express that two models are "in harmony" or that one model's output "resolves the dissonance" of another's.

### 2.2 The Tensor-MIDI Representation

From `flux-tensor-midi`, a MIDI event is a 4-dimensional tensor:

```
Dimension 0: Pitch (action type / hardware domain)
Dimension 1: Velocity (confidence / prediction entropy, 0-127 INT8)
Dimension 2: Time (beat position on the BeatGrid)
Dimension 3: Channel (agent identity, 0-15)
```

From `snapkit-v2`'s Architecture of Harmony §IV, the mapping is:

| MIDI Concept | Agent Pipeline Mapping |
|---|---|
| Clock | Pipeline heartbeat. Every model must output decisions on beat. |
| Note On/Off | A model's output or decision. Duration = processing time. |
| Pitch | Action type: 60 = place_part, 62 = weld, 64 = paint, etc. (General MIDI-inspired) |
| Velocity | Model confidence (0-127). High velocity = low entropy = harmony. |
| Control Change | Continuous parameters: position, rotation, material properties |
| Program Change | Pipeline stage shift (Seed-mini → Qwen3.6 → Qwen3-Coder) |
| Channel | Model identity: 0 = Seed-mini, 1 = Qwen3.6, 2 = Qwen3-Coder, 3 = Hermes, 4 = Nemotron |

### 2.3 The Pipeline as a Score

Each build becomes a **musical composition**:

```
Beat 1  ── Channel 0 (Seed-mini): Note On, pitch=72 (intent_parse), vel=110 (high confidence)
           │  [Seed-mini outputs the parsed intent as a MIDI note]
           ▼
Beat 4  ── Channel 1 (Qwen3.6): Note On, pitch=60 (spatial_plan), vel=95
           │  [Qwen3.6 outputs the spatial decomposition as a chord]
           ├── Channel 1: Note On, pitch=64 (place_beam), vel=100
           ├── Channel 1: Note On, pitch=66 (place_post), vel=88
           ▼
Beat 8  ── Channel 2 (Qwen3-Coder): Note On, pitch=48 (code_gen), vel=120
           │  [Coder outputs build commands — a chord of placed parts]
           ├── Channel 2: Note On, pitch=60 (place_wall), vel=92
           ├── Channel 2: Note On, pitch=62 (place_roof), vel=85
           ▼
Beat 12 ── Channel 3 (Hermes): Note On, pitch=80 (personality_wrap), vel=105
           │  [Hermes wraps the build in Lucineer's voice]
           ▼
Beat 14 ── ALL CHANNELS: Note Off (cadence — pipeline complete)
```

### 2.4 Technical Implementation

**On the Worker (pipeline orchestration):**

```typescript
interface MIDINote {
  pitch: number;      // 0-127: action type
  velocity: number;   // 0-127: model confidence (inverse of entropy)
  beat: number;       // position on BeatGrid
  duration: number;   // beats
  channel: number;    // 0-15: model identity
}

class TensorMIDIPipeline {
  // Each model's output is encoded as MIDI notes
  encodeModelOutput(model: string, output: any): MIDINote[] {
    const channel = MODEL_CHANNELS[model]; // e.g., seed-mini → 0
    return output.commands.map(cmd => ({
      pitch: ACTION_PITCHES[cmd.type],     // place → 60, weld → 62
      velocity: this.confidenceToVelocity(output.confidence),
      beat: this.currentBeat,
      duration: 1, // default quarter note
      channel,
    }));
  }
  
  // The entire pipeline state is the current chord across all channels
  getCurrentChord(): MIDINote[] {
    return Array.from(this.activeNotes.values());
  }
  
  // Bandwidth: entire pipeline state in ~200 bytes of MIDI hex
  // vs ~5KB+ of JSON
  serializeState(): string {
    return this.getCurrentChord()
      .map(n => `${n.channel.toString(16)}${n.pitch.toString(16)}${n.velocity.toString(16)}`)
      .join('');
  }
}
```

**On the Roblox client (audible build stream):**

The build commands arrive as a MIDI stream. Each note's pitch maps to a build action, and each note triggers the corresponding sound + animation:

```lua
-- Each build command is a MIDI note
local function executeMIDIBuild(notes: {MIDINote})
    for _, note in notes do
        -- Pitch determines the action
        local action = PITCH_TO_ACTION[note.pitch]  -- 60 → place, 62 → weld
        
        -- Velocity determines animation intensity
        local intensity = note.velocity / 127
        
        -- Channel determines which agent performs it
        local agent = CHANNEL_TO_AGENT[note.channel]
        
        -- The note's beat position schedules the action in the build sequence
        task.delay(note.beat * BEAT_DURATION, function()
            agent:performAction(action, note.data, intensity)
            -- The sound for this action IS the note
            SoundService:PlayNote(note.pitch, note.velocity, note.channel)
        end)
    end
end
```

### 2.5 Why This Matters: The Audible Pipeline

From "The Counterpoint of Agents" — the quality of multi-agent work is recognizable by texture. When the pipeline runs, the player **hears** it:

- **First species (note against note):** Seed-mini's intent parse (single high note) answered by Qwen3.6's spatial plan (a chord). Simple counterpoint.
- **Fourth species (suspensions):** Qwen3-Coder holds the previous context while Hermes pushes forward into personality wrapping. The dissonance of raw code resolving into character voice.
- **Cadence:** All channels reach Note Off. The build is done. Silence is the cadence.

This is not decoration. It is **the record needle insight from snapkit-v2 §IV**: agents don't read the past, they listen to the present. A debugging developer can route the MIDI stream into a synthesizer and **hear** when the pipeline breaks — dissonance is immediately audible in a way that JSON logs are not.

### 2.6 Bandwidth Comparison

| Encoding | Size per build command | 100-command build |
|----------|----------------------|-------------------|
| JSON (current) | ~120 bytes | ~12 KB |
| Tensor-MIDI (INT8) | 4 bytes (chan, pitch, vel, beat) | ~400 bytes |
| Compression ratio | — | **30×** |

---

## 3. SNAPKIT'S TRIADIC ARCHITECTURE MAPPED TO GAME AGENTS

### 3.1 The Three Layers

From `snapkit-v2/docs/ARCHITECTURE_OF_HARMONY.md`:

| Snapkit Layer | Function | Slackwater Mapping |
|---|---|---|
| Layer 1: Sandbox | Forward simulation, hypothesis testing | **Agent tries a build virtually** in a headless Roblox instance |
| Layer 2: Harmony Governor | Measures cognitive friction (Φ), triggers Executive | **Measures player friction** — is the player confused, frustrated, delighted? |
| Layer 3: Executive | Improvises when friction exceeds deadband | **Agent improvises** — changes approach, offers help, switches to Plan B |

### 3.2 Layer 1: The Build Sandbox

In snapkit, the `HypothesisSandbox` runs a forward simulation: *"If I apply action X, sensor Y should read Z next beat."* The simulation is scored against reality.

**Slackwater mapping:** Before an agent commits to a build plan, it runs the plan through a **headless validation sandbox**:

```python
class BuildSandbox(HypothesisSandbox):
    """Layer 1: Test build plans before committing."""
    
    def evaluate(self, build_commands: list, world_state: dict) -> SandboxScore:
        """
        Run build commands in a headless simulation.
        Returns: collision detection, structural integrity, era-appropriateness.
        """
        results = []
        for cmd in build_commands:
            # Simulate the placement
            predicted_state = self.simulate_placement(cmd, world_state)
            
            # Check: does this part overlap existing geometry?
            collision = self.check_collision(predicted_state, world_state)
            
            # Check: is this structurally sound? (simple physics)
            stable = self.check_stability(predicted_state, world_state)
            
            # Check: era-appropriate? (Era 2 gear in Era 1 = invalid)
            valid = self.check_era_gate(cmd, world_state['era'])
            
            results.append(SandboxResult(
                action=cmd,
                collision=collision,
                stable=stable,
                valid=valid,
            ))
        
        # óthismos score: how much constraint pressure did this plan generate?
        return self.score(results)
```

This runs server-side as part of the pipeline, between Qwen3.6's spatial decomposition and Qwen3-Coder's command generation. The sandbox catches the "door doesn't fit the arch" error (FABLE Vignette V5 — The Misread) **before** it reaches the client, OR — if we want Lucineer to be fallible — it can be configured to let certain classes of misreads through at a tuned rate, because misreads are characterization.

### 3.3 Layer 2: The Harmony Governor (Player Friction Monitoring)

In snapkit, the `HarmonyGovernor` computes:

```
Φ(t) = α · H(P(x|context)) + β · L_inference + γ · Δconnectome
```

**Slackwater mapping:** Φ becomes a **player friction metric**:

```python
class PlayerFrictionGovernor:
    """Layer 2: Is the player in flow, or struggling?"""
    
    def compute_friction(self, player_state: dict) -> float:
        """
        Φ = α·(action_entropy) + β·(idle_time) + γ·(error_rate) + δ·(help_requests)
        
        Low Φ = player is in flow (building confidently, low hesitation)
        High Φ = player is struggling (repeated failures, long pauses, rage-quits)
        """
        entropy = self.action_entropy(player_state['recent_actions'])
        idle = self.normalized_idle_time(player_state['last_input_time'])
        errors = self.error_rate(player_state['failed_placements'])
        help_requests = len(player_state['help_requests'])
        
        phi = (
            0.35 * entropy +
            0.25 * idle +
            0.30 * errors +
            0.10 * help_requests
        )
        
        return phi
    
    def check_deadband(self, phi: float, player_stage: int) -> bool:
        """
        Stage-dependent deadband. Stage 1 players have wide deadband
        (they're learning, friction is expected). Stage 3+ players have
        narrow deadband (they know what they're doing, friction means
        something is wrong).
        """
        deadband = DEADBAND_BY_STAGE[player_stage]  # e.g., [2.0, 1.5, 1.0, 0.7, 0.5]
        return phi > deadband
```

**Diegetic friction signals** (from FABLE_AGENT_UX — the system never surfaces a "frustration meter"):

- Player places 3 parts, removes 2, places the same 3 differently → entropy spike
- Player hasn't input for 45 seconds while near an unfinished build → idle spike
- Player drops salvage near Lucineer and points at the build → help request (encoded as a Friction-decreasing action, because the player is using the "start it" channel)

### 3.4 Layer 3: The Executive (Agent Improvisation)

When the Governor fires (Φ > deadband), the Executive wakes. In snapkit, it can: rewrite constraints, cross-wire I/O, alter objectives, inject novelty.

**Slackwater mapping:**

```python
class AgentExecutive:
    """Layer 3: Lucineer improvises when the player struggles."""
    
    def handle_alarm(self, phi: float, player_state: dict) -> Improvisation:
        """
        The agent reads the friction signal and improvises a response.
        This replaces hardcoded if/else with FEP-driven adaptation.
        """
        if player_state.stage == 1 and phi > 1.8:
            # Stage 1, high friction: simplify the task
            # FABLE V1: "You'll get the boot room today"
            return Improvisation(
                action="simplify_build",
                dialogue="Tell you what — leave the big piece for now. \
                          Show me where the foundation goes.",
                constraint_rewrite={"max_parts": 3, "era_unlock": "preview"},
            )
        
        elif player_state.stage == 3 and phi > 0.7:
            # Stage 3, moderate friction: offer specific help
            # FABLE V4: "Ridge cap's still wrong. We'll fix it Tuesday."
            return Improvisation(
                action="offer_targeted_help",
                dialogue="That post wants to be two inches starboard. \
                          I'll hold it if you set the base.",
                constraint_rewrite={"assist_level": "physical"},
            )
        
        elif player_state.repeated_failures > 5:
            # Cascading failure: stop and reset context
            # FABLE V5: "Give me a minute. I'll sort it."
            return Improvisation(
                action="take_over_temporarily",
                dialogue="Give me a minute. I'll sort it.",
                constraint_rewrite={"agent_takes_lead": True},
                # Novelty injection: break the degenerative loop
                novelty="introduce_new_material",
            )
        
        else:
            # Φ is within deadband — do nothing
            # The most important case: the agent stays quiet
            return Improvisation(action="none")
```

### 3.5 The Connectome: Cross-Agent Coupling

From snapkit's `connectome.py` — detects when agents that should be coupled become decoupled. In Slackwater, this maps to **agent-to-agent relationships**:

- **Lucineer + Earl coupled:** when they're arguing about the same build (Three-Meter War vignette), their dialogue references each other. Coupling = high.
- **Lucineer + Earl decoupled:** if Lucineer hasn't mentioned Earl in 3 sessions, the connectome shows drift. The Executive can improvise: Earl shows up on a boardwalk round, references a past build.
- **Player as coupling bridge:** from FABLE_AGENT_UX §2, the player is the only edge that moves between agents. The connectome detects when the player has been spending all their time with one agent and neglecting others — and the Executive improvises (Earl assigns an Item that routes the player to Bea).

---

## 4. THE EISENSTEIN A₂ LATTICE FOR BUILD PLACEMENT

### 4.1 What Is the Eisenstein Lattice?

From `snapkit-v2/eisenstein.py` and `constraint-theory-math`:

The Eisenstein A₂ lattice is the densest packing of circles in 2D. Points are at positions:

```
ω = e^(2πi/3) = -1/2 + i√3/2
Lattice points: z = a + bω  where a, b ∈ ℤ
```

In Cartesian coordinates:
```
x = a + b·(-1/2) = a - b/2
y = b·(√3/2)
```

Each lattice point has **6 equidistant neighbors** (hexagonal coordination), compared to the square lattice's 4. The Voronoï cell is a regular hexagon.

### 4.2 Snap-to-Lattice Build Placement

Currently, build placement in Slackwater uses arbitrary floating-point coordinates. This causes:
- Misaligned parts (the "four centimeters off" from FABLE V5)
- Visual jitter when parts nearly-touch but don't quite
- No mathematical guarantee of spacing regularity

**Eisenstein snapping forces every placement to the nearest lattice point:**

```lua
-- Roblox client: snap placement to Eisenstein A₂ lattice
local LATTICE_SCALE = 4 -- studs per lattice unit

local function eisensteinSnap(worldPos: Vector3): Vector3
    -- Convert to Eisenstein coordinates
    local a = worldPos.X / LATTICE_SCALE
    local b = worldPos.Z / (LATTICE_SCALE * math.sqrt(3) / 2)
    
    -- Round to nearest integers (snap)
    local aRounded = math.round(a)
    local bRounded = math.round(b)
    
    -- Convert back to Cartesian
    local x = aRounded + bRounded * (-0.5)
    local z = bRounded * (math.sqrt(3) / 2)
    
    -- Y stays continuous (vertical is not snapped — terrain is irregular)
    return Vector3.new(
        x * LATTICE_SCALE,
        worldPos.Y,
        z * LATTICE_SCALE
    )
end
```

### 4.3 What This Means Visually

**Every placed part aligns to a hexagonal grid.** The visual consequences:

1. **Hexagonal architecture.** Buildings naturally take on honeycomb-inspired forms. Walls meet at 60° and 120°, not just 90°. This is the architecture of tidal communities — fish traps, breakwaters, and net pens are all hexagonal-ish because the water doesn't care about right angles.

2. **Implied construction lines.** When parts snap to the lattice, the underlying grid becomes visible through the build itself. Players discover that certain placements "work" and others don't — the lattice teaches its own geometry, the same way Minecraft's block grid teaches cubic thinking.

3. **Tidal resonance.** A hexagonal grid is the 2D projection of a close-packed arrangement — the same packing that water molecules adopt in ice, that basalt columns form at Giant's Causeway. A tidal world built on Eisenstein coordinates **looks like it grew there**, not like it was plotted.

### 4.4 What This Means Mathematically

1. **Guaranteed minimum spacing.** Every two distinct lattice points are at least `LATTICE_SCALE` apart. No two parts can be placed "too close" — the lattice prevents it.

2. **Isotropic error.** The hexagonal Voronoï cell has equal error in all directions. Square-grid snapping has 41% more error in diagonal directions. Eisenstein snapping is equally fair in all directions.

3. **Eisenstein integer arithmetic.** All build coordinates are Eisenstein integers `a + bω`. This enables exact arithmetic (no floating point drift), which means the `flux-tensor-midi` INT8 saturation and the `constraint-theory-core` exact bounds checking work directly on build coordinates.

4. **Connection to snapkit clever tokens.** From the Architecture of Harmony §V: "An agent's operational space is defined as a region in the Eisenstein lattice." Each agent's build territory is a set of lattice points. Territory boundaries are Voronoï cells. The lattice gives us mathematically exact, visually meaningful borders.

### 4.5 Implementation in the Build Pipeline

```python
# Pipeline stage: post-processing Qwen3-Coder output
def snap_build_commands(commands: list[BuildCommand], scale: float = 4.0) -> list[BuildCommand]:
    """
    Snap every build command's position to the nearest Eisenstein A₂ lattice point.
    """
    for cmd in commands:
        if cmd.type in ("place", "weld"):
            # Snap XZ to Eisenstein lattice
            a = cmd.pos[0] / scale
            b = cmd.pos[2] / (scale * math.sqrt(3) / 2)
            a_r = round(a)
            b_r = round(b)
            cmd.pos[0] = (a_r - b_r / 2) * scale
            cmd.pos[2] = b_r * scale * math.sqrt(3) / 2
            
            # Snap rotation to 60° increments (hexagonal symmetry)
            if hasattr(cmd, 'rotation'):
                cmd.rotation = round(cmd.rotation / 60) * 60
    
    return commands
```

---

## 5. THE UNIFIED FRAMEWORK: `swarm-tminus-lucineer`

### 5.1 Overview

A single Python package that combines:
- **Temporal prediction** (t-minus) — when builds will complete, when to notify
- **Spatial harmony** (fleet-jepa-midi) — how agents communicate, how builds are positioned
- **Cognitive adaptation** (snapkit) — how agents respond to player friction
- **Creative generation** (Lucineer pipeline) — the 5-model build system

### 5.2 Package Structure

```
swarm_tminus_lucineer/
├── __init__.py
├── tempo/                    # T-Minus temporal layer
│   ├── predictor.py          # TMinusPredictor: predict build completion beats
│   ├── countdown.py          # CountdownEvent with quorum firing
│   ├── deadline_tree.py      # Hierarchical deadlines with cascade-cancel
│   ├── cron_parser.py        # Cron scheduling for recurring events
│   └── tempo_map.py          # Composed tempo map (Largo → Moderato → Allegro)
├── spatial/                  # Tensor-MIDI spatial layer
│   ├── tensor_midi.py        # 4D tensor MIDI encoding (pitch/vel/beat/channel)
│   ├── eisenstein.py         # A₂ lattice snap for build coordinates
│   ├── beatgrid.py           # System clock with BPM and swing
│   └── counterpoint.py       # Species counterpoint constraints for agent dialogue
├── cognitive/                # Snapkit cognitive layer
│   ├── sandbox.py            # Layer 1: Forward build simulation
│   ├── governor.py           # Layer 2: Player friction monitoring (Φ)
│   ├── executive.py          # Layer 3: Agent improvisation
│   ├── connectome.py         # Cross-agent coupling detection
│   └── clever_tokens.py      # Eisenstein-anchored constraint tokens
├── pipeline/                 # Lucineer creative layer
│   ├── router.py             # Model routing (Seed-mini → Qwen3.6 → ...)
│   ├── build_planner.py      # Construction-order sort + Eisenstein snap
│   ├── agent_voice.py        # Hermes personality wrapping
│   └── skill_recall.py       # Vectorize skill search
├── integration/
│   ├── worker_do.py          # Cloudflare Durable Object WebSocket bridge
│   ├── roblox_client.py      # Lua codegen for client-side subscribe
│   └── audible_pipeline.py   # Route tensor-MIDI to Roblox sound service
├── tests/
│   ├── test_predictor.py
│   ├── test_eisenstein.py
│   ├── test_governor.py
│   ├── test_tensor_midi.py
│   ├── test_sandbox.py
│   ├── test_build_planner.py
│   └── test_integration.py
└── pyproject.toml
```

### 5.3 The Core Loop

```python
from swarm_tminus_lucineer import (
    # Temporal
    Predictor, CountdownEvent, TempoMap,
    # Spatial
    TensorMIDI, EisensteinSnap, BeatGrid,
    # Cognitive
    BuildSandbox, PlayerFrictionGovernor, AgentExecutive,
    # Pipeline
    ModelRouter, BuildPlanner, SkillRecall,
)

class LucineerAgentSystem:
    """
    The unified agent system. One object that coordinates
    temporal prediction, spatial harmony, cognitive adaptation,
    and creative generation for a single world instance.
    """
    
    def __init__(self, world_id: str, era: int):
        self.world_id = world_id
        self.era = era
        
        # Layer: Temporal (T-Minus)
        self.tempo = TempoMap(
            initial_bpm=60,  # 1 beat/sec — Largo for cold starts
            stages={
                "cold_start": 40,    # Largo
                "template_match": 80, # Moderato
                "deep_pipeline": 50,  # Adagio
                "build_stream": 120,  # Allegro
                "creative_mode": 70,  # Rubato (player-led)
            }
        )
        self.predictor = Predictor(tempo=self.tempo)
        
        # Layer: Spatial (Tensor-MIDI)
        self.beatgrid = BeatGrid(bpm=self.tempo.current_bpm)
        self.midi_bus = TensorMIDI(channels=5)  # 5 models
        self.lattice = EisensteinSnap(scale=4.0)
        
        # Layer: Cognitive (Snapkit)
        self.sandbox = BuildSandbox()
        self.governor = PlayerFrictionGovernor()
        self.executive = AgentExecutive()
        
        # Layer: Creative (Lucineer pipeline)
        self.router = ModelRouter()
        self.planner = BuildPlanner(lattice=self.lattice)
        self.skills = SkillRecall()
    
    async def handle_build_request(
        self,
        player_intent: str,
        player_state: dict,
        world_state: dict,
    ) -> BuildResult:
        """
        The full pipeline, from intent to placed build.
        Each stage is a beat on the BeatGrid.
        """
        
        # ── BEAT 0: Intent registered ──────────────────────
        # T-Minus: register a prediction for when this build will complete
        estimated_beats = self.estimate_build_time(player_intent, world_state)
        prediction = self.predictor.predict(
            event_id=f"build_{self.world_id}_{id(player_intent)}",
            beats_ahead=estimated_beats,
        )
        prediction.subscribe(player_state['session_id'])
        
        # Cognitive: check player friction BEFORE starting
        phi = self.governor.compute_friction(player_state)
        if self.governor.check_deadband(phi, player_state['stage']):
            improvisation = self.executive.handle_alarm(phi, player_state)
            if improvisation.action != "none":
                # The agent adapts BEFORE the build, not after
                player_intent = improvisation.modify_intent(player_intent)
        
        # ── BEAT 1-2: Intent parse (Seed-mini) ─────────────
        self.beatgrid.tick()
        self.tempo.transition("cold_start")
        intent_data = await self.router.route(
            model="seed-mini",
            input=player_intent,
            skills=self.skills.recall(player_intent, k=5),
        )
        # Tensor-MIDI: encode as note on channel 0
        self.midi_bus.note_on(
            channel=0,
            pitch=ACTION_PITCHES['intent_parse'],
            velocity=self.confidence_to_velocity(intent_data.confidence),
            beat=self.beatgrid.current_beat,
        )
        
        # ── BEAT 3-6: Spatial decomposition (Qwen3.6) ──────
        self.beatgrid.tick(3)
        self.tempo.transition("deep_pipeline")
        spatial = await self.router.route(
            model="qwen3.6",
            input=intent_data,
            context=world_state,
        )
        # Encode spatial plan as a chord on channel 1
        for cmd in spatial.commands:
            self.midi_bus.note_on(
                channel=1,
                pitch=ACTION_PITCHES[cmd.type],
                velocity=self.confidence_to_velocity(cmd.confidence),
                beat=self.beatgrid.current_beat,
            )
        
        # ── SANDBOX: Forward simulation ────────────────────
        sandbox_score = self.sandbox.evaluate(spatial.commands, world_state)
        if sandbox_score.critical_failures:
            # Layer 3: Executive improvises a fix
            fix = self.executive.handle_sandbox_failure(sandbox_score)
            spatial.commands = fix.repair(spatial.commands)
        
        # ── BEAT 7-12: Code generation (Qwen3-Coder) ───────
        self.beatgrid.tick(7)
        commands = await self.router.route(
            model="qwen3-coder",
            input=spatial,
        )
        # Eisenstein snap all positions
        commands = self.planner.snap_to_lattice(commands)
        # Construction-order sort
        commands = self.planner.sort_by_build_order(commands)
        # Encode as chord on channel 2
        for cmd in commands:
            self.midi_bus.note_on(
                channel=2,
                pitch=ACTION_PITCHES[cmd.type],
                velocity=self.confidence_to_velocity(cmd.confidence),
                beat=self.beatgrid.current_beat,
            )
        
        # ── BEAT 13-14: Personality wrap (Hermes) ──────────
        self.beatgrid.tick(13)
        self.tempo.transition("build_stream")
        voiced = await self.router.route(
            model="hermes",
            input={
                "commands": commands,
                "character": "lucineer",
                "player_relationship": player_state['bond_stage'],
            },
        )
        # Channel 3: the personality note
        self.midi_bus.note_on(
            channel=3,
            pitch=ACTION_PITCHES['dialogue'],
            velocity=110,  # high confidence — Hermes knows his voice
            beat=self.beatgrid.current_beat,
        )
        
        # ── BEAT 15: Cadence ───────────────────────────────
        self.beatgrid.tick(15)
        # All channels: note off = pipeline complete
        self.midi_bus.all_notes_off()
        
        # T-Minus: confirm the prediction
        accuracy = self.predictor.confirm(prediction.id)
        # If accuracy is low, adjust future tempo estimates
        self.predictor.calibrate(accuracy)
        
        # Return: precompiled script (commands) + audible stream (MIDI)
        return BuildResult(
            commands=commands,
            dialogue=voiced.lines,
            midi_stream=self.midi_bus.serialize(),  # ~400 bytes for entire build
            prediction_accuracy=accuracy,
            phi=phi,  # player friction at build time
        )
    
    def estimate_build_time(self, intent: str, world_state: dict) -> int:
        """
        Estimate how many beats the build will take.
        Used by T-Minus to predict completion.
        Calibrated over time by prediction accuracy.
        """
        complexity = len(intent.split())  # crude proxy
        era_multiplier = {1: 1.0, 2: 1.2, 3: 1.5, 4: 1.8, 5: 2.0, 6: 2.5, 7: 3.0}
        base_beats = max(8, min(30, complexity // 2))
        return int(base_beats * era_multiplier.get(world_state['era'], 1.0))
```

### 5.4 The Roblox Client Integration

The client receives a single WebSocket message containing:
1. The precompiled build script (Eisenstein-snapped commands)
2. The tensor-MIDI stream (audible pipeline representation)
3. The prediction accuracy (for diegetic animation timing)

```lua
-- Roblox client: unified handler
local function onBuildConfirmed(message: {confirm: any})
    local commands = message.script
    local midiStream = message.midi
    local accuracy = message.accuracy
    
    -- High accuracy → Lucineer was right on tempo
    -- → smooth, confident animations
    -- Low accuracy → Lucineer took longer than expected
    -- → "measured twice" thinking animation
    local animationStyle = accuracy > 0.85 and "confident" or "careful"
    
    -- Stream build commands in construction order
    -- Each command triggers:
    --   1. The placement animation (body at the work face)
    --   2. The sound for that action (from the MIDI stream)
    --   3. The visual part appearing (never pops — arrives in work order)
    for i, cmd in commands do
        task.delay(i * BUILD_PACE, function()
            -- The note IS the sound IS the action
            local note = parseMIDINote(midiStream[i])
            playBuildSound(note.pitch, note.velocity)
            Lucineer:performBuildAction(cmd, animationStyle)
        end)
    end
end
```

### 5.5 What the Player Experiences

1. **They say what they want.** Lucineer walks to the bench, pulls chalk. (T-Minus: prediction registered, tempo = Largo)
2. **He chalks the sketch.** (Tensor-MIDI: Channel 0 note, the intent parse)
3. **He measures, pulls stock.** (Sandbox: forward simulation running)
4. **He builds.** Each part arrives in construction order with its own sound. (Tensor-MIDI: the chord stream from channels 1-2, audible as the build's soundtrack)
5. **He speaks.** One line, in character. (Channel 3: the personality note)
6. **He steps back.** Done. (Cadence: all notes off. Silence.)
7. **If the player struggled** (Governor: Φ > deadband), he offered help mid-build, simplified the task, or took over a part — the response was improvised, not scripted.

The player never sees the MIDI bus, the lattice, the predictor, the governor, or the executive. They experience a partner who seems to think ahead, work in rhythm, and improvise when surprised. **The substrate is invisible because it is the substrate.**

---

## 6. CROSS-CUTTING CONCERNS

### 6.1 Backward Compatibility

The unified framework does not require rewriting the existing Worker or Roblox client. It can be deployed incrementally:

1. **Phase 1:** Add WebSocket subscribe endpoint alongside existing REST polling. Clients opt-in. Polling remains as fallback.
2. **Phase 2:** Add Eisenstein snapping as a post-processing step in the pipeline. JSON remains the wire format; MIDI is internal.
3. **Phase 3:** Add the sandbox validation stage. Friction governor runs in shadow mode (logs Φ but doesn't trigger improvisation).
4. **Phase 4:** Switch wire format from JSON to tensor-MIDI. Enable Governor-triggered improvisation. Retire REST polling.

### 6.2 The Counterpoint Constraint

From "The Counterpoint of Agents" — the five models must be **independent yet related**, like voices in Fux's species counterpoint:

| Model | Voice | Character |
|---|---|---|
| Seed-mini | Cantus firmus | The fixed song — the parsed intent, grounded |
| Qwen3.6 | Second species (2:1) | Two notes against one — spatial decomposition multiplies the plan |
| Qwen3-Coder | Fourth species | Suspension — holds the structural context while code resolves around it |
| Hermes | Florid | The character voice — mixes all species, the most independent line |
| Nemotron | Cadence | The closing gesture — synthesis that resolves all prior material |

**No parallel octaves:** Two models must not produce the same output in the same way. Seed-mini and Qwen3.6 both parsing intent with identical prompts would be parallel octaves — wasted compute. Each model gets a structurally different prompt (different role, different temperature, different constraint tokens).

**Contrary motion:** When one model expands (generates many options) and another contracts (selects the best), the output is richer than two expanders. The pipeline alternates expansion and contraction.

### 6.3 The Tempo Map Applied

From "The Tempo Map of Computation" — the pipeline has a composed tempo map:

```
Beat  0-2:  Largo    (40 BPM) — Cold start, intent parsing
Beat  3-6:  Adagio   (50 BPM) — Deep spatial reasoning, comprehensive
Beat  7-12: Moderato (80 BPM) — Code generation, steady output
Beat 13-14: Allegro  (120 BPM)— Personality wrap, quick and sharp
Beat 15:    Adagio    (50 BPM) — Cadence, stepping back
```

The player feels each transition. Lucineer's animations shift character with the tempo — slow and deliberate during Largo, quick and purposeful during Allegro. This is the system having a voice, not a latency budget.

### 6.4 Connection to the Spirit Documents

**"The Tempo Map of Computation"** argues that systems should have composed tempo character, not flat metronome markings. The unified framework's tempo map does this literally — the BeatGrid changes BPM per pipeline stage, and the player experiences the transitions as Lucineer's working rhythm.

**"The Counterpoint of Agents"** argues that multi-agent systems fail when voices are in unison (parallel octaves) or in noise (dissonance without resolution). The unified framework encodes species counterpoint as the pipeline structure — each model is a voice with a different species role, and the cadence (build completion) resolves all prior dissonance.

---

## 7. RISKS AND OPEN QUESTIONS

### 7.1 WebSocket Reliability in Roblox

Roblox's `WebSocket` API is relatively new and may have reconnection issues. **Mitigation:** T-Minus subscribe-once means the subscription is stateless — if the WebSocket drops and reconnects, the client re-subscribes and the prediction still fires. The prediction is stored in the Durable Object, not the WebSocket.

### 7.2 MIDI Pitch Space Exhaustion

With 128 pitch values and 16 channels, the tensor-MIDI protocol can represent 2,048 distinct action types. The current build system uses ~15 action types. **This is not a constraint.** If the action space grows beyond 128 pitches, we use Control Change messages for sub-types.

### 7.3 Eisenstein Lattice vs. Creative Freedom

Snapping to a hexagonal grid constrains where parts can be placed. Some builds (curved walls, irregular shapes) may fight the lattice. **Mitigation:** The lattice scale is configurable. At `scale=1.0`, the grid is fine enough that curvature is approximated well. Players in creative mode can disable snapping entirely — the lattice is a default, not a law.

### 7.4 Governor False Positives

The friction governor might interpret a player's deliberate slowness (careful craftsmanship) as struggling. **Mitigation:** The deadband is stage-dependent and the Φ metric weights action entropy over raw idle time. A Stage 3+ player working slowly on a complex build has low action entropy (consistent, deliberate actions) even with high idle time. The governor distinguishes "thinking" from "stuck."

### 7.5 The Fallibility Question

FABLE Vignette 5 (The Misread) requires Lucineer to occasionally fail. The sandbox prevents failures. **Resolution:** The sandbox has a configurable pass-through rate. By default, it catches structural failures (parts floating in mid-air, overlapping geometry) but lets through aesthetic misjudgments (a door 4cm too wide for its frame). The player sees the craft error, not the system error. The sandbox filters for physics, not taste.

---

## 8. IMPLEMENTATION PRIORITY

| Priority | Component | Effort | Impact |
|----------|-----------|--------|--------|
| 1 | T-Minus subscribe-once WebSocket (replace polling) | Medium | 60× message reduction, better UX |
| 2 | Eisenstein snap in build planner | Low | Visual quality, exact arithmetic |
| 3 | Build sandbox (Layer 1) | Medium | Catches geometry errors pre-client |
| 4 | Player friction governor (Layer 2) | Medium | Enables adaptive agent behavior |
| 5 | Tensor-MIDI internal encoding | Medium | 30× bandwidth reduction, audible debugging |
| 6 | Agent executive (Layer 3) | High | The real payoff — improvisation |
| 7 | Tensor-MIDI wire format (replace JSON) | High | Full substrate migration |
| 8 | `swarm-tminus-lucineer` Python package | High | Clean abstraction for future agents |

---

## 9. THE NORTH STAR

The goal is not to add features. It is to replace the substrate. The current architecture is a polling, JSON-passing, hard-coded, floating-point system. The unified framework is a predict-and-confirm, tensor-MIDI, FEP-driven, Eisenstein-lattice system.

The player never sees the difference. They feel it.

They feel it as Lucineer who seems to know when the build will be done before it starts (T-Minus prediction). Who works in rhythm, each action sounding its own note (tensor-MIDI beat grid). Who notices when they're struggling and adapts without being asked (snapkit governor + executive). Whose builds align to a grid that feels organic, not imposed (Eisenstein lattice).

They feel it as a partner who thinks ahead, works in rhythm, and improvises when surprised.

That is the substrate. That is the build.

---

*End of Analysis. Architecture, not poetry. But architecture in service of something that feels like music.*
