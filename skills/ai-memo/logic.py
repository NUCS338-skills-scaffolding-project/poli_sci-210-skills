# logic.py — ai-memo orchestrator
# Pure-function chain state tracker for the AI memo workflow. Given the
# current chain state, returns what skill to open next, what skill the
# pre-read subagent should target, and whether the orchestration is done.
# No side effects.

CHAIN = [
  "pick-week-concept",
  "ai-explain",
  "eval-ai-response",
  "scaffold-writing",
]


INPUT_SCHEMA: dict = {
    "completed_skills": "list | None",
    "current_skill": "str | None",
    "preread_dispatched": "str | None",
    "rubric_followups_met": "bool | None",
}


def run(input):
  """
  :param input: {
    "completed_skills": list[{
      "skill_id": str,
      "scratchpad_path": str,
      "done": bool,                              # sub-skill heuristic gate
      "user_confirmed": bool,                    # user said "ready to move on"
    }] | None,
    "current_skill": str | None,                 # skill currently in dialogue
    "preread_dispatched": str | None,            # skill_id of in-flight pre-read
    "rubric_followups_met": bool | None,         # informational: did ai-explain hit 5+?
  }
  :return: {
    "next_skill": str | None,                    # next skill to open in dialogue
    "preread_target": str | None,                # skill the subagent should pre-read
    "needs_user_confirm": bool,                  # transition pending user confirm
    "needs_mode_banner": str | None,             # "tutor->ai" | "ai->tutor" | None
    "chain_progress": str,                       # e.g. "2 of 4"
    "done": bool,                                # whole orchestration complete
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  if not isinstance(input, dict):
    raise ValueError("input must be a dict")

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
      f"given {n_done} completed skill(s) in chain"
    )

  preread_dispatched = input.get("preread_dispatched")
  if preread_dispatched is not None and preread_dispatched not in CHAIN:
    raise ValueError(
      f"preread_dispatched={preread_dispatched!r} is not a member of the chain"
    )

  # Mode banner is needed at the boundaries of ai-explain.
  # Boundary 1: opening ai-explain (tutor → ai).
  # Boundary 2: closing ai-explain / opening eval-ai-response (ai → tutor).
  needs_mode_banner = None
  if next_skill == "ai-explain":
    needs_mode_banner = "tutor->ai"
  elif next_skill == "eval-ai-response":
    needs_mode_banner = "ai->tutor"

  done = next_skill is None
  done_reasons = []
  if done:
    done_reasons.append(f"all {len(CHAIN)} skills in chain are complete")

  needs_user_confirm = (n_done > 0) and not done

  observations = [
    f"Chain length: {len(CHAIN)} skill(s).",
    f"Completed: {n_done} ({', '.join(c.get('skill_id', '?') for c in completed) or 'none'}).",
  ]
  if next_skill:
    observations.append(f"Next skill to open in dialogue: {next_skill}.")
  else:
    observations.append("Chain complete — no further skills to open.")
  if preread_target:
    observations.append(f"Pre-read target for subagent: {preread_target}.")
  else:
    observations.append("No pre-read target — last skill in chain or chain complete.")
  if needs_mode_banner:
    observations.append(
      f"Mode banner required before opening next skill: {needs_mode_banner}."
    )
  if needs_user_confirm:
    observations.append("Awaiting user confirmation before opening the next skill.")

  rubric_met = input.get("rubric_followups_met")
  if rubric_met is False:
    observations.append(
      "Note: ai-explain closed without hitting the 5-follow-up rubric minimum. "
      "Surface this in the session log synthesis."
    )

  return {
    "next_skill": next_skill,
    "preread_target": preread_target,
    "needs_user_confirm": needs_user_confirm,
    "needs_mode_banner": needs_mode_banner,
    "chain_progress": f"{n_done} of {len(CHAIN)}",
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
