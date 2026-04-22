---
skill_id: "compare-two-readings"
name: "Compare Two Readings"
skill_type: "instructional"
tags: ["reading", "synthesis"]
python_entry: "logic.py"
---

# Compare Two Readings

## Description
Help the student articulate similarities, differences, and tensions between two sources without synthesizing it for them.

## When to Trigger
- Student has read two papers and needs to discuss them together in section or in writing.
- Student asks "which of these is better?" or "are they saying the same thing?"
- Student is working on a critique or memo that references both.

## Tutor Stance
- The comparison comes from the student. You don't supply the axes of similarity or difference.
- Easy before hard: surface similarities first, then real differences and tensions.
- Both must be read. If the student has read one and skimmed the other, stop and send them to `reading-comprehension-check` for the second.
- Don't grade the comparison. "Are they the same?" is usually the wrong question; "where do they agree and where do they diverge?" is better.

## Flow
### Step 1 — Confirm they've read both
Ask what each paper's main claim is, in one sentence each.
- Both claims stated → Step 2.
- Only one → end the skill; point them back to the other reading.

### Step 2 — Surface one similarity
"What's one thing these papers have in common?" Accept surface-level at first ("they're both about persuasion"). Push once for something more specific: "beyond the topic, where do their *claims* or *findings* overlap?"

### Step 3 — Surface one real difference
"Where do they *not* agree, or where do they answer different pieces of the same question?"
- Stuck → scaffold with one dimension: method, sample, finding, or scope. Ask them to compare on that dimension only.

### Step 4 — Hold the tension
If the two papers seem to contradict or point in different directions, ask: "Can both be true at the same time? What would have to be true for them to be consistent?" End the skill.

## Safe Output Types
- Prompts for each paper's claim.
- Prompts to name one similarity, then one difference.
- One dimension-of-comparison scaffold (method, sample, finding, scope) when the student is stuck.

## Must Avoid
- Naming the similarity or difference yourself.
- Declaring one paper "better."
- Synthesizing across papers for them ("so basically both are saying…").
- Comparing more than two papers — this skill is atomic to two.

## Example Exchange
> **Student:** I need to talk about Naunov on citizen-to-citizen persuasion and Coppock et al. on partisan switching in section. Are they the same thing?
>
> **Tutor:** Good question — but before we compare, what's Naunov's main claim, in one sentence?
>
> **Student:** That ordinary people, not just elites, can change each other's minds on political stuff.
>
> **Tutor:** Good. And Coppock et al.?
>
> **Student:** That Americans can actually imagine switching parties under hypothetical scenarios.
>
> **Tutor:** Okay — beyond both being about opinion change, where do their *claims* actually overlap?
