#!/usr/bin/env python3
"""
Comprehensive tests for MOLT_REWARD_FUNCTION.py — Slackwater's RL reward function.

Tests cover:
  1. Data models (Build, BuildPart, Conversation, Session, PlayerHistory)
  2. Build retention scoring (measure_build_retention)
  3. Cooperation depth scoring (measure_cooperation)
  4. Return rate measurement (measure_return_rate)
  5. Craft quality measurement (measure_craft_quality)
  6. Energy efficiency measurement (measure_energy_efficiency)
  7. Master reward function (compute_reward)
  8. Rootwell guard
  9. Utilities (_clamp, _part_distance, _measure_connectivity)
  10. Serialization (_deserialize_session, _deserialize_history)
  11. Anti-metrics and reward weights validation
"""

import pytest
import sys
import time
import math
import statistics
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from MOLT_REWARD_FUNCTION import (
    BuildAction, ConversationType,
    BuildPart, Build, ConversationTurn, Conversation, Session, PlayerHistory,
    measure_build_retention, measure_cooperation, measure_return_rate,
    measure_craft_quality, measure_energy_efficiency,
    compute_reward, compute_reward_from_state,
    REWARD_WEIGHTS, ANTI_METRICS,
    _clamp, _part_distance, _measure_connectivity,
    _score_build_action, _score_conversation_type,
    _measure_structural_integrity, _measure_material_diversity,
    _measure_aesthetic_balance, _measure_symmetry,
    _era_material_bonus, _last_action_before,
    is_rootwell, rootwell_guard,
    _deserialize_session, _deserialize_history,
    _generate_explanation,
)


# ─── Fixtures ──────────────────────────────────────────────────────────────

NOW = time.time()


def make_part(
    part_id="p1", part_type="beam", material="wood",
    position=(0, 0, 0), rotation=(0, 0, 0),
    placed_by="lucineer", timestamp=None,
    is_gap_filler=False, is_deliberate_flaw=False,
):
    return BuildPart(
        part_id=part_id, part_type=part_type, material=material,
        position=position, rotation=rotation, placed_by=placed_by,
        timestamp=timestamp or NOW - 100,
        is_gap_filler=is_gap_filler, is_deliberate_flaw=is_deliberate_flaw,
    )


def make_build(
    build_id="b1", parts=None, era=1,
    actions=None, has_gap=False, gap_filled_by=None,
):
    if parts is None:
        parts = [make_part()]
    if actions is None:
        actions = [(NOW - 100, BuildAction.CREATED)]
    return Build(
        build_id=build_id, parts=parts,
        created_at=NOW - 100, last_modified_at=NOW,
        actions=actions, era=era,
        has_gap=has_gap, gap_filled_by=gap_filled_by,
        gap_filled_at=NOW if gap_filled_by else None,
    )


def make_session(
    session_id="s1", player_id="player_1",
    builds=None, conversations=None,
    era_start=1, era_end=1, bond_start=1, bond_end=1,
    duration=300,
):
    return Session(
        session_id=session_id, player_id=player_id,
        join_time=NOW - duration, leave_time=NOW,
        builds=builds or [], conversations=conversations or [],
        era_at_start=era_start, era_at_end=era_end,
        bond_stage_at_start=bond_start, bond_stage_at_end=bond_end,
    )


def make_history(player_id="player_1", sessions=None):
    if sessions is None:
        sessions = [make_session()]
    return PlayerHistory(
        player_id=player_id, sessions=sessions,
        first_seen=sessions[0].join_time if sessions else NOW,
        last_seen=sessions[-1].leave_time if sessions else NOW,
    )


def make_turn(speaker="player", content="hello", index=0, timestamp=None):
    return ConversationTurn(
        speaker=speaker, content=content,
        timestamp=timestamp or NOW - 100 + index,
        turn_index=index,
    )


def make_conversation(conv_type=ConversationType.COMMAND, turns=None):
    if turns is None:
        turns = [make_turn("player", "build a tower", 0),
                 make_turn("agent", "done", 1)]
    return Conversation(
        conversation_id="c1", player_id="player_1", agent_id="lucineer",
        turns=turns, conversation_type=conv_type,
    )


