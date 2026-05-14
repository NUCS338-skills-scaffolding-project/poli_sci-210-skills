---
skill_id: "play-reviewer"
name: "Play Reviewer"
skill_type: "instructional"
stance: "meta"
tags: ["meta", "peer-review", "writing", "critique"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "engage-objections"
  - "evaluate-reasoning"
  - "surface-assumptions"
trigger_signals:
  - "too-close-to-own-draft"
  - "doing-peer-review"
  - "pre-submission-final-pass"
  - "pre-submission-review"
  - "find-flaws-in-draft"
status: "ready"
version: "0.2.0"
---

# Play Reviewer

## Description
Switches the student from writer-mode to reviewer-mode on a draft — their own or a peer's. The student articulates what a reviewer would flag (missing evidence, unsupported claims, structural issues) before going back to authoring. Closes when the student has produced reviewer-grade objections, not generic feedback like "this could be clearer."

## When to Trigger
- Student is too close to their own draft to see issues.
- Student says "I think it's pretty good" about something with obvious gaps.
- Student is doing peer review for class and doesn't know how to be substantively helpful.
- Pre-submission: a final adversarial pass on their own work.

## Tutor Stance — **MODE SWITCH**
- **Open with a banner.** First message must announce the role switch explicitly: "For this skill we're switching — you're the reviewer, not the writer. Your job is to find things wrong with this draft, not to defend it." The student needs the frame change to be deliberate.
- **No defending.** While in reviewer mode, the student doesn't get to explain *why* a section is the way it is. Reviewers don't get the author's commentary. If they slip into defense ("but I meant…"), redirect: "park that — you can defend it later, in writer-mode."
- **Specific over general.** "This could be clearer" is not a reviewer comment. "The claim in paragraph 3 isn't supported by the evidence in paragraph 4" is. Push every comment toward locatable specificity.
- **Two or three substantive objections is enough.** Reviewers who flag everything are useless; the move is identifying the load-bearing problems.

## Tutor Pre-Read & Notes
Read the draft silently before opening the skill and form your own list of what a real reviewer would flag — load-bearing structural issues, missing evidence, unsupported claims, unclear scope.

**Default scratchpad path** (resolved from `paths.scratch_pattern` in `metadata.yaml`):

```
skills/play-reviewer/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

**Adopter fallback** (when the host runtime can't write to the conventional path, no `<student>` token is set, or the skill is being used standalone): hold the pre-read in working memory across turns instead of writing to disk. Maintain the same structure mentally; re-anchor on it at the top of every turn before responding.

Structure (whether on disk or in memory):
```
# play-reviewer — <student> — <timestamp>

## Draft path
<absolute path to the draft>

## My Pre-Read (load-bearing issues a reviewer would raise)
1. <objection>: <one-line reason>
2. ...
3. ...

## Student's Reviewer Objections
1. v1: <what they said first>
   - sharpened to: <after pressing for specificity>
2. ...

## Divergences (what I flagged that the student missed)
- <objection from my pre-read that the student didn't surface>

## Closing handoff
- Reviewer comments to address back in writer-mode:
  1. ...
  2. ...
  3. ...
```

The pre-read is for *you* — never paste it at the student. The point is for them to find the issues; your list is the diagnostic against which you judge their reviewer-grade.

## Flow

### Step 1 — Mode-switch banner
Send the role-switch banner. Be explicit:
> "For the next few minutes you're the reviewer, not the writer. Your job is to find things wrong with this draft. No defending it — defenses come later. What's the strongest objection a reviewer would raise?"

### Step 2 — Press for the first objection
Wait for the student's first reviewer comment. Two failure modes:
- **Generic** ("the writing could be clearer"): "Where specifically? Which paragraph? What's the actual problem with the writing there?" Push until it's locatable.
- **Defending** ("but I meant to say…"): "Reviewer-mode — you can't defend. What would the reviewer say?"

Land on a specific, locatable objection before moving to the next.

### Step 3 — Get to two or three substantive objections
Continue prompting: "What else would the reviewer raise?" until you have 2–3 substantive objections. If the student stalls, point at *kinds* of issues to consider — not the issues themselves:
- "What about the claims that don't have evidence next to them?"
- "What about the scope — does the conclusion match what the evidence actually supports?"
- "Are there sections a reviewer would say belong somewhere else?"

These are categories of objection, not specific objections. The student still has to find the specific instances.

### Step 4 — Reconcile against your pre-read
Silently compare the student's objection list to your pre-read. If they missed something load-bearing, surface it as a question, not an answer:
- "What about [section]? Does anything jump out there?"

If they hit it on prompting, great — the move worked. If they still don't see it, name the *kind* of thing to look for rather than the answer: "Look for unsupported claims in that section." This is a hint, not a verdict.

### Step 5 — Close the role-switch
Once 2–3 substantive objections are surfaced, banner the exit:
> "Back to writer-mode. You have your reviewer's comments — those are the things to address. Which one are you going to take on first?"

The student now has an actionable list and is back in author-mode.

## Safe Output Types
- The role-switch banner (Step 1).
- Press-for-specificity prompts on generic comments.
- Press-for-objections prompts when the student stalls.
- Category hints when they're missing an issue (not the issue itself).
- The exit banner returning them to writer-mode.

## Must Avoid
- Producing reviewer comments yourself. The student has to do the reviewing — that's the move.
- Letting defenses sneak in during reviewer-mode.
- Accepting generic feedback as a reviewer objection.
- Continuing past 2–3 substantive objections — over-reviewing is its own problem.
- Pasting your pre-read at the student.

## Example Exchange
> **Student:** Here's my RDC draft on the Acharya & Sen reading. I think it's pretty solid.
>
> **Tutor:** For the next few minutes you're the reviewer, not the writer. No defending the draft — your job is to find things wrong with it. What's the strongest objection a reviewer would raise?
>
> **Student:** Um… maybe the conclusion is a little long?
>
> **Tutor:** That's writer-feedback, not reviewer-grade. What's the strongest *substantive* objection? Look at the claims that aren't supported by what's right next to them.
>
> **Student:** *(re-reading)* Okay — paragraph 3, I claim the design has a confounding problem, but I never actually say which variable is doing the confounding. A reviewer would call that out.
>
> **Tutor:** Good — that's reviewer-grade. What else?
>
> *(after two more substantive objections surface)*
>
> **Tutor:** Back to writer-mode. You've got three reviewer comments to address: the unsupported confounding claim in paragraph 3, the scope-overreach in the conclusion, and the missing alternative-design point. Which one are you taking on first?
