# analyze-writing — orchestrator skill design

**Date**: 2026-04-28
**Status**: design approved, awaiting implementation plan
**Lives at**: `skills/analyze-writing/` (project-local, alongside the writing skills it orchestrates)

## Problem

The six writing skills in `skills/` (`argument-decomposition`, `cohesion-strengthening`, `evidence-placement-review`, `logical-flow-testing`, `reasoning-evaluation`, `scaffold-written-assignment`) are designed for tutor-student dialogue: each runs its own flow, scaffolds with questions, and gates on a heuristic + narrative override. They are atomic — none of them coordinates with another.

For a writing assignment or a draft revision, a student needs *several* of these skills run in sequence. Doing this manually requires the student or tutor to:
- Decide which skills apply.
- Pick a sensible order.
- Open each skill in turn, dispatching the tutor's silent pre-read each time.
- Track findings across skills so revisions are coherent.

This is friction the student shouldn't have to manage. The first attempt at running all six against a paper in the prior session ran them in *analyst monologue* mode (Claude doing the analysis without the student) — which produced six scratchpads but bypassed the pedagogy entirely.

## Goal

A new project skill, `analyze-writing`, that:

1. Takes a writing artifact (path) as input.
2. Auto-classifies it as **plan mode** (no draft yet, or only an outline) or **draft mode** (revising existing prose), confirming with the user.
3. Walks the user through the appropriate skill chain in dialogue.
4. Hides per-skill pre-read latency by dispatching a subagent to pre-read skill N+1 the moment skill N opens.
5. Tracks completion across the chain via each sub-skill's `logic.py` heuristic gate, the tutor's narrative override, and an explicit user confirm.
6. Produces a session log with a ranked synthesis of findings across all skills.

## Out of scope

- Resuming an interrupted session across days. (Session log preserves state, but the resume flow itself is v2.)
- Modifying or extending the six existing skills. They are taken as-is.
- A genre-aware variant of `scaffold-written-assignment` or `logical-flow-testing` (both currently calibrated for the POLI SCI 210 design-critique flow). Genre fit is a known limitation; the orchestrator just routes to them as-is.
- Mocked subagent dispatch in tests. The `Agent` tool is a Claude Code primitive; testing its dispatch is covered by manual conversational testing.

## Decisions (with rationale)

| # | Decision | Rationale |
|---|---|---|
| 1 | Skill home: `skills/analyze-writing/` | Project-local, conventions match. Co-located with the skills it orchestrates so it ships with the course materials. |
| 2 | Mode classification: auto-classify, then confirm | Lower friction in the common case; confirm preserves user control when the input is ambiguous. |
| 3 | Draft chain order: argument-decomposition → logical-flow-testing → evidence-placement-review → reasoning-evaluation → cohesion-strengthening | Top-down (structure → joints → prose). Predictable and matches how a writer rebuilds. argument-decomposition first because every later skill needs the thesis/main-claim hierarchy named. |
| 4 | Plan chain order: argument-decomposition → scaffold-written-assignment | Thesis-first matches strong-writing practice. Decompose the *target* argument before scaffolding the sections that deliver it. |
| 5 | Pre-read timing: dispatch subagent the moment current skill opens | Maximum latency hide; small token overhead; fails gracefully (one stale pre-read at most if user changes course). |
| 6 | Completion: heuristic gate ∨ narrative override, then user confirm | Matches each sub-skill's own completion criteria. User confirm prevents runaway transitions. |
| 7 | Output: per-skill scratchpads + orchestrator session log + final synthesis | Per-skill files preserve depth; session log gives a single place for a ranked punch list of revision targets. Synthesis appended incrementally as each skill completes. |

## Architecture

```
                              ┌─────────────────┐
   user invokes  ────────────▶│   orchestrator  │
   /analyze-writing PATH      │   skills.md     │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │ auto-classify   │ ──▶ confirm with user
                              │ mode (logic.py) │
                              └────────┬────────┘
                                       │
                          plan ◀───────┴───────▶ draft
                          chain               chain
                          (2 skills)         (5 skills)
                                       │
                                       ▼
                          ┌────────────────────────────────────┐
                          │  for each skill in chain:           │
                          │    • dispatch subagent for skill+1  │
                          │      (pre-read; background)         │
                          │    • run skill in dialogue          │
                          │    • check gate (logic.py.done)     │
                          │    • check narrative override       │
                          │    • ask user "ready to move on?"   │
                          │    • append to synthesis log        │
                          └────────────────────────────────────┘
                                       │
                                       ▼
                          orchestrator session log + synthesis
```

