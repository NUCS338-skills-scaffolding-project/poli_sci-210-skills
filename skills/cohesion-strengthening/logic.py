# logic.py — cohesion-strengthening
# Diagnoses a transition between two adjacent sentences or paragraphs:
# whether the student has named the relationship, whether any transition
# signal appears in the text, and whether the text looks choppy.

import re

TRANSITION_WORDS = {
  "addition": ("also", "moreover", "furthermore", "in addition", "additionally"),
  "contrast": ("however", "but", "yet", "although", "whereas", "on the other hand"),
  "example": ("for example", "for instance", "such as", "e.g.", "including"),
  "consequence": ("therefore", "so", "thus", "as a result", "consequently", "hence"),
}
ALL_TRANSITIONS = tuple(w for group in TRANSITION_WORDS.values() for w in group)

def run(input):
  """
  :param input: {
    "text_before": str,          # last sentence of paragraph A (or prior sentence)
    "text_after": str,           # first sentence of paragraph B (or next sentence)
    "student_relationship": str | None,  # their label: addition/contrast/example/consequence
  }
  :return: {
    "relationship_named": bool,
    "relationship_matches_signal": bool,
    "signals_found": list[str],
    "looks_choppy": bool,
  }
  """
  before = input.get("text_before", "") or ""
  after = input.get("text_after", "") or ""
  label = (input.get("student_relationship") or "").strip().lower()

  joined = f"{before} {after}".lower()
  signals = [w for w in ALL_TRANSITIONS if re.search(rf"\b{re.escape(w)}\b", joined)]

  named = label in TRANSITION_WORDS
  matches_signal = named and any(w in signals for w in TRANSITION_WORDS[label])

  # Choppy ≈ both halves short and no transition signal bridging them.
  short_before = len(before.split()) < 8
  short_after = len(after.split()) < 8
  choppy = (short_before or short_after) and not signals

  observations = []
  if named and matches_signal:
    observations.append(f"Named the transition as '{label}'; the text carries that relationship's signal words.")
  elif named and signals:
    observations.append(f"Named the transition as '{label}', but the text uses different signals: {', '.join(signals)}.")
  elif named:
    observations.append(f"Named the transition as '{label}', but no transition signal appears in the text.")
  elif signals:
    observations.append(f"Did not name the transition; the text contains these signals: {', '.join(signals)}.")
  else:
    observations.append("No transition relationship named, and no signal words detected in the text.")
  if choppy:
    observations.append("Adjacent sentences read choppy — both short and unbridged by a transition.")

  # LLM stub: a semantic check could confirm whether the student's named
  # relationship actually matches the *meaning* of the two sentences, not
  # just presence of a keyword.
  return {
    "relationship_named": named,
    "relationship_matches_signal": matches_signal,
    "signals_found": signals,
    "looks_choppy": choppy,
    "observations": observations,
  }
