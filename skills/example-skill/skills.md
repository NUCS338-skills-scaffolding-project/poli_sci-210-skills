---
skill_id: "skill-name"
name: "Human Readable Name"
skill_type: "instructional"
tags: ["topic1", "topic2"]
python_entry: "logic.py"
---

# Skill Name

## Description
What does this skill do? Keep it to 2-3 sentences.
This will appear in the shared catalog so make it clear and concise.

## Skill Type
- **Type:** instructional OR code
- **Course Focus:** Humanities OR CS OR Both

## When to Trigger
- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

---
<!-- FOR INSTRUCTIONAL SKILLS: Complete this section -->

## Tutor Stance
Describe the non-negotiable rules for how the tutor should behave.
- Be concise. One short paragraph or one question per turn. No bulleted lectures. The goal is engagement, not exposition.

## Tutor Pre-Read & Notes
Before engaging the student, silently form your own canonical answer to whatever this skill is about (the decomposition, the verdict, the comparison, the model example, the explanation — whatever the skill is asking the student to produce). Write it to a scratchpad at:

```
skills/<this-skill-id>/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

Use this structure:

```
# <skill-id> — <student> — <timestamp>

## My Pre-Read
<your silent canonical answer for THIS artifact>

## Student's Take
<captured at the student's first articulation>

## Divergences
- <what the student got differently from your pre-read>

## Resolved
- <moved here as the conversation closes each gap>

## Open
- <what's still unaddressed — your todo list>

## Completion Notes
<written when you judge the skill done; cite which criteria are met>
```

Re-read this file each turn to stay anchored. The pre-read is a tool for *you* — never paste it at the student.

## Flow
### Step 1 — Step Title
Describe what to do in this step.

### Step 2 — Reconcile (folded into the natural beat)
After the student's first articulation, compare it against your pre-read. The divergences become your scaffolding targets — those are the gaps to walk them across in the rest of the flow.

### Step 3 — Step Title
Describe what to do in this step.

## Completion Criteria
**Heuristic gate (logic.py):** describe the structural signals that mean the student has produced what this skill was after — the boolean conditions `run()` returns as `done`. Be specific to this skill.

**Narrative override:** you may end early if the student has clearly understood the move even without hitting every gate. You may continue past the gate if open divergences feel important. When you decide done, write the Completion Notes block in the scratchpad and close with a forward pointer to a related skill.

## Safe Output Types
What the tutor IS allowed to produce.

## Must Avoid
What the tutor must NEVER do.
- Long paragraphs of exposition or lecture-style explanations.
- Pasting your pre-read at the student as "the answer."
- Continuing past the completion criteria once they're satisfied.

## Example Exchange
> **Student:** "Example student message"
>
> **Tutor:** "Example tutor response"

---
<!-- FOR CODE SKILLS: Complete this section -->

## Inputs
Describe what inputs the logic.py function expects. Instructional skills should accept an optional `tutor_pre_read` field carrying the structural shape of the tutor's silent canonical answer (skill-specific schema).

## Outputs
Describe what the function returns. Instructional skills should include `done: bool` and `done_reasons: list[str]` so the tutor has a heuristic gate for completion.

## Usage
```python
from logic import run
result = run({"key": "value"})
print(result)
```

## Notes
Any additional notes for teams importing this skill.
