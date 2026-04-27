"""Run a skill against a student artifact and append the result to that
student's knowledge file.

Two modes:

  Scripted (reproducible demo from a YAML scenario):
    python demos/run_skill.py --scenario demos/scenarios/01-rdc8-argument-decomposition.yaml

  Conversational (called mid-conversation, e.g. by the tutor):
    python demos/run_skill.py \\
      --skill cohesion-strengthening \\
      --student bryan \\
      --source students/bryan/submissions/AIMEMO9-2.md \\
      --assignment ai_memos \\
      --input '{"text_before": "...", "text_after": "...", "student_relationship": "contrast"}' \\
      --notes "After Bryan named the relationship as contrast"

Both modes share the same internals: load the skill's logic.py, call run(),
and append a knowledge-file entry whose centerpiece is the skill's
'observations' list.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
STUDENTS_DIR = REPO_ROOT / "students"


def load_skill_run(skill_id: str):
    logic_path = SKILLS_DIR / skill_id / "logic.py"
    if not logic_path.exists():
        raise FileNotFoundError(f"No logic.py for skill '{skill_id}' at {logic_path}")
    spec = importlib.util.spec_from_file_location(f"skills.{skill_id}.logic", logic_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "run"):
        raise AttributeError(f"Skill '{skill_id}' logic.py has no run() function")
    return module.run


def render_entry(scenario: dict, output: dict) -> str:
    observations = output.get("observations", []) or []
    raw = {k: v for k, v in output.items() if k != "observations"}

    header_extras = []
    if scenario.get("source"):
        header_extras.append(f"`{scenario['source']}`")
    if scenario.get("assignment"):
        header_extras.append(scenario["assignment"])
    header_suffix = f" — {' · '.join(header_extras)}" if header_extras else ""

    lines = [
        f"## {date.today().isoformat()} · {scenario['skill']}{header_suffix}",
        "",
    ]
    if observations:
        for obs in observations:
            lines.append(f"- {obs}")
    else:
        lines.append("_(no observations returned)_")

    if scenario.get("notes"):
        lines += ["", f"**Context:** {scenario['notes'].strip()}"]

    lines += [
        "",
        "<details><summary>raw diagnostic</summary>",
        "",
        "```json",
        json.dumps(raw, indent=2, default=str),
        "```",
        "",
        "</details>",
        "",
        "---",
        "",
    ]
    return "\n".join(lines)


def append_to_knowledge(student: str, entry: str) -> Path:
    knowledge_path = STUDENTS_DIR / student / "student_knowledge.md"
    if not knowledge_path.exists():
        raise FileNotFoundError(f"No knowledge file for student '{student}' at {knowledge_path}")
    with knowledge_path.open("a", encoding="utf-8") as f:
        f.write("\n" + entry)
    return knowledge_path


def load_scenario(scenario_path: Path) -> dict:
    with scenario_path.open() as f:
        scenario = yaml.safe_load(f)
    if not isinstance(scenario, dict) or "skill" not in scenario or "student" not in scenario or "input" not in scenario:
        raise ValueError(f"Scenario must define 'skill', 'student', and 'input': {scenario_path}")
    return scenario


def build_scenario_from_args(args: argparse.Namespace) -> dict:
    try:
        input_dict = json.loads(args.input)
    except json.JSONDecodeError as e:
        raise SystemExit(f"--input must be valid JSON: {e}")
    if not isinstance(input_dict, dict):
        raise SystemExit("--input must be a JSON object")
    scenario = {
        "skill": args.skill,
        "student": args.student,
        "input": input_dict,
    }
    if args.source:
        scenario["source"] = args.source
    if args.assignment:
        scenario["assignment"] = args.assignment
    if args.notes:
        scenario["notes"] = args.notes
    return scenario


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scenario", type=Path, help="Path to a scenario YAML")
    parser.add_argument("--skill", help="Skill id (folder under skills/)")
    parser.add_argument("--student", help="Student id (folder under students/)")
    parser.add_argument("--source", help="Path to the artifact the skill is examining")
    parser.add_argument("--assignment", help="Assignment type (e.g. ai_memos)")
    parser.add_argument("--input", help="JSON object passed to the skill's run()")
    parser.add_argument("--notes", help="Free-text context for the knowledge entry")
    args = parser.parse_args(argv)

    if args.scenario:
        scenario = load_scenario(args.scenario.resolve())
    else:
        missing = [a for a in ("skill", "student", "input") if not getattr(args, a)]
        if missing:
            parser.error(f"In conversational mode, --{', --'.join(missing)} is required (or use --scenario)")
        scenario = build_scenario_from_args(args)

    run = load_skill_run(scenario["skill"])
    output = run(scenario["input"])

    print(f"Skill:   {scenario['skill']}")
    print(f"Student: {scenario['student']}")
    print("Observations:")
    for obs in output.get("observations", []) or ["(none)"]:
        print(f"  - {obs}")

    entry = render_entry(scenario, output)
    knowledge_path = append_to_knowledge(scenario["student"], entry)
    print(f"\nAppended to {knowledge_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
