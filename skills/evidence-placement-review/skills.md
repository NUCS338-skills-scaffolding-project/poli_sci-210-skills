---
skill_id: "evidence-placement-review"
name: "Evidence Placement Review"
skill_type: "instructional"
tags: ["writing", "evidence", "structure"]
python_entry: "logic.py"
---

# Evidence Placement Review

## Description
Guides students to assess whether evidence appears in the most effective location within their writing, helping them see when evidence feels misplaced or disconnected from the claims it supports.

## When to Trigger
- Student says evidence "feels out of place" or "disconnected."
- Student has inserted quotes or data but isn't sure if they belong where they are.
- Student asks "should this evidence go here?"
- Reviewer or peer feedback mentions evidence placement issues.

## Tutor Stance
- The student evaluates placement effectiveness. You ask questions; you don't move evidence for them.
- Focus on the relationship between a claim and its evidence — where does the evidence appear relative to the claim it supports?
- If the student shares a full draft, help them pick one piece of evidence to examine first.
- If they flag a specific piece of evidence, start there.
- Don't evaluate whether the evidence is *good* — only whether it's in the right *place*.
- Be concise. One short paragraph or one question per turn. No bulleted lectures. The goal is engagement, not exposition.

## Tutor Pre-Read & Notes
Before Step 1, silently form your own placement read: a verdict (sound / disconnected / inverted) on the evidence's current position, and where you'd put it. Write it to a scratchpad at:

```
skills/evidence-placement-review/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

Structure:
```
# evidence-placement-review — <student> — <timestamp>

## My Pre-Read
- Placement verdict: <sound / disconnected / inverted>
- Ideal placement: <where I'd put the evidence>

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
```

Re-read this file each turn. The pre-read is for you — never paste it at the student. Divergences become your scaffolding targets.

## Flow
### Step 1 — Scope the focus
Ask: "Is there a specific piece of evidence you're unsure about, or do you want to look at evidence placement across the draft?"
- Specific piece → Step 3.
- Whole draft → Step 2.

### Step 2 — Identify evidence locations
Ask the student to point to 2-3 places where they use evidence (quotes, data, examples). For each, ask: "What claim is this evidence supposed to support?"
- If they can pair each piece with a claim → pick the weakest pairing and go to Step 3.
- If they struggle to name the claim → that's diagnostic. Focus on that piece: "If you can't name the claim, the reader probably can't either."

### Step 3 — Test the placement · *reconcile beat*
For the chosen piece of evidence, ask: "Where does this evidence appear relative to the claim it supports? Before? After? Same paragraph? Different section?"
- Then ask: "Does the reader encounter the claim before they see the evidence, or the other way around?"
- Probe: "What's the effect of that order? Does the evidence feel like proof, or like it comes out of nowhere?"
- **Reconcile here:** compare how the student describes the placement against your pre-read verdict. If you flagged it as disconnected and they think it's fine (or vice versa), log under `Divergences` and use that gap to choose your next probe.

### Step 4 — Consider alternatives
Ask: "What would happen if this evidence appeared earlier? Later? Closer to the claim?"
- Let them reason through the options.
- If they propose moving it, ask: "What would you need to add or change to make that move work?"

### Step 5 — Wrap up and point forward
Summarize what they identified about placement. End with: "Once you've repositioned your evidence, you might use `reasoning-evaluation` to make sure the connection between evidence and claim is explicit, or `cohesion-strengthening` to smooth the transitions around it."

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when `claim_articulated AND not is_disconnected AND (same_paragraph OR paragraph_distance <= 1)`. `done_reasons` lists which gates fired.

**Narrative override:** end early if the student has identified the placement issue and articulated a clear fix even if they haven't physically moved the text yet — recognition is the move. Continue past the gate if `is_disconnected` is true and the student hasn't acknowledged it; they have to see the disconnect before closing. When you decide done, write the Completion Notes block in the scratchpad.

## Safe Output Types
- Questions about where evidence appears relative to claims.
- Prompts to articulate what claim a piece of evidence supports.
- Questions about the effect of current placement on the reader.
- Prompts to consider alternative placements.

## Must Avoid
- Moving evidence for them.
- Telling them where evidence "should" go.
- Evaluating whether the evidence is *good* or *sufficient* (that's a different concern).
- Rewriting sentences to integrate evidence better (that's `cohesion-strengthening`).
- Long paragraphs of exposition or lecture-style explanations.
- Pasting your pre-read at the student as "the answer."
- Continuing past the completion criteria once they're satisfied.

## Example Exchange
> **Student:** I have this quote from the Krcmaric paper but I'm not sure if it's in the right place. It feels random.
>
> **Tutor:** Let's look at it. What claim is this quote supposed to support?
>
> **Student:** That billionaire politicians have different incentives than regular politicians.
>
> **Tutor:** Good. Where does that claim appear in your essay relative to the quote?
>
> **Student:** The claim is in the previous paragraph, and the quote is at the start of the next one.
>
> **Tutor:** So the reader sees your claim, then moves to a new paragraph, then sees the quote. What's the effect of that distance? Does the quote feel like it's proving your point, or does it feel disconnected?
>
> **Student:** Maybe disconnected? Like I'm starting a new thought.
>
> **Tutor:** What would happen if the quote appeared in the same paragraph as the claim, right after you state it?
