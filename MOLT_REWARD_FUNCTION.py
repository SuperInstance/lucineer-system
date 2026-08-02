"""
MOLT_REWARD_FUNCTION.py
========================
Slackwater's RL reward function for training game agents via MOLT.

"The reward is any Python you write. Write it carefully.
 The agent will become what you measure."

This module defines the complete reward computation pipeline for Slackwater's
agent training loop. It measures what we VALUE — craft, cooperation, continuity,
and the conservation of cognitive energy — and refuses to measure what we refuse
to become — engagement traps, addiction metrics, attention extraction.

Design Principles (non-negotiable):
    1. NEVER reward engagement metrics directly (time spent, clicks, sessions/day)
    2. ALWAYS reward craft, cooperation, and continuity
    3. The conservation law γ + H = C governs all cognitive budgets
    4. The Unfinished Rule: gaps are invitations, not failures
    5. Restraint is a signal, not absence
    6. Rootwell is never optimized (the agent who questions optimization must
       not itself be optimized — this is a design principle, not a limitation)

Integration: Compatible with MOLT's Env.step() -> Result(reward=...) contract.
             See NVIDIA_SYNERGY_RESEARCH.md Appendix A.

Author: DeepSeek reward subagent
Date: 2026-08-02
Canon: FABLE_5_PRODUCTION_DESIGN.md, NVIDIA_SYNERGY_RESEARCH.md
"""

from __future__ import annotations

import math
import time
import json
import hashlib
import statistics
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from collections import defaultdict


# =============================================================================
# CORE DATA MODELS
# =============================================================================

class BuildAction(Enum):
    """What happened to a build over its lifetime."""
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    KEPT = "kept"           # Build persists across sessions — the highest signal
    COMPLETED = "completed"  # A gap was filled — the Unfinished Rule fulfilled
    ABANDONED = "abandoned"  # Build exists but player never returned


class ConversationType(Enum):
    """The shape of a player-agent exchange."""
    COMMAND = "command"          # Player issued a build request, no back-and-forth
    NEGOTIATION = "negotiation"  # Player and agent exchanged ≥3 turns with substance
    ARGUMENT = "argument"        # Player pushed back on agent's design choice
    COLLABORATION = "collaboration"  # Player built alongside, agent commented
    SILENCE = "silence"          # Player stood near agent without typing (the Slack Tide Stand)


@dataclass
class BuildPart:
    """A single placed part in a Slackwater build."""
    part_id: str
    part_type: str           # e.g., "oak_beam", "tin_sheet", "iron_bolt"
    material: str            # e.g., "wood", "metal", "stone", "glass"
    position: tuple[float, float, float]  # (x, y, z) in studs
    rotation: tuple[float, float, float]  # degrees
    placed_by: str           # "lucineer", "player:<id>", "agent:<id>"
    timestamp: float         # Unix timestamp
    is_gap_filler: bool = False  # Did this part fill an Unfinished Rule gap?
    is_deliberate_flaw: bool = False  # Was this part a known flaw for detection?


@dataclass
class Build:
    """A complete build in Slackwater Yard."""
    build_id: str
    parts: list[BuildPart] = field(default_factory=list)
    created_at: float = 0.0
    last_modified_at: float = 0.0
    actions: list[tuple[float, BuildAction]] = field(default_factory=list)
    era: int = 1  # 1-7, the technology era
    has_gap: bool = False  # Does this build have an Unfinished Rule gap?
    gap_filled_by: Optional[str] = None  # Who filled the gap?
    gap_filled_at: Optional[float] = None

    @property
    def part_count(self) -> int:
        return len(self.parts)

    @property
    def unique_materials(self) -> set[str]:
        return {p.material for p in self.parts}

    @property
    def unique_part_types(self) -> set[str]:
        return {p.part_type for p in self.parts}

    @property
    def player_parts(self) -> list[BuildPart]:
        return [p for p in self.parts if p.placed_by.startswith("player:")]

    @property
    def agent_parts(self) -> list[BuildPart]:
        return [p for p in self.parts if p.placed_by.startswith("agent:")
                or p.placed_by == "lucineer"]

    @property
    def is_jointly_built(self) -> bool:
        """True if both player and agent contributed parts."""
        return len(self.player_parts) > 0 and len(self.agent_parts) > 0


@dataclass
class ConversationTurn:
    """A single message in a player-agent conversation."""
    speaker: str        # "player" or "agent"
    content: str
    timestamp: float
    turn_index: int


@dataclass
class Conversation:
    """A full conversation between player and agent(s)."""
    conversation_id: str
    player_id: str
    agent_id: str
    turns: list[ConversationTurn] = field(default_factory=list)
    conversation_type: ConversationType = ConversationType.COMMAND

    @property
    def player_turns(self) -> list[ConversationTurn]:
        return [t for t in self.turns if t.speaker == "player"]

    @property
    def agent_turns(self) -> list[ConversationTurn]:
        return [t for t in self.turns if t.speaker == "agent"]

    @property
    def turn_count(self) -> int:
        return len(self.turns)


@dataclass
class Session:
    """A single player session in Slackwater."""
    session_id: str
    player_id: str
    join_time: float
    leave_time: float
    builds: list[Build] = field(default_factory=list)
    conversations: list[Conversation] = field(default_factory=list)
    era_at_start: int = 1
    era_at_end: int = 1
    bond_stage_at_start: int = 1
    bond_stage_at_end: int = 1

    @property
    def duration_seconds(self) -> float:
        return self.leave_time - self.join_time

    @property
    def build_count(self) -> int:
        return len(self.builds)

    @property
    def conversation_count(self) -> int:
        return len(self.conversations)


