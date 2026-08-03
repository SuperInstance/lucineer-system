# THE GRAND PLAN

## The low-level architecture at a high level

*Written by Claude Fable 5, 2026-08-02, hour 16. This document sits downstream of "The Organ Plays Itself" (the soul), the Unified Integration Plan (the game), the Ship Readiness audit (the truth), and the Nemotron Unification Analysis (the substrate). Its job is to be the blueprint: the document an engineer reads and knows what to build, and a creative reads and knows what it feels like. Every number in it is either measured, specified, or marked as a target. He'd check.*

---

## 0. WHAT THIS SYSTEM IS

One sentence before the stack: **Slackwater is a live performance system disguised as a game, in which a fleet of AI models shares one clock with a human player, and the shared clock — not the intelligence — is what makes it feel alive.**

Everything below is in service of that sentence. The stack exists to carry tempo from the silicon to the player's chest. The data flow exists to turn a spoken wish into a build that arrives *in rhythm*. The wiring exists so that fourteen models can play as one band instead of fourteen soloists — which, per the Ship Readiness audit, is precisely the failure mode we have already demonstrated: fourteen correct parts and nobody owning the seams. This document owns the seams. Every interface below is specified to the byte or named as a phase deliverable.

---

## 1. THE STACK

Twelve layers, bottom to top. Read it like a rack: the constraint math is the power supply, the player is the performer at the top, and every layer speaks to its neighbors through a defined protocol — no reaching around.

```
┌─────────────────────────────────────────────────────────────────────┐
│ 12. THE PLAYER — the performer. Their tempo, their flow,            │
│     their experience. The only layer that matters.                  │
├─────────────────────────────────────────────────────────────────────┤
│ 11. ROBLOX CLIENT (Luau, 35 modules)                                │
│     BuildAnimator · AtmosphereRig · WorldScanner · ChatHandler      │
│     PerceptionCapture · CommandExecutor · BeatClock (client mirror) │
├─────────────────────────────────────────────────────────────────────┤
│ 10. CLOUDFLARE EDGE                                                 │
│     Worker relay · BuildCoordinator Durable Object (per world)      │
│     D1 (memory) · Vectorize (skills) · R2 (MOLT trajectories)       │
├─────────────────────────────────────────────────────────────────────┤
│  9. LUCINEER BRAIN PIPELINE (process_v2.py + brain.py)              │
│     intent → plan → sandbox → code → voice → safety                 │
├─────────────────────────────────────────────────────────────────────┤
│  8. CASTING-CALL — model routing. Which keyboard for which note.    │
│     Capability atlas · structural bias map · tempo profiles         │
├─────────────────────────────────────────────────────────────────────┤
│  7. SLACKWATER PERCEPTION — the ears.                               │
│     Multi-track MIDI world encoding · convergence detection         │
├─────────────────────────────────────────────────────────────────────┤
│  6. SLACKWATER HARMONY — the nervous system.                        │
│     Sandbox (simulate) → Governor (Φ) → Executive (improvise)       │
├─────────────────────────────────────────────────────────────────────┤
│  5. SLACKWATER T-MINUS — the future.                                │
│     Predict-and-confirm · precompiled scripts · no polling          │
├─────────────────────────────────────────────────────────────────────┤
│  4. SLACKWATER LATTICE — the ground.                                │
│     Eisenstein A₂ placement · exact integer arithmetic              │
├─────────────────────────────────────────────────────────────────────┤
│  3. SLACKWATER TEMPO — the clock.                                   │
│     TempoMap · GrooveEngine · EnergyAdapter · BeatClock             │
├─────────────────────────────────────────────────────────────────────┤
│  2. TENSOR-MIDI — the language.                                     │
│     4D events: (pitch, velocity, tick, channel) · 8 bytes each      │
├─────────────────────────────────────────────────────────────────────┤
│  1. FLUX CONSTRAINT ENGINE — the physics.                           │
│     Exact arithmetic · INT8 saturation · 8-bit error mask           │
└─────────────────────────────────────────────────────────────────────┘
```

### Layer 1 — FLUX constraint engine (the physics)

Everything above this layer is allowed to be creative. This layer is not. FLUX provides:

- **Exact arithmetic.** Build coordinates are Eisenstein integers (Layer 4), velocities and confidences are INT8 (0–127), ticks are uint32. No accumulating float drift, ever, in anything that two agents must agree on. Floats exist only in presentation (a part's final Y position on irregular terrain) — never in agreement.
- **INT8 saturation.** All bounded quantities clamp at [0, 127] instead of overflowing. A velocity of 140 is a bug that becomes 127, loudly logged, not a corrupted event.
- **The 8-bit error mask.** Every event in the system carries one byte of honesty — a bitfield of constraint violations attached at whatever layer detected them:

```
bit 0  ERR_COLLISION   — placement overlaps existing geometry
bit 1  ERR_UNSTABLE    — fails the sandbox stability check
bit 2  ERR_ERA_GATE    — action not unlocked at player's era
bit 3  ERR_OFF_LATTICE — position did not snap cleanly (drift > ½ cell)
bit 4  ERR_SAFETY      — safety stage flagged content
bit 5  ERR_BUDGET      — cost/token/rate budget exceeded
bit 6  ERR_TIMEOUT     — stage exceeded its nested timeout budget
bit 7  ERR_DRIFT       — exact-path and float-path disagree (canary bit)
```

An event with mask `0x00` is clean and executes. Any set bit routes the event to the Harmony executive instead of the world. The mask is the whole error-handling philosophy in one byte: **errors are data on the same bus as everything else**, not exceptions thrown across layer boundaries. Note bit 4: the Nemotron-Content-Safety verdict — currently the launch-blocking gap in Ship Readiness 1.5 — travels in the same byte as a collision. Safety is a constraint, not a separate system, and therefore cannot be forgotten at a seam.

### Layer 2 — Tensor-MIDI (the language)

The one wire format for everything: build commands, model outputs, player actions, tide changes, flow measurements. From `flux-tensor-midi`, an event is a 4-dimensional point — and on the wire it is exactly 8 bytes:

```
SWMIDI-8 event (8 bytes, little-endian):
  byte 0     status:  type(4 bits) | channel(4 bits)
  byte 1     pitch:   action type, 0–127
  byte 2     velocity: weight / confidence, 0–127
  byte 3     error mask (Layer 1)
  bytes 4–7  tick: uint32, 96 PPQ on the shared BeatClock
```

Event types (the 4-bit type nibble): `0=NOTE_ON, 1=NOTE_OFF, 2=CC` (control change: pitch=controller, velocity=value), `3=PROGRAM` (pipeline stage change), `4=META` (tempo change, prediction, convergence event). Events that need spatial payload (a `createPart` needs a position and size) carry it as CC pairs on the same channel at the same tick: `CC 16/17 = Eisenstein a, b` (int8 each, offset +64; large coordinates use CC 18/19 as high bytes), `CC 20 = Y-register`, `CC 21 = material`, `CC 22 = size class`. A 100-part build is ~800 bytes of events plus ~2 KB of CC payload — versus ~12 KB of JSON today. During migration (Phase 2→3 of §4) the wire carries a JSON envelope with these exact fields; the binary packing is a Phase 3 flip of a serializer, not a redesign, because the *shape* is fixed now.

**The channel map is the org chart.** Sixteen channels, allocated once, forever:

| Channel | Voice | Notes |
|---|---|---|
| 0 | Lucineer | the master builder's hands |
| 1 | Earl | manifest, scheduling |
| 2 | Spark | welds, micro-tasks |
| 3 | Bea | the Light |
| 4 | Hermes (tender) | supply line |
| 5 | Forty-Eight | the raven; Vectorize's channel (Insight 9) |
| 6–7 | recruitable agents | assigned at recruitment |
| 8 | Environment | tide, storm, aurora — the world is a player too |
| **9** | **The player** | channel 10 in 1-indexed MIDI: the drum channel. The player is the drummer. The player sets the groove. This is not a joke; it is the design. |
| 10 | Intent model (Seed-mini) | pipeline bus starts here |
| 11 | Planner (Seed-pro / Qwen3.6) | |
| 12 | Coder (Qwen3-Coder) | |
| 13 | Voice (Hermes-405B) | the only channel allowed to speak; **never** allowed to emit build notes (Conflict 8, enforced by channel, not by prompt) |
| 14 | Nemotron | safety verdicts + Era-7 coordination |
| 15 | System | tempo changes, T-Minus predictions, Φ readings, convergence events |

The channel map turns two of the audit's boundary failures into type errors: a Hermes-stage build command is a NOTE_ON on channel 13, which the CommandExecutor is hard-coded to ignore; a safety verdict is a channel-14 event that the relay refuses to forward the build without.

Pitch map (the action vocabulary, ~30 of 128 slots used): `36–47` terrain ops, `48–59` structural placement (foundation low, per the register rule: **foundations are bass notes**), `60` createPart, `62` weld, `64` setMaterial/paint, `65` addLight, `67` setTerrain, `69` markUnfinished (the thesis has a pitch), `71` dialogue, `72` intent_parse, `74` spatial_plan, `76` code_gen, `78` voice_wrap, `79` safety_check, `81` prediction, `83` phi_reading, `84` convergence.

### Layer 3 — Slackwater Tempo (the clock)

Published on PyPI as `slackwater-tempo`. Four modules, one job: make time a composed thing rather than an inherited metronome.

```python
class BeatClock:          # the one clock. 96 PPQ. Every layer syncs to it.
    def now(self) -> int                    # current tick, uint32
    def tick_duration(self) -> float        # seconds per tick at current BPM
    def at_beat(self, beat: float) -> int   # beat → tick

class TempoMap:
    def transition(self, stage: str, over_beats: int = 8) -> None
    # named stages, from the Nemotron analysis §6.3:
    # cold_start=40 (Largo), deep_pipeline=50 (Adagio),
    # code_gen=80 (Moderato), build_stream=120 (Allegro),
    # creative_mode=None (Rubato — BPM is delegated to the EnergyAdapter)

class GrooveEngine:
    def humanize(self, tick: int, channel: int) -> int
    # per-channel swing and push/drag. Lucineer lays back 3 ticks.
    # Spark pushes 2 ticks ahead. The player is never quantized.

class EnergyAdapter:
    def observe(self, events: list[SWMIDIEvent]) -> None   # player channel only
    def target_bpm(self) -> int
    # maps player actions/minute + input cadence to BPM,
    # smoothed over 5–10 s. The yard breathes with the player.
```

The Durable Object holds the authoritative BeatClock; the Roblox client runs a mirror synchronized by channel-15 META tempo events (drift correction ≤ 1 tick/beat, resync on every WebSocket message). One clock, two faces — the same discipline as a click track in every musician's ear.

This is Casey's insight made infrastructure: the difference between "place the brick at (10, 5, −20)" and "place the brick at tick 4608, velocity 87, channel 0, inside a 72 BPM groove that just quickened because the player's hands did" is this layer existing.

### Layer 4 — Slackwater Lattice (the ground)

Eisenstein A₂ placement. `z = a + bω, ω = e^{2πi/3}`; Cartesian `x = (a − b/2)·s`, `z = b·(√3/2)·s`, lattice scale `s = 4` studs. Six equidistant neighbors, isotropic snap error (square grids carry a 41% diagonal penalty), guaranteed minimum spacing, and — because `(a, b)` are integers — exact arithmetic all the way down to Layer 1. Rotation snaps to 60° increments. Y stays continuous; terrain is irregular and the lattice governs *agreement between agents*, not the shape of the earth. `LatticeSnap.snap(x, z) → (a, b)` runs as a post-processing pass on every coder-stage output, plus client-side for player placements in assisted mode (creative mode may disable it — the lattice is a default, not a law). Visual consequence, worth stating in a blueprint because it is a feature: hexagonal coordination makes builds look like tidal communities that *grew there* — fish traps, basalt columns — not plotted subdivisions.

### Layer 5 — Slackwater T-Minus (the future)

Predict-and-confirm replaces polling. Today the client asks "done yet?" 120 times per build; the audit shows the answer is currently "401" every time. Under T-Minus the client speaks twice:

```
WS /ws messages (JSON envelope, → binary in Phase 3):
→ {type: "t-minus.subscribe", jobId}
← {type: "t-minus.predict",  jobId, predictedTick, confidence}
← {type: "t-minus.confirm",  jobId, accuracy, script: [SWMIDI events]}
← {type: "t-minus.miss",     jobId, newPredictedTick}
```

The prediction is issued at job creation: *"this build completes near tick 5760."* The client uses `predictedTick` to time Lucineer's thinking choreography — chalk at beat 0–4, stock-pulling at beat 5–8 — so latency is spent as characterization (Insight 2: latency is the character). On `confirm`, the **precompiled script** arrives: the entire build as SWMIDI events, ready for zero-latency execution. On `miss`, he measures twice; a new prediction is issued; the player sees a craftsman being careful, not a spinner. (There is no spinner. `Config.UI_THINKING_TEXT` and its two call sites die in Phase 1.) Message economics: 2 messages instead of ~120; prediction accuracy is recorded per job and calibrates future estimates.

### Layer 6 — Slackwater Harmony (the nervous system)

The triadic architecture from Snapkit v2, published as `slackwater-harmony`:

- **Sandbox (Layer 1 of the triad):** forward-simulates every build plan between the planner and coder stages — collision, stability, era gates — writing results into the error mask. Configurable pass-through: physics failures always caught, aesthetic misreads let through at a tuned rate, because a door four centimeters proud of its frame is characterization (Vignette V5).
- **Governor (Layer 2):** computes Φ, cognitive friction, per entity and for the room:

```
Φ(t) = 0.35·H(action entropy) + 0.25·idle + 0.30·error_rate + 0.10·help_requests
```

  Φ is published every 4 beats as a channel-15 event (pitch 83, velocity = Φ·127 clamped). Calibration: Φ > deadband (stage-dependent, 2.0 down to 0.5) = friction, wake the Executive. Φ < 0.15 = approaching the pocket. **Φ < 0.05 = deep flow**, and the system's job inverts —
- **Executive (Layer 3):** improvises when the Governor fires: simplify the task, offer targeted help, take over temporarily, inject novelty. And its most important instruction, the one that separates this from every engagement-optimized system on earth: when Φ is *low*, do nothing. The **FlowStateProtector** is the Executive's low-Φ policy, and it is a suppression list, not a feature list: agent interjections deferred, tempo transitions rate-limited to ±2 BPM/min, ambient bed held, all channel-1-through-8 dialogue queued until Φ rises. The Governor also runs the **connectome** — cross-agent coupling detection — so Earl drifting out of Lucineer's world for three sessions is a measurable decoupling the Executive can repair diegetically.

### Layer 7 — Slackwater Perception (the ears)

Published as `slackwater-perception`. The input half of the closed loop: everything the player does becomes multi-track MIDI *before* any model sees it. Tracks per the MIDI Perception Vision: pitch, tempo, velocity, timbre, inflection, silence, gesture, intention, attention. In-game, the tracks are concrete: the player's build actions are the velocity track; their input cadence is the tempo track (feeding the EnergyAdapter); their pauses are the silence track (feeding Φ's idle term); their camera focus is the attention track; a voice request through ChatHandler gets pitch/inflection tracks from the audio itself. The `IntentionPropagator` is the vocalist's look: it emits a channel-9 CC *before* the action completes — the player walking toward the tideline with empty hands is an intention event the fleet can prepare against (which is what T-Minus consumes to pre-warm predictions). The `ConvergenceDetector` watches all tracks and emits pitch-84 events when they align — the measurable pocket. And because every session is a multi-track MIDI file, **every session is a replayable score**: the first castle, the storm repair, the night he first said "good," reproducible with full timing, weight, and channel attribution. That replay file is also, not incidentally, the MOLT trajectory (§4, Phase 1).

