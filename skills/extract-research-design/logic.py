# logic.py — extract-research-design phase orchestrator
# Phase 2 of critique-research-design. Tracks progress through three granular
# skills (skeleton, operationalization, alignment) for a single article.
# Receives week + method + article_path + prior_session_logs from the main
# orchestrator and threads them downward. Pure function; no side effects.

CHAIN = [
  "design-skeleton",
  "operationalization-check",
  "method-week-alignment",
]

VALID_METHODS = (
  "theory-data",
  "inference",
  "surveys",
  "experiments",
  "large-n",
  "small-n",
  "machine-learning",
)


def run(input):
  """
  :param input: {
    "week": int,
    "method": str,
    "article_path": str,
    "prior_session_logs": list[str] | None,   # main orchestrator passes [Phase 1 log]
    "completed_skills": list[{
      "skill_id": str,
      "scratchpad_path": str,
      "done": bool,
      "user_confirmed": bool,
    }] | None,
    "current_skill": str | None,
    "preread_dispatched": str | None,
  }
  :return: {
    "next_skill": str | None,
    "preread_target": str | None,
    "needs_user_confirm": bool,
    "chain_progress": str,
    "downstream_inputs": {
      "week": int,
      "method": str,
      "article_path": str,
      "prior_session_logs": list[str],
    },
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  if not isinstance(input, dict):
    raise ValueError("input must be a dict")

  week = input.get("week")
  method = input.get("method")
  article_path = (input.get("article_path") or "").strip()
  prior_logs = input.get("prior_session_logs") or []

  if not isinstance(week, int):
    raise ValueError("week is required and must be an int (3-9)")
  if method not in VALID_METHODS:
    raise ValueError(f"method={method!r} must be one of {VALID_METHODS}")
  if not article_path:
    raise ValueError("article_path is required and must be a non-empty string")
  if not isinstance(prior_logs, list):
    raise ValueError("prior_session_logs must be a list")
  if len(prior_logs) < 1:
    # Phase 2 always runs after Phase 1; missing the Phase 1 log is a contract
    # violation from the main orchestrator. Allow it but flag.
    pass

  completed = input.get("completed_skills") or []
  if not isinstance(completed, list):
    raise ValueError("completed_skills must be a list")

  for i, entry in enumerate(completed):
    if not isinstance(entry, dict):
      raise ValueError(f"completed_skills[{i}] must be a dict")
    if i >= len(CHAIN):
      raise ValueError(
        f"completed_skills has more entries ({len(completed)}) than chain ({len(CHAIN)})"
      )
    sid = entry.get("skill_id")
    if sid != CHAIN[i]:
      raise ValueError(
        f"completed_skills[{i}].skill_id={sid!r} does not match chain[{i}]={CHAIN[i]!r}"
      )

  n_done = len(completed)
  next_skill = CHAIN[n_done] if n_done < len(CHAIN) else None
  preread_target = CHAIN[n_done + 1] if (n_done + 1) < len(CHAIN) else None

  current = input.get("current_skill")
  if current is not None and current != next_skill:
    raise ValueError(
      f"current_skill={current!r} does not match expected next skill {next_skill!r} "
      f"given {n_done} completed skill(s) in the extract-research-design chain"
    )

  preread_dispatched = input.get("preread_dispatched")
  if preread_dispatched is not None and preread_dispatched not in CHAIN:
    raise ValueError(
      f"preread_dispatched={preread_dispatched!r} is not a member of the extract-research-design chain"
    )

  done = next_skill is None
  done_reasons = []
  if done:
    done_reasons.append(f"all {len(CHAIN)} sub-skills are user-confirmed complete")

  needs_user_confirm = (n_done > 0) and not done

  observations = [
    f"Phase: extract-research-design (Phase 2).",
    f"Week: {week}, Method: {method}.",
    f"Article: {article_path}.",
    f"Prior phase logs: {len(prior_logs)} ({prior_logs or 'none'}).",
    f"Completed: {n_done} ({', '.join(c.get('skill_id', '?') for c in completed) or 'none'}).",
  ]
  if len(prior_logs) < 1:
    observations.append(
      "WARNING: no prior phase logs supplied — Phase 2 expects Phase 1's session log."
    )
  if next_skill:
    observations.append(f"Next sub-skill to open: {next_skill}.")
  else:
    observations.append("Phase complete — no further sub-skills.")
  if preread_target:
    observations.append(f"Pre-read target for subagent: {preread_target}.")
  else:
    observations.append("No pre-read target — last sub-skill in chain or phase complete.")
  if needs_user_confirm:
    observations.append("Awaiting student confirmation before opening the next sub-skill.")

  return {
    "next_skill": next_skill,
    "preread_target": preread_target,
    "needs_user_confirm": needs_user_confirm,
    "chain_progress": f"{n_done} of {len(CHAIN)}",
    "downstream_inputs": {
      "week": week,
      "method": method,
      "article_path": article_path,
      "prior_session_logs": prior_logs,
    },
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