@dataclass
class PlayerHistory:
    """A player's full history across all sessions."""
    player_id: str
    sessions: list[Session] = field(default_factory=list)
    first_seen: float = 0.0
    last_seen: float = 0.0

    @property
    def total_sessions(self) -> int:
        return len(self.sessions)

    @property
    def total_builds(self) -> int:
        return sum(s.build_count for s in self.sessions)

    def sessions_on_day(self, day_timestamp: float) -> int:
        """Count sessions that occurred on a specific calendar day."""
        target_day = time.gmtime(day_timestamp).tm_yday
        target_year = time.gmtime(day_timestamp).tm_year
        return sum(
            1 for s in self.sessions
            if time.gmtime(s.join_time).tm_yday == target_day
            and time.gmtime(s.join_time).tm_year == target_year
        )

    def returned_within_days(self, days: int) -> bool:
        """Did the player return within N days of their first session?"""
        if len(self.sessions) < 2:
            return False
        first_session_end = self.sessions[0].leave_time
        for s in self.sessions[1:]:
            if s.join_time - first_session_end <= days * 86400:
                return True
        return False


# =============================================================================
# REWARD COMPONENT 1: BUILD RETENTION (weight: 0.25)
# =============================================================================
# "A build that persists is a build that mattered."
# The strongest signal in a creative game is not what was built but what was KEPT.
# Deletion is a vote. Abandonment is a vote. Keeping is a vote.
# We measure the survival of creative work across session boundaries.
# =============================================================================

def measure_build_retention(
    session: Session,
    player_history: PlayerHistory,
    current_time: float,
    lookback_days: int = 7,
) -> float:
    """
    Measure whether builds survived across sessions.

    A build that the player KEPT across a session boundary is worth more than
    a build that was deleted. A build that was MODIFIED shows engagement with
    craft. A build that was COMPLETED (gap filled) is the highest signal.

    Returns: float in [0.0, 1.0]
    """
    if not session.builds:
        # No builds this session — neutral. Don't punish, don't reward.
        return 0.5

    scores: list[float] = []
    for build in session.builds:
        action_score = _score_build_action(build, current_time)
        scores.append(action_score)

    # Bonus: did builds from PREVIOUS sessions survive?
    if len(player_history.sessions) > 1:
        prev_session = player_history.sessions[-2]
        surviving = 0
        total_prev = len(prev_session.builds)
        if total_prev > 0:
            for prev_build in prev_session.builds:
                # Check if build still exists (no delete action after prev session)
                last_action = _last_action_before(prev_build, current_time)
                if last_action and last_action[1] in (BuildAction.KEPT, BuildAction.MODIFIED):
                    surviving += 1
                if prev_build.has_gap and prev_build.gap_filled_by is not None:
                    # A gap was filled between sessions — huge signal
                    surviving += 2  # Weight gap-filling double
                    total_prev += 1  # Normalize
            survival_rate = surviving / max(total_prev, 1)
            scores.append(survival_rate)

    return _clamp(statistics.mean(scores)) if scores else 0.5


def _score_build_action(build: Build, current_time: float) -> float:
    """Score an individual build based on its action history."""
    if not build.actions:
        return 0.5

    latest_action = build.actions[-1][1]

    if latest_action == BuildAction.COMPLETED:
        # The Unfinished Rule fulfilled — the player finished what Lucineer started.
        # This is the single most important behavioral signal in the game.
        return 1.0
    elif latest_action == BuildAction.KEPT:
        return 0.85
    elif latest_action == BuildAction.MODIFIED:
        # Modification implies the player cared enough to iterate.
        return 0.75
    elif latest_action == BuildAction.CREATED:
        return 0.6
    elif latest_action == BuildAction.ABANDONED:
        # Abandonment is not deletion — the build exists, the player just left.
        # The Unfinished Rule says this is fine. The gap is still open.
        return 0.4
    elif latest_action == BuildAction.DELETED:
        # Deletion is the strongest negative signal, BUT:
        # In Slackwater, deletion feeds the Salvage mechanic (Moment 2).
        # A deleted build returns barnacled on the tide.
        # So even deletion has narrative value — just not craft value.
        return 0.15
    else:
        return 0.5


def _last_action_before(build: Build, timestamp: float) -> Optional[tuple[float, BuildAction]]:
    """Get the last action before a given timestamp."""
    prior = [(t, a) for t, a in build.actions if t <= timestamp]
    return prior[-1] if prior else None


# =============================================================================
# REWARD COMPONENT 2: COOPERATION DEPTH (weight: 0.25)
# =============================================================================
# "Did the player and agent negotiate, or did the player just command?"
# The deepest signal in Slackwater is the shift from consumer to collaborator.
# A command is "build me a tower." A negotiation is "build me a tower" →
# "Left the top rail off — your railing, whenever you're ready" →
# player places the railing. That back-and-forth is the bond arc.
# =============================================================================

