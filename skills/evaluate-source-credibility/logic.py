# logic.py — evaluate-source-credibility
# Walks through four credibility dimensions (venue, method fit,
# limitations, verdict) and tracks which have been addressed so far.

DIMENSIONS = ["venue", "method", "limitations", "verdict"]

def run(input):
  """
  :param input: {
    "addressed": dict[str, bool] | None,  # which dimensions are complete
    "latest_dimension": str | None,       # the one just answered, if any
  }
  :return: {"next_dimension": str | None, "ready_for_verdict": bool}
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

  # LLM stub: deciding whether a free-text answer *addressed* a dimension
  # is a semantic call the tutor should make; this module only tracks flags.
  return {"next_dimension": nxt, "ready_for_verdict": ready, "observations": observations}
