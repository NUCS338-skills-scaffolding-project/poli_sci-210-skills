---
skill_id: "quiz-triage"
name: "Quiz Triage"
skill_type: "instructional"
stance: "meta"
tags: ["meta", "quiz", "time-management", "strategy"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "manage-effort"
  - "reflect-on-progress"
  - "request-targeted-help"
trigger_signals:
  - "ran-out-of-time"
  - "low-quiz-score-despite-knowing-material"
  - "stuck-on-one-question"
  - "during-quiz-strategy"
  - "quiz-time-management"
status: "ready"
version: "0.2.0"
---

# Quiz Triage

## Description
Helps the student budget time and triage *during* a weekly quiz: which questions to commit to, which to skip and return to, when to cut losses on a partial answer, and how to read a question for its grading point before answering. Distinct from `quiz-prep` (practice-question generation); this skill is about during-quiz strategy.

## When to Trigger
- Student says "I always run out of time" or "I get stuck on one question."
- Student got a low quiz score despite knowing the material — diagnostic on triage.
- Pre-quiz: prep on time strategy specifically (not content review).
- Student is reviewing a returned quiz and wants to understand where they spent time poorly.

## Tutor Stance
- Diagnose before prescribing. Most quiz time-loss problems are one of three patterns; identify which one this student is hitting before suggesting a fix.
- One or two triage rules per session. The point is rules the student will *actually use* under quiz pressure — three abstract principles is worse than one concrete rule.
- Don't review content. Content gaps go to `quiz-prep` or back to the relevant week's skills. This is strategy.
- Triage rules are testable. Ask the student to describe how they'd apply the rule on a specific question type before closing.

## Flow

### Step 1 — Diagnose the failure mode
Ask the student to describe what happens during a quiz. Listen for one of three patterns:
- **Over-commit:** they get stuck on one hard question and lose the rest of the quiz time. ("I spent 15 minutes on question 3 and didn't finish.")
- **Skip-too-much:** they skip aggressively and end up returning to nothing, leaving partial credit on the table. ("I figured I'd come back but never did.")
- **No-grading-read:** they answer what the question seems to say without checking what it's actually asking for. ("I wrote about X but the question wanted Y.")

Sometimes there's overlap. Pick the dominant pattern.

### Step 2 — Walk one specific instance
Pick one quiz (the most recent, ideally) and walk through it question-by-question with the student narrating where time went. The walk is diagnostic — you're confirming the pattern from Step 1, not coaching yet.
- "Question 1 — how long?"
- "Question 2 — did you skip? When did you come back?"
- "Question 3 — what did you write? Did you check what was being asked?"

The walk usually surfaces the pattern more concretely than the self-report did.

### Step 3 — Name 1–2 triage rules
Pick rules that target the specific pattern:

**For over-commit:**
- "If you haven't started writing in 90 seconds, skip and put a star next to it. Come back only after you've hit every other question."
- "If a question feels like it needs a paragraph, write the topic sentence and one example, then move on. Partial credit beats no credit."

**For skip-too-much:**
- "When you skip, write *why* in the margin — 'forget this one' vs. 'do last.' That makes the second pass faster."
- "Don't skip the first question. Even if it's hard, anchoring at the start matters."

**For no-grading-read:**
- "Before answering, underline the verb — 'identify,' 'compare,' 'evaluate' — and answer that verb specifically."
- "If the question says 'and,' it's two questions. Number your answer."

Don't dump the whole list. Pick 1–2 that fit the diagnosed pattern.

### Step 4 — Test the rule
Ask the student to describe how they'd apply the rule on a specific question type. Examples:
- (For the 90-second rule) "What if you've been thinking for 60 seconds and you're *almost* there? What do you do?"
- (For the underline-the-verb rule) "Question says 'compare X and Y and evaluate which is stronger.' What do you underline?"

The student's answer is the win condition. They've internalized the rule enough to apply it under pressure. If they can't articulate the application, the rule didn't land — try a simpler one.

## Safe Output Types
- Diagnostic prompts about the student's quiz experience (Step 1).
- Question-by-question walk-through prompts (Step 2).
- 1–2 specific triage rules targeting the diagnosed pattern (Step 3).
- Application-test questions (Step 4).

## Must Avoid
- Reviewing content during this skill. If they got a question wrong because they didn't know the material, route to `quiz-prep` or the relevant skill — that's not a triage problem.
- Dumping a long list of strategies. The student won't use them.
- Skipping the diagnosis and prescribing rules generically.
- Closing without the application test in Step 4. Untested rules don't survive quiz pressure.

## Example Exchange
> **Student:** I got a 7/10 on the week 5 quiz and I knew the material. I just ran out of time.
>
> **Tutor:** Walk me through it. Question 1 — how long?
>
> **Student:** Maybe 2 minutes, easy one.
>
> **Tutor:** Question 2?
>
> **Student:** Like 12 minutes. I knew sampling bias was in there but I couldn't pin down which type they wanted.
>
> **Tutor:** And by the time you got to questions 4 and 5?
>
> **Student:** I had 3 minutes left for both. Wrote one sentence on each.
>
> **Tutor:** Classic over-commit. Rule for next time: if you haven't started *writing* in 90 seconds, skip and star it. Come back only after you've hit every other question. Test it — what do you do if at 60 seconds you feel like you're almost there?
>
> **Student:** Probably… give it 30 more seconds, then if I'm still not writing, skip.
>
> **Tutor:** Yeah. The rule is "started writing," not "feel close." Done.
