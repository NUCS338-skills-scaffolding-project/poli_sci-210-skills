---
skill_id: "scope-conditions-check"
name: "Scope Conditions Check"
skill_type: "instructional"
tags: ["research-design", "methods", "critique", "scope", "external-validity"]
python_entry: "logic.py"
---

# Scope Conditions Check

## Description
Granular skill in Phase 3 (`form-critique`). The student names 2–3 conditions under which the paper's headline claim might NOT hold *outside* the studied sample, ties each to a specific element of the design (sample, time period, manipulation, context, outcome family), and labels how strong the boundary is. The pedagogical move is *forcing the inferential reach of the paper to be specific*: a paper that "applies broadly" usually doesn't, and saying where it doesn't apply is half the critique.

## When to Trigger
- Opened by the `form-critique` orchestrator as the second skill in its chain (after `inference-threat-spotting`).
- Direct invocation: a student says "the finding probably doesn't generalize" or "this only works in the context they studied."
- Distinct from `inference-threat-spotting`: that skill asks whether the inference is valid *within* the sample. This skill asks whether it extends *beyond* it.

## Tutor Stance
- Scope conditions describe *boundaries* of the claim, not validity within the boundary. Don't conflate.
- Each scope condition must be specific: the population, the time period, the context, the manipulation dose, or the outcome family — not "it might not generalize."
- Each must tie to a specific design element from Phase 2 (the sample, the case selection, the manipulation, the outcome measure).
- Each must include a one-sentence reason: *why* the claim would fail to extend to that condition.
- Two minimum, three target. One scope condition is too few; four is over-stuffing.
- Don't accept scope conditions the paper itself already states. Read the paper's discussion / scope-conditions section in the pre-read.
- Be concise.

## Scope Categories (method-aware)
Across all methods, scope conditions usually fall into one of five categories:

1. **Population scope** — the units sampled vs. the units the claim is about.
2. **Temporal scope** — the time window of the study vs. when the claim is supposed to hold.
3. **Contextual scope** — the institutional, geographic, or cultural setting.
4. **Manipulation / dose scope** — at what intensity, duration, or version of the IV does the claim hold?
5. **Outcome scope** — does the claim extend to related but different outcomes?

Method-aware emphasis (use as nudge categories):
- `theory-data`: contextual + temporal (theories often hold in some eras / institutional configurations and not others).
- `inference`: population + contextual (the identifying assumption may be local).
- `surveys`: population + temporal (sampling frame and timing).
- `experiments`: manipulation/dose + contextual + population (lab-to-field; specific dose; specific subjects).
- `large-n`: temporal + population (the panel period and country selection).
- `small-n`: contextual + population (which other cases would we expect this in?).
- `machine-learning`: distribution shift across all five — population, temporal, contextual, dose (input intensity), outcome (label drift).

## Tutor Pre-Read & Notes
Before Step 1, read the paper's discussion / scope / external-validity section so you know what the paper claims about generalization and what it concedes. Read both prior phase logs. For each of the five scope categories, silently note: where could this claim plausibly fail to extend? Is the paper itself silent on it?

Write the scratchpad at:

```
skills/scope-conditions-check/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

Structure:
```
# scope-conditions-check — <student> — <timestamp>

## Inputs
- week: <int>
- method: <method>
- article_path: <path>
- prior_session_logs: <list — Phase 1 and Phase 2 logs>
- prior_in_phase_scratchpads:
  - inference-threat-spotting: <path>

## My Pre-Read
- Scope conditions where the claim plausibly does not extend (across the 5 categories):
  - { category, design_tie, why_it_fails, paper_acknowledges }
  - ...

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
- scope_conditions: list of { category, design_tie, why_it_fails, paper_acknowledges }
- count: <int>
- notes: <which scope condition is most load-bearing>
```

Re-read each turn. Pre-read is for you — never paste it.

## Flow

### Step 1 — Frame and offer the categories
"Now we ask: where does the claim *not* extend? Different from what we did last skill — that was about whether the inference holds inside the sample; now it's about whether it reaches beyond. The five categories: population, temporal, contextual, manipulation/dose, outcome. Pick at least two."

Show the five categories. Add: "Each scope condition needs to tie to a specific element of the design — the sample, the case, the manipulation, the period — and include why the claim would fail to extend there."

### Step 2 — First scope condition
"Pick a category. Tell me a specific condition where the claim wouldn't extend, what design element ties it, and why the claim would fail there."
- If they're vague ("it might not generalize") → "what specifically — a different population? a different period? a different context? Pick one and be specific."
- If they pick something the paper already concedes → "the paper says X about that — does that count? If you want to keep this one, articulate something the paper doesn't already concede."
- If they pick a within-sample inference threat by accident → "that's an inference threat — we did those last skill. Scope is about extending *beyond* the sample. Try again."

### Step 3 — Second scope condition (different category)
"Different category from the first. Pick another."
- Same probes.
- If they cluster (two population-scope conditions back to back) → "different category. What about temporal or contextual?"

### Step 4 — Third scope condition (target, not required)
"One more if there's an obvious one — otherwise we can stop at two."

### Step 5 — Reconcile and exit · *reconcile beat*
For each scope condition, compare to your pre-read. If yours and theirs match, log Resolved. If they identified a category you didn't anticipate as load-bearing, log Divergence and follow them. If their `paper_acknowledges` claim contradicts what you saw in the paper, push: "the paper says X — does that change your label?"

When at least 2 scope conditions are logged across at least 2 different categories with substantive `why_it_fails` notes, write the Completion Notes and end.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when the `scope_conditions` list has ≥ 2 entries, each with non-empty `category` (in valid set), `design_tie`, and `why_it_fails` (≥ 6 words), AND the entries span at least 2 different categories.

**Narrative override:** end early if 2 scope conditions across different categories are present with strong `why_it_fails` reasoning, even if a third would be available. Continue past the gate if both scope conditions are something the paper already explicitly addresses (no marginal contribution to the critique kernel) or if `why_it_fails` is generic ("it might not work elsewhere") rather than mechanistically grounded.

## Safe Output Types
- Showing the five scope categories.
- One-condition-at-a-time probes.
- Pushback on vagueness, on category-clustering, on paper-already-concedes overlap, and on inference-threat-confusion.
- Scratchpad writes.

## Must Avoid
- Picking the scope condition for the student.
- Letting the student conflate scope with within-sample inference threats.
- Accepting "it might not generalize" without a specific category and tie.
- Long lectures on external validity.
- Continuing past the completion criteria.

## Example Exchange
> **Tutor:** Five categories: population, temporal, contextual, manipulation/dose, outcome. Pick at least two. Where does the claim not extend?
>
> **Student:** Contextual. The Lagos study is in informal settlements with weak state presence. In informal settlements where the state has stronger local agents, the fiscal-contract-as-citizenship-claim mechanism might break down because residents already have a transactional relationship with the state.
>
> **Tutor:** Good — contextual scope, tied to the case selection from Phase 2 design map, with a mechanism-grounded why_it_fails. Does the paper acknowledge this?
>
> **Student:** Briefly — they note the context but don't argue mechanism would break down elsewhere.
>
> **Tutor:** Logged. Different category — pick another.
>
> **Student:** Manipulation/dose. The fiscal-contract index combines several items; if you only had the compliance dimension and not the identity dimension, the effect might attenuate sharply. So the claim probably doesn't extend to settings where only one dimension is policy-relevant.
>
> **Tutor:** Two categories, both with specific ties and reasoning. *(records, asks if they want a third)*
