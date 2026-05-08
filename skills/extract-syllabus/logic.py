"""extract-syllabus — parser for the LLM's structured response.

Validates and normalizes the JSON returned by the prompt in skills.md.
- Drops malformed assignment rows; appends explanatory strings to `warnings`.
- Coerces unknown `type` values to `homework`.
- Raises ParseError on top-level invalid JSON.
"""
from __future__ import annotations

import json
from typing import Any


ALLOWED_TYPES = {"writing", "code", "quiz", "homework"}


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

    course = _normalize_course(data.get("course"))
    warnings: list[str] = list(data.get("warnings") or [])
    assignments = _normalize_assignments(data.get("assignments"), warnings)

    return {"course": course, "assignments": assignments, "warnings": warnings}


def _normalize_course(course: Any) -> dict[str, str]:
    if not isinstance(course, dict):
        course = {}
    return {
        "code": str(course.get("code") or ""),
        "name": str(course.get("name") or ""),
        "instructor": str(course.get("instructor") or ""),
        "term": str(course.get("term") or ""),
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
        out.append({
            "name": name,
            "type": raw_type,
            "due": str(row.get("due") or ""),
            "prompt": str(row.get("prompt") or ""),
        })
    return out
