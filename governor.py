"""
Governor Φ — Phase 1 shadow-mode friction governor.

Computes Φ (flow friction) from perception tracks.
SHADOW MODE: logs Φ but does not act on it.

Per the Grand Plan §4 Phase 1 Days 15-24:
    "Governor computing Φ from the same minimal tracks, logged to
     trajectories, not yet acting."

And §1 Layer 6:

    Φ(t) = 0.35·H(action entropy) + 0.25·idle + 0.30·error_rate + 0.10·help_requests

In Phase 1, we compute a simplified Φ from minimal tracks:
    - action_cadence (from EnergyAdapter)
    - idle_time
    - error_rate (build failures, mismatches)
    - stage (which pipeline stage we're in)

The Φ values are logged to the trajectory but never used to trigger
Executive actions. This is the calibration period: we collect Φ data
to set deadbands for Phase 2.

Usage::

    governor = Governor()
    phi = governor.observe({
        "action_cadence": 12,
        "idle_time": 2.0,
        "error_rate": 0.0,
        "stage": "code",
    })
    print(f"Φ = {phi:.3f}")  # logged, not acted upon

Author: Lucineer build system
Date: 2026-08-02
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Optional

# Try to import slackwater_harmony's FlowStateDetector for future integration.
# Fall back gracefully if not available — the Governor works standalone
# in Phase 1 shadow mode.
try:
    from slackwater_harmony import FlowStateDetector, HarmonyGovernor
    _HARMONY_AVAILABLE = True
except Exception:
    _HARMONY_AVAILABLE = False


# ── Φ formula weights (from Grand Plan §1 Layer 6) ──────────────────────────

WEIGHT_ENTROPY = 0.35     # H(action entropy)
WEIGHT_IDLE = 0.25         # idle fraction
WEIGHT_ERROR = 0.30        # error rate
WEIGHT_HELP = 0.10         # help requests

# Normalization: max possible Φ with all terms at maximum
PHI_MAX = WEIGHT_ENTROPY + WEIGHT_IDLE + WEIGHT_ERROR + WEIGHT_HELP  # = 1.0

# Deadband thresholds (from Grand Plan §1 Layer 6)
# These are NOT acted on in shadow mode. They are logged for calibration.
DEADBAND_STAGE = {
    "intent":  2.0,   # Wide — intent parsing is forgiving
    "plan":    1.5,
    "code":    1.0,
    "voice":   0.5,   # Tight — voice should be smooth
    "idle":    3.0,   # Widest — idle is relaxed
}

# Below this Φ, the system is approaching "the pocket"
PHI_POCKET = 0.15

# Below this Φ, the system is in deep flow
PHI_DEEP_FLOW = 0.05


# ── Shadow log entry ─────────────────────────────────────────────────────────

@dataclass
class PhiEntry:
    """A single Φ observation in shadow mode.

    Records the Φ value and the tracks that produced it.
    This is the calibration dataset for setting deadbands
    in Phase 2.
    """
    timestamp: float
    phi: float
    tracks: dict
    deadband: float
    would_alarm: bool
    in_pocket: bool
    in_deep_flow: bool
    reason: str = ""


# ── The Governor ─────────────────────────────────────────────────────────────

class Governor:
    """Computes Φ (flow friction) from perception tracks.

    SHADOW MODE: logs Φ but does not act on it.

    The Governor is the system's awareness of cognitive friction.
    In Phase 1, it observes and records. In Phase 2, its observations
    will drive the Executive: waking it when Φ exceeds the deadband,
    suppressing it when Φ drops into the pocket.

    The Φ formula from the Grand Plan:

        Φ(t) = 0.35·H(action entropy)
             + 0.25·idle
             + 0.30·error_rate
             + 0.10·help_requests

    Each term is normalized to [0, 1]:

    - **Action entropy**: Shannon entropy of action types.
      Low entropy (repetitive actions) = low friction = focused.
      High entropy (scattered actions) = high friction = confused.

    - **Idle**: fraction of time spent idle.
      Low idle = engaged. High idle = lost or bored.

    - **Error rate**: fraction of actions that failed.
      Zero errors = smooth. High errors = something is wrong.

    - **Help requests**: frequency of help-seeking behavior.
      Zero = self-sufficient. High = struggling.

    For Phase 1, we compute a simplified version from the minimal
    tracks available: action_cadence, idle_time, error_rate, and stage.

    Attributes:
        phi_history: All Φ readings.
        shadow_log: Full Φ observation log with context.
    """

    def __init__(self):
        """Initialize the Governor in shadow mode."""
        self.phi_history: list[float] = []
        self.shadow_log: list[PhiEntry] = []

        # Track action types for entropy calculation
        self._action_types: list[str] = []
        self._max_history: int = 1000

        # Optional: harmony integration for Phase 2
        self._harmony_governor: Optional[HarmonyGovernor] = None
        if _HARMONY_AVAILABLE:
            # We create a HarmonyGovernor but don't use it for decisions.
            # It's here so we can cross-validate our Φ against the full
            # harmony implementation.
            try:
                self._harmony_governor = HarmonyGovernor()
                self._harmony_governor.register_agent("lucineer", base_deadband=1.0)
            except Exception:
                self._harmony_governor = None

    # ── Observation ──────────────────────────────────────────────────

    def observe(self, tracks: dict) -> float:
        """Feed perception tracks, get Φ back.

        Args:
            tracks: A dictionary of perception signals. Expected keys
                    for Phase 1 (all optional, defaults applied):

                - action_cadence: float — actions per minute
                - idle_time: float — seconds since last action
                - error_rate: float — 0.0 to 1.0
                - help_requests: int — count in recent window
                - stage: str — current pipeline stage
                - matched: bool — whether keyword matched
                - command_count: int — commands in current build
                - action_type: str — category of current action

        Returns:
            Φ value (0.0 = deep flow, 1.0 = max friction).

        In shadow mode, the returned Φ is for logging only.
        No Executive is triggered.
        """
        now = time.time()

        # Extract tracks with defaults
        action_cadence = tracks.get("action_cadence", 0.0)
        idle_time = tracks.get("idle_time", 0.0)
        error_rate = tracks.get("error_rate", 0.0)
        help_requests = tracks.get("help_requests", 0)
        stage = tracks.get("stage", "idle")
        matched = tracks.get("matched", True)
        command_count = tracks.get("command_count", 0)
        action_type = tracks.get("action_type")

        # Track action types for entropy
        if action_type:
            self._action_types.append(action_type)
            if len(self._action_types) > self._max_history:
                self._action_types.pop(0)

        # ── Compute Φ terms ─────────────────────────────────────────

        # Term 1: Action entropy (0.0 = perfectly focused, 1.0 = scattered)
        entropy = self._compute_action_entropy()

        # Term 2: Idle fraction (0.0 = active, 1.0 = fully idle)
        idle_fraction = self._compute_idle_fraction(idle_time)

        # Term 3: Error rate (already 0.0-1.0)
        # A mismatched keyword is a mild error
        effective_error = error_rate
        if not matched:
            effective_error = max(effective_error, 0.3)

        # Term 4: Help requests (normalized)
        help_normalized = min(1.0, help_requests / 3.0)

        # Weighted sum
        phi = (
            WEIGHT_ENTROPY * entropy
            + WEIGHT_IDLE * idle_fraction
            + WEIGHT_ERROR * effective_error
            + WEIGHT_HELP * help_normalized
        )

        # Clamp
        phi = max(0.0, min(PHI_MAX, phi))

        # Store
        self.phi_history.append(phi)
        if len(self.phi_history) > self._max_history:
            self.phi_history.pop(0)

        # Determine context
        deadband = DEADBAND_STAGE.get(stage, 1.0)
        would_alarm = phi > deadband
        in_pocket = phi < PHI_POCKET
        in_deep_flow = phi < PHI_DEEP_FLOW

        # Build reason string
        reasons = []
        if entropy > 0.5:
            reasons.append(f"high entropy ({entropy:.2f})")
        if idle_fraction > 0.5:
            reasons.append(f"idle ({idle_fraction:.2f})")
        if effective_error > 0.3:
            reasons.append(f"errors ({effective_error:.2f})")
        if help_normalized > 0.3:
            reasons.append(f"help ({help_normalized:.2f})")
        if not reasons:
            reasons.append("smooth")
        reason = ", ".join(reasons)

        # Log to shadow log
        entry = PhiEntry(
            timestamp=now,
            phi=phi,
            tracks=dict(tracks),  # copy
            deadband=deadband,
            would_alarm=would_alarm,
            in_pocket=in_pocket,
            in_deep_flow=in_deep_flow,
            reason=reason,
        )
        self.shadow_log.append(entry)

        return phi

    # ── Φ term computations ─────────────────────────────────────────

    def _compute_action_entropy(self) -> float:
        """Compute normalized Shannon entropy of recent action types.

        Low entropy (repetitive actions) = focused = low Φ.
        High entropy (many different actions) = scattered = high Φ.

        Returns:
            Normalized entropy [0.0, 1.0].
        """
        if len(self._action_types) < 2:
            return 0.0  # Not enough data — assume focused

        # Count frequencies
        counts: dict[str, int] = {}
        for action in self._action_types:
            counts[action] = counts.get(action, 0) + 1

        n = len(self._action_types)
        entropy = 0.0
        for count in counts.values():
            p = count / n
            if p > 0:
                entropy -= p * math.log2(p)

        # Normalize by max possible entropy
        max_entropy = math.log2(len(counts)) if len(counts) > 1 else 1.0
        if max_entropy == 0:
            return 0.0

        return entropy / max_entropy

    def _compute_idle_fraction(self, idle_seconds: float) -> float:
        """Convert idle time to a [0, 1] fraction.

        Maps:
            0s idle      → 0.0 (fully engaged)
            10s idle     → 0.3 (slight idle)
            30s idle     → 0.7 (clearly idle)
            60s+ idle    → 1.0 (fully idle)

        This is a smooth mapping, not a step function.

        Edge cases: a negative idle time is a clock artifact (the last action
        timestamp is in the future) — clamp to fully engaged (0.0) rather than
        punishing the agent for clock skew. Infinite idle means the agent has
        truly stopped — that is fully idle (1.0). NaN must never poison Φ.
        """
        if idle_seconds < 0:
            return 0.0
        if idle_seconds == float('inf'):
            return 1.0
        if idle_seconds != idle_seconds:  # NaN
            return 0.0
        # Sigmoid-like mapping centered at 15 seconds
        return 1.0 / (1.0 + math.exp(-(idle_seconds - 15.0) / 8.0))

    # ── Queries ─────────────────────────────────────────────────────

    @property
    def current_phi(self) -> float:
        """Most recent Φ reading."""
        return self.phi_history[-1] if self.phi_history else 0.0

    @property
    def avg_phi(self) -> float:
        """Average Φ over all observations."""
        if not self.phi_history:
            return 0.0
        return sum(self.phi_history) / len(self.phi_history)

    @property
    def in_pocket(self) -> bool:
        """True if the most recent Φ is below the pocket threshold."""
        return self.current_phi < PHI_POCKET

    @property
    def in_deep_flow(self) -> bool:
        """True if the most recent Φ is below the deep flow threshold."""
        return self.current_phi < PHI_DEEP_FLOW

    def get_shadow_summary(self) -> dict:
        """Summarize the shadow log for trajectory reporting."""
        if not self.shadow_log:
            return {
                "observations": 0,
                "avg_phi": 0.0,
                "max_phi": 0.0,
                "min_phi": 0.0,
                "alarms": 0,
                "pocket_time": 0.0,
            }

        phis = [e.phi for e in self.shadow_log]
        alarms = sum(1 for e in self.shadow_log if e.would_alarm)
        pocket = sum(1 for e in self.shadow_log if e.in_pocket)
        deep = sum(1 for e in self.shadow_log if e.in_deep_flow)

        return {
            "observations": len(self.shadow_log),
            "avg_phi": sum(phis) / len(phis),
            "max_phi": max(phis),
            "min_phi": min(phis),
            "would_alarm_count": alarms,
            "pocket_count": pocket,
            "deep_flow_count": deep,
            "pocket_fraction": pocket / len(self.shadow_log),
        }

    # ── CNS v3 telemetry hook ────────────────────────────────────────

    def emit_telemetry(self, role: str = "lucineer-governor") -> str | None:
        """Emit a CNS v3 pulse derived from current governor state.

        Production implementations should call this from observe() once
        per observation cycle. The shared helper handles packet formatting
        and CNS bus write atomics.
        """
        try:
            from lucineer.cns_telemetry import TelemetryQuantum, emit_cns_pulse
        except Exception:
            return None

        phi = self.current_phi
        now = time.time()
        idle_seconds = (now - self._action_types[-1]) if self._action_types else 0.0

        temperature = phi * 5.0
        idle_fraction = self._compute_idle_fraction(idle_seconds)
        last_entry = self.shadow_log[-1] if self.shadow_log else None
        last_validation = last_entry.timestamp if last_entry else ""

        tq = TelemetryQuantum(
            agent_id="governor-1",
            gamma=0.5,
            eta=0.25,
            delta=0.25,
            temperature=temperature,
            semantic_distance=0.5,
            melt_pressure=0.0,
            max_crystallization_rate=0.0,
            deterministic=False,
            molt_count=0,
            capability=1.0 - idle_fraction,
            tau=phi,
            timestamp=datetime.now(timezone.utc).isoformat(),
            is_dreaming=idle_fraction > 0.8,
            temperature_idle=idle_seconds / 60.0,
            temperature_task=1.0 - temperature / 5.0,
            time_since_validation_seconds=now - last_validation if last_validation else 0.0,
            molt_phase="stable",
            creative_value=0.5,
            kappa_delta=0.0,
        )
        return emit_cns_pulse(
            agent_id="governor-1",
            telemetry=tq,
            role=role,
            model="lucineer-governor",
        )

    def __repr__(self) -> str:
        mode = "SHADOW"
        phi = self.current_phi
        state = "deep_flow" if self.in_deep_flow else ("pocket" if self.in_pocket else "normal")
        return (
            f"Governor({mode} Φ={phi:.3f}, state={state}, "
            f"observations={len(self.phi_history)})"
        )