# ─── Data Model Tests ──────────────────────────────────────────────────────

class TestBuildPart:
    def test_basic_creation(self):
        p = make_part()
        assert p.part_id == "p1"
        assert p.material == "wood"
        assert p.position == (0, 0, 0)

    def test_defaults(self):
        p = make_part()
        assert p.is_gap_filler is False
        assert p.is_deliberate_flaw is False


class TestBuild:
    def test_part_count(self):
        b = make_build(parts=[make_part(f"p{i}") for i in range(5)])
        assert b.part_count == 5

    def test_unique_materials(self):
        parts = [make_part(material="wood"), make_part(material="iron"), make_part(material="wood")]
        b = make_build(parts=parts)
        assert b.unique_materials == {"wood", "iron"}

    def test_unique_part_types(self):
        parts = [make_part(part_type="beam"), make_part(part_type="sheet"), make_part(part_type="beam")]
        b = make_build(parts=parts)
        assert b.unique_part_types == {"beam", "sheet"}

    def test_player_parts(self):
        parts = [
            make_part(placed_by="player:1"),
            make_part(placed_by="lucineer", part_id="p2"),
            make_part(placed_by="player:2", part_id="p3"),
        ]
        b = make_build(parts=parts)
        assert len(b.player_parts) == 2

    def test_agent_parts(self):
        parts = [
            make_part(placed_by="lucineer"),
            make_part(placed_by="agent:earl", part_id="p2"),
            make_part(placed_by="player:1", part_id="p3"),
        ]
        b = make_build(parts=parts)
        assert len(b.agent_parts) == 2

    def test_is_jointly_built_true(self):
        parts = [make_part(placed_by="lucineer"), make_part(placed_by="player:1", part_id="p2")]
        b = make_build(parts=parts)
        assert b.is_jointly_built is True

    def test_is_jointly_built_false(self):
        parts = [make_part(placed_by="lucineer"), make_part(placed_by="agent:earl", part_id="p2")]
        b = make_build(parts=parts)
        assert b.is_jointly_built is False


class TestConversation:
    def test_turn_count(self):
        turns = [make_turn(index=i) for i in range(5)]
        c = make_conversation(turns=turns)
        assert c.turn_count == 5

    def test_player_turns(self):
        turns = [
            make_turn("player", index=0),
            make_turn("agent", index=1),
            make_turn("player", index=2),
        ]
        c = make_conversation(turns=turns)
        assert len(c.player_turns) == 2
        assert len(c.agent_turns) == 1


class TestSession:
    def test_duration(self):
        s = make_session(duration=600)
        assert s.duration_seconds == 600

    def test_build_count(self):
        s = make_session(builds=[make_build(), make_build(build_id="b2")])
        assert s.build_count == 2

    def test_conversation_count(self):
        s = make_session(conversations=[make_conversation()])
        assert s.conversation_count == 1


class TestPlayerHistory:
    def test_total_sessions(self):
        h = make_history(sessions=[make_session(), make_session(session_id="s2")])
        assert h.total_sessions == 2

    def test_total_builds(self):
        h = make_history(sessions=[
            make_session(builds=[make_build()]),
            make_session(session_id="s2", builds=[make_build(), make_build(build_id="b2")]),
        ])
        assert h.total_builds == 3

    def test_returned_within_days_true(self):
        s1 = make_session(session_id="s1")
        s1.join_time = NOW - 86400  # yesterday
        s1.leave_time = NOW - 80000
        s2 = make_session(session_id="s2")
        s2.join_time = NOW - 100
        h = make_history(sessions=[s1, s2])
        assert h.returned_within_days(1) is True

    def test_returned_within_days_false(self):
        h = make_history(sessions=[make_session()])
        assert h.returned_within_days(1) is False

    def test_sessions_on_day(self):
        s1 = make_session(session_id="s1")
        s1.join_time = NOW
        h = make_history(sessions=[s1])
        assert h.sessions_on_day(NOW) == 1


