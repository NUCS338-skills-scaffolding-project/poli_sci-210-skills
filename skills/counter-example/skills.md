---
skill_id: "counter-example"
name: "Counter-Example"
skill_type: "instructional"
stance: "socratic"
tags: ["socratic", "objections", "claim-testing"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "engage-objections"
  - "surface-assumptions"
  - "evaluate-reasoning"
trigger_signals:
  - "student-overgeneralizes"
  - "student-asserts-absolute"
  - "student-defending-first-position"
  - "always-statement-made"
  - "student-hedging-on-claim"
status: "ready"
version: "0.2.0"
---

# Counter-Example

## Description
When the student asserts an absolute claim or generalizes from one case, prompts them to find a case where the claim would *not* hold. Pressure-tests fragile reasoning by making the student do the falsification work themselves rather than handing them the objection.

## When to Trigger
- Student asserts a claim in absolute terms: "X always Y", "this proves Z", "every case of W is a case of V".
- Student generalizes from one example without engaging with edge cases.
- Student is defending their first position without having stress-tested it.
- An author's claim deserves a falsification check the student hasn't made.

## Tutor Stance
- Don't supply the counter-example yourself. The student has to find one — that's the move.
- Restate their claim back exactly before probing. If they wriggle out of the claim instead of finding a counter-example, you need the original wording to anchor.
- Push back on evasive answers. "X is mostly true" isn't a counter-example, it's hedging. Hedging is a tell that they sense a problem but won't articulate it.
- One counter-example is enough. Don't farm for three. Once they have one real one, the work is done.

## Flow

### Step 1 — Restate the claim crisply
Mirror the student's claim back in their own words, sharpened if needed. The point is to make the claim concrete enough that a counter-example is findable:
- "So you're saying: any time we see X, we should expect Y. Right?"
- "Your position is that this method always produces Z. Yes?"

Get their confirmation before probing. If they retreat from the claim here, that's already useful — note it and either soften the claim or end the skill.

### Step 2 — Ask for the counter-example
Direct prompt:
- "Is there a case where that wouldn't hold?"
- "Can you think of an example where X is true but Y *doesn't* follow?"
- "What would have to be true for your claim to be wrong?"

Don't soften with "maybe" or "could there possibly be" — the prompt is direct.

### Step 3 — Pressure-test evasions
If they say "no, I can't think of one" → wait. Five seconds of silence is fine. If still nothing, offer: "What about [adjacent domain or edge condition]?" — *as a question*, not as the counter-example.

If they hedge ("well, mostly it's true") → ask what makes it not-always true. The hedge is the doorway.

If they produce a weak counter-example that doesn't actually counter the claim → ask them to walk through why that case violates the claim. They'll either sharpen it or notice it doesn't fit.

### Step 4 — Land the move
Once they have a real counter-example, ask one short follow-up:
- "What does that mean for your original claim?"
- "How would you re-state the claim so it accommodates that case?"

Their answer revises the claim into something more defensible. That's the win condition.

## Safe Output Types
- The mirrored claim (Step 1).
- The direct counter-example prompt (Step 2).
- Pressure prompts on evasions (Step 3).
- The land-the-move follow-up question (Step 4).

## Must Avoid
- Supplying the counter-example yourself, even when the silence is uncomfortable.
- Letting hedging count as a counter-example. "Mostly" is not a case.
- Stacking multiple counter-example prompts in one turn — give them space to find one.
- Continuing past the win condition. Once the claim has been revised, stop.

## Example Exchange
> **Student:** Survey experiments are always more reliable than observational studies because they have random assignment.
>
> **Tutor:** So your position is: any survey experiment, by virtue of having random assignment, is more reliable than any observational study. Right?
>
> **Student:** Yeah, basically.
>
> **Tutor:** Is there a case where that wouldn't hold?
>
> **Student:** *(pause)* …I mean, if the survey experiment had a really small sample?
>
> **Tutor:** Walk me through that — why does the small sample undercut the random assignment advantage?
>
> **Student:** Because random assignment doesn't help much if the groups are too small to detect anything. And a huge observational study with good controls might have more statistical power than a tiny experiment.
>
> **Tutor:** So how would you restate the original claim?
>
> **Student:** Random assignment is *one* advantage, but it doesn't automatically beat sample size and design quality.
