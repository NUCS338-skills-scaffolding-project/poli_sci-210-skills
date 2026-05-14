# logic.py — pick-week-concept
# Validates the student's chosen {week, concept, ai_prompt} and returns
# a heuristic "done" gate for the orchestrator. No side effects.

VALID_WEEKS = set(range(1, 10))  # 1..9 inclusive — class is in session; week 10 is reading period

# Topic-sized words that should not stand alone as the concept phrase.
# This is a guardrail, not a vocabulary — narrowing is a tutor judgment.
TOPIC_WORDS = {
  "surveys", "experiments", "inference", "theory", "data",
  "machine learning", "ml", "small n", "large n", "sampling",
}


def _is_specific(concept_phrase):
  """A specific concept phrase is short and not just a topic word."""
  if not concept_phrase:
    return False
  phrase = concept_phrase.strip().lower()
  if not phrase:
    return False
  if phrase in TOPIC_WORDS:
    return False
  # Many words → likely a sentence, not a phrase. ≤10 words is the band we want.
  if len(phrase.split()) > 10:
    return False
  return True


INPUT_SCHEMA: dict = {
    "week": "int | None",
    "concept_phrase": "str | None",
    "ai_prompt": "str | None",
    "has_hypothesis": "bool | None",
    "tutor_pre_read": "dict | None",
}


def run(input):
  """
  :param input: {
    "week": int | None,                    # 1..9
    "concept_phrase": str | None,          # e.g. "social desirability bias"
    "ai_prompt": str | None,               # one-sentence "what to ask the AI"
    "has_hypothesis": bool | None,         # tutor flag: student named a course-vs-AI gap they expect
    "tutor_pre_read": dict | None,         # surveyed slide topics (informational)
  }
  :return: {
    "week_valid": bool,
    "concept_is_specific": bool,
    "ai_prompt_framed": bool,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  if not isinstance(input, dict):
    raise ValueError("input must be a dict")

  week = input.get("week")
  concept = (input.get("concept_phrase") or "").strip()
  ai_prompt = (input.get("ai_prompt") or "").strip()
  has_hypothesis = bool(input.get("has_hypothesis"))

  week_valid = isinstance(week, int) and week in VALID_WEEKS
  concept_specific = _is_specific(concept)
  prompt_framed = len(ai_prompt.split()) >= 5  # rough: needs at least a real sentence

  done_reasons = []
  observations = []

  if week_valid:
    done_reasons.append(f"week {week} is a valid course week")
  else:
    observations.append("Week not yet set or out of range (1..9).")

  if concept_specific:
    done_reasons.append(f"concept '{concept}' is specific enough")
  elif concept:
    observations.append(
      f"Concept '{concept}' is too broad or topic-sized — push toward a one-line phrase."
    )
  else:
    observations.append("No concept named yet.")

  if prompt_framed:
    done_reasons.append("a one-sentence AI prompt is framed")
  else:
    observations.append("No 'what to ask the AI' sentence yet — get one before exiting.")

  if not has_hypothesis:
    observations.append(
      "Student hasn't named any expected course-vs-AI gap — soft signal, not a gate."
    )

  done = week_valid and concept_specific and prompt_framed

  return {
    "week_valid": week_valid,
    "concept_is_specific": concept_specific,
    "ai_prompt_framed": prompt_framed,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
