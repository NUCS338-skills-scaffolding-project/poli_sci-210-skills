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
  }
  :return: {"template": str, "llm_prompt": str}
  """
  topic = input.get("topic", "")
  level = input.get("level", "practice")
  fmt = input.get("format", "tf")
  template = TEMPLATES.get(fmt, TEMPLATES["tf"])
  llm_prompt = (
    f"Generate one {level}-difficulty {fmt} question about '{topic}'. "
    f"Do NOT reveal the answer. The question tests a student; never pre-answer it."
  )
  observations = [f"Generated a {level}-difficulty {fmt} question template for '{topic}'."]
  return {"template": template, "llm_prompt": llm_prompt, "observations": observations}
