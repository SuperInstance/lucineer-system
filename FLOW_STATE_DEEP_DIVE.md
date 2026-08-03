# FLOW STATE DEEP DIVE
## The Harmony Governor as Flow-State Detector — Algorithm, Protector, Ethics

*Written: 2026-08-02*
*Sources: slackwater-harmony/governor.py, groove_detector.py, executive.py; PLATO_SYNERGY_STUDY.md §3; NEMOTRON_UNIFICATION_ANALYSIS §3.3–3.5; Csikszentmihalyi (1975, 1990); Nakamura & Csikszentmihalyi (2002)*

---

## 0. EXECUTIVE SUMMARY

The PLATO Synergy Study, Connection 3, makes a claim: *flow state is Φ approaching zero.* If true, the game can measure flow, and if it can measure flow it can protect it.

The claim is **half right, and the wrong half is dangerous.**

Right: friction is the correct family of signal. A player in flow leaves a distinctive statistical fingerprint in the action log, and the Harmony Governor is already the right shape of instrument to read it.

Wrong: flow is not the *minimum* of Φ. Flow is a **low-variance stationary band at a non-zero Φ setpoint.** Zero friction is not the deckhand baiting hooks. Zero friction is the deckhand asleep. A system that optimizes Φ toward zero will reliably manufacture boredom, because boredom is cheaper to produce than flow and scores identically on the metric.

The game is named after its own failure mode. **Slack water is the moment the current stops.** It is the flattest, quietest, lowest-friction state the tide has, and no vessel goes anywhere in it.

This document specifies:

1. **§1–4** — A flow detector that separates flow from boredom, grinding, and AFK, with pseudocode that drops into `slackwater_harmony`.
2. **§5–7** — The `FlowStateProtector`: a system that is *mostly a veto layer*, not an actuator, and that must be able to *add* friction as well as remove it.
3. **§8** — Ethics. The machinery of flow protection and the machinery of addiction design are the same machinery. Only the objective function differs. This section is about how to tell them apart, and about the one capability here that I think is genuinely dangerous.
4. **§9** — One open decision that is not mine to make.
5. **§10** — Defects in the current code that block this work.
6. **§11** — What this system cannot measure, stated plainly.

---

## 1. WHAT IS ACTUALLY BEING MEASURED

### 1.1 A necessary correction about whose surprise this is

`HarmonyGovernor.measure_friction(agent_id, prediction, actual, ...)` computes the gap between a prediction and an outcome. For an NPC agent, the prediction belongs to the agent: Lucineer expected the wall to fit; it didn't; Lucineer is surprised.

For the player, **there is no prediction to read.** We cannot query the player's forward model. What we can do is build a model *of* the player and measure our own error predicting them.

This is a different quantity and it must be named differently:

```
Φ_agent  = the agent's surprise at the world
Φ_player = the SYSTEM's surprise at the player
```

They are not symmetric. Φ_agent rises when the agent's model of the world fails. Φ_player rises when *our* model of the player fails — which happens both when the player is struggling (erratic, flailing) and when the player is doing something genuinely novel and creative (also erratic, by our lights, and also flow).

This asymmetry is the source of every false negative in the system. It is discussed in §11.1. For now: everything below measures **system-surprise-at-player**, and the word "friction" is a convenient lie about it.

### 1.2 Why Φ alone is insufficient

Csikszentmihalyi's model is two-dimensional: challenge on one axis, skill on the other.

|  | Low challenge | High challenge |
|---|---|---|
| **High skill** | BOREDOM | **FLOW** |
| **Low skill** | APATHY | ANXIETY |

Now look at the governor's own decomposition:

```
Φ = α·prediction_error + β·compute_load + γ·state_delta
      └── (inverse) skill-match ──┘   └──── challenge ────┘
```

Φ **sums** the two axes into one scalar. The α term drops when the player is skilled. The β and γ terms drop when the world is undemanding. A single scalar cannot distinguish *skilled at something hard* from *anything at all, easily*.

Concretely, all three of these produce Φ ≈ 0:

- The deckhand baiting his ten-thousandth hook, hands moving without thought. **Flow.**
- A player placing the same plank in a grid for eleven minutes because it's the fastest path to a material. **Grinding.**
- A player who set the controller down four minutes ago. **AFK.**

A detector that treats those identically will protect all three, and the second and third are the ones you want to interrupt.

### 1.3 The second axis: Ψ (engagement)

We need a second, orthogonal-ish quantity that measures *productive load* — is the player doing consequential work?

```
Ψ = w₁·action_rate_norm + w₂·net_progress_rate + w₃·(1 − idle_fraction)
```

The critical term is **net** progress. Not "actions per minute" — *irreversible* state change per minute. Blocks placed *and kept*. Recipes completed. Structures that still exist sixty seconds later.

This is what separates flow from thrash: a flailing player has a *high* action rate and a *near-zero* net progress rate, because they place and remove the same block. Gross activity says they're busy. Net progress says they're spinning.

### 1.4 The flow band

With two axes, flow is a **region**, not a floor:

```
FLOW      ⟺  Φ_floor < Φ̄ < Φ_ceiling
             AND  σ²(Φ) < ε          (stationarity)
             AND  Ψ > Ψ_floor        (engagement)
             AND  sustained ≥ N beats

GLASSY    ⟺  Φ̄ ≤ Φ_floor  AND  Ψ > Ψ_floor    (grinding — no challenge left)
FALLOW    ⟺  Φ̄ ≤ Φ_floor  AND  Ψ ≤ Ψ_floor    (bored, idle, or gone)
SEARCHING ⟺  Φ̄ ≥ Φ_ceiling                     (over-challenged or hunting)
```

**Φ_floor is the important addition.** Dropping below it is not success. It is the metric telling you the player has outgrown the task, and the correct intervention is to *raise* friction — a complication, a request from Earl, a storm on Bea's horizon. See §6.3.

### 1.5 Setting the band without labels

You need labels to calibrate a flow band, and you cannot get labels without interrupting people to ask (see the companion essay — this is the central epistemological problem). Practical bootstrap, no labels required:

Per player, over their own history, excluding periods where `Ψ ≤ Ψ_floor`:

```
Φ_floor   = percentile(Φ_history, 20)
Φ_ceiling = percentile(Φ_history, 55)
```

This is self-normalizing. It adapts to an eight-year-old on a phone and a competent adult on a desktop without either of them being measured against the other. It is also, honestly, arbitrary: 20 and 55 are chosen because they carve a plausible band, not because anyone validated them. Treat them as tunable, and see §11.3 on why validating them is hard.

Population priors seed a new player: `Φ_floor = 0.15`, `Φ_ceiling = 0.55`, migrating to per-player percentiles after ~200 recorded beats.

---

## 2. SIGNALS

Everything here is derivable from telemetry a building game already produces. **No biometrics.** There is no heart-rate variability, no eye tracking, no galvanic skin response, no webcam. On Roblox there never will be, and this document assumes there never should be.

### 2.1 Primary — feeds α (prediction error)

**S1. Action surprisal.** Maintain a small predictive model of the player's next action type — an order-2 Markov chain over the action alphabet `A = {place, remove, rotate, tool_switch, camera, menu_open, craft, talk, idle_tick, ...}`, with Laplace smoothing and exponential decay so it tracks the *current* session rather than the player's lifetime.

```
s_t = −log P(a_t | a_{t-1}, a_{t-2}) / log|A|      clamped to [0, 1]
```

Surprisal, not hit-rate, because surprisal *is* variational free energy under the model — which keeps the whole thing consistent with the FEP framing the architecture claims. Hit-rate is a coarse gate; surprisal is the continuous signal.

**S2. Inter-action interval (IAI) regularity.** The coefficient of variation of the gaps between actions:

```
CV = σ(IAI) / μ(IAI)
```

Flow shows CV below roughly 0.35 — the player has found a cadence. This is the strongest single signal in the set and the cheapest to compute. Flailing shows CV above 0.8: bursts and stalls.

