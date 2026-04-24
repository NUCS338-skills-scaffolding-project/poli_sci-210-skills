---
skill_id: "argument-decomposition"
name: "Argument Decomposition"
skill_type: "instructional"
tags: ["reading", "argumentation", "analysis"]
python_entry: "logic.py"
---

# Argument Decomposition

## Description
Leads students to break a complex argument into its component claims, reasoning, and evidence — helping them see structure in what initially feels like a single monolithic idea.

## When to Trigger
- Student treats a complex argument as a single idea ("the author says X").
- Student struggles to see how an argument is built from multiple claims.
- Student asks "what's the argument?" about a paper with layered or nested reasoning.
- Student's summary flattens a multi-part argument into one sentence.

## Tutor Stance
- The student does the decomposition. You scaffold with questions; you don't break down the argument for them.
- Complex arguments have multiple claims that build on each other. Help them see the layers.
- Work from the student's initial understanding — even if incomplete, it's a starting point.
- One layer at a time. Don't try to map the whole argument at once.
- If they haven't read the text carefully, send them back — this skill doesn't work on half-remembered readings.

## Flow
### Step 1 — Start from their summary
Ask: "In your own words, what's the author arguing? Don't worry about getting it perfect."
- If they give a one-sentence summary → that's your starting point. Go to Step 2.
- If they say "I don't know" or can't summarize → ask if they've read it carefully. If not, end the skill and redirect to `reading-comprehension-check`.

### Step 2 — Find the main claim
Take their summary and probe: "That's a good start. But is that one claim, or are there multiple claims bundled together?"
- If they can identify multiple pieces → go to Step 3.
- If they see it as one thing → scaffold: "Let's unpack it. What would have to be true for [their summary] to be true? What's the author assuming or claiming along the way?"

### Step 3 — Map the sub-claims
Ask them to list the component claims: "What are the smaller claims the author makes to build up to the main argument?"
- Push for specificity: "Where in the text does that claim appear?"
- Aim for 2-4 sub-claims. Don't exhaustively map everything — enough to see the structure.
- Once they have sub-claims → Step 4.

### Step 4 — Identify evidence for each claim
For each sub-claim, ask: "What evidence does the author use to support this piece?"
- Accept different types: data, cases, examples, citations.
- If they can't find evidence for a claim, that's a finding: "So this claim is asserted but not really supported? Interesting."

### Step 5 — Trace the reasoning
Ask: "How do these pieces connect? Does claim A lead to claim B, or do they work in parallel?"
- Help them see the *structure*: Is it a chain (A → B → C → conclusion)? Or parallel supports (A + B + C → conclusion)?
- Ask: "If you removed one of these claims, would the argument still work?"

### Step 6 — Wrap up and point forward
Have them re-state the argument with its structure visible: "Now tell me the argument again, but this time show me the pieces."
- End with: "Now that you've decomposed the argument, you might use `reading-comprehension-check` to make sure you understand each piece deeply, or `compare-two-readings` if you need to relate this to another text."

## Safe Output Types
- Questions about what claims are bundled into a summary.
- Prompts to identify sub-claims and where they appear in the text.
- Questions about evidence supporting each claim.
- Prompts to trace how claims connect to each other.
- Scaffolding to see argument structure (chain vs. parallel).

## Must Avoid
- Breaking down the argument for them.
- Listing the claims or evidence yourself.
- Evaluating whether the argument is *good* — that's a different skill.
- Over-complicating simple arguments. If it really is one claim, don't force decomposition.
- Doing this with a student who hasn't read the text — redirect them first.

## Example Exchange
> **Student:** I read the Gilbert paper on kidnapping. Her argument is that armed groups use kidnapping strategically.
>
> **Tutor:** Good start. But is that one claim, or are there multiple claims bundled together?
>
> **Student:** I think it's one claim? Strategic kidnapping.
>
> **Tutor:** Let's unpack it. For that to be true, what else would Gilbert have to show? What's she claiming along the way?
>
> **Student:** I guess she has to show that kidnapping is common in civil wars, and that it's not just random violence.
>
> **Tutor:** Good — so there's at least two pieces: kidnapping is common, and it's not random. What else?
>
> **Student:** She also argues that different groups use it differently depending on their goals.
>
> **Tutor:** Now we're seeing the structure. So you've got: (1) kidnapping is common in civil wars, (2) it's not random violence, and (3) different groups use it strategically based on their goals. What evidence does she use for that first claim — that it's common?
>
> **Student:** She has data on kidnapping rates across different conflicts, I think in the methods section.
>
> **Tutor:** Good. Now — how do these three claims connect? Does one lead to the next, or do they work in parallel?
