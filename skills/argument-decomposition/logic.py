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
  }
  :return: {
    "thesis_named": bool,
    "main_claim_count": int,
    "main_claims_without_support": list[str],
    "levels_built": int,                         # 0..3 — thesis, main, sub
    "shape_articulated": bool,
  }
  """
  thesis = (input.get("thesis") or "").strip()
  main_claims = input.get("main_claims") or []
  sub_supports = input.get("sub_supports") or {}
  shape = (input.get("shape_description") or "").strip()

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

  # LLM stub: a semantic check could verify each main claim is genuinely
  # one level below the thesis (not a restatement of it, not a piece of
  # evidence in disguise) — and flag level-collapse the heuristic misses.
  return {
    "thesis_named": thesis_named,
    "main_claim_count": len(main_claims),
    "main_claims_without_support": unsupported,
    "levels_built": levels_built,
    "shape_articulated": shape_articulated,
  }
