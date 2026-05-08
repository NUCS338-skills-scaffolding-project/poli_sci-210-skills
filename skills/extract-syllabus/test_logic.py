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
