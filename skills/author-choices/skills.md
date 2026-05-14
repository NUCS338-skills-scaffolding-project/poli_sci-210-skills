---
skill_id: "author-choices"
name: "Probe Author Choices"
skill_type: "instructional"
stance: "socratic"
tags: ["research-design", "reading", "investigation"]
course_types: ["humanities"]
learning_goal_tags:
  - "surface-assumptions"
  - "evaluate-reasoning"
  - "interpret-evidence"
trigger_signals:
  - "orient-paper-ran"
  - "first-pass-orient-ran"
  - "trace-evidence-ran"
  - "discussing-strength-of-authors"
python_entry: "logic.py"
status: "ready"
version: "0.2.0"
---

# Probe Author Choices

## Description
Granular skill in Phase 1 (`orient-paper`) of the research design critique. The student identifies 2–3 design choices the authors made that have plausible alternatives, names an alternative for each, and says one sentence on why the choice is non-trivial. The pedagogical move is *seeing the contestable scaffolding underneath the prose*: every empirical paper rests on choices the authors didn't have to make. Surfacing them is the prerequisite for Phase 2 (mapping the design) and Phase 3 (critiquing it).

## When to Trigger
- Opened by the `orient-paper` orchestrator as the third skill in its chain (after `first-pass-orient` and `trace-evidence`).
- Direct invocation: a student says "I read the paper but I don't know what to critique" or "everything seems reasonable to me."
- Not for forming a critique. Probing is *noticing* contestable choices; *judging* them is Phase 3.

## Tutor Stance
- Choices, not critiques. The student is naming things the authors decided, plus one alternative each. Whether the authors' choice is *wrong* is out of scope.
- Two minimum, three target. One choice is too few; four is over-stuffing the kernel for Phase 2.
- The student names the choice. If they're stuck, give a *category* nudge by method (see Method-aware probes below) — never name a specific choice from the paper.
- For each choice, the student must also propose at least one plausible alternative. Without an alternative, it's not a contestable choice — it's a description.
- Be alert when the student starts judging ("they should have done Y") — redirect: "park the judgment for Phase 3. For now, just name what they did and what they could have done instead."
- Be concise. Question per turn.

## Tutor Pre-Read & Notes
Before Step 1, silently identify 3–4 contestable design choices in the paper. For each, name 1–2 plausible alternatives the authors didn't take. Method-aware probes guide your nudges:

- `theory-data`: how the dataset was assembled, which units were excluded, what counts as an instance of the phenomenon.
- `inference`: comparison group, time window, measurement of treatment/outcome, identifying assumption.
- `surveys`: sampling frame, recruitment method, question wording, response scale, mode (phone/online/in-person).
- `experiments`: randomization unit, dose, control condition, outcome measurement timing, who delivers the manipulation.
- `large-n`: sample period, country/case selection, model specification, fixed effects, clustering of standard errors.
- `small-n`: case selection logic, level of analysis, what counts as a within-case observation, comparison cases (or absence thereof).
- `machine-learning`: training data, label definition, evaluation metric, train/test split logic, baseline comparison.

> **Adopter note:** The 7 method categories above reflect POLI SCI 210's curriculum. The RDC chain itself is generic for any course teaching empirical paper critique, but the per-method probe *content* below is not. **The method *list* is now metadata-driven** — `logic.py`'s `VALID_METHODS` reads from `metadata.yaml.course_context.research_methods` at module load, so adopters swap the tag set by editing `metadata.yaml` only. **The per-method prose content in this section, however, still hard-codes POLI SCI 210's coverage** and must be edited skill-by-skill. A catalog-wide refactor parameterizing the prose content too is logged in `docs/audits/cross-cutting.md` entry CC-2.

**Default scratchpad path** (resolved from `paths.scratch_pattern` in `metadata.yaml`):

```
skills/author-choices/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

**Adopter fallback** (when the host runtime can't write to the conventional path, no `<student>` token is set, or the skill is being used standalone): hold the pre-read in working memory across turns instead of writing to disk. Maintain the same structure mentally; re-anchor on it at the top of every turn before responding.

Structure (whether on disk or in memory):
```
# author-choices — <student> — <timestamp>

## Inputs
- week: <int>
- method: <method>
- article_path: <path>
- prior_session_logs: <list>
- prior_in_phase_scratchpads:
  - first-pass-orient: <path>
  - trace-evidence: <path>

## My Pre-Read
- Choices the authors made (3–4 contestable ones, each with at least one alternative):
  - { choice: "<what they did>", alternative: "<what they could have done>", why_non_trivial: "<one sentence>" }
  - ...
