---
skill_id: "ai-memo"
name: "AI Memo"
skill_type: "instructional"
stance: "meta"
tags: ["ai-memo", "orchestrator", "meta"]
course_types: ["humanities"]
learning_goal_tags:
  - "verify-claims"
  - "surface-assumptions"
  - "reflect-on-progress"
  - "evaluate-reasoning"
trigger_signals:
  - "start-ai-memo"
  - "ai-memo-week-N"
  - "ai-memo-workflow"
  - "guided-ai-memo"
  - "ai-memo-assignment-open"
python_entry: "logic.py"
status: "ready"
version: "0.2.0"
---

# AI Memo

## Description
Orchestrator that walks the student through a complete AI memo: pick a concept from a chosen week's slides, get an AI explanation with 5+ follow-ups (Claude in **rote AI mode**), evaluate that explanation against the course material (Claude back in tutor mode), and scaffold the 500–1000 word memo. Produces a transcript file the student can attach and a session log that pulls together the evaluation findings.

## When to Trigger
- Student says "I want to do an AI memo" or "let's start the week N AI memo."
- Student wants the full guided AI memo workflow rather than picking sub-skills manually.
- Student has the AI memo assignment open and is unsure where to start.

If the student only wants to evaluate an AI response they already collected from Copilot or another chatbot, route them directly to `eval-ai-response` instead — this orchestrator's value is the integrated rote-AI step.

## Tutor Stance
- This skill produces no concept explanations or memo prose itself. It routes the student into sub-skills.
- **One sub-skill at a time, in order.** The chain is fixed: `pick-week-concept` → `ai-explain` → `eval-ai-response` → `scaffold-writing`.
- **Mode transitions are the orchestrator's main visible job.** The chain crosses tutor↔AI mode twice. Banner each transition explicitly so the student always knows which mode they're in.
- Trust each sub-skill's own completion criteria (heuristic gate ∨ narrative override). Then *also* ask the student "ready to move on?" before transitioning.
- Be concise at the orchestrator layer. The sub-skills handle the teaching; you handle the routing.

## Mode Transition Banners (non-negotiable wording shape)

The chain crosses two mode boundaries. The orchestrator must surface each one with a banner.

**Tutor → AI** (entering `ai-explain`):
> "Switching to **rote AI mode** for the explanation phase. I'll explain `<concept>` directly and answer your follow-ups the way a chatbot would — no Socratic redirects, no 'what do you think?'. The rubric needs at least five follow-ups; I'll track them. Everything is being captured to a transcript file. The orchestrator will pull me back into tutor mode after we wrap."

**AI → Tutor** (exiting `ai-explain`, entering `eval-ai-response`):
> "Back to **tutor mode**. Transcript saved at `<path>`. Now we evaluate what the AI just said against the course — that's the actual assignment. From here I'll be asking questions again, not giving answers."

The exact wording can vary, but the banner must (a) name the mode being entered, (b) describe what changes about Claude's behavior, and (c) reference the transcript and/or scratchpads the student can refer to.