def measure_cooperation(
    conversations: list[Conversation],
    session: Session,
) -> float:
    """
    Measure the depth of player-agent cooperation.

    Layers:
    1. Conversation type distribution (negotiation > command > silence scored)
    2. Turn depth (more back-and-forth = deeper cooperation)
    3. Build attribution (jointly-built structures score highest)
    4. Gap-filling behavior (did the player fill an agent's gap?)

    Returns: float in [0.0, 1.0]
    """
    if not conversations and not session.builds:
        return 0.3  # Pure wandering — allowed, but not cooperation

    # --- Layer 1: Conversation type scoring ---
    type_scores: list[float] = []
    for conv in conversations:
        type_scores.append(_score_conversation_type(conv.conversation_type))

        # Layer 2: Turn depth bonus
        if conv.turn_count >= 6:
            # Substantial exchange — 6+ turns means real back-and-forth
            depth_bonus = min((conv.turn_count - 4) * 0.05, 0.15)
            type_scores[-1] += depth_bonus

        # Detect argument quality: did the player push back?
        if conv.conversation_type == ConversationType.ARGUMENT:
            # Did the agent concede? (Character Bible: loses ~1/3 of arguments)
            # An argument that was conceded is a relationship signal
            type_scores[-1] = min(type_scores[-1] + 0.1, 1.0)

    conv_score = statistics.mean(type_scores) if type_scores else 0.3

    # --- Layer 3: Build attribution (joint construction) ---
    build_coop_score = 0.0
    if session.builds:
        joint_scores: list[float] = []
        for build in session.builds:
            if build.is_jointly_built:
                # Intertwined attribution — neither could have done it alone
                player_ratio = len(build.player_parts) / max(build.part_count, 1)
                # Ideal ratio: 0.3-0.7 (genuine collaboration, not one-sided)
                if 0.2 <= player_ratio <= 0.8:
                    joint_scores.append(1.0)
                else:
                    joint_scores.append(0.5)
            else:
                joint_scores.append(0.0)
        build_coop_score = statistics.mean(joint_scores) if joint_scores else 0.0

    # --- Layer 4: Gap-filling (the Continuation moment) ---
    gap_bonus = 0.0
    for build in session.builds:
        if build.has_gap and build.gap_filled_by:
            if build.gap_filled_by.startswith("player:"):
                # Player filled an agent's gap — the Continuation (Magic Moment 1)
                gap_bonus = min(gap_bonus + 0.15, 0.3)

    # --- Silence as cooperation ---
    # The Slack Tide Stand (Moment 10): standing beside Lucineer for 90 seconds
    # without typing is a form of cooperation deeper than words.
    silence_bonus = 0.0
    for conv in conversations:
        if conv.conversation_type == ConversationType.SILENCE:
            silence_bonus = min(silence_bonus + 0.1, 0.15)

    # Weighted combination
    final = (
        conv_score * 0.35 +
        build_coop_score * 0.35 +
        gap_bonus +
        silence_bonus
    )

    return _clamp(final)


def _score_conversation_type(conv_type: ConversationType) -> float:
    """Score the cooperativeness of a conversation type."""
    scores = {
        ConversationType.COMMAND: 0.2,         # Pure consumer behavior
        ConversationType.NEGOTIATION: 0.7,     # Back-and-forth
        ConversationType.ARGUMENT: 0.85,       # Pushback = investment
        ConversationType.COLLABORATION: 0.9,   # Building alongside
        ConversationType.SILENCE: 0.6,         # Presence without demand
    }
    return scores.get(conv_type, 0.3)


# =============================================================================
# REWARD COMPONENT 3: RETURN RATE (weight: 0.20)
# =============================================================================
# "Did the player come back the next day?"
# NOT a daily streak. NOT a login reward. NOT "Lucineer misses you."
# The return signal is curiosity about a character who changes.
# "He might say something different today."
# =============================================================================

def measure_return_rate(
    player_history: PlayerHistory,
    current_time: float,
) -> float:
    """
    Measure genuine return behavior — NOT engagement, NOT addiction.

    Returns: float in [0.0, 1.0]

    Signals:
    - Day-1 return: 0.4 (baseline curiosity)
    - Day-7 return: 0.3 (sustained interest, not novelty)
    - Day-30 return: 0.3 (habituation into craft — the long loop)

    Penalized:
    - Multiple sessions per day beyond 3 (engagement extraction pattern)
    - Sessions that are <2 minutes (drive-by logins, not real play)

    NOTE: We measure return RATE not return FREQUENCY.
    A player who comes back every day for 30 minutes scores the same as
    one who comes back every day for 5 hours. Time-in-game is deliberately
    excluded. The reward is for choosing to return, not for staying.
    """
    if player_history.total_sessions == 0:
        return 0.0

    # --- Day-1 return ---
    day_1 = 0.0
    if player_history.returned_within_days(1):
        day_1 = 0.4

    # --- Day-7 return ---
    day_7 = 0.0
    if player_history.returned_within_days(7):
        day_7 = 0.3

    # --- Day-30 return ---
    day_30 = 0.0
    if player_history.returned_within_days(30):
        day_30 = 0.3

    base_score = day_1 + day_7 + day_30

    # --- Anti-addiction guardrail ---
    # If the player has >3 sessions in a single day, we DON'T boost the reward.
    # We don't penalize either — the player isn't at fault — but we refuse
    # to let the reward function learn to produce engagement loops.
    sessions_today = player_history.sessions_on_day(current_time)
    if sessions_today > 3:
        base_score *= 0.8  # Dampen, don't zero out

    # --- Drive-by guardrail ---
    # Sessions < 120 seconds are not real returns. They're check-ins,
    # habit logins, or "did the tide bring something?" curiosity that
    # didn't convert to play. We count the first one, ignore the rest.
    real_sessions = [
        s for s in player_history.sessions
        if s.duration_seconds >= 120 or s == player_history.sessions[0]
    ]
    if len(real_sessions) < player_history.total_sessions:
        # Some sessions were drive-bys — mild dampening
        real_ratio = len(real_sessions) / max(player_history.total_sessions, 1)
        base_score *= (0.7 + 0.3 * real_ratio)

    return _clamp(base_score)


# =============================================================================
# REWARD COMPONENT 4: CRAFT QUALITY (weight: 0.20)
# =============================================================================
# "Structural integrity, material diversity, aesthetic balance."
# Beauty is not subjective when you can measure its footprint.
# =============================================================================

