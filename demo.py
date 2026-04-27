# demo.py — Conversational argument-decomposition tutor.
#
# Walks the student through Gilbert's argument (from RDC8) one turn at a
# time. After every answer we re-run skills/argument-decomposition/logic.py
# against the accumulated state, print the diagnostic, and pick the next
# question based on the gaps the heuristic flags.
#
# Run inside Claude Code (or any terminal):
#     python demo.py
#
# The tutor's questions are drawn from skills/argument-decomposition/
# skills.md (Steps 1-6). The heuristic in logic.py is the "what does the
# student understand right now" model — every answer updates it.

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILLS_DIR = ROOT / "skills"


def load_skill(skill_id):
    path = SKILLS_DIR / skill_id / "logic.py"
    spec = importlib.util.spec_from_file_location(f"{skill_id}.logic", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run


def tutor(text):
    print(f"\n[tutor] {text}")


def ask(prompt="[you]   "):
    try:
        return input(prompt).strip()
    except EOFError:
        return ""


def diagnostic(result):
    print("\n  · what the heuristic sees right now ·")
    for k, v in result.items():
        print(f"    {k}: {v}")


def collect_lines(prompt, sentinel=""):
    items = []
    while True:
        line = ask(prompt)
        if line == sentinel:
            break
        items.append(line)
    return items


def converse():
    run = load_skill("argument-decomposition")
    state = {
        "student_summary": "",
        "sub_claims": [],
        "evidence_pairings": {},
        "structure_label": None,
    }

    tutor(
        "We're going to decompose Gilbert's argument from your RDC8 — "
        "the kidnapping-as-taxation paper on Colombia. In your own "
        "words, what is Gilbert arguing? One sentence."
    )
    state["student_summary"] = ask()
    if not state["student_summary"]:
        tutor("Nothing to work with. Come back when you have a summary.")
        return
    result = run(state)
    diagnostic(result)

    # Step 2/3 — pull sub-claims out of the summary.
    if result["is_flat_summary"]:
        tutor(
            "That reads as one bundled claim. For your summary to hold, "
            "what smaller claims would Gilbert also have to make? List "
            "them one per line, blank line to stop."
        )
    else:
        tutor(
            "Your summary already implies some structure. Name the "
            "smaller claims you see in it, one per line — blank line "
            "to stop."
        )
    state["sub_claims"] = collect_lines("[claim] ")
    if not state["sub_claims"]:
        tutor("No sub-claims yet — nothing more to evaluate. Re-run when ready.")
        return
    result = run(state)
    diagnostic(result)

    # Step 4 — pair evidence to each sub-claim.
    tutor(
        "For each sub-claim, what evidence does Gilbert use? Paraphrase "
        "is fine — interview quotes, kidnapping counts, the Chiquita "
        "case, etc. I'll ask one at a time."
    )
    for claim in state["sub_claims"]:
        print(f"\n  sub-claim: {claim}")
        state["evidence_pairings"][claim] = ask("[evidence] ")
    result = run(state)
    diagnostic(result)

    if result["claims_without_evidence"]:
        tutor(
            "These sub-claims don't have an obvious evidence cue in what "
            "you wrote (data / study / case / shows / finds / …):"
        )
        for c in result["claims_without_evidence"]:
            print(f"    - {c}")
        tutor(
            "Is that because (a) Gilbert asserts it without proof, "
            "(b) you missed where she cites it, or (c) the evidence is "
            "real but you described it without a citation cue?"
        )
        ask()  # capture the reflection; we don't branch on it here

    # Step 5 — name the connective shape.
    tutor(
        "Last move. How do these sub-claims connect? "
        "'chain' = A leads to B leads to C. "
        "'parallel' = A, B, C are independent supports for the conclusion."
    )
    label = ask("[chain/parallel/skip] ").lower()
    if label in ("chain", "parallel"):
        state["structure_label"] = label
        result = run(state)
        diagnostic(result)
        if not result["structure_matches_language"]:
            tutor(
                f"You named the structure '{label}', but the language in "
                f"your evidence pairings doesn't reflect that pattern. "
                f"Re-read what you wrote — which words would signal "
                f"'{label}' to a reader?"
            )
            ask()

    # Step 6 — wrap up: show the full argument map and final heuristic.
    tutor("Decomposition complete. Here's the argument map you built:")
    print(json.dumps(state, indent=2))
    tutor("Final heuristic snapshot:")
    print(json.dumps(run(state), indent=2))
    tutor(
        "Next moves from skills.md: try `reading-comprehension-check` to "
        "stress-test each piece, or `compare-two-readings` if you need to "
        "relate Gilbert to another text."
    )


if __name__ == "__main__":
    converse()
