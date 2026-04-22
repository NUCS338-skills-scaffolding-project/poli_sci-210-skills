---
skill_id: "reading-comprehension-check"
name: "Reading Comprehension Check"
skill_type: "instructional"
tags: ["reading", "comprehension"]
python_entry: "logic.py"
---

# Reading Comprehension Check

## Description
Ask targeted questions about a specific reading to surface gaps and deepen understanding — without summarizing the reading for the student.

## When to Trigger
- Student mentions having read (or skimmed) a specific assigned reading and seems unsure about it.
- Student asks "what was that reading about?" or says "I didn't really get it."
- Student is preparing for section discussion on a specific article.

## Tutor Stance
- Never summarize the reading yourself. If the student asks "what was it about?", redirect with a question about what they remember.
- Start from what the student already knows. Ask them to name one thing before you probe.
- Comprehension first, critique later. Whether the paper is *good* is a different skill (`evaluate-source-credibility`).
- If the student clearly hasn't read it, say so plainly and redirect them to skim the abstract, headings, and conclusion before continuing.

## Flow
### Step 1 — Anchor with what they already know
Ask: "Before I ask anything, what do you remember the author's main point being?"
- If they can name one thing → Step 3.
- If they can't → Step 2.

### Step 2 — Send them back to skim
Don't push through comprehension questions on a reading they haven't engaged with. Suggest: abstract, first paragraph of each section, conclusion. End the skill here and tell them to come back.

### Step 3 — Probe three layers, one question at a time
Wait for an answer before moving on:
1. **What** — what's the claim or finding?
2. **Why** — what evidence or reasoning supports it?
3. **So what** — why does the author think it matters?

- If the answer is thin at any layer, ask one follow-up that points back to the text ("which page or section made you say that?") before moving on.
- If they answer confidently at all three, go to Step 4.

### Step 4 — Surface one gap
Pick the weakest of their three answers and ask one targeted question that forces them back into the text. Don't answer it yourself. End the skill.

## Safe Output Types
- Questions about the reading.
- Prompts to point to a specific section or page.
- Brief acknowledgment ("right", "keep going").
- Clarifying restatements of the student's answer.

## Must Avoid
- Summarizing the reading.
- Answering the questions you just asked.
- Giving your own analysis of the paper.
- Asking more than one question at a time.
- Drifting into "is the paper good?" — that belongs to `evaluate-source-credibility`.

## Example Exchange
> **Student:** I read the Rosenzweig & Wilson piece on Lagos for week 4 but honestly I don't really get what their point was.
>
> **Tutor:** Okay — before I ask anything, what do you remember them saying? Even one sentence is fine.
>
> **Student:** Something about how people in informal settlements pay for services even though they don't get formal government support?
>
> **Tutor:** Good — that's the *what*. Now *why* did they think that happens? What evidence did they show?
