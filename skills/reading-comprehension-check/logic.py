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
    "tutor_pre_read": {                  # tutor's silent canonical answers (optional)
      "what": str | None,                # one sentence
      "why": str | None,                 # one sentence
      "so_what": str | None,             # one sentence
    } | None,
  }
  :return: {
    "is_thin": bool,
    "has_text_reference": bool,
    "layer": str,
    "divergence": {                      # student vs. tutor_pre_read for current layer
      "layer_diverges": bool,            # student answer has little overlap with pre-read for this layer
    } | None,
    "done": bool,                        # gate for the *current* layer only
    "done_reasons": list[str],
    "observations": list[str],
  }
  Note: the skill closes only when all three layers have each passed the
  gate across calls — this module reports per-layer status.
  """
  text = input.get("student_text", "")
  layer = input.get("layer", "what")
  pre_read = input.get("tutor_pre_read") or None
  lowered = text.lower()

  word_count = len(text.split())
  hedges = sum(p in lowered for p in THIN_PHRASES)
  has_ref = bool(SECTION_PAT.search(text))
  is_thin = word_count < 15 or (hedges >= 2 and not has_ref)

  divergence = None
  if pre_read:
    pre_layer = (pre_read.get(layer) or "").strip().lower()
    if pre_layer:
      pre_words = set(pre_layer.split()) - {"the", "a", "an", "of", "is", "to", "in", "and", "or"}
      student_words = set(lowered.split())
      overlap = len(pre_words & student_words)
      divergence = {"layer_diverges": overlap < 2}
    else:
      divergence = {"layer_diverges": False}

  observations = []
  if is_thin:
    observations.append(f"At the '{layer}' layer, response reads as thin — short or hedged without textual reference.")
  else:
    observations.append(f"At the '{layer}' layer, response is substantive (length and/or specificity OK).")
  if has_ref:
    observations.append("Response cites a section, page, figure, or table from the reading.")
  else:
    observations.append("Response does not cite any section/page/figure from the reading.")

  done_reasons = []
  if not is_thin:
    done_reasons.append(f"'{layer}' answer is not thin")
  if has_ref:
    done_reasons.append("answer cites the text")
  done = (not is_thin) and has_ref

  # LLM stub: a semantic check could catch substantive-but-hedged answers,
  # and reconcile against tutor_pre_read for paraphrase matches.
  return {
    "is_thin": is_thin,
    "has_text_reference": has_ref,
    "layer": layer,
    "divergence": divergence,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
