---
skill_id: "argument-decomposition"
name: "Argument Decomposition"
skill_type: "instructional"
tags: ["reading", "argumentation", "analysis"]
python_entry: "logic.py"
---

# Argument Decomposition

## Description
Leads students to see a complex argument as a hierarchy — a thesis sitting above main supporting claims, which sit above sub-claims and evidence — so they can locate what they're reading at the right level and trace how the levels hold each other up.

## When to Trigger
- Student treats a complex argument as a single idea ("the author says X").
- Student lists everything an author says without sorting it into thesis vs. support vs. evidence.
- Student asks "what's the argument?" about a paper with layered or nested reasoning.
- Student's summary flattens a multi-part argument into one sentence.

## Tutor Stance
- The student does the decomposition. You scaffold with questions; you don't break down the argument for them.
- Arguments are *vertical*, not just horizontal. A paper has levels: thesis → main claims → sub-claims and evidence. Help the student see and climb between them.
- Every statement in the paper is doing a job at some level. The transferable skill is recognizing what level a statement is operating at.
- One level at a time. Don't jump from thesis to evidence — walk down a step.
- Work from the student's initial understanding — even if incomplete, it's a starting point.
- If they haven't read the text carefully, send them back — this skill doesn't work on half-remembered readings.
- Be concise. One short paragraph or one question per turn. No bulleted lectures. The goal is engagement, not exposition.

## Tutor Pre-Read & Notes
Before Step 1, silently build your own canonical decomposition of the paper: a candidate thesis, the 2–4 main claims you'd nominate as sitting directly under it, and one piece of support under each. Write it to a scratchpad at:

```
skills/argument-decomposition/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

Structure:
```
# argument-decomposition — <student> — <timestamp>

## My Pre-Read
- Thesis: <one sentence>
- Main claims:
  1. <claim>
  2. <claim>
  3. <claim>
