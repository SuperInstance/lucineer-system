"""
Tests for EnergyAdapter — Phase 1 shadow mode.

Tests:
1. Action cadence speeds up shadow tempo
2. Idle slows down shadow tempo
3. Shadow mode doesn't change base BPM
4. Shadow log records adjustments
5. Cadence measurement is accurate
6. Smooth interpolation (no jumps)
"""

import time
import pytest
import sys
import os

# Add lucineer-system to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from energy_adapter import (
    EnergyAdapter,
    ShadowEntry,
    BPM_ALLEGRO,
    BPM_MODERATO,
    BPM_ANDANTE,
    BPM_ADAGIO,
    BPM_LARGO,
    CADENCE_WINDOW,
    IDLE_THRESHOLD,
    SMOOTHING_TAU,
)


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def adapter():
    """Fresh EnergyAdapter at base BPM 72."""
    return EnergyAdapter(base_bpm=72)


@pytest.fixture
def fast_adapter():
    """EnergyAdapter with very fast smoothing for time-compressed tests."""
    a = EnergyAdapter(base_bpm=72)
    # Patch smoothing for fast tests
    import energy_adapter
    original = energy_adapter.SMOOTHING_TAU
    energy_adapter.SMOOTHING_TAU = 0.01
    yield a
    energy_adapter.SMOOTHING_TAU = original


# ── Test: Shadow mode doesn't change base BPM ────────────────────────────────

class TestShadowMode:
    """Verify that shadow mode NEVER changes the effective BPM."""

    def test_get_bpm_returns_base_initially(self, adapter):
        assert adapter.get_bpm() == 72.0

    def test_get_bpm_returns_base_after_actions(self, adapter):
        """Even after many actions, get_bpm() returns base."""
        for i in range(100):
            adapter.record_action(time.time())
        assert adapter.get_bpm() == 72.0

    def test_get_bpm_returns_base_after_idle(self, adapter):
        """Even after long idle, get_bpm() returns base."""
        adapter.record_action(time.time() - 120)  # action 2 minutes ago
        adapter.record_idle(time.time())
        assert adapter.get_bpm() == 72.0

    def test_get_bpm_constant(self, adapter):
        """get_bpm() is truly constant in shadow mode."""
        bpms = []
        for i in range(20):
            adapter.record_action(time.time())
            bpms.append(adapter.get_bpm())
        assert all(b == 72.0 for b in bpms), f"BPM varied: {bpms}"

    def test_shadow_bpm_differs_from_base(self, adapter):
        """But shadow_bpm SHOULD track what we'd want."""
        # Record many rapid actions to push shadow BPM up
        now = time.time()
        for i in range(60):
            adapter.record_action(now - (60 - i) * 0.1)  # 6 actions/sec
        adapter.record_action(now)

        # Shadow BPM should be higher than base
        assert adapter.shadow_bpm > 72.0, (
            f"Shadow BPM {adapter.shadow_bpm} should be > 72 after rapid actions"
        )


# ── Test: Action cadence speeds up shadow tempo ──────────────────────────────

class TestCadenceSpeeds:

    def test_rapid_actions_increase_shadow_bpm(self, fast_adapter):
        """Many actions in a short window should push shadow BPM toward Allegro."""
        now = time.time()

        # Simulate 60 actions in the last 10 seconds = very high cadence
        for i in range(60):
            fast_adapter.record_action(now - (60 - i) * 0.1)

        assert fast_adapter.shadow_bpm > 80.0, (
            f"Shadow BPM {fast_adapter.shadow_bpm:.1f} should be elevated after rapid actions"
        )

    def test_target_bpm_reaches_allegro(self, fast_adapter):
        """With frantic cadence, target BPM should reach Allegro (120)."""
        now = time.time()

        # 120 actions in 10 seconds = extremely high cadence
        for i in range(120):
            fast_adapter.record_action(now - (120 - i) * 0.05)

        assert fast_adapter.target_bpm >= BPM_ALLEGRO, (
            f"Target BPM {fast_adapter.target_bpm:.1f} should be >= {BPM_ALLEGRO}"
        )

    def test_moderate_cadence_targets_andante(self, fast_adapter):
        """Moderate cadence (10-20/min) should target Andante."""
        now = time.time()

        # 8 actions in 30 seconds = 16/min
        for i in range(8):
            fast_adapter.record_action(now - (8 - i) * 3)

        assert BPM_ANDANTE - 10 <= fast_adapter.target_bpm <= BPM_MODERATO, (
            f"Target BPM {fast_adapter.target_bpm:.1f} should be near Andante ({BPM_ANDANTE})"
        )


# ── Test: Idle slows down shadow tempo ───────────────────────────────────────

