# logic.py — identify-argument-structure
# Classifies a student's response as descriptive (topic-like) or a claim,
# and flags whether they pointed to a specific section of the text.

import re

CLAIM_MARKERS = ("argues", "claims", "shows", "demonstrates", "finds", "because", "therefore", "suggests")
DESCRIPTIVE_MARKERS = ("is about", "talks about", "describes", "discusses", "covers")
SECTION_PAT = re.compile(r"\b(section|chapter|page|pp?\.|intro|conclusion|abstract|figure|table)\b", re.I)

def run(input):
  """
  :param input: {
    "student_response": str,
    "piece": "thesis" | "evidence" | "warrant",
  }
  :return: {"type": "claim" | "descriptive", "has_section_ref": bool, "piece": str}
  """
  text = input.get("student_response", "")
  piece = input.get("piece", "thesis")
  lowered = text.lower()

  claim_hits = sum(m in lowered for m in CLAIM_MARKERS)
  desc_hits = sum(m in lowered for m in DESCRIPTIVE_MARKERS)
  resp_type = "claim" if claim_hits > desc_hits else "descriptive"
  has_ref = bool(SECTION_PAT.search(text))
  # LLM stub: marker-counting misses subtle claims; escalate when confidence is low.
  return {"type": resp_type, "has_section_ref": has_ref, "piece": piece}
