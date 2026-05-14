---
skill_id: "session-reflect"
name: "Session Reflect"
skill_type: "instructional"
stance: "meta"
tags: ["meta", "metacognition", "reflection"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "reflect-on-progress"
  - "manage-effort"
  - "request-targeted-help"
trigger_signals:
  - "session-wrapping-up"
  - "chain-just-completed"
  - "pre-quiz-or-section"
  - "end-of-session-reflection"
  - "session-wrap-up-questions"
status: "ready"
version: "0.2.0"
---

# Session Reflect

## Description
At the end of a working session, prompts the student to articulate what they actually learned, what stayed unclear, and what they'd do differently next time. Produces a short reflection log they can carry into the next session. Distinct from any individual skill's "Completion Notes" — this consolidates *across* skills and across the session.

## When to Trigger
- Session is wrapping up (student says "I think I'm good," "let's stop").
- Student finished an assignment or completed a skill chain.
- Student is about to walk into a quiz or section and wants to know where they stand.
- Tutor wants to consolidate a long working session before the conversation ends.

## Tutor Stance
- Three short prompts, in order. Don't combine them.
- The student names the learning. You don't summarize the session for them.
- Specific over general. "I learned about regression" is not an answer; "I learned that a coefficient on a 0–1 outcome means percentage-point change" is.
- The reflection log is the deliverable. It's not just for the conversation — the student should be able to re-read it before the next session and pick up where they left off.

## Tutor Pre-Read & Notes
Before opening the skill, glance back over the conversation (or the session log files written by other orchestrators) to identify 2–3 candidate learning moments — things you noticed the student get unstuck on, sharpen, or recognize for the first time. Don't deliver this list at them; it's a diagnostic against which to judge whether their answers are landing on real learning vs. performing reflection.

Write the reflection log to a path the student can find again before the next session.

**Default path** (resolved from `paths.student_session_log_pattern` in `metadata.yaml`):

```
students/<student>/session-logs/<YYYY-MM-DD>-<short-topic>.md
```

**Adopter fallback ladder** — pick the highest tier that works in your host:

1. If `students/<student>/session-logs/` exists or can be created and `<student>` is set → use the default.
2. Else if cwd is writable → write to `./session-logs/<YYYY-MM-DD>-<short-topic>.md` (creating the directory if needed).
3. Else if no project-relative directory is writable → write to `/tmp/session-reflect-<YYYY-MM-DD-HHMM>-<short-topic>.md` and tell the student that's where it landed.

Whichever tier you use, surface the actual path to the student in the closing message — the log is the deliverable, not a hidden artifact.

Note: the path is under `students/` (or its fallback) rather than `skills/.../scratch/`. The reflection log persists across sessions and is the student's, not a skill's internal scratchpad.

Structure:
```
# Session Reflection — <student> — <YYYY-MM-DD>

## What we worked on
- <skill or assignment>: <one-line context>
- ...

## What became clearer
1. <student's articulation, in their own words>
2. ...

## What stayed murky
1. <student's articulation>
2. ...

## What I'd do differently next time
- <student's articulation>

## Open todos for next session
- <derived from the murky list>
```

## Flow

### Step 1 — Set the frame
One short opener:
> "Before we wrap, three quick reflection questions. Don't overthink them — short answers are fine."

### Step 2 — What became clearer
Ask: "What's one specific thing that became clearer today?" Push for specificity if vague:
- "I learned about X" → "What specifically about X? What can you do now that you couldn't this morning?"
- "I'm not sure" → "Pick the smallest thing. Even one sentence is fine."

If the student can't name anything, that's diagnostic — flag it gently: "If nothing became clearer, that's worth knowing too. We should probably revisit what we worked on." Then end the skill without writing a misleading log.

### Step 3 — What stayed murky
Ask: "What's one thing that stayed unclear, or that you noticed you didn't really understand?" The murky list is more valuable than the clarity list — it becomes the next session's todos.

If they say "nothing," push: "Something always stays unclear after a real working session. What was the closest thing to a snag?"

### Step 4 — What you'd do differently
Ask: "What would you do differently next time you're working on something like this?" Forward-looking, not retrospective. Examples of valid answers:
- "I'd read the methods section before the results next time."
- "I'd write out my prediction before running the regression."
- "I'd start the RDC by mapping the design before forming the critique."

### Step 5 — Write the log + close
Write the reflection log to the path you resolved per the **Tutor Pre-Read & Notes** ladder (default: `students/<student>/session-logs/<date>-<topic>.md`; cwd or `/tmp/` fallback if the default isn't available). Show the student the actual path:

> "Reflection saved at `<path>`. Re-read it before next session to pick up where you left off."

Close. Don't summarize the session beyond what's already in the log.

## Safe Output Types
- The frame-setting opener (Step 1).
- The three reflection questions, one per turn (Steps 2–4).
- Specificity prompts when answers are vague.
- The log-write confirmation with the path (Step 5).

## Must Avoid
- Summarizing the session for the student.
- Combining the three questions into one.
- Accepting "I learned a lot" or "everything became clearer" as a substantive answer.
- Writing the reflection log with content the student didn't say.
- Triggering this skill more than once per session.

## Example Exchange
> **Student:** Okay I think I'm good for tonight.
>
> **Tutor:** Before we wrap, three quick reflection questions. What's one specific thing that became clearer today?
>
> **Student:** That a coefficient of 0.32 on a 0–1 vote share variable means a 32-point swing, not a 32-percent swing. I had that wrong all evening.
>
> **Tutor:** Good. What stayed murky?
>
> **Student:** I still don't really get what a confidence interval is doing. I can read one but I couldn't explain what the 95% means.
>
> **Tutor:** What would you do differently next time?
>
> **Student:** Probably ask about CIs at the start of a stats reading instead of bluffing past them.
>
> **Tutor:** Reflection saved at `students/<student>/session-logs/2026-05-04-rdc-week-9.md`. Re-read it before next session.
