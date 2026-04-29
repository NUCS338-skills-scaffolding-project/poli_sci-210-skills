# logic.py — inference-threat-spotting
# Granular skill in Phase 3 (form-critique). Tracks whether the student has
# named at least one inference threat with a specific design tie, a non-minor
# severity, and a defensible claim_movement. Pure function; no side effects.

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
MIN_DESIGN_TIE_WORDS = 5
MIN_CLAIM_MOVEMENT_WORDS = 6
GENERIC_TIE_CUES = ("the methodology", "their methods", "the design generally", "the paper")


def _entry_complete(entry):
  if not isinstance(entry, dict):
    return False
  threat = (entry.get("threat") or "").strip()
  design_tie = (entry.get("design_tie") or "").strip()
  severity = (entry.get("severity") or "").strip().lower()
  claim_movement = (entry.get("claim_movement") or "").strip()
  if not threat:
    return False
  if len(design_tie.split()) < MIN_DESIGN_TIE_WORDS:
    return False
  if severity not in VALID_SEVERITY:
    return False
  if len(claim_movement.split()) < MIN_CLAIM_MOVEMENT_WORDS:
    return False
  return True


def _design_tie_is_generic(value):
  v_low = (value or "").strip().lower()
  return any(c in v_low for c in GENERIC_TIE_CUES) and len(v_low.split()) <= 6


def _has_substantive_non_minor(threats):
  """At least one fully-filled threat with severity moderate or load-bearing."""
  for c in threats:
    if not _entry_complete(c):
      continue
    sev = (c.get("severity") or "").strip().lower()
    if sev in ("moderate", "load-bearing") and not _design_tie_is_generic(c.get("design_tie")):
      return True
  return False


def run(input):
  """
  :param input: {
    "week": int,
    "method": str,
    "article_path": str,
    "prior_session_logs": list[str] | None,         # Phase 1 + Phase 2 logs
    "prior_in_phase_scratchpads": dict[str, str] | None,
    "threats": list[{
      "threat": str,                                # name from method catalog
      "design_tie": str,                            # specific design element from Phase 2
      "severity": str,                              # "minor" | "moderate" | "load-bearing"
      "claim_movement": str,                        # how the headline claim moves
      "paper_self_addressed": bool | None,          # whether the paper already addresses it
    }] | None,
  }
  :return: {
    "complete_count": int,
    "incomplete_count": int,
    "minor_only": bool,                             # all complete entries are minor
    "generic_tie_indices": list[int],
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

  threats = input.get("threats") or []
  if not isinstance(threats, list):
    raise ValueError("threats must be a list")

  complete = [c for c in threats if _entry_complete(c)]
  incomplete = [c for c in threats if not _entry_complete(c)]
  generic_tie_indices = [
    i for i, c in enumerate(threats) if _design_tie_is_generic(c.get("design_tie"))
  ]

  minor_only = (
    len(complete) >= 1
    and all((c.get("severity") or "").strip().lower() == "minor" for c in complete)
  )

  has_strong = _has_substantive_non_minor(threats)

  if len(complete) == 0 and len(incomplete) == 0:
    next_prompt = "show_catalog_and_ask_first"
  elif len(incomplete) > 0:
    last = incomplete[-1]
    if not (last.get("threat") or "").strip():
      next_prompt = "ask_threat"
    elif len((last.get("design_tie") or "").split()) < MIN_DESIGN_TIE_WORDS:
      next_prompt = "ask_design_tie"
    elif (last.get("severity") or "").strip().lower() not in VALID_SEVERITY:
      next_prompt = "ask_severity"
    else:
      next_prompt = "ask_claim_movement"
  elif minor_only:
    next_prompt = "push_for_stronger_threat"
  elif not has_strong:
    next_prompt = "push_for_substantive_threat"
  else:
    next_prompt = "reconcile_and_exit"

  done = has_strong and not minor_only

  done_reasons = []
  if has_strong:
    done_reasons.append("at least one threat with severity ≥ moderate is fully filled")
  if not minor_only:
    done_reasons.append("not gated by minor-only state")
  if has_strong and not generic_tie_indices:
    done_reasons.append("no threat tie is generic")

  observations = [
    f"Method: {method}.",
    f"Complete entries: {len(complete)}.",
    f"Incomplete entries: {len(incomplete)}.",
  ]
  if generic_tie_indices:
    observations.append(
      f"Generic design ties detected at indices {generic_tie_indices} — push for a specific Phase 2 design field."
    )
  if minor_only:
    observations.append("All complete entries are severity=minor — push for a stronger threat.")
  observations.append(f"Next tutor move: {next_prompt}.")

  # LLM stub: a semantic check would verify the claim_movement actually
  # traces a plausible mechanism from the threat to a movement in the
  # headline claim, and would catch threats picked from the wrong method
  # catalog (e.g., classic confounding in a documented RCT).
  return {
    "complete_count": len(complete),
    "incomplete_count": len(incomplete),
    "minor_only": minor_only,
    "generic_tie_indices": generic_tie_indices,
    "next_prompt": next_prompt,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
