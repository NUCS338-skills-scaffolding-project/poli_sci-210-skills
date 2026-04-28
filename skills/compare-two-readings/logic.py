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
  :param input: {
    "student_comparison": str,
    "tutor_pre_read": {                  # tutor's silent canonical comparison (optional)
      "similarities": list[str] | None,  # 2 items
      "differences": list[str] | None,   # 2 items
      "axis": str | None,                # the dimension I'd organize around
    } | None,
  }
  :return: {
    "dimension": str | None,
    "is_surface": bool,
    "hits": dict[str, int],              # per-dimension cue counts
    "total_hits": int,                   # sum across dimensions
    "divergence": {                      # student vs. tutor_pre_read, if pre-read provided
      "axis_diverges": bool,             # student's strongest dimension differs from tutor's axis
    } | None,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  text = input.get("student_comparison", "").lower()
  pre_read = input.get("tutor_pre_read") or None

  hits = {dim: sum(cue in text for cue in cues) for dim, cues in DIMENSION_CUES.items()}
  total_hits = sum(hits.values())
  best = max(hits, key=hits.get) if any(hits.values()) else None
  # Surface = no dimension cue AND short answer.
  is_surface = best is None and len(text.split()) < 25

  divergence = None
  if pre_read:
    pre_axis = (pre_read.get("axis") or "").strip().lower()
    pre_axis_key = next((k for k in DIMENSION_CUES if k in pre_axis), None)
    divergence = {
      "axis_diverges": bool(pre_axis_key) and best is not None and best != pre_axis_key,
    }

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

  done_reasons = []
  if not is_surface:
    done_reasons.append("comparison is not surface-level")
  if total_hits >= 2:
    done_reasons.append(f"comparison touches {total_hits} dimensional cues")
  done = (not is_surface) and total_hits >= 2

  # LLM stub: catches dimension language the cue lists miss (paraphrases),
  # and reconciles the student's axis against tutor_pre_read more deeply.
  return {
    "dimension": best,
    "is_surface": is_surface,
    "hits": hits,
    "total_hits": total_hits,
    "divergence": divergence,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
