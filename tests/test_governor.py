"""
Tests for Governor Φ — Phase 1 shadow mode.

Tests:
1. Φ computation from tracks
2. Shadow logging
3. Φ responds to different track qualities (smooth vs friction)
4. Deadband calibration (would_alarm detection)
5. Pocket and deep flow detection
"""

import time
import math
import pytest
import sys
import os

# Add lucineer-system to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from governor import (
    Governor,
    PhiEntry,
    WEIGHT_ENTROPY,
    WEIGHT_IDLE,
    WEIGHT_ERROR,
    WEIGHT_HELP,
    PHI_POCKET,
    PHI_DEEP_FLOW,
    DEADBAND_STAGE,
)


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def governor():
    """Fresh Governor."""
    return Governor()


# ── Test: Φ computation ──────────────────────────────────────────────────────

class TestPhiComputation:

    def test_phi_returns_float(self, governor):
        """observe() returns a float."""
        phi = governor.observe({"action_cadence": 10, "idle_time": 2.0})
        assert isinstance(phi, float)

    def test_phi_in_valid_range(self, governor):
        """Φ should always be in [0, 1]."""
        # Various track inputs
        tracks_list = [
            {"action_cadence": 0, "idle_time": 0},
            {"action_cadence": 100, "idle_time": 0},
            {"action_cadence": 0, "idle_time": 120},
            {"action_cadence": 50, "idle_time": 1.0, "error_rate": 0.5},
            {"action_cadence": 10, "idle_time": 5.0, "error_rate": 1.0, "help_requests": 5},
        ]
        for tracks in tracks_list:
            phi = governor.observe(tracks)
            assert 0.0 <= phi <= 1.0, f"Φ={phi} out of range for tracks={tracks}"

    def test_smooth_tracks_produce_low_phi(self, governor):
        """Low idle, no errors, focused actions → low Φ."""
        phi = governor.observe({
            "action_cadence": 15,
            "idle_time": 0.5,
            "error_rate": 0.0,
            "matched": True,
            "stage": "code",
        })
        assert phi < 0.3, f"Φ={phi:.3f} should be low for smooth tracks"

    def test_high_idle_increases_phi(self, governor):
        """Long idle time should increase Φ."""
        phi_active = governor.observe({
            "action_cadence": 20,
            "idle_time": 0.5,
            "error_rate": 0.0,
            "stage": "code",
        })

        # Fresh governor for comparison
        gov2 = Governor()
        phi_idle = gov2.observe({
            "action_cadence": 0,
            "idle_time": 60.0,
            "error_rate": 0.0,
            "stage": "code",
        })

        assert phi_idle > phi_active, (
            f"Idle Φ={phi_idle:.3f} should be > active Φ={phi_active:.3f}"
        )

    def test_errors_increase_phi(self, governor):
        """High error rate should increase Φ."""
        phi_clean = governor.observe({
            "action_cadence": 10,
            "idle_time": 1.0,
            "error_rate": 0.0,
            "matched": True,
            "stage": "code",
        })

        gov2 = Governor()
        phi_errors = gov2.observe({
            "action_cadence": 10,
            "idle_time": 1.0,
            "error_rate": 1.0,
            "matched": False,
            "stage": "code",
        })

        assert phi_errors > phi_clean, (
            f"Error Φ={phi_errors:.3f} should be > clean Φ={phi_clean:.3f}"
        )

    def test_mismatched_keyword_adds_friction(self, governor):
        """A keyword mismatch (default response) should add to Φ."""
        phi_matched = governor.observe({
            "action_cadence": 5,
            "idle_time": 2.0,
            "matched": True,
            "stage": "intent",
        })

        gov2 = Governor()
        phi_unmatched = gov2.observe({
            "action_cadence": 5,
            "idle_time": 2.0,
            "matched": False,
            "stage": "intent",
        })

        assert phi_unmatched > phi_matched, (
            f"Unmatched Φ={phi_unmatched:.3f} should be > matched Φ={phi_matched:.3f}"
        )

    def test_help_requests_increase_phi(self, governor):
        """Help requests should increase Φ."""
        phi_no_help = governor.observe({
            "action_cadence": 5,
            "idle_time": 2.0,
            "help_requests": 0,
            "stage": "code",
        })

        gov2 = Governor()
        phi_help = gov2.observe({
            "action_cadence": 5,
            "idle_time": 2.0,
            "help_requests": 3,
            "stage": "code",
        })

        assert phi_help > phi_no_help, (
            f"Help Φ={phi_help:.3f} should be > no-help Φ={phi_no_help:.3f}"
        )


