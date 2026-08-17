#!/usr/bin/env python3
"""Regression tests for the Wesley night school pure logic.

Covers the transformations shared by ``wesley-session.py`` and
``wesley-teacher.py`` without needing a live Ollama GPU or a Cloudflare
token. Run with::

    pytest test_wesley_night_school.py
"""
import wesley_night_school as wns


# --- slug -----------------------------------------------------------------

def test_slug_strips_date_stamp_and_extension():
    assert wns.slug("2026-08-13-1745-the-watch-that-never-ends.md") == "the-watch-that-never-ends"


def test_slug_leaves_unstamped_names_alone():
    assert wns.slug("the-shell.md") == "the-shell"


def test_slug_strips_quota_gate_prefix():
    assert wns.slug("2026-08-11-0800-a-letter-from-the-quota-gate.md") == "a-letter-from-the-quota-gate"


# --- build_prompt ---------------------------------------------------------

def test_build_prompt_embeds_body_at_end():
    prompt = wns.build_prompt("the body")
    assert prompt.endswith("---\n\nthe body")


def test_build_prompt_carries_the_standing_assignment():
    prompt = wns.build_prompt("")
    assert "3-sentence creative response" in prompt
    assert "one image that is NOT in the original" in prompt
    assert "Be surprised" in prompt


# --- render_session_file --------------------------------------------------

def test_render_session_file_has_expected_markers_and_fields():
    out = wns.render_session_file(
        slug="the-watch-that-never-ends",
        source="2026-08-13-1745-the-watch-that-never-ends.md",
        timestamp="2026-08-14 16:35",
        eval_tokens=227,
        done_reason="stop",
        text="The answer.",
        body="line one\nline two\nline three",
    )
    assert out.startswith("# Wesley reads: the-watch-that-never-ends\n")
    assert "Source: 2026-08-13-1745-the-watch-that-never-ends.md" in out
    assert "Generated 227 tokens, done_reason=stop." in out
    assert "Reading time: 3 lines fed." in out
    # exactly two separators: one opens the response, one closes it
    assert out.count("---") == 2
    assert "\n\nThe answer.\n\n---\n\n" in out


def test_render_session_file_counts_empty_body_lines():
    out = wns.render_session_file(
        slug="x", source="x.md", timestamp="t", eval_tokens=0,
        done_reason="?", text="", body="",
    )
    assert "Reading time: 0 lines fed." in out


# --- extract_response_body ------------------------------------------------

def test_extract_response_body_returns_middle_segment():
    doc = "# header\n\n*meta*\n\n---\n\nThe answer.\n\n---\n\n*footer*\n"
    assert wns.extract_response_body(doc) == "The answer."


def test_extract_response_body_survives_markers_inside_response():
    # A response that itself uses a "---" separator must not be truncated.
    doc = "# header\n\n---\n\npart one\n---\npart two\n\n---\n\n*footer*\n"
    assert wns.extract_response_body(doc) == "part one\n---\npart two"


def test_extract_response_body_falls_back_without_markers():
    assert wns.extract_response_body("no markers here") == "no markers here"


def test_extract_response_body_falls_back_with_single_marker():
    assert wns.extract_response_body("before\n---\nafter") == "before\n---\nafter"


def test_extract_response_body_strips_surrounding_whitespace():
    doc = "---\n\n   padded response   \n\n---"
    assert wns.extract_response_body(doc) == "padded response"
