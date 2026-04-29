# logic.py — probe-author-choices
# Granular skill in Phase 1 (investigate-reading). Tracks whether the student
# has surfaced at least 2 contestable design choices, each with a plausible
# alternative and a one-sentence why-non-trivial. Pure function; no side
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

MIN_CHOICES = 2
TARGET_CHOICES = 3
MIN_REASON_WORDS = 6

JUDGMENT_CUES = ("they should", "they shouldn't", "the right way", "would've been better", "would have been better")


def _entry_complete(entry):
  if not isinstance(entry, dict):
    return False
  choice = (entry.get("choice") or "").strip()
  alt = (entry.get("alternative") or "").strip()
  why = (entry.get("why_non_trivial") or "").strip()
  return bool(choice) and bool(alt) and len(why.split()) >= MIN_REASON_WORDS


def _has_judgment_language(entry):
  blob = " ".join([
    (entry.get("choice") or ""),
    (entry.get("alternative") or ""),
    (entry.get("why_non_trivial") or ""),
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
    "choices": list[{
      "choice": str,                    # what the authors did
      "alternative": str,               # what they could have done
      "why_non_trivial": str,           # one sentence
      "category": str | None,           # optional method-relevant category tag
    }] | None,
  }
  :return: {
    "complete_count": int,
    "incomplete_count": int,
    "judgment_flagged": list[int],      # indices of entries that read as judgments
    "category_clustered": bool,         # all categories the same?
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

  choices = input.get("choices") or []
  if not isinstance(choices, list):
    raise ValueError("choices must be a list")

  complete = [c for c in choices if _entry_complete(c)]
  incomplete = [c for c in choices if not _entry_complete(c)]
  judgment_flagged = [i for i, c in enumerate(choices) if _has_judgment_language(c)]

  categories = [c.get("category") for c in complete if c.get("category")]
  clustered = (
    len(complete) >= 2
    and len(categories) == len(complete)
    and len(set(categories)) == 1
  )

  if len(complete) == 0 and len(incomplete) == 0:
    next_prompt = "ask_first_choice"
  elif len(incomplete) > 0:
    last = incomplete[-1]
    if not (last.get("choice") or "").strip():
      next_prompt = "ask_choice"
    elif not (last.get("alternative") or "").strip():
      next_prompt = "ask_alternative"
    else:
      next_prompt = "ask_why_non_trivial"
  elif len(complete) < MIN_CHOICES:
    next_prompt = "ask_next_choice"
  elif clustered:
    next_prompt = "push_different_category"
  elif len(complete) < TARGET_CHOICES:
    next_prompt = "offer_third_choice"
  else:
    next_prompt = "reconcile_and_exit"

  done = len(complete) >= MIN_CHOICES and not clustered

  done_reasons = []
  if len(complete) >= MIN_CHOICES:
    done_reasons.append(f"{len(complete)} substantive choice(s) with alternatives logged")
  if not clustered:
    done_reasons.append("choices span more than one category (or category not declared)")

  observations = [
    f"Method: {method}.",
    f"Complete entries: {len(complete)} (need {MIN_CHOICES}, target {TARGET_CHOICES}).",
    f"Incomplete entries: {len(incomplete)}.",
  ]
  if judgment_flagged:
    observations.append(
      f"Judgment-shaped language detected at indices {judgment_flagged} — redirect: park for Phase 3."
    )
  if clustered:
    observations.append(
      "All choices fall in one category — push the student toward a different category."
    )
  observations.append(f"Next tutor move: {next_prompt}.")

  # LLM stub: a semantic check would tag each choice's method-relevant
  # category (sampling, measurement, comparison, etc.) so clustering is real
  # rather than dependent on an optional input field, and would judge whether
  # an "alternative" is actually plausible vs. trivially dismissible.
  return {
    "complete_count": len(complete),
    "incomplete_count": len(incomplete),
    "judgment_flagged": judgment_flagged,
    "category_clustered": clustered,
    "next_prompt": next_prompt,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