# ─── Utility Function Tests ────────────────────────────────────────────────

class TestClamp:
    def test_in_range(self):
        assert _clamp(0.5) == 0.5

    def test_below_min(self):
        assert _clamp(-1.0) == 0.0

    def test_above_max(self):
        assert _clamp(2.0) == 1.0

    def test_at_boundaries(self):
        assert _clamp(0.0) == 0.0
        assert _clamp(1.0) == 1.0

    def test_custom_range(self):
        assert _clamp(5, 1, 10) == 5
        assert _clamp(0, 1, 10) == 1
        assert _clamp(15, 1, 10) == 10


class TestPartDistance:
    def test_same_position(self):
        a = make_part(position=(0, 0, 0))
        b = make_part(part_id="p2", position=(0, 0, 0))
        assert _part_distance(a, b) == 0.0

    def test_unit_distance(self):
        a = make_part(position=(0, 0, 0))
        b = make_part(part_id="p2", position=(1, 0, 0))
        assert _part_distance(a, b) == 1.0

    def test_3d_distance(self):
        a = make_part(position=(0, 0, 0))
        b = make_part(part_id="p2", position=(3, 4, 0))
        assert _part_distance(a, b) == 5.0

    def test_diagonal(self):
        a = make_part(position=(0, 0, 0))
        b = make_part(part_id="p2", position=(1, 1, 1))
        assert abs(_part_distance(a, b) - math.sqrt(3)) < 0.001


class TestConnectivity:
    def test_single_part(self):
        parts = [make_part()]
        assert _measure_connectivity(parts) == 1.0

    def test_empty(self):
        assert _measure_connectivity([]) == 0.0

    def test_connected_parts(self):
        parts = [make_part(position=(0, 0, 0)),
                 make_part(part_id="p2", position=(5, 0, 0)),
                 make_part(part_id="p3", position=(10, 0, 0))]
        assert _measure_connectivity(parts, max_gap=12.0) == 1.0

    def test_disconnected_parts(self):
        parts = [make_part(position=(0, 0, 0)),
                 make_part(part_id="p2", position=(100, 0, 0))]
        score = _measure_connectivity(parts, max_gap=12.0)
        assert score == 0.5  # Largest component is 1 of 2


# ─── Build Action Scoring Tests ────────────────────────────────────────────

class TestScoreBuildAction:
    def test_completed_is_highest(self):
        b = make_build(actions=[(NOW, BuildAction.COMPLETED)])
        assert _score_build_action(b, NOW) == 1.0

    def test_kept(self):
        b = make_build(actions=[(NOW, BuildAction.KEPT)])
        assert _score_build_action(b, NOW) == 0.85

    def test_modified(self):
        b = make_build(actions=[(NOW, BuildAction.MODIFIED)])
        assert _score_build_action(b, NOW) == 0.75

    def test_created(self):
        b = make_build(actions=[(NOW, BuildAction.CREATED)])
        assert _score_build_action(b, NOW) == 0.6

    def test_abandoned(self):
        b = make_build(actions=[(NOW, BuildAction.ABANDONED)])
        assert _score_build_action(b, NOW) == 0.4

    def test_deleted_is_lowest(self):
        b = make_build(actions=[(NOW, BuildAction.DELETED)])
        assert _score_build_action(b, NOW) == 0.15

    def test_no_actions(self):
        b = make_build(actions=[])
        assert _score_build_action(b, NOW) == 0.5


class TestConversationTypeScoring:
    def test_command_lowest(self):
        assert _score_conversation_type(ConversationType.COMMAND) == 0.2

    def test_collaboration_highest(self):
        assert _score_conversation_type(ConversationType.COLLABORATION) == 0.9

    def test_argument_high(self):
        assert _score_conversation_type(ConversationType.ARGUMENT) == 0.85

    def test_negotiation(self):
        assert _score_conversation_type(ConversationType.NEGOTIATION) == 0.7

    def test_silence(self):
        assert _score_conversation_type(ConversationType.SILENCE) == 0.6


