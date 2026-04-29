# logic.py — critique-research-design orchestrator
# Top-level state tracker for the POLI SCI 210 research design critique
# assignment. Routes through three phase sub-orchestrators in order, then
# signals handoff to scaffold-written-assignment. Pure function; no side
# effects. Each week maps to a method tag that downstream skills branch on.

WEEK_METHOD = {
  3: ("theory-data",      "Krcmaric, Nelson & Roberts 2024"),
  4: ("inference",        "Rosenzweig & Wilson 2023"),
  5: ("surveys",          "Naunov 2025"),
  6: ("experiments",      "Coppock, Green & Porter 2026"),
  7: ("large-n",          "Harbridge-Yong, Volden & Wiseman 2023"),
  8: ("small-n",          "Gilbert 2022"),
  9: ("machine-learning", "Libgober & Jerzak 2024"),
}

CHAIN = [
  "investigate-reading",
  "extract-research-design",
  "form-critique",
]

HANDOFF = "scaffold-written-assignment"


def run(input):
  """
  :param input: {
    "week": int | None,                       # 3..9; None = needs identification
    "article_path": str | None,
    "completed_phases": list[{
      "phase_id": str,                        # one of CHAIN
      "session_log": str,                     # path to that phase's session log
      "done": bool,                           # phase orchestrator's heuristic gate
      "user_confirmed": bool,                 # student said move on
    }] | None,
    "current_phase": str | None,              # phase currently in dialogue
  }
  :return: {
    "week": int | None,
    "method": str | None,
    "paper_short": str | None,
    "next_phase": str | None,                 # next phase orchestrator to open
    "handoff_target": str | None,             # set when chain complete
    "needs_identification": bool,             # week + article_path not yet resolved
    "needs_user_confirm": bool,               # transition pending student confirm
    "chain_progress": str,                    # e.g. "1 of 3"
    "prior_session_logs": list[str],          # paths to feed into next phase's pre-read
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  if not isinstance(input, dict):
    raise ValueError("input must be a dict")

  week = input.get("week")
  article_path = (input.get("article_path") or "").strip() or None

  if week is None or article_path is None:
    return {
      "week": week,
      "method": None,
      "paper_short": None,
      "next_phase": None,
      "handoff_target": None,
      "needs_identification": True,
      "needs_user_confirm": False,
      "chain_progress": "0 of 3",
      "prior_session_logs": [],
      "done": False,
      "done_reasons": [],
      "observations": [
        "Identification pending: need both week (3-9) and article_path before opening phase 1.",
      ],
    }

  if week not in WEEK_METHOD:
    raise ValueError(
      f"Unknown week: {week!r}. Expected one of {sorted(WEEK_METHOD)}."
    )

  method, paper_short = WEEK_METHOD[week]

  completed = input.get("completed_phases") or []
  if not isinstance(completed, list):
    raise ValueError("completed_phases must be a list")

  for i, entry in enumerate(completed):
    if not isinstance(entry, dict):
      raise ValueError(f"completed_phases[{i}] must be a dict")
    if i >= len(CHAIN):
      raise ValueError(
        f"completed_phases has more entries ({len(completed)}) than chain ({len(CHAIN)})"
      )
    pid = entry.get("phase_id")
    if pid != CHAIN[i]:
      raise ValueError(
        f"completed_phases[{i}].phase_id={pid!r} does not match chain[{i}]={CHAIN[i]!r}"
      )

  n_done = len(completed)
  next_phase = CHAIN[n_done] if n_done < len(CHAIN) else None
  prior_logs = [c.get("session_log") for c in completed if c.get("session_log")]

  current = input.get("current_phase")
  if current is not None and current != next_phase:
    raise ValueError(
      f"current_phase={current!r} does not match expected next phase {next_phase!r} "
      f"given {n_done} completed phase(s)"
    )

  done = next_phase is None
  handoff_target = HANDOFF if done else None

  done_reasons = []
  if done:
    done_reasons.append("all three phase orchestrators are user-confirmed complete")
    done_reasons.append(f"handoff to {HANDOFF} pending student invocation")

  needs_user_confirm = (n_done > 0) and not done

  observations = [
    f"Week: {week} ({paper_short}, {method}).",
    f"Article: {article_path}.",
    f"Completed phases: {n_done} ({', '.join(c.get('phase_id', '?') for c in completed) or 'none'}).",
  ]
  if next_phase:
    observations.append(f"Next phase to open: {next_phase}.")
    if prior_logs:
      observations.append(
        f"Pass prior phase session log(s) into next phase's pre-read: {prior_logs}."
      )
  else:
    observations.append(f"All phases complete. Handoff target: {HANDOFF}.")
  if needs_user_confirm:
    observations.append("Awaiting student confirmation before opening the next phase.")

  return {
    "week": week,
    "method": method,
    "paper_short": paper_short,
    "next_phase": next_phase,
    "handoff_target": handoff_target,
    "needs_identification": False,
    "needs_user_confirm": needs_user_confirm,
    "chain_progress": f"{n_done} of {len(CHAIN)}",
    "prior_session_logs": prior_logs,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
