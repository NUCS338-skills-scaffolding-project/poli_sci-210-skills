# logic.py — first-pass-orient
# Granular skill in Phase 1 (investigate-reading). Tracks whether the student
# has produced a clean one-sentence puzzle and one-sentence answer in their
# own words. Pure function; no side effects.

VALID_METHODS = (
  "theory-data",
  "inference",
  "surveys",
  "experiments",
  "large-n",
  "small-n",
  "machine-learning",
)

MAX_SENTENCE_WORDS = 30
TOPIC_RESTATEMENT_CUES = ("they study", "this paper studies", "this paper is about", "they look at")


def _word_count(s):
  return len(s.split())


def _looks_like_topic_restatement(s):
  s_low = s.lower().strip()
  return any(s_low.startswith(c) for c in TOPIC_RESTATEMENT_CUES)


def run(input):
  """
  :param input: {
    "week": int,
    "method": str,
    "article_path": str,
    "prior_session_logs": list[str] | None,    # from main orchestrator (empty for Phase 1)
    "puzzle": str | None,                      # student's one-sentence puzzle
    "answer": str | None,                      # student's one-sentence answer
    "abstract_overlap_high": bool | None,      # heuristic flag from tutor (or LLM stub)
  }
  :return: {
    "puzzle_ok": bool,
    "answer_ok": bool,
    "next_prompt": str,                        # which step the tutor should run next
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

  puzzle = (input.get("puzzle") or "").strip()
  answer = (input.get("answer") or "").strip()
  parrot = bool(input.get("abstract_overlap_high"))

  puzzle_ok = bool(puzzle) and _word_count(puzzle) <= MAX_SENTENCE_WORDS and not parrot
  answer_ok = (
    bool(answer)
    and _word_count(answer) <= MAX_SENTENCE_WORDS
    and not parrot
    and not _looks_like_topic_restatement(answer)
  )

  if not puzzle:
    next_prompt = "ask_puzzle"
  elif not puzzle_ok:
    next_prompt = "redo_puzzle"
  elif not answer:
    next_prompt = "ask_answer"
  elif not answer_ok:
    next_prompt = "redo_answer"
  else:
    next_prompt = "reconcile_and_exit"

  done = puzzle_ok and answer_ok
  done_reasons = []
  if puzzle_ok:
    done_reasons.append("puzzle is one short sentence and not abstract-parroting")
  if answer_ok:
    done_reasons.append("answer is one short sentence, not parroting, not a topic restatement")

  observations = [
    f"Method: {method}.",
    f"Puzzle: {'present' if puzzle else 'missing'}{' (over length)' if puzzle and _word_count(puzzle) > MAX_SENTENCE_WORDS else ''}.",
    f"Answer: {'present' if answer else 'missing'}{' (over length)' if answer and _word_count(answer) > MAX_SENTENCE_WORDS else ''}.",
  ]
  if parrot:
    observations.append("Abstract-overlap flag is HIGH — student is parroting the abstract.")
  if answer and _looks_like_topic_restatement(answer):
    observations.append("Answer reads as a topic restatement, not a finding ('they study...').")
  observations.append(f"Next tutor move: {next_prompt}.")

  # LLM stub: a semantic check would compare puzzle/answer against the
  # abstract for paraphrased parroting (rather than verbatim overlap), and
  # would also verify the answer names a finding rather than a topic.
  return {
    "puzzle_ok": puzzle_ok,
    "answer_ok": answer_ok,
    "next_prompt": next_prompt,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
