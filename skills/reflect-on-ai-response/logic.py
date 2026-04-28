# logic.py — reflect-on-ai-response
# Surfaces basic diff signals between an AI chatbot's claim and what the
# course material says: length ratio, term overlap, and whether the AI
# answer cites any sources.

import re

SOURCE_PAT = re.compile(r"https?://|www\.|\([12]\d{3}\)|\bet al\b", re.I)

def _terms(text):
  return {w for w in re.findall(r"[a-zA-Z]{4,}", text.lower())}

def run(input):
  """
  :param input: {
    "ai_claim": str,
    "course_claim": str,
    "gaps_named": bool | None,           # has the student named >=1 gap?
    "corrections_named": bool | None,    # has the student named >=1 course-source correction?
    "tutor_pre_read": {                  # tutor's silent assessment (optional)
      "ai_strengths": str | None,
      "ai_gaps": str | None,
      "course_corrections": str | None,
    } | None,
  }
  :return: {
    "has_sources": bool,
    "length_ratio": float,
    "ai_only_terms": list[str],
    "course_only_terms": list[str],
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  Note: divergence is not computed here — comparing free-text gaps to
  pre-read gaps is a semantic call best left to the tutor LLM.
  """
  ai = input.get("ai_claim", "")
  course = input.get("course_claim", "")
  gaps_named = bool(input.get("gaps_named"))
  corrections_named = bool(input.get("corrections_named"))

  ai_terms, course_terms = _terms(ai), _terms(course)
  ratio = (len(ai.split()) / max(1, len(course.split()))) if course else 0.0
  has_sources = bool(SOURCE_PAT.search(ai))
  ai_only = sorted(ai_terms - course_terms)[:10]
  course_only = sorted(course_terms - ai_terms)[:10]

  observations = []
  observations.append("AI claim cites a source." if has_sources else "AI claim cites no source (no URL, year, or 'et al').")
  observations.append(f"AI vs course length ratio: {round(ratio, 2)} (>1 = AI longer).")
  if ai_only:
    observations.append(f"AI-only terms worth verifying: {', '.join(ai_only[:5])}.")
  if course_only:
    observations.append(f"Course-only terms missing from AI claim: {', '.join(course_only[:5])}.")

  done_reasons = []
  if has_sources:
    done_reasons.append("AI claim cites a source")
  if gaps_named and corrections_named:
    done_reasons.append("student named at least one gap and one correction")
  done = has_sources or (gaps_named and corrections_named)

  # LLM stub: semantic diff would catch paraphrased-but-equivalent terms,
  # and could reconcile the student's named gaps against tutor_pre_read.
  return {
    "has_sources": has_sources,
    "length_ratio": round(ratio, 2),
    "ai_only_terms": ai_only,
    "course_only_terms": course_only,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
