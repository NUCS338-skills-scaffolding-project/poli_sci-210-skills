# logic.py — trace-claim-to-evidence
# Granular skill in Phase 1 (investigate-reading). Tracks whether the student
# has named a headline claim, pointed to a specific evidence locus, and read
# what the evidence actually shows. Pure function; no side effects.

import re

VALID_METHODS = (
  "theory-data",
  "inference",
  "surveys",
  "experiments",
  "large-n",
  "small-n",
  "machine-learning",
)

VALID_MATCH = ("tight", "loose", "suspicious gap", "")

# A specific locus must reference a labeled artifact: Table N, Figure N,
# Section X.Y, page N, or an explicit subsection name. "Results section" alone
# is too vague.
LOCUS_PATTERN = re.compile(
  r"\b(table\s+\d+|figure\s+\d+|fig\.?\s+\d+|section\s+\d+(\.\d+)?|p\.?\s*\d+|page\s+\d+|appendix\s+\w)",
  re.IGNORECASE,
)

VAGUE_LOCUS_CUES = ("results section", "the results", "their results", "the tables", "the figures")


def run(input):
  """
  :param input: {
    "week": int,
    "method": str,
    "article_path": str,
    "prior_session_logs": list[str] | None,
    "prior_in_phase_scratchpads": dict[str, str] | None,  # e.g. {"first-pass-orient": "<path>"}
    "headline_claim": str | None,
    "evidence_locus": str | None,
    "evidence_reading": str | None,                       # student's description of what's there
    "claim_evidence_match": str | None,                   # "tight" | "loose" | "suspicious gap"
  }
  :return: {
    "claim_ok": bool,
    "locus_ok": bool,
    "reading_ok": bool,
    "next_prompt": str,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  if not isinstance(input, dict):
    raise ValueError("input must be a dict")

  method = input.get("method")
  if method not in VALID_METHODS:
    raise ValueError(f"method={method!r} must be one of {VALID_METHODS}")

  claim = (input.get("headline_claim") or "").strip()
  locus = (input.get("evidence_locus") or "").strip()
  reading = (input.get("evidence_reading") or "").strip()
  match = (input.get("claim_evidence_match") or "").strip().lower()
  if match not in VALID_MATCH:
    raise ValueError(f"claim_evidence_match={match!r} must be one of {VALID_MATCH}")

  claim_ok = bool(claim) and len(claim.split()) >= 4
  locus_low = locus.lower()
  is_vague = any(c in locus_low for c in VAGUE_LOCUS_CUES) and not LOCUS_PATTERN.search(locus)
  locus_ok = bool(locus) and bool(LOCUS_PATTERN.search(locus)) and not is_vague

  # A real reading references the evidence, not just the claim. Heuristic: at
  # least one digit OR a comparison word ("higher", "lower", "more", "less",
  # "negative", "positive", "stronger", "weaker") in the reading.
  has_number = bool(re.search(r"\d", reading))
  has_comparison = bool(re.search(
    r"\b(higher|lower|more|less|negative|positive|stronger|weaker|coefficient|p\s*<|significant)\b",
    reading,
    re.IGNORECASE,
  ))
  reading_ok = bool(reading) and (has_number or has_comparison)

  if not claim:
    next_prompt = "ask_claim"
  elif not claim_ok:
    next_prompt = "redo_claim"
  elif not locus:
    next_prompt = "ask_locus"
  elif not locus_ok:
    next_prompt = "redo_locus"
  elif not reading:
    next_prompt = "ask_reading"
  elif not reading_ok:
    next_prompt = "redo_reading"
  elif not match:
    next_prompt = "label_match"
  else:
    next_prompt = "reconcile_and_exit"

  done = claim_ok and locus_ok and reading_ok and bool(match)
  done_reasons = []
  if claim_ok:
    done_reasons.append("headline claim is named with substance")
  if locus_ok:
    done_reasons.append("evidence locus matches a specific artifact reference")
  if reading_ok:
    done_reasons.append("reading references the evidence (numbers or comparison language)")
  if match:
    done_reasons.append(f"claim_evidence_match labeled: {match}")

  observations = [
    f"Method: {method}.",
    f"Claim: {'present' if claim else 'missing'}.",
    f"Locus: {'present' if locus else 'missing'}{' (vague)' if locus and is_vague else ''}.",
    f"Reading: {'present' if reading else 'missing'}{' (no numbers/comparison language)' if reading and not reading_ok else ''}.",
    f"Match label: {match or 'unset'}.",
  ]
  if match == "suspicious gap":
    observations.append(
      "Suspicious gap flagged — log under Divergences and surface in Completion Notes for Phase 3."
    )
  observations.append(f"Next tutor move: {next_prompt}.")

  # LLM stub: a semantic check would verify that the locus actually contains
  # the claim (rather than just being a labeled artifact reference) and would
  # detect when the student's "reading" is just a paraphrase of the claim.
  return {
    "claim_ok": claim_ok,
    "locus_ok": locus_ok,
    "reading_ok": reading_ok,
    "next_prompt": next_prompt,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