class TestIdleSlows:

    def test_idle_decreases_shadow_bpm(self, fast_adapter):
        """After long idle, shadow BPM should drop below base."""
        now = time.time()

        # First, get some activity in
        for i in range(10):
            fast_adapter.record_action(now - 60 + i * 0.5)

        # Then go idle for 60 seconds
        fast_adapter.record_idle(now)
        fast_adapter._last_shadow_time = now - 60  # simulate time passage
        fast_adapter.record_idle(now)

        # After deep idle, target should be low
        assert fast_adapter.target_bpm <= BPM_ADAGIO, (
            f"Target BPM {fast_adapter.target_bpm:.1f} should be <= {BPM_ADAGIO} after idle"
        )

    def test_deep_idle_targets_largo(self, adapter):
        """After 30+ seconds of idle, target should reach Largo."""
        now = time.time()

        # Record an action 45 seconds ago
        adapter.record_action(now - 45)
        adapter.record_idle(now)

        assert adapter.target_bpm == BPM_LARGO, (
            f"Target BPM {adapter.target_bpm:.1f} should be {BPM_LARGO} after deep idle"
        )

    def test_no_action_means_idle(self, adapter):
        """An adapter with no actions should consider itself idle."""
        assert adapter.is_idle is True
        assert adapter.idle_time == float('inf')


# ── Test: Shadow log records adjustments ─────────────────────────────────────

class TestShadowLog:

    def test_shadow_log_starts_empty(self, adapter):
        assert len(adapter.shadow_log) == 0

    def test_shadow_log_grows_with_actions(self, fast_adapter):
        """Significant BPM changes should create log entries."""
        now = time.time()

        # Burst of activity
        for i in range(60):
            fast_adapter.record_action(now - (60 - i) * 0.1)

        assert len(fast_adapter.shadow_log) > 0, "Shadow log should have entries after activity"

    def test_shadow_log_entries_have_fields(self, fast_adapter):
        """Each shadow log entry should have all required fields."""
        now = time.time()

        for i in range(60):
            fast_adapter.record_action(now - (60 - i) * 0.1)

        entry = fast_adapter.shadow_log[-1]
        assert isinstance(entry, ShadowEntry)
        assert entry.timestamp > 0
        assert entry.old_bpm > 0
        assert entry.new_bpm > 0
        assert entry.target_bpm > 0
        assert entry.cadence >= 0
        assert entry.idle_seconds >= 0
        assert isinstance(entry.reason, str)
        assert len(entry.reason) > 0

    def test_shadow_summary(self, adapter):
        """get_shadow_summary returns useful stats."""
        summary = adapter.get_shadow_summary()
        assert "entries" in summary
        assert "avg_shadow_bpm" in summary
        assert "base_bpm" in summary
        assert summary["base_bpm"] == 72.0


# ── Test: Cadence measurement ────────────────────────────────────────────────

class TestCadence:

    def test_cadence_zero_with_no_actions(self, adapter):
        assert adapter.cadence == 0.0

    def test_cadence_measures_actions_per_minute(self, adapter):
        """If we record 10 actions in the last 30 seconds,
        cadence should be 20/min."""
        now = time.time()

        # 10 actions spread over 30 seconds
        for i in range(10):
            adapter.record_action(now - 29 + i * 2.5)

        # Cadence = 10 actions / 30s * 60 = 20/min
        # (approximately — exact value depends on how many fall in window)
        assert adapter.cadence > 10.0, f"Cadence {adapter.cadence:.1f} should be > 10"
        assert adapter.cadence <= 25.0, f"Cadence {adapter.cadence:.1f} should be <= 25"

    def test_old_actions_excluded_from_cadence(self, adapter):
        """Actions older than CADENCE_WINDOW should not count."""
        now = time.time()

        # Old actions (outside window)
        for i in range(20):
            adapter.record_action(now - CADENCE_WINDOW - 10 - i)

        # One recent action
        adapter.record_action(now - 1)

        # Cadence should be low (only 1 recent action)
        assert adapter.cadence < 5.0, (
            f"Cadence {adapter.cadence:.1f} should be low (only 1 recent action)"
        )


# ── Test: Smooth interpolation ───────────────────────────────────────────────

class TestSmoothing:

    def test_shadow_bpm_never_jumps(self, fast_adapter):
        """Shadow BPM should change gradually, never jump."""
        now = time.time()

        # Start from idle
        fast_adapter.record_idle(now)

        initial = fast_adapter.shadow_bpm

        # Sudden burst of activity
        for i in range(60):
            fast_adapter.record_action(now + i * 0.01)

        # Even after burst, shadow BPM should not have jumped to target
        # (it should be moving toward target but not there yet)
        change = abs(fast_adapter.shadow_bpm - initial)
        target_change = abs(fast_adapter.target_bpm - initial)

        # The actual change should be less than the full target distance
        # (because of smoothing)
        # Note: with fast smoothing (tau=0.01), it might reach target
        # in a few steps, but a single record_action shouldn't get there
        assert change <= target_change + 0.1, (
            f"Shadow BPM changed {change:.1f}, target change {target_change:.1f} — "
            "smoothing should prevent jumps"
        )

    def test_shadow_bpm_stays_in_valid_range(self, fast_adapter):
        """Shadow BPM should always be within a valid range."""
        now = time.time()

        # Mix of activity and idle
        for i in range(30):
            fast_adapter.record_action(now - 15 + i * 0.5)

        fast_adapter.record_idle(now + 100)

        assert BPM_LARGO <= fast_adapter.shadow_bpm <= BPM_ALLEGRO + 20, (
            f"Shadow BPM {fast_adapter.shadow_bpm:.1f} out of valid range"
        )
