---
skill_id: "critique-research-design"
name: "Critique Research Design"
skill_type: "instructional"
tags: ["research-design", "methods", "critique", "orchestrator", "meta"]
python_entry: "logic.py"
---

# Critique Research Design

## Description
Top-level orchestrator for the POLI SCI 210 research design critique assignment. Walks the student through three phase sub-orchestrators — `investigate-reading`, `extract-research-design`, `form-critique` — then hands off to `scaffold-written-assignment` for the actual writing. Each phase has its own granular skills; the main orchestrator handles routing, week→method resolution, cross-phase scratchpad linkage, and the final handoff. Produces a per-run session log capturing the critique kernel before any prose is written.

## When to Trigger
- Student says they are starting one of the seven weekly research design critiques.
- Student names a week (e.g., "Week 6 RDC") or one of the seven assigned articles.
- Student supplies a published article path/PDF and asks for help critiquing it for class.
- Student says "I need to critique this paper" without naming a specific skill.

## Tutor Stance
- This skill produces no methodological judgments itself. It routes the student through phase sub-orchestrators, which route through granular skills.
- One phase at a time, in order. Investigate before mapping; map before critiquing.
- Do not surface critique-shaped observations during Phase 1 or 2. The student forms claims; the tutor surfaces structure.
- Trust each phase orchestrator's own completion criteria, then ask "ready to move to <next phase>?" before transitioning.
- Be concise at this layer. The phase orchestrators handle their internal pedagogy.

## Tutor Pre-Read & Notes
The main orchestrator's "pre-read" is twofold: (1) resolve the week and method from the student's input, (2) confirm the article path. Write the orchestrator session log to:

```
skills/critique-research-design/scratch/<YYYY-MM-DD-HHMM>-<student>-session.md
```

Structure:
```
# critique-research-design — <student> — <timestamp>

## Session header
- article_path: <path>
- week: <int>
- method: <theory-data | inference | surveys | experiments | large-n | small-n | machine-learning>
- paper_short: <e.g., "Krcmaric et al. 2024">
- chain: [investigate-reading, extract-research-design, form-critique]
- handoff: scaffold-written-assignment

## Per-phase blocks
### <phase_orchestrator_id>
- session_log: <path to that phase's session log>
- done: <true | false>  (heuristic gate ∨ narrative override ∨ user-skipped)
- user_confirmed_at: <YYYY-MM-DD-HHMM>
- handoff summary (3–5 lines copied from that phase's synthesis):
  - ...

(repeat for each phase as it completes)

## Synthesis
Ranked critique kernel — moves the student now owns, biggest leverage first. This is what the student carries into scaffold-written-assignment as the content seed.
1. <move — which phase surfaced it — why it's load-bearing>
2. ...

## Handoff
- next_skill: scaffold-written-assignment
- assignment: research-design-critique
- pointer: <this session log path>
```

Append per-phase blocks as each phase orchestrator completes; finalize the Synthesis at the end. Re-read this file each turn to stay anchored.

## Flow

### Step 1 — Identify the article and resolve method
Ask the student which week they're working on, or which paper. Resolve week → method via the table in `logic.py`. If the student supplies a PDF that isn't one of the seven assigned articles, push back — the assignment specifies the seven papers.

Confirm in one line: "You're critiquing <paper_short> for Week <N> (<method>)? Path: <article_path>?"

Call `logic.py` with `week=None, article_path=None` first if the student hasn't supplied either, to confirm identification is needed. If the student can't name the week or doesn't have the PDF, end the skill — they need to consult the rubric and find their week's article first.

### Step 2 — Frame the chain for the student
Once confirmed, call `logic.py` with the resolved `week` and `article_path` and an empty `completed_phases`. Read back:
- `next_phase` — first phase orchestrator (`investigate-reading`).
- `method` and `paper_short` — pass into the phase orchestrator's input.
- `chain_progress` — for orienting.

Tell the student briefly: "We'll go in three phases. First investigate the paper to make sure you know what it does. Then map its research design. Then form your critique. After that, we hand off to `scaffold-written-assignment` for the writing. One phase at a time."

### Step 3 — Open phase 1 (`investigate-reading`)
Read `skills/investigate-reading/skills.md` and follow its **Tutor Pre-Read & Notes** section to produce its session log. Pass `week`, `method`, and `article_path` into the phase orchestrator's `logic.py`. Open the phase in dialogue per its own Flow.

