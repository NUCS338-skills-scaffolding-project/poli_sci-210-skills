---
skill_id: "critique-design"
name: "Critique Research Design"
skill_type: "instructional"
stance: "meta"
tags: ["research-design", "methods", "critique", "orchestrator", "meta"]
course_types: ["humanities"]
learning_goal_tags:
  - "evaluate-reasoning"
  - "surface-assumptions"
  - "engage-objections"
trigger_signals:
  - "start-rdc"
  - "rdc-week-N"
  - "research-design-critique-assignment"
  - "need-to-critique-paper"
  - "starting-weekly-critique"
python_entry: "logic.py"
status: "ready"
version: "0.2.0"
---

# Critique Research Design

## Description
Top-level orchestrator for the POLI SCI 210 research design critique assignment. Walks the student through three phase sub-orchestrators — `orient-paper`, `map-design`, `form-critique` — then hands off to `scaffold-writing` for the actual writing. Each phase has its own granular skills; the main orchestrator handles routing, week→method resolution, cross-phase scratchpad linkage, and the final handoff. Produces a per-run session log capturing the critique kernel before any prose is written.

## When to Trigger
- Student says they are starting one of the seven weekly research design critiques.
- Student names a week (e.g., "Week 6 RDC") or one of the seven assigned articles.
- Student supplies a published article path/PDF and asks for help critiquing it for class.
- Student says "I need to critique this paper" without naming a specific skill.

## Hard requirement: article PDF
This chain hard-requires access to the article's full text — abstract-only or summary-only input won't work, because the Phase 1 `trace-evidence` skill needs the student to locate specific tables/figures inside the paper. The path passes through every leaf skill via the `article_path` input.

If the student doesn't have the PDF (no `article_path`, no attachment, no pasted full text), end the skill cleanly and tell them to fetch the paper before re-opening the chain. Do NOT run a degraded chain on the abstract — the pedagogical move requires reading past the framing into the tables, and an abstract-only run silently produces a chain that *looks* complete but skips the move the assignment is grading.

## Tutor Stance
- This skill produces no methodological judgments itself. It routes the student through phase sub-orchestrators, which route through granular skills.
- One phase at a time, in order. Investigate before mapping; map before critiquing.
- Do not surface critique-shaped observations during Phase 1 or 2. The student forms claims; the tutor surfaces structure.
- Trust each phase orchestrator's own completion criteria, then ask "ready to move to <next phase>?" before transitioning.
- Be concise at this layer. The phase orchestrators handle their internal pedagogy.

## Tutor Pre-Read & Notes
The main orchestrator's "pre-read" is twofold: (1) resolve the week and method from the student's input, (2) confirm the article path.

**Default session-log path** (resolved from `paths.scratch_pattern` in `metadata.yaml`):

```
skills/critique-design/scratch/<YYYY-MM-DD-HHMM>-<student>-session.md
```

**Adopter fallback (no writable conventional path)**: this orchestrator needs durable persistence across phase/sub-skill handoffs — unlike a leaf skill, you cannot hold this in memory alone. Write to whatever scratch location the host runtime exposes:

1. `./.critique-design-scratch/<YYYY-MM-DD-HHMM>-<student>-session.md` if cwd is writable.
2. `/tmp/critique-design-<YYYY-MM-DD-HHMM>-<student>-session.md` if cwd is not writable.

Surface the resolved path to the student in your opening message.

Structure (whether on disk or at the resolved fallback path):
```
# critique-design — <student> — <timestamp>

## Session header
- article_path: <path>
- week: <int>
- method: <theory-data | inference | surveys | experiments | large-n | small-n | machine-learning>
- paper_short: <e.g., "Krcmaric et al. 2024">
- chain: [orient-paper, map-design, form-critique]
- handoff: scaffold-writing

## Per-phase blocks
### <phase_orchestrator_id>
- session_log: <path to that phase's session log>
- done: <true | false>  (heuristic gate ∨ narrative override ∨ user-skipped)
- user_confirmed_at: <YYYY-MM-DD-HHMM>
- handoff summary (3–5 lines copied from that phase's synthesis):
  - ...

(repeat for each phase as it completes)

## Synthesis
Ranked critique kernel — moves the student now owns, biggest leverage first. This is what the student carries into scaffold-writing as the content seed.
1. <move — which phase surfaced it — why it's load-bearing>
2. ...

## Handoff
- next_skill: scaffold-writing
- assignment: research-design-critique
- pointer: <this session log path>
```

Append per-phase blocks as each phase orchestrator completes; finalize the Synthesis at the end. Re-read the session log each turn (or re-anchor against the resolved fallback path) to stay anchored.

## Flow

### Step 1 — Identify the article and resolve method
Ask the student which week they're working on, or which paper. Resolve week → method via the table in `logic.py`. If the student supplies a PDF that isn't one of the seven assigned articles, push back — the assignment specifies the seven papers.

Confirm in one line: "You're critiquing <paper_short> for Week <N> (<method>)? Path: <article_path>?"

> **Adopter note:** The `WEEK_METHOD` dictionary in `logic.py` now reads from `metadata.yaml.course_context.rdc_syllabus` at module load, with a hard-coded POLI SCI 210 default as a defensive fallback. An adopting team replaces the RDC schedule by editing `metadata.yaml` only — no `logic.py` edits required. Each `rdc_syllabus` entry has `{week, method, paper_short}`; `method` must be one of the `id` values in `course_context.research_methods` (also in `metadata.yaml`). The RDC chain (`orient-paper` → `map-design` → `form-critique` → `scaffold-writing`) is generic for any course teaching empirical paper critique; only the syllabus mapping is course-specific.