# ── Test: Shadow logging ─────────────────────────────────────────────────────

class TestShadowLog:

    def test_shadow_log_starts_empty(self, governor):
        assert len(governor.shadow_log) == 0

    def test_observe_creates_log_entry(self, governor):
        governor.observe({
            "action_cadence": 10,
            "idle_time": 2.0,
            "stage": "code",
        })
        assert len(governor.shadow_log) == 1

    def test_multiple_observations_create_multiple_entries(self, governor):
        for i in range(10):
            governor.observe({
                "action_cadence": i,
                "idle_time": float(i),
                "stage": "code",
            })
        assert len(governor.shadow_log) == 10

    def test_log_entry_has_all_fields(self, governor):
        governor.observe({
            "action_cadence": 10,
            "idle_time": 2.0,
            "error_rate": 0.1,
            "stage": "code",
            "matched": True,
            "command_count": 5,
        })
        entry = governor.shadow_log[-1]
        assert isinstance(entry, PhiEntry)
        assert entry.timestamp > 0
        assert 0.0 <= entry.phi <= 1.0
        assert isinstance(entry.tracks, dict)
        assert entry.deadband > 0
        assert isinstance(entry.would_alarm, bool)
        assert isinstance(entry.in_pocket, bool)
        assert isinstance(entry.in_deep_flow, bool)
        assert isinstance(entry.reason, str)

    def test_phi_history_tracks_all_observations(self, governor):
        """phi_history should have one entry per observe() call."""
        for i in range(5):
            governor.observe({"action_cadence": i * 5})
        assert len(governor.phi_history) == 5

    def test_shadow_summary(self, governor):
        """get_shadow_summary returns useful stats."""
        for i in range(10):
            governor.observe({
                "action_cadence": i,
                "idle_time": float(i * 2),
                "stage": "code",
            })

        summary = governor.get_shadow_summary()
        assert summary["observations"] == 10
        assert "avg_phi" in summary
        assert "max_phi" in summary
        assert "min_phi" in summary
        assert "would_alarm_count" in summary
        assert "pocket_fraction" in summary


# ── Test: Pocket and deep flow detection ────────────────────────────────────

class TestFlowDetection:

    def test_perfect_tracks_enter_pocket(self, governor):
        """Zero friction tracks should indicate pocket."""
        # Give some focused action history first
        for i in range(20):
            governor._action_types.append("build")

        phi = governor.observe({
            "action_cadence": 15,
            "idle_time": 0.1,
            "error_rate": 0.0,
            "matched": True,
            "stage": "code",
            "action_type": "build",
        })

        # With repetitive actions (low entropy), no idle, no errors → low Φ
        assert phi < 0.2, f"Φ={phi:.3f} should be low for focused, smooth tracks"
        assert governor.in_pocket, "Should be in pocket with low Φ"

    def test_very_low_phi_indicates_deep_flow(self, governor):
        """Extremely low Φ should indicate deep flow."""
        # All same action type (entropy = 0)
        for i in range(20):
            governor._action_types.append("build")

        phi = governor.observe({
            "action_cadence": 20,
            "idle_time": 0.0,
            "error_rate": 0.0,
            "matched": True,
            "stage": "code",
        })

        # Should be very close to 0
        assert phi < PHI_POCKET, f"Φ={phi:.3f} should be below pocket threshold"

    def test_scattered_actions_prevent_pocket(self, governor):
        """High action entropy should prevent pocket detection."""
        # Many different action types (high entropy)
        for action in ["build", "paint", "move", "chat", "delete", "rotate", "scale", "weld"]:
            governor._action_types.append(action)

        phi = governor.observe({
            "action_cadence": 10,
            "idle_time": 2.0,
            "error_rate": 0.0,
            "matched": True,
            "stage": "code",
        })

        assert not governor.in_deep_flow, (
            f"Should not be in deep flow with scattered actions (Φ={phi:.3f})"
        )


