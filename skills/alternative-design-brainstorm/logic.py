# logic.py — alternative-design-brainstorm
# Granular skill in Phase 3 (form-critique). Tracks whether the student has
# proposed at least one specific, feasible design change that addresses a
# prior critique with a defensible predicted claim_movement. Pure function;
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

MIN_ALTERNATIVES = 1
TARGET_ALTERNATIVES = 2

MIN_CHANGE_WORDS = 6
MIN_FEASIBILITY_WORDS = 4
MIN_CLAIM_MOVEMENT_WORDS = 6
MIN_TIE_WORDS = 4

GENERIC_CHANGE_CUES = (
  "be more careful",
  "be more rigorous",
  "use better methods",
  "collect more data",
  "use better data",
  "do more research",
  "improve the study",
  "better analysis",
)


def _is_generic_change(value):
  v_low = (value or "").strip().lower()
  if not v_low:
    return True
  return any(c in v_low for c in GENERIC_CHANGE_CUES)


def _entry_complete(entry):
  if not isinstance(entry, dict):
    return False
  change = (entry.get("change") or "").strip()
  addresses = (entry.get("addresses_critique") or "").strip()
  feasibility = (entry.get("feasibility") or "").strip()
  claim_movement = (entry.get("expected_claim_movement") or "").strip()
  if len(change.split()) < MIN_CHANGE_WORDS:
    return False
  if _is_generic_change(change):
    return False
  if len(addresses.split()) < MIN_TIE_WORDS:
    return False
  if len(feasibility.split()) < MIN_FEASIBILITY_WORDS:
    return False
  if len(claim_movement.split()) < MIN_CLAIM_MOVEMENT_WORDS:
    return False
  return True


def run(input):
  """
  :param input: {
    "week": int,
    "method": str,
    "article_path": str,
    "prior_session_logs": list[str] | None,
    "prior_in_phase_scratchpads": dict[str, str] | None,
    "alternatives": list[{
      "change": str,                      # specific design change
      "addresses_critique": str,          # which prior critique it addresses
      "feasibility": str,                 # what would be needed
      "expected_claim_movement": str,     # predicted direction
    }] | None,
  }
  :return: {
    "complete_count": int,
    "incomplete_count": int,
    "generic_change_indices": list[int],
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

  alternatives = input.get("alternatives") or []
  if not isinstance(alternatives, list):
    raise ValueError("alternatives must be a list")

  complete = [a for a in alternatives if _entry_complete(a)]
  incomplete = [a for a in alternatives if not _entry_complete(a)]
  generic_indices = [
    i for i, a in enumerate(alternatives) if _is_generic_change(a.get("change"))
  ]

  if len(complete) == 0 and len(incomplete) == 0:
    next_prompt = "ask_first_alternative"
  elif len(incomplete) > 0:
    last = incomplete[-1]
    if len((last.get("change") or "").split()) < MIN_CHANGE_WORDS or _is_generic_change(last.get("change")):
      next_prompt = "ask_change"
    elif len((last.get("addresses_critique") or "").split()) < MIN_TIE_WORDS:
      next_prompt = "ask_addresses_critique"
    elif len((last.get("feasibility") or "").split()) < MIN_FEASIBILITY_WORDS:
      next_prompt = "ask_feasibility"
    else:
      next_prompt = "ask_claim_movement"
  elif len(complete) < MIN_ALTERNATIVES:
    next_prompt = "ask_next_alternative"
  elif len(complete) < TARGET_ALTERNATIVES:
    next_prompt = "offer_second_alternative"
  else:
    next_prompt = "reconcile_and_exit"

  done = len(complete) >= MIN_ALTERNATIVES

  done_reasons = []
  if len(complete) >= MIN_ALTERNATIVES:
    done_reasons.append(f"{len(complete)} fully-filled, non-generic alternative(s) logged")
  if not generic_indices:
    done_reasons.append("no generic change strings in the list")

  observations = [
    f"Method: {method}.",
    f"Complete entries: {len(complete)} (need {MIN_ALTERNATIVES}, target {TARGET_ALTERNATIVES}).",
    f"Incomplete entries: {len(incomplete)}.",
  ]
  if generic_indices:
    observations.append(
      f"Generic change strings detected at indices {generic_indices} — push for specifics."
    )
  observations.append(f"Next tutor move: {next_prompt}.")

  # LLM stub: a semantic check would verify the change actually addresses the
  # cited critique (rather than being plausible-sounding but unrelated), would
  # judge feasibility against the research question's actual constraints, and
  # would test that expected_claim_movement is a real direction prediction
  # rather than "we'd find out."
  return {
    "complete_count": len(complete),
    "incomplete_count": len(incomplete),
    "generic_change_indices": generic_indices,
    "next_prompt": next_prompt,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
