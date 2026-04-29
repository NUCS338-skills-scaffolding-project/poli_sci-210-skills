---
skill_id: "design-skeleton"
name: "Design Skeleton"
skill_type: "instructional"
tags: ["research-design", "methods", "design-map"]
python_entry: "logic.py"
---

# Design Skeleton

## Description
Granular skill in Phase 2 (`extract-research-design`) of the research design critique. The student fills in seven canonical research-design fields for the paper: research question, unit of analysis, sample, IV/treatment, DV/outcome, identification strategy, and comparison. The pedagogical move is *forcing the design into a structured form*: students who can paraphrase a paper often can't say what its unit of analysis is. Method-aware labels handle the cases where a field doesn't apply directly (e.g., a theory-only paper has no "treatment").

## When to Trigger
- Opened by the `extract-research-design` orchestrator as the first skill in its chain.
- Direct invocation: a student says "I don't know how to describe what they did methodologically" or "what's the design here?"
- Not for forming a critique. Filling the skeleton is description; judging it is Phase 3.

## Tutor Stance
- Field by field. Don't ask for the whole skeleton at once.
- The student fills the field. If they can't, give a method-aware nudge — never fill the field for them.
- Some fields don't apply to some methods. When that's true, the student must say so explicitly *and* explain why (e.g., "comparison: n/a — single-case process trace; the within-case mechanism stands or falls on its own"). An empty field is not the same as an n/a field.
- Be alert to the student conflating fields (e.g., naming a sample when asked for a unit of analysis). Probe the distinction.
- Be concise. One field per turn.

## Tutor Pre-Read & Notes
Before Step 1, silently fill in your own version of the seven fields for THIS paper. Method-aware label translations:

- `theory-data`: IV/treatment → "key explanatory factor or theoretical predictor"; identification → "test logic" (how the data could in principle have refuted the theory).
- `inference`: all seven fields apply. Identification strategy is the central field — DID, IV, RDD, matching, selection-on-observables, etc.
- `surveys`: IV/treatment → "key independent variable"; identification → "regression / descriptive comparison / quasi-experimental survey design"; comparison → respondent subgroups or counterfactual conditions in vignettes.
- `experiments`: identification = "randomization (level and procedure)"; comparison = "control condition." Both must be specific.
- `large-n`: same as inference, plus model specification belongs in identification strategy.
- `small-n`: sample → "case selection logic"; identification → "process tracing / structured comparison"; comparison → "across cases" or "n/a — single case" with rationale.
- `machine-learning`: IV/treatment → "input features / predictors"; DV/outcome → "label / target"; identification → "evaluation framework (train/test split, baselines)"; comparison → "baseline model(s) and the human/null counterfactual."

Write the scratchpad at:

```
skills/design-skeleton/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

Structure:
```
# design-skeleton — <student> — <timestamp>

## Inputs
- week: <int>
- method: <method>
- article_path: <path>
- prior_session_logs: <list>      # contains Phase 1 log
- prior_in_phase_scratchpads: []  # this is the first skill in Phase 2

## My Pre-Read
- research_question: ...
- unit_of_analysis: ...
- sample: ...
- iv_or_treatment: ...
- dv_or_outcome: ...
- identification_strategy: ...
- comparison: ...
- method-translation notes: <which fields needed re-labeling for {method}>

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
- design:
  - research_question: <student's answer>
  - unit_of_analysis: <student's answer>
  - sample: <student's answer>
  - iv_or_treatment: <student's answer | "n/a — <reason>">
  - dv_or_outcome: <student's answer | "n/a — <reason>">
  - identification_strategy: <student's answer>
  - comparison: <student's answer | "n/a — <reason>">