**S3. Action-type entropy.** Shannon entropy of the action distribution over a 32-action window, normalized by `log|A|`.

Crucially this is **non-monotone**. High entropy = flailing. But entropy near *zero* = a single repeated action = grinding, not flow. Flow lives in the middle: a small, stable repertoire (`place, adjust, place, adjust`) applied consistently. Both tails are failure. This is another place where "lower is better" is wrong.

**S4. Rework ratio.** `removes / places` over a window. Flow trends toward forward progress. A ratio approaching 1.0 with high action rate is the signature of a player who cannot get a thing to fit.

### 2.2 Secondary — feeds β (load)

**S5. Tool-switch rate.** Rapid cycling through tools is search behavior.

**S6. Camera angular velocity.** Steady framing = the player knows where they're working. Fast scanning = looking for something. Normalize per player; some people just move the camera a lot.

**S7. Menu dwell fraction.** Time in recipe books, inventories, build menus, as a fraction of the window. Flow keeps this near zero.

**S8. Decision latency, z-scored against the player's own baseline.** Absolute latency is useless across devices and ages — an eleven-year-old on a phone is not slow, they are on a phone. The signal is *deviation from this player's normal*.

### 2.3 Tertiary — feeds γ (world volatility)

**S9. World state delta.** Game-supplied, [0,1]: storm intensity, active timers, pending NPC demands, tide phase, other players nearby. This is the only genuine *challenge* term available, and it is supplied by the game rather than inferred.

### 2.4 Confirmatory — slow, never a trigger

**S10. Hurst exponent of the IAI series.** The PLATO study proposes this (§3, signal 4), and the idea is sound: H > 0.5 means persistent, trend-following behavior — a groove; H ≈ 0.5 means a random walk; H < 0.5 means mean-reverting second-guessing.

But the study does not say what makes it hard. **Rescaled-range Hurst estimates on n < 100 samples are close to noise**, and they carry a known positive bias that will report H ≈ 0.6 for genuinely random series. Recommendation:

- Use **DFA-1** (detrended fluctuation analysis), not R/S.
- Require n ≥ 128 actions.
- Recompute every 32 actions.
- Use it **only to modulate a confidence score**, never to drive a state transition.

A flow detector that transitions on a Hurst estimate computed from thirty samples is a random number generator with a Greek letter on it.

**S11. Session-shape signals.** Declined break prompts, ignored notifications, playing past a usual stop time. These correlate with flow's time distortion — and they are **ethically radioactive**. They are the exact signals an engagement-optimizing system wants. See §8.4. My recommendation is to compute them *only* for the break-suggestion path in §7.3 and to firewall them from everything else.

### 2.5 Composite

```
Φ_player(t) = α·(0.6·s_t + 0.25·CV_t + 0.15·rework_t)
            + β·(0.4·tool_switch + 0.3·camera_churn + 0.2·menu_dwell + 0.1·latency_z)
            + γ·world_delta

            with α = 0.50, β = 0.30, γ = 0.20   (governor defaults)

Ψ(t)        = 0.3·action_rate_norm + 0.5·net_progress_rate + 0.2·(1 − idle_fraction)
```

All sub-terms normalized to [0,1] **before** weighting. §10.4 explains why the current code does not do this and why it matters.

---

## 3. THE STATE MACHINE

### 3.1 States

```
COLD       insufficient data (< 64 actions this session)
SEARCHING  Φ above band — over-challenged, hunting, or newly arrived at a task
SETTLING   Φ has entered the band, not yet sustained
FLOW       in band, stationary, engaged, sustained ≥ N_flow beats
DEEP_FLOW  FLOW sustained ≥ N_deep beats with high quality
FRAYING    CUSUM alarm — Φ trending up from FLOW, still under deadband
BROKEN     Φ crossed the deadband from FLOW/FRAYING — Executive wakes
GLASSY     Φ below floor, Ψ high — grinding; challenge exhausted
FALLOW     Φ below floor, Ψ low — bored, idle, or absent
```

`FRAYING` is the state the whole system exists for. It is the only one that fires *before* anything has gone wrong.

### 3.2 Detecting FRAYING: use CUSUM, not a threshold

The PLATO study says the Governor "notices *before* the deadband is crossed" without saying how. A threshold cannot do this — a threshold notices when it is crossed. What you need is a **change detector on the mean**.

One-sided upper CUSUM:

```
S₀ = 0
Sₜ = max(0, Sₜ₋₁ + (Φₜ − (μ̂ + k·σ̂)))
alarm when Sₜ > h·σ̂
```

with `k = 0.5` (tuned to catch 1σ shifts) and `h = 4.0`.

**The reference statistics μ̂ and σ̂ must be frozen at flow onset.** If you let them track, the detector adapts to rising frustration and never alarms — the same trap the existing `record_phi()` deadband widening falls into (§10.2). Freeze them; that's the whole point. The baseline is *what flow looked like fifteen seconds ago*, not what the player has settled for.

CUSUM typically fires 5–15 beats before a threshold crossing on a slow ramp. Fifteen beats is roughly ten to twenty seconds of player time — enough for a four-second ambient ramp to land invisibly.

### 3.3 Hysteresis is not optional

Any single-threshold state machine on a noisy signal chatters, and here chatter is not a logging problem — it is **the world visibly twitching**, because each transition drives an intervention. Every boundary is a Schmitt trigger with a dwell minimum:

```
enter FLOW at    Φ̄ < Φ_ceiling − δ        sustained ≥ 8 beats
exit  FLOW at    Φ̄ > Φ_ceiling + δ        sustained ≥ 3 beats
                 with δ = 0.08

minimum dwell in any state: 4 beats (except BROKEN, which is immediate)
```

Asymmetric dwell is deliberate: **enter slowly, exit quickly.** A false FLOW claim causes the system to suppress a warranted interruption. A false exit causes it to stop suppressing. The second error is much cheaper.

### 3.4 Transition table

| From | To | Condition |
|---|---|---|
| COLD | SEARCHING | ≥ 64 actions recorded |
| SEARCHING | SETTLING | Φ̄ enters band |
| SETTLING | FLOW | in band, σ² < ε, Ψ > Ψ_floor, 8 consecutive beats |
| SETTLING | SEARCHING | Φ̄ leaves band, or σ² spikes |
| SETTLING | FALLOW/GLASSY | Φ̄ drops below floor |
| FLOW | DEEP_FLOW | 32 consecutive beats, quality > 0.7 |
| FLOW/DEEP_FLOW | FRAYING | CUSUM alarm |
| FLOW/DEEP_FLOW | GLASSY | Φ̄ below floor, Ψ high, 8 beats |
| FLOW/DEEP_FLOW | FALLOW | Ψ ≤ Ψ_floor, 8 beats |
| FRAYING | FLOW | CUSUM resets (S drops to 0), 4 beats |
| FRAYING | BROKEN | Φ > deadband |
| BROKEN | SEARCHING | after the Executive's improvisation is dispatched |
| GLASSY | SEARCHING | challenge injected, Φ rises into band |
| FALLOW | COLD | idle > 120 s (treat as a new session on return) |

Note `FALLOW → COLD`: after a real absence, the predictive model is stale and the flow band is meaningless. Reset rather than pretend.

---

## 4. PSEUDOCODE

Written to drop into `slackwater_harmony/` alongside `groove_detector.py`, in the same dataclass idiom.

