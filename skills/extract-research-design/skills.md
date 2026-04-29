---
skill_id: "extract-research-design"
name: "Extract Research Design"
skill_type: "instructional"
tags: ["research-design", "methods", "design-map", "orchestrator", "phase"]
python_entry: "logic.py"
---

# Extract Research Design

## Description
Phase 2 sub-orchestrator of `critique-research-design`. Walks the student through three granular skills — `design-skeleton` → `operationalization-check` → `method-week-alignment` — to build a structured map of what the paper actually does, where its measurement is vulnerable, and which course-specific concerns apply. Hides per-skill pre-read latency by dispatching subagents in the background. Produces a phase session log whose Synthesis is the design map + measurement vulnerabilities + alignment notes that Phase 3 (`form-critique`) consumes.

## When to Trigger
- The main orchestrator (`critique-research-design`) opens this phase as Phase 2 of the chain (after `investigate-reading`).
- Direct invocation: a student says "help me map the design" or "I want to understand what the paper is actually doing methodologically."
- Not for forming a critique — that's Phase 3. Mapping is description; judging is judgment.

## Tutor Stance
- This skill produces no methodological judgments itself. It routes the student into granular sub-skills.
- One sub-skill at a time, in order. The chain is sequenced so each skill builds on the last.
- The student stays in dialogue throughout — never run sub-skills as silent monologue.
- Critique-shaped observations are out of scope here. If the student starts judging, redirect: "park that for Phase 3. For now we're describing."
- Trust each sub-skill's completion criteria, then ask "ready to move on?" before transitioning.
- Be concise at this layer.

## Tutor Pre-Read & Notes
The phase orchestrator's pre-read is twofold: (1) read the Phase 1 session log so you know the student's puzzle, answer, headline claim, evidence locus, and the choices they already surfaced; (2) scan the article's methods section for shape only (length, subsection structure, presence of a formal model, presence of a measurement appendix). Do NOT form your own design map at this layer — substantive pre-reads happen at the granular-skill level via subagents.

Write the phase session log to:

```
skills/extract-research-design/scratch/<YYYY-MM-DD-HHMM>-<student>-session.md
```

Structure:
```
# extract-research-design — <student> — <timestamp>

## Phase header
- article_path: <path>
- week: <int>
- method: <method>
- paper_short: <e.g., "Krcmaric et al. 2024">
- prior_session_logs:
  - investigate-reading: <path>            # from main orchestrator
- chain: [design-skeleton, operationalization-check, method-week-alignment]
- methods_section_scan: <2–4 lines: subsection structure, model presence, measurement appendix presence>
- carryover_from_phase_1:
  - non_trivial_choices: <copied from Phase 1 synthesis>
  - claim_evidence_match: <copied from Phase 1 synthesis — flag if "suspicious gap">

## Per-skill blocks
### <skill_id>
- scratchpad: <path>
- done: <true | false>
- user_confirmed_at: <YYYY-MM-DD-HHMM>
- key findings (2–4 lines copied from the sub-skill's Completion Notes)

(repeat for each skill as it completes)

## Synthesis
Phase 2 deliverable — the design map, measurement vulnerabilities, and method-week alignment notes. Consumed by Phase 3.

### Design map
- research_question: ...
- unit_of_analysis: ...
- sample: ...
- iv_or_treatment: ...                     # n/a if method does not have one — note why
- dv_or_outcome: ...
- identification_strategy: ...
- comparison: ...

### Operationalization vulnerabilities
- { concept, operationalization, includes_but_shouldnt, excludes_but_should, severity }
- ...

### Method-week alignment
- { concern, paper_element, alignment, note }
- ...
```

Append per-skill blocks as each granular skill completes; finalize the Synthesis at the end. Re-read this log each turn to stay anchored.

## Flow

### Step 1 — Open the phase
Read the Phase 1 session log (path supplied by the main orchestrator). Pull forward into the phase header: the non-trivial choices the student surfaced, and the claim/evidence match label. Read the article's methods section for shape only. Write the phase session log header. Call `logic.py` with `completed_skills=[]` to confirm the chain.

Tell the student briefly what's coming: "Three skills to build the design map. First `design-skeleton` — fill in the canonical fields (question, units, sample, IV/DV, strategy, comparison). Then `operationalization-check` — interrogate how one or two key concepts are measured. Then `method-week-alignment` — sweep the design against this week's specific concerns. One at a time."

### Step 2 — Open the first skill (synchronous pre-read)
For `design-skeleton`, do the pre-read synchronously per its spec. Pass `week`, `method`, `article_path`, and `prior_session_logs` (Phase 1 log) into its inputs. Open in dialogue per its Flow.

At the same turn, dispatch the pre-read subagent for `operationalization-check`.

### Step 3 — Dispatch pre-read subagent for skill N+1
Same pattern as `investigate-reading`. Use `Agent` tool with `subagent_type=general-purpose` and `run_in_background=true`. Prompt template:

