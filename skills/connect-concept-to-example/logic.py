# logic.py — connect-concept-to-example
# Checks whether a student's example contains the concept's defining
# feature, and generates an adversarial tweak to stress-test the example.

CONCRETE_CUES = ("i ", "we ", "they ", "flip", "assign", "ask", "measure", "sample", "survey")

def run(input):
  """
  :param input: {
    "concept": str,
    "student_example": str,
    "defining_feature": str,            # one short phrase (e.g. "equal probability")
    "feature_cues": list[str] | None,   # optional keywords indicating the feature
  }
  :return: {
    "contains_feature": bool,
    "is_example_concrete": bool,
    "suggested_break": str,
  }
  """
  example = input.get("student_example", "").lower()
  feature = input.get("defining_feature", "").lower()
  cues = [c.lower() for c in (input.get("feature_cues") or feature.split()) if c]
  contains = any(cue in example for cue in cues) if cues else False
  concrete = any(c in example for c in CONCRETE_CUES)
  break_q = (
    f"What if we changed one detail so the example no longer had "
    f"'{feature}' — would it still count? Why or why not?"
  )
  # LLM stub: a semantic feature match is more robust than keyword cues.
  return {"contains_feature": contains, "is_example_concrete": concrete, "suggested_break": break_q}
