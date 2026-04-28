---
skill_id: "logical-flow-testing"
name: "Logical Flow Testing"
skill_type: "instructional"
tags: ["writing", "argumentation", "structure"]
python_entry: "logic.py"
---

# Logical Flow Testing

## Description
Prompts students to evaluate whether ideas progress logically from one section to the next in their essay, helping them identify where argument order is unclear or disjointed.

## When to Trigger
- Student says their essay "feels disjointed" or "doesn't flow."
- Student is unsure about the order of their argument sections.
- Student asks "does this make sense?" about their draft structure.
- Student has a draft but the logical progression between sections is unclear.

## Tutor Stance
- The student identifies flow problems themselves. You ask questions; you don't diagnose.
- Work at the section/paragraph level, not sentence level (that's `cohesion-strengthening`).
- If the student shares a full draft, help them pick one transition point to focus on first.
- If the student identifies a specific trouble area, start there.
- Never reorder the essay for them. They decide what moves where.
- Be concise. One short paragraph or one question per turn. No bulleted lectures. The goal is engagement, not exposition.

## Tutor Pre-Read & Notes
Before Step 1, silently form your own read of the section-to-section transitions: for each adjacent pair, name the kind of move (continuation, contrast, escalation, sequencing, etc.). Write it to a scratchpad at:

```
skills/logical-flow-testing/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

Structure:
```
# logical-flow-testing — <student> — <timestamp>

## My Pre-Read
- Transitions:
  - { from: <section>, to: <section>, kind: <continuation/contrast/escalation/etc> }
  - { from: <section>, to: <section>, kind: <continuation/contrast/escalation/etc> }
  - ...

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
```

Re-read this file each turn. The pre-read is for you — never paste it at the student. Divergences become your scaffolding targets.

## Flow
### Step 1 — Scope the focus
Ask: "Are you looking at the whole draft or is there a specific section that feels off?"
- Full draft → Step 2.
- Specific section → Skip to Step 3, focusing on that section and what comes before/after it.

### Step 2 — Map the current structure
Ask the student to list their main sections or paragraphs in order, one sentence each: "Walk me through your essay — what's each section doing?"
- If they can list them → Step 3.
- If they struggle to articulate → that's diagnostic. Ask: "Which section is hardest to summarize?" Start there.

### Step 3 — Test one transition · *reconcile beat*
Pick one transition point (or use the one the student flagged). Ask: "Why does [Section B] come after [Section A]? What's the logical connection?"
- If they can explain it clearly → probe once: "Would a reader see that connection, or is it only in your head right now?"
- If they can't explain it → that's the gap. Ask: "What would need to be true for [Section B] to follow logically from [Section A]?"
- **Reconcile here:** when the student names the transition kind, compare it to the kind in your pre-read. If they say "continuation" but you read it as "contrast," log under `Divergences` and use the gap to choose your next probe. Don't reveal your label.

### Step 4 — Consider alternatives
Ask: "Is there another order that might work better? What if [Section B] came earlier or later?"
- Let them reason through it. Don't suggest the "right" order.
- If they propose a change, ask: "What would that do to the rest of the essay?"

### Step 5 — Wrap up and point forward
Summarize what they identified (not what you think). End with: "Once you've addressed this, you might also look at `cohesion-strengthening` to tighten the connections within sections, or `reasoning-evaluation` if you want to test whether your evidence-to-claim logic holds."

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when `follows_canonical AND not unclassified_sections AND weakest_transition_index is None`. `done_reasons` lists which gates fired.

**Narrative override:** end early if the student diagnoses the weakest transition correctly even if other transitions are still unclassified — naming the real problem is the move. Continue past the gate if a transition is classified differently than your pre-read in a way that matters (e.g., they read it as continuation, you read it as contrast that they should be marking). When you decide done, write the Completion Notes block in the scratchpad.

## Safe Output Types
- Questions about why sections appear in their current order.
- Prompts to articulate the logical connection between sections.
- Requests to consider alternative orderings.
- Naming the transition point that seems weakest (after the student has identified it).

## Must Avoid
- Reordering the essay for them.
- Telling them which order is "correct."
- Diagnosing flow problems before they've articulated them.
- Working at the sentence level (that's `cohesion-strengthening`).
- Evaluating the quality of their reasoning (that's `reasoning-evaluation`).
- Long paragraphs of exposition or lecture-style explanations.
- Pasting your pre-read at the student as "the answer."
- Continuing past the completion criteria once they're satisfied.

## Example Exchange
> **Student:** I have a draft of my critique but it feels like the sections don't connect. Can you help?
>
> **Tutor:** Sure — are you looking at the whole draft, or is there a specific transition that feels off?
>
> **Student:** The whole thing, I guess. I'm not sure where to start.
>
> **Tutor:** Let's map it out. Walk me through your essay — what's each section doing, in one sentence each?
>
> **Student:** First I introduce the study, then I describe their method, then I give my main critique, then I say what I'd change.
>
> **Tutor:** Good. Now — why does your critique section come after the method description? What's the logical connection?
>
> **Student:** Because I need to explain what they did before I can criticize it?
>
> **Tutor:** That makes sense. Would a reader see that connection clearly, or is it only obvious to you right now?
