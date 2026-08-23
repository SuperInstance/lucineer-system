"""
EnergyAdapter — Phase 1 shadow-mode energy adapter.

Reads player action cadence + idle time. Adjusts system tempo based
on player energy. SHADOW MODE: logs adjustments but does not apply them yet.

This is the processor-side companion to slackwater-tempo's EnergyAdapter.
Where the slackwater-tempo version reads PlayerBehavior snapshots and
drives a TempoMap directly, this version is simpler: it reads raw
action timestamps and computes what the BPM *would* be, logging
everything for offline calibration.

Per the Grand Plan §4 Phase 1 Days 15-24:
    "EnergyAdapter reading a minimal PerceptionCapture
     (action cadence + idle only) in shadow mode Days 15-20,
     live Days 21+"

The shadow log is the calibration dataset. By Day 21 we'll know:
- What action rates correspond to which BPM feels right
- How much smoothing is needed
- What the idle thresholds should be

Usage::

    adapter = EnergyAdapter(base_bpm=72)
    adapter.record_action(time.time())   # player did something
    adapter.record_idle(time.time())     # player is idle
    print(adapter.get_bpm())             # still returns base_bpm
    print(adapter.shadow_log)            # but look at what it WOULD do

Author: Lucineer build system
Date: 2026-08-02
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional


# ── Constants ────────────────────────────────────────────────────────────────

# BPM ranges for each tempo marking, matching the Grand Plan
BPM_ALLEGRO = 120     # Fast — intent parse, high-energy building
BPM_MODERATO = 100    # Moderate — planning
BPM_ANDANTE = 80      # Walking — code gen, steady building
BPM_ADAGIO = 60       # Slow — voice, personality, idle contemplation
BPM_LARGO = 40        # Very slow — cold start, deep idle

# How far back to look for action cadence (seconds)
CADENCE_WINDOW = 30.0

# Idle threshold: if no action for this many seconds, player is "idle"
IDLE_THRESHOLD = 10.0

# Deep idle: player has been idle for a while
DEEP_IDLE_THRESHOLD = 30.0

# BPM smoothing rate (how fast tempo changes). Lower = smoother.
# The Grand Plan says 5-10 seconds for transitions.
# This is the per-second rate at which shadow BPM moves toward target.
SMOOTHING_TAU = 7.0   # time constant in seconds

# Minimum BPM change to log (avoid jitter in the shadow log)
MIN_LOG_CHANGE = 2.0


# ── Shadow log entry ─────────────────────────────────────────────────────────

@dataclass
class ShadowEntry:
    """A single shadow-mode observation.

    Records what the EnergyAdapter WOULD do if it were live.
    This is the calibration dataset.
    """
    timestamp: float
    old_bpm: float
    new_bpm: float
    target_bpm: float
    cadence: float          # actions per minute in the window
    idle_seconds: float     # seconds since last action
    reason: str             # human-readable explanation


# ── The EnergyAdapter ────────────────────────────────────────────────────────

class EnergyAdapter:
    """Reads player action cadence + idle time.

    Adjusts system tempo based on player energy.
    SHADOW MODE: logs adjustments but does not apply them yet.

    In shadow mode:
    - get_bpm() always returns base_bpm (the system doesn't change)
    - shadow_log records what the BPM WOULD be if we were live
    - The shadow log is the calibration data for going live on Day 21

    The adaptation logic:

        Fast cadence (many actions/minute) → speed up toward Allegro
        Moderate cadence                    → hold at Moderato/Andante
        Slow cadence / idle                 → slow down toward Adagio/Largo

    The mapping uses the same energy model as slackwater-tempo:
    action rate maps to energy [0,1], energy maps to BPM.

    Attributes:
        base_bpm: The anchor BPM. Shadow mode never deviates from this.
        current_bpm: The shadow BPM (what it WOULD be if live).
        action_history: Timestamps of recorded actions.
        last_action_time: When the player last did something.
        shadow_log: Full history of shadow-mode adjustments.
    """

    def __init__(self, base_bpm: float = 72.0):
        """Initialize the energy adapter.

        Args:
            base_bpm: The anchor tempo. In shadow mode, get_bpm()
                      always returns this value.
        """
        self.base_bpm: float = float(base_bpm)
        self.current_bpm: float = float(base_bpm)
        self._target_bpm: float = float(base_bpm)

        self.action_history: list[float] = []
        self.last_action_time: Optional[float] = None
        self._last_shadow_time: float = time.time()

        self.shadow_log: list[ShadowEntry] = []
        self._last_logged_bpm: float = float(base_bpm)

        # Cap history to prevent unbounded growth
        self._max_history: int = 1000

    # ── Recording ──────────────────────────────────────────────────

    def record_action(self, timestamp: Optional[float] = None):
        """Record a player action (build command, chat, etc.).

        Args:
            timestamp: When the action occurred. Defaults to now.
        """
        if timestamp is None:
            timestamp = time.time()

        self.action_history.append(timestamp)
        self.last_action_time = timestamp

        # Trim history
        if len(self.action_history) > self._max_history:
            self.action_history = self.action_history[-self._max_history:]

        self._adapt(timestamp)

    def record_idle(self, timestamp: Optional[float] = None):
        """Record that the player is idle (no action for >threshold).

        This is called periodically (e.g., every poll cycle) so the
        adapter can detect increasing idle time and slow the tempo.

        Args:
            timestamp: Current time. Defaults to now.
        """
        if timestamp is None:
            timestamp = time.time()

        self._adapt(timestamp)

    # ── Adaptation (SHADOW) ─────────────────────────────────────────

    def _adapt(self, now: float):
        """SHADOW MODE: calculate what the BPM would be, log it, don't apply.

        The algorithm:
        1. Count actions in the last CADENCE_WINDOW seconds
        2. Compute actions-per-minute (cadence)
        3. Map cadence + idle time to a target BPM
        4. Smoothly interpolate current_bpm toward target
        5. Log the adjustment if it's significant

        The cadence → BPM mapping:
            0 actions/min (idle)     → Largo 40 or Adagio 60
            1-5 actions/min (relaxed) → Adagio 60-72
            5-20 actions/min (steady) → Andante 80-92
            20-60 actions/min (active) → Moderato 100-120
            60+ actions/min (intense)  → Allegro 120+
        """
        # Calculate cadence: actions in the last CADENCE_WINDOW seconds
        window_start = now - CADENCE_WINDOW
        recent_actions = [t for t in self.action_history if t >= window_start]
        cadence = len(recent_actions) / (CADENCE_WINDOW / 60.0)  # actions per minute

        # Calculate idle time
        if self.last_action_time is not None:
            idle_seconds = now - self.last_action_time
        else:
            idle_seconds = float('inf')

        # Map cadence + idle to target BPM
        if idle_seconds > DEEP_IDLE_THRESHOLD:
            target_bpm = BPM_LARGO
            reason = f"deep_idle ({idle_seconds:.0f}s since last action)"
        elif idle_seconds > IDLE_THRESHOLD:
            target_bpm = BPM_ADAGIO
            reason = f"idle ({idle_seconds:.0f}s since last action)"
        elif cadence >= 60:
            target_bpm = BPM_ALLEGRO
            reason = f"frantic ({cadence:.0f} actions/min)"
        elif cadence >= 30:
            target_bpm = 110.0  # Between Moderato and Allegro
            reason = f"engaged ({cadence:.0f} actions/min)"
        elif cadence >= 15:
            target_bpm = BPM_MODERATO
            reason = f"moderate ({cadence:.0f} actions/min)"
        elif cadence >= 5:
            target_bpm = BPM_ANDANTE
            reason = f"steady ({cadence:.0f} actions/min)"
        elif cadence >= 1:
            target_bpm = 72.0  # Adagio/relaxed
            reason = f"relaxed ({cadence:.0f} actions/min)"
        else:
            target_bpm = BPM_ADAGIO
            reason = f"nearly_idle ({cadence:.1f} actions/min)"

        self._target_bpm = target_bpm

        # Smooth interpolation toward target
        dt = now - self._last_shadow_time
        if dt > 0:
            alpha = dt / (dt + SMOOTHING_TAU)
            self.current_bpm += (target_bpm - self.current_bpm) * alpha
        self._last_shadow_time = now

        # Log if the shadow BPM changed meaningfully
        if abs(self.current_bpm - self._last_logged_bpm) >= MIN_LOG_CHANGE:
            entry = ShadowEntry(
                timestamp=now,
                old_bpm=self._last_logged_bpm,
                new_bpm=self.current_bpm,
                target_bpm=self._target_bpm,
                cadence=cadence,
                idle_seconds=idle_seconds if idle_seconds != float('inf') else -1,
                reason=reason,
            )
            self.shadow_log.append(entry)
            self._last_logged_bpm = self.current_bpm

    # ── Queries ─────────────────────────────────────────────────────

    def get_bpm(self) -> float:
        """Return the effective BPM.

        In shadow mode, this always returns base_bpm.
        The system doesn't actually change tempo yet.
        """
        return self.base_bpm

    @property
    def shadow_bpm(self) -> float:
        """The BPM the adapter WOULD apply if it were live."""
        return self.current_bpm

    @property
    def target_bpm(self) -> float:
        """The BPM the adapter is smoothing toward."""
        return self._target_bpm

    @property
    def cadence(self) -> float:
        """Current action rate (actions per minute, last 30s window)."""
        now = time.time()
        window_start = now - CADENCE_WINDOW
        recent = [t for t in self.action_history if t >= window_start]
        return len(recent) / (CADENCE_WINDOW / 60.0)

    @property
    def idle_time(self) -> float:
        """Seconds since last action (inf if no actions recorded)."""
        if self.last_action_time is None:
            return float('inf')
        return time.time() - self.last_action_time

    @property
    def is_idle(self) -> bool:
        """True if the player has been idle longer than the threshold."""
        return self.idle_time > IDLE_THRESHOLD

    def get_shadow_summary(self) -> dict:
        """Summarize the shadow log for trajectory reporting."""
        if not self.shadow_log:
            return {
                "entries": 0,
                "avg_shadow_bpm": self.base_bpm,
                "min_shadow_bpm": self.base_bpm,
                "max_shadow_bpm": self.base_bpm,
                "avg_cadence": 0.0,
                "base_bpm": self.base_bpm,
            }

        bpm_values = [e.new_bpm for e in self.shadow_log]
        cadence_values = [e.cadence for e in self.shadow_log]

        return {
            "entries": len(self.shadow_log),
            "avg_shadow_bpm": sum(bpm_values) / len(bpm_values),
            "min_shadow_bpm": min(bpm_values),
            "max_shadow_bpm": max(bpm_values),
            "avg_cadence": sum(cadence_values) / len(cadence_values),
            "base_bpm": self.base_bpm,
        }

    # ── CNS v3 telemetry hook ────────────────────────────────────────

    def emit_telemetry(self, role: str = "lucineer-energy-adapter") -> str | None:
        """Emit a CNS v3 pulse derived from current energy adapter state.

        Production callers should call this after _adapt() or record_action()
        so the fleet receives live creative/thermal telemetry. The packet
        format and CNS bus IO are handled by the shared helper.
        """
        try:
            from lucineer.cns_telemetry import TelemetryQuantum, emit_cns_pulse
        except Exception:
            return None

        idle_seconds = self.idle_time
        idle_fraction = min(1.0, max(0.0, idle_seconds / 60.0))
        bpm = self.shadow_bpm

        tq = TelemetryQuantum(
            agent_id="energy-adapter-1",
            gamma=0.5,
            eta=0.25,
            delta=0.25,
            temperature=idle_fraction * 2.0,
            semantic_distance=idle_fraction,
            melt_pressure=0.0,
            max_crystallization_rate=0.0,
            deterministic=False,
            molt_count=0,
            capability=1.0 - idle_fraction,
            tau=idle_fraction,
            timestamp=datetime.now(timezone.utc).isoformat(),
            is_dreaming=idle_fraction > 0.8,
            temperature_idle=idle_seconds / 60.0,
            temperature_task=1.0,
            molt_phase="stable",
            creative_value=1.0 - (bpm / 120.0),
            kappa_delta=0.0,
        )
        return emit_cns_pulse(
            agent_id="energy-adapter-1",
            telemetry=tq,
            role=role,
            model="lucineer-energy-adapter",
        )

    def __repr__(self) -> str:
        mode = "SHADOW" if self.get_bpm() == self.base_bpm else "LIVE"
        return (
            f"EnergyAdapter({mode} base={self.base_bpm:.0f}, "
            f"shadow={self.current_bpm:.0f}→{self._target_bpm:.0f}, "
            f"cadence={self.cadence:.0f}/min, "
            f"idle={self.idle_time:.0f}s)"
        )