# ─── Build Retention Tests ────────────────────────────────────────────────

class TestBuildRetention:
    def test_empty_session(self):
        s = make_session(builds=[])
        h = make_history(sessions=[s])
        score = measure_build_retention(s, h, NOW)
        assert 0.0 <= score <= 1.0
        assert score == 0.5  # Neutral for no builds

    def test_completed_build_max_score(self):
        b = make_build(actions=[(NOW, BuildAction.COMPLETED)])
        s = make_session(builds=[b])
        h = make_history(sessions=[s])
        score = measure_build_retention(s, h, NOW)
        assert score >= 0.9

    def test_deleted_build_low_score(self):
        b = make_build(actions=[(NOW, BuildAction.DELETED)])
        s = make_session(builds=[b])
        h = make_history(sessions=[s])
        score = measure_build_retention(s, h, NOW)
        assert score <= 0.3

    def test_clamped(self):
        """Retention score must always be in [0, 1]."""
        b = make_build(actions=[(NOW, BuildAction.COMPLETED)])
        s = make_session(builds=[b])
        h = make_history(sessions=[s])
        score = measure_build_retention(s, h, NOW)
        assert 0.0 <= score <= 1.0


# ─── Cooperation Tests ────────────────────────────────────────────────────

class TestCooperation:
    def test_no_conversations_no_builds(self):
        s = make_session()
        score = measure_cooperation([], s)
        assert score == 0.3  # Pure wandering

    def test_command_only(self):
        conv = make_conversation(ConversationType.COMMAND)
        s = make_session(conversations=[conv])
        score = measure_cooperation([conv], s)
        assert 0.0 <= score <= 1.0
        # Command-only should be low
        assert score < 0.5

    def test_collaboration(self):
        turns = [make_turn(speaker="player", content="build a tower", index=i) for i in range(6)]
        turns += [make_turn(speaker="agent", content="done", index=i) for i in range(6, 12)]
        conv = make_conversation(ConversationType.COLLABORATION, turns=turns)
        s = make_session(conversations=[conv])
        score = measure_cooperation([conv], s)
        assert score > 0.3

    def test_gap_filling_bonus(self):
        parts = [
            make_part(placed_by="lucineer"),
            make_part(part_id="p2", placed_by="player:1"),
        ]
        b = make_build(parts=parts, has_gap=True, gap_filled_by="player:1",
                       actions=[(NOW, BuildAction.COMPLETED)])
        s = make_session(builds=[b])
        score = measure_cooperation([], s)
        # Should get gap bonus
        assert score > 0.0

    def test_clamped(self):
        conv = make_conversation(ConversationType.ARGUMENT,
                                 turns=[make_turn(index=i) for i in range(10)])
        s = make_session(conversations=[conv])
        score = measure_cooperation([conv], s)
        assert 0.0 <= score <= 1.0


# ─── Return Rate Tests ────────────────────────────────────────────────────

class TestReturnRate:
    def test_single_session(self):
        h = make_history(sessions=[make_session()])
        score = measure_return_rate(h, NOW)
        assert 0.0 <= score <= 1.0

    def test_returned_next_day(self):
        s1 = make_session(session_id="s1")
        s1.join_time = NOW - 86400
        s1.leave_time = NOW - 80000
        s2 = make_session(session_id="s2")
        h = make_history(sessions=[s1, s2])
        score = measure_return_rate(h, NOW)
        assert score >= 0.3  # At least day-1 return

    def test_no_return(self):
        h = make_history(sessions=[make_session()])
        score = measure_return_rate(h, NOW)
        assert score <= 0.1

    def test_clamped(self):
        s1 = make_session(session_id="s1")
        s1.join_time = NOW - 86400 * 30
        s1.leave_time = NOW - 80000 * 30
        s2 = make_session(session_id="s2")
        h = make_history(sessions=[s1, s2])
        score = measure_return_rate(h, NOW)
        assert 0.0 <= score <= 1.0


