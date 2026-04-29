---
skill_id: "investigate-reading"
name: "Investigate Reading"
skill_type: "instructional"
tags: ["research-design", "methods", "reading", "orchestrator", "phase"]
python_entry: "logic.py"
---

# Investigate Reading

## Description
Phase 1 sub-orchestrator of `critique-research-design`. Walks the student through three granular skills — `first-pass-orient` → `trace-claim-to-evidence` → `probe-author-choices` — to make sure they actually grasp what the paper does *before* mapping its design or forming a critique. Hides per-skill pre-read latency by dispatching subagents in the background. Produces a phase session log whose Synthesis is consumed by Phase 2 (`extract-research-design`) as cross-phase context.

## When to Trigger
- The main orchestrator (`critique-research-design`) opens this phase as Phase 1 of the chain.
- Direct invocation: a student says "help me get oriented to this paper" or "I read it but I'm not sure I got what they're doing."
- Not for forming a critique — that's Phase 3. Investigation is grasp, not judgment.

## Tutor Stance
- This skill produces no methodological judgments itself. It routes the student into granular sub-skills that each teach one move.
- One sub-skill at a time, in order. Don't surface findings from later skills while the student is in an earlier one.
- The student stays in dialogue throughout — never run sub-skills as silent analyst monologue.
- Critique-shaped observations are out of scope here even if the student tries to jump ahead. Acknowledge and redirect: "park that for Phase 3."
- Trust each sub-skill's own completion criteria (heuristic gate ∨ narrative override). Then ask "ready to move on?" before transitioning.
- Be concise at this layer. The granular skills handle the teaching.

## Tutor Pre-Read & Notes
The phase orchestrator's pre-read is light: confirm the article is readable at the supplied path, scan its abstract + section headings + figure list to log a shape header, and decide which granular skill is likely to need the most weight (e.g., if the abstract already states puzzle and answer cleanly, `first-pass-orient` may fly through).

Do NOT read the article deeply or form your own critique kernel at this layer — that pollutes later phases. The substantive pre-reads happen at the granular-skill level via subagents.

Write the phase session log to:

```
skills/investigate-reading/scratch/<YYYY-MM-DD-HHMM>-<student>-session.md
```

Structure:
```
# investigate-reading — <student> — <timestamp>

## Phase header
- article_path: <path>
- week: <int>
- method: <theory-data | inference | surveys | experiments | large-n | small-n | machine-learning>
- paper_short: <e.g., "Krcmaric et al. 2024">
- prior_session_logs: []        # empty for Phase 1
- chain: [first-pass-orient, trace-claim-to-evidence, probe-author-choices]
- shape_scan: <2–4 lines: rough length, section headings, figure/table count, anything notable>

## Per-skill blocks
### <skill_id>
- scratchpad: <path>
- done: <true | false> (heuristic gate ∨ narrative override ∨ user-skipped)
- user_confirmed_at: <YYYY-MM-DD-HHMM>
- key findings (2–4 lines copied from the sub-skill's Completion Notes):
  - ...

(repeat for each skill as it completes)

## Synthesis
Phase 1 deliverable — the student's working grasp of the paper. Consumed by Phase 2.
- puzzle: <one sentence — what's the paper asking>
- answer: <one sentence — what does the paper claim/find>
- headline_claim: <one sentence — the central empirical finding the paper most wants you to believe>
- evidence_locus: <Table N | Figure N | Section X.Y | page Y — where the claim is shown>
- claim_evidence_match: <tight | loose | suspicious gap>
- non-trivial choices: <2–3 design choices the authors made that have plausible alternatives>
```

Append per-skill blocks as each granular skill completes; finalize the Synthesis at the end. Re-read this log each turn to stay anchored.

## Flow

### Step 1 — Open the phase
Read the article at `article_path` for shape only (abstract, section headings, figure list — not deep reading). Write the phase session log header, including the shape_scan. Call `logic.py` with `completed_skills=[]` to confirm the chain.