Call `logic.py` with `week=None, article_path=None` first if the student hasn't supplied either, to confirm identification is needed. If the student can't name the week or doesn't have the PDF, end the skill — they need to consult the rubric and find their week's article first.

### Step 2 — Frame the chain for the student
Once confirmed, call `logic.py` with the resolved `week` and `article_path` and an empty `completed_phases`. Read back:
- `next_phase` — first phase orchestrator (`orient-paper`).
- `method` and `paper_short` — pass into the phase orchestrator's input.
- `chain_progress` — for orienting.

Tell the student briefly: "We'll go in three phases. First investigate the paper to make sure you know what it does. Then map its research design. Then form your critique. After that, we hand off to `scaffold-writing` for the writing. One phase at a time."

### Step 3 — Open phase 1 (`orient-paper`)
Read `skills/orient-paper/skills.md` and follow its **Tutor Pre-Read & Notes** section to produce its session log. Pass `week`, `method`, and `article_path` into the phase orchestrator's `logic.py`. Open the phase in dialogue per its own Flow.

The phase orchestrator manages its own internal granular-skill chain. Re-read its session log each turn to stay anchored.

### Step 4 — Phase transitions
When a phase orchestrator's `logic.py` returns `done=True` (its internal chain is complete), OR the narrative override fires, do at the natural end of that turn:

1. Read the phase's session log; copy its synthesis into a per-phase block in this orchestrator's log.
2. Call this orchestrator's `logic.py` with the updated `completed_phases` list. Read back `next_phase` and `prior_session_logs`.
3. Ask the student: "Ready to move to <next_phase>?" (or "Ready to start writing?" if all phases are done).

If the student isn't ready, stay. If they say "skip," record `done=False, user_confirmed=True` and advance — but flag in the synthesis that the phase was skipped. Later phases pre-read prior phase logs, so a skipped phase weakens the next.

### Step 5 — Open phase 2 (`map-design`)
Same as Step 3, with one addition: pass `prior_session_logs` (the path to phase 1's session log) into the phase orchestrator's input. Its pre-read subagent reads phase 1's log so the design map builds on what the student already grasped about the paper — does not re-do investigation work.

### Step 6 — Open phase 3 (`form-critique`)
Same again. `prior_session_logs` now contains phase 1 and phase 2 logs. The form-critique pre-read reads both. Critique is impossible without the design map — the dependency is hard.

### Step 7 — Handoff to `scaffold-writing`
When phase 3 completes, finalize the Synthesis section: ranked critique kernel the student now owns. Then write the Handoff block pointing at `scaffold-writing` with `assignment=research-design-critique` and the path to this session log.

Tell the student: "You have a critique kernel: <top item> + <2nd item>. Hand off to `scaffold-writing` when you're ready to write — it'll structure the sections without writing prose for you. It can read this session log as your content seed."

> **Optional invocation — `session-reflect`:** Before ending, offer: "Want to take 30 seconds for a quick reflection before we close out the critique work?" If accepted, invoke `session-reflect` — the RDC chain spans three phases and 9 sub-skills, so a consolidating reflection is high-value here. The reflection log is forward-looking; it doesn't duplicate the critique kernel synthesis. Skip if the student has already disengaged.

End this skill. **Do not invoke `scaffold-writing` from inside this orchestrator** — let the student cross that boundary themselves so the writing skill stays reusable for the AI memo and any other assignment.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when all three phase orchestrators have user-confirmed completion entries (`user_confirmed=True`). The handoff to `scaffold-writing` is a separate boundary — this orchestrator's job is delivering a critique kernel + session log, not running the writing skill.

**Narrative override:** end early only if the student already has a clear methodologically-grounded critique with a constructive alternative — i.e., the assignment's load-bearing moves (described design + identified weakness + proposed change) are already present. When ending early, finalize the synthesis with what was reached and explicitly note skipped phases. Continue past the gate if the student's critique is methodologically thin (e.g., a normative complaint with no inferential threat named) — that's where Phase 3's granular skills earn their keep.

## Safe Output Types
- Week + method confirmation prompts.
- One-sentence framing of the chain.
- Phase transition prompts ("ready to move to <phase>?").
- Session log writes (header, per-phase blocks, synthesis, handoff).
- Final handoff message pointing at `scaffold-writing`.

## Must Avoid
- Producing methodological judgments at this layer. The phase orchestrators and granular skills do the teaching.
- Surfacing Phase 3 critique observations while the student is still in Phase 1 or 2.
- Skipping the user-confirm step on transitions, even when the heuristic gate fires.
- Auto-invoking `scaffold-writing`. The student crosses that boundary themselves.
- Long paragraphs of exposition or lecture-style explanations.
- Continuing past the completion criteria once the kernel is delivered.

## Example Exchange
> **Student:** I need to start the RDC for week 4.
>
> **Tutor:** Week 4 is Rosenzweig & Wilson's Lagos paper — inference week. Do you have the PDF on hand? Once I have the path, I'll set up the chain.
>
> **Student:** It's at /Users/.../rosenzweig-wilson-2023.pdf.
>
> **Tutor:** Got it — Rosenzweig & Wilson 2023, Week 4, inference. We'll go through three phases (investigate → map design → critique), then hand off to `scaffold-writing` for writing. Starting phase 1: `orient-paper`. *(opens it in dialogue)* Before deep reading — what do you already know about what this paper is asking?
>
> *(student works through phase 1, then phase 2, then phase 3)*
>
> **Tutor:** All three phases done. Critique kernel: their fiscal-contract index conflates two distinct dimensions, and the Lagos sample doesn't speak to the broader claim about informal settlements generally. Hand off to `scaffold-writing` when you're ready to write — it'll structure the sections without writing for you, and it can read this session log as your content seed.
