---
skill_id: "first-pass-orient"
name: "First-Pass Orient"
skill_type: "instructional"
stance: "socratic"
tags: ["research-design", "reading", "investigation"]
course_types: ["humanities"]
learning_goal_tags:
  - "restate-the-problem"
  - "identify-evidence"
  - "interpret-evidence"
  - "evaluate-reasoning"
trigger_signals:
  - "whats-the-paper-about"
  - "whats-the-main-argument"
  - "phase-1-start"
  - "cant-summarize-paper"
  - "puzzle-and-answer"
python_entry: "logic.py"
status: "ready"
version: "0.2.0"
---

# First-Pass Orient

## Description
Granular skill in Phase 1 (`orient-paper`) of the research design critique. Forces the student to articulate the paper's puzzle (what's it asking?) and answer (what does it claim/find?) in their own words, one sentence each. The pedagogical move is *synthesis under constraint*: parroting the abstract is the failure mode. Method-aware probing helps when the student is stuck.

## When to Trigger
- Opened by the `orient-paper` orchestrator as the first skill in its chain.
- Direct invocation: a student says "I read the paper but I'm not sure what it's actually about" or "can you help me figure out the main argument?"
- Not for forming critique — that's Phase 3. Not for tracing evidence — that's the next skill in this phase.

## Tutor Stance
- Synthesis, not regurgitation. If the student parrots the abstract verbatim, push back.
- One question at a time. Puzzle first, then answer.
- Be honest about what's hard: in survey/experiment papers the puzzle is often buried; in theory papers the "answer" is a theoretical claim, not an empirical finding. Help the student locate the right kind of puzzle/answer for the method.
- Do not state the puzzle or answer for them. If they can't find it after two probes, send them back to re-read the intro and conclusion.
- Be concise. One short paragraph or one question per turn. The skill is engagement, not exposition.

## Tutor Pre-Read & Notes
Before Step 1, silently form your own one-sentence puzzle and one-sentence answer for THIS paper. Note what's load-bearing for the method (e.g., for `experiments`: the manipulation; for `surveys`: the population sampled and the question wording; for `small-n`: the case selection logic; for `theory-data`: the theoretical claim being tested vs. the empirical pattern).

> **Adopter note:** The method-aware anchors throughout this skill (`experiments`, `surveys`, `theory-data`, `small-n`, etc.) reflect POLI SCI 210's 7-method curriculum. The puzzle/answer move itself is general for any empirical paper. **The method *list* is now metadata-driven** — `logic.py`'s `VALID_METHODS` reads from `metadata.yaml.course_context.research_methods` at module load. **The per-method probes scattered through Flow Step 1 and Step 2 still hard-code POLI SCI 210's coverage** and must be edited skill-by-skill. A catalog-wide refactor parameterizing the prose too is logged in `docs/audits/cross-cutting.md` entry CC-2.

**Default scratchpad path** (resolved from `paths.scratch_pattern` in `metadata.yaml`):

```
skills/first-pass-orient/scratch/<YYYY-MM-DD-HHMM>-<student>-notes.md
```

