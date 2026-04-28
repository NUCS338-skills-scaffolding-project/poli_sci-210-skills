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
    "tutor_pre_read": {                   # tutor's silent placement read (optional)
      "placement_verdict": str | None,    # sound / disconnected / inverted
      "ideal_placement": str | None,      # where I'd put it
    } | None,
  }
  :return: {
    "claim_articulated": bool,
    "same_paragraph": bool,
    "paragraph_distance": int,
    "evidence_before_claim": bool,
    "is_disconnected": bool,
    "divergence": {                       # student vs. tutor_pre_read, if pre-read provided
      "verdict_diverges": bool,           # tutor flagged disconnected/inverted but text reads as sound, etc.
    } | None,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  claim = (input.get("claim_text") or "").strip()
  evidence = (input.get("evidence_text") or "").strip()
  cp = int(input.get("claim_paragraph", 0) or 0)
  ep = int(input.get("evidence_paragraph", 0) or 0)
  cs = input.get("claim_sentence_idx")
  es = input.get("evidence_sentence_idx")
  pre_read = input.get("tutor_pre_read") or None

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

  divergence = None
  if pre_read:
    verdict = (pre_read.get("placement_verdict") or "").strip().lower()
    text_reads_disconnected = disconnected
    text_reads_inverted = before and same_para
    tutor_says_disconnected = verdict == "disconnected"
    tutor_says_inverted = verdict == "inverted"
    tutor_says_sound = verdict == "sound"
    verdict_diverges = (
      (tutor_says_disconnected and not text_reads_disconnected) or
      (tutor_says_inverted and not text_reads_inverted) or
      (tutor_says_sound and (text_reads_disconnected or text_reads_inverted))
    )
    divergence = {"verdict_diverges": bool(verdict) and verdict_diverges}

  observations = []
  observations.append("Claim is articulated." if articulated else "Claim is not articulated yet (fewer than 4 words).")
  position = "before" if before else "after"
  if same_para:
    observations.append(f"Evidence sits in the same paragraph as the claim, positioned {position} it.")
  else:
    observations.append(f"Evidence is {distance} paragraph(s) {position} the claim — not adjacent.")
  if disconnected:
    observations.append("Evidence and claim are disconnected (distance >= 1 paragraph or claim missing).")
  else:
    observations.append("Evidence and claim are tightly placed.")

  done_reasons = []
  if articulated:
    done_reasons.append("claim is articulated")
  if not disconnected:
    done_reasons.append("evidence and claim are not disconnected")
  if same_para or distance <= 1:
    done_reasons.append("evidence sits within one paragraph of the claim")
  done = articulated and (not disconnected) and (same_para or distance <= 1)

  # LLM stub: a semantic check can confirm whether the evidence *actually*
  # supports the claim, which keyword distance cannot, and reconcile the
  # student's read against tutor_pre_read.
  return {
    "claim_articulated": articulated,
    "same_paragraph": same_para,
    "paragraph_distance": distance,
    "evidence_before_claim": before,
    "is_disconnected": disconnected,
    "divergence": divergence,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
