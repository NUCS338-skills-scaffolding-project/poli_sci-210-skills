# logic.py — argument-decomposition
# Detects how far a student has built up a leveled view of an argument:
# whether they've located a thesis, named main claims directly under it,
# put sub-claims or evidence under those, and described the overall shape.

SHAPE_CUES = (
  "chain", "parallel", "pillars", "stacked", "branches", "supports",
  "leads to", "builds on", "independent", "depends on", "rests on",
)

def run(input):
  """
  :param input: {
    "thesis": str | None,                        # top-level claim, in the student's words
    "main_claims": list[str] | None,             # claims directly under the thesis
    "sub_supports": dict[str, list[str]] | None, # main_claim -> sub-claims or evidence under it
    "shape_description": str | None,             # student's description of how the levels fit together
    "tutor_pre_read": {                          # tutor's silent canonical decomposition (optional)
      "thesis": str | None,
      "main_claims": list[str] | None,
      "sub_supports": dict[str, list[str]] | None,
      "shape": str | None,
    } | None,
  }
  :return: {
    "thesis_named": bool,
    "main_claim_count": int,
    "main_claims_without_support": list[str],
    "levels_built": int,                         # 0..3 — thesis, main, sub
    "shape_articulated": bool,
    "divergence": {                              # student vs. tutor_pre_read, if pre-read provided
      "thesis_diverges": bool,
      "main_claim_count_delta": int,             # student - tutor
    } | None,
    "done": bool,
    "done_reasons": list[str],
  }
  """
  thesis = (input.get("thesis") or "").strip()
  main_claims = input.get("main_claims") or []
  sub_supports = input.get("sub_supports") or {}
  shape = (input.get("shape_description") or "").strip()
  pre_read = input.get("tutor_pre_read") or None

  # A thesis worth its name is a claim, not a topic fragment.
  thesis_named = len(thesis.split()) >= 4

  unsupported = [c for c in main_claims if not (sub_supports.get(c) or [])]

  levels_built = 0
  if thesis_named:
    levels_built += 1
  if len(main_claims) >= 2:
    levels_built += 1
  if any(sub_supports.get(c) for c in main_claims):
    levels_built += 1

  lowered = shape.lower()
  shape_articulated = len(shape.split()) >= 8 or any(cue in lowered for cue in SHAPE_CUES)

  divergence = None
  if pre_read:
    pre_thesis = (pre_read.get("thesis") or "").strip().lower()
    pre_main = pre_read.get("main_claims") or []
    student_thesis_words = set(thesis.lower().split())
    pre_thesis_words = set(pre_thesis.split())
    overlap = len(student_thesis_words & pre_thesis_words)
    divergence = {
      "thesis_diverges": bool(pre_thesis) and overlap < 3,
      "main_claim_count_delta": len(main_claims) - len(pre_main),
    }

  done_reasons = []
  if levels_built >= 3:
    done_reasons.append("all three levels built")
  if shape_articulated:
    done_reasons.append("shape articulated in student's words")
  if main_claims and not unsupported:
    done_reasons.append("every main claim has support")
  done = (
    levels_built >= 3
    and shape_articulated
    and bool(main_claims)
    and not unsupported
  )

  # LLM stub: a semantic check could verify each main claim is genuinely
  # one level below the thesis (not a restatement of it, not a piece of
  # evidence in disguise) and reconcile against tutor_pre_read more deeply
  # than the bag-of-words overlap above.
  return {
    "thesis_named": thesis_named,
    "main_claim_count": len(main_claims),
    "main_claims_without_support": unsupported,
    "levels_built": levels_built,
    "shape_articulated": shape_articulated,
    "divergence": divergence,
    "done": done,
    "done_reasons": done_reasons,
  }
