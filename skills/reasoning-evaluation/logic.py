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
    "warrant": str,                          # the student's stated reason evidence supports claim
    "student_addressed_gap": bool | None,    # has the student named/patched the gap the tutor flagged?
    "tutor_pre_read": {                      # tutor's silent triple + gap (optional)
      "claim": str | None,
      "evidence": str | None,
      "warrant": str | None,
      "likely_gap": str | None,              # the gap I'd flag
    } | None,
  }
  :return: {
    "warrant_stated": bool,
    "uses_causal_language": bool,
    "contains_unstated_assumption": bool,
    "is_hedged": bool,
    "likely_gap": str | None,
    "divergence": {                          # student vs. tutor_pre_read, if pre-read provided
      "warrant_diverges": bool,              # student warrant has little overlap with pre-read warrant
    } | None,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  claim = (input.get("claim") or "").strip()
  evidence = (input.get("evidence") or "").strip()
  warrant = (input.get("warrant") or "").strip()
  addressed_gap = bool(input.get("student_addressed_gap"))
  pre_read = input.get("tutor_pre_read") or None
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

  divergence = None
  if pre_read:
    pre_warrant = (pre_read.get("warrant") or "").strip().lower()
    if pre_warrant and warrant:
      pre_words = set(pre_warrant.split()) - {"the", "a", "an", "of", "is", "to", "in", "and", "or"}
      student_words = set(w_lower.split())
      overlap = len(pre_words & student_words)
      divergence = {"warrant_diverges": overlap < 2}
    else:
      divergence = {"warrant_diverges": bool(pre_warrant) and not warrant}

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

  done_reasons = []
  if stated:
    done_reasons.append("warrant stated")
  if not assumed:
    done_reasons.append("no unstated assumption flagged")
  if gap is None:
    done_reasons.append("no likely gap detected")
  elif addressed_gap:
    done_reasons.append("student addressed the flagged gap")
  done = stated and (not assumed) and (gap is None or addressed_gap)

  # LLM stub: the hardest check — does the warrant *actually* bridge this
  # specific evidence to this specific claim — is a semantic judgment that
  # this keyword-based pass cannot make. Should also reconcile the
  # student's warrant against tutor_pre_read.warrant for paraphrase fit.
  return {
    "warrant_stated": stated,
    "uses_causal_language": causal,
    "contains_unstated_assumption": assumed,
    "is_hedged": hedged,
    "likely_gap": gap,
    "divergence": divergence,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