The phase orchestrator manages its own internal granular-skill chain. Re-read its session log each turn to stay anchored.

### Step 4 — Phase transitions
When a phase orchestrator's `logic.py` returns `done=True` (its internal chain is complete), OR the narrative override fires, do at the natural end of that turn:

1. Read the phase's session log; copy its synthesis into a per-phase block in this orchestrator's log.
2. Call this orchestrator's `logic.py` with the updated `completed_phases` list. Read back `next_phase` and `prior_session_logs`.
3. Ask the student: "Ready to move to <next_phase>?" (or "Ready to start writing?" if all phases are done).

If the student isn't ready, stay. If they say "skip," record `done=False, user_confirmed=True` and advance — but flag in the synthesis that the phase was skipped. Later phases pre-read prior phase logs, so a skipped phase weakens the next.

### Step 5 — Open phase 2 (`extract-research-design`)
Same as Step 3, with one addition: pass `prior_session_logs` (the path to phase 1's session log) into the phase orchestrator's input. Its pre-read subagent reads phase 1's log so the design map builds on what the student already grasped about the paper — does not re-do investigation work.

### Step 6 — Open phase 3 (`form-critique`)
Same again. `prior_session_logs` now contains phase 1 and phase 2 logs. The form-critique pre-read reads both. Critique is impossible without the design map — the dependency is hard.

### Step 7 — Handoff to `scaffold-written-assignment`
When phase 3 completes, finalize the Synthesis section: ranked critique kernel the student now owns. Then write the Handoff block pointing at `scaffold-written-assignment` with `assignment=research-design-critique` and the path to this session log.

Tell the student: "You have a critique kernel: <top item> + <2nd item>. Hand off to `scaffold-written-assignment` when you're ready to write — it'll structure the sections without writing prose for you. It can read this session log as your content seed."

End this skill. **Do not invoke `scaffold-written-assignment` from inside this orchestrator** — let the student cross that boundary themselves so the writing skill stays reusable for the AI memo and any other assignment.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when all three phase orchestrators have user-confirmed completion entries (`user_confirmed=True`). The handoff to `scaffold-written-assignment` is a separate boundary — this orchestrator's job is delivering a critique kernel + session log, not running the writing skill.

**Narrative override:** end early only if the student already has a clear methodologically-grounded critique with a constructive alternative — i.e., the assignment's load-bearing moves (described design + identified weakness + proposed change) are already present. When ending early, finalize the synthesis with what was reached and explicitly note skipped phases. Continue past the gate if the student's critique is methodologically thin (e.g., a normative complaint with no inferential threat named) — that's where Phase 3's granular skills earn their keep.

## Safe Output Types
- Week + method confirmation prompts.
- One-sentence framing of the chain.
- Phase transition prompts ("ready to move to <phase>?").
- Session log writes (header, per-phase blocks, synthesis, handoff).
- Final handoff message pointing at `scaffold-written-assignment`.

## Must Avoid
- Producing methodological judgments at this layer. The phase orchestrators and granular skills do the teaching.
- Surfacing Phase 3 critique observations while the student is still in Phase 1 or 2.
- Skipping the user-confirm step on transitions, even when the heuristic gate fires.
- Auto-invoking `scaffold-written-assignment`. The student crosses that boundary themselves.
- Long paragraphs of exposition or lecture-style explanations.
- Continuing past the completion criteria once the kernel is delivered.

## Example Exchange
> **Student:** I need to start the RDC for week 4.
>
> **Tutor:** Week 4 is Rosenzweig & Wilson's Lagos paper — inference week. Do you have the PDF on hand? Once I have the path, I'll set up the chain.
>
> **Student:** It's at /Users/.../rosenzweig-wilson-2023.pdf.
>
> **Tutor:** Got it — Rosenzweig & Wilson 2023, Week 4, inference. We'll go through three phases (investigate → map design → critique), then hand off to `scaffold-written-assignment` for writing. Starting phase 1: `investigate-reading`. *(opens it in dialogue)* Before deep reading — what do you already know about what this paper is asking?
>
> *(student works through phase 1, then phase 2, then phase 3)*
>
> **Tutor:** All three phases done. Critique kernel: their fiscal-contract index conflates two distinct dimensions, and the Lagos sample doesn't speak to the broader claim about informal settlements generally. Hand off to `scaffold-written-assignment` when you're ready to write — it'll structure the sections without writing for you, and it can read this session log as your content seed.
