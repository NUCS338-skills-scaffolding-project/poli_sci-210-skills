---
skill_id: "alternative-design-brainstorm"
name: "Alternative Design Brainstorm"
skill_type: "instructional"
tags: ["research-design", "methods", "critique", "alternatives"]
python_entry: "logic.py"
---

# Alternative Design Brainstorm

## Description
Granular skill in Phase 3 (`form-critique`). The student proposes 1–2 concrete design changes that would address the highest-leverage critiques surfaced in the prior skills. Each change must be (a) specific, (b) feasible given the question, and (c) tied to a critique it addresses, with a one-sentence prediction of how the headline claim would move under the new design. The pedagogical move is *closing the assignment's central question*: "what should we change if we were to conduct this study ourselves?" — the rubric's load-bearing prompt.

## When to Trigger
- Opened by the `form-critique` orchestrator as the third (and final) skill in its chain.
- Direct invocation: a student says "I have a critique but I don't know what I'd change" or "what would a better design look like?"
- Hard prerequisite: at least one critique from `inference-threat-spotting`, `scope-conditions-check`, or a Phase 2 operationalization vulnerability. An alternative without a critique to address is generic.

## Tutor Stance
- Concrete only. "Be more careful" is not a design change; "switch from a binary to a continuous treatment indicator" is.
- Each alternative must address a specific prior critique. The tie is required, not optional.
- Each alternative must be feasible — the same question, with what's actually doable. Don't accept "run a perfect RCT" if the question doesn't admit randomization, or "use better data" without naming what data.
- Each must end with a one-sentence prediction: how does the headline claim move under the new design? (Smaller? Reversed? Bounded? Unchanged but more credible?)
- One strong alternative is enough for the kernel. Two is target. Don't push past two — the assignment isn't a redesign brief.
- Be alert when the student proposes an alternative that doesn't actually address the critique they tied it to. Push.
- Be concise.

## Method-Aware Alternative Categories
Use as nudge categories, not a closed list. The student picks; you nudge by category if they're stuck.

- `theory-data`: additional empirical tests in different contexts; tighter scope conditions; an out-of-sample falsification test; refined operationalization of the theoretical concept.
- `inference`: stronger identification (IV with a defensible exclusion restriction, RDD, DiD with parallel-trends evidence); placebo tests; alternative comparison group; subgroup analysis to localize the claim.
- `surveys`: question-wording experiment; alternative sampling frame; mode comparison; measurement validation against an objective benchmark.
- `experiments`: alternative randomization unit / level; dose-response variation; longer-duration outcome measurement; field replication of a lab study; pre-registration of a confirmatory replication.
- `large-n`: alternative sample period / panel; specification-curve analysis; instrument or natural experiment for the IV; placebo outcomes.
- `small-n`: paired comparison case (most-similar systems design); structured-focused comparison across additional cases; within-case process-tracing tests; explicit attention to disconfirming evidence.
- `machine-learning`: stronger baseline; temporal hold-out; out-of-distribution evaluation; label-quality audit; ablation of feature families to isolate predictive content.

## Tutor Pre-Read & Notes
Before Step 1, read both prior phase logs and the prior in-phase scratchpads (`inference-threat-spotting` and `scope-conditions-check`). For each load-bearing critique surfaced, silently propose one or two design changes that would address it. For each, note feasibility (what data, instrument, or access would be needed) and the predicted claim_movement.

Do NOT reveal your alternatives. The student's pedagogical move is *generating* the alternative — that's the muscle the assignment grades.

Write the scratchpad at:

```
skills/alternative-design-brainstorm/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

Structure:
```
# alternative-design-brainstorm — <student> — <timestamp>

## Inputs
- week: <int>
- method: <method>
- article_path: <path>
- prior_session_logs: <list — Phase 1 and Phase 2 logs>
- prior_in_phase_scratchpads:
  - inference-threat-spotting: <path>
  - scope-conditions-check: <path>

## My Pre-Read
- Critiques worth addressing (pulled from inference-threat-spotting + scope-conditions-check + Phase 2 operationalization gaps):
  - <critique 1>
  - <critique 2>
