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
  }
  :return: {"is_surface": bool, "matched_objective_idx": int | None}
  """
  text = input.get("student_text", "").lower()
  topic = input.get("week_topic", "").lower()
  objectives = input.get("learning_objectives") or OBJECTIVES

  topic_words = {w for w in topic.split() if len(w) > 2}
  content_words = {w for w in text.split() if len(w) > 3}
  is_surface = len(content_words - topic_words) < 3

  matched = None
  for i, obj in enumerate(objectives):
    obj_words = {w for w in obj.lower().split() if len(w) > 3}
    if len(obj_words & content_words) >= 2:
      matched = i
      break
  # LLM stub: if keyword overlap misses, a semantic match could catch paraphrases.
  return {"is_surface": is_surface, "matched_objective_idx": matched}
