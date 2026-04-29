---
skill_id: "operationalization-check"
name: "Operationalization Check"
skill_type: "instructional"
tags: ["research-design", "methods", "measurement"]
python_entry: "logic.py"
---

# Operationalization Check

## Description
Granular skill in Phase 2 (`extract-research-design`) of the research design critique. The student picks 1–2 of the design's key concepts and interrogates how the paper measures them: what the operationalization includes that arguably shouldn't be in, what it excludes that arguably should be in, and how load-bearing the gap is. The pedagogical move is *bridging concept to measure*: this is where the strongest empirical critiques almost always live, including Bryan's example "the billionaire-politician definition feels loose."

## When to Trigger
- Opened by the `extract-research-design` orchestrator as the second skill in its chain (after `design-skeleton`).
- Direct invocation: a student says "their measure of X feels off" or "I'm not sure their variable captures the concept."
- Not for forming a critique. Identifying a measurement gap is description; arguing it produced a wrong inference is Phase 3.

## Tutor Stance
- One concept at a time. Pick before probing.
- The student picks the concept. Foreground any measurement-category choice the student already flagged in Phase 1 (`probe-author-choices`) — that's the natural starting point. Never name the concept yourself.
- Each concept must produce four substantive things: the operationalization, what's in that shouldn't be, what's out that should be, and a severity label. A concept with three of four is incomplete.
- "Includes/excludes" is symmetric and both matter. Don't accept just one direction.
- Severity labels — `minor`, `moderate`, `load-bearing` — are about whether the gap *plausibly affects the headline claim*. Push for `load-bearing` only when the student can articulate why.
- Be alert when the student starts judging ("this measure is wrong") — redirect: "describe the gap, save the verdict for Phase 3."
- Be concise.

## Tutor Pre-Read & Notes
Before Step 1, read the paper's measurement section(s) and the Phase 1 `probe-author-choices` output. Identify 2–3 concepts whose operationalizations have plausible includes/excludes gaps. For each, name the operationalization (variable, scale, coding rules, source data), one thing arguably-included that shouldn't be, one thing arguably-excluded that should be, and an honest severity assessment.

