# logic.py — explain-back-check
# Detects which of the three expected components are present in a
# student's own-words explanation: definition, importance, example.

DEFINITION_CUES = (" is ", " means ", "refers to", "defined as")
IMPORTANCE_CUES = ("matters", "important", "because", "so that", "allows", "prevents", "without it")
EXAMPLE_CUES = ("for example", "for instance", "e.g.", "such as", "like when", "imagine")

def _has_any(text, cues):
  lowered = text.lower()
  return any(c in lowered for c in cues)

def run(input):
  """
  :param input: {"student_explanation": str, "concept": str | None}
  :return: {
    "has_definition": bool,
    "has_importance": bool,
    "has_example": bool,
    "missing": list[str],
  }
  """
  text = input.get("student_explanation", "")
  has_def = _has_any(text, DEFINITION_CUES) and len(text.split()) >= 6
  has_imp = _has_any(text, IMPORTANCE_CUES)
  has_ex = _has_any(text, EXAMPLE_CUES)
  missing = [k for k, v in [("definition", has_def), ("importance", has_imp), ("example", has_ex)] if not v]
  # LLM stub: cues miss paraphrased explanations; escalate when missing looks wrong.
  return {"has_definition": has_def, "has_importance": has_imp, "has_example": has_ex, "missing": missing}
