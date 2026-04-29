---
skill_id: "method-week-alignment"
name: "Method-Week Alignment"
skill_type: "instructional"
tags: ["research-design", "methods", "course-alignment"]
python_entry: "logic.py"
---

# Method-Week Alignment

## Description
Granular skill in Phase 2 (`extract-research-design`) of the research design critique. The student sweeps the paper's design against a method-specific checklist of concerns drawn from the week's course material. For each concern they pick, they tie it to a concrete element of the paper's design and label whether the paper addressed it (`addressed`, `partially addressed`, `unaddressed`). The pedagogical move is *applying course material to a specific paper*: this is the move that turns the critique from generic into POLI SCI 210 — coursework.

## When to Trigger
- Opened by the `extract-research-design` orchestrator as the third skill in its chain (after `design-skeleton` and `operationalization-check`).
- Direct invocation: a student says "what should I be looking at given that this is the surveys week?" or "I don't know which course concepts apply."
- Not for forming a critique. Alignment is "which concerns apply"; judging adequacy is partly here (alignment label) but the *consequences* for the headline claim are Phase 3.

## Tutor Stance
- Two minimum, four target. One concern is too few; six is over-stuffing.
- The student picks the concerns from the method-specific checklist embedded in this skill (below). They don't have to invent the list.
- For each concern, they must tie it to a *concrete paper element* — not a generic "they should worry about X." Specificity is the gate.
- The alignment label (`addressed`, `partially addressed`, `unaddressed`) describes what the paper *did*, not whether what they did is right. That's still description, just at a higher level than design-skeleton.
- Encourage diversity: don't let all concerns be from the same family (e.g., for `experiments`, all about randomization).
- Be concise.

## Method-Specific Checklists
The student picks from the checklist matching the paper's `method` (passed in from the orchestrator). Each checklist is 5–7 items.

### theory-data
- Theoretical claim is falsifiable (not just descriptive).
- Operationalization aligns with the theoretical concept.
- Scope conditions are stated.
- The empirical pattern would look different if the theory were wrong.
- Data sourcing and quality transparency.
- Alternative theoretical explanations are addressed.

### inference
- Identification strategy is named and method-appropriate (DID, IV, RDD, matching, selection-on-observables, etc.).
- Comparison group / counterfactual is plausible.
- Threats to inference (confounding, selection, reverse causation, measurement) discussed.
- Scope of the causal claim (populations, conditions, time).
- Robustness to alternative specifications.
- Heterogeneous effects acknowledged or tested.

### surveys
- Sampling frame matches target population.
- Response rate and non-response bias considered.
- Question wording, order, and framing.
- Response scale discriminates meaningfully.
- Mode effects (phone / online / in-person).
- Weighting / poststratification.
- Pre-registration or robustness across question variants.

### experiments
- Randomization (level, procedure, balance check).
- Compliance / treatment uptake.
- Attrition and differential attrition.
- SUTVA / spillovers / no-interference assumption.
- External validity (sample, setting, dose, duration).
- Outcome measurement timing and instrument.
- Pre-registration of hypotheses and analyses.

### large-n
- Sample period justification.
- Case / country selection (universe, panel, balanced/unbalanced).
- Model specification (controls, fixed effects, interactions).
- Standard errors (clustering, robust, bootstrap).
- Robustness to alternative specifications.
- Generalization beyond the sample.
- Outliers and influential observations.

### small-n
- Case selection logic (typical, deviant, most-likely, least-likely, structured-focused).
- Within-case evidence quality (process tracing, causal-process observations).
- Comparative logic (or rationale for single case).
- Alternative explanations addressed.
- Generalization claims and their scope.
- Source triangulation and bias.

### machine-learning
- Training data: representativeness, label provenance, leakage.
- Evaluation metric matches the inferential target.
- Train/test split logic (random / temporal / blocked / clustered).
- Baseline comparison (random, simpler model, human).
- Interpretation: does prediction quality answer the substantive question?
- Out-of-sample generalization (across time, domains, populations).
- Fairness / disparate performance across subgroups.

## Tutor Pre-Read & Notes
Before Step 1, pull up the checklist matching the paper's `method`, then for each item silently note: did the paper address it, partially address it, or leave it unaddressed? Tie each to a concrete paper element. Read the Phase 1 and Phase 2 outputs to know what the student already surfaced — operationalization concerns from `operationalization-check` may already have an alignment item that matches, in which case foreground it.