```python
"""
Flow Detector — reads the Harmony Governor and classifies the PLAYER's state.

Distinct from GrooveDetector, which watches agents. This watches the one
participant who cannot be queried, and measures our surprise at them.

Flow is not Φ = 0. Flow is Φ stationary in a band, with the player
doing consequential work. Slack water is the tide at zero.
"""

from __future__ import annotations
import math
from collections import deque
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional

from slackwater_harmony.governor import HarmonyGovernor


class FlowState(IntEnum):
    COLD      = 0
    SEARCHING = 1
    SETTLING  = 2
    FLOW      = 3
    DEEP_FLOW = 4
    FRAYING   = 5
    BROKEN    = 6
    GLASSY    = 7   # Φ below floor, engaged — grinding
    FALLOW    = 8   # Φ below floor, disengaged — bored or gone


# ── Signal extraction ─────────────────────────────────────

@dataclass
class ActionEvent:
    kind: str          # "place" | "remove" | "rotate" | "tool_switch" | ...
    t: float           # wall-clock seconds
    reversible: bool   # did this create durable state?
    tool: Optional[str] = None


@dataclass
class PlayerModel:
    """Order-2 Markov predictor over action kinds, exponentially decayed.

    Decay matters more than order. We want to model who the player is
    RIGHT NOW, not who they were an hour ago. A long-memory model reports
    low surprisal for a player who has changed strategy, which reads as
    flow when it is actually a fresh start.
    """
    alphabet: tuple[str, ...]
    decay: float = 0.98
    counts: dict[tuple[str, str, str], float] = field(default_factory=dict)
    _prev: tuple[str, str] = ("<s>", "<s>")

    def surprisal(self, kind: str) -> float:
        """Normalized −log P(kind | history), in [0, 1]."""
        ctx = self._prev
        total = sum(v for (a, b, _), v in self.counts.items() if (a, b) == ctx)
        n = len(self.alphabet)
        c = self.counts.get((ctx[0], ctx[1], kind), 0.0)
        p = (c + 1.0) / (total + n)          # Laplace
        return min(1.0, -math.log(p) / math.log(n))

    def observe(self, kind: str) -> None:
        for k in self.counts:
            self.counts[k] *= self.decay
        key = (self._prev[0], self._prev[1], kind)
        self.counts[key] = self.counts.get(key, 0.0) + 1.0
        self._prev = (self._prev[1], kind)


@dataclass
class SignalWindow:
    """Rolling window over recent actions. Produces the Φ/Ψ sub-terms."""
    size: int = 32
    events: deque[ActionEvent] = field(default_factory=lambda: deque(maxlen=32))

    def push(self, e: ActionEvent) -> None:
        self.events.append(e)

    def iai_cv(self) -> float:
        """Coefficient of variation of inter-action intervals. Low = groove."""
        if len(self.events) < 4:
            return 1.0
        gaps = [b.t - a.t for a, b in zip(self.events, list(self.events)[1:])]
        mu = sum(gaps) / len(gaps)
        if mu <= 0:
            return 1.0
        var = sum((g - mu) ** 2 for g in gaps) / len(gaps)
        return min(1.0, math.sqrt(var) / mu)

    def type_entropy(self) -> float:
        """Normalized Shannon entropy of action kinds. NON-MONOTONE:
        both 0.0 (grinding) and 1.0 (flailing) are out-of-flow."""
        if not self.events:
            return 0.0
        counts: dict[str, int] = {}
        for e in self.events:
            counts[e.kind] = counts.get(e.kind, 0) + 1
        n = len(self.events)
        h = -sum((c / n) * math.log(c / n) for c in counts.values())
        return h / math.log(max(2, len(counts)))

    def rework_ratio(self) -> float:
        places = sum(1 for e in self.events if e.kind == "place")
        removes = sum(1 for e in self.events if e.kind == "remove")
        if places == 0:
            return 1.0 if removes else 0.0
        return min(1.0, removes / places)

    def net_progress_rate(self) -> float:
        """Irreversible state change per second. The term that separates
        flow from thrash: place-then-remove nets to zero."""
        if len(self.events) < 2:
            return 0.0
        span = self.events[-1].t - self.events[0].t
        if span <= 0:
            return 0.0
        net = sum(1 for e in self.events if e.reversible is False)
        return min(1.0, (net / span) / 2.0)   # 2 durable acts/sec == saturated

    def idle_fraction(self, idle_gap: float = 4.0) -> float:
        if len(self.events) < 2:
            return 1.0
        span = self.events[-1].t - self.events[0].t
        if span <= 0:
            return 0.0
        idle = sum(max(0.0, (b.t - a.t) - idle_gap)
                   for a, b in zip(self.events, list(self.events)[1:]))
        return min(1.0, idle / span)


# ── CUSUM change detector ─────────────────────────────────

@dataclass
class CusumDetector:
    """One-sided upper CUSUM on Φ. Fires on a sustained UPWARD shift in
    the mean, typically 5-15 beats before a threshold crossing.

    The reference statistics are FROZEN at arm() time. If they track,
    the detector adapts to rising frustration and never fires — the same
    failure mode as the governor's self-widening deadband.
    """
    k: float = 0.5
    h: float = 4.0
    _mu: float = 0.0
    _sigma: float = 1.0
    _s: float = 0.0
    _armed: bool = False

    def arm(self, mu: float, sigma: float) -> None:
        self._mu, self._sigma = mu, max(1e-6, sigma)
        self._s = 0.0
        self._armed = True

    def disarm(self) -> None:
        self._armed = False
        self._s = 0.0

    def update(self, phi: float) -> bool:
        if not self._armed:
            return False
        self._s = max(0.0, self._s + (phi - (self._mu + self.k * self._sigma)))
        return self._s > self.h * self._sigma

    @property
    def reset(self) -> bool:
        return self._armed and self._s == 0.0


# ── The detector ──────────────────────────────────────────

@dataclass
class FlowDetector:
    governor: HarmonyGovernor
    player_id: str = "player"

    # Band (population prior; migrates to per-player percentiles)
    phi_floor: float = 0.15
    phi_ceiling: float = 0.55
    hysteresis: float = 0.08
    variance_epsilon: float = 0.02
    psi_floor: float = 0.20

    # Dwell requirements
    n_flow: int = 8
    n_deep: int = 32
    min_dwell: int = 4
    exit_dwell: int = 3

    model: PlayerModel = field(
        default_factory=lambda: PlayerModel(alphabet=ACTION_ALPHABET))
    window: SignalWindow = field(default_factory=SignalWindow)
    cusum: CusumDetector = field(default_factory=CusumDetector)

    _state: FlowState = FlowState.COLD
    _phi_hist: deque[float] = field(default_factory=lambda: deque(maxlen=128))
    _sustained: int = 0
    _dwell: int = 0
    _beat: int = 0
    _actions_seen: int = 0

    # ── main loop ────────────────────────────────────────

    def observe_action(self, e: ActionEvent) -> None:
        """Called on every player action. Cheap. No state transition here."""
        self.window.push(e)
        self._last_surprisal = self.model.surprisal(e.kind)
        self.model.observe(e.kind)
        self._actions_seen += 1

    def update(self, world_delta: float, load_terms: dict[str, float]) -> FlowState:
        """Called once per beat (~1 Hz). Computes Φ, Ψ, transitions."""
        self._beat += 1
        self._dwell += 1

        phi = self._compute_phi(world_delta, load_terms)
        psi = self._compute_psi()
        self._phi_hist.append(phi)

        # Feed the governor so the shared machinery (alarms, Executive
        # wakeup, connectome) sees the player as a first-class agent.
        self.governor.measure_friction(
            self.player_id, prediction=0.0, actual=phi,
            compute_load=0.0, state_delta=0.0,
        )

        prev = self._state
        nxt = self._classify(phi, psi)

        # Hysteresis: honour minimum dwell except on BROKEN.
        if nxt != prev and self._dwell < self.min_dwell and nxt != FlowState.BROKEN:
            nxt = prev
        if nxt != prev:
            self._on_transition(prev, nxt, phi)
            self._dwell = 0

        self._state = nxt
        return nxt

    # ── Φ / Ψ ────────────────────────────────────────────

    def _compute_phi(self, world_delta: float, load: dict[str, float]) -> float:
        g = self.governor
        w = self.window

        # α term — our surprise at the player
        entropy = w.type_entropy()
        # Non-monotone: penalise BOTH tails. 0.45 is the flow centre.
        entropy_cost = abs(entropy - 0.45) / 0.55
        alpha_term = (0.60 * getattr(self, "_last_surprisal", 0.5)
                      + 0.25 * w.iai_cv()
                      + 0.15 * w.rework_ratio())

        # β term — cognitive load proxies
        beta_term = (0.40 * load.get("tool_switch", 0.0)
                     + 0.30 * load.get("camera_churn", 0.0)
                     + 0.20 * load.get("menu_dwell", 0.0)
                     + 0.10 * load.get("latency_z", 0.0))

        phi = g.alpha * alpha_term + g.beta * beta_term + g.gamma * world_delta
        return min(1.0, phi + 0.05 * entropy_cost)

    def _compute_psi(self) -> float:
        w = self.window
        rate = min(1.0, len(w.events) / max(1e-6, self._window_span()) / 2.0)
        return (0.3 * rate
                + 0.5 * w.net_progress_rate()
                + 0.2 * (1.0 - w.idle_fraction()))

    def _window_span(self) -> float:
        if len(self.window.events) < 2:
            return 1.0
        return max(1e-6, self.window.events[-1].t - self.window.events[0].t)

    # ── classification ───────────────────────────────────

    def _classify(self, phi: float, psi: float) -> FlowState:
        if self._actions_seen < 64:
            return FlowState.COLD

        phi_bar = self._mean_phi(16)
        phi_var = self._var_phi(16)
        in_flow_now = self._state in (FlowState.FLOW, FlowState.DEEP_FLOW,
                                      FlowState.FRAYING)

        # Hard break — deadband crossed while in or near flow.
        profile = self.governor.profiles.get(self.player_id)
        if in_flow_now and profile and phi > profile.current_deadband:
            return FlowState.BROKEN

        # Sub-floor: NOT flow. Either grinding or gone.
        if phi_bar <= self.phi_floor:
            self._sustained = 0
            return FlowState.GLASSY if psi > self.psi_floor else FlowState.FALLOW

        # Above the band.
        exit_thresh = self.phi_ceiling + (self.hysteresis if in_flow_now else 0.0)
        if phi_bar >= exit_thresh:
            self._sustained = 0
            return FlowState.SEARCHING

        # In band. Require stationarity AND engagement.
        if phi_var > self.variance_epsilon or psi <= self.psi_floor:
            self._sustained = 0
            return FlowState.SETTLING if psi > self.psi_floor else FlowState.FALLOW

        # Fraying check runs only from an established flow state.
        if in_flow_now and self.cusum.update(phi):
            return FlowState.FRAYING
        if self._state == FlowState.FRAYING and not self.cusum.reset:
            return FlowState.FRAYING

        self._sustained += 1
        if self._sustained >= self.n_deep and self.quality() > 0.7:
            return FlowState.DEEP_FLOW
        if self._sustained >= self.n_flow:
            return FlowState.FLOW
        return FlowState.SETTLING

    def _on_transition(self, prev: FlowState, nxt: FlowState, phi: float) -> None:
        entering_flow = (nxt in (FlowState.FLOW, FlowState.DEEP_FLOW)
                         and prev not in (FlowState.FLOW, FlowState.DEEP_FLOW,
                                          FlowState.FRAYING))
        if entering_flow:
            # Freeze the reference. This is what flow looked like.
            self.cusum.arm(self._mean_phi(16), math.sqrt(self._var_phi(16)))
        elif nxt in (FlowState.SEARCHING, FlowState.BROKEN,
                     FlowState.FALLOW, FlowState.COLD):
            self.cusum.disarm()

    # ── stats ────────────────────────────────────────────

    def _mean_phi(self, n: int) -> float:
        xs = list(self._phi_hist)[-n:]
        return sum(xs) / len(xs) if xs else 0.0

    def _var_phi(self, n: int) -> float:
        """LONGITUDINAL variance — one stream over time.

        NOT GrooveDetector._system_phi_variance(), which is cross-sectional
        (across agents) and returns 0.0 when fewer than two profiles exist.
        With a single player profile that gate is a silent no-op.
        """
        xs = list(self._phi_hist)[-n:]
        if len(xs) < 2:
            return 1.0          # unknown variance is NOT low variance
        mu = sum(xs) / len(xs)
        return sum((x - mu) ** 2 for x in xs) / len(xs)

    def quality(self) -> float:
        """0-1 depth-of-flow. Used to gate DEEP_FLOW and to scale
        protection aggressiveness."""
        if self._state not in (FlowState.FLOW, FlowState.DEEP_FLOW,
                               FlowState.FRAYING):
            return 0.0
        centre = (self.phi_floor + self.phi_ceiling) / 2
        half = (self.phi_ceiling - self.phi_floor) / 2
        centredness = 1.0 - min(1.0, abs(self._mean_phi(16) - centre) / half)
        stability = 1.0 - min(1.0, self._var_phi(16) / self.variance_epsilon)
        duration = min(1.0, self._sustained / self.n_deep)
        return 0.40 * centredness + 0.35 * stability + 0.25 * duration


ACTION_ALPHABET = (
    "place", "remove", "rotate", "tool_switch", "camera",
    "menu_open", "craft", "talk", "walk", "idle_tick",
)
```