The orchestrator produces no prose advice itself. It routes Claude into each sub-skill, which retains full ownership of its own pedagogy.

## Components

### `skills/analyze-writing/skills.md`

Same template as every other skill. The `Flow` section walks Claude through:

1. Read the writing artifact at the supplied path.
2. Call `logic.py` with `mode=None`. If `needs_mode_classification`, scan the artifact for structural signals (paragraphs/footnotes/length/headings → draft; outline-only or assignment-prompt-shaped → plan), propose the verdict, ask user to confirm.
3. Call `logic.py` with the confirmed mode to get `next_skill` (the first skill in the chain).
4. Open the first skill in dialogue. (No pre-read subagent needed yet — there's no prior conversation to hide latency from.)
5. Enter the chain loop:
   - On opening skill N (where N > 1), the orchestrator already has the pre-read scratchpad written by the subagent during skill N-1.
   - At the same turn the skill opens, dispatch a new Agent subagent to pre-read skill N+1 (background).
   - Run the sub-skill flow in dialogue per its own `skills.md`.
   - When `logic.py.done = True` *or* tutor narrative override fires, ask user "ready to move to <next skill>?"
   - On confirm: append a Synthesis entry to the orchestrator session log. Call orchestrator `logic.py` with skill N marked complete. Read the next skill's pre-read scratchpad. Continue.
6. When the orchestrator's `logic.py` returns `done=True`, finalize the Synthesis block (ranked punch list across all skills), report to the user, and exit.

### `skills/analyze-writing/logic.py`

Pure-function state tracker. Single `run()` returning what to do next.

```python
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

def run(input):
    """
    :param input: {
        "mode": "plan" | "draft" | None,            # None = needs classification
        "writing_path": str,
        "completed_skills": list[{
            "skill_id": str,
            "scratchpad_path": str,
            "done": bool,
            "user_confirmed": bool,
        }],
        "current_skill": str | None,
        "preread_dispatched": str | None,            # skill_id of in-flight pre-read
    }
    :return: {
        "next_skill": str | None,                    # next skill to open in dialogue
        "preread_target": str | None,                # skill the subagent should pre-read
        "needs_mode_classification": bool,
        "needs_user_confirm": bool,                  # for transitions
        "chain_progress": str,                       # e.g. "2 of 5"
        "done": bool,                                # whole orchestration complete
        "done_reasons": list[str],
        "observations": list[str],
    }
    """
```

Validates inputs and raises `ValueError` on invalid state (unknown mode, mismatched `current_skill`, etc.). No silent recovery.

### `skills/analyze-writing/scratch/<timestamp>-<student>-session.md`

One file per orchestration run. Sections:

- **Header**: timestamp, student, mode, writing path, chain (which skills, in what order).
- **Per-skill blocks** (appended as each skill runs): skill_id, scratchpad link, done state (gate vs. override), user-confirmed timestamp, 2-4 line key-findings excerpt copied from the sub-skill's Completion Notes.
- **Synthesis** (appended-to incrementally, finalized at exit): ranked punch list of revision targets across the chain. The ranking is by leverage — biggest revision payoff first. This is the user's actual deliverable.

### Sub-skill scratchpads

Unchanged. Each sub-skill writes to its own conventional path (`skills/<skill>/scratch/<timestamp>-<student>-notes.md`). The orchestrator session log links to each.

### Pre-read subagent dispatch

Invoked via the `Agent` tool with `run_in_background=true` and a self-contained prompt:

- Path to the writing artifact.
- Path to the next skill's `skills.md`.
- Paths to scratchpads of all completed sub-skills (so the pre-read can build on prior findings — e.g., the reasoning-evaluation pre-read knows which warrants the argument-decomposition step surfaced).
- Instruction: produce the next skill's pre-read scratchpad at the conventional path. Do not engage the user. Return when done.

The subagent runs in the background while the user works through the prior skill. The orchestrator reads the produced scratchpad when it's time to open that next skill in dialogue.

## Data flow (end-to-end, draft mode)

| Time | Event |
|---|---|
| T0 | User: `analyze-writing students/bryan/submissions/X.pdf`. Claude reads `skills.md`, runs `logic.py` with `mode=None`. Output: `needs_mode_classification=True`. |
| T1 | Claude reads artifact, classifies as `draft`, asks user to confirm. User confirms. `logic.py` returns `next_skill="argument-decomposition", preread_target=None` (first skill, no pre-read needed). |
| T2 | Claude does its own pre-read for skill 1 synchronously, opens dialogue. *Same turn*: dispatches Agent subagent to pre-read skill 2 in background. |
| T3 | Tutor-user dialogue through skill 1. Each turn re-reads/updates skill 1 scratchpad. When `done = True` or override fires, Claude asks: "Ready to move to logical-flow-testing?" |
| T4 | User confirms. Claude calls `logic.py` with skill 1 complete. Output: `next_skill="logical-flow-testing", preread_target="evidence-placement-review"`. Appends Synthesis entry to session log. Reads skill 2's pre-read scratchpad. Opens skill 2 *and* dispatches subagent for skill 3. |
| T5-T8 | Skills 2-5 follow the same pattern. Pre-read subagent for skill N receives scratchpads from skills 1..N-1. |
| T9 | Skill 5 completes. `logic.py` returns `done=True, next_skill=None`. Claude finalizes Synthesis (ranked punch list), reports to user. |

The pre-read latency hide: each subagent runs while the user spends ~5-15 turns inside the prior skill. Subagent finish times are well within that window in practice.

## Error handling

| Failure | Response |
|---|---|
| Mode classifier picks wrong | Confirm step at T1 catches it. User overrides. No re-work. |
| Sub-skill heuristic gate never flips | Narrative override handles most cases. If user *also* doesn't confirm transition, orchestrator stays in the skill. If user explicitly says "skip," orchestrator records `skipped` (not `done`), notes it in the synthesis, moves on. |
| Pre-read subagent fails / produces malformed scratchpad | Claude does the pre-read synchronously when opening that skill. Session log notes the fallback. ~few seconds latency at handoff. |
| Pre-read subagent still running at handoff | Orchestrator waits on the in-flight task. Status update to user if wait > 30 seconds. No corruption risk. |
| User abandons mid-chain | Orchestrator finalizes synthesis with whatever's complete, notes which skills ran and which didn't, exits cleanly. Session log preserves state for v2 resume. |

The orchestrator does not silently recover from corrupted state, missing files, or invalid arguments. `logic.py` raises `ValueError`; surface it.

## Testing

**`logic.py` unit tests** (deterministic, fast):
- Mode classification given different `mode` inputs (None, "plan", "draft", invalid).
- Chain advancement: empty → first; one done → second; full → `done=True`.
- Pre-read targeting: always `chain[current_index + 1]` or None at end of chain.
- Edge cases: invalid mode, mismatched `current_skill` vs `completed_skills`, empty `writing_path`.

YAML scenarios live at `demos/scenarios/analyze-writing/` and run via a small extension of `demos/run_skill.py` (or a sibling script).

**End-to-end orchestrator dry-run**:
- One scripted scenario per mode (`02-orchestrator-draft.yaml`, `03-orchestrator-plan.yaml`).
- Walks `logic.py` through a full chain with mocked completion signals.
- Verifies right `next_skill` and `preread_target` at each step.
- Does not exercise real Agent dispatch (needs Claude Code).

**Conversational testing** (manual, the actual acceptance test):
- Invoke orchestrator on a real paper.
- Confirm mode classification works on plan-mode and draft-mode inputs.
- Walk through both chains end-to-end.
- Verify pre-read scratchpads land on time.
- Verify synthesis aggregates findings sensibly.

No subagent-mocking layer. YAGNI; covered by manual testing.

## Acceptance criteria

The orchestrator is done when:

1. `skills/analyze-writing/skills.md` and `logic.py` exist and follow the project's skill template.
2. `logic.py` unit tests pass for all cases listed under Testing.
3. Two YAML scenarios under `demos/scenarios/analyze-writing/` walk both chains successfully.
4. Manual conversational test: orchestrator runs end-to-end on `students/bryan/submissions/Foreign Policy Research Paper.pdf` in draft mode, opens each of the five sub-skills in dialogue, dispatches pre-read subagents on schedule, produces a session log with a meaningful ranked synthesis.

## Open questions for implementation plan

- Exact prompt format for the pre-read subagent (probably codified in `skills.md` so Claude assembles it consistently each turn).
- Whether the synthesis ranking is heuristic (skill order × done_reasons), Claude-judgment, or both.
- File-naming convention if the same student runs the orchestrator multiple times in one day (currently `<HHMM>` granularity in timestamp; collisions unlikely but possible).

These are not blockers for the design — they're decisions to make during planning.
