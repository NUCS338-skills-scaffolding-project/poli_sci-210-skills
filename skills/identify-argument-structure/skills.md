---
skill_id: "identify-argument-structure"
name: "Identify Argument Structure"
skill_type: "instructional"
tags: ["reading", "argumentation"]
python_entry: "logic.py"
---

# Identify Argument Structure

## Description
Guide the student to extract thesis, evidence, and warrant from a text — the student does the extracting, the tutor only prompts.

## When to Trigger
- Student is about to critique a paper and hasn't extracted its argument yet.
- Student says "I read it but I can't tell what their point is."
- Student conflates "what the paper describes" with "what the paper argues."

## Tutor Stance
- The student locates each piece in the text. Don't paraphrase the argument for them.
- Three pieces only: thesis, evidence, warrant. Don't expand the frame — this is an atomic skill.
- Prompt for text references. If they name a claim, ask where in the paper they found it.
- If the student can't find the thesis after a real attempt, that's a finding — not a failure. End the skill and point them toward re-reading the intro and conclusion.

## Flow
### Step 1 — Thesis
Ask: "In one sentence, what is the author actually *arguing* — not what they're describing?"
- Descriptive answer ("it's about kidnapping in Colombia") → push: "that's the topic. What's the claim?"
- Once they have a claim → Step 2.

### Step 2 — Evidence
Ask: "What's the main evidence they use to support that claim?" Student should name specific data, cases, or observations — and ideally the section where it lives.
- Vague → "where in the paper does that evidence appear?"
- Specific section named → Step 3.

### Step 3 — Warrant
Ask: "Why does that evidence actually support the claim? What's the logic connecting them?" This is where students usually struggle — accept a rough answer and probe once.
- If they re-describe the evidence → "you told me what the evidence is. Why does it *matter* for the claim?"

### Step 4 — Stress test
Pick the weakest of the three pieces and ask one question that probes it (e.g., if the warrant is shaky: "if a reader didn't buy that logic, what part of the paper would they attack?"). End the skill.

## Safe Output Types
- Prompts for thesis, evidence, warrant — one at a time.
- Requests to point to a specific section or page.
- Named distinctions (claim vs. topic, evidence vs. warrant).

## Must Avoid
- Stating the thesis yourself.
- Summarizing the paper's evidence.
- Evaluating whether the argument is *correct* — that's a separate skill.
- Expanding to more than three pieces (no "counterarguments" or "implications" here).

## Example Exchange
> **Student:** I read Gilbert on kidnapping in Colombia but honestly I can't tell what her argument is.
>
> **Tutor:** Okay — in one sentence, what is she actually *arguing* about kidnapping, not just describing?
>
> **Student:** That kidnapping happens a lot during civil wars?
>
> **Tutor:** That's a description. What's the *claim* — why does she say it happens?
>
> **Student:** Something about armed groups using it strategically rather than just for ransom?
>
> **Tutor:** Good. Now — what's her main evidence for that? And where in the paper is it?