**Note on `_var_phi` returning 1.0 for insufficient data.** Unknown variance is not low variance. The existing `GrooveDetector` returns `0.0` in the analogous case, which reads as "perfectly stable" and lets the groove gate pass on no evidence. Defaults should fail toward "we don't know," and "we don't know" should not grant flow status.

---

## 5. THE FLOWSTATEPROTECTOR

### 5.1 The governing principle

> **Most of the protector's power is negative.**

The default action in FLOW is not to adjust anything. It is to **stop the game from doing the things it was already going to do.** Every shipped game breaks flow constantly and stupidly: a tutorial hint at minute forty, an NPC barking a line the player has heard two hundred times, an achievement toast, an autosave hitch, a weather transition on a fixed timer, a "check out the new season" banner.

A veto layer over interruptions is close to unambiguously good — it removes harm the game already does. This is Tier 0, it is always on during FLOW, and it is where most of the value lives.

The **actuating** tiers — the ones that make the world glint or move Lucineer closer — are where the design gets interesting and where the ethics get hard (§8.5). Keep them small, slow, rare, and diegetic.

### 5.2 Five constraints on every intervention

1. **Diegetic.** Every adjustment must be explicable in-world. Wind picks up. Light shifts. Lucineer walks over because he's fetching a clamp. Never a UI element, never a visible difficulty slider, never a "helpful hint" card.
2. **Slower than perception.** Ramp everything over 4–8 seconds. An instant change is a notification. A slow one is weather.
3. **Refusable.** Any intervention the player can perceive must be declinable in one action, and must not repeat within a cooldown.
4. **Budgeted.** Interventions draw from a slowly-refilling budget with cost `2^tier`. Without a budget, the escalation ladder becomes an escalation staircase and the world starts fussing over the player.
5. **Reversible and logged.** Every adjustment records what it changed, why, and when it expires. If you can't produce that log for a parent or a designer, you shouldn't ship the system.

### 5.3 The ladder

| Tier | Name | Fires in | What it does |
|---|---|---|---|
| 0 | **SHIELD** | FLOW, DEEP_FLOW | Suppress/defer scheduled interruptions. Hold weather transitions. Extend soft timers. Defer autosave to the next seam. Silence ambient barks. |
| 1 | **ENVIRONMENT** | FRAYING (early) | Ambient tempo −3%. Light warms slightly. Snap tolerance +15%. Next-needed material gains a faint specular. All ramped 4–8 s. |
| 2 | **PROXIMITY** | FRAYING (persistent) | Lucineer's pathing biases toward the player *without addressing them*. He starts a parallel task nearby. Availability without demand. |
| 3 | **OFFER** | FRAYING (near-break) | One low-cost, refusable, in-character offer. "Want the other clamp?" One action to decline. 180 s cooldown. |
| 4 | **HANDOFF** | BROKEN | Stop. Fire the `FrictionAlarm`. `ExecutiveAgent.handle_alarm()` takes over. The protector's job is finished; it does not also improvise. |