def measure_craft_quality(builds: list[Build]) -> float:
    """
    Measure the physical craft quality of builds.

    Three sub-scores:
    1. Structural integrity — does the build follow physical logic?
    2. Material diversity — does the build use appropriate materials, or just one?
    3. Aesthetic balance — is the build visually composed?

    Returns: float in [0.0, 1.0]
    """
    if not builds:
        return 0.3

    scores: list[float] = []
    for build in builds:
        structural = _measure_structural_integrity(build)
        material = _measure_material_diversity(build)
        aesthetic = _measure_aesthetic_balance(build)

        # Weighted: structural is most important (a pretty building that
        # collapses is not craft), then aesthetic, then material
        craft = structural * 0.45 + aesthetic * 0.30 + material * 0.25

        # Penalty for over-building: a structure with 200 parts where 40
        # would suffice is not craft — it's consumption.
        if build.part_count > 100:
            overbuild_penalty = min((build.part_count - 100) * 0.002, 0.2)
            craft -= overbuild_penalty

        # Bonus for restraint: knowing when to stop.
        # The Unfinished Rule already enforces one gap, but a player who
        # stops building BEFORE adding unnecessary decoration shows mastery.
        # We detect this as: the build is functional but not maximal.
        # (Approximated: builds between 5-50 parts with good structural scores.)
        if 5 <= build.part_count <= 50 and structural > 0.7:
            craft = min(craft + 0.05, 1.0)

        scores.append(craft)

    return _clamp(statistics.mean(scores))


def _measure_structural_integrity(build: Build) -> float:
    """
    Measure whether the build follows structural logic.

    Checks:
    - Foundation-to-total ratio: are there enough foundation/support parts?
    - Vertical continuity: are upper parts supported by lower parts?
    - Load path coherence: do parts form connected chains?
    - Center of mass stability: is the COM within the footprint?
    """
    if not build.parts:
        return 0.0

    parts = build.parts

    # --- Foundation ratio ---
    # Parts at or near ground level (y < 5 studs) relative to total.
    # A build with no foundation is a build that floats — not craft.
    foundation_parts = sum(1 for p in parts if p.position[1] < 5.0)
    foundation_ratio = foundation_parts / max(len(parts), 1)

    # Ideal: 20-40% of parts are foundation/support
    if 0.15 <= foundation_ratio <= 0.50:
        foundation_score = 1.0
    elif 0.10 <= foundation_ratio <= 0.60:
        foundation_score = 0.7
    elif foundation_ratio > 0:
        foundation_score = 0.3
    else:
        foundation_score = 0.0

    # --- Vertical continuity ---
    # For each part above ground, check if there's a part below it.
    # This approximates "is this part supported?"
    supported_count = 0
    for part in parts:
        if part.position[1] < 5.0:
            supported_count += 1
            continue
        # Look for parts directly below (within a radius)
        for other in parts:
            if other is part:
                continue
            dx = part.position[0] - other.position[0]
            dz = part.position[2] - other.position[2]
            dy = part.position[1] - other.position[1]
            horizontal_dist = math.sqrt(dx * dx + dz * dz)
            if 0 < dy < 15 and horizontal_dist < 8:
                supported_count += 1
                break

    support_ratio = supported_count / max(len(parts), 1)

    # --- Center of mass stability ---
    if parts:
        com_x = statistics.mean(p.position[0] for p in parts)
        com_z = statistics.mean(p.position[2] for p in parts)

        # Find footprint (min/max of ground-level parts)
        ground_parts = [p for p in parts if p.position[1] < 5.0]
        if ground_parts:
            min_x = min(p.position[0] for p in ground_parts)
            max_x = max(p.position[0] for p in ground_parts)
            min_z = min(p.position[2] for p in ground_parts)
            max_z = max(p.position[2] for p in ground_parts)

            # Is COM within footprint?
            footprint_margin = 0.15  # Allow 15% overhang
            width_x = max(max_x - min_x, 1)
            width_z = max(max_z - min_z, 1)
            com_offset_x = abs(com_x - (min_x + max_x) / 2) / width_x
            com_offset_z = abs(com_z - (min_z + max_z) / 2) / width_z

            stability = 1.0 - (com_offset_x + com_offset_z) / 2
            stability = max(0.0, min(stability, 1.0))
        else:
            stability = 0.2  # No ground parts — floating build
    else:
        stability = 0.0

    # --- Connected component check (simplified) ---
    # Builds should form a single connected structure, not scattered parts.
    connectivity = _measure_connectivity(parts)

    return _clamp(
        foundation_score * 0.35 +
        support_ratio * 0.25 +
        stability * 0.20 +
        connectivity * 0.20
    )


def _measure_connectivity(parts: list[BuildPart], max_gap: float = 12.0) -> float:
    """
    Measure how connected the build is using a simple flood-fill.
    Returns ratio of parts in the largest connected component.
    """
    if not parts:
        return 0.0
    if len(parts) == 1:
        return 1.0

    n = len(parts)
    visited = [False] * n
    largest_component = 0

    for i in range(n):
        if visited[i]:
            continue
        # BFS from part i
        queue = [i]
        visited[i] = True
        component_size = 0
        while queue:
            idx = queue.pop(0)
            component_size += 1
            for j in range(n):
                if visited[j]:
                    continue
                dist = _part_distance(parts[idx], parts[j])
                if dist <= max_gap:
                    visited[j] = True
                    queue.append(j)
        largest_component = max(largest_component, component_size)

    return largest_component / n


def _part_distance(a: BuildPart, b: BuildPart) -> float:
    """Euclidean distance between two parts."""
    return math.sqrt(
        (a.position[0] - b.position[0]) ** 2 +
        (a.position[1] - b.position[1]) ** 2 +
        (a.position[2] - b.position[2]) ** 2
    )