Write the scratchpad at:

```
skills/method-week-alignment/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

Structure:
```
# method-week-alignment — <student> — <timestamp>

## Inputs
- week: <int>
- method: <method>
- article_path: <path>
- prior_session_logs: <list>
- prior_in_phase_scratchpads:
  - design-skeleton: <path>
  - operationalization-check: <path>

## My Pre-Read
- Checklist for {method} (each item with my call):
  - { concern, paper_element, alignment, note }
  - ... (4–6 items)

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
- concerns: list of { concern, paper_element, alignment, note }
- count: <int>
- notes: <anything Phase 3 should know — e.g., "the unaddressed compliance concern is the most load-bearing for the headline claim">
```

Re-read each turn. Pre-read is for you — never paste it.

## Flow

### Step 1 — Frame the move
"Now we sweep against the {method} checklist for this week. I'll show you the list. You pick at least two concerns, tie each to a specific element of the paper's design, and label whether the paper addressed it. The label describes what the paper *did*, not whether you agree with it — that's Phase 3."

Show the checklist for the paper's method (from this skills.md). Don't paraphrase — show the list verbatim.

### Step 2 — First concern
"Pick one. Tie it to a specific element of the paper's design. Then label: addressed, partially addressed, or unaddressed."
- If they pick a concern but tie it to "the methodology in general" → "which specific element? A specific section, table, or design choice."
- If they pick something that overlaps with their `operationalization-check` finding → fine, but tie it specifically to the alignment concern, not just restate the gap.
- If they label `unaddressed` for something the paper clearly does address → push back: "look at <pre-read evidence> — does that count as addressing it, even partially?"

### Step 3 — Second concern (different family)
"Pick another. Different family — not another randomization concern if the first was about randomization."
- Same probes.

### Step 4 — Third and fourth (target, not required)
"More if there are obvious ones. Otherwise we can stop at two."
- Encourage variety. If the student has stamina, push toward 4.

### Step 5 — Reconcile and exit · *reconcile beat*
For each concern, compare to your pre-read. If your call and the student's diverge on `alignment` (you said `partial`, they said `unaddressed`), probe once: "what would count as the paper addressing this?" If the student has a clear answer, log Divergence and follow them; if they don't, push to revise the label.

Highlight which `unaddressed` or `partially addressed` items are most load-bearing for the headline claim — but don't critique. Just note it for Phase 3.

When at least 2 concerns are logged with substantive paper elements and alignment labels (and they're not all from one family), write the Completion Notes and end.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when the `concerns` list has ≥ 2 entries, each with non-empty `concern`, `paper_element`, `alignment` (in valid set), and `note`, AND not all entries' `concern` strings come from the same checklist sub-family (heuristic: see `logic.py`).

**Narrative override:** end early if the student has 2 concerns that span different families and at least one is `unaddressed` or `partially addressed` with a load-bearing tie to the headline claim. Continue past the gate if all concerns are labeled `addressed` and the student is missing the gaps that a reader would flag.

## Safe Output Types
- Showing the method-specific checklist.
- One-concern-at-a-time prompts.
- Pushback on vague paper elements and on label/evidence mismatch.
- Pushback on family-clustering.
- Scratchpad writes.

## Must Avoid
- Picking the concern for the student.
- Accepting "the methodology in general" as a paper element.
- Critiquing the paper's design choices — Phase 3.
- Letting all concerns come from one family (e.g., all randomization, all sampling).
- Long lectures on what each concern means (give a one-line definition only if asked).
- Continuing past the completion criteria.

## Example Exchange
> **Tutor:** Surveys week. Here's the checklist: sampling frame match, response rate / non-response, question wording, response scale, mode effects, weighting, pre-registration / question-variant robustness. Pick one, tie it to a specific element, label.
>
> **Student:** Question wording. Their item asks "do you trust the government to deliver services" with a five-point scale. I'd label it `partially addressed` — they show robustness to dropping the middle point but don't test wording variants.
>
> **Tutor:** Good. Different family — pick another.
>
> **Student:** Sampling frame match. They sample registered voters, but the puzzle is about all citizens including unregistered ones. `Partially addressed` — they discuss the limitation in a footnote but don't have data on the unregistered.
>
> **Tutor:** Two concerns, two different families, both with specific paper elements and partial labels. *(records, asks if they want a third)*