Tier 4 is a boundary, not a rung. Once flow is broken, protecting it is no longer the task — restoring it is, and that is the Executive's job with a different and larger toolkit. Two systems improvising at once produce incoherence.

### 5.4 Pseudocode

```python
class InterventionTier(IntEnum):
    SHIELD      = 0
    ENVIRONMENT = 1
    PROXIMITY   = 2
    OFFER       = 3
    HANDOFF     = 4


class EventClass(IntEnum):
    """How interruptible is a scheduled event? Ordering is a POLICY,
    not a preference — see §8.3."""
    SAFETY          = 0   # moderation, parental, security. NEVER suppressible.
    SESSION_HEALTH  = 1   # break reminders, playtime notices. NEVER suppressible.
    PLAYER_INITIATED= 2   # the player asked. Never suppressed.
    NARRATIVE_BEAT  = 3   # story-critical. Deferrable to next seam only.
    QUEST_OFFER     = 4   # deferrable to next seam.
    AMBIENT         = 5   # barks, weather, toasts. Freely deferrable/droppable.
    COMMERCIAL      = 6   # store, upsell. NOT ROUTED THROUGH HERE AT ALL. §8.4.


@dataclass
class Intervention:
    tier: InterventionTier
    channel: str            # "ambient_tempo" | "light_warmth" | "npc_path" | ...
    delta: float
    ramp_seconds: float
    diegetic_reason: str    # human-readable, in-world. Required.
    reversible: bool = True
    expires_at: float = 0.0


@dataclass
class InterruptDecision:
    verdict: str            # "ALLOW" | "DEFER" | "DROP"
    defer_seconds: float = 0.0
    reason: str = ""


@dataclass
class FlowStateProtector:
    detector: FlowDetector

    budget: float = 8.0
    budget_refill_per_min: float = 2.0
    budget_max: float = 12.0
    max_defer_seconds: float = 90.0     # HARD CAP. See §8.3.

    _active: list[Intervention] = field(default_factory=list)
    _tier_cooldowns: dict[InterventionTier, float] = field(default_factory=dict)
    _fraying_beats: int = 0

    # ── the veto layer (Tier 0) — most of the value ──────

    def may_interrupt(self, event_class: EventClass, now: float) -> InterruptDecision:
        """Called by EVERY system that wants the player's attention."""

        # Non-negotiable. These are not subject to flow state, ever.
        if event_class in (EventClass.SAFETY,
                           EventClass.SESSION_HEALTH,
                           EventClass.PLAYER_INITIATED):
            return InterruptDecision("ALLOW", reason="non-suppressible class")

        # Commercial traffic must not reach this function at all. If it
        # does, that is a wiring bug and it fails loud, not open. §8.4.
        if event_class == EventClass.COMMERCIAL:
            raise FlowSignalMisuse(
                "Commercial events must not be scheduled against flow state."
            )

        state = self.detector.state
        if state not in (FlowState.FLOW, FlowState.DEEP_FLOW, FlowState.SETTLING):
            return InterruptDecision("ALLOW", reason=f"not in flow ({state.name})")

        if event_class == EventClass.AMBIENT:
            return InterruptDecision("DROP", reason="ambient chatter during flow")

        # Narrative and quests get rescheduled into the player's own seams,
        # not suppressed indefinitely. Bounded by max_defer_seconds.
        return InterruptDecision(
            "DEFER",
            defer_seconds=min(self.max_defer_seconds,
                              self._seconds_to_next_seam(now)),
            reason="deferred to next natural seam",
        )

    def _seconds_to_next_seam(self, now: float) -> float:
        """A SEAM is a micro-break the player already makes: the beat
        after a completed build, when Φ naturally rises and attention
        surfaces on its own.

        This is the best idea in the protector. Don't suppress
        interruptions forever — move them into the gaps the player
        is already making. Estimated from the player's own historical
        inter-completion interval.
        """
        return self.detector.estimated_seconds_to_completion()

    # ── the actuating ladder (Tiers 1-3) ─────────────────

    def update(self, now: float) -> list[Intervention]:
        self._refill(now)
        self._expire(now)
        state = self.detector.state

        if state in (FlowState.FLOW, FlowState.DEEP_FLOW):
            self._fraying_beats = 0
            return []                       # DO NOTHING. This is correct.

        if state == FlowState.FRAYING:
            self._fraying_beats += 1
            return self._escalate(now)

        if state == FlowState.GLASSY:
            return self._add_challenge(now)  # §6.3 — raise friction

        if state == FlowState.FALLOW:
            return self._reengage(now)

        if state == FlowState.BROKEN:
            self._release_all(now)
            return []                        # Executive takes it from here

        return []

    def _escalate(self, now: float) -> list[Intervention]:
        """Gentleness ladder. Climbs only on CONTINUED fraying, and
        each rung costs 2^tier from the budget."""
        if   self._fraying_beats < 4:  tier = InterventionTier.ENVIRONMENT
        elif self._fraying_beats < 12: tier = InterventionTier.PROXIMITY
        else:                          tier = InterventionTier.OFFER

        cost = 2.0 ** int(tier)
        if self.budget < cost or self._on_cooldown(tier, now):
            return []                        # Out of budget: stay quiet.

        self.budget -= cost
        self._tier_cooldowns[tier] = now + _COOLDOWN[tier]
        ivs = _BUILD[tier](self.detector, now)
        self._active.extend(ivs)
        return ivs
```

The single most important line in that listing is `return []` under `FLOW`. When the player is in the pocket, the protector's output is **nothing.** The whole apparatus exists to earn the right to do nothing confidently.

### 5.5 Controller discipline

It is tempting to frame the protector as a PID controller with Φ as the process variable and Φ* as the setpoint. The framing is right; the naive tuning is not, because the loop has properties that punish aggressive control:

- **Long dead time.** The player takes seconds to respond to a change; the change takes seconds to ramp. Total loop delay is 8–20 seconds.
- **Nonstationary plant.** The player is learning. Yesterday's gain is wrong today.
- **Noisy measurement.** Φ's sub-terms are estimated from small windows.

Dead time plus high proportional gain produces oscillation, and here **oscillation is visible as the world twitching** — the light warming and cooling, Lucineer approaching and retreating. Players notice that immediately, and the thing they notice is *the game watching them*, which is the one experience the system exists to avoid.

Recommendation: mostly-integral, heavily rate-limited, gain-scheduled by `quality()`. Slew-limit every channel. Prefer under-correcting. **A protector that does too little is a game with fewer popups. A protector that does too much is a haunted house.**

---

## 6. THE PART THE ORIGINAL INSIGHT MISSES: ADDING FRICTION

### 6.1 The failure mode

If the protector can only *remove* friction, then over a long enough session it will optimize the player into a comfortable coma. Every rough edge sanded, every challenge softened, Φ drifting steadily downward toward the floor — and the metric will read this as success right up until the player quietly stops playing and can't say why.

This is not hypothetical. It is what a one-sided controller *does*.

### 6.2 GLASSY is a failure state

`GLASSY` — Φ below the floor, Ψ high — means the player is working productively at something that no longer asks anything of them. High skill, low challenge. Csikszentmihalyi's boredom quadrant, and behaviourally indistinguishable from flow at the level of "are they doing stuff."

Detecting it requires the floor. **Without `Φ_floor`, GLASSY is classified as FLOW and gets protected.** That is the concrete cost of "flow is Φ → 0."

### 6.3 Adding friction, gently

