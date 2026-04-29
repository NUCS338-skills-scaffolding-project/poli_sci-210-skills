# logic.py — scope-conditions-check
# Granular skill in Phase 3 (form-critique). Tracks whether the student has
# named at least 2 scope conditions where the headline claim plausibly does
# not extend, across at least 2 different categories. Pure function; no side
# effects.

VALID_METHODS = (
  "theory-data",
  "inference",
  "surveys",
  "experiments",
  "large-n",
  "small-n",
  "machine-learning",
)

VALID_CATEGORIES = ("population", "temporal", "contextual", "manipulation", "outcome")
MIN_CONDITIONS = 2
TARGET_CONDITIONS = 3
MIN_TIE_WORDS = 4
MIN_WHY_WORDS = 6


def _entry_complete(entry):
  if not isinstance(entry, dict):
    return False
  category = (entry.get("category") or "").strip().lower()
  design_tie = (entry.get("design_tie") or "").strip()
  why_it_fails = (entry.get("why_it_fails") or "").strip()
  if category not in VALID_CATEGORIES:
    return False
  if len(design_tie.split()) < MIN_TIE_WORDS:
    return False
  if len(why_it_fails.split()) < MIN_WHY_WORDS:
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
    "scope_conditions": list[{
      "category": str,                  # one of VALID_CATEGORIES
      "design_tie": str,                # specific design element
      "why_it_fails": str,              # one-sentence mechanism
      "paper_acknowledges": bool | None,
    }] | None,
  }
  :return: {
    "complete_count": int,
    "incomplete_count": int,
    "categories_represented": list[str],
    "all_one_category": bool,
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

  conditions = input.get("scope_conditions") or []
  if not isinstance(conditions, list):
    raise ValueError("scope_conditions must be a list")

  complete = [c for c in conditions if _entry_complete(c)]
  incomplete = [c for c in conditions if not _entry_complete(c)]
  categories = [(c.get("category") or "").strip().lower() for c in complete]
  unique_categories = sorted(set(categories))

  all_one_category = (
    len(complete) >= 2
    and len(set(categories)) == 1
  )

  if len(complete) == 0 and len(incomplete) == 0:
    next_prompt = "show_categories_and_ask_first"
  elif len(incomplete) > 0:
    last = incomplete[-1]
    if (last.get("category") or "").strip().lower() not in VALID_CATEGORIES:
      next_prompt = "ask_category"
    elif len((last.get("design_tie") or "").split()) < MIN_TIE_WORDS:
      next_prompt = "ask_design_tie"
    else:
      next_prompt = "ask_why_it_fails"
  elif len(complete) < MIN_CONDITIONS:
    next_prompt = "ask_next_condition"
  elif all_one_category:
    next_prompt = "push_different_category"
  elif len(complete) < TARGET_CONDITIONS:
    next_prompt = "offer_third_condition"
  else:
    next_prompt = "reconcile_and_exit"

  done = (
    len(complete) >= MIN_CONDITIONS
    and not all_one_category
  )

  done_reasons = []
  if len(complete) >= MIN_CONDITIONS:
    done_reasons.append(f"{len(complete)} substantive scope condition(s) logged")
  if not all_one_category:
    done_reasons.append("scope conditions span more than one category")

  observations = [
    f"Method: {method}.",
    f"Complete entries: {len(complete)} (need {MIN_CONDITIONS}, target {TARGET_CONDITIONS}).",
    f"Incomplete entries: {len(incomplete)}.",
    f"Categories represented: {unique_categories or 'none'}.",
  ]
  if all_one_category:
    observations.append(
      f"All conditions in category '{categories[0]}' — push the student to a different category."
    )
  observations.append(f"Next tutor move: {next_prompt}.")

  # LLM stub: a semantic check would catch within-sample inference threats
  # mislabeled as scope conditions, would detect when paper_acknowledges is
  # mis-claimed, and would test that why_it_fails actually traces a mechanism
  # rather than restating "it might not generalize."
  return {
    "complete_count": len(complete),
    "incomplete_count": len(incomplete),
    "categories_represented": unique_categories,
    "all_one_category": all_one_category,
    "next_prompt": next_prompt,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