# ── Test: Deadband calibration ──────────────────────────────────────────────

class TestDeadbands:

    def test_deadband_varies_by_stage(self):
        """Different stages should have different deadbands."""
        assert DEADBAND_STAGE["intent"] > DEADBAND_STAGE["code"]
        assert DEADBAND_STAGE["code"] > DEADBAND_STAGE["voice"]

    def test_would_alarm_triggers_on_high_phi(self, governor):
        """High Φ should set would_alarm=True."""
        # Create high-friction conditions
        governor.observe({
            "action_cadence": 0,
            "idle_time": 60.0,
            "error_rate": 1.0,
            "matched": False,
            "help_requests": 5,
            "stage": "voice",  # tight deadband
        })

        entry = governor.shadow_log[-1]
        assert entry.would_alarm, (
            f"Should alarm: Φ={entry.phi:.3f}, deadband={entry.deadband}"
        )

    def test_no_alarm_on_low_phi(self, governor):
        """Low Φ should NOT set would_alarm."""
        for i in range(20):
            governor._action_types.append("build")

        governor.observe({
            "action_cadence": 15,
            "idle_time": 0.1,
            "error_rate": 0.0,
            "matched": True,
            "stage": "code",
        })

        entry = governor.shadow_log[-1]
        assert not entry.would_alarm, (
            f"Should NOT alarm: Φ={entry.phi:.3f}, deadband={entry.deadband}"
        )


# ── Test: Reproducibility and properties ────────────────────────────────────

class TestProperties:

    def test_same_tracks_produce_same_phi(self):
        """Identical tracks should produce identical Φ."""
        gov1 = Governor()
        gov2 = Governor()

        tracks = {"action_cadence": 10, "idle_time": 2.0, "error_rate": 0.1}
        phi1 = gov1.observe(dict(tracks))
        phi2 = gov2.observe(dict(tracks))

        assert abs(phi1 - phi2) < 0.001, (
            f"Same tracks should produce same Φ: {phi1} vs {phi2}"
        )

    def test_phi_history_bounded(self, governor):
        """Phi history should not grow unbounded."""
        for i in range(2000):
            governor.observe({"action_cadence": i})
        assert len(governor.phi_history) <= 1100  # max_history + buffer

    def test_repr_works(self, governor):
        """__repr__ should return a readable string."""
        governor.observe({"action_cadence": 10, "idle_time": 2.0})
        r = repr(governor)
        assert "Governor" in r
        assert "SHADOW" in r
        assert "Φ=" in r

    def test_current_phi_property(self, governor):
        """current_phi returns the last observation."""
        governor.observe({"action_cadence": 10, "idle_time": 2.0, "error_rate": 0.5})
        assert governor.current_phi == governor.phi_history[-1]

    def test_avg_phi_property(self, governor):
        """avg_phi returns the mean of all observations."""
        governor.observe({"action_cadence": 10, "idle_time": 2.0, "error_rate": 0.0})
        governor.observe({"action_cadence": 0, "idle_time": 60.0, "error_rate": 1.0})

        expected = (governor.phi_history[0] + governor.phi_history[1]) / 2
        assert abs(governor.avg_phi - expected) < 0.001
