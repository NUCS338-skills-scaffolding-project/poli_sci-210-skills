#!/usr/bin/env python3
"""check_method_coverage.py

Verifies that every method id listed in metadata.yaml.course_context.research_methods
has matching inline per-method content in each of the RDC skills that ship per-method
prose. Catches drift when an adopter adds a method to metadata but forgets to update
the corresponding sections in skills.md.

The skills below carry per-method content blocks (catalogs, checklists, focus areas,
locus expectations, label translations, or inline probes). If a method id appears in
metadata but is missing from any one of these skill bodies, the catalog is silently
incomplete for that method.

Usage
-----
Run from the repo root:

    python3 scripts/check_method_coverage.py

Exit code 0 if all methods are covered across all listed skills; exit code 1
otherwise. The output lists every (skill, missing_method_id) pair so adopters
can fix in one pass.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent

# Skills that ship per-method prose content. If an adopter changes the method
# list in metadata.yaml.course_context.research_methods, these are the files
# they need to keep in sync.
RDC_PROSE_SKILLS = [
    "alt-designs",
    "author-choices",
    "design-skeleton",
    "first-pass-orient",
    "inference-threats",
    "method-align",
    "op-check",
    "scope-check",
    "trace-evidence",
]


def _extract_method_ids(methods_field) -> list[str]:
    """Accept either a flat string list or list-of-dicts; return id strings."""
    if not isinstance(methods_field, list):
        return []
    out: list[str] = []
    for m in methods_field:
        if isinstance(m, str):
            out.append(m)
        elif isinstance(m, dict) and isinstance(m.get("id"), str):
            out.append(m["id"])
    return out


def main() -> int:
    metadata_path = REPO_ROOT / "metadata.yaml"
    if not metadata_path.is_file():
        print(f"ERROR: {metadata_path} not found", file=sys.stderr)
        return 1

    metadata = yaml.safe_load(metadata_path.read_text()) or {}
    methods_field = (metadata.get("course_context") or {}).get("research_methods") or []
    method_ids = _extract_method_ids(methods_field)

    if not method_ids:
        print(
            "ERROR: metadata.yaml.course_context.research_methods is empty or malformed",
            file=sys.stderr,
        )
        return 1

    failures: list[tuple[str, str]] = []
    missing_skill_files: list[str] = []
    for skill in RDC_PROSE_SKILLS:
        skill_md = REPO_ROOT / "skills" / skill / "skills.md"
        if not skill_md.is_file():
            missing_skill_files.append(str(skill_md))
            continue
        body = skill_md.read_text()
        for method_id in method_ids:
            # The per-method content blocks use the bare id as a header or list
            # marker. Style varies (backticked, headed, etc.); a literal substring
            # check is the broadest, lowest-false-negative gate.
            if method_id not in body:
                failures.append((skill, method_id))

    if missing_skill_files:
        print("ERROR: missing expected skill files:", file=sys.stderr)
        for path in missing_skill_files:
            print(f"  {path}", file=sys.stderr)
        return 1

    if failures:
        print(f"FAIL: {len(failures)} method-coverage gaps detected", file=sys.stderr)
        print("(each row: skill missing per-method content for the given id)", file=sys.stderr)
        for skill, method_id in failures:
            print(f"  {skill}: missing per-method content for '{method_id}'", file=sys.stderr)
        print(
            "\nAn adopter who added a new method to metadata.yaml must also add\n"
            "the corresponding per-method block (catalog entry, checklist item,\n"
            "focus area, locus pattern, or probe) to each skill above before the\n"
            "RDC chain will produce useful output for that method.",
            file=sys.stderr,
        )
        return 1

    print(
        f"OK: all {len(method_ids)} method id(s) appear in all "
        f"{len(RDC_PROSE_SKILLS)} RDC prose skills."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