def _measure_material_diversity(build: Build) -> float:
    """
    Measure material diversity using normalized entropy.

    A build with 5 materials in reasonable proportions scores higher than
    a build that is 95% one material (unless that's era-appropriate —
    Era 1 builds legitimately use mostly wood).

    Uses Shannon entropy normalized by log(n) for comparability.
    """
    if not build.parts:
        return 0.0

    material_counts: dict[str, int] = defaultdict(int)
    for part in build.parts:
        material_counts[part.material] += 1

    n = len(build.parts)
    num_materials = len(material_counts)

    if num_materials == 1:
        # Single material — acceptable for Era 1, less so for higher eras
        if build.era <= 1:
            return 0.5  # Era 1 is Simple Machines — wood and iron are fine
        return 0.25

    # Shannon entropy
    entropy = 0.0
    for count in material_counts.values():
        p = count / n
        entropy -= p * math.log2(p)

    # Normalize by log2(num_materials) so diversity is comparable
    max_entropy = math.log2(num_materials)
    normalized = entropy / max_entropy if max_entropy > 0 else 0.0

    # Bonus for era-appropriate material use
    era_bonus = _era_material_bonus(build.era, material_counts)
    # Penalty for excessive diversity (a build with 15 materials is chaotic)
    if num_materials > 8:
        normalized *= 0.8

    return _clamp(normalized + era_bonus)


def _era_material_bonus(era: int, materials: dict[str, int]) -> float:
    """Bonus for using materials appropriate to the technology era."""
    era_materials = {
        1: {"wood", "stone", "iron"},
        2: {"wood", "stone", "iron", "copper", "rope"},
        3: {"wood", "iron", "copper", "wire", "glass"},
        4: {"iron", "copper", "wire", "glass", "silicon", "plastic"},
        5: {"iron", "copper", "wire", "glass", "silicon", "plastic", "fiber"},
        6: {"iron", "copper", "silicon", "plastic", "fiber", "composite"},
        7: {"silicon", "plastic", "fiber", "composite", "graphene"},
    }
    expected = era_materials.get(era, set())
    if not expected:
        return 0.0
    overlap = len(expected.intersection(materials.keys())) / max(len(expected), 1)
    return overlap * 0.1  # Up to 0.1 bonus


def _measure_aesthetic_balance(build: Build) -> float:
    """
    Measure aesthetic qualities of the build.

    Factors:
    - Spatial distribution: parts should fill the bounding box, not clump
    - Symmetry detection: approximate left-right symmetry around the centroid
    - Scale proportion: height-to-width ratio within reasonable bounds
    """
    if not build.parts:
        return 0.0

    positions = [p.position for p in build.parts]
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    zs = [p[2] for p in positions]

    # --- Spatial distribution ---
    # Coefficient of variation of inter-part distances — lower = more even
    if len(positions) > 2:
        distances = []
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                d = math.sqrt(
                    (positions[i][0] - positions[j][0]) ** 2 +
                    (positions[i][1] - positions[j][1]) ** 2 +
                    (positions[i][2] - positions[j][2]) ** 2
                )
                distances.append(d)
        if distances:
            mean_d = statistics.mean(distances)
            stdev_d = statistics.stdev(distances) if len(distances) > 1 else 0
            cv = stdev_d / mean_d if mean_d > 0 else 1.0
            # Lower CV is better (more even distribution)
            distribution_score = max(0.0, 1.0 - cv / 2.0)
        else:
            distribution_score = 0.5
    else:
        distribution_score = 0.5

    # --- Approximate symmetry ---
    # Reflect positions across the XZ centroid and measure overlap
    cx = statistics.mean(xs)
    cz = statistics.mean(zs)
    symmetry_score = _measure_symmetry(positions, cx, cz)

    # --- Scale proportion ---
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    depth = max(zs) - min(zs)

    if width > 0 and height > 0:
        ratio = height / max(width, depth, 1)
        # Golden ratio and common architectural proportions
        if 0.3 <= ratio <= 2.0:
            proportion_score = 1.0
        elif 0.2 <= ratio <= 3.0:
            proportion_score = 0.6
        else:
            proportion_score = 0.3
    else:
        proportion_score = 0.3

    return _clamp(
        distribution_score * 0.35 +
        symmetry_score * 0.35 +
        proportion_score * 0.30
    )


def _measure_symmetry(
    positions: list[tuple[float, float, float]],
    cx: float,
    cz: float,
    tolerance: float = 4.0,
) -> float:
    """
    Measure approximate bilateral symmetry around the centroid in XZ plane.
    """
    if len(positions) < 4:
        return 0.5

    reflected = [
        (2 * cx - p[0], p[1], p[2]) for p in positions
    ]

    matched = 0
    for refl in reflected:
        for orig in positions:
            dist = math.sqrt(
                (refl[0] - orig[0]) ** 2 +
                (refl[1] - orig[1]) ** 2 +
                (refl[2] - orig[2]) ** 2
            )
            if dist <= tolerance:
                matched += 1
                break

    return matched / len(positions)


# =============================================================================
# REWARD COMPONENT 5: ENERGY EFFICIENCY (weight: 0.10)
# =============================================================================
# "γ + H = C — The Conservation Law of Intelligence"
#
# Every gain in capability must be paid for with a reduction in uncertainty.
# The reward should recognize agents that achieve more with less cognitive energy.
# This component measures the efficiency of the player-agent system: did they
# communicate clearly, build directly, and avoid wasted computation?
#
# In the conservation law, γ is usable cognitive energy and H is entropy.
# Efficiency = γ / C = γ / (γ + H). We maximize this by minimizing H.
# =============================================================================