Method-aware focus areas:
- `theory-data`: how the concept is defined and operationalized to count instances (e.g., "billionaire politician").
- `inference`: treatment and outcome measurement; pre-treatment covariates if the strategy depends on them.
- `surveys`: question wording, response scale, ordering, what's lumped into a single index.
- `experiments`: the manipulation (does it deliver the construct?), the outcome measure (does it capture what theory predicts?).
- `large-n`: indices and composite measures, country-level proxies, time-aggregation choices.
- `small-n`: what counts as evidence of a within-case mechanism; coding of the case as "outcome present/absent."
- `machine-learning`: label definition (what's labeled as positive/negative), feature definition.

Write the scratchpad at:

```
skills/operationalization-check/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

Structure:
```
# operationalization-check — <student> — <timestamp>

## Inputs
- week: <int>
- method: <method>
- article_path: <path>
- prior_session_logs: <list>
- prior_in_phase_scratchpads:
  - design-skeleton: <path>
- phase_1_carryover:
  - non_trivial_choices_with_measurement_flavor: <list — pull from Phase 1 probe-author-choices>

## My Pre-Read
- Concepts with operationalization gaps (2–3, each with all four fields):
  - { concept, operationalization, includes_but_shouldnt, excludes_but_should, severity }
  - ...

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
- concepts: list of { concept, operationalization, includes_but_shouldnt, excludes_but_should, severity }
- count: <int>
- notes: <anything Phase 3 should know — e.g., "primary load-bearing gap is the country-coded political institutions measure">
```

Re-read each turn. Pre-read is for you — never paste it.

## Flow

### Step 1 — Pick the first concept
"Pick a key concept and we'll interrogate how the paper measures it. Pull from your Phase 1 list if a measurement-category choice is already there — that's the natural starting point."
- If they pick a Phase-1 measurement choice → record, advance.
- If they pick something not in Phase 1 → fine, accept.
- If they're stuck → method-aware nudge by category (treatment, outcome, key construct, index component) — never name the concept.

### Step 2 — Operationalization
"How does the paper actually measure that concept? Variable name, scale, coding rule, source — whatever's specific."
- If vague → push for the specifics.
- If they paraphrase the construct rather than describe the measure → "that's the construct. What's the *measure* — the variable as it appears in the data?"

### Step 3 — Includes-but-shouldn't
"What does the operationalization include that arguably shouldn't be in — given the concept they're trying to measure?"
- If they say "nothing" → "really? Look at the coding rule — anything that gets in and feels like a stretch?"
- For `theory-data`: e.g., does the "billionaire politician" definition include people whose political role is honorary, ceremonial, or party-affiliated without office?
- For `surveys`: does the question conflate two things into one scale point?

### Step 4 — Excludes-but-should
"What gets *excluded* that arguably should be in?"
- If they say "nothing" → "really? Anything the construct should cover that the measure misses?"
- The pair forces them to think about both type-1 and type-2 measurement error.

### Step 5 — Severity
"How load-bearing is the gap — minor, moderate, or load-bearing? `Load-bearing` means the gap plausibly affects the headline claim from Phase 1."
- If they say `load-bearing` → "in one sentence: how would the headline claim move if the gap were fixed?" If they can't answer, downgrade to moderate.

### Step 6 — Second concept (target, not required)
"One more concept if there's an obvious one — different category, ideally. Otherwise we can stop at one if the first was load-bearing."
- Same Steps 2–5 for the second concept.

### Step 7 — Reconcile and exit · *reconcile beat*
For each concept, compare to your pre-read. If the student's gap is one you anticipated, log Resolved. If it's one you didn't anticipate but is defensible, log Divergence and follow them. If their includes/excludes feel asymmetric (one direction strong, the other weak), nudge for symmetry once.

When at least one concept is fully filled (all four fields, with severity that the student can defend), write the Completion Notes and end. If the only filled concept is severity = `minor`, push for a second — a single minor gap won't carry Phase 3.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when the `concepts` list has ≥ 1 fully-filled entry (all four fields non-empty). If the only entry is severity = `minor`, the gate stays open until a second is added.

**Narrative override:** end early if the student has one truly load-bearing gap with strong includes/excludes language and can articulate how the headline claim would move if the gap were fixed. Continue past the gate if the only gap is generic ("the variable could be more precise") with no specific includes/excludes content.

## Safe Output Types
- One-question-at-a-time probes (concept, operationalization, includes, excludes, severity).
- Method-aware category nudges.
- Pushback on vagueness, asymmetry, and judgment-shaped responses.
- Scratchpad writes.

## Must Avoid
- Naming the concept for the student.
- Accepting one-direction gap analysis (only includes, only excludes).
- Letting `load-bearing` be claimed without articulating *how* the claim would move.
- Critiquing — Phase 3.
- Long lectures on construct validity.
- Continuing past the completion criteria once a substantive gap is logged.

## Example Exchange
> **Tutor:** Pick a concept. Your Phase 1 list flagged the "billionaire politician" definition — start there if you want.
>
> **Student:** Yeah, that one.
>
> **Tutor:** How does the paper actually measure it? Variable, scale, coding rule.
>
> **Student:** Binary indicator: 1 if the person has $1B+ wealth and held an elected office between 2000 and 2020.
>
> **Tutor:** What does that include that arguably shouldn't be?
>
> **Student:** Honorary or ceremonial elected positions. Some elected councils have no policy authority — they're really patronage roles.
>
> **Tutor:** And what's excluded that should be in?
>
> **Student:** Appointed positions with significant policy authority — cabinet ministers, central bank governors. Those are politically powerful billionaires, just not elected.
>
> **Tutor:** Severity?
>
> **Student:** Load-bearing.
>
> **Tutor:** In one sentence — how does the headline claim move if the definition is fixed?
>
> **Student:** If we add appointed roles and drop ceremonial elected ones, the cross-country distribution shifts heavily — countries with weak institutions but strong patronage networks would jump up, possibly inverting the headline pattern.
>
> **Tutor:** That defends `load-bearing`. *(records, asks about a second concept)*