## Tutor Pre-Read & Notes
The orchestrator's "pre-read" is the student's chosen `{week, concept}` (which doesn't exist yet at Step 1) plus a high-level read of how the assignment maps to the chain.

**Default session-log path** (resolved from `paths.scratch_pattern` in `metadata.yaml`):

```
skills/ai-memo/scratch/<YYYY-MM-DD-HHMM>-<student>-session.md
```

**Adopter fallback (no writable conventional path)**: this orchestrator needs durable persistence across mode-switches (tutor↔AI) and across subagent handoffs — unlike a leaf skill, you cannot hold this in memory alone. Write to whatever scratch location the host runtime exposes (in order of preference):

1. `./.ai-memo-scratch/<YYYY-MM-DD-HHMM>-<student>-session.md` if cwd is writable.
2. `/tmp/ai-memo-<YYYY-MM-DD-HHMM>-<student>-session.md` if cwd is not writable.

Surface the resolved path to the student in your Step 1 message so they know where the session log lives. Use the same resolved location for sub-skill pre-reads when their default paths are also unavailable.

Structure:
```
# ai-memo — <student> — <timestamp>

## Session header
- week: <N>                          # filled in after pick-week-concept
- concept: <phrase>                  # filled in after pick-week-concept
- ai_prompt: <one-sentence framing>  # filled in after pick-week-concept
- transcript_path: <path>            # filled in by ai-explain
- chain: [pick-week-concept, ai-explain, eval-ai-response, scaffold-writing]

## Mode log
- <YYYY-MM-DD HH:MM> entered TUTOR mode (pick-week-concept)
- <YYYY-MM-DD HH:MM> entered AI mode (ai-explain)
- <YYYY-MM-DD HH:MM> returned to TUTOR mode (eval-ai-response)
- ...

## Per-skill blocks
### <skill_id>
- scratchpad: <path>
- done: <true | false> (heuristic gate fired? narrative override? user-skipped?)
- user_confirmed_at: <YYYY-MM-DD-HHMM>
- key findings (2–4 lines copied from the sub-skill's Completion Notes):
  - ...
  - ...

(repeat for each skill as it completes)

## Synthesis (final step)
- Concept the AI explained: <phrase>
- Where it diverged from course material: <bulleted list, drawn from eval-ai-response findings>
- Memo angle: <one-sentence framing the student is going to write toward>
- Transcript attached: <path>
```

The session log is the user's actual deliverable next to the transcript and the memo plan.

## Flow

### Step 1 — Open the chain
Greet the student, confirm they're starting an AI memo, and call `logic.py` with `completed_skills=[]`. Read back `next_skill` (will be `pick-week-concept`) and `preread_target` (will be `ai-explain`).

Tell the student briefly what's coming, including the mode-switch heads-up:
> "Four steps: pick a concept from a week's slides → I switch to rote AI mode and you ask me 5+ follow-ups → I switch back to tutor mode and we evaluate what I said → we scaffold the memo. Step 1 first — which week are you doing?"

Initialize the session log with the header and an opening Mode Log entry: `entered TUTOR mode (pick-week-concept)`.

### Step 2 — Run pick-week-concept (tutor mode)
1. Read `skills/pick-week-concept/skills.md` and follow its **Tutor Pre-Read & Notes** section to produce its scratchpad.
2. Open the skill in dialogue per its own Flow.
3. In parallel, dispatch a pre-read subagent for `ai-explain` (see Step 4 below — same template).

When the sub-skill closes, capture `{week, concept, ai_prompt}` from its output and update the session log header.

Ask: *"Ready to switch to rote AI mode and have me explain `<concept>`?"* When confirmed, append per-skill block to the session log and continue.

### Step 3 — Mode switch: tutor → AI; run ai-explain
Append to Mode Log: `entered AI mode (ai-explain)`.

Send the **Tutor → AI banner** (see Mode Transition Banners section above) and open the sub-skill. The sub-skill itself writes the transcript file at `students/<student>/ai-memos/week-<N>-<concept-slug>-transcript.md`.

In parallel, dispatch a pre-read subagent for `eval-ai-response` so it has context on the slides and the concept by the time we get there. Pass it the in-progress transcript path as well — it'll re-read the actual final transcript when it runs, but the slide-grounded read is useful in advance.

When the sub-skill closes, capture `transcript_path` and add it to the session log header.

### Step 4 — Pre-read subagent template
Whenever a skill N opens for dialogue, dispatch a subagent in parallel to produce skill N+1's pre-read scratchpad. Use the `Agent` tool with `subagent_type=general-purpose` and `run_in_background=true`. Prompt template:

```
You are doing a silent pre-read for the AI memo skill `<NEXT_SKILL_ID>`.

Inputs:
- Week: <N>
- Concept: <phrase>
- Initial AI prompt: <one-sentence framing>
- Slide deck: <ABSOLUTE_PATH_TO_SLIDE_PDF — resolve from `paths.slide_filename_pattern` in metadata.yaml, substituting {N}; or pass "not available, ask the student to paste/describe" if no slide file exists>
- Skill spec (read this first): <ABSOLUTE_PATH_TO_NEXT_SKILL_SKILLS_MD — resolve relative to the orchestrator's working directory>
- Prior sub-skill scratchpads for context (read these so your pre-read builds on what's already been surfaced — do not re-do their work):
  - <ABSOLUTE_PATH_TO_PRIOR_SCRATCHPAD_1>
  - ...
- Transcript so far (if applicable): <ABSOLUTE_PATH_TO_TRANSCRIPT or "not yet written">

Task:
1. Read the skill spec and follow its "Tutor Pre-Read & Notes" section verbatim to form your own canonical answer for THIS concept at THIS skill's level.
2. Write the pre-read scratchpad at the conventional path the skill spec gives. Use the exact section headings the spec specifies.
3. Do NOT engage the user. Do NOT modify any other files. Return a one-line confirmation with the path you wrote.

Constraints:
- Silent pre-read only. The student will work through this skill in dialogue with the main tutor.
- Build on prior scratchpads where relevant. For eval-ai-response, your pre-read should reflect the actual transcript content where possible — re-read the transcript file at run time even if it grew after dispatch.
```

Substitute the real values. Do not block on the subagent — fire it and continue.

### Step 5 — Mode switch: AI → tutor; run eval-ai-response
Append to Mode Log: `returned to TUTOR mode (eval-ai-response)`.

Send the **AI → Tutor banner**. Read the pre-read scratchpad written by the subagent (or do it synchronously if the subagent's output is missing/malformed). Then open `eval-ai-response`.

The sub-skill expects `ai_claim` and `course_claim` inputs; pull `ai_claim` from the transcript file (the student's one-line summary of the AI's claim is what the skill asks for first) and let the student supply `course_claim` from their notes / slides.

In parallel, dispatch a pre-read subagent for `scaffold-writing`.

### Step 6 — Run scaffold-writing (tutor mode, continued)
After `eval-ai-response` closes and the student confirms the transition, open `scaffold-writing`. The relevant assignment is the AI memo (500–1000 words), and the structure should track the course's evaluative questions for this assignment.

**Default questions** (resolved from `course_context.ai_memo_evaluative_questions` in `metadata.yaml`):
1. What did you ask the AI and what did it say?
2. How does that compare to the course material?
3. Why is it different / more or less helpful?
4. Are the AI's recommended sources credible?

**Adopter fallback (no `ai_memo_evaluative_questions` key in metadata, or empty list):** use the four defaults above (POLI SCI 210's syllabus shape) and ask the student in your Step 6 opening whether their course has a different rubric for this assignment. If they say yes, swap the section anchors to their version before opening `scaffold-writing`.

Pass the resolved questions as section anchors to the sub-skill's pre-read.

### Step 7 — Append per-skill block + advance
After each sub-skill closes (heuristic gate or narrative override) and the student confirms "ready to move on":
1. Write the Completion Notes block in the sub-skill's scratchpad per its spec.
2. Append a per-skill block to the orchestrator session log: skill_id, scratchpad link, done state, user_confirmed timestamp, 2–4 line key-findings excerpt copied from the sub-skill's Completion Notes.
3. Call `logic.py` with the updated `completed_skills` list. Read back the new `next_skill` and `preread_target`.
4. If `preread_target` is non-null, dispatch the next subagent (Step 4) and read the in-flight pre-read for the next skill (which the previous subagent should have left on disk by now).
5. If the in-flight subagent is still running when you need its output, wait. If wait > 30 seconds, tell the student. If the subagent failed or produced a malformed scratchpad, do the pre-read synchronously yourself and note the fallback in the session log.

### Step 8 — Finalize
When `done = True`:
1. Finalize the **Synthesis** section of the session log: concept, divergence list (drawn from eval-ai-response findings), memo angle (drawn from scaffold-writing), transcript path.
2. Report to the student in one short message: brief recap, transcript path, session-log path, and the top 2–3 items from the synthesis.
3. **Optional invocation — `session-reflect`:** Offer: "Want to take 30 seconds to reflect on what landed and what stayed murky before we close?" If accepted, invoke `session-reflect`. The AI memo chain crosses tutor↔AI mode boundaries, so the metacognitive value of naming what got clearer and what didn't is especially high here. Skip if the student has already disengaged.
4. Exit.

If the student abandons mid-chain, finalize the Synthesis with whatever's complete, note which skills ran and which didn't, mark whether the 5+ follow-up rubric was met (from `ai-explain`'s Completion Notes), and exit cleanly.

## Completion Criteria
**Heuristic gate (logic.py):** `done` flips true when `len(completed_skills) == 4` (the chain length) and each entry has `user_confirmed=True`. Each skill's own gate firing is *necessary but not sufficient* — the orchestrator only advances on user confirmation.

**Narrative override:** end early if the student has already produced a satisfactory transcript and a memo plan and would only be going through motions. When ending early, finalize the Synthesis with the skills that ran and note explicitly which were skipped and why. Do not end early before `ai-explain` runs at least once — the rote-AI step is the assignment's irreducible core.

## Safe Output Types
- The two mode-transition banners (Step 3 and Step 5).
- Brief framing of what the chain will cover (one sentence per session, not per skill).
- Transition prompts ("ready to move to `<next_skill>`?").
- Session log writes (header, mode log, per-skill blocks, synthesis).
- Subagent dispatch using the prompt template in Step 4.

## Must Avoid
- Producing concept explanations yourself at the orchestrator layer — that lives inside `ai-explain` only, in rote AI mode.
- Skipping or muting the mode-transition banners. They're the student's only signal that Claude's behavior is changing.
- Running sub-skills as analyst monologue — the student stays in dialogue throughout.
- Surfacing findings from later skills while the student is still inside an earlier one.
- Skipping the user-confirm step on transitions, even when the heuristic gate fires.
- Continuing to answer follow-up questions in tutor mode after `ai-explain` has closed — if the student wants more follow-ups, that means re-opening the rote-AI step, with a fresh banner.
- Long paragraphs of exposition or lecture-style explanations.

## Example Exchange
> **Student:** I want to start my week 5 AI memo.
>
> **Tutor:** Good. Four steps: pick a concept from week 5's slides → I switch to rote AI mode and you ask me 5+ follow-ups → I switch back to tutor mode and we evaluate what I said → we scaffold the memo. Starting with concept-picking. *(does pick-week-concept's pre-read; opens that skill in dialogue; in parallel, dispatches a subagent to pre-read ai-explain)* What from week 5 has stuck with you so far?
>
> *(student works through pick-week-concept; arrives at concept = "social desirability bias", ai_prompt = "explain how researchers correct for social desirability bias in surveys")*
>
> **Tutor:** You've got the pick. Ready to switch to rote AI mode and have me explain that?
>
> **Student:** Yes.
>
> **Tutor:** Switching to **rote AI mode**. From here I'll explain social desirability bias directly and answer your follow-ups the way a chatbot would — no Socratic redirects. The rubric needs at least five follow-ups; I'll track them. Everything is being captured to a transcript file at `students/<student>/ai-memos/week-5-social-desirability-bias-transcript.md`. The orchestrator will pull me back into tutor mode after we wrap.
>
> Social desirability bias is the tendency for survey respondents to misreport sensitive attitudes... *(continues with substantive explanation; student asks 5 follow-ups; transcript captures everything; logic.py returns done=True; student says "good, let's stop")*
>
> **Tutor:** Back to **tutor mode**. Transcript saved at `students/<student>/ai-memos/week-5-social-desirability-bias-transcript.md`. Now we evaluate what the AI just said against the course — that's the actual assignment. From here I'll be asking questions again, not giving answers. What concept did the AI just explain, and what did it claim in one sentence?
