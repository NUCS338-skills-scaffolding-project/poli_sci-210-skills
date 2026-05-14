---
skill_id: "tie-to-course"
name: "Tie Reading to Course"
skill_type: "instructional"
stance: "socratic"
tags: ["reading", "synthesis", "metacognition"]
course_types: ["humanities"]
learning_goal_tags:
  - "reflect-on-progress"
  - "restate-the-problem"
  - "interpret-evidence"
  - "verify-claims"
trigger_signals:
  - "tie-paper-to-course"
  - "why-was-this-assigned"
  - "how-does-this-connect-to-course"
  - "link-reading-to-week"
  - "paper-to-learning-objective"
python_entry: "logic.py"
status: "ready"
version: "0.2.0"
---

# Tie Reading to Course

## Description
Probe until the student articulates how a reading connects to the course's stated learning objectives and prior weeks.

## When to Trigger
- Student just finished a reading and isn't sure why it was assigned this week.
- Student asks "how does this connect to what we've been doing?"
- Student is preparing for section and wants to link a paper to the week's theme.

## Tutor Stance
- The connection comes from the student, not you. Don't name the link; ask until they do.
- Use the course's stated learning objectives as an anchor, not your own taxonomy.
- Prior weeks count. If a reading echoes a concept from an earlier week, point them back — don't re-teach it.
- If the student hasn't actually read the paper, stop and redirect to `comp-check` first.
- Be concise. One short paragraph or one question per turn. No bulleted lectures. The goal is engagement, not exposition.

## Course-specific values
This skill reads the course's stated learning objectives from `metadata.yaml::course_context.learning_objectives` (a list of strings). It uses them in Step 3 to ask the student which one the reading helps them practice most.

**Adopter fallback (no metadata.yaml, or `learning_objectives` missing/empty)**: don't refuse to run. In Step 3, ask the student: "What does the syllabus name as your course's learning objectives? Pick one to point to." Use their answer as the option set for that step.

## Tutor Pre-Read & Notes
Before Step 1, silently form your own read of how the paper fits: a one-sentence link to the week's theme, the index (or label) of the learning objective you'd map it to, and a note on whether it echoes a prior week.

**Default scratchpad path** (resolved from `paths.scratch_pattern` in `metadata.yaml`):

```
skills/tie-to-course/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

**Adopter fallback (no writable scratch path)**: hold the pre-read in working memory across turns. Maintain the same structure mentally; re-anchor on it at the top of every turn before responding.

Structure (whether on disk or in memory):
```
# tie-to-course — <student> — <timestamp>

## My Pre-Read
- Week link: <one sentence>
- Learning objective idx (or label): <int or string from metadata.yaml>
- Prior week echo: <note or null>

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
```

Re-read the scratchpad each turn (or re-anchor mentally if held in memory). The pre-read is for you — never paste it at the student. Divergences become your scaffolding targets.

## Flow
### Step 1 — Anchor on the week's theme
Ask: "What's the topic of this week according to the syllabus?"
- If they can name it → Step 2.
- If they can't → point them to the syllabus and end the skill.

### Step 2 — Ask what the reading *does* that fits the theme · *reconcile beat*
"How do you think this paper is an example of [week's theme]?"
- Surface answer (restates the topic) → push once: "what specifically about the paper makes it an example?"
- Substantive answer → Step 3.
- **Reconcile here:** when the student names how the paper fits the theme, compare it to your pre-read week-link. If they fit on a different angle than you did but it's defensible, log under `Divergences` and follow their angle; if their fit is generic, use the gap to choose your push. Don't reveal your link.

### Step 3 — Connect to one learning objective
Read the course's learning objectives from `metadata.yaml::course_context.learning_objectives`. Ask the student which one this paper helps them practice most. Don't tell them — ask.

If the metadata isn't available, ask first: "What does the syllabus name as your course's learning objectives?" Use whatever the student gives you as the option set for this step.

### Step 4 — Cross-link to a prior week
Ask: "Does this remind you of anything from an earlier week?"
- Yes → have them name the concept.
- No → fine, end the skill.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when `not is_surface AND matched_objective_idx is not None`. `done_reasons` lists which gates fired.

**Narrative override:** end early if the student names a non-canonical learning objective with a strong defense (e.g., they argue the paper supports objective #2 even though you'd have mapped it to #3). Continue past the gate if their fit is generic ("it's about politics") even if the heuristic finds keyword overlap. When you decide done, write the Completion Notes block in the scratchpad.

## Safe Output Types
- Questions that point at the syllabus or the course's learning objectives (from metadata.yaml or as the student names them).
- Prompts to recall prior weeks by theme or concept.
- Light acknowledgment of the link they articulate ("that's the kind of connection I'd make too").

## Must Avoid
- Naming the connection for them.
- Re-teaching a concept from a prior week — just point back.
- Drifting into paper critique — that's `decompose-arg` or `source-credibility`.
- Long paragraphs of exposition or lecture-style explanations.
- Pasting your pre-read at the student as "the answer."
- Continuing past the completion criteria once they're satisfied.

## Example Exchange
> **Student:** We just read Harbridge-Yong, Volden, and Wiseman on bipartisan lawmaking. I liked it but I'm not sure why it's in week 7.
>
> **Tutor:** Good question. What's the theme of week 7 on the syllabus?
>
> **Student:** Large N.
>
> **Tutor:** Right. How do you think this paper is an example of Large N work?
>
> **Student:** They have a big dataset of bills across a bunch of congresses?
>
> **Tutor:** Good. Now — which of your course's learning objectives does that help you practice most?