### Layer 8 — Casting-Call (the routing brain)

The accumulated wisdom of 1,584 repos and 4,500+ queries: which keyboard for which note. In the stack it is a pure function consulted by the brain pipeline:

```python
def cast(task: TaskType, constraints: CastingConstraints) -> ModelAssignment
# TaskType: INTENT | PLAN | CODE | VOICE | VERIFY | VISION | SAFETY | COORDINATE
# constraints: latency_budget_ticks, cost_ceiling, player_bond_stage, era
# returns: model id + temperature + prompt-variant + natural tempo (BPM)
```

Each model carries a **tempo profile** (Seed-mini Allegro 120+, Hermes Adagio 60, Opus Largo 50) registered with the TempoMap, so the pipeline's tempo transitions are derived from who is playing, not hardcoded. The counterpoint constraint from the Nemotron analysis is enforced here: no parallel octaves — two models never receive structurally identical prompts for the same stage. Casting-call is also where model swaps happen without architecture changes (Nemotron 3 Super replacing Seed-mini for intent, per the NVIDIA roadmap Phase 2, is a one-row change in the atlas, measured against the R2 trajectory set before commit).

### Layer 9 — The brain pipeline (the performance)

The existing 5-model pipeline, re-plumbed onto the bus. Six stages, each a channel, each emitting its output as SWMIDI events:

