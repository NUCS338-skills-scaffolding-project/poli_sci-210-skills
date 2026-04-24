# logic.py — evidence-placement-review
# Diagnoses whether a piece of evidence is placed near the claim it
# supports: same paragraph? before vs. after the claim? And whether the
# student has paired the evidence with an articulated claim at all.

EVIDENCE_MARKERS = ("quote", "\"", "“", "data", "table", "figure", "statistic", "percent", "%", "survey", "interview")

def run(input):
  """
  :param input: {
    "claim_text": str,
    "evidence_text": str,
    "claim_paragraph": int,     # 0-indexed paragraph number of the claim
    "evidence_paragraph": int,  # 0-indexed paragraph number of the evidence
    "claim_sentence_idx": int | None,     # sentence position within the claim's paragraph
    "evidence_sentence_idx": int | None,  # sentence position within the evidence's paragraph
  }
  :return: {
    "claim_articulated": bool,
    "same_paragraph": bool,
    "paragraph_distance": int,
    "evidence_before_claim": bool,
    "is_disconnected": bool,
  }
  """
  claim = (input.get("claim_text") or "").strip()
  evidence = (input.get("evidence_text") or "").strip()
  cp = int(input.get("claim_paragraph", 0) or 0)
  ep = int(input.get("evidence_paragraph", 0) or 0)
  cs = input.get("claim_sentence_idx")
  es = input.get("evidence_sentence_idx")

  articulated = len(claim.split()) >= 4
  # Heuristic check that the provided evidence actually looks like evidence.
  looks_like_evidence = any(m in evidence.lower() for m in EVIDENCE_MARKERS) or len(evidence.split()) >= 6

  same_para = cp == ep
  distance = abs(cp - ep)

  if same_para and cs is not None and es is not None:
    before = es < cs
  else:
    before = ep < cp

  # Disconnected = the student gave evidence but no articulated claim,
  # OR the evidence sits >= 1 paragraph away from its claim.
  disconnected = (not articulated and looks_like_evidence) or distance >= 1

  # LLM stub: a semantic check can confirm whether the evidence *actually*
  # supports the claim, which keyword distance cannot.
  return {
    "claim_articulated": articulated,
    "same_paragraph": same_para,
    "paragraph_distance": distance,
    "evidence_before_claim": before,
    "is_disconnected": disconnected,
  }
