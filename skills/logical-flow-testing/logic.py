# logic.py — logical-flow-testing
# Maps a student's ordered list of section summaries to the canonical
# POLI SCI 210 critique order (question → design → critique → change)
# and flags the weakest transition point.

import re

SECTION_KINDS = {
  "question": ("research question", "why it matters", "motivation", "relevance", "introduction", "question"),
  "change":   ("would change", "propose changes", "propose", "recommendation", "alternative", "improve", "fix", "change"),
  "critique": ("critique", "criticism", "limitation", "weakness", "problem", "issue", "concern"),
  "design":   ("research design", "methods", "method", "procedure", "approach", "design", "sample", "data"),
}
CANONICAL_ORDER = ("question", "design", "critique", "change")

def _classify(summary):
  lowered = summary.lower()
  # Score each kind by how many cues match; break ties by canonical order.
  scores = {}
  for kind, cues in SECTION_KINDS.items():
    hits = sum(1 for c in cues if re.search(rf"\b{re.escape(c)}\b", lowered))
    if hits:
      scores[kind] = hits
  if not scores:
    return None
  return max(scores, key=lambda k: (scores[k], -CANONICAL_ORDER.index(k) if k in CANONICAL_ORDER else 0))

def run(input):
  """
  :param input: {
    "section_summaries": list[str],     # one-sentence summary per section in order
    "student_transitions": list[str],   # why each section follows the previous (optional)
  }
  :return: {
    "classified_kinds": list[str | None],
    "follows_canonical": bool,
    "unclassified_sections": list[int],
    "weakest_transition_index": int | None,  # 0 means between section 0 and 1
  }
  """
  sections = input.get("section_summaries") or []
  transitions = input.get("student_transitions") or []

  kinds = [_classify(s) for s in sections]
  unclassified = [i for i, k in enumerate(kinds) if k is None]

  known = [k for k in kinds if k]
  expected = [k for k in CANONICAL_ORDER if k in known]
  follows = known == expected

  # Weakest transition: first one where the student's justification is short
  # or missing, or where kinds jump out of canonical order.
  weakest = None
  for i in range(len(sections) - 1):
    justification = transitions[i] if i < len(transitions) else ""
    thin_justification = len(justification.split()) < 6
    a, b = kinds[i], kinds[i + 1]
    out_of_order = (
      a in CANONICAL_ORDER and b in CANONICAL_ORDER
      and CANONICAL_ORDER.index(a) > CANONICAL_ORDER.index(b)
    )
    if thin_justification or out_of_order or a is None or b is None:
      weakest = i
      break

  # LLM stub: a semantic classifier can pick up sections that don't use the
  # cue words but still play one of these roles (e.g., an intro that never
  # says "question" but poses one).
  return {
    "classified_kinds": kinds,
    "follows_canonical": follows,
    "unclassified_sections": unclassified,
    "weakest_transition_index": weakest,
  }
