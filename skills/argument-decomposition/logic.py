# logic.py — argument-decomposition
# Detects how far a student has gone in decomposing an argument:
# whether their summary is flat (one bundled claim) or shows structure
# (multiple sub-claims, evidence pairings, and a named connective shape).

import re

CONNECTIVES = ("and", "also", "but", "however", "because", "therefore", "first", "second", "third", "while", "whereas")
EVIDENCE_CUES = ("data", "evidence", "shows", "finds", "found", "study", "survey", "case", "example", "figure", "table", "section", "page")
STRUCTURE_CUES = {
  "chain": ("leads to", "then", "which means", "because", "so that", "causes"),
  "parallel": ("also", "in addition", "as well", "separately", "independently", "alongside"),
}

def run(input):
  """
  :param input: {
    "student_summary": str,           # their one-sentence argument
    "sub_claims": list[str] | None,   # the sub-claims they've named so far
    "evidence_pairings": dict[str, str] | None,  # claim -> evidence text
    "structure_label": str | None,    # "chain" | "parallel" | None
  }
  :return: {
    "is_flat_summary": bool,
    "sub_claim_count": int,
    "claims_without_evidence": list[str],
    "structure_named": bool,
    "structure_matches_language": bool,
  }
  """
  summary = input.get("student_summary", "")
  sub_claims = input.get("sub_claims") or []
  pairings = input.get("evidence_pairings") or {}
  label = input.get("structure_label")

  lowered = summary.lower()
  has_connective = any(re.search(rf"\b{c}\b", lowered) for c in CONNECTIVES)
  is_flat = len(summary.split()) < 20 and not has_connective and len(sub_claims) == 0

  missing = [c for c in sub_claims if not any(cue in (pairings.get(c, "") or "").lower() for cue in EVIDENCE_CUES)]

  structure_named = label in STRUCTURE_CUES
  joined_pairings = " ".join(pairings.values()).lower()
  matches = structure_named and any(cue in joined_pairings for cue in STRUCTURE_CUES[label])

  # LLM stub: a semantic check catches decomposition phrased without cue words
  # (e.g., a student who names structure without using "chain" / "parallel").
  return {
    "is_flat_summary": is_flat,
    "sub_claim_count": len(sub_claims),
    "claims_without_evidence": missing,
    "structure_named": structure_named,
    "structure_matches_language": matches,
  }
