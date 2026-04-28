# logic.py — generate-study-questions
# Returns a question template and an LLM prompt for a given topic,
# difficulty level, and format. The tutor fills in the blanks or calls
# the LLM prompt; this module never answers its own question.

TEMPLATES = {
  "tf": "True or false: {claim_about_topic}",
  "mc": "Which of the following best describes {concept}?\n  a) ...\n  b) ...\n  c) ...\n  d) ...",
  "short": "In two sentences, explain {concept} in your own words.",
  "matching": "Match each term to its definition:\n  terms: {terms}\n  definitions: {defs}",
}

def run(input):
  """
  :param input: {
    "topic": str,
    "level": "review" | "practice" | "stretch",
    "format": "tf" | "mc" | "short" | "matching",
    "student_answers_count": int | None,        # how many questions the student has answered so far
    "answers_above_recall_level": bool | None,  # has at least one answer engaged above recall?
    "tutor_pre_read": {                         # tutor's silent target (optional)
      "target_concepts": list[str] | None,
      "intended_difficulty": str | None,        # recall / apply / analyze / evaluate
    } | None,
  }
  :return: {
    "template": str,
    "llm_prompt": str,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  Note: divergence is not computed here — comparing free-text student answers
  to target concepts is a semantic call best left to the tutor LLM.
  """
  topic = input.get("topic", "")
  level = input.get("level", "practice")
  fmt = input.get("format", "tf")
  answers_count = int(input.get("student_answers_count") or 0)
  above_recall = bool(input.get("answers_above_recall_level"))

  template = TEMPLATES.get(fmt, TEMPLATES["tf"])
  llm_prompt = (
    f"Generate one {level}-difficulty {fmt} question about '{topic}'. "
    f"Do NOT reveal the answer. The question tests a student; never pre-answer it."
  )
  observations = [f"Generated a {level}-difficulty {fmt} question template for '{topic}'."]
  if answers_count:
    observations.append(f"Student has answered {answers_count} question(s) so far.")
  if above_recall:
    observations.append("At least one answer engaged above the recall level.")

  done_reasons = []
  if answers_count >= 3:
    done_reasons.append(f"student answered {answers_count} questions")
  if above_recall:
    done_reasons.append("at least one answer above recall level")
  done = answers_count >= 3 and above_recall

  return {
    "template": template,
    "llm_prompt": llm_prompt,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
