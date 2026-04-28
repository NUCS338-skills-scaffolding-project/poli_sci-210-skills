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
  :param input: {
    "current_section": int,
    "student_plan": str,
    "tutor_pre_read": {                  # tutor's silent outline (optional)
      "sections": list[{
        "name": str,
        "main_point": str,               # one sentence
      }] | None,
    } | None,
  }
  :return: {
    "section_name": str,
    "plan_is_thin": bool,
    "next_section": int | None,
    "divergence": {                      # student vs. tutor_pre_read, if pre-read provided
      "section_count_delta": int,        # canonical 4 sections - pre-read sections (if specified)
    } | None,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  idx = max(0, min(input.get("current_section", 0), len(SECTIONS) - 1))
  plan = input.get("student_plan", "")
  pre_read = input.get("tutor_pre_read") or None

  # Thin = short AND without committal language.
  is_thin = len(plan.split()) < 12 and not any(c in plan.lower() for c in COMMIT_CUES)
  nxt = idx + 1 if idx + 1 < len(SECTIONS) else None

  divergence = None
  if pre_read:
    pre_sections = pre_read.get("sections") or []
    divergence = {
      "section_count_delta": len(SECTIONS) - len(pre_sections),
    }

  observations = [f"Working on section: '{SECTIONS[idx]}'."]
  if is_thin:
    observations.append("Current plan reads as thin — short and lacks committal language ('I will', 'my point', etc.).")
  else:
    observations.append("Current plan reads as substantive — has length and/or commitment language.")
  if nxt is not None:
    observations.append(f"Next section after this: '{SECTIONS[nxt]}'.")
  else:
    observations.append("This is the last section — no next section.")

  done_reasons = []
  if not is_thin:
    done_reasons.append("current section plan is substantive")
  if nxt is None:
    done_reasons.append("on the final section")
  done = (not is_thin) and (nxt is None)

  # LLM stub: semantic check catches a substantive plan phrased unusually,
  # and could reconcile each section's plan against tutor_pre_read.
  return {
    "section_name": SECTIONS[idx],
    "plan_is_thin": is_thin,
    "next_section": nxt,
    "divergence": divergence,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
