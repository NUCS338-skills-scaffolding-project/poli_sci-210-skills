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
  :param input: {
    "student_explanation": str,
    "concept": str | None,
    "tutor_pre_read": {                  # tutor's silent three-part canonical (optional)
      "definition": str | None,          # one sentence
      "importance": str | None,          # one sentence
      "example": str | None,             # concrete
    } | None,
  }
  :return: {
    "has_definition": bool,
    "has_importance": bool,
    "has_example": bool,
    "missing": list[str],
    "divergence": {                      # student vs. tutor_pre_read, if pre-read provided
      "missing_relative_to_pre_read": list[str],  # which pre-read parts have no match in student text
    } | None,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  text = input.get("student_explanation", "")
  pre_read = input.get("tutor_pre_read") or None

  has_def = _has_any(text, DEFINITION_CUES) and len(text.split()) >= 6
  has_imp = _has_any(text, IMPORTANCE_CUES)
  has_ex = _has_any(text, EXAMPLE_CUES)
  missing = [k for k, v in [("definition", has_def), ("importance", has_imp), ("example", has_ex)] if not v]
  present = [k for k in ("definition", "importance", "example") if k not in missing]

  divergence = None
  if pre_read:
    pre_missing = []
    if pre_read.get("definition") and not has_def:
      pre_missing.append("definition")
    if pre_read.get("importance") and not has_imp:
      pre_missing.append("importance")
    if pre_read.get("example") and not has_ex:
      pre_missing.append("example")
    divergence = {"missing_relative_to_pre_read": pre_missing}

  observations = []
  if present:
    observations.append(f"Explanation contains: {', '.join(present)}.")
  if missing:
    observations.append(f"Explanation missing: {', '.join(missing)}.")
  else:
    observations.append("Explanation hits all three components (definition, importance, example).")

  done_reasons = []
  if has_def:
    done_reasons.append("definition present")
  if has_imp:
    done_reasons.append("importance present")
  if has_ex:
    done_reasons.append("example present")
  done = has_def and has_imp and has_ex

  # LLM stub: cues miss paraphrased explanations; escalate when missing
  # looks wrong, and reconcile against tutor_pre_read for paraphrase matches.
  return {
    "has_definition": has_def,
    "has_importance": has_imp,
    "has_example": has_ex,
    "missing": missing,
    "divergence": divergence,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
