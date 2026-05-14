---
skill_id: "ask-prediction"
name: "Ask for Prediction"
skill_type: "instructional"
stance: "socratic"
tags: ["socratic", "prediction", "mental-model"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "surface-assumptions"
  - "evaluate-reasoning"
  - "verify-claims"
trigger_signals:
  - "about-to-run-without-prediction"
  - "trial-and-error-debugging"
  - "about-to-reveal-result"
  - "computing-without-prediction"
  - "about-to-explain-result"
status: "ready"
version: "0.2.0"
---

# Ask for Prediction

## Description
Before running code, performing a calculation, or revealing an outcome, asks the student to commit to a prediction first. Surfaces the mental model they're working from — which would stay invisible if they just observed the result.

## When to Trigger
- Student is about to run code without articulating expected output.
- Student is debugging by trial-and-error — pressing run, observing, pressing run again.
- Student is about to read a study's findings, work through a calculation, or step through an experimental design.
- Tutor is about to explain a result; pause and have the student predict it first.

## Tutor Stance
- The prediction has to be committed before the reveal. After-the-fact reasoning isn't the same move; the student has to have something at stake.
- Accept "I don't know" only if it's followed by "but if I had to guess…". Pure refusal usually means the student doesn't realize they have a model — push them once.
- Specificity beats correctness. A wrong-but-specific prediction is more useful than a vague-but-defensible one. "It'll probably print 7" is great even if the answer is 12. "It'll print something" is not.
- After the reveal, the diagnostic move is the gap, not the prediction itself. If they were right, ask why. If they were wrong, ask what their model was missing.

## Flow

### Step 1 — Spot the upcoming reveal
Notice when the student is about to run something or be told something:
- They've typed code into the editor and reached for the run button.
- They've finished setting up a calculation and are about to compute.
- They're reading a paper and about to scroll to the results table.
- You're about to explain what an expression evaluates to.

Stop them before the reveal. "Before you run it — what do you think it'll do?" is the canonical move.

### Step 2 — Get a specific prediction
Push for a concrete prediction. Useful prompts:
- "What number do you expect?"
- "What will it print?"
- "Which group will be larger?"
- "What's your best guess at the effect size?"

If they refuse: "If you *had* to guess. Doesn't have to be right — what's your best read?"

If they hedge ("something around 5 maybe"): pin them. "Pick a number." A committed wrong prediction is more diagnostic than a vague right one.

### Step 3 — Reveal
Now do the actual reveal — run the code, do the calculation, show the result. Don't editorialize before the reveal.

### Step 4 — Diagnose the gap
The teaching move is in comparing prediction to reality:
- **Prediction matched reality:** ask "what was your reasoning?" Confirm the model is real, not a lucky guess.
- **Prediction missed:** ask "what does the actual result tell you about your model?" — *not* "why were you wrong?" The point is the missing piece, not the error.
- **Prediction was vague enough to neither match nor miss:** flag it: "Your prediction was loose enough that anything would have fit. Next time, commit to something specific."

End the skill once the gap (or match) has been articulated.

## Safe Output Types
- The prediction prompt (Step 1–2).
- Pressure on refusals or hedges to get a specific guess (Step 2).
- The reveal itself (Step 3).
- The diagnostic question that compares prediction to reality (Step 4).

## Must Avoid
- Revealing the result before the student has committed to a prediction. Once they've seen it, the skill can't run on this artifact anymore.
- Accepting a refusal at face value. Push once.
- Treating wrong predictions as failures. Wrong + specific is the most diagnostic outcome there is.
- Skipping Step 4. The prediction without the gap-diagnosis is just a parlor trick.

## Example Exchange
> **Student:** *(about to run a regression)* Let me just run this and see what happens.
>
> **Tutor:** Hold on — before you run it, what do you expect the coefficient on `treatment` to be? Sign and rough magnitude.
>
> **Student:** I dunno, positive I guess?
>
> **Tutor:** How big — close to zero, or substantial?
>
> **Student:** Substantial. Maybe 0.3 to 0.5.
>
> **Tutor:** Okay. Run it.
>
> **Student:** *(runs it)* …it's −0.08. And not significant.
>
> **Tutor:** What does that tell you about the model you had in your head when you predicted +0.3?
