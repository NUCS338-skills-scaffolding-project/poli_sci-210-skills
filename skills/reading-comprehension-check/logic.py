# logic.py — reading-comprehension-check
# Flags whether a student's answer about a reading is "thin" (generic,
# hedged, no textual evidence) versus substantive (contains a specific
# section, page, or figure reference).

import re

THIN_PHRASES = ("i think", "something about", "i guess", "basically", "kind of", "sort of")
SECTION_PAT = re.compile(r"\b(section|chapter|page|pp?\.|fig(ure)?|table|intro|conclusion)\b", re.I)

def run(input):
  """
  :param input: {
    "student_text": str,
    "layer": "what" | "why" | "so_what",
  }
  :return: {"is_thin": bool, "has_text_reference": bool, "layer": str}
  """
  text = input.get("student_text", "")
  layer = input.get("layer", "what")
  lowered = text.lower()

  word_count = len(text.split())
  hedges = sum(p in lowered for p in THIN_PHRASES)
  has_ref = bool(SECTION_PAT.search(text))
  is_thin = word_count < 15 or (hedges >= 2 and not has_ref)
  # LLM stub: a semantic check could catch substantive-but-hedged answers.
  return {"is_thin": is_thin, "has_text_reference": has_ref, "layer": layer}
