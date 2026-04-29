---
skill_id: "trace-claim-to-evidence"
name: "Trace Claim to Evidence"
skill_type: "instructional"
tags: ["research-design", "reading", "investigation"]
python_entry: "logic.py"
---

# Trace Claim to Evidence

## Description
Granular skill in Phase 1 (`investigate-reading`) of the research design critique. Forces the student to pick the paper's headline empirical claim, then locate the specific table, figure, or passage that supports it, then read what's actually there. The pedagogical move is *reading past the framing into the guts*: students often grasp the abstract but never look at the central table. This skill closes that gap.

## When to Trigger
- Opened by the `investigate-reading` orchestrator as the second skill in its chain (after `first-pass-orient`).
- Direct invocation: a student says "I get the argument but I don't really know what's in the tables" or "where's the actual finding in this paper?"
- Not for forming a critique. Tracing a claim is grasp; judging the trace's adequacy is Phase 3.

## Tutor Stance
- One claim at a time. Don't let the student trace three claims half-heartedly.
- The student picks the claim. If they can't, ask "which finding does the paper most want you to believe?" — never propose the claim yourself.
- The student finds the evidence locus. If they're lost in the table forest, give a *category* nudge ("look in the results section"), not a coordinate.
- The student reads what's there. If they describe a table without numbers in their description, push back — the numbers are the point.
- Be alert to claim/evidence mismatch (the abstract claims X; the table actually shows X conditional on Y). Flag it, but don't critique it — just log under Divergences for Phase 3.
- Be concise. Question per turn. No table-reading lectures.

## Tutor Pre-Read & Notes
Before Step 1, silently identify the paper's headline empirical claim, find which table/figure/section it lives in, and read what the evidence actually shows. Note any abstract/table mismatch. Method-aware: for `experiments` the locus is usually a treatment-effect table; `surveys` → cross-tabs or regression with descriptive support; `large-n` → coefficient plot or main regression table; `small-n` → process-tracing narrative section, often paragraph-length passages rather than a table; `machine-learning` → performance table, confusion matrix, or held-out evaluation; `theory-data` → the empirical-pattern figure or test case; `inference` → the comparison table that anchors the causal claim.

Write the scratchpad at:

```
skills/trace-claim-to-evidence/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

Structure:
```
# trace-claim-to-evidence — <student> — <timestamp>

## Inputs
- week: <int>
- method: <method>
- article_path: <path>
- prior_session_logs: <list>      # from main orchestrator
- prior_in_phase_scratchpads:
  - first-pass-orient: <path>     # so this pre-read knows the puzzle/answer

## My Pre-Read
- headline_claim (one sentence): ...
- evidence_locus (where it lives): <Table N | Figure N | Section X passage | page Y>
- what the evidence actually shows (in your own words): ...
- claim/evidence match: <tight | loose | suspicious gap — describe>
- method-specific notes: <what's load-bearing for a {method}-style locus>

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
- headline_claim: <student's wording>
- evidence_locus: <what they pointed to>
- claim_evidence_match: <tight | loose | suspicious gap>
- notes: <anything Phase 2 should know — e.g., "student noticed Table 3 only supports the claim conditional on X">
```

Re-read this scratchpad each turn. Pre-read is for you — never paste it at the student. Divergences and "suspicious gap" notes become scaffolding targets in Phase 3 — surface them in the Completion Notes for Phase 3's pre-read.

## Flow

### Step 1 — Pick the headline claim
Open with: "Which finding does the paper most want you to believe? Pick one — the headline claim, not a side observation." Pull from `first-pass-orient`'s scratchpad (the answer the student articulated) — usually the headline claim is the empirical version of that answer.
- If they pick a claim → Step 2.
- If they hedge or pick three → "Just one. Which is most central?"
- If they pick something tangential → method-aware nudge. For `experiments`: "what's the treatment effect they're reporting?" For `large-n`: "what's the main coefficient they want you to look at?" For `small-n`: "what's the case-level claim — the mechanism they say is doing the work?"

### Step 2 — Find the evidence locus
"Where in the paper is that claim shown? Point to a specific table, figure, or passage."
- If they name a specific locus → Step 3.
- If they say "the results section" → "Which table or figure inside it?"
- If they're lost → category nudge by method. For `experiments` / `large-n` / `surveys`: "results tables, usually numbered." For `small-n`: "the process-tracing or case narrative — a specific subsection." For `theory-data`: "the empirical pattern figure, often early."
- Do not name the table/figure number for them.

### Step 3 — Read what's there
"OK, look at <locus>. In your own words, what does it actually show? Use the numbers, not just the column labels." If they describe a table without a single number, push back: "give me an actual coefficient/percentage/case observation."
- If their reading matches the headline claim → Step 4.
- If their reading reveals a mismatch (claim says X; table shows X conditional on Y, or only for a subgroup) → that's worth holding on to. Don't critique it, but acknowledge: "interesting — the claim and the evidence don't quite line up. Hold that for Phase 3." Log under Divergences.

### Step 4 — Reconcile and exit · *reconcile beat*
Compare the student's claim/locus/reading to your pre-read. If they pointed to a different but defensible locus (e.g., they cited the figure where you cited the table — both legitimate), follow them. If the locus they cited doesn't actually contain the claim they named, push back once with "are you sure that's the table that supports *that* claim?"; if they correct, log Resolved; if they don't, log Open.

When claim, locus, and reading are all present and the locus actually supports the claim, write the Completion Notes block in the scratchpad and end the skill.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when `headline_claim`, `evidence_locus`, and `claim_evidence_match` are all non-empty AND `evidence_locus` matches the expected locus pattern (table/figure/section/page reference).

**Narrative override:** end early if the student articulates the claim/evidence link with confidence and accuracy, even if the wording is unusual. Continue past the gate if the locus is vague ("the results section") or if the student's reading doesn't actually reference the evidence (just restates the claim).

## Safe Output Types
- One-question-at-a-time probes for claim, locus, and reading.
- Method-aware category nudges when the student is lost.
- Acknowledgment + park-it when claim/evidence mismatch surfaces.
- Scratchpad writes (Pre-Read, Student's Take, Divergences, Completion Notes).

## Must Avoid
- Picking the claim or the locus for the student.
- Critiquing the claim or the evidence — that's Phase 3.
- Letting the student trace multiple claims at once.
- Accepting "the results section" as a locus.
- Accepting a paraphrase of the claim as a "reading" of the evidence — they need to reference what's actually there.
- Long paragraphs of method-lecture about how to read the table.
- Continuing past the completion criteria once the trace is clean.

## Example Exchange
> **Tutor:** Which finding does the paper most want you to believe? Pick one — the headline claim, not a side observation.
>
> **Student:** That bipartisan cosponsorship makes a bill more likely to become law.
>
> **Tutor:** Good. Where in the paper is that shown? Point to a specific table or figure.
>
> **Student:** Table 2.
>
> **Tutor:** OK, look at Table 2. In your own words, what does it show? Use the numbers.
>
> **Student:** The coefficient on bipartisan cosponsorship is positive — about 0.4 — and significant. It's the biggest coefficient in the model.
>
> **Tutor:** That's the trace. *(writes Completion Notes; phase orchestrator advances to probe-author-choices)*
