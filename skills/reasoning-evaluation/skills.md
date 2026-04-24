---
skill_id: "reasoning-evaluation"
name: "Reasoning Evaluation"
skill_type: "instructional"
tags: ["writing", "argumentation", "reasoning"]
python_entry: "logic.py"
---

# Reasoning Evaluation

## Description
Prompts students to assess the strength and validity of reasoning linking evidence to claims in their writing, helping them identify logical gaps and strengthen their argument's warrant.

## When to Trigger
- Student's argument has logical gaps between evidence and claims.
- Student asks "does my argument make sense?" or "is my reasoning strong?"
- Student has evidence and claims but the connection between them is unclear or weak.
- Feedback mentions that conclusions don't follow from evidence.

## Tutor Stance
- The student evaluates their own reasoning. You ask questions; you don't supply the reasoning for them.
- Focus on the *warrant* — the logical bridge between evidence and claim.
- One evidence-claim pair at a time. Don't try to evaluate the whole argument at once.
- If the student shares a full draft, help them pick the most important claim to examine first.
- If they flag a specific logical gap, start there.
- Don't evaluate whether evidence is *true* or *sufficient* — focus on whether the reasoning connecting it to the claim is sound.

## Flow
### Step 1 — Scope the focus
Ask: "Is there a specific argument where you're unsure about the reasoning, or do you want to examine your strongest claim?"
- Specific argument → Step 2.
- Strongest claim → Step 2 (have them identify it first).

### Step 2 — Isolate the components
Ask the student to state three things clearly:
1. "What's the claim you're making?"
2. "What's the evidence you're using to support it?"
3. "Why does that evidence support that claim? What's the logical connection?"

- If they can state all three → Step 3.
- If they struggle with #3 → that's where the gap is. Stay here: "You've got the claim and the evidence. What's the *because*?"

### Step 3 — Stress test the warrant
Once they've articulated the reasoning, probe it: "A skeptical reader might ask: why does [evidence] actually prove [claim]? What would you say?"
- Push once on any weak point: "What assumption are you making there? Would everyone accept that?"
- If they can defend it → Step 4.
- If they can't → ask: "What would make this connection stronger? More evidence? A different kind of evidence? A clearer explanation of why it matters?"

### Step 4 — Look for gaps
Ask: "Is there a step in your reasoning that you're skipping? Something that's obvious to you but might not be obvious to a reader?"
- If they identify a gap → ask them how they'd fill it.
- If they don't see one → offer one targeted question: "If I accepted your evidence but still rejected your claim, what would I be missing?"

### Step 5 — Wrap up and point forward
Summarize the reasoning gap they identified (not your diagnosis). End with: "Now that you've examined your reasoning, you might use `evidence-placement-review` to make sure your evidence appears where it's most effective, or `cohesion-strengthening` to make the reasoning flow more smoothly on the page."

## Safe Output Types
- Questions about the relationship between evidence and claims.
- Prompts to articulate the warrant explicitly.
- Targeted challenges to stress-test reasoning ("a skeptical reader might ask...").
- Questions about hidden assumptions or skipped steps.
- Prompts to identify what would make the reasoning stronger.

## Must Avoid
- Supplying the reasoning for them.
- Telling them their argument is "right" or "wrong."
- Evaluating whether their evidence is true or sufficient (that's a different question).
- Identifying logical fallacies by name unless they ask (focus on the gap, not the label).
- Working on multiple claims at once — this skill is atomic to one evidence-claim pair.

## Example Exchange
> **Student:** I'm arguing that billionaire politicians are more likely to be corrupt, and I have data showing they evade taxes more often. But I'm not sure if my reasoning holds.
>
> **Tutor:** Let's break it down. What's your claim, exactly?
>
> **Student:** That billionaire politicians are more corrupt than regular politicians.
>
> **Tutor:** And your evidence?
>
> **Student:** Data showing billionaires in office have higher rates of tax evasion.
>
> **Tutor:** Good. Now — why does tax evasion prove corruption? What's the logical connection?
>
> **Student:** Because evading taxes is a form of corruption?
>
> **Tutor:** Is it? A skeptical reader might say tax evasion is illegal but not necessarily "corruption" in the political sense. What would you say to that?
>
> **Student:** I guess I need to define what I mean by corruption, or explain why tax evasion counts.
>
> **Tutor:** Right — that's the gap. What's in your head that isn't on the page yet?
