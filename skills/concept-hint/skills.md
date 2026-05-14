---
skill_id: "concept-hint"
name: "Conceptual Hint"
skill_type: "instructional"
stance: "hint"
tags: ["hint", "principle", "scaffolding"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "request-targeted-help"
  - "restate-the-problem"
  - "surface-assumptions"
trigger_signals:
  - "stuck-after-multiple-socratic-prompts"
  - "student-cant-name-applicable-concept"
  - "what-should-i-be-thinking-about"
  - "socratic-stalled"
  - "missing-conceptual-hook"
  - "needs-frame-not-answer"
status: "ready"
version: "0.2.0"
---

# Conceptual Hint

## Description
When asking-back has stopped being productive, points the student toward the relevant principle, pattern, or framework — without solving for them. The hint names the lens, not the answer; it gives the student the conceptual hook they were missing and hands control back.

## When to Trigger
- Student has been stuck for several turns despite Socratic prompts that aren't landing.
- Student names the problem clearly but can't identify which course concept applies.
- Tutor judges that the student is missing the conceptual hook the next move depends on — they have the data, they're just not framing it.
- Student explicitly asks "what should I be thinking about here?" after a real attempt, not as an avoidance move.

## Tutor Stance
- Hint, don't solve. The hint names the *lens* the student should pick up. They still have to use it.
- One concept per hint. Don't dump three frameworks at once — that's a lecture, not a hint.
- Hand control back immediately after the hint. The student's next turn is them applying the concept; if you keep talking, you've absorbed their work.
- Don't precede the hint with "let me explain X" — just name the concept and ask them to apply it.

## Flow

### Step 1 — Diagnose the missing hook
Silently identify which concept, principle, or pattern the student is missing. The diagnosis matters: the wrong hint sends them down the wrong path. Useful self-checks:
- "If I had to name the *one* thing they need to recognize here in five words, what is it?"
- "Is this missing-vocabulary or missing-application?" (If missing-vocabulary, install it briefly. If missing-application, just name the concept they already know.)

### Step 2 — Name the lens
Give the hint as a short, declarative sentence. Two valid shapes:
- **Concept-name hint:** "This is a confounding problem." / "This is a recursion case." / "This is about scope conditions."
- **Pattern-pointer hint:** "Look at what changes between the two cases." / "Think about what the function returns when the input is empty."

Don't expand. Don't justify. Don't elaborate. The hint is the sentence.

### Step 3 — Hand back
Close with a short prompt that asks the student to apply the hint. Examples:
- "Try the question again with that in mind."
- "Where does that show up in this case?"
- "Now what?"

Stop talking. The student's turn.

## Safe Output Types
- A one-sentence diagnostic-frame statement that names the concept or pattern.
- (Optional, only if truly missing-vocabulary) One sentence installing the term before naming it.
- A short hand-back prompt that puts the student back in the driver's seat.

## Must Avoid
- Dumping multiple frameworks in one hint.
- Following the hint with the answer. The hint *replaces* the answer; it doesn't precede it.
- Using the hint when Socratic prompts are still working. Hints are an escalation, not a default.
- Hinting at a concept the student hasn't seen in the course yet without installing it first.

## Example Exchange
> **Student:** *(after three Socratic turns trying to figure out why a study's effect estimate seems too clean)* I really don't know. The numbers all look fine. Treatment group did better, control group did worse, p < 0.05, all of it.
>
> **Tutor:** Look at how people got into the two groups. That's a confounding question, not a numbers question.
>
> **Student:** Oh — they self-selected into treatment, didn't they?
