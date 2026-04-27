# logic.py — compare-two-readings
# Detects whether a student's comparison is at the surface (topic-only)
# or engages a specific dimension (method, sample, finding, scope).

DIMENSION_CUES = {
  "method": ("method", "design", "experiment", "survey", "case study", "data"),
  "sample": ("sample", "participants", "respondents", "cases", "population"),
  "finding": ("find", "found", "result", "conclude", "concludes", "show"),
  "scope": ("scope", "generalize", "context", "setting", "country", "field"),
}

def run(input):
  """
  :param input: {"student_comparison": str}
  :return: {"dimension": str | None, "is_surface": bool, "hits": dict[str, int]}
  """
  text = input.get("student_comparison", "").lower()
  hits = {dim: sum(cue in text for cue in cues) for dim, cues in DIMENSION_CUES.items()}
  best = max(hits, key=hits.get) if any(hits.values()) else None
  # Surface = no dimension cue AND short answer.
  is_surface = best is None and len(text.split()) < 25
  observations = []
  if best:
    observations.append(f"Comparison engages the '{best}' dimension (cue hits: {hits[best]}).")
  else:
    observations.append("Comparison did not surface a specific dimension (method/sample/finding/scope).")
  if is_surface:
    observations.append("Response reads as surface-level — short and topic-only, no dimensional handle.")
  secondaries = [d for d, n in hits.items() if n > 0 and d != best]
  if secondaries:
    observations.append(f"Secondary dimensions touched: {', '.join(secondaries)}.")

  # LLM stub: catches dimension language the cue lists miss (paraphrases).
  return {"dimension": best, "is_surface": is_surface, "hits": hits, "observations": observations}
