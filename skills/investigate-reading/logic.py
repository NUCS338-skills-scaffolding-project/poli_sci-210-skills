# logic.py — investigate-reading phase orchestrator
# Phase 1 of critique-research-design. Tracks progress through three granular
# skills (orient, trace, probe) for a single article. Receives week + method
# + article_path from the main orchestrator and threads them downward so each
# granular skill can branch on method. Pure function; no side effects.

CHAIN = [
  "first-pass-orient",
  "trace-claim-to-evidence",
  "probe-author-choices",
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
    "week": int,                              # 3..9
    "method": str,                            # one of VALID_METHODS
    "article_path": str,
    "prior_session_logs": list[str] | None,   # from main orchestrator (empty for Phase 1)
    "completed_skills": list[{
      "skill_id": str,                        # one of CHAIN
      "scratchpad_path": str,
      "done": bool,                           # sub-skill heuristic gate
      "user_confirmed": bool,                 # student said move on
    }] | None,
    "current_skill": str | None,              # skill currently in dialogue
    "preread_dispatched": str | None,         # skill_id of in-flight pre-read
  }
  :return: {
    "next_skill": str | None,                 # next granular skill to open
    "preread_target": str | None,             # skill the subagent should pre-read
    "needs_user_confirm": bool,
    "chain_progress": str,                    # e.g. "1 of 3"
    "downstream_inputs": {                    # to thread into sub-skill calls
      "week": int,
      "method": str,
      "article_path": str,
      "prior_session_logs": list[str],
    },
    "done": bool,                             # phase complete
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
      f"given {n_done} completed skill(s) in the investigate-reading chain"
    )

  preread_dispatched = input.get("preread_dispatched")
  if preread_dispatched is not None and preread_dispatched not in CHAIN:
    raise ValueError(
      f"preread_dispatched={preread_dispatched!r} is not a member of the investigate-reading chain"
    )

  done = next_skill is None
  done_reasons = []
  if done:
    done_reasons.append(f"all {len(CHAIN)} sub-skills are user-confirmed complete")

  needs_user_confirm = (n_done > 0) and not done

  observations = [
    f"Phase: investigate-reading (Phase 1).",
    f"Week: {week}, Method: {method}.",
    f"Article: {article_path}.",
    f"Completed: {n_done} ({', '.join(c.get('skill_id', '?') for c in completed) or 'none'}).",
  ]
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
