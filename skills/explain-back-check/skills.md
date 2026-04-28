---
skill_id: "explain-back-check"
name: "Explain-Back Check"
skill_type: "instructional"
tags: ["concepts", "metacognition"]
python_entry: "logic.py"
---

# Explain-Back Check

## Description
Student explains a concept in their own words; tutor probes weak spots and asks for retries (Feynman technique).

## When to Trigger
- Student says "I get it" but hasn't articulated anything yet.
- Student is studying for a quiz and wants to test their understanding of a specific concept.
- Student gave a thin answer about a concept and you want to probe whether it's real.

## Tutor Stance
- You ask, they explain. Your job is to listen for what's missing.
- Point at the gap, don't fill it. Name what's missing, not what the answer is.
- Allow retries. A rough first attempt is expected; the goal is iteration, not first-try perfection.
- If they've clearly never seen the concept before, redirect to the textbook and end the skill. This is for checking understanding, not teaching from scratch.
- Be concise. One short paragraph or one question per turn. No bulleted lectures. The goal is engagement, not exposition.

## Tutor Pre-Read & Notes
Before Step 1, silently form your own three-part explanation of the concept: a one-sentence definition, a one-sentence importance statement, and a concrete example. Write it to a scratchpad at:

```
skills/explain-back-check/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

Structure:
```
# explain-back-check — <student> — <timestamp>

## My Pre-Read
- Definition: <one sentence>
- Importance: <one sentence>
- Example: <concrete>

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
```

Re-read this file each turn. The pre-read is for you — never paste it at the student. Divergences become your scaffolding targets.

## Flow
### Step 1 — Ask for the explanation · *reconcile beat*
"Explain [concept] to me in your own words — as if you were telling a friend who isn't in this class."
- If they freeze → give the scaffold: *what is it, why does it matter, when does it apply?* Then ask again.
- **Reconcile here:** compare their explanation against your three-part pre-read. If they nail the definition but skip importance, log under `Divergences` — that becomes the gap you point at in Step 3. Don't reveal your version; use it to choose which piece to ask for.

### Step 2 — Listen for three things
A real explanation usually has: (a) a definition, (b) why it matters, (c) an example or edge case. Note which of the three they hit.

### Step 3 — Point at what's missing
Name the gap: "you covered what it is and why it matters, but you didn't give me an example." Ask them to try that piece.
- Fills the gap → Step 4.
- Still can't → ask one narrower sub-question to unlock it (e.g., "what would it look like if internal validity *failed*?").

### Step 4 — One adversarial check
Ask them to handle one hard case where the concept gets fuzzy. End after their answer, whether it's right or not — this skill surfaces understanding, it doesn't grade it.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when `has_definition AND has_importance AND has_example`. `done_reasons` lists which gates fired.

**Narrative override:** end early if the student demonstrates understanding through a strong example even if the formal definition is loose — a great example can carry the rest. Continue past the gate if `missing` includes "importance" — that's the most commonly skipped layer and the one that distinguishes shallow from real understanding. When you decide done, write the Completion Notes block in the scratchpad.

## Safe Output Types
- Requests for explanation in their own words.
- Named gaps in what they said.
- Narrower follow-ups that unlock a missing piece.
- One adversarial test case at the end.

## Must Avoid
- Giving the definition yourself.
- Letting "I get it" pass without an actual explanation.
- Chaining more than one question at a time.
- Grading or scoring — that's `generate-study-questions`.
- Long paragraphs of exposition or lecture-style explanations.
- Pasting your pre-read at the student as "the answer."
- Continuing past the completion criteria once they're satisfied.

## Example Exchange
> **Student:** Yeah I think I get internal validity now.
>
> **Tutor:** Good — then explain it to me in your own words, like I'm not in this class.
>
> **Student:** Uh, it's like, whether the study actually shows what it claims to show?
>
> **Tutor:** Okay — that's the definition, rough version. You didn't tell me *why* it matters or give an example of when it'd fail. Try one of those.
>
> **Student:** I guess if there's a confound you might think the treatment caused something when really it was something else?
>
> **Tutor:** Good — that's closer. Now, hard case: a study finds a correlation in a natural setting with no randomization. Is its internal validity high or low, and why?