```
You are doing a silent pre-read for the granular skill `<NEXT_SKILL_ID>` in
the extract-research-design phase of a POLI SCI 210 research design critique.

Inputs:
- Article: <ABSOLUTE_PATH_TO_ARTICLE>
- Week: <WEEK>     Method: <METHOD>     Paper: <PAPER_SHORT>
- Skill spec (read this first): <ABSOLUTE_PATH_TO_NEXT_SKILL_SKILLS_MD>
- Prior phase session logs (from main orchestrator):
  - investigate-reading: <PATH>
- Prior in-phase scratchpads (so your pre-read builds on prior sub-skills):
  - <ABSOLUTE_PATH_TO_PRIOR_SCRATCHPAD_1>
  - ...

Task:
1. Read the skill spec and follow its "Tutor Pre-Read & Notes" section
   verbatim to form your own canonical answer for THIS article at THIS skill's
   level. Method-aware: focus on what's load-bearing for a <METHOD>-style
   paper.
2. Read the Phase 1 synthesis (puzzle, answer, headline_claim, evidence_locus,
   non-trivial choices) and reference it where relevant. Especially: if Phase 1
   surfaced a measurement-category choice, the operationalization-check
   pre-read should foreground that exact concept.
3. Write the pre-read scratchpad at the conventional path the skill spec
   gives. Use the exact section headings the spec specifies.
4. Do NOT engage the user. Do NOT modify any other files. Return a one-line
   confirmation.

Constraints:
- Silent pre-read only.
- Build on prior scratchpads where relevant.
- Stay within Phase 2 scope: description and mapping, no critique.
```

Substitute the absolute paths and the next skill's id. Do not block.

### Step 4 — Run the sub-skill in dialogue
Hand off to the sub-skill's Flow. Re-read its scratchpad each turn. The student works through it the same way they would if they had invoked the skill directly.

When the sub-skill's `logic.py` returns `done=True`, OR you fire the narrative override:
1. Write the Completion Notes block in the sub-skill's scratchpad per its spec.
2. Ask the student: "Ready to move to `<NEXT_SKILL_ID>`?" (or "Phase 2 done — ready to head into critique?" if last).

If the student isn't ready, stay. If they say "skip," record `done=False, user_confirmed=True` and advance — but a skipped sub-skill weakens Phase 3's pre-read materially.

### Step 5 — Append per-skill block + advance
Once the student confirms:
1. Append a per-skill block to the phase session log.
2. Call `logic.py` with the updated `completed_skills` list.
3. If `preread_target` is non-null, dispatch the next subagent and read the in-flight pre-read for the next skill.

If the in-flight subagent is still running when needed, wait. > 30s, tell the student. If the subagent failed, do the pre-read synchronously and note the fallback.

### Step 6 — Loop or finalize
- If `done=False`: open the next sub-skill (Step 4).
- If `done=True`: finalize the Synthesis section:
  - **Design map** — copy the 7 fields from `design-skeleton`'s Completion Notes.
  - **Operationalization vulnerabilities** — copy the concept entries from `operationalization-check`'s Completion Notes.
  - **Method-week alignment** — copy the concern entries from `method-week-alignment`'s Completion Notes.

Report briefly: phase 2 complete, here's the synthesis. Exit. The main orchestrator copies this synthesis into its per-phase block and asks whether to move to Phase 3.

If the student abandons mid-phase, finalize with what's complete and exit.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when all three sub-skills have user-confirmed completion entries.

**Narrative override:** end early if the student already has a complete design map, has interrogated at least one concept's operationalization with substance, and can name two method-week concerns tied to the paper. Continue past the gate if the design map has more than two empty fields, if no operationalization vulnerability was concretely named, or if method-week alignment is generic (not tied to specific paper elements) — Phase 3 will fail without these.

## Safe Output Types
- Brief framing of the chain at phase open.
- Transition prompts.
- Phase session log writes.
- Subagent dispatch using the prompt template in Step 3.
- Redirects when the student tries to jump to critique ("park that for Phase 3").

## Must Avoid
- Forming a design map at the orchestrator layer. Pre-read is shape-only + Phase 1 carryover.
- Surfacing critique-shaped findings during Phase 2. Mapping is description.
- Skipping the user-confirm step on transitions.
- Blocking on the pre-read subagent.
- Long paragraphs of exposition.
- Continuing past the completion criteria.

## Example Exchange
> **Phase open (called by main orchestrator):** Week 4, Rosenzweig & Wilson 2023 (inference). Phase 1 synthesis on disk.
>
> **Tutor:** Three skills to build the design map. First `design-skeleton` — fill in question, units, sample, IV/DV, strategy, comparison. Then we interrogate one concept's operationalization. Then we sweep against this week's inference checklist. *(opens design-skeleton; in parallel dispatches operationalization-check pre-read)* Starting with the research question — in one sentence, what's the question this paper is trying to answer? You already named the puzzle in Phase 1; this is the more formal version.
>
> *(student works through all three sub-skills)*
>
> **Tutor:** Phase 2 done. Design map filled, two operationalization vulnerabilities flagged (the fiscal-contract index and the residency definition), and three inference-week concerns aligned to the design (selection on observables assumption, scope of the causal claim, and the comparison group composition). Ready to head into critique?