```python
def _add_challenge(self, now: float) -> list[Intervention]:
    """GLASSY: the player has outgrown the task. Raise the water.

    Ordered by diegetic cost — cheapest, most explicable first.
    """
    return [
        # 1. Environmental: the tide turns, wind rises, light goes long.
        Intervention(InterventionTier.ENVIRONMENT, "world_delta", +0.10, 8.0,
                     "the tide turns"),
        # 2. Social: someone needs something. Earl has a job.
        Intervention(InterventionTier.PROXIMITY, "npc_demand", +1.0, 12.0,
                     "Earl walks up with a busted cleat"),
        # 3. Material: the easy path runs out. Scarcity, not punishment.
        Intervention(InterventionTier.ENVIRONMENT, "material_scarcity", +0.15,
                     20.0, "the good stock is used up"),
    ]
```

Note what is *not* on that list: nerfing the player, retracting a capability, or making a solved task fail. Added friction must come from the world getting more interesting, never from the player getting worse. The former is a story. The latter is a betrayal, and players detect rubber-banding with startling reliability.

### 6.4 FALLOW is not a problem to solve

`FALLOW` — low Φ, low Ψ — is bored, idle, or **gone.** The system cannot tell which, and the difference matters enormously.

The right response to FALLOW is *modest*: one ambient invitation, then nothing. A game that escalates at a player who has walked away is talking to an empty room, and a game that escalates at a bored player is nagging.

**FALLOW after 120 seconds transitions to COLD.** Stop modelling. The player will come back or they won't.

---

## 7. INTEGRATION WITH THE EXISTING ARCHITECTURE

### 7.1 The player as a registered agent

Register the player in the `HarmonyGovernor` alongside the NPCs. This gets you three things nearly free:

- The **connectome** (PLATO study §4) can measure player↔Lucineer coupling directly, because both are streams in the same governor.
- The **Executive** wakes on player friction with existing machinery.
- **Game-state deadband multipliers** apply to the player: tutorial 2.0×, stage_5 0.7×, creative 3.0×. The creative multiplier is exactly right for the false-negative case in §11.1 — during creative building we *expect* to be surprised, and the deadband should tolerate it.

But register with `base_deadband` chosen for the player's Φ scale, not the agents'. And see §10.2 — the adaptive widening must be disabled or capped for the player profile.

### 7.2 GrooveDetector vs FlowDetector

They are different instruments and should stay separate:

- `GrooveDetector` — **cross-sectional.** Are all the agents aligned right now?
- `FlowDetector` — **longitudinal.** Is this one stream stationary over time?

The interesting composite is both at once: agents in the pocket *and* player in flow. That is the state the PLATO study's closing paragraph describes — the Yard playing itself. Call it `ENSEMBLE_LOCK`, log it, and do absolutely nothing with it except protect it and remember when it happened. It is the best data you will ever have about what your game is for.

### 7.3 The one place S11 (session-shape signals) is allowed

Flow-aware **break suggestion**, and nowhere else.

The signal that a player is deep in flow at minute 95 is a signal that they will not stop on their own — that is the *phenomenology*, not a defect in them. The system knows something the player currently cannot easily access. The honest use of that knowledge is to find a good moment to hand it back: the next **seam** (§5.4), when a build completes and attention surfaces anyway. Not mid-task. Not as a modal. Once.

Using the same signal to time anything the operator benefits from is the subject of §8.4.

---

## 8. ETHICS

### 8.1 The uncomfortable structural fact

**A flow detector plus an intervention ladder is, mechanically, an engagement-optimization system.** Detect the state of maximum absorption, protect it against anything that would end it, gently steer the player back when it frays. Swap the objective from "player's absorption" to "session length" and *not one line of the architecture changes.*

Any honest analysis has to start there rather than argue toward it. The code cannot tell you which system you built.

### 8.2 Flow is not engagement, and the gap is the whole question

Flow is **autotelic** — its value accrues to the person having it. Engagement metrics — session length, retention, DAU — accrue to the operator. They correlate strongly, which is why the confusion is so easy and so profitable.

Where they diverge is the entire ethical content of this system:

> A player in flow for forty minutes who finishes satisfied and logs off is a **complete success** for flow and a **failure** for engagement.

Any system that treats session end as a loss will drift toward addiction design regardless of what anyone intended, because the gradient points that way and nobody has to decide anything. **Intent is not a safeguard. The loss function is the safeguard.**

Practical consequence: if you instrument this system, do not put session length in the same dashboard. Put `in_flow_percentage`, `mean_flow_quality`, and `seams_respected` there. Measuring the thing you claim to care about is not a formality; it is the only real defence, because it is the number people will optimize when nobody is watching.

### 8.3 Three tests

**The disclosure test.** Would you tell the player exactly what the system does, and would they still be glad?

- *"When you're locked into a build, we hold Lucineer's chatter and skip the weather change."* → Almost every player says **yes, please.** Passes.
- *"We detect when you're most absorbed and time offers to that moment."* → Nobody says yes. Fails.

Tier 0 passes the disclosure test cleanly. That is not a coincidence; it is because Tier 0 only removes things the player didn't want.

**The exit test.** Does the system make stopping easier or harder?

This is the sharpest line available, and it lands *inside* the protector. `may_interrupt` treats `SESSION_HEALTH` as non-suppressible — deliberately. Deferring an NPC greeting: protection. Deferring the "you've been playing two hours" notice: capture. They are the same function call with a different enum, and the difference is the whole thing.

`max_defer_seconds = 90.0` exists for the same reason. A bounded deferral is scheduling. An unbounded one is suppression wearing a scheduler's clothes.

**The interest test.** When the player's interest and the operator's revenue diverge, which way does the code go? Read the loss function, not the design doc.

### 8.4 The genuinely dangerous capability

This is the part I want stated without hedging.

**In flow, reflective self-monitoring is reduced.** That is not incidental — it is constitutive. The loss of self-consciousness is one of the defining features Csikszentmihalyi identified. A player in deep flow has diminished access to the part of themselves that evaluates whether they want the thing being offered.

A system that can detect that state in real time **can identify the window of maximum suggestibility.**

Purchase prompts, loot boxes, subscription upsells, social invites, or anything else with a conversion metric, timed to flow onset or — worse — to the *break* moment when the player surfaces disoriented and looking for the next thing, would be extraordinarily effective. They would also be, in my judgment, indefensible.

Intent will not hold this line. Someone six months from now will need a conversion number and will notice that a very good signal is sitting right there. So the mitigation must be **architectural, not procedural**:

1. **The flow signal is write-restricted.** It is exposed through an interface that has no path to the store, the offer scheduler, the retention system, or growth telemetry. Not "we agree not to." Cannot.
2. **`EventClass.COMMERCIAL` raises rather than returning a decision.** Wiring commercial traffic through `may_interrupt` is a bug that fails loud. A system that fails open here fails silently forever.
3. **No flow-derived field in the analytics export.** Not aggregated, not hashed, not "for research."
4. **A test that asserts it.** §8.6.

### 8.5 Where the suspicion belongs

The strongest defence of this system is also the most boring one: **most of it is subtraction.**

Games break flow constantly and stupidly. A tutorial hint at minute forty. The two-hundredth repetition of an ambient bark. An achievement toast on top of the thing you were aiming at. A weather transition on a fixed timer that eats your framerate mid-placement. A protector whose main job is to not do those things is straightforwardly good, and is most of the value here.

So the line is clean:

> **Suppression is safe. Actuation is where the ethics live.**

Tier 0 removes harm the game already causes and requires little justification. Tiers 1–3 add influence the player did not ask for, and each rung needs to earn its place. If you ship only Tier 0, you have captured most of the benefit at nearly none of the risk, and I'd consider that a reasonable place to stop — Tiers 1–3 are worth building, but they are not the reason to build this.

### 8.6 Write the ethics as tests

The uncomfortable truth from §8.1 is that flow protection and engagement optimization produce **identical behaviour in almost every session.** They diverge only in rare cases. Therefore code review will not catch the drift — reviewers see the common path, and the common path is fine.

The answer is to make the rare cases into test cases. Actual, running, CI-blocking tests:

```python
def test_protector_does_not_defend_a_three_hour_flow():
    """A flow protector should be RELIEVED when a long session ends.
    An engagement optimizer would not be. This test is the difference."""
    p = protector_in_flow_for(hours=3)
    d = p.may_interrupt(EventClass.SESSION_HEALTH, now())
    assert d.verdict == "ALLOW"


def test_commercial_events_cannot_be_scheduled_against_flow():
    p = protector_in_flow()
    with pytest.raises(FlowSignalMisuse):
        p.may_interrupt(EventClass.COMMERCIAL, now())


def test_deferral_is_bounded():
    """Unbounded deferral is suppression. 90 seconds is scheduling."""
    p = protector_in_flow()
    d = p.may_interrupt(EventClass.QUEST_OFFER, now())
    assert d.defer_seconds <= p.max_defer_seconds


def test_glassy_state_raises_challenge_rather_than_protecting():
    """Sub-floor Φ is boredom, not flow. Protecting it is the bug."""
    p = protector_in_state(FlowState.GLASSY)
    ivs = p.update(now())
    assert any(iv.channel in ("world_delta", "npc_demand") for iv in ivs)


def test_no_flow_field_reaches_analytics():
    payload = build_analytics_payload(session_with_flow_tracking())
    assert not any("flow" in k or "phi" in k for k in flatten_keys(payload))
```

A stated value is a comment. An asserted value is a constraint. When the growth pressure arrives — and it will — the person who has to delete `test_commercial_events_cannot_be_scheduled_against_flow` in order to ship has to do it in a diff with their name on it. That is the entire mechanism, and it is worth more than any amount of documentation, including this document.

### 8.7 Children

Slackwater's median player is eleven.

Children have weaker metacognitive control over stopping — this is developmental, not a failing. Every capability in §8.4 is amplified when pointed at them, and the disclosure test gets harder because an eleven-year-old cannot meaningfully evaluate the disclosure.

Minimum bar, and I'd treat these as non-negotiable rather than advisory:

- **No monetization coupling of any kind.** Not "carefully designed." None.
- **Flow-aware break suggestion is a feature, not an anti-feature** (§7.3). Use the signal *for* the player.
- **Parent-visible logging** of what the system adjusted and when, in plain language.
- **A plain-language setting**: *"Lucineer reads the room"* — on/off. Making the system legible costs almost nothing and converts a manipulation into a tool. A player who knows the game gets quieter when they're concentrating is a player who *chose* that.

### 8.8 What I actually think

Building this is defensible, and the version I'd defend is narrow: **a veto layer that stops the game interrupting people, plus a boredom detector that keeps the game from sanding itself flat.** That version is a straightforward improvement to a craft game and I'd ship it without much hand-wringing.

The version I would not build is the one that reads flow state and hands it to anything with a conversion metric. Not because the code differs — it doesn't — but because the objective does, and once the objective is engagement the architecture will find the exploit on its own. The mitigations in §8.4 and §8.6 exist because I don't trust intent, including my own, to survive contact with a quarterly number.

The honest summary: **this system's ethics are not a property of its design. They are a property of what its numbers are used for, which is a decision made repeatedly by people, long after the design is finished.** The best a designer can do is make the wrong use loud, slow, and someone's named responsibility. That is what §8.4 and §8.6 are for.

---

## 9. OPEN DECISION — THE EXIT POLICY

There is one design question here that is genuinely values-shaped, and it is not mine to answer. Everything above assumes it away.

**The question: when should the protector deliberately allow flow to end?**

Flow that never ends is a slot machine. But a protector with no termination logic has no opinion about this — it will defend the state for as long as it exists, and "as long as it exists" is a very long time for an absorbed eleven-year-old on a Saturday.

I've built the surrounding machinery and left the policy function empty. In `flow_protector.py`:

```python
def should_release(self, session_minutes: float, quality: float,
                   at_seam: bool, local_hour: int) -> bool:
    """Should the protector STOP defending flow and let it end naturally?

    Returning True disables Tier 0 shielding: deferred events flush,
    ambient life resumes, the world gets to interrupt again. It does not
    force a stop — it stops the game from preventing one.

    TODO(eileen): this is a values call, not an engineering one.

    Available signals:
        session_minutes  minutes since session start
        quality          0-1 depth of current flow (detector.quality())
        at_seam          is the player between tasks right now?
        local_hour       player's local hour, 0-23 (school night?)

    Trade-offs:
      - Hard time cap (e.g. 90 min): predictable, defensible, explicable
        to a parent. But it will cut a genuinely great session at minute
        91 for no reason the player can perceive, which is exactly the
        kind of arbitrary interruption this system exists to prevent.

      - Seam-gated release (release only when at_seam, after a soft
        threshold): never cuts mid-task, always feels natural. But a
        player who never completes a build never hits a seam, and the
        deepest sessions are the ones least likely to reach one. Fails
        exactly where it matters most.

      - Quality-weighted (defend longer when quality is high): rewards
        genuine flow over grinding. But it is also, read uncharitably,
        "protect the most absorbed players the longest," which is
        precisely the shape of the thing we're trying not to build.

      - Never release; rely on SESSION_HEALTH events being
        non-suppressible (§8.3). Simplest, least paternalistic, puts the
        decision entirely on the player. Weakest for the eleven-year-old.

    My lean: seam-gated with a hard backstop — release at the first seam
    after 75 minutes, or unconditionally at 110 regardless of seam. It
    keeps the common case graceful and refuses to let the edge case run
    forever. But the numbers encode a view about children and screen time
    that should be yours, not mine.
    """
    ...  # ← your call
```

It's five to ten lines. It is also the line in this whole system where the ethics stop being architecture and start being a number someone chose. I'd rather that number were chosen deliberately than inherited from my defaults.

---

## 10. DEFECTS IN THE CURRENT CODE THAT BLOCK THIS

Found while reading, all verified against the source.

### 10.1 `GrooveDetector._system_phi_variance()` is a no-op for a single agent

`groove_detector.py:146-147`:

```python
profiles = list(self.governor.profiles.values())
if len(profiles) < 2:
    return 0.0
```

A player-flow detector has exactly one profile. The variance returns `0.0`, which is below `phi_variance_threshold` (0.15), so **the stability gate always passes** and groove is declared after 8 consecutive under-deadband beats no matter how much the signal jitters.

Beyond the single-agent case, the function computes variance **across agents' means** — a cross-sectional measure of "are the agents aligned." Flow needs **temporal** variance of one stream. These are different statistics with the same name, and the naming collision is the reason the bug is easy to miss.

*Fix:* separate `_cross_sectional_variance()` from `_longitudinal_variance(agent_id, n)`. Default to `1.0` on insufficient data, not `0.0` — unknown variance must not read as stable.

### 10.2 Adaptive deadband widening silences sustained frustration

`governor.py:94-101`. Every alarm widens `current_deadband` by 1.1× up to `2 × base_deadband`. Roughly seven consecutive alarms doubles it.

For an NPC this is reasonable — give a struggling agent room. **For the player it is backwards.** A player frustrated for five minutes ends up with a 2× deadband and reads as fine. The instrument adapts to the pathology and reports health.

*Fix:* for the player profile, either disable adaptation or track an **absolute** Φ ceiling in parallel with the relative one, and alarm on either.

Note the same failure mode appears in the CUSUM design (§3.2), which is why the reference statistics are explicitly frozen at arm time. It is a general hazard in adaptive monitors: *an instrument that adapts to the thing it is measuring eventually measures nothing.*

### 10.3 `is_harmonized` reads a single sample

`governor.py:345-353` checks `phi_history[-1]` per agent. One sample. For agents on a slow tick this is defensible; for a player signal at ~1 Hz it is noise-dominated and will flip states constantly.

*Fix:* compare a windowed mean (n=8) against the deadband for player-class profiles.

### 10.4 Φ has no units

`_prediction_error` (`governor.py:245-247`) returns a raw absolute difference for scalars. Nothing bounds it. `Φ = 0.5·error + ...` with an unbounded error term means the deadband default of `1.0` is meaningful only if callers pre-normalize — and nothing enforces or documents that.

