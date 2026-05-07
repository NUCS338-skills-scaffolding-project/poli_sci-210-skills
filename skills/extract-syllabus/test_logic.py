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