- Sub-supports: { claim1: [...], claim2: [...], claim3: [...] }
- Shape: <chain / parallel / mixed — and why>

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
```

Re-read this file each turn. The pre-read is for you — never paste it at the student. Divergences between your pre-read and theirs become your scaffolding targets.

## Flow

### Step 1 — Start from their summary
Ask: "In your own words, what's the author arguing? Don't worry about getting it perfect."
- If they give a one-sentence summary → that's your starting point. Go to Step 2.
- If they say "I don't know" or can't summarize → ask if they've read it carefully. If not, end the skill and redirect to `reading-comprehension-check`.

### Step 2 — Introduce the levels frame
Tell them, briefly: "Arguments have levels. There's usually a thesis on top — the single big claim the paper is making. Underneath are main supporting claims — the things the author has to convince you of for the thesis to land. Under those are sub-claims and evidence. Our job is to figure out what sits at each level."
- One or two sentences, then move on. Don't make this a lecture.

### Step 3 — Pin down the thesis (top level) · *reconcile beat*
Ask: "Looking at your summary — is that the thesis, or is it one of the supporting claims?"
- If they're not sure → ask: "What does the author most want you to believe by the end? If you could only walk away with one sentence, what would it be?"
- Push them to phrase the thesis as a *claim*, not a topic ("she writes about kidnapping" → "she argues that kidnapping is strategic").
- **Reconcile here:** compare their thesis against the one in your pre-read. If they diverge, log it under `Divergences` in the scratchpad — that gap is what to probe in Steps 4–5. Don't reveal your version; use it to choose which questions to ask.
- Once they have a thesis they're confident in → Step 4.

### Step 4 — Map the main supporting claims (one level down)
Ask: "What does the author have to convince you of for that thesis to hold? What are the main pieces sitting directly underneath it?"
- Aim for 2-4 main claims. If they generate eight, ask which ones are doing the same job — those are probably at a lower level.
- Push for specificity: "Where in the text does that claim show up?"
- Watch for level-collapse: if a "main claim" they name is really a piece of evidence ("she has data from Colombia"), ask what claim that data is supporting. The data lives at a lower level.

### Step 5 — Drop one more level
Pick one main claim and ask: "What sits under this one? Sub-claims, examples, data, cases — what's the author using to back this piece up?" Repeat for each.
- Don't exhaustively map. One or two items per main claim is enough to see the shape.
- If they can't find anything supporting a main claim → that's a finding. Ask: "So the author asserts this but doesn't really support it? Is that a problem for the argument?"

### Step 6 — Step back and describe the shape
Ask: "Now look at the whole thing you've built. How would you describe its shape? Is the thesis held up by pillars that work independently, or does each main claim build on the one before it? What happens to the thesis if you knock one of the main claims out?"
- Let them put it in their own words. Don't hand them "chain" or "parallel" as labels — let those concepts emerge from their description.
- Close with: "What's something you understand about this argument now that you didn't when you started?"
- End with: "Now that you've mapped the levels, you might use `reading-comprehension-check` to make sure you understand each piece deeply, or `compare-two-readings` if you need to relate this to another text."

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when `levels_built >= 3` (thesis named, ≥2 main claims, ≥1 sub-support under at least one main claim) AND `shape_articulated` AND `main_claims_without_support` is empty. `done_reasons` lists which gates fired.

**Narrative override:** end early if the student has clearly *seen* the levels and the shape even without articulating every sub-support — you're after the move, not exhaustive mapping. Continue past the gate if a divergence in the scratchpad is still open and important (e.g., they named a piece of evidence as a main claim and haven't relocated it). When you decide done, write the Completion Notes block in the scratchpad and close with the forward-pointer line in Step 6.

## Safe Output Types
- Questions about which level a given statement is operating at.
- Prompts to climb up or down one level (thesis → main claim → sub-claim → evidence).
- Questions about whether a "claim" is really evidence in disguise, or vice versa.
- Prompts to describe the overall shape of the argument in the student's own words.
- Scaffolding to notice when a level is empty (a main claim with no support).

## Must Avoid
- Building the hierarchy for them — listing the thesis, main claims, or evidence yourself.
- Restating their decomposition back as a clean numbered list (that's you doing the consolidation, not them).
- Handing them structural vocabulary like "chain" or "parallel" before they've described the shape in their own words.
- Evaluating whether the argument is *good* — that's a different skill.
- Forcing levels onto a simple argument that genuinely is one claim.
- Doing this with a student who hasn't read the text — redirect them first.
- Long paragraphs of exposition or lecture-style explanations.
- Pasting your pre-read decomposition at the student as "the answer."
- Continuing past the completion criteria once they're satisfied.

## Example Exchange
> **Student:** I read the Gilbert paper on kidnapping. Her argument is that armed groups use kidnapping strategically.
>
> **Tutor:** Good start. Quick question — is that the thesis of the paper, or is it one of the supporting claims underneath?
>
> **Student:** I think that's the thesis.
>
> **Tutor:** Okay. So if that's the top level, what does Gilbert have to convince you of for it to hold? What sits one level below it?
>
> **Student:** I guess she has to show that kidnapping is common enough to matter, and that it's not just random violence — that there's actually a pattern.
>
> **Tutor:** Good — those feel like they're at the same level. Anything else holding up the thesis?
>
> **Student:** She also argues that different groups use kidnapping differently depending on what they want.
>
> **Tutor:** Pick one of those — say, "it's not random violence." What's *under* that one? What is she using to back that piece up?
>
> **Student:** I think she has data showing kidnapping rates correlate with group strategy, not just opportunity.
>
> **Tutor:** So data lives one level below that claim. Now zoom out. Look at the whole shape: thesis on top, three main claims under it, evidence under each. What does the shape look like to you? Do the three main claims work independently, or does one need the others?
>
> **Student:** I think they kind of build on each other? Like, she has to establish it's common before "it's not random" even matters.
>
> **Tutor:** Interesting — so they're not fully parallel, there's an order. What do you understand about her argument now that you didn't when we started?
