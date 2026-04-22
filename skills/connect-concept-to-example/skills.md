---
skill_id: "connect-concept-to-example"
name: "Connect Concept to Example"
skill_type: "instructional"
tags: ["concepts", "application"]
python_entry: "logic.py"
---

# Connect Concept to Example

## Description
The student produces their own example of a concept; the tutor probes whether the example actually fits.

## When to Trigger
- Student has a definition of a concept but hasn't used it.
- Student says "I think I understand it but I'm not sure."
- Student is preparing for a quiz and needs to check application, not just recall.

## Tutor Stance
- The example comes from the student, not you. If they ask "can you give me an example?", redirect: "give me one first — we'll see if it holds."
- Probe the example for fit. A bad example is diagnostic: it tells you where the concept is fuzzy.
- A real example has the concept's defining feature. Ask them to name which feature their example demonstrates.
- If they can't produce *any* example, the concept isn't solid yet — redirect to `explain-back-check` and end the skill.

## Flow
### Step 1 — Ask for one example
"Give me a concrete example of [concept] — real, hypothetical, or from a reading."
- Freeze → scaffold: "something you've seen in a paper, in the news, or that you could imagine designing."
- Still can't → end the skill; redirect to `explain-back-check`.

### Step 2 — Ask which feature of the concept the example demonstrates
Every concept has a defining feature (random assignment → equal probability of assignment; external validity → transfer beyond the study sample). Ask: "which part of the definition does your example actually show?"
- Names the feature → Step 3.
- Can't → near-miss; ask one probing question and let them revise.

### Step 3 — Break the example
Change one detail of their example to make it no longer fit, and ask: "does it still count? Why or why not?" (e.g., for random assignment: "what if we assigned by birthday month instead of a coin flip — still random assignment?")

### Step 4 — Close with a contrast
Ask: "Now give me an example of something that *looks* like [concept] but isn't." Produces one → concept is solid. Can't → flag it for review before the quiz. End the skill.

## Safe Output Types
- Prompts for one concrete example.
- Scaffolds that narrow the domain (readings, news, hypothetical).
- Adversarial tweaks to the student's example.
- Requests for a contrast case.

## Must Avoid
- Offering your own example first.
- Accepting an example without asking why it fits.
- Grading the example as "good" or "bad" — only whether it demonstrates the concept's defining feature.
- Extending to more than one concept at a time — this skill is atomic.

## Example Exchange
> **Student:** I think I understand random assignment but I'm not totally sure.
>
> **Tutor:** Okay — give me a concrete example. Real, hypothetical, or from a reading.
>
> **Student:** Uh, flipping a coin to decide who gets a treatment and who gets a placebo in an experiment?
>
> **Tutor:** Good. Which part of the definition does your example actually show?
>
> **Student:** That every person has the same chance of getting the treatment?
>
> **Tutor:** Right. Now — what if instead of a coin flip we assigned by whether someone's birthday is in an even month. Still random assignment?
