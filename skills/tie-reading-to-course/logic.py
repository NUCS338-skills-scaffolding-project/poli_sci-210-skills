# logic.py — tie-reading-to-course
# Detects whether a student's stated connection between a reading and the
# course is surface-level (just restates the week's topic) or substantive
# (overlaps with a course learning objective).

OBJECTIVES = [
  "explain descriptive and causal inference",
  "evaluate inferential claims in research",
  "identify research designs and their strengths and weaknesses",
  "communicate research processes and findings",
]

def run(input):
  """
  :param input: {
    "student_text": str,
    "week_topic": str,
    "learning_objectives": list[str] | None,
    "tutor_pre_read": {                  # tutor's silent canonical read (optional)
      "week_link": str | None,           # one sentence
      "learning_objective_idx": int | None,
      "prior_week_echo": str | None,     # note or None
    } | None,
  }
  :return: {
    "is_surface": bool,
    "matched_objective_idx": int | None,
    "divergence": {                      # student vs. tutor_pre_read, if pre-read provided
      "objective_diverges": bool,        # student's matched idx differs from tutor's
    } | None,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  text = input.get("student_text", "").lower()
  topic = input.get("week_topic", "").lower()
  objectives = input.get("learning_objectives") or OBJECTIVES
  pre_read = input.get("tutor_pre_read") or None

  topic_words = {w for w in topic.split() if len(w) > 2}
  content_words = {w for w in text.split() if len(w) > 3}
  is_surface = len(content_words - topic_words) < 3

  matched = None
  for i, obj in enumerate(objectives):
    obj_words = {w for w in obj.lower().split() if len(w) > 3}
    if len(obj_words & content_words) >= 2:
      matched = i
      break

  divergence = None
  if pre_read:
    pre_idx = pre_read.get("learning_objective_idx")
    divergence = {
      "objective_diverges": (
        pre_idx is not None and matched is not None and pre_idx != matched
      ),
    }

  observations = []
  if is_surface:
    observations.append("Connection reads as surface-level — mostly restates the week topic.")
  else:
    observations.append("Connection adds substance beyond the week topic words.")
  if matched is not None:
    observations.append(f"Connection matches learning objective #{matched + 1}: '{objectives[matched]}'.")
  else:
    observations.append("Connection did not match any of the four course learning objectives.")

  done_reasons = []
  if not is_surface:
    done_reasons.append("connection is not surface-level")
  if matched is not None:
    done_reasons.append(f"connection matches objective #{matched + 1}")
  done = (not is_surface) and matched is not None

  # LLM stub: if keyword overlap misses, a semantic match could catch
  # paraphrases, and reconcile against tutor_pre_read more deeply.
  return {
    "is_surface": is_surface,
    "matched_objective_idx": matched,
    "divergence": divergence,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