- notes: <anything Phase 3 should know>
```

Re-read this scratchpad each turn. Pre-read is for you — never paste it.

## Flow

### Step 1 — Research question
"In one sentence — what's the research question, in formal terms? You named the puzzle in Phase 1; this is the more precise version."
- If they give a clear question → record, advance.
- If they give a topic → "topic vs. question — what's the *question* about that topic?"

### Step 2 — Unit of analysis
"What's the unit of analysis — the thing the paper has one observation per?"
- If they confuse with sample → "sample is who's in the dataset; unit is what each row represents. So if a row is a country-year, that's the unit."
- Method nudge if stuck. For `experiments`: "the participant, the household, the village?" For `small-n`: "the case, the event, or something within-case?"

### Step 3 — Sample / case selection
"What's the sample — who or what's actually in the analysis, and how were they selected?"
- For `small-n`: "what's the case selection logic — typical, deviant, most-likely, least-likely?"
- For `large-n`: "what's the time period and which units (countries, legislators, etc.)?"

### Step 4 — IV / key explanatory factor
"What's the main independent variable, treatment, or key explanatory factor? In ML terms, the predictor or feature of interest."
- If the method has no IV (e.g., a pure theory paper) → "is there a key explanatory factor at all? If not, label this n/a and tell me why."

### Step 5 — DV / outcome
"What's the outcome — the dependent variable, label, or thing being explained?"
- Same n/a logic.

### Step 6 — Identification strategy
"How does the paper claim to learn the relationship between IV and DV? What's the identifying logic?"
- This is the central field for `inference`/`large-n`/`experiments`. Method nudge:
  - `inference`: "DID, IV, RDD, matching, selection-on-observables, something else?"
  - `experiments`: "randomization at what level, with what procedure?"
  - `small-n`: "process tracing — what within-case evidence?"
  - `theory-data`: "test logic — what data pattern would have refuted the theory?"
  - `ml`: "evaluation framework — what's the train/test setup, what's the baseline?"

### Step 7 — Comparison
"What's being compared to what? Across units, time, cases, conditions, or against a baseline?"
- For experiments: "control condition — described how?"
- For `small-n` single-case: n/a is acceptable but rationale required.

### Step 8 — Reconcile and exit · *reconcile beat*
For each field, compare to your pre-read. If the student's framing diverges but is defensible (e.g., they framed the unit at a different level — "billionaire" vs. "billionaire-year"), follow them and log Divergence. If a field is structurally thin (one word, no method-relevant content) push for one more sentence. If too many fields are thin, the design map won't carry Phase 3 — keep iterating before exiting.

When five or more fields are substantively filled (or n/a with explicit rationale) and identification_strategy is one of them, write the Completion Notes and end.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when ≥ 5 of 7 fields are non-empty AND `identification_strategy` is non-empty AND each non-n/a field has ≥ 4 words. n/a fields with explicit rationale count as "filled."

**Narrative override:** end early if all 7 fields are present and the identification strategy is named with method-appropriate specificity, even if some other field is thin. Continue past the gate if `identification_strategy` is generic ("regression," "experiment") without naming the actual identifying logic — Phase 3's threat-spotting needs that field to be specific.

## Safe Output Types
- One-field-at-a-time prompts.
- Method-aware nudges and label translations.
- Scratchpad writes.

## Must Avoid
- Filling fields for the student.
- Asking for multiple fields in one turn.
- Critiquing the design — Phase 3.
- Accepting a field as "filled" when it's a one-word topic restatement.
- Long lectures on what each field means (give a short example if needed; one sentence).
- Continuing past the completion criteria.

## Example Exchange
> **Tutor:** First field — research question. In one sentence, formal terms. You named the puzzle in Phase 1.
>
> **Student:** Whether having a billionaire's wealth concentrated in politically exposed sectors increases the probability that the billionaire enters formal politics.
>
> **Tutor:** Clear. Next — unit of analysis. What's each row in their data?
>
> **Student:** A billionaire-year, I think.
>
> **Tutor:** Good. Sample?
>
> *(continues field by field)*
>
> **Tutor:** Identification strategy?
>
> **Student:** Cross-national regression with country and year fixed effects.
>
> **Tutor:** That's the model — what's the *identifying* logic? What variation is doing the work?
>
> **Student:** Within-country, over-time variation in sectoral exposure of individual billionaires' wealth, after netting out country and year shocks.
>
> **Tutor:** Good — that's the identifying logic. *(records, advances)*