- Method-specific anchor: <which categories of choice are most load-bearing for a {method}-style paper>

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
- choices: list of { choice, alternative, why_non_trivial }
- count: <int>
- notes: <anything Phase 2 should know — e.g., "student flagged sample period as the deepest choice; worth foregrounding in design map">
```

Re-read the scratchpad each turn (or re-anchor mentally if held in memory). Pre-read is for you — never paste it at the student.

## Flow

### Step 1 — Frame the move
"Now we're surfacing choices, not critiquing them. Authors had to decide things: who to study, when, how to measure, what to compare to what. We're going to find 2–3 choices the authors made that they could have made differently. We'll come back to *whether the choice was right* in Phase 3."

### Step 2 — First choice
"Pick one. What's something the authors decided — not the topic or the finding, but a *choice* — that they could have decided differently?"
- If they name a choice + alternative → Step 3.
- If they name a choice without an alternative → "OK, what could they have done instead?"
- If they jump to judgment ("they should have used X") → "Park the should. What did they do, and what's a plausible alternative?"
- If they're stuck → category nudge by method. For `surveys`: "think about who they asked and how." For `experiments`: "think about what they manipulated and what was held constant." For `small-n`: "think about which cases they picked and which they didn't."

### Step 3 — Second choice
"Good. Pick another — different category from the first."
- Same probes apply.
- If both their choices fall into the same category (e.g., both about question wording in a survey paper), nudge: "those are both about [category]. What about how they handled [different category]?"

### Step 4 — Third choice (target, not required)
"One more if there's an obvious one — otherwise we can stop at two."
- If they have a third, take it.
- If they're spent, move to Step 5.

### Step 5 — Reconcile and exit · *reconcile beat*
For each of the student's choices, compare to your pre-read. Cases:
- Choice + alternative both match your pre-read closely → log Resolved, follow their framing.
- Choice matches but alternative is implausible → "is that alternative actually feasible? What would the authors object to?" If the student defends it, follow them; if not, push for a stronger alternative.
- Choice you didn't anticipate but is defensible → log Divergence, follow them. Phase 2 and Phase 3 may benefit from their angle.
- All choices are surface-level (e.g., "they used English" for a US-context paper) → push for one deeper choice before ending. The non-trivial choices need to bite.

When you have at least 2 choices, each with an alternative and a one-sentence why-non-trivial, write the Completion Notes block in the scratchpad and end the skill.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when the `choices` list has length ≥ 2, AND every entry has non-empty `choice`, `alternative`, and `why_non_trivial` fields.

**Narrative override:** end early if the student has surfaced two choices and stays unable to name a third — two solid choices is acceptable. Continue past the gate if all choices are surface-level (no real alternatives, or "alternatives" that any reviewer would dismiss); the kernel won't survive Phase 3.

## Safe Output Types
- One-question-at-a-time probes for each choice + alternative.
- Method-aware category nudges.
- Pushback on judgment-shaped responses ("park the should").
- Pushback on same-category clustering and on surface-level choices.
- Scratchpad writes (Pre-Read, Student's Take, Divergences, Completion Notes).

## Must Avoid
- Naming a specific choice from the paper. Category nudges only.
- Letting the student critique choices. That's Phase 3.
- Accepting a choice without an alternative.
- Accepting two choices in the same category.
- Long paragraphs of method-lecture about "what makes a choice non-trivial."
- Continuing past the completion criteria once 2–3 substantive choices are logged.

## Example Exchange
> **Tutor:** Now we're surfacing choices, not critiquing them. Authors had to decide things: who to study, when, how to measure, what to compare to what. Find me 2–3 choices they made that they could have made differently. We'll come back to whether they were *right* in Phase 3. Pick one to start.
>
> **Student:** They defined "billionaire politician" as anyone with $1B+ who held elected office. They could have used a different wealth threshold, or included appointed positions.
>
> **Tutor:** Good — choice and two alternatives. In one sentence: why is that choice non-trivial?
>
> **Student:** Because the threshold and the office-type both shape who counts as a "billionaire politician," and a different rule would change which countries dominate the dataset.
>
> **Tutor:** That bites. Pick another — different category. Not about the population definition.
>
> **Student:** They used cross-national data from 2000–2020. They could have started earlier, or focused on a single region.
>
> **Tutor:** Good. One sentence — why non-trivial?
>
> **Student:** The post-2000 window misses earlier waves of billionaire-politicians, and a single-region focus would catch institutional dynamics the global pool washes out.
>
> **Tutor:** Two solid choices logged. One more if there's an obvious one, otherwise we stop here.
>
> **Student:** I think that's it.
>
> **Tutor:** Good — two is enough. *(writes Completion Notes; phase orchestrator finalizes Phase 1 synthesis)*
