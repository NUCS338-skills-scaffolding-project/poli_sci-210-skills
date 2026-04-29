# logic.py — analyze-writing orchestrator
# Pure-function state tracker for a chain of writing skills run against a
# single artifact. Given the current chain state, returns what skill (if any)
# to open next, what skill the pre-read subagent should target, and whether
# the orchestration is complete. No side effects.

DRAFT_CHAIN = [
  "argument-decomposition",
  "logical-flow-testing",
  "evidence-placement-review",
  "reasoning-evaluation",
  "cohesion-strengthening",
]

PLAN_CHAIN = [
  "argument-decomposition",
  "scaffold-written-assignment",
]

VALID_MODES = ("plan", "draft")


def _chain_for(mode):
  if mode == "plan":
    return PLAN_CHAIN
  if mode == "draft":
    return DRAFT_CHAIN
  raise ValueError(f"Unknown mode: {mode!r}. Expected 'plan' or 'draft'.")


def run(input):
  """
  :param input: {
    "mode": "plan" | "draft" | None,             # None = needs classification
    "writing_path": str,
    "completed_skills": list[{
      "skill_id": str,
      "scratchpad_path": str,
      "done": bool,                              # sub-skill heuristic gate
      "user_confirmed": bool,                    # user said "ready to move on"
    }] | None,
    "current_skill": str | None,                 # skill currently in dialogue
    "preread_dispatched": str | None,            # skill_id of in-flight pre-read
  }
  :return: {
    "next_skill": str | None,                    # next skill to open in dialogue
    "preread_target": str | None,                # skill the subagent should pre-read
    "needs_mode_classification": bool,
    "needs_user_confirm": bool,                  # transition pending user confirm
    "chain_progress": str,                       # e.g. "2 of 5"
    "done": bool,                                # whole orchestration complete
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  if not isinstance(input, dict):
    raise ValueError("input must be a dict")

  writing_path = (input.get("writing_path") or "").strip()
  if not writing_path:
    raise ValueError("writing_path is required and must be a non-empty string")

  mode = input.get("mode")

  if mode is None:
    return {
      "next_skill": None,
      "preread_target": None,
      "needs_mode_classification": True,
      "needs_user_confirm": False,
      "chain_progress": "0 of ?",
      "done": False,
      "done_reasons": [],
      "observations": [
        f"Mode not yet classified for {writing_path!r}.",
        "Read the artifact, propose 'plan' or 'draft', and ask the user to confirm.",
      ],
    }

  if mode not in VALID_MODES:
    raise ValueError(f"Unknown mode: {mode!r}. Expected 'plan' or 'draft'.")

  chain = _chain_for(mode)

  completed = input.get("completed_skills") or []
  if not isinstance(completed, list):
    raise ValueError("completed_skills must be a list")

  for i, entry in enumerate(completed):
    if not isinstance(entry, dict):
      raise ValueError(f"completed_skills[{i}] must be a dict")
    if i >= len(chain):
      raise ValueError(
        f"completed_skills has more entries ({len(completed)}) than chain ({len(chain)}) for mode={mode!r}"
      )
    sid = entry.get("skill_id")
    if sid != chain[i]:
      raise ValueError(
        f"completed_skills[{i}].skill_id={sid!r} does not match chain[{i}]={chain[i]!r}"
      )

  n_done = len(completed)
  next_skill = chain[n_done] if n_done < len(chain) else None
  preread_target = chain[n_done + 1] if (n_done + 1) < len(chain) else None

  current = input.get("current_skill")
  if current is not None and current != next_skill:
    raise ValueError(
      f"current_skill={current!r} does not match expected next skill {next_skill!r} "
      f"given {n_done} completed skill(s) in {mode}-mode chain"
    )

  preread_dispatched = input.get("preread_dispatched")
  if preread_dispatched is not None and preread_dispatched not in chain:
    raise ValueError(
      f"preread_dispatched={preread_dispatched!r} is not a member of the {mode}-mode chain"
    )

  done = next_skill is None
  done_reasons = []
  if done:
    done_reasons.append(f"all {len(chain)} skills in {mode}-mode chain are complete")

  needs_user_confirm = (n_done > 0) and not done

  observations = [
    f"Mode: {mode}.",
    f"Chain length: {len(chain)} skill(s).",
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
  if needs_user_confirm:
    observations.append("Awaiting user confirmation before opening the next skill.")

  return {
    "next_skill": next_skill,
    "preread_target": preread_target,
    "needs_mode_classification": False,
    "needs_user_confirm": needs_user_confirm,
    "chain_progress": f"{n_done} of {len(chain)}",
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
