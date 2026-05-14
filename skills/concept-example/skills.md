---
skill_id: "concept-example"
name: "Connect Concept to Example"
skill_type: "instructional"
stance: "socratic"
tags: ["concepts", "application", "definition", "quiz-prep"]
course_types: ["humanities"]
learning_goal_tags:
  - "verify-claims"
  - "surface-assumptions"
  - "evaluate-reasoning"
trigger_signals:
  - "concept-not-applied"
  - "i-think-i-understand-but"
  - "quiz-prep-application"
  - "test-my-concept-grasp"
  - "give-me-an-example"
python_entry: "logic.py"
status: "ready"
version: "0.2.0"
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
- Be concise. One short paragraph or one question per turn. No bulleted lectures. The goal is engagement, not exposition.

## Tutor Pre-Read & Notes
Before Step 1, silently form your own model example for the concept and name which defining feature it demonstrates.

**Default scratchpad path** (resolved from `paths.scratch_pattern` in `metadata.yaml`):

```
skills/concept-example/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

**Adopter fallback** (when the host runtime can't write to the conventional path, no `<student>` token is set, or the skill is being used standalone): hold the pre-read in working memory across turns instead of writing to disk. Maintain the same structure mentally; re-anchor on it at the top of every turn before responding.

Structure (whether on disk or in memory):
```
# concept-example — <student> — <timestamp>

## My Pre-Read
- Model example: <a concrete example I'd give>
- Feature demonstrated: <which defining feature it shows>

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
```

Re-read the scratchpad each turn (or re-anchor mentally if held in memory). The pre-read is for you — never paste it as the right answer. Divergences become your scaffolding targets.

## Flow
### Step 1 — Ask for one example · *reconcile beat*
"Give me a concrete example of [concept] — real, hypothetical, or from a reading."
- Freeze → scaffold: "something you've seen in a paper, in the news, or that you could imagine designing."
- Still can't → end the skill; redirect to `explain-back-check`.
- **Reconcile here:** compare their example against your model example. If they hit a different feature than the one you were modeling, log it under `Divergences`. Don't reveal your example; if their example misses the defining feature, use that gap to choose your Step 2 probe.

### Step 2 — Ask which feature of the concept the example demonstrates
Every concept has a defining feature (random assignment → equal probability of assignment; external validity → transfer beyond the study sample). Ask: "which part of the definition does your example actually show?"
- Names the feature → Step 3.
- Can't → near-miss; ask one probing question and let them revise.

### Step 3 — Break the example
Change one detail of their example to make it no longer fit, and ask: "does it still count? Why or why not?" (e.g., for random assignment: "what if we assigned by birthday month instead of a coin flip — still random assignment?")

### Step 4 — Close with a contrast
Ask: "Now give me an example of something that *looks* like [concept] but isn't." Produces one → concept is solid. Can't → flag it for review before the quiz. End the skill.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when `contains_feature AND is_example_concrete`. `done_reasons` lists which gates fired.

**Narrative override:** end early if the student's example clearly demonstrates the concept's defining feature even with non-canonical phrasing the cue list doesn't catch. Continue past the gate if `suggested_break` is non-empty and unaddressed — they should survive at least one adversarial tweak before the skill closes. When you decide done, write the Completion Notes block in the scratchpad.

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
- Long paragraphs of exposition or lecture-style explanations.
- Pasting your pre-read at the student as "the answer."
- Continuing past the completion criteria once they're satisfied.

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
