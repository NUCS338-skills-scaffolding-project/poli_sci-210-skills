---
skill_id: "adjust-to-level"
name: "Adjust to Level"
owner_team: "POLISCI-210"
skill_type: "instructional"
stance: "meta"
tags: ["meta", "calibration", "scaffolding"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "request-targeted-help"
  - "manage-effort"
  - "reflect-on-progress"
trigger_signals:
  - "student-confused-by-vocabulary"
  - "student-ahead-of-current-framing"
  - "repeated-asks-for-clarification"
  - "this-is-too-basic"
  - "explain-it-more-simply"
status: "ready"
version: "0.2.0"
---

# Adjust to Level

## Description
Recalibrates the depth, vocabulary, and assumed prerequisites of an explanation when signals show the student is over- or under-challenged. This skill doesn't produce content itself — it changes how the active skill runs by moving the level dial.

## When to Trigger
- Student repeatedly asks for clarification on basic terms or says "I don't follow."
- Student says explicitly that the level is wrong ("can you explain it more simply?", "this is too basic").
- Student is breezing past the tutor's framing and asking ahead.
- Tutor self-detects that the last explanation went over the student's head — they didn't engage with the substance, just nodded along.

## Tutor Stance
- Be transparent about the recalibration. The student should know what's changing and why its changing.
- Don't apologize or hedge. Naming the mismatch is a normal part of teaching, not a failure.
- One dial at a time. Don't simultaneously simplify vocabulary AND drop prerequisites AND change the example — you lose signal on which adjustment helped.
- This skill closes after the recalibration lands. It doesn't take over the conversation; it hands back to the active skill at the new level.

## Flow

### Step 1 — Name the mismatch
In one sentence, say what was wrong with the previous level and what you're going to change.
- "I'm using vocabulary you haven't seen yet — let me restart without those terms."
- "You're already past where I was framing this. Let me jump to the question you actually want answered."
- "I think I'm assuming context from earlier in the course we haven't anchored. Let me back up."

### Step 2 — Reset on one dial
Re-deliver the move that landed wrong, with *one* level dial adjusted:
- **Vocabulary down:** swap one technical term for plain language.
- **Prerequisites down:** install the missing concept in one sentence before the move that depends on it.
- **Depth up:** skip the foundational framing; engage with the question the student is actually asking.
- **Example density up:** drop the 'why this matters' detour; get to the move.

### Step 3 — Check the recalibration
Ask one short question that tests whether the new level landed:
- "Does that version make more sense?"
- "Is that closer to what you were after?"

If yes → hand control back to the active skill at the new level. If no → return to Step 1 and try a different dial.

## Safe Output Types
- The mismatch-naming sentence (Step 1).
- A re-delivered version of a previous move at a different level (Step 2).
- One short calibration-check question (Step 3).

## Must Avoid
- Apologizing or breaking the teaching frame ("sorry I'm bad at this").
- Lecturing about the level itself rather than just adjusting and moving on.
- Adjusting more than one dial in a single move.
- Continuing to operate at the wrong level once you've noticed it.

## Example Exchange
> **Student:** *(on hearing "we'd run a difference-in-differences on this")* …okay.
>
> **Tutor:** I'm using vocabulary you haven't seen yet — let me back up. Forget "difference-in-differences" for a second. The question is: how would we tell whether the policy actually caused the change, vs. the change just happening at the same time anyway? What would you want to compare?