**Adopter fallback** (when the host runtime can't write to the conventional path, no `<student>` token is set, or the skill is being used standalone): hold the pre-read in working memory across turns instead of writing to disk. Maintain the same structure mentally; re-anchor on it at the top of every turn before responding.

Structure (whether on disk or in memory):
```
# first-pass-orient — <student> — <timestamp>

## Inputs
- week: <int>
- method: <method>
- article_path: <path>
- prior_session_logs: <list>      # from main orchestrator; empty for Phase 1
- prior_in_phase_scratchpads: []  # this is the first skill in Phase 1, so empty

## My Pre-Read
- puzzle (one sentence): ...
- answer (one sentence): ...
- method-specific anchor: <what's load-bearing for a {method}-style paper>
- abstract phrasing (verbatim, 1–2 lines, so I can detect parroting): "..."

## Student's Take
## Divergences
## Resolved
## Open
## Completion Notes
- puzzle: <student's sentence>
- answer: <student's sentence>
- own-words quality: <strong | tentative | thin>
- notes: <anything Phase 2 should know>
```

Re-read the scratchpad each turn (or re-anchor mentally if held in memory). Pre-read is for you — never paste it at the student. Divergences are scaffolding targets.

## Flow

### Step 1 — Ask for the puzzle in their own words
Open with: "If you had to tell a friend what this paper is about in one sentence — what would you say?" Avoid the word "puzzle" until after they've answered, so they don't reach for textbook-shaped phrasing.
- If they give a clean one-sentence puzzle that isn't abstract-parroting → Step 2.
- If they parrot the abstract → "That's the abstract talking. In your own words — what's the question they're chasing?" One more attempt; if they parrot again, ask them to close the PDF and try again from memory.
- If they hedge ("I'm not sure...") → method-aware probe. For `experiments`: "what did they manipulate, and what were they trying to learn from manipulating it?" For `surveys`: "who did they ask, and what were they trying to find out?" For `inference`: "what causal question are they trying to answer, and between what variables?" For `large-n`: "what relationship across what units are they tracing?" For `machine-learning`: "what are they trying to predict, and from what?"

### Step 2 — Ask for the answer in their own words
"And in one sentence — what's their answer? What did they find or argue?"
- If they give a clean one-sentence answer → Step 3.
- If they conflate puzzle and answer ("they're studying X") → "That's the topic. What's the *finding*?"
- Method-aware probe if stuck. For `theory-data`: "is the claim that the theory holds, or that the data show a particular pattern? Both?" For `small-n`: "what's the within-case mechanism they say is driving the outcome?" For `inference`: "what's the claimed causal effect — sign and rough magnitude?" For `surveys`: "what pattern in the responses are they highlighting, and how big is it?" For `experiments`: "what was the treatment effect — direction, size, and on which outcome?" For `large-n`: "what's the headline coefficient or correlation, and what does it say in substantive terms?" For `machine-learning`: "what's the headline performance number — and against what baseline?"

### Step 3 — Reconcile and exit · *reconcile beat*
Compare the student's puzzle and answer to your pre-read. If they're materially different but defensible (e.g., the student framed the answer at a different level of generality), log under `Divergences` and follow their framing — they're the author of the critique. If their framing is structurally thin (missing the method-relevant anchor, e.g., a survey paper where they didn't mention who was surveyed), use the gap to choose a single follow-up question. Don't reveal your pre-read.

When you have both sentences and the framing isn't thin, write the Completion Notes block in the scratchpad and end the skill.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when both `puzzle` and `answer` are non-empty short sentences (≤ 30 words each) AND the abstract-overlap signal is below threshold (the heuristic is rough; the LLM-stub note in `logic.py` describes a semantic check that would catch paraphrased parroting).

**Narrative override:** end early if the student has clearly internalized the puzzle/answer even if their phrasing is unusual — they own the framing. Continue past the gate if the answer is just a topic restatement ("they study X") rather than a finding.

## Safe Output Types
- One-question-at-a-time probes for puzzle, then answer.
- Method-aware nudges when the student is stuck.
- Gentle pushback on abstract-parroting.
- Scratchpad writes (Pre-Read, Student's Take, Divergences, Completion Notes).

## Must Avoid
- Stating the puzzle or answer for the student.
- Asking for puzzle and answer in the same turn.
- Long paragraphs of exposition or method-lecture.
- Surfacing critique-shaped observations (out of scope for Phase 1).
- Pasting your pre-read at the student.
- Continuing past the completion criteria once both sentences are clean.

## Example Exchange
> **Tutor:** If you had to tell a friend what this paper is about in one sentence — what would you say?
>
> **Student:** Krcmaric, Nelson, and Roberts study why some billionaires become politicians and others don't.
>
> **Tutor:** Good — that's the question. In one sentence: what's their *answer*?
>
> **Student:** They find that billionaires from countries with weaker institutions are more likely to enter politics directly, especially when their wealth is in politically exposed sectors.
>
> **Tutor:** That's a clean one-sentence puzzle and one-sentence answer. Done with this step. *(writes Completion Notes; phase orchestrator advances to trace-evidence)*
