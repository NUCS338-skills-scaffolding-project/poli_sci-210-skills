# logic.py — operationalization-check
# Granular skill in Phase 2 (extract-research-design). Tracks whether the
# student has identified at least one concept whose operationalization has a
# substantive includes/excludes gap with a defended severity. Pure function;
# no side effects.

VALID_METHODS = (
  "theory-data",
  "inference",
  "surveys",
  "experiments",
  "large-n",
  "small-n",
  "machine-learning",
)

VALID_SEVERITY = ("minor", "moderate", "load-bearing")
MIN_FIELD_WORDS = 4
MIN_CONCEPTS = 1
JUDGMENT_CUES = ("this measure is wrong", "this is bad", "they messed up", "this is a mistake")


def _entry_complete(entry):
  if not isinstance(entry, dict):
    return False
  for f in ("concept", "operationalization", "includes_but_shouldnt", "excludes_but_should"):
    v = (entry.get(f) or "").strip()
    if len(v.split()) < MIN_FIELD_WORDS:
      return False
  sev = (entry.get("severity") or "").strip().lower()
  if sev not in VALID_SEVERITY:
    return False
  return True


def _has_judgment_language(entry):
  blob = " ".join([
    (entry.get("operationalization") or ""),
    (entry.get("includes_but_shouldnt") or ""),
    (entry.get("excludes_but_should") or ""),
  ]).lower()
  return any(c in blob for c in JUDGMENT_CUES)


def run(input):
  """
  :param input: {
    "week": int,
    "method": str,
    "article_path": str,
    "prior_session_logs": list[str] | None,
    "prior_in_phase_scratchpads": dict[str, str] | None,
    "concepts": list[{
      "concept": str,
      "operationalization": str,
      "includes_but_shouldnt": str,
      "excludes_but_should": str,
      "severity": str,                    # "minor" | "moderate" | "load-bearing"
      "claim_movement": str | None,       # required if severity == "load-bearing"
    }] | None,
  }
  :return: {
    "complete_count": int,
    "incomplete_count": int,
    "load_bearing_undefended": list[int],
    "judgment_flagged": list[int],
    "next_prompt": str,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  if not isinstance(input, dict):
    raise ValueError("input must be a dict")

  method = input.get("method")
  if method not in VALID_METHODS:
    raise ValueError(f"method={method!r} must be one of {VALID_METHODS}")

  concepts = input.get("concepts") or []
  if not isinstance(concepts, list):
    raise ValueError("concepts must be a list")

  complete = [c for c in concepts if _entry_complete(c)]
  incomplete = [c for c in concepts if not _entry_complete(c)]

  load_bearing_undefended = []
  for i, c in enumerate(concepts):
    sev = (c.get("severity") or "").strip().lower()
    if sev == "load-bearing":
      cm = (c.get("claim_movement") or "").strip()
      if len(cm.split()) < MIN_FIELD_WORDS:
        load_bearing_undefended.append(i)

  judgment_flagged = [i for i, c in enumerate(concepts) if _has_judgment_language(c)]

  only_minor = (
    len(complete) == 1
    and (complete[0].get("severity") or "").strip().lower() == "minor"
    and len(incomplete) == 0
  )

  if len(complete) == 0 and len(incomplete) == 0:
    next_prompt = "ask_first_concept"
  elif len(incomplete) > 0:
    last = incomplete[-1]
    if not (last.get("concept") or "").strip():
      next_prompt = "ask_concept"
    elif not (last.get("operationalization") or "").strip():
      next_prompt = "ask_operationalization"
    elif not (last.get("includes_but_shouldnt") or "").strip():
      next_prompt = "ask_includes"
    elif not (last.get("excludes_but_should") or "").strip():
      next_prompt = "ask_excludes"
    else:
      next_prompt = "ask_severity"
  elif load_bearing_undefended:
    next_prompt = "defend_load_bearing"
  elif only_minor:
    next_prompt = "ask_second_concept"
  else:
    next_prompt = "reconcile_and_exit"

  done = (
    len(complete) >= MIN_CONCEPTS
    and not load_bearing_undefended
    and not only_minor
  )

  done_reasons = []
  if len(complete) >= MIN_CONCEPTS:
    done_reasons.append(f"{len(complete)} fully-filled concept(s) logged")
  if not load_bearing_undefended:
    done_reasons.append("no undefended 'load-bearing' severity claims")
  if not only_minor:
    done_reasons.append("not gated by single-minor-only state")

  observations = [
    f"Method: {method}.",
    f"Complete entries: {len(complete)} (min {MIN_CONCEPTS}).",
    f"Incomplete entries: {len(incomplete)}.",
  ]
  if load_bearing_undefended:
    observations.append(
      f"'load-bearing' severity at indices {load_bearing_undefended} lacks claim_movement defense."
    )
  if only_minor:
    observations.append(
      "Only one concept logged and severity is 'minor' — push for a second concept."
    )
  if judgment_flagged:
    observations.append(
      f"Judgment-shaped language detected at indices {judgment_flagged} — redirect: park for Phase 3."
    )
  observations.append(f"Next tutor move: {next_prompt}.")

  # LLM stub: a semantic check would verify includes/excludes are actually
  # symmetric (catching cases where excludes is just a paraphrase of includes
  # in negation), and would test whether claim_movement actually traces a
  # plausible path from gap to inferential consequence.
  return {
    "complete_count": len(complete),
    "incomplete_count": len(incomplete),
    "load_bearing_undefended": load_bearing_undefended,
    "judgment_flagged": judgment_flagged,
    "next_prompt": next_prompt,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
