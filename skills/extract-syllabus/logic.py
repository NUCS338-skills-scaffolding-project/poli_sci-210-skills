"""extract-syllabus — parser for the LLM's structured response.

Validates and normalizes the JSON returned by the prompt in skills.md.
- Drops malformed assignment rows; appends explanatory strings to `warnings`.
- Coerces unknown `type` values to `homework`.
- Raises ParseError on top-level invalid JSON.
"""
from __future__ import annotations

import json
import re
from typing import Any


INPUT_SCHEMA: dict = {
    "llm_output": "str",  # raw text returned by the LLM for the prompt in skills.md
}


_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


ALLOWED_TYPES = {"writing", "code", "quiz", "homework"}
ALLOWED_RECURRENCE_KINDS = {"weekly"}
ALLOWED_WEEKDAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}


class ParseError(Exception):
    """Raised when the LLM output isn't valid JSON or lacks the top-level shape."""


def _strip_code_fences(s: str) -> str:
    """Remove surrounding ```json … ``` or ``` … ``` markdown fences.

    LLMs frequently wrap JSON in fences despite "JSON only" instructions.
    Strips at most one outer fenced block; bare JSON passes through unchanged.
    """
    s = s.strip()
    if not s.startswith("```"):
        return s
    nl = s.find("\n")
    if nl == -1:
        return s
    body = s[nl + 1:]
    if body.endswith("```"):
        body = body[:-3]
    return body.strip()


def parse_extraction(llm_output: str) -> dict[str, Any]:
    cleaned = _strip_code_fences(llm_output)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ParseError(f"LLM output is not valid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ParseError("LLM output must be a JSON object")

    warnings: list[str] = list(data.get("warnings") or [])
    course = _normalize_course(data.get("course"), warnings)
    assignments = _normalize_assignments(data.get("assignments"), warnings)

    return {"course": course, "assignments": assignments, "warnings": warnings}


def _normalize_course(course: Any, warnings: list[str]) -> dict[str, str]:
    if not isinstance(course, dict):
        course = {}
    term_start = str(course.get("term_start") or "")
    if term_start and not _ISO_DATE_RE.match(term_start):
        warnings.append(f"Invalid term_start '{term_start}' — expected YYYY-MM-DD, cleared.")
        term_start = ""
    return {
        "code": str(course.get("code") or ""),
        "name": str(course.get("name") or ""),
        "instructor": str(course.get("instructor") or ""),
        "term": str(course.get("term") or ""),
        "term_start": term_start,
    }


def _normalize_recurrence(rec: Any, row_name: str, warnings: list[str]) -> dict | None:
    """Return a clean recurrence dict, or None if absent/invalid.

    Drops the whole object on any validation failure and appends a warning that
    names the assignment row + which field was bad.
    """
    if rec is None:
        return None
    if not isinstance(rec, dict):
        warnings.append(f"'{row_name}': recurrence is not an object, dropped.")
        return None

    kind = str(rec.get("kind") or "").strip().lower()
    if kind not in ALLOWED_RECURRENCE_KINDS:
        warnings.append(f"'{row_name}': unknown recurrence kind '{kind}', dropped.")
        return None

    count = rec.get("count")
    if not isinstance(count, int) or count < 1 or count > 52:
        warnings.append(f"'{row_name}': recurrence count must be 1..52, got {count!r}, dropped.")
        return None

    weekday = str(rec.get("anchor_weekday") or "").strip().title()
    if weekday not in ALLOWED_WEEKDAYS:
        warnings.append(f"'{row_name}': unknown anchor_weekday '{weekday}', dropped.")
        return None

    first_week = rec.get("first_week", 1)
    if not isinstance(first_week, int) or first_week < 1:
        first_week = 1

    skip = rec.get("skip_weeks") or []
    if not isinstance(skip, list) or not all(isinstance(w, int) for w in skip):
        skip = []

    return {
        "kind": kind,
        "count": count,
        "anchor_weekday": weekday,
        "first_week": first_week,
        "skip_weeks": skip,
    }


def _normalize_assignments(rows: Any, warnings: list[str]) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        return []
    out: list[dict[str, Any]] = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            warnings.append(f"Row {i}: not a JSON object, dropped.")
            continue
        name = str(row.get("name") or "").strip()
        if not name:
            warnings.append(f"Row {i}: missing name, dropped.")
            continue
        raw_type = str(row.get("type") or "homework").strip().lower()
        if raw_type not in ALLOWED_TYPES:
            warnings.append(
                f"Row {i} ('{name}'): unknown type '{raw_type}', coerced to 'homework'."
            )
            raw_type = "homework"
        recurrence = _normalize_recurrence(row.get("recurrence"), name, warnings)
        out.append({
            "name": name,
            "type": raw_type,
            "due": str(row.get("due") or ""),
            "prompt": str(row.get("prompt") or ""),
            "recurrence": recurrence,
        })
    return out


def run(input: dict) -> dict:
    """Standard skill contract wrapper.

    Delegates to ``parse_extraction``. The orchestrator's
    ``syllabus_importer`` service calls ``parse_extraction`` directly; this
    wrapper exists so adopters and harnesses invoking skills through the
    standard ``run(input) -> dict`` contract get the same behavior.

    :param input: dict with key ``llm_output`` (str) — the raw LLM response.
    :return: dict ``{course, assignments, warnings}``.
    :raises ParseError: if ``llm_output`` is not valid JSON.
    :raises ValueError: if ``input`` shape is wrong.
    """
    if not isinstance(input, dict):
        raise ValueError("input must be a dict")
    llm_output = input.get("llm_output")
    if not isinstance(llm_output, str):
        raise ValueError("input['llm_output'] must be a string")
    return parse_extraction(llm_output)