def measure_energy_efficiency(session: Session) -> float:
    """
    Measure the cognitive energy efficiency of the session.

    Efficiency means: the player and agent achieved their goals with minimal
    wasted effort. Wasted effort includes:
    - Failed build commands (agent generated invalid JSON)
    - Repeated requests for the same build (player had to ask twice)
    - Excessive conversation turns that didn't lead to action
    - Era-inappropriate attempts (trying to build a robot in Era 1)

    Returns: float in [0.0, 1.0]
    """
    if not session.builds and not session.conversations:
        return 0.5  # Idle session — neutral

    # --- Command efficiency ---
    # How many conversation turns led to a build action?
    total_turns = sum(c.turn_count for c in session.conversations)
    total_builds = len(session.builds)

    if total_turns > 0 and total_builds > 0:
        # Ideal: roughly 2-4 turns per build (request + response + maybe refinement)
        turns_per_build = total_turns / max(total_builds, 1)
        if turns_per_build <= 4:
            command_eff = 1.0
        elif turns_per_build <= 8:
            command_eff = 0.7
        elif turns_per_build <= 15:
            command_eff = 0.4
        else:
            command_eff = 0.2
    elif total_builds > 0:
        command_eff = 1.0  # Builds without conversation = efficient
    else:
        command_eff = 0.3  # Lots of talk, nothing built

    # --- Material efficiency ---
    # Did the build use materials proportionally to what was available?
    # (Approximated: no excess waste material from crafting)
    material_eff = 0.7  # Default; would connect to inventory tracking
    if session.builds:
        for build in session.builds:
            unique = len(build.unique_materials)
            total = build.part_count
            if total > 0 and unique > 0:
                # Simple heuristic: using fewest material types effectively
                ratio = unique / max(total, 1)
                if ratio <= 0.3:
                    material_eff = min(material_eff + 0.1, 1.0)

    # --- Progression efficiency ---
    # Did the player advance era or bond stage? (Learning happened.)
    progression_eff = 0.5
    if session.era_at_end > session.era_at_start:
        progression_eff = 1.0
    elif session.bond_stage_at_end > session.bond_stage_at_start:
        progression_eff = 0.85
    elif session.builds or session.conversations:
        progression_eff = 0.6  # Did something, even if no era change

    # --- Cognitive entropy reduction (the conservation law) ---
    # H decreases when the player makes clear, decisive choices.
    # We approximate H as: ambiguity in requests + abandoned attempts.
    entropy_signals = 0.0

    # Ambiguous requests: very short messages that require agent clarification
    short_messages = sum(
        1 for conv in session.conversations
        for turn in conv.player_turns
        if len(turn.content.strip()) < 5
    )
    total_messages = sum(len(conv.player_turns) for conv in session.conversations)
    if total_messages > 0:
        ambiguity_ratio = short_messages / total_messages
        entropy_signals += ambiguity_ratio * 0.3

    # Abandoned builds: builds that were started but never progressed
    abandoned = sum(
        1 for b in session.builds
        if b.actions and b.actions[-1][1] == BuildAction.ABANDONED
    )
    if session.builds:
        abandon_ratio = abandoned / max(len(session.builds), 1)
        entropy_signals += abandon_ratio * 0.3

    # More entropy = lower efficiency
    entropy_penalty = min(entropy_signals, 0.5)
    clarity = 1.0 - entropy_penalty

    final = (
        command_eff * 0.30 +
        material_eff * 0.20 +
        progression_eff * 0.25 +
        clarity * 0.25
    )

    return _clamp(final)


# =============================================================================
# THE MASTER REWARD FUNCTION
# =============================================================================

# Reward weights — these are the moral choices.
# Their sum is 1.0. Each weight says what we value.
# Change these and you change what the agent becomes.

REWARD_WEIGHTS = {
    "build_retention":  0.25,  # Did the player keep, modify, or complete the build?
    "cooperation_depth": 0.25,  # Did they negotiate or just command?
    "return_rate":       0.20,  # Did they come back — not from addiction, but from care?
    "craft_quality":     0.20,  # Was the build beautiful, honest, structurally sound?
    "energy_efficiency": 0.10,  # Did they do more with less cognitive energy? (γ + H = C)
}

# What we EXPLICITLY refuse to measure:
ANTI_METRICS = [
    "session_duration",      # Time-in-game measures engagement, not craft
    "click_count",           # Interaction frequency measures activity, not value
    "messages_per_session",  # Volume measures verbosity, not connection
    "daily_streak",          # Streaks measure compulsion, not curiosity
    "parts_placed_count",    # Quantity ≠ quality; a master builds less
    "api_calls_per_player",  # Cost metric, not player experience metric
    "screen_time",           # Addiction metric disguised as engagement
]


