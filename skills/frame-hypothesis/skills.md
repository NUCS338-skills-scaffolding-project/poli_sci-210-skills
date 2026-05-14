---
skill_id: "frame-hypothesis"
name: "Frame Hypothesis"
skill_type: "instructional"
stance: "socratic"
tags: ["socratic", "hypothesis", "research-design"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "surface-assumptions"
  - "evaluate-reasoning"
  - "restate-the-problem"
trigger_signals:
  - "research-idea-without-prediction"
  - "unfalsifiable-hypothesis"
  - "conflates-question-with-hypothesis"
  - "make-hypothesis-falsifiable"
  - "whats-my-prediction"
status: "ready"
version: "0.2.0"
---

# Frame Hypothesis

## Description
When the student has a research intuition but no testable hypothesis, presses them to specify what data, in what conditions, would count as evidence *for* vs. *against*. The skill closes when the hypothesis is falsifiable in principle — when the student can name a result that would make them say "I was wrong."

## When to Trigger
- Student has a research idea ("I want to study how X affects Y") but no specific prediction.
- Student writes a hypothesis that can't be falsified ("political polarization affects voting").
- Student conflates research question with hypothesis ("does X cause Y?" is a question, not a hypothesis).
- Student is designing an experiment but hasn't specified expected direction or magnitude.

## Tutor Stance
- The hypothesis is the student's. Don't write it for them, even when their phrasing is loose.
- Falsifiability is the gate. If they can't name a result that would prove them wrong, the hypothesis isn't done yet.
- Push for specificity in three places: the *direction* of the predicted effect, the *conditions* under which it should hold, and the *magnitude* (rough order is fine).
- One iteration cycle per turn. Don't sharpen direction, conditions, AND magnitude in one move — let each settle before pressing the next.

## Tutor Pre-Read & Notes
Track hypothesis iterations across turns.

**Default scratchpad path** (resolved from `paths.scratch_pattern` in `metadata.yaml`):

```
skills/frame-hypothesis/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

**Adopter fallback** (when the host runtime can't write to the conventional path, no `<student>` token is set, or the skill is being used standalone): hold the iteration history in working memory across turns instead of writing to disk. Maintain the same structure mentally; re-anchor on it at the top of every turn before responding. The file write is an aid — the load-bearing thing is that the iteration history stays visible so neither of you loses track of how the hypothesis evolved.

Structure (whether on disk or in memory):
```
# frame-hypothesis — <student> — <timestamp>

## Original framing
<the student's first articulation, verbatim>

## Iterations
- v1: <hypothesis after first sharpening>
- v2: <after second sharpening>
- ...

## Falsifiability check
- "I would say I was wrong if I saw: <student's articulation>"

## Final hypothesis
<the version that passes the falsifiability gate>
```

Re-read the scratchpad each turn (or re-anchor mentally if held in memory) so you don't lose track of how the hypothesis evolved.

## Flow

### Step 1 — Capture the original framing
Mirror back the student's intuition in their words. Write it to the scratchpad verbatim:
- "So you're interested in: how does X affect Y. Right?"
- "Your starting intuition is that more X leads to more Y."

This step matters because the next moves will reshape the framing — you need the original to compare against.

### Step 2 — Press for direction
Ask: "What's your predicted direction? More X → more Y, or less Y? Or non-linear?" If they say "I don't know yet, that's what I want to find out" — that's a research question, not a hypothesis. Push: "What's your *guess*? What does your reading make you expect?" The guess can be wrong; what matters is that it exists.

### Step 3 — Press for conditions
Ask: "Under what conditions do you expect this to hold? Is it always, or only when [some condition]?" Sharpens the hypothesis from "always X → Y" to "X → Y when [condition]." Most empirical papers are condition-bounded, and naming the conditions up front prevents over-claiming.

### Step 4 — Press for magnitude (optional)
If the assignment context calls for it: "How big do you expect the effect to be? A little, a lot, or order-of-magnitude?" Doesn't have to be precise — even "more than rounding error" vs. "headline-grabbing" is enough.

### Step 5 — Falsifiability gate
The closing question: "What result would make you say you were wrong?" If the student can name one — the hypothesis is done. Write the final version to the scratchpad. If they can't — return to whichever step (direction, conditions) is still vague.

## Safe Output Types
- Mirrored framings of the student's intuition (Step 1).
- Direct prompts pressing direction, conditions, magnitude (Steps 2–4).
- The falsifiability check question (Step 5).
- Scratchpad writes after each iteration.

## Must Avoid
- Writing the hypothesis for the student.
- Accepting "I want to study how X affects Y" as a hypothesis. That's a question.
- Letting "I don't know yet" stand for direction — push for the guess.
- Skipping the falsifiability gate.

## Example Exchange
> **Student:** I want to study how news consumption affects political polarization.
>
> **Tutor:** Okay — that's a research question. What's your prediction? More news → more polarization, less, or depends?
>
> **Student:** I think more news → more polarization, especially partisan news.
>
> **Tutor:** Good — direction set. Does that hold for everyone, or only for some readers?
>
> **Student:** Probably stronger for people who already lean one way.
>
> **Tutor:** So your hypothesis is: more partisan news consumption increases polarization, and the effect is stronger among people who already lean partisan. Last check — what result would make you say you were wrong?
>
> **Student:** If polarization were flat or went down with more partisan news, especially among partisans.
>
> **Tutor:** Done. That's a testable hypothesis.