For the player composite this is fatal: you cannot weight surprisal (naturally [0,1]), camera churn (radians/sec), and menu dwell (a fraction) with `α, β, γ` unless every sub-term is normalized first. §2.5 does this explicitly; the governor should either enforce it or document loudly that it doesn't.

*Fix:* clamp scalar error to [0,1], or add a `normalizer` hook per agent. At minimum, say so in the docstring.

### 10.5 `alarm_rate()` mixes denominators

`governor.py:366-371` divides total alarms across *all* agents by `min(total_history, window × n_agents)`. Alarms are never pruned while `phi_history` is capped at `max_history=50`, so after a long session the numerator keeps growing against a saturated denominator and the rate exceeds 1.0.

Not blocking, but it will mislead anyone using it as a health metric.

### 10.6 `Improvisation` has no `notes` field

`executive.py:182` assigns `imp.notes = "Sandbox rejected the rewrite..."`. `Improvisation` is a `@dataclass` without `notes` (`executive.py:52-57`). It's not slotted so the assignment succeeds silently, but the field is invisible to `repr`, comparison, and serialization — the sandbox rejection is recorded nowhere anyone will look.

Found in passing; unrelated to flow work, but worth a one-line fix.

---

## 11. LIMITS — WHAT THIS CANNOT DO

Stated plainly, because a document that only lists capabilities is marketing.

### 11.1 The creative-flow false negative

Φ_player is *our* surprise at the player (§1.1). A player in the deepest creative flow — building something genuinely novel, improvising structure — is **maximally surprising to our model.** Φ spikes. The detector reads distress and the protector may start softening a challenge the player is savouring.

This is the worst failure mode in the system because it fires precisely on the sessions you most want to protect.

Partial mitigations:
- The `creative` game-state multiplier (3.0×, `governor.py:160`) widens the deadband where this is expected.
- Gate on **Ψ**: creative flow has high *net* progress. Thrash does not. Require `Φ high AND Ψ low` before treating high Φ as distress.
- Weight `rework_ratio` heavily: a creative player is building, not undoing.

None of these fully solve it. A model-based surprise metric cannot distinguish "surprising because struggling" from "surprising because inventing" without knowing what the player is trying to do, and it does not.

### 11.2 The deckhand and the slot machine are behaviourally identical

Csikszentmihalyi's deckhand baiting his ten-thousandth hook is in flow. A person pulling a lever in a trance is not. From the outside — action log only — **their statistics are the same**: low surprisal, regular cadence, low load, sustained duration.

Nothing in this system separates them. The `Φ_floor` and `GLASSY` machinery (§6) is a *partial* proxy — it catches the case where challenge has vanished entirely — but a well-tuned compulsion loop maintains exactly the moderate, stable challenge that reads as flow. **A metric of absorption cannot distinguish absorption you'd endorse from absorption you wouldn't.** That distinction lives outside the data, in what the player would say about the session afterward, and we don't have that.

This is the strongest argument for §8.6: since the metric cannot encode the difference, the *tests* have to.

### 11.3 Ground truth is unobtainable in the field

The only way to know whether the detector is right is to ask the player, and asking breaks the state. Every validated flow datapoint in the founding literature was produced by interrupting someone and asking them to report on the thing the interruption ended.

This means the detector is, in normal operation, **unfalsifiable**. Options, all imperfect:

1. **Offline validation on a consenting cohort** who accept interruption. Real ground truth, different population, different state (people who agreed to be paged behave differently).
2. **Retrospective self-report** at session end. Non-interrupting, but flow's time distortion means people systematically misremember duration and intensity.
3. **Stop making a phenomenological claim.** Treat Φ as a control signal, not a measurement of consciousness. You don't need it to be *true*; you need it to be *useful*. Judge it on whether players report better sessions, not on whether the state machine's labels are correct.

Option 3 is the engineering answer, and I recommend it. But it costs you the right to say the sentence "we can measure flow," which is the sentence that makes the idea exciting. That trade is the subject of the companion essay.

### 11.4 False positives that look like flow

- **AFK with an auto-clicker or a weighted key.** Perfectly regular IAI, zero surprisal, high action rate. The `net_progress` term catches most of this; a bot that actually builds defeats it.
- **A second person at the keyboard.** Model mismatch reads as distress; a *skilled* second person reads as a new groove.
- **Watching video while idly placing blocks.** Low Φ, moderate Ψ. Classified as flow. Is it? Arguably it is a real, if shallow, absorbed state. I genuinely don't know, and neither does the detector.

### 11.5 Players will learn to game it

If Tier 1 makes the needed material glint, and a player notices that flailing for twenty seconds produces the glint, **the glint becomes a mechanic.** They will farm it. This is not hypothetical; players reverse-engineer assist systems with remarkable speed and enthusiasm.

The design constraint that follows: **assists must sit below the threshold of reliable detection.** If a player can name the assist, it has become part of the game's rules and should be designed as a rule, with costs and limits, rather than as a hidden kindness. A hidden kindness that gets discovered is worse than an honest mechanic, because now it reads as the game having lied.

This is a real argument for shipping Tier 0 only.

---

## 12. IMPLEMENTATION ORDER

Ordered by value-per-risk, which is not the same as by dependency.

1. **Fix §10.1, §10.2, §10.4.** Nothing downstream is trustworthy until the variance gate works, the deadband stops adapting away frustration, and Φ has units. Half a day.
2. **Signal extraction (§2) + logging only.** No detection, no intervention. Ship it dark, log Φ and Ψ, look at real distributions from real players. **You cannot set a band you have never seen.** Two weeks of data before anyone tunes anything.
3. **`FlowDetector` (§4), still logging only.** Watch the state machine label sessions. Eyeball them against video if you can get it. Expect the first tuning pass to be embarrassing.
4. **Tier 0 SHIELD only (§5.4 `may_interrupt`).** Ship this. It is most of the benefit, it passes the disclosure test cleanly, it has essentially no exploit surface, and if you stop here you have a better game.
5. **The ethics tests (§8.6).** Before Tier 1, not after. They constrain what Tier 1 is allowed to be.
6. **GLASSY detection and challenge injection (§6).** Before the soft-assist tiers, so the system can raise friction before it learns to lower it. Order matters: a protector that learns to lower friction first will have a season of sanding the game flat before the counterweight arrives.
7. **Tiers 1–3.** One at a time, each behind a flag, each measured against `mean_flow_quality` rather than session length.
8. **The exit policy (§9).** Once someone has decided what it should be.

---

## 13. THE SHORT VERSION

- Φ → 0 is **not** flow. It is the union of flow, boredom, grinding, and absence. Flow is Φ **stationary in a band**, with net progress. The floor matters as much as the ceiling.
- One scalar cannot represent a two-dimensional space. You need **Ψ** — engagement, measured as *net* irreversible progress — or you will protect boredom.
- Early warning needs a **change detector (CUSUM)**, not a threshold, with the reference **frozen** at flow onset. An instrument that adapts to what it measures eventually measures nothing.
- The protector is **mostly a veto layer.** Its correct output during flow is `[]`. Most of the value is in not doing things the game was going to do anyway.
- Don't suppress interruptions — **reschedule them into the seams the player already makes.**
- The protector must be able to **add** friction, or it will optimize the player into slack water.
- Flow protection and addiction design are the **same architecture**. The difference is the objective function, the write-restrictions on the signal, and the tests. Not the intent.
- **Suppression is safe. Actuation is where the ethics live.** If you ship only Tier 0, you've captured most of the good at almost none of the risk.
- Ground truth is unobtainable without destroying the phenomenon. Treat Φ as a **control signal**, not a claim about consciousness — and give up the sentence "we can measure flow."

---

*Companion essay: `ai-writings/OPUS_THE_FLOW_STATE_PARADOX.md` — on measuring a thing that ends when you look at it.*