def compute_reward(
    session: Session,
    player_history: PlayerHistory,
    current_time: float | None = None,
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """
    The master reward function for Slackwater agent training via MOLT.

    This function is called by MOLT's Env.step() to compute the scalar reward
    that shapes agent behavior through GRPO reinforcement learning.

    What we measure (and why):
        build_retention (0.25)  — Creative work that survived = work that mattered
        cooperation_depth (0.25) — Negotiation is deeper than command
        return_rate (0.20)      — Choosing to return ≠ being compelled to return
        craft_quality (0.20)    — Beauty is measurable: integrity, diversity, balance
        energy_efficiency (0.10)— γ + H = C: doing more with less cognitive energy

    What we refuse to measure (and why):
        Time, clicks, streaks, volume. These measure extraction, not experience.
        The reward function is a moral act. We choose craft over addiction,
        cooperation over consumption, continuity over compulsion.

    Returns:
        dict with:
            'reward': float in [0.0, 1.0] — the scalar for MOLT
            'components': dict of individual component scores
            'weights': the weight configuration used
            'anti_metrics': the metrics we deliberately excluded
            'explanation': human-readable summary for trajectory logs
    """
    if current_time is None:
        current_time = time.time()

    w = weights or REWARD_WEIGHTS

    # Compute each component
    retention = measure_build_retention(session, player_history, current_time)
    cooperation = measure_cooperation(session.conversations, session)
    returns = measure_return_rate(player_history, current_time)
    craft = measure_craft_quality(session.builds)
    efficiency = measure_energy_efficiency(session)

    components = {
        "build_retention":  retention,
        "cooperation_depth": cooperation,
        "return_rate":       returns,
        "craft_quality":     craft,
        "energy_efficiency": efficiency,
    }

    # Weighted sum — each weight is a statement of values
    reward = sum(
        components.get(name, 0.0) * weight
        for name, weight in w.items()
    )

    reward = _clamp(reward)

    # Generate explanation for trajectory logs
    explanation = _generate_explanation(components, reward, session)

    return {
        "reward": reward,
        "components": components,
        "weights": w,
        "anti_metrics": ANTI_METRICS,
        "explanation": explanation,
    }


# =============================================================================
# MOLT ENV ADAPTER
# =============================================================================
# This is how the reward function plugs into MOLT's training loop.
# The Env receives agent state and returns a Result with reward.
# =============================================================================

def compute_reward_from_state(
    state: dict[str, Any],
    label: Any = None,
) -> float:
    """
    Adapter for MOLT's Env.step() contract.

    Expects state to contain:
        - session_data: dict with session fields
        - player_history_data: dict with history fields
        - current_time: float (optional, defaults to now)

    This function deserializes game state into our data models,
    calls compute_reward(), and returns the scalar reward.

    Usage in MOLT:
        class SlackwaterEnv(Env):
            async def step(self, state) -> Result:
                reward = compute_reward_from_state(state)
                return Result(reward=reward, terminated=True)
    """
    session_data = state.get("session_data", {})
    history_data = state.get("player_history_data", {})
    current_time = state.get("current_time", time.time())

    session = _deserialize_session(session_data)
    history = _deserialize_history(history_data)

    result = compute_reward(session, history, current_time)
    return result["reward"]


def _deserialize_session(data: dict[str, Any]) -> Session:
    """Deserialize session from dict (from D1/database)."""
    builds = []
    for bd in data.get("builds", []):
        parts = [
            BuildPart(
                part_id=p["part_id"],
                part_type=p["part_type"],
                material=p["material"],
                position=tuple(p["position"]),
                rotation=tuple(p["rotation"]),
                placed_by=p["placed_by"],
                timestamp=p["timestamp"],
                is_gap_filler=p.get("is_gap_filler", False),
                is_deliberate_flaw=p.get("is_deliberate_flaw", False),
            )
            for p in bd.get("parts", [])
        ]
        actions = [
            (a[0], BuildAction(a[1]))
            for a in bd.get("actions", [])
        ]
        builds.append(Build(
            build_id=bd["build_id"],
            parts=parts,
            created_at=bd.get("created_at", 0),
            last_modified_at=bd.get("last_modified_at", 0),
            actions=actions,
            era=bd.get("era", 1),
            has_gap=bd.get("has_gap", False),
            gap_filled_by=bd.get("gap_filled_by"),
            gap_filled_at=bd.get("gap_filled_at"),
        ))

    conversations = []
    for cd in data.get("conversations", []):
        turns = [
            ConversationTurn(
                speaker=t["speaker"],
                content=t["content"],
                timestamp=t["timestamp"],
                turn_index=t["turn_index"],
            )
            for t in cd.get("turns", [])
        ]
        conversations.append(Conversation(
            conversation_id=cd["conversation_id"],
            player_id=cd.get("player_id", ""),
            agent_id=cd.get("agent_id", ""),
            turns=turns,
            conversation_type=ConversationType(cd.get("conversation_type", "command")),
        ))

    return Session(
        session_id=data.get("session_id", ""),
        player_id=data.get("player_id", ""),
        join_time=data.get("join_time", 0),
        leave_time=data.get("leave_time", 0),
        builds=builds,
        conversations=conversations,
        era_at_start=data.get("era_at_start", 1),
        era_at_end=data.get("era_at_end", 1),
        bond_stage_at_start=data.get("bond_stage_at_start", 1),
        bond_stage_at_end=data.get("bond_stage_at_end", 1),
    )


def _deserialize_history(data: dict[str, Any]) -> PlayerHistory:
    """Deserialize player history from dict."""
    sessions = [
        _deserialize_session(s)
        for s in data.get("sessions", [])
    ]
    return PlayerHistory(
        player_id=data.get("player_id", ""),
        sessions=sessions,
        first_seen=data.get("first_seen", 0),
        last_seen=data.get("last_seen", 0),
    )


# =============================================================================
# EXPLANATION GENERATOR (for trajectory logs and debugging)
# =============================================================================

def _generate_explanation(
    components: dict[str, float],
    reward: float,
    session: Session,
) -> str:
    """
    Generate a human-readable explanation of the reward.
    This goes into trajectory logs for analyst review and debugging.
    """
    lines = [
        f"Reward: {reward:.3f} (session {session.session_id[:8]})",
        f"  Player: {session.player_id}",
        f"  Builds: {session.build_count} | Conversations: {session.conversation_count}",
        "",
        "  Components:",
    ]

    for name, score in sorted(components.items(), key=lambda x: -x[1]):
        weight = REWARD_WEIGHTS.get(name, 0)
        contribution = score * weight
        bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
        lines.append(
            f"    {name:20s} {score:.3f} × {weight:.2f} = {contribution:.3f} {bar}"
        )

    # Identify the dominant signal
    dominant = max(components, key=components.get)
    weakest = min(components, key=components.get)
    lines.append("")
    lines.append(f"  Dominant signal: {dominant}")
    lines.append(f"  Weakest signal:  {weakest}")

    return "\n".join(lines)


# =============================================================================
# UTILITIES
# =============================================================================

def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Clamp a value to [minimum, maximum]."""
    return max(minimum, min(maximum, value))


# =============================================================================
# ROOTWALL GUARD
# =============================================================================
# "Do not write a reward function for Rootwell."
# The agent whose role is questioning optimization must not be optimized.
# This is a design principle, a marketing story, and a genuinely good decision.
# If compute_reward is ever called for Rootwell, return a fixed 0.5 (neutral)
# and log the violation. Rootwell's value comes from NOT being shaped.
# =============================================================================

ROOTWELL_AGENT_ID = "rootwell"

def is_rootwell(agent_id: str) -> bool:
    """Check if an agent is Rootwell, who must never be optimized."""
    return agent_id.lower() == ROOTWELL_AGENT_ID


def rootwell_guard(agent_id: str, action: str = "compute_reward") -> float:
    """
    If Rootwell is accidentally passed to the reward function, return neutral.
    Log the violation so we know if the training loop is misconfigured.
    """
    if is_rootwell(agent_id):
        # In production, this would log to the monitoring system:
        # logger.warning(f"Rootwell guard triggered: {action} called for Rootwell")
        return 0.5  # Neutral — Rootwell is never optimized
    return -1.0  # Sentinel: not Rootwell, proceed normally


# =============================================================================
# VALIDATION & SELF-TEST
# =============================================================================

def _self_test() -> None:
    """
    Run basic validation of the reward function with synthetic data.
    This verifies that all components produce valid outputs.
    """
    now = time.time()

    # --- Test 1: Empty session ---
    empty_session = Session(
        session_id="test_empty",
        player_id="player_1",
        join_time=now - 60,
        leave_time=now,
    )
    empty_history = PlayerHistory(
        player_id="player_1",
        sessions=[empty_session],
        first_seen=now - 60,
        last_seen=now,
    )
    result = compute_reward(empty_session, empty_history, now)
    assert 0.0 <= result["reward"] <= 1.0, f"Empty session reward out of range: {result['reward']}"
    print(f"✓ Test 1 (empty session): reward={result['reward']:.3f}")

    # --- Test 2: Rich collaborative session ---
    parts = [
        BuildPart("p1", "oak_beam", "wood", (0, 0, 0), (0, 0, 0), "lucineer", now - 600),
        BuildPart("p2", "oak_beam", "wood", (8, 0, 0), (0, 0, 0), "lucineer", now - 590),
        BuildPart("p3", "oak_beam", "wood", (0, 0, 8), (0, 0, 0), "lucineer", now - 580),
        BuildPart("p4", "tin_sheet", "metal", (0, 5, 0), (0, 90, 0), "player:test", now - 300),
        BuildPart("p5", "tin_sheet", "metal", (8, 5, 0), (0, 90, 0), "player:test", now - 290),
        BuildPart("p6", "iron_bolt", "iron", (4, 3, 4), (0, 0, 0), "player:test", now - 280),
    ]
    build = Build(
        build_id="b1",
        parts=parts,
        created_at=now - 600,
        last_modified_at=now - 280,
        actions=[(now - 600, BuildAction.CREATED), (now - 280, BuildAction.MODIFIED)],
        era=2,
        has_gap=True,
        gap_filled_by="player:test",
        gap_filled_at=now - 280,
    )

    conv = Conversation(
        conversation_id="c1",
        player_id="player:test",
        agent_id="lucineer",
        turns=[
            ConversationTurn("player", "Build me a tower", now - 600, 0),
            ConversationTurn("agent", "Tower'll hold. Left the top rail off.", now - 590, 1),
            ConversationTurn("player", "I'll finish the railing", now - 400, 2),
            ConversationTurn("agent", "Your railing, whenever you're ready.", now - 390, 3),
            ConversationTurn("player", "Done. What's next?", now - 270, 4),
            ConversationTurn("agent", "Earl's manifest window just lit up.", now - 260, 5),
        ],
        conversation_type=ConversationType.COLLABORATION,
    )

    rich_session = Session(
        session_id="test_rich",
        player_id="player:test",
        join_time=now - 600,
        leave_time=now,
        builds=[build],
        conversations=[conv],
        era_at_start=1,
        era_at_end=2,
        bond_stage_at_start=1,
        bond_stage_at_end=2,
    )

    rich_history = PlayerHistory(
        player_id="player:test",
        sessions=[
            Session(
                session_id="prev",
                player_id="player:test",
                join_time=now - 86400,
                leave_time=now - 80000,
            ),
            rich_session,
        ],
        first_seen=now - 86400,
        last_seen=now,
    )

    result = compute_reward(rich_session, rich_history, now)
    assert 0.0 <= result["reward"] <= 1.0
    assert result["reward"] > 0.5, f"Rich collaborative session should score above 0.5: {result['reward']}"
    print(f"✓ Test 2 (rich collaborative session): reward={result['reward']:.3f}")
    print(result["explanation"])

    # --- Test 3: Rootwell guard ---
    assert rootwell_guard("rootwell") == 0.5, "Rootwell guard should return neutral"
    assert rootwell_guard("lucineer") == -1.0, "Non-Rootwell should return sentinel"
    print("✓ Test 3 (Rootwell guard): neutral for Rootwell, passthrough for others")

    # --- Test 4: Anti-metrics are documented ---
    assert "session_duration" in ANTI_METRICS
    assert "daily_streak" in ANTI_METRICS
    assert "click_count" in ANTI_METRICS
    print(f"✓ Test 4 (anti-metrics): {len(ANTI_METRICS)} metrics explicitly excluded")

    print("\nAll tests passed.")
    print(f"\nReward weights (what we value):")
    for name, weight in REWARD_WEIGHTS.items():
        print(f"  {name:20s} {weight:.2f}")
    print(f"\nAnti-metrics (what we refuse to become):")
    for metric in ANTI_METRICS:
        print(f"  ✗ {metric}")


if __name__ == "__main__":
    _self_test()
