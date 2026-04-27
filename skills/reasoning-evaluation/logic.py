# logic.py — reasoning-evaluation
# Tests the warrant — the logical bridge from evidence to claim.
# Flags whether the student has stated a warrant at all, whether it uses
# causal/inferential language, and whether an unstated assumption is
# likely lurking.

import re

WARRANT_CUES = ("because", "since", "which means", "this shows", "this means", "implies", "therefore", "so ", "as a result")
ASSUMPTION_CUES = ("obviously", "clearly", "of course", "everyone knows", "it's just", "naturally")
HEDGE_CUES = ("maybe", "i think", "kind of", "sort of", "possibly", "might")

def run(input):
  """
  :param input: {
    "claim": str,
    "evidence": str,
    "warrant": str,   # the student's stated reason evidence supports claim
  }
  :return: {
    "warrant_stated": bool,
    "uses_causal_language": bool,
    "contains_unstated_assumption": bool,
    "is_hedged": bool,
    "likely_gap": str | None,
  }
  """
  claim = (input.get("claim") or "").strip()
  evidence = (input.get("evidence") or "").strip()
  warrant = (input.get("warrant") or "").strip()
  w_lower = warrant.lower()

  stated = len(warrant.split()) >= 5
  causal = any(c in w_lower for c in WARRANT_CUES)
  assumed = any(c in w_lower for c in ASSUMPTION_CUES)
  hedged = any(c in w_lower for c in HEDGE_CUES)

  if not stated:
    gap = "missing_warrant"
  elif not causal:
    gap = "warrant_lacks_inferential_link"
  elif assumed:
    gap = "warrant_hides_an_assumption"
  elif not claim or not evidence:
    gap = "claim_or_evidence_missing"
  else:
    gap = None

  observations = []
  if stated:
    observations.append("Warrant is stated (5+ words).")
  else:
    observations.append("Warrant is not stated — student gave evidence and claim but no bridge.")
  if causal:
    observations.append("Warrant uses causal/inferential language ('because', 'therefore', etc.).")
  elif stated:
    observations.append("Warrant lacks causal/inferential cue words.")
  if assumed:
    observations.append("Warrant flags an unstated assumption (uses 'obviously', 'clearly', etc.).")
  if hedged:
    observations.append("Warrant is hedged ('maybe', 'i think', 'kind of').")
  if gap:
    observations.append(f"Likely reasoning gap: {gap}.")

  # LLM stub: the hardest check — does the warrant *actually* bridge this
  # specific evidence to this specific claim — is a semantic judgment that
  # this keyword-based pass cannot make.
  return {
    "warrant_stated": stated,
    "uses_causal_language": causal,
    "contains_unstated_assumption": assumed,
    "is_hedged": hedged,
    "likely_gap": gap,
    "observations": observations,
  }
