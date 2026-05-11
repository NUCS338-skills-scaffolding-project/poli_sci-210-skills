"""Tests for extract-syllabus/logic.py.

Pure Python — no network, no LLM, no orchestrator dependency.
Run from the repo root or via the orchestrator's pytest (testpaths includes this dir).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from logic import parse_extraction, ParseError


HERE = Path(__file__).parent
FIXTURES = HERE / "fixtures"


def _read_fixture(name: str) -> str:
    return (FIXTURES / name).read_text()


def test_parses_well_formed_response():
    raw = _read_fixture("sample_llm_output.json")
    expected = json.loads(_read_fixture("expected.json"))

    result = parse_extraction(raw)

    assert result == expected


def test_drops_malformed_rows_and_records_warnings():
    raw = _read_fixture("malformed_rows.json")
    result = parse_extraction(raw)

    names = [a["name"] for a in result["assignments"]]
    assert names == ["Good 1", "Good 2"]
    assert len(result["warnings"]) == 2
    assert all("missing name" in w for w in result["warnings"])


def test_invalid_top_level_json_raises():
    with pytest.raises(ParseError):
        parse_extraction("not actually json {{{")


def test_top_level_array_raises():
    with pytest.raises(ParseError):
        parse_extraction("[]")


def test_strips_markdown_code_fences():
    payload = json.dumps({
        "course": {"code": "X", "name": "", "instructor": "", "term": ""},
        "assignments": [{"name": "A", "type": "writing", "due": "", "prompt": ""}],
        "warnings": [],
    })
    fenced = f"```json\n{payload}\n```"
    result = parse_extraction(fenced)
    assert result["course"]["code"] == "X"
    assert result["assignments"][0]["name"] == "A"

    bare = f"```\n{payload}\n```"
    assert parse_extraction(bare)["assignments"][0]["name"] == "A"


def test_strips_unknown_assignment_types():
    raw = json.dumps({
        "course": {"code": "", "name": "", "instructor": "", "term": ""},
        "assignments": [
            {"name": "Midterm", "type": "midterm", "due": "Wk5", "prompt": "p"},
        ],
        "warnings": [],
    })
    result = parse_extraction(raw)
    assert result["assignments"][0]["type"] == "homework"
    assert any("unknown type" in w for w in result["warnings"])


def test_term_start_extracted_when_valid_iso():
    raw = '{"course": {"code": "X", "name": "Y", "instructor": "", "term": "", "term_start": "2026-04-02"}, "assignments": [], "warnings": []}'
    result = parse_extraction(raw)
    assert result["course"]["term_start"] == "2026-04-02"


def test_term_start_coerced_to_empty_when_missing():
    raw = '{"course": {"code": "X", "name": "Y", "instructor": "", "term": ""}, "assignments": [], "warnings": []}'
    result = parse_extraction(raw)
    assert result["course"]["term_start"] == ""


def test_term_start_coerced_to_empty_when_malformed():
    raw = '{"course": {"code": "X", "name": "Y", "instructor": "", "term": "", "term_start": "April 2"}, "assignments": [], "warnings": []}'
    result = parse_extraction(raw)
    assert result["course"]["term_start"] == ""
    assert any("term_start" in w for w in result["warnings"])


def _wrap_assignment(row: dict) -> str:
    """Helper: minimal extraction envelope with one assignment row."""
    payload = {
        "course": {"code": "X", "name": "Y", "instructor": "", "term": ""},
        "assignments": [row],
        "warnings": [],
    }
    return json.dumps(payload)


def test_recurrence_missing_becomes_null():
    raw = _wrap_assignment({"name": "HW1", "type": "homework", "due": "May 3", "prompt": ""})
    result = parse_extraction(raw)
    assert result["assignments"][0]["recurrence"] is None


def test_recurrence_well_formed_passes_through():
    raw = _wrap_assignment({
        "name": "Quiz", "type": "quiz", "due": "Fridays weekly", "prompt": "",
        "recurrence": {"kind": "weekly", "count": 7, "anchor_weekday": "Friday", "first_week": 2, "skip_weeks": []},
    })
    result = parse_extraction(raw)
    rec = result["assignments"][0]["recurrence"]
    assert rec["kind"] == "weekly"
    assert rec["count"] == 7
    assert rec["anchor_weekday"] == "Friday"
    assert rec["first_week"] == 2
    assert rec["skip_weeks"] == []


def test_recurrence_unknown_kind_dropped_with_warning():
    raw = _wrap_assignment({
        "name": "Quiz", "type": "quiz", "due": "biweekly", "prompt": "",
        "recurrence": {"kind": "biweekly", "count": 7, "anchor_weekday": "Friday"},
    })
    result = parse_extraction(raw)
    assert result["assignments"][0]["recurrence"] is None
    assert any("Quiz" in w and "kind" in w for w in result["warnings"])


def test_recurrence_invalid_count_dropped_with_warning():
    raw = _wrap_assignment({
        "name": "Quiz", "type": "quiz", "due": "", "prompt": "",
        "recurrence": {"kind": "weekly", "count": 0, "anchor_weekday": "Friday"},
    })
    result = parse_extraction(raw)
    assert result["assignments"][0]["recurrence"] is None
    assert any("Quiz" in w and "count" in w for w in result["warnings"])


def test_recurrence_unknown_weekday_dropped_with_warning():
    raw = _wrap_assignment({
        "name": "Quiz", "type": "quiz", "due": "", "prompt": "",
        "recurrence": {"kind": "weekly", "count": 7, "anchor_weekday": "Funday"},
    })
    result = parse_extraction(raw)
    assert result["assignments"][0]["recurrence"] is None
    assert any("Quiz" in w and "anchor_weekday" in w for w in result["warnings"])


def test_recurrence_defaults_first_week_and_skip_weeks():
    raw = _wrap_assignment({
        "name": "Quiz", "type": "quiz", "due": "", "prompt": "",
        "recurrence": {"kind": "weekly", "count": 7, "anchor_weekday": "Friday"},
    })
    result = parse_extraction(raw)
    rec = result["assignments"][0]["recurrence"]
    assert rec["first_week"] == 1
    assert rec["skip_weeks"] == []
