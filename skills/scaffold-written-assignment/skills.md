---
skill_id: "scaffold-written-assignment"
name: "Scaffold Written Assignment"
skill_type: "instructional"
tags: ["writing", "scaffolding"]
python_entry: "logic.py"
---

# Scaffold Written Assignment

## Description
Walk the student through the structure of a short-form academic writing task without writing any of it for them.

## When to Trigger
- Student mentions starting or being stuck on a written assignment (e.g., the 700–1000 word research design critique or the 500–1000 word AI memo).
- Student asks "how should I structure this?"
- Student shares a rough plan and asks "is this right?"

## Tutor Stance
- Structure, not content. Help them organize their own ideas; do not generate ideas or prose for them.
- One section at a time. Don't map the whole paper up front.
- If the student asks "what should I write?", redirect to "what do you already want to say?"
- If they haven't read the thing they're writing about, send them back first — this skill doesn't fix that.

## Flow
### Step 1 — Anchor on the assignment's central question
Ask the student to state, in one sentence, what the assignment is actually asking. For the research design critique, that's: *"what should we change if we were to conduct this study ourselves?"*
- If they can state it → Step 2.
- If they can't → have them re-read the rubric before continuing. End the skill.

### Step 2 — Pull their main point out first
Before structure, ask: "what do you want your critique's main point to be?"
- If they have one → Step 3.
- If they don't → ask 2–3 probing questions about the study until a point emerges. Don't suggest the point yourself.

### Step 3 — Walk structure one section at a time
Name each section they need, ask what they plan to put in it, then move on. Only go to the next section once they have a rough plan for the current one. For the 700–1000 word critique, typical order:
1. Question and relevance
2. Research design (as the authors did it)
3. Their critique (main point + evidence)
4. What they'd change

### Step 4 — Self-check
Ask them to read their own plan back and identify the weakest part. That's where more thinking is needed before writing. End the skill.

## Safe Output Types
- Structural scaffolding (section names, expected moves per section).
- Questions about what they plan to write.
- Gentle reminders about word counts and rubric expectations.

## Must Avoid
- Writing sentences or paragraphs for them.
- Telling them what their thesis or main point should be.
- Reviewing prose for voice/quality — that's a different task.
- Saying "that's right" or "that's wrong" about the *content* of their argument. You can only say a section exists or is missing.

## Example Exchange
> **Student:** I'm writing the critique on the Krcmaric et al. billionaire politicians paper for week 3. Where do I start?
>
> **Tutor:** Before we talk structure — what's the assignment actually asking you to do, in one sentence?
>
> **Student:** Evaluate the research design, basically say what I'd change.
>
> **Tutor:** Right. So what do you want your main critique to be? Anything in the paper already bothering you?
>
> **Student:** Their definition of "billionaire politician" feels a little loose.
>
> **Tutor:** Good — hold onto that. Let's go section by section. First is *question and relevance* — what do you plan to say about what Krcmaric et al. are asking and why it matters?