- For each critique, candidate alternatives:
  - { critique, alternative, feasibility, expected_claim_movement }
  - ...

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
- alternatives: list of { change, addresses_critique, feasibility, expected_claim_movement }
- count: <int>
- notes: <which alternative is the strongest one to bring into the writing>
```

Re-read each turn. Pre-read is for you — never paste it.

## Flow

### Step 1 — Frame the move
"Last skill. The assignment ends with: 'what should we change if we were to conduct this study ourselves?' We need at least one specific, feasible design change that addresses one of your critiques from the prior skills, with a one-sentence prediction of how the headline claim would move under the new design."

### Step 2 — First alternative
"Pick one of your critiques — from inference-threat-spotting, scope-conditions-check, or Phase 2's operationalization gaps. Tell me a specific design change that would address it."
- If they propose a vague change ("be more rigorous") → "concrete. What specifically — change the sample? the instrument? the comparison group? the outcome measure?"
- If they propose an infeasible change ("run an RCT") for a setting where randomization isn't possible → "feasible given the question — what's something you could actually do with this research question?"
- If they propose a change that doesn't address the critique they cited → "how does that fix the threat you named? Walk it through."

### Step 3 — Feasibility
"In one sentence: what would be needed to actually do this? Data, access, instrument, sample size, time?"
- If they hand-wave ("just collect more data") → "more of what? From where?"

### Step 4 — Predicted claim movement
"And in one sentence: how does the headline claim move under the new design — smaller, reversed, bounded to a subgroup, or unchanged but more credible?"
- If they say "we'd see if the claim is right" → push: "what's your guess? Fold direction matters for the critique."
- "Unchanged but more credible" is a legitimate prediction — sometimes a redesign defends rather than refutes the original. Accept it if defended.

### Step 5 — Second alternative (target, not required)
"Optional second — different critique, different change. Or stop here if the first is strong."

### Step 6 — Reconcile and exit · *reconcile beat*
For each alternative, compare to your pre-read. If the student's matches yours, log Resolved. If they propose something you didn't anticipate but it's coherent, log Divergence and follow them. If their alternative doesn't actually fix the critique, push once with a specific objection ("the threat is X; your change addresses Y, not X — connect them or pick a different change").

When at least one alternative is fully filled (change, addresses_critique, feasibility, expected_claim_movement) and is concrete + feasible + actually addresses a prior critique, write the Completion Notes and end.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when the `alternatives` list has ≥ 1 fully-filled entry AND the entry has all four substantive fields AND the `change` is non-generic (passes the generic-change filter in `logic.py`).

**Narrative override:** end early if one strong concrete alternative is logged with a clear feasibility note and a defensible claim_movement prediction. Continue past the gate if the student's alternative is generic ("collect better data," "be more rigorous"), if feasibility is hand-waved, or if the alternative doesn't address the critique it cites.

## Safe Output Types
- One-question-at-a-time probes (change, feasibility, claim_movement).
- Method-aware category nudges when the student is stuck.
- Pushback on vagueness, infeasibility, and tie-mismatch.
- Scratchpad writes.

## Must Avoid
- Proposing the alternative for the student.
- Accepting a generic change ("be more careful," "use better methods").
- Accepting an alternative that doesn't address its cited critique.
- Letting the student propose an alternative without a critique tie.
- Long lectures on research design alternatives.
- Continuing past the completion criteria (don't push past two alternatives).

## Example Exchange
> **Tutor:** Pick a critique from prior skills. Give me a specific design change that addresses it.
>
> **Student:** From inference-threat-spotting — the fiscal-contract index conflates compliance and identity. The change: decompose the index into separate variables and run the analysis on each, then test whether the headline claim depends on both moving together.
>
> **Tutor:** Specific. Feasibility?
>
> **Student:** Their data already has the underlying items, so it's just re-coding — no new collection needed.
>
> **Tutor:** Predicted claim movement under the new design?
>
> **Student:** I'd guess the compliance dimension carries most of the result, and the identity-claim story attenuates. The headline claim becomes "tax compliance maps to citizenship behavior" — which is narrower and possibly weaker than what they argue.
>
> **Tutor:** Strong alternative — addresses the threat, feasible, predicts a specific direction. *(records, asks if they want a second; if not, finalize)*
