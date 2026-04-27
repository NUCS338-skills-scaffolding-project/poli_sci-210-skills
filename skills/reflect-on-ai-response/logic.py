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
  :param input: {"ai_claim": str, "course_claim": str}
  :return: {
    "has_sources": bool,
    "length_ratio": float,
    "ai_only_terms": list[str],
    "course_only_terms": list[str],
  }
  """
  ai = input.get("ai_claim", "")
  course = input.get("course_claim", "")
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

  # LLM stub: semantic diff would catch paraphrased-but-equivalent terms.
  return {
    "has_sources": has_sources,
    "length_ratio": round(ratio, 2),
    "ai_only_terms": ai_only,
    "course_only_terms": course_only,
    "observations": observations,
  }
