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
  # LLM stub: semantic diff would catch paraphrased-but-equivalent terms.
  return {
    "has_sources": bool(SOURCE_PAT.search(ai)),
    "length_ratio": round(ratio, 2),
    "ai_only_terms": sorted(ai_terms - course_terms)[:10],
    "course_only_terms": sorted(course_terms - ai_terms)[:10],
  }