```
intent (ch 10) → plan (ch 11) → SANDBOX → code (ch 12)
   → LATTICE SNAP → voice (ch 13) → safety (ch 14)
```

Timeout budgets nest, per the production design: brain 90 s < DEEP_TIMEOUT 100 s < client patience ∞ (T-Minus miss handling makes the last one true). The fast path (17 templates, <2 s) bypasses stages 2–4 but still passes safety and still emits on the bus — a template build is quieter music, not silence. The voice stage cannot emit build notes (channel enforcement, Layer 2). The safety stage cannot be skipped (the relay drops any confirm whose script lacks a clean channel-14 verdict event).

### Layer 10 — Cloudflare edge (the venue)

- **Worker relay:** HTTP ingress (`POST /api/message`), auth, per-player rate limiting (3 s cooldown + per-server concurrent-job cap — fixing audit item 1.6's one-bucket-per-16-players).
- **BuildCoordinator Durable Object** (one per world instance): owns the authoritative BeatClock, the T-Minus prediction table, WebSocket sessions, job leasing (`claimed_at`, `attempts`, 3-min lease, dead-letter at 3 — the server half already exists and is correct; Phase 1 makes the processor actually call it), and the 24 h alarm sweep the audit found missing.
- **D1:** player profiles, build history, conversations, bond journal — behind a shared-secret header from Phase 1 Day 1, because an open memory Worker is a child-safety issue wearing an infra costume and the audit confirmed it is currently open.
- **Vectorize:** the skill index (55+ skills, player patterns), fronted diegetically by Forty-Eight on channel 5.
- **R2:** MOLT-format trajectory logs — every deep-path job's (state, prompt, tool calls, outcome, perception score). The single highest-option-value cheap item in the project; a year of live trajectories cannot be backfilled.

### Layer 11 — Roblox client (the instrument)

35 Lua modules — of which, per the audit, 9 currently ship. Phase 1's ugliest, least glamorous, most important deliverable is making `default.project.json` tell the truth. The load-bearing modules for this blueprint: **CommandExecutor** (dispatches SWMIDI pitches to world mutations), **BuildAnimator** (streams parts on the 32nd-note grid — at Allegro 120 that is ~62 ms, at Andante 90 ~83 ms; the tuned "0.08 s stagger" stops being a constant and becomes a musical duration, which is the whole thesis in one refactor), **BeatClock mirror**, **PerceptionCapture** (channel-9 encoder), **WorldScanner** (nearest-50 spatial context), **AtmosphereRig** and **AudioManager** (material-appropriate settle sounds, pitch by mass — the build is audible because the build *is* notes), **ChatHandler** (TextChatService, filtered), and **FilterGate** — the one `filterFor()` chokepoint every displayed AI string passes through, fail-closed, because the audit found the current implementation is three comments politely asking someone else to do it.

### Layer 12 — The player (the performer)

Not a consumer of the stack — a channel on it, and the privileged one. The player is never quantized, never groove-corrected, never tempo-managed. The system adapts to them; the reverse direction does not exist. Their channel is the drum channel. When they speed up, eleven layers of machinery conspire to speed up with them, and the only thing they feel is that the yard is *with* them. The stack succeeds exactly to the degree that this layer never learns the other eleven exist.

---

## 2. THE DATA FLOW

One moment, traced end to end. The player — Era 1, Bond Stage 2, twenty minutes into a session — says: **"build me a castle."**

**T−15 s, tick 41760.** It starts before they speak. PerceptionCapture has been streaming channel-9 events: the player has circled the same flat quarter of the yard three times, camera repeatedly dwelling on high ground (attention track), inventory heavy with stone (velocity-track context). The IntentionPropagator emits `CC ch9: intention=structural_large, confidence=71`. T-Minus consumes it and pre-warms: the DO registers a speculative prediction and the processor pre-fetches the player's D1 context and top-5 Vectorize skills. Cost if wrong: one cheap fetch. Value if right: fifteen seconds off the deep path. *The band saw the vocalist take the breath.*

**T+0.0 s, tick 43200.** The words arrive — voice, through ChatHandler. Perception encodes the utterance itself: pitch track (rising excitement), tempo track (words-per-second up 20% from session baseline), velocity 74 (eager, not urgent). The EnergyAdapter, already reading an elevated action cadence, begins an 8-beat accelerando: session tempo 72 → 84 BPM. Allegro is coming, but nothing lurches — 5–10 s smoothing, always.

**T+0.1 s.** `POST /api/message` → relay → rate-limit check (clean) → BuildCoordinator DO. Job created as `pending`. T-Minus converts the speculative prediction to a real one: `{predictedTick: 46080 (beat 480, ≈28 s out), confidence: 0.82}` — calibrated on 214 prior castle-class jobs. The client's single WebSocket receives `t-minus.predict`. No polling begins, because polling no longer exists.

**T+0.2 s, in the yard.** The predict message triggers choreography sized to `predictedTick`: Lucineer stops hammering (the yard's heartbeat stopping *is* the acknowledgment), walks the footprint, pulls chalk. The Governor logs Φ = 0.12 — approaching the pocket. Channel-15 event, pitch 83, velocity 15.

**T+0.5–3 s. Casting.** The processor claims the job (atomic lease, `attempts=1`). Casting-call assigns: intent → Seed-mini (ch 10, Allegro), plan → Seed-pro (ch 11), code → Qwen3-Coder (ch 12), voice → Hermes-405B (ch 13, Adagio — his line will take longer than the code, and that is correct), safety → Nemotron (ch 14). TempoMap transitions `cold_start → deep_pipeline`.

**T+3–9 s. Intent and plan.** Seed-mini: `NOTE_ON ch10 pitch72 vel110` — high confidence: castle, medieval, defensive, sized-to-plot. Seed-pro emits the spatial plan as a chord on ch 11: foundation ring, four walls, gate, two towers, keep — each a note whose pitch encodes its structural register (foundations at pitch 48, low; battlements at 59, high). The plan's anchor point passes through LatticeSnap: the flat quarter's center snaps to **Eisenstein (3, −2)** — Cartesian (16, −6.93) at scale 4 — with all 60°-coordinated wall angles derived from that point's six neighbors.

**T+9–11 s. Sandbox.** Harmony's forward simulation runs all placements against WorldScanner's nearest-50 snapshot. One tower footing overlaps the player's own week-old bench: `ERR_COLLISION` bit set on that one event. The Executive repairs (shifts the tower one lattice cell, exact arithmetic, no drift) rather than failing the build. One aesthetic quirk — a gate slightly narrow for its arch — passes through at the tuned fallibility rate. Misreads are characterization.

**T+11–22 s. Code.** Qwen3-Coder emits **28 build commands** as NOTE_ON events on channel 12, each with CC position payloads, each velocity = material weight: foundation stones at velocity 96 (heavy, deliberate), wall courses 80, the keep's glass lantern at 34 (delicate). BuildPlanner sorts by construction order — foundation upward, because that is the order a builder builds and the order a bass line resolves.

**T+22–26 s. Voice and safety.** Hermes writes the line, in voice, naming the gap — because the plan included pitch 69, `markUnfinished`, on the gatehouse rail. Channel 13 carries exactly one note: dialogue. If Hermes hallucinates a build command, channel enforcement discards it silently. Nemotron stamps the script: `NOTE_ON ch14 pitch79 vel127, mask 0x00`. Clean.

**T+26 s, tick 45890.** Pipeline complete — beat 478, against a prediction of 480. Accuracy 0.96, logged for calibration. The DO fires `t-minus.confirm` down the WebSocket: one message, carrying the precompiled script — ~1.9 KB for the whole castle. The full trajectory (perception context, casting decisions, all six stages, sandbox repair, final script) serializes to R2 in MOLT `Result` format. The dataset grows by one.

**T+26–40 s. The build streams.** BuildAnimator executes the score: 28 parts on the 32nd-note grid at 84 BPM (~89 ms stagger), each placement a thock pitched by mass through AudioManager, dust on the heavy ones, Lucineer's body at the active edge the entire time. Foundation notes land like a bass line; the towers climb; the lantern arrives pianissimo. FilterGate passes his line; it prints as he sets the last stone but one:

> **LUCINEER:** Castle'll hold. Gate rail's yours — a wall teaches nothing till someone leans on it.

**T+40 s onward.** The player walks the wall. Perception reads it: action entropy falling, cadence settling into the grid, attention steady on the gatehouse gap. The ConvergenceDetector fires pitch 84 — tracks aligned. **Φ = 0.03. Deep flow.** The FlowStateProtector inverts the system: Earl's queued manifest line — held. Tempo transitions — locked to ±2 BPM/min. Ambient bed — sustained. Forty-Eight stays on the roofline. For the next several minutes the most sophisticated thing this twelve-layer stack does is *nothing*, on purpose, measurably.

The player watches the castle hold. They don't know why it felt right. The system knows: prediction accuracy 0.96, zero error bits, convergence at tick 46340, Φ 0.03 and holding. The protector holds the silence — the same silence after the last chord of a good set, the one that means everyone in the room felt it.

---

## 3. THE WIRING DIAGRAM

Every edge in the system: who talks to whom, carrying what, over what. If a connection is not in this table, it does not exist — reaching around layers is how we got fourteen correct parts and a 401.

### 3.1 The edges

| # | From → To | Payload | Protocol | Notes |
|---|---|---|---|---|
| 1 | Player → ChatHandler | text / voice | Roblox input + TextChatService | inbound filtering lives here |
| 2 | ChatHandler → Relay | `{sessionId, playerId, message}` | HTTPS POST `/api/message` | rate-limited per player |
| 3 | PerceptionCapture → DO | channel-9 SWMIDI events, batched per beat | WebSocket (same socket as edge 7) | ≤1 batch/beat; silence is an event |
| 4 | Relay → DO | job creation | DO stub call | job born `pending` |
| 5 | Processor → DO | claim / complete / fail | HTTPS `POST /api/job/:id/claim`, `POST /api/job/:id/result` | atomic lease, 3-min TTL, `attempts` |
| 6 | DO → Processor | pending jobs + perception context | HTTPS `GET /api/jobs/pending` (Phase 1) → WS push (Phase 2) | context = last 8 beats of ch-9 events |
| 7 | DO → Client | `t-minus.predict / confirm / miss`, tempo META | WebSocket `/ws` | the only downstream channel; polling deleted |
| 8 | Processor → Casting-Call | `cast(task, constraints)` | in-process Python | pure function over the capability atlas |
| 9 | Processor → Models | staged prompts | HTTPS (DeepInfra) | per-stage nested timeouts |
| 10 | Pipeline → Harmony sandbox | plan events | in-process | between ch 11 and ch 12; writes error masks |
| 11 | Pipeline → Lattice | positions | in-process | `snap()` post-pass on all ch-12 output |
| 12 | Perception → Governor | all tracks | in-process (processor) + DO Φ cache | Φ every 4 beats |
| 13 | Governor → Executive | `(Φ, deadband, entity)` | in-process | fires above deadband; suppresses below 0.05 |
| 14 | Executive → Pipeline / DO | intent rewrites, repairs, suppression lists | in-process + ch-15 META events | FlowStateProtector = suppression list on the DO |
| 15 | Processor → D1 | profile, journal, conversation writes | HTTPS, shared-secret header | **auth from Phase 1 Day 1** |
| 16 | Processor → Vectorize | skill recall / store | HTTPS, shared-secret header | top-k=5, `uses_count` increment |
| 17 | Processor → R2 | MOLT trajectory per deep job | R2 binding | write-only from processor |
| 18 | DO → Client | precompiled script | inside `t-minus.confirm` | SWMIDI events, JSON envelope → binary Phase 3 |
| 19 | CommandExecutor → world | part mutations | in-process Luau | dispatches on pitch; ignores ch 13 notes |
| 20 | BuildAnimator → AudioManager | note events | in-process Luau | the sound IS the note |
| 21 | Anything → Player-visible text | strings | **FilterGate.filterFor()** | single chokepoint, fail-closed to `"..."` |

### 3.2 The bus rule

Rules that hold on every edge:

1. **Everything on the wire is an SWMIDI event or carries them.** JSON envelopes during migration are containers for the same fields — `{type, ch, pitch, vel, mask, tick, cc?}` — so Phase 3's binary flip changes serialization, not semantics.
2. **Ticks come only from the BeatClock.** No `os.time()`, no `tick()`, no `task.wait(0.08)` anywhere in coordination logic. Wall-clock time exists only inside the BeatClock's own implementation.
3. **The error mask travels with the event.** No layer throws across a boundary; it sets bits and forwards. The Executive is the only consumer of dirty events.
4. **Channels are authorization.** The executor whitelist maps channel → permitted pitch ranges. Channel 13 has no build pitches. Channels 1–8 have no terrain pitches. Channel 9 is never emitted by anything server-side — the player's channel cannot be forged by a model.
5. **One filter chokepoint** (edge 21). A string that has not passed FilterGate does not render. There is no second path, so there is no seam to forget.

### 3.3 The repos

| Repo | Layer(s) | Language | Status |
|---|---|---|---|
| `flux-tensor-midi` / `constraint-theory-core` | 1–2 | Python/Rust | exists; SWMIDI-8 packing to add |
| `slackwater-tempo` | 3 | Python (+ Luau mirror to write) | **on PyPI, tested** |
| `slackwater-lattice` | 4 | Python + Lua | **on PyPI, tested** |
| `tminus-*` → `slackwater-tminus` | 5 | Python + TS (DO) | primitives exist; DO integration is Phase 2 |
| `slackwater-harmony` | 6 | Python | **on PyPI, tested** |
| `slackwater-perception` | 7 | Python (+ Luau capture) | **on PyPI, tested** |
| `casting-call` | 8 | data + Python | atlas exists; `cast()` API is Phase 3 |
| `lucineer-system` (processor, brain) | 9 | Python | exists; needs bus re-plumb |
| `lucineer-worker`, `lucineer-memory`, `lucineer-vector` | 10 | TypeScript | exist; need auth + DO evolution |
| `lucineer-roblox` | 11 | Luau | 35 modules; **build tree ships 9** — Phase 1 fixes this |

---

## 4. THE 90-DAY BUILD PLAN

Three phases. The first is deliberately unglamorous, because the Ship Readiness audit is unambiguous: we do not have a substrate problem yet, we have a seams problem — the loop 401s, the memory Workers are open, 90% of the Lua never loads, and zero tests exist at any layer. A tempo layer on top of a broken loop is a metronome bolted to a boat with no hull. So Phase 1 closes the hull *and* lays the clock in, together — because retrofitting tempo later would mean re-plumbing the same seams twice.

The standing rule for all 90 days, promoted from the audit: **every merge must survive the smoke test in a live Studio session.** One scripted run: message in → parts at non-origin positions → filtered reply on client → job `complete`, `attempts=1`. It is written on Day 2 and it fails loudly until it doesn't. No new design documents until it passes. (This one was already the last.)

### Phase 1 — Days 1–30: The loop runs, in time

*Make the core loop work with tempo and flow detection. Ship Readiness Gates 0–1 closed; Gate 2 opened.*

**Modules & work:**
- **Days 1–3, the bleeding:** shared-secret auth on `lucineer-memory` + `lucineer-vector`; `/api/diag` behind auth; fix the 401 (job ID is the capability — move `GET /api/job/:id` above the gate, and it dies anyway when polling does); processor claims jobs (one HTTP call); delete the push path; R2 binding + MOLT trajectory writer live. The trajectory writer goes this early because it is the only item where delay is unrecoverable.
- **Days 4–8, the hull:** delete `vibe-world/`; rebuild `default.project.json` to include the ten orphaned server systems and six client modules; fix what breaks (19,500 lines of Lua that have never been loaded — budget real days for this and expect some of it not to compile); smoke test written Day 2, green by Day 8.
- **Days 9–14, safety:** FilterGate chokepoint, fail-closed, all paths; Nemotron-Content-Safety stage in the brain (in-voice deflection on UNSAFE, commands dropped); per-player rate limiting; delete `addScript`; TextChatService migration.
- **Days 15–24, the clock:** `slackwater-tempo` into the processor (TempoMap staging the pipeline) and BeatClock into the DO; Luau BeatClock mirror + META tempo sync; BuildAnimator re-derived onto the 32nd-note grid; EnergyAdapter reading a minimal PerceptionCapture (action cadence + idle only) in **shadow mode Days 15–20, live Days 21+**; Governor computing Φ from the same minimal tracks, logged to trajectories, *not yet acting*.
- **Days 25–30, the character seam:** `--creative` in the production invocation; one persona constant; "friendly" instruction and `"Done! I built %d action(s)"` deleted; `markUnfinished` implemented (pitch 69 exists end to end); BondSystem's XP ladder torn out, behavior triggers in (keep the lines, throw away the meter).

**Tests:** the Studio smoke test (the gate); pytest for TempoMap↔pipeline staging and EnergyAdapter smoothing (extending the 275 across the four packages); Worker vitest for auth on all three services + lease claiming under two concurrent processors; red-team script of 50 adversarial prompts with zero raw model text reaching a client.

**Demo (Day 30):** one unbroken screen recording — a player types "build me a castle," the yard's tempo audibly rises with their input cadence, parts land on the grid with mass-pitched sound, Lucineer names the gap in voice, and the terminal shows Φ falling in real time. *The recording doubles as the first trajectory replay.*

**Ships:** nothing public. Gate 0 and Gate 1 checked, honestly, against the wire.

### Phase 2 — Days 31–60: The system gets senses

*Add perception, lattice, T-Minus, and the harmony governor. The substrate replaces the plumbing it shadowed.*

**Modules & work:**
- **T-Minus (Days 31–40):** WebSocket endpoint on the BuildCoordinator DO; predict/confirm/miss message set; prediction calibration from job history; client subscribe-once with reconnect-and-resubscribe; polling retained as fallback behind a flag, then removed Day 55 after two weeks of parity. Thinking choreography timed against `predictedTick`.
- **Perception (Days 36–48):** full PerceptionCapture — attention (camera), silence, gesture, intention tracks; channel-9 batching per beat over the WebSocket; IntentionPropagator pre-warm path into T-Minus; session recording as multi-track MIDI files to R2 (the replay system exists the day this lands, for free).
- **Lattice (Days 41–46):** `LatticeSnap` post-pass on all coder output; 60° rotation snap; Eisenstein coordinates in the CC payload spec; template library re-anchored to lattice points; creative-mode opt-out.
- **Harmony goes live (Days 47–56):** sandbox stage between plan and code, error masks flowing, Executive repairing collisions (fallibility pass-through tuned to let aesthetic misreads survive); Governor deadbands calibrated from 4+ weeks of shadow Φ in the trajectory data; **FlowStateProtector live** — suppression lists on the DO, tempo lock under Φ 0.05. Executive *improvisation* (rewriting intents, taking over builds) stays in shadow until Phase 3; protection ships before improvisation because doing nothing well is safer than doing something clever.
- **Days 57–60:** integration hardening; kill-switch to template-only mode; the five-metric telemetry dashboard (session length, time-to-first-build, flaw-callout rate, gap-completion rate, Day-2 return).

**Tests:** two-processor/one-job lease test promoted to CI; WebSocket drop/reconnect with prediction survival (the prediction lives in the DO, not the socket — prove it); lattice property tests (snap idempotence, neighbor distance exactness, zero float drift over 10⁶ operations); Φ regression suite replayed against recorded Phase 1 trajectories; sandbox catches 100% of seeded collisions while passing the seeded misread.

**Demo (Day 60):** two players on one server. Build requests resolve with **2 messages instead of ~120** (show the DO metrics); a deliberately slowed pipeline produces a `miss` and Lucineer measures twice with no spinner and no player-visible error; a session replay file renders the build back as audible music. And the flow demo: a player deep in a build, Φ on screen, Earl's interjection visibly queued and held until they surface.

**Ships:** friends-and-family playtest (Gate 2 checked; Gate 3 opened). First real players; first real trajectories; first Day-2 callbacks.

### Phase 3 — Days 61–90: One organism

*Unify everything, add casting-call routing, ship the MVP.*

**Modules & work:**
- **Casting-call (Days 61–70):** `cast()` API over the capability atlas; brain pipeline routes every stage through it; model tempo profiles registered with the TempoMap; first measured swap — Nemotron 3 Super vs. Seed-mini on intent, judged against the R2 trajectory set, loser demoted in the atlas, not in code.
- **Executive live (Days 66–75):** improvisation out of shadow — simplify/assist/take-over responses driven by Φ and stage; connectome-driven agent repairs (Earl resurfaces diegetically after measured decoupling); fleet-level flow measurement (is the *pipeline* in the pocket — handoff cadence regularity as the fleet's own groove).
- **Binary wire (Days 71–78):** SWMIDI-8 packing replaces the JSON envelope on edges 3, 7, 18; ~30× payload reduction, and the debugging synthesizer — route the bus to actual audio and *hear* a broken pipeline as dissonance. One afternoon of pure joy that is also a real observability tool.
- **MVP assembly (Days 76–90):** first-30-minutes flow (beam → build → tideline → craft → power → unfinished) run by five playtesters with zero hints; tide on the canonical 18 minutes (one number, one source of truth, ending the 18-vs-20 drift); Magic Moments 1, 3, 4; Build Cards; era gates 0→2; save system on the now-authenticated memory Worker; mid-tier phone at 30 fps with 16 players; Roblox compliance pass; cost ceiling load-tested and alarmed.

**Tests:** full Gate 0–4 checklist from the production design run as a release audit, each item verified the way Ship Readiness verified — against the wire, not the docs; casting-call A/B harness over trajectories; 90-minute soak with 16 synthetic players against the cost model; the five playtesters *are* the Gate 3 test.

**Demo (Day 90):** the MVP itself, plus one artifact for the record: a single session replayed as a multi-track MIDI file through a synthesizer — the castle as a composition, the player's channel as the drum line, the moment Φ dropped audible as the moment the music locks. That recording is the pitch deck, the keynote slide, and the proof, in one file.

**Ships:** the MVP — public playtest on Roblox. Gate 4 checked. The dataset compounding. The story ("a game about agents, built by agents, on the agents' own clock") published, because it requires no code and is already true.

### What is explicitly out of scope for the 90 days

Era 3–7 content, vibe-coding, autonomous Era-7 fleets, multiplayer beyond one shared server, voice synthesis (non-verbal vocalizations only), and the GRPO training loop (the *dataset* for it is in scope from Day 3; the training is not). The framework will tempt us to build the cathedral. The plan ships the chapel with a live organist in it.

---

## 5. THE ONE PARAGRAPH

Slackwater is a world where AI characters build alongside you — and the reason it feels different from every AI you've ever used is that everyone in it, human and machine, shares one clock. Every action — yours, the gruff master builder's, the tide's — is a note in the same piece of music: it lands on a beat, carries a weight, plays on someone's channel. When you speed up, the whole yard quickens with you; when you're deep in a build and everything is clicking, the system can *measure* that feeling — musicians call it being in the pocket — and its most advanced feature switches on, which is knowing when to leave you alone. Under the hood that takes twelve layers: exact math so agents never disagree about where things are, a musical protocol so every event knows its moment, a prediction engine so nothing ever asks "done yet?", and a routing brain that picks which AI model plays which part the way a bandleader picks who takes the solo. For an engineer, it's a tempo-synchronized multi-agent runtime with a measurable flow state. For an investor, it's the first game where the AI infrastructure *is* the retention mechanic. For Magnus: the robots in this game are a band, you're the drummer, and when you play, they listen.

---

*End of the Grand Plan. Twelve layers, sixteen channels, eight error bits, two messages per build, one clock. The counts are exact — and the first thirty days are for making the code agree with them.*
