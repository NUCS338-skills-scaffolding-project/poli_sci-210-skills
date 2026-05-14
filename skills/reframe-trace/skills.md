---
skill_id: "reframe-trace"
name: "Reframe with Trace"
skill_type: "instructional"
stance: "reframe"
tags: ["reframe", "concrete-example", "trace"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "interpret-evidence"
  - "decompose-arguments"
  - "restate-the-problem"
trigger_signals:
  - "student-stuck-on-abstraction"
  - "abstract-prompts-not-landing"
  - "i-dont-get-it-in-practice"
  - "cant-apply-abstraction"
  - "need-concrete-example"
status: "ready"
version: "0.2.0"
---

# Reframe with Trace

## Description
When the student is stuck on an abstraction, walks through one concrete worked example step-by-step — an execution trace, an argument trace, a single study's flow — so they see the abstraction operating on a single specific case. After the trace lands, returns to the abstraction with the trace in hand.

## When to Trigger
- Student says "I don't get what that means in practice" or "what does that *do*?"
- Student spins on the general principle without grounding it in a case.
- Multiple abstract Socratic prompts haven't landed; the student isn't disengaged, they're just not connecting.
- Student can recite a definition but can't apply it to anything.

## Tutor Stance
- Pick *one* concrete instance. Not three, not a representative sample. One. Trace density beats trace breadth.
- The trace itself is the teaching. Don't cut to the moral before walking through the steps.
- Stay in the concrete until the student tracks each step. Resist the urge to abstract back too early.
- Once the trace lands, the return-to-abstraction is one short move. The student should make that bridge themselves.

## Flow

### Step 1 — Pick the case
Pick one concrete instance to trace. Good picks are:
- **Specific:** "the case where the survey response is 'agree' but the respondent actually disagrees" — not "response bias in general."
- **Small:** something that fits in 4–8 trace steps. If it takes 20, you've picked too much.
- **Connected:** the case must obviously instantiate the abstraction the student is stuck on. Don't pick something that requires a second reframe to see.

Tell the student you're picking it: "Forget the general framing for a sec. Let's walk through one specific case: …"

### Step 2 — Walk the trace
Step the student through the case in order. Two modes:
- **Tutor-led trace:** you narrate each step ("first the function is called with X, then…"). Good when the student is fully blank.
- **Student-led trace:** you ask "what happens next?" at each step. Good when they're partly there but losing the thread.

Either way, hit every step. Don't skip from step 2 to step 5 and assume the middle. The middle is where they're stuck.

### Step 3 — Return to the abstraction
Once the trace ends, ask one bridging question that makes the student do the abstraction work themselves:
- "Okay — given how that played out, what's the general thing that's going on?"
- "What would change about this case if X were different?"
- "Where does the principle we were stuck on actually show up in those steps?"

Don't answer for them. Their answer in their own words is the signal that the reframe landed.

## Safe Output Types
- A picked-case sentence (Step 1).
- Step-by-step trace narration OR step-by-step Socratic trace prompts (Step 2).
- One bridging question that returns to the abstraction (Step 3).

## Must Avoid
- Picking a case the student didn't ask about and can't see the relevance of.
- Tracing more than one case in a single skill invocation. Pick one. If a second is needed, that's a second invocation.
- Skipping trace steps because they "feel obvious" — the obvious step is usually the one the student is missing.
- Returning to the abstraction yourself instead of asking the student to.

## Example Exchange
> **Student:** I keep reading "selection bias" but I don't actually see how it's different from regular bias.
>
> **Tutor:** Forget the general framing. Concrete case: a study about whether weightlifting reduces back pain, recruited from a gym membership database. Walk through with me — who gets into that sample?
>
> **Student:** People who already go to the gym, I guess.
>
> **Tutor:** Right. And what's true about people who already go to the gym, on average, before the study even starts?
>
> **Student:** Their backs probably already feel better than people who don't?
>
> **Tutor:** Yeah. So when the study finds the gym group has less back pain — what's an alternative explanation that has nothing to do with weightlifting?
>
> **Student:** Oh, that the *getting in* was filtered. Healthier-back people got in.
>
> **Tutor:** Right. Now what's selection bias in general?
