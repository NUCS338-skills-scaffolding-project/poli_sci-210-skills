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
    "tutor_pre_read": {                  # tutor's silent canonical read (optional)
      "relationship": str | None,        # contrast/cause/sequence/addition/example/consequence
      "rationale": str | None,           # one sentence why
    } | None,
  }
  :return: {
    "relationship_named": bool,
    "relationship_matches_signal": bool,
    "signals_found": list[str],
    "looks_choppy": bool,
    "divergence": {                      # student vs. tutor_pre_read, if pre-read provided
      "relationship_diverges": bool,
    } | None,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  before = input.get("text_before", "") or ""
  after = input.get("text_after", "") or ""
  label = (input.get("student_relationship") or "").strip().lower()
  pre_read = input.get("tutor_pre_read") or None

  joined = f"{before} {after}".lower()
  signals = [w for w in ALL_TRANSITIONS if re.search(rf"\b{re.escape(w)}\b", joined)]

  named = label in TRANSITION_WORDS
  matches_signal = named and any(w in signals for w in TRANSITION_WORDS[label])

  # Choppy ≈ both halves short and no transition signal bridging them.
  short_before = len(before.split()) < 8
  short_after = len(after.split()) < 8
  choppy = (short_before or short_after) and not signals

  divergence = None
  if pre_read:
    pre_rel = (pre_read.get("relationship") or "").strip().lower()
    divergence = {
      "relationship_diverges": bool(pre_rel) and bool(label) and pre_rel != label,
    }

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

  done_reasons = []
  if named:
    done_reasons.append("relationship named")
  if matches_signal:
    done_reasons.append("named relationship matches a signal in the text")
  if not choppy:
    done_reasons.append("text does not read choppy")
  done = named and matches_signal and not choppy

  # LLM stub: a semantic check could confirm whether the student's named
  # relationship actually matches the *meaning* of the two sentences, not
  # just presence of a keyword, and reconcile against tutor_pre_read.
  return {
    "relationship_named": named,
    "relationship_matches_signal": matches_signal,
    "signals_found": signals,
    "looks_choppy": choppy,
    "divergence": divergence,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