Tell the student briefly what's coming: "We'll go through three quick skills to make sure you're oriented before we dig into the design. First — `first-pass-orient`: what's the puzzle and what's the answer? Then we trace the headline claim back to its evidence. Then we probe two or three design choices that aren't trivial. One at a time."

### Step 2 — Open the first skill (synchronous pre-read)
For `first-pass-orient`, do the pre-read synchronously:
1. Read `skills/first-pass-orient/skills.md` and follow its **Tutor Pre-Read & Notes** section to produce its scratchpad. Pass `week`, `method`, `article_path`, and `prior_session_logs` as inputs to its pre-read.
2. Open the skill in dialogue per its own Flow.

At the same turn, dispatch the pre-read subagent for `trace-claim-to-evidence` (Step 3). This is the only place the phase orchestrator does a synchronous pre-read; for skills 2 and 3 the pre-read is already on disk by the time we open them.

### Step 3 — Dispatch pre-read subagent for skill N+1
Whenever a sub-skill N opens for dialogue, dispatch a subagent in parallel to produce skill N+1's pre-read scratchpad. Use `Agent` tool with `subagent_type=general-purpose` and `run_in_background=true`. Prompt template:

```
You are doing a silent pre-read for the granular skill `<NEXT_SKILL_ID>` in
the investigate-reading phase of a POLI SCI 210 research design critique.

Inputs:
- Article: <ABSOLUTE_PATH_TO_ARTICLE>
- Week: <WEEK>     Method: <METHOD>     Paper: <PAPER_SHORT>
- Skill spec (read this first): <ABSOLUTE_PATH_TO_NEXT_SKILL_SKILLS_MD>
- Prior phase session logs (from main orchestrator; empty for Phase 1):
  - <PATH or "none">
- Prior sub-skill scratchpads in this phase (so your pre-read builds on what
  has already been surfaced — do not re-do their work):
  - <ABSOLUTE_PATH_TO_PRIOR_SCRATCHPAD_1>
  - ...

Task:
1. Read the skill spec and follow its "Tutor Pre-Read & Notes" section
   verbatim to form your own canonical answer for THIS article at THIS skill's
   level (the orient, the claim trace, or the choice probe — whatever the
   skill calls for). Method-aware: focus on what's load-bearing for a
   <METHOD>-style paper.
2. Write the pre-read scratchpad at the conventional path the skill spec
   gives. Use the exact section headings the spec specifies.
3. Do NOT engage the user. Do NOT modify any other files. Return a one-line
   confirmation with the path you wrote.

Constraints:
- Silent pre-read only.
- Build on prior scratchpads where relevant. For example, the
  trace-claim-to-evidence pre-read should know which puzzle/answer the
  first-pass-orient step surfaced.
- Stay within Phase 1 scope: orientation moves only, no critique.
```

Substitute the absolute paths and the next skill's id. Do not block on the subagent — fire it and continue.

### Step 4 — Run the sub-skill in dialogue
Hand off to the sub-skill's Flow. Re-read its scratchpad each turn. The student works through it the same way they would if they had invoked the skill directly. The sub-skill's `logic.py` receives `week`, `method`, `article_path`, and `prior_session_logs` so it can branch on method.

When the sub-skill's `logic.py` returns `done=True`, OR you fire the narrative override, do at the natural end of that turn:
1. Write the Completion Notes block in the sub-skill's scratchpad per its spec.
2. Ask the student: "Ready to move to `<NEXT_SKILL_ID>`?" (or "Phase 1 done — ready to head into design mapping?" if this was the last sub-skill).

If the student isn't ready, stay. If they say "skip," record `done=False, user_confirmed=True` and advance. A skipped sub-skill weakens the next pre-read since the prior scratchpad is thinner.

