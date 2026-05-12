# logic.py — ai-explain
# Tracks the follow-up count for the AI memo's interaction phase.
# `done` becomes true at the rubric minimum (5) — that's a *prompt to wrap*,
# not a forced exit. The tutor confirms with the student before closing.

MIN_FOLLOWUPS = 5


INPUT_SCHEMA: dict = {
    "followup_count": "int",
    "student_signaled_done": "bool | None",
    "transcript_path": "str | None",
}


def run(input):
  """
  :param input: {
    "followup_count": int,                  # number of student follow-ups so far
    "student_signaled_done": bool | None,   # student said "stop" / "good"
    "transcript_path": str | None,          # informational; the tutor writes the file
  }
  :return: {
    "followup_count": int,
    "min_required": int,
    "remaining": int,                       # max(0, min - count)
    "wrap_up_eligible": bool,               # count >= min — tutor may propose ending
    "done": bool,                           # wrap_up_eligible AND student_signaled_done
    "rubric_met": bool,                     # whether the 5+ requirement was satisfied
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  if not isinstance(input, dict):
    raise ValueError("input must be a dict")

  raw_count = input.get("followup_count", 0)
  if not isinstance(raw_count, int) or raw_count < 0:
    raise ValueError("followup_count must be a non-negative int")
  count = raw_count

  signaled = bool(input.get("student_signaled_done"))

  remaining = max(0, MIN_FOLLOWUPS - count)
  wrap_up_eligible = count >= MIN_FOLLOWUPS
  rubric_met = wrap_up_eligible
  done = wrap_up_eligible and signaled

  done_reasons = []
  observations = []

  if wrap_up_eligible:
    done_reasons.append(f"follow-up count {count} meets rubric minimum of {MIN_FOLLOWUPS}")
  else:
    observations.append(
      f"Follow-up count {count}/{MIN_FOLLOWUPS}; {remaining} more needed for rubric."
    )

  if signaled and not wrap_up_eligible:
    observations.append(
      "Student signaled stop before reaching 5 follow-ups — rubric requirement not met. "
      "Flag this for the orchestrator's session log."
    )

  if signaled and wrap_up_eligible:
    done_reasons.append("student confirmed end of interaction")

  if not signaled and wrap_up_eligible:
    observations.append("Wrap-up eligible — propose ending and wait for student confirmation.")

  return {
    "followup_count": count,
    "min_required": MIN_FOLLOWUPS,
    "remaining": remaining,
    "wrap_up_eligible": wrap_up_eligible,
    "done": done,
    "rubric_met": rubric_met,
    "done_reasons": done_reasons,
    "observations": observations,
  }