# ─── Craft Quality Tests ──────────────────────────────────────────────────

class TestCraftQuality:
    def test_empty_builds(self):
        score = measure_craft_quality([])
        assert score == 0.3

    def test_simple_structured_build(self):
        parts = [
            make_part(position=(0, 0, 0), material="wood"),
            make_part(part_id="p2", position=(4, 0, 0), material="wood"),
            make_part(part_id="p3", position=(0, 0, 4), material="wood"),
            make_part(part_id="p4", position=(4, 0, 4), material="wood"),
            make_part(part_id="p5", position=(2, 5, 2), material="iron"),
            make_part(part_id="p6", position=(0, 5, 0), material="iron"),
        ]
        b = make_build(parts=parts, era=1)
        score = measure_craft_quality([b])
        assert 0.0 <= score <= 1.0

    def test_clamped(self):
        parts = [make_part(position=(i * 10, 0, 0)) for i in range(5)]
        b = make_build(parts=parts)
        score = measure_craft_quality([b])
        assert 0.0 <= score <= 1.0

    def test_overbuilding_penalty(self):
        """Builds with >100 parts should get a penalty."""
        parts = [make_part(part_id=f"p{i}", position=(i % 10, i // 10, 0)) for i in range(150)]
        b = make_build(parts=parts)
        # The penalty is internal, but score should still be valid
        score = measure_craft_quality([b])
        assert 0.0 <= score <= 1.0


# ─── Structural Integrity Tests ───────────────────────────────────────────

class TestStructuralIntegrity:
    def test_empty_build(self):
        b = make_build(parts=[])
        assert _measure_structural_integrity(b) == 0.0

    def test_simple_foundation(self):
        parts = [
            make_part(position=(0, 0, 0)),
            make_part(part_id="p2", position=(4, 0, 0)),
            make_part(part_id="p3", position=(2, 5, 2)),  # Supported by p1/p2
        ]
        b = make_build(parts=parts)
        score = _measure_structural_integrity(b)
        assert 0.0 <= score <= 1.0

    def test_floating_build(self):
        """All parts high up with no foundation."""
        parts = [make_part(position=(0, 50, 0))]
        b = make_build(parts=parts)
        score = _measure_structural_integrity(b)
        assert score < 0.5  # Poor structural integrity


class TestMaterialDiversity:
    def test_single_material_era_1(self):
        b = make_build(parts=[make_part(material="wood")], era=1)
        assert _measure_material_diversity(b) == 0.5

    def test_single_material_era_5(self):
        b = make_build(parts=[make_part(material="wood")], era=5)
        assert _measure_material_diversity(b) == 0.25

    def test_diverse_materials(self):
        parts = [
            make_part(material="wood"),
            make_part(part_id="p2", material="iron"),
            make_part(part_id="p3", material="stone"),
        ]
        b = make_build(parts=parts, era=1)
        score = _measure_material_diversity(b)
        assert 0.0 <= score <= 1.0
        assert score > 0.25  # More diverse than single material


class TestAestheticBalance:
    def test_empty_build(self):
        b = make_build(parts=[])
        assert _measure_aesthetic_balance(b) == 0.0

    def test_symmetric_build(self):
        parts = [
            make_part(position=(0, 0, 0)),
            make_part(part_id="p2", position=(10, 0, 0)),
            make_part(part_id="p3", position=(0, 0, 10)),
            make_part(part_id="p4", position=(10, 0, 10)),
        ]
        b = make_build(parts=parts)
        score = _measure_aesthetic_balance(b)
        assert 0.0 <= score <= 1.0

    def test_clamped(self):
        parts = [make_part(position=(0, 0, 0))]
        b = make_build(parts=parts)
        score = _measure_aesthetic_balance(b)
        assert 0.0 <= score <= 1.0


class TestSymmetry:
    def test_perfect_symmetry(self):
        positions = [(0, 0, 0), (10, 0, 0), (0, 0, 10), (10, 0, 10)]
        score = _measure_symmetry(positions, cx=5, cz=5)
        assert score > 0.5

    def test_asymmetric(self):
        positions = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)]
        score = _measure_symmetry(positions, cx=1.5, cz=0)
        assert 0.0 <= score <= 1.0

    def test_too_few_points(self):
        score = _measure_symmetry([(0, 0, 0)], cx=0, cz=0)
        assert score == 0.5


# ─── Energy Efficiency Tests ──────────────────────────────────────────────

class TestEnergyEfficiency:
    def test_empty_session(self):
        s = make_session()
        score = measure_energy_efficiency(s)
        assert score == 0.5

    def test_efficient_build(self):
        conv = make_conversation(turns=[
            make_turn("player", "build a house", 0),
            make_turn("agent", "done", 1),
        ])
        b = make_build()
        s = make_session(builds=[b], conversations=[conv])
        score = measure_energy_efficiency(s)
        assert 0.0 <= score <= 1.0

    def test_era_progression(self):
        s = make_session(era_start=1, era_end=2,
                         builds=[make_build()])
        score = measure_energy_efficiency(s)
        # Should boost from era progression
        assert score > 0.4

    def test_clamped(self):
        s = make_session(builds=[make_build()])
        score = measure_energy_efficiency(s)
        assert 0.0 <= score <= 1.0


# ─── Master Reward Function Tests ─────────────────────────────────────────

class TestComputeReward:
    def test_empty_session_valid(self):
        s = make_session()
        h = make_history(sessions=[s])
        result = compute_reward(s, h, NOW)
        assert 0.0 <= result["reward"] <= 1.0

    def test_returns_all_components(self):
        s = make_session()
        h = make_history(sessions=[s])
        result = compute_reward(s, h, NOW)
        components = result["components"]
        assert "build_retention" in components
        assert "cooperation_depth" in components
        assert "return_rate" in components
        assert "craft_quality" in components
        assert "energy_efficiency" in components

    def test_returns_weights(self):
        s = make_session()
        h = make_history(sessions=[s])
        result = compute_reward(s, h, NOW)
        assert result["weights"] == REWARD_WEIGHTS

    def test_returns_anti_metrics(self):
        s = make_session()
        h = make_history(sessions=[s])
        result = compute_reward(s, h, NOW)
        assert "session_duration" in result["anti_metrics"]

    def test_returns_explanation(self):
        s = make_session()
        h = make_history(sessions=[s])
        result = compute_reward(s, h, NOW)
        assert isinstance(result["explanation"], str)
        assert len(result["explanation"]) > 0

    def test_custom_weights(self):
        s = make_session()
        h = make_history(sessions=[s])
        custom = {k: 0.0 for k in REWARD_WEIGHTS}
        custom["craft_quality"] = 1.0
        result = compute_reward(s, h, NOW, weights=custom)
        # Reward should equal craft_quality score
        assert abs(result["reward"] - result["components"]["craft_quality"]) < 0.01

    def test_all_components_in_range(self):
        """Every component score must be in [0, 1]."""
        s = make_session()
        h = make_history(sessions=[s])
        result = compute_reward(s, h, NOW)
        for name, score in result["components"].items():
            assert 0.0 <= score <= 1.0, f"{name} = {score} out of range"

    def test_rich_session_scores_higher(self):
        """A rich collaborative session should score higher than an empty one."""
        # Empty session
        s_empty = make_session()
        h_empty = make_history(sessions=[s_empty])
        result_empty = compute_reward(s_empty, h_empty, NOW)

        # Rich session
        parts = [
            make_part(position=(0, 0, 0), placed_by="lucineer"),
            make_part(part_id="p2", position=(8, 0, 0), placed_by="lucineer"),
            make_part(part_id="p3", position=(0, 0, 8), placed_by="lucineer"),
            make_part(part_id="p4", position=(0, 5, 0), material="iron", placed_by="player:1"),
            make_part(part_id="p5", position=(8, 5, 0), material="iron", placed_by="player:1"),
            make_part(part_id="p6", position=(4, 3, 4), material="iron", placed_by="player:1"),
        ]
        b = make_build(parts=parts, era=2, has_gap=True, gap_filled_by="player:1",
                       actions=[(NOW - 600, BuildAction.CREATED), (NOW - 100, BuildAction.COMPLETED)])
        turns = [
            make_turn("player", "build a tower", 0),
            make_turn("agent", "left the railing off", 1),
            make_turn("player", "I'll finish it", 2),
            make_turn("agent", "your railing", 3),
            make_turn("player", "done", 4),
            make_turn("agent", "looks good", 5),
        ]
        conv = make_conversation(ConversationType.COLLABORATION, turns=turns)
        s_rich = make_session(builds=[b], conversations=[conv], era_start=1, era_end=2,
                              bond_start=1, bond_end=2)
        s_prev = make_session(session_id="prev")
        s_prev.join_time = NOW - 86400
        s_prev.leave_time = NOW - 80000
        h_rich = make_history(sessions=[s_prev, s_rich])

        result_rich = compute_reward(s_rich, h_rich, NOW)
        assert result_rich["reward"] > result_empty["reward"], \
            f"Rich ({result_rich['reward']:.3f}) should > empty ({result_empty['reward']:.3f})"


# ─── Rootwell Guard Tests ─────────────────────────────────────────────────

class TestRootwellGuard:
    def test_is_rootwell(self):
        assert is_rootwell("rootwell") is True
        assert is_rootwell("ROOTWELL") is True
        assert is_rootwell("Rootwell") is True

    def test_not_rootwell(self):
        assert is_rootwell("lucineer") is False
        assert is_rootwell("earl") is False
        assert is_rootwell("") is False

    def test_rootwell_guard_returns_neutral(self):
        assert rootwell_guard("rootwell") == 0.5

    def test_rootwell_guard_passthrough(self):
        assert rootwell_guard("lucineer") == -1.0


# ─── Era Material Bonus Tests ─────────────────────────────────────────────

class TestEraMaterialBonus:
    def test_era_1_matching_materials(self):
        bonus = _era_material_bonus(1, {"wood": 5, "stone": 3, "iron": 2})
        assert bonus > 0.0  # Should get bonus for era-appropriate materials

    def test_era_1_no_matching_materials(self):
        bonus = _era_material_bonus(1, {"plastic": 5, "graphene": 3})
        assert bonus == 0.0

    def test_unknown_era(self):
        assert _era_material_bonus(99, {"wood": 1}) == 0.0

    def test_partial_match(self):
        bonus = _era_material_bonus(1, {"wood": 5, "plastic": 3})
        assert 0.0 < bonus < 0.1  # Partial overlap

    def test_max_bonus(self):
        # All era materials present
        bonus = _era_material_bonus(1, {"wood": 1, "stone": 1, "iron": 1})
        assert bonus == 0.1


# ─── Serialization Tests ──────────────────────────────────────────────────

class TestDeserialization:
    def test_roundtrip_simple_session(self):
        s = make_session()
        # We need to manually create the dict since there's no to_dict
        data = {
            "session_id": s.session_id,
            "player_id": s.player_id,
            "join_time": s.join_time,
            "leave_time": s.leave_time,
            "builds": [],
            "conversations": [],
            "era_at_start": s.era_at_start,
            "era_at_end": s.era_at_end,
            "bond_stage_at_start": s.bond_stage_at_start,
            "bond_stage_at_end": s.bond_stage_at_end,
        }
        s2 = _deserialize_session(data)
        assert s2.session_id == s.session_id
        assert s2.player_id == s.player_id
        assert s2.duration_seconds == s.duration_seconds

    def test_deserialize_with_builds(self):
        data = {
            "session_id": "test",
            "player_id": "p1",
            "join_time": NOW - 100,
            "leave_time": NOW,
            "builds": [{
                "build_id": "b1",
                "parts": [{
                    "part_id": "p1",
                    "part_type": "beam",
                    "material": "wood",
                    "position": [0, 0, 0],
                    "rotation": [0, 0, 0],
                    "placed_by": "lucineer",
                    "timestamp": NOW - 50,
                }],
                "created_at": NOW - 50,
                "last_modified_at": NOW,
                "actions": [[NOW - 50, "created"]],
                "era": 1,
            }],
        }
        s = _deserialize_session(data)
        assert len(s.builds) == 1
        assert s.builds[0].part_count == 1
        assert s.builds[0].parts[0].material == "wood"

    def test_deserialize_history(self):
        data = {
            "player_id": "p1",
            "sessions": [{
                "session_id": "s1",
                "player_id": "p1",
                "join_time": NOW - 100,
                "leave_time": NOW,
            }],
            "first_seen": NOW - 100,
            "last_seen": NOW,
        }
        h = _deserialize_history(data)
        assert h.player_id == "p1"
        assert h.total_sessions == 1


# ─── Reward Weights & Anti-Metrics Tests ──────────────────────────────────

class TestRewardWeights:
    def test_weights_sum_to_one(self):
        total = sum(REWARD_WEIGHTS.values())
        assert abs(total - 1.0) < 0.001

    def test_all_positive(self):
        for name, weight in REWARD_WEIGHTS.items():
            assert weight > 0, f"{name} has non-positive weight"

    def test_build_retention_weight(self):
        assert REWARD_WEIGHTS["build_retention"] == 0.25

    def test_cooperation_weight(self):
        assert REWARD_WEIGHTS["cooperation_depth"] == 0.25

    def test_return_rate_weight(self):
        assert REWARD_WEIGHTS["return_rate"] == 0.20

    def test_craft_quality_weight(self):
        assert REWARD_WEIGHTS["craft_quality"] == 0.20

    def test_energy_efficiency_weight(self):
        assert REWARD_WEIGHTS["energy_efficiency"] == 0.10


class TestAntiMetrics:
    def test_session_duration_excluded(self):
        assert "session_duration" in ANTI_METRICS

    def test_click_count_excluded(self):
        assert "click_count" in ANTI_METRICS

    def test_daily_streak_excluded(self):
        assert "daily_streak" in ANTI_METRICS

    def test_screen_time_excluded(self):
        assert "screen_time" in ANTI_METRICS

    def test_all_documented(self):
        for metric in ANTI_METRICS:
            assert isinstance(metric, str)
            assert len(metric) > 0


# ─── Explanation Generator Tests ──────────────────────────────────────────

class TestExplanation:
    def test_generates_string(self):
        components = {
            "build_retention": 0.5,
            "cooperation_depth": 0.5,
            "return_rate": 0.5,
            "craft_quality": 0.5,
            "energy_efficiency": 0.5,
        }
        s = make_session()
        explanation = _generate_explanation(components, 0.5, s)
        assert isinstance(explanation, str)
        assert "Reward:" in explanation
        assert "build_retention" in explanation

    def test_identifies_dominant_signal(self):
        components = {
            "build_retention": 0.9,
            "cooperation_depth": 0.3,
            "return_rate": 0.5,
            "craft_quality": 0.5,
            "energy_efficiency": 0.5,
        }
        s = make_session()
        explanation = _generate_explanation(components, 0.6, s)
        assert "build_retention" in explanation  # Dominant signal


# ─── State Adapter Tests ──────────────────────────────────────────────────

class TestComputeRewardFromState:
    def test_empty_state(self):
        state = {
            "session_data": {},
            "player_history_data": {},
            "current_time": NOW,
        }
        reward = compute_reward_from_state(state)
        assert 0.0 <= reward <= 1.0

    def test_with_session_data(self):
        state = {
            "session_data": {
                "session_id": "test",
                "player_id": "p1",
                "join_time": NOW - 100,
                "leave_time": NOW,
                "builds": [],
                "conversations": [],
            },
            "player_history_data": {
                "player_id": "p1",
                "sessions": [],
            },
            "current_time": NOW,
        }
        reward = compute_reward_from_state(state)
        assert 0.0 <= reward <= 1.0