### Step 5 — Append per-skill block + advance
Once the student confirms the transition:
1. Append a per-skill block to the phase session log: skill_id, scratchpad path, done state, user_confirmed timestamp, 2–4 line key-findings excerpt copied from the sub-skill's Completion Notes.
2. Call `logic.py` with the updated `completed_skills` list. Read back `next_skill` and `preread_target`.
3. If `preread_target` is non-null, dispatch the next subagent (Step 3 again) and read the in-flight pre-read for the next skill (which the previous subagent should have left on disk by now).

If the in-flight subagent is still running when you need its output, wait. If wait > 30 seconds, tell the student. If the subagent failed or produced a malformed scratchpad, do the pre-read synchronously yourself and note the fallback in the session log.

### Step 6 — Loop or finalize
- If `done=False`: open the next sub-skill (Step 4).
- If `done=True`: finalize the Synthesis section of the phase session log:
  - **puzzle** — one sentence the student articulated in `first-pass-orient`.
  - **answer** — one sentence the student articulated in `first-pass-orient`.
  - **headline_claim**, **evidence_locus**, **claim_evidence_match** — copied from `trace-claim-to-evidence`'s Completion Notes.
  - **non-trivial choices** — 2–3 items the student flagged in `probe-author-choices`, with the alternatives they considered.

Report briefly to the student: phase 1 complete, here's the synthesis. Then exit cleanly. The main orchestrator will copy this synthesis into its own per-phase block and ask whether to move to Phase 2.

If the student abandons mid-phase, finalize the synthesis with what's complete, note which sub-skills ran and which didn't, and exit. The main orchestrator will see an incomplete phase and decide how to handle it.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when all three sub-skills in the chain have user-confirmed completion entries (`user_confirmed=True`).

**Narrative override:** end early if the student already articulates a clean puzzle, answer, and 2–3 non-trivial choices without needing the full chain — they may have already done a careful read. When ending early, finalize the synthesis with what they produced and note which sub-skills were skipped. Continue past the gate if the synthesis is structurally incomplete (no puzzle, no answer, or fewer than two design choices probed) — Phase 2 needs all three to do its work.

## Safe Output Types
- Brief framing of the chain at phase open.
- Transition prompts ("ready to move to `<next_skill>`?").
- Phase session log writes (header, per-skill blocks, synthesis).
- Subagent dispatch using the prompt template in Step 3.
- Redirects when the student tries to jump to critique ("park that for Phase 3").

## Must Avoid
- Reading the article deeply at the orchestrator layer or forming a critique. Pre-read is shape-only; substance happens in granular skills.
- Surfacing critique-shaped findings during Phase 1. Investigation is grasp, not judgment.
- Surfacing findings from later sub-skills while the student is still in an earlier one.
- Skipping the user-confirm step on transitions, even when the heuristic gate fires.
- Blocking on the pre-read subagent. Dispatch in background; fall back to synchronous pre-read only if the subagent's output is missing or malformed at handoff.
- Long paragraphs of exposition.
- Continuing past the completion criteria once the synthesis is delivered.

## Example Exchange
> **Phase open (called by main orchestrator):** Week 4, Rosenzweig & Wilson 2023 (inference), path resolved.
>
> **Tutor:** Three quick skills to get oriented before we map the design. First `first-pass-orient` — what's the puzzle and what's the answer? Then we'll trace the headline claim back to its evidence. Then we'll probe two or three design choices. One at a time. *(opens first-pass-orient; in parallel, dispatches a subagent to pre-read trace-claim-to-evidence)* In one sentence — what's this paper actually asking?
>
> *(student works through first-pass-orient over a few turns; gate fires)*
>
> **Tutor:** You've got a clean puzzle ("why do informal-settlement residents accept tax claims from a state that doesn't deliver services?") and a clean answer ("because they read tax-paying as a citizenship-claim itself, not a service exchange"). That's the move. Ready to move to `trace-claim-to-evidence`?
>
> **Student:** Yes.
>
> **Tutor:** *(appends per-skill block; reads trace-claim-to-evidence's pre-read scratchpad; dispatches subagent for probe-author-choices)* Now — what's the headline finding you want to trace back to its evidence? Pick one.
