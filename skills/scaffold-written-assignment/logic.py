# logic.py — scaffold-written-assignment
# Tracks progress through the four sections of the POLI SCI 210 research
# design critique and flags whether the student's plan for the current
# section is thin.

SECTIONS = [
  "question and relevance",
  "research design",
  "critique (main point + evidence)",
  "what they'd change",
]

COMMIT_CUES = ("i will", "i plan to", "my point", "my argument", "i'd argue", "i want to")

def run(input):
  """
  :param input: {"current_section": int, "student_plan": str}
  :return: {
    "section_name": str,
    "plan_is_thin": bool,
    "next_section": int | None,
  }
  """
  idx = max(0, min(input.get("current_section", 0), len(SECTIONS) - 1))
  plan = input.get("student_plan", "")
  # Thin = short AND without committal language.
  is_thin = len(plan.split()) < 12 and not any(c in plan.lower() for c in COMMIT_CUES)
  nxt = idx + 1 if idx + 1 < len(SECTIONS) else None
  # LLM stub: semantic check catches a substantive plan phrased unusually.
  return {"section_name": SECTIONS[idx], "plan_is_thin": is_thin, "next_section": nxt}
