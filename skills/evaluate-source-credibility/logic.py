# logic.py — evaluate-source-credibility
# Walks through four credibility dimensions (venue, method fit,
# limitations, verdict) and tracks which have been addressed so far.

DIMENSIONS = ["venue", "method", "limitations", "verdict"]

def run(input):
  """
  :param input: {
    "addressed": dict[str, bool] | None,  # which dimensions are complete
    "latest_dimension": str | None,       # the one just answered, if any
    "tutor_pre_read": {                   # tutor's silent canonical read (optional)
      "authorship": str | None,
      "methodology_fit": str | None,
      "limitations": str | None,
      "verdict": str | None,
    } | None,
  }
  :return: {
    "next_dimension": str | None,
    "ready_for_verdict": bool,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  Note: divergence is not computed here — comparing free-text verdicts is a
  semantic judgment best left to the tutor LLM.
  """
  addressed = dict(input.get("addressed") or {})
  latest = input.get("latest_dimension")
  if latest in DIMENSIONS:
    addressed[latest] = True

  remaining = [d for d in DIMENSIONS if not addressed.get(d)]
  ready = not remaining or remaining == ["verdict"]
  nxt = remaining[0] if remaining else None

  done_count = sum(1 for d in DIMENSIONS if addressed.get(d))
  observations = [f"Addressed {done_count}/{len(DIMENSIONS)} credibility dimension(s)."]
  if latest in DIMENSIONS:
    observations.append(f"Just addressed: {latest}.")
  if nxt:
    observations.append(f"Next dimension to address: {nxt}.")
  if ready and nxt is None:
    observations.append("All four dimensions covered — verdict step complete.")
  elif ready:
    observations.append("Three substantive dimensions covered — verdict step is unlocked.")

  all_addressed = all(addressed.get(d) for d in DIMENSIONS)
  done_reasons = []
  if ready:
    done_reasons.append("ready for verdict")
  if all_addressed:
    done_reasons.append("all four dimensions addressed")
  done = ready and all_addressed

  # LLM stub: deciding whether a free-text answer *addressed* a dimension
  # is a semantic call the tutor should make; this module only tracks flags.
  # The tutor should also reconcile the student's verdict against
  # tutor_pre_read to surface ignored dimensions.
  return {
    "next_dimension": nxt,
    "ready_for_verdict": ready,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
