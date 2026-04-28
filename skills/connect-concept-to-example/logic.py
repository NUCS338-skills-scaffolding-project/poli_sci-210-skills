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
    "tutor_pre_read": {                 # tutor's silent model example (optional)
      "model_example": str | None,      # a concrete example I'd give
      "feature_demonstrated": str | None,  # which defining feature it shows
    } | None,
  }
  :return: {
    "contains_feature": bool,
    "is_example_concrete": bool,
    "suggested_break": str,
    "divergence": {                     # student vs. tutor_pre_read, if pre-read provided
      "feature_diverges": bool,         # student's example targets a different feature
    } | None,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  example = input.get("student_example", "").lower()
  feature = input.get("defining_feature", "").lower()
  cues = [c.lower() for c in (input.get("feature_cues") or feature.split()) if c]
  pre_read = input.get("tutor_pre_read") or None

  contains = any(cue in example for cue in cues) if cues else False
  concrete = any(c in example for c in CONCRETE_CUES)
  break_q = (
    f"What if we changed one detail so the example no longer had "
    f"'{feature}' — would it still count? Why or why not?"
  )
  concept = input.get("concept", "")

  divergence = None
  if pre_read:
    pre_feature = (pre_read.get("feature_demonstrated") or "").strip().lower()
    divergence = {
      "feature_diverges": bool(pre_feature) and bool(feature) and pre_feature != feature,
    }

  observations = []
  if contains:
    observations.append(f"Example contains the defining feature ('{feature}') of '{concept}'.")
  else:
    observations.append(f"Example does not surface the defining feature ('{feature}') of '{concept}'.")
  if concrete:
    observations.append("Example is concrete — uses agent/action language ('I', 'we', 'flip', etc.).")
  else:
    observations.append("Example is abstract — no concrete agent or action verbs detected.")

  done_reasons = []
  if contains:
    done_reasons.append("example contains the defining feature")
  if concrete:
    done_reasons.append("example is concrete")
  done = contains and concrete

  # LLM stub: a semantic feature match is more robust than keyword cues,
  # and could reconcile against tutor_pre_read.model_example.
  return {
    "contains_feature": contains,
    "is_example_concrete": concrete,
    "suggested_break": break_q,
    "divergence": divergence,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
