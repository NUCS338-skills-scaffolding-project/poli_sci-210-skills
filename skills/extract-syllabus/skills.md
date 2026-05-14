---
skill_id: "extract-syllabus"
name: "Extract Syllabus"
skill_type: "code"
tags: ["import", "syllabus", "course-setup"]
course_types: ["cs", "humanities"]
learning_goal_tags:
  - "extract-requirements"
  - "specify-io"
trigger_signals:
  - "import-syllabus"
  - "extract-syllabus-text"
  - "bootstrap-course-from-syllabus"
  - "parse-syllabus-pdf"
python_entry: "logic.py"
status: "ready"
version: "0.2.0"
---

# Extract Syllabus

## Description
Extracts course metadata and an assignment list from raw syllabus text. Used by the orchestrator's `/syllabus/extract` endpoint to bootstrap a course's assignments from a PDF or pasted text.

## When to Trigger
- The orchestrator's `/syllabus/extract` endpoint receives a PDF upload or pasted syllabus text and needs to bootstrap a course's structured assignments.
- An adopter wants to extract `{course, assignments, warnings}` JSON from a syllabus standalone, outside the parent orchestrator (see "Standalone Usage" below).
- An automated import pipeline needs to convert syllabi from many courses into the registry's structured format.

## Inputs
The orchestrator substitutes `{syllabus_text}` (below) with the full extracted PDF text or pasted block before sending to the LLM.

## Outputs
Strict JSON with three top-level fields: `course`, `assignments`, `warnings`.

## Prompt Template

You are extracting structured data from a course syllabus. Read the syllabus text below and output **valid JSON only** (no prose, no markdown fences) matching this exact shape:

```json
{
  "course": {
    "code": "<short code like 'POLI SCI 210' — empty string if missing>",
    "name": "<full course title — empty string if missing>",
    "instructor": "<primary instructor name — empty string if missing>",
    "term": "<e.g. 'Spring 2026' — empty string if missing>",
    "term_start": "<YYYY-MM-DD of the first day of Week 1 — empty string if missing>"
  },
  "assignments": [
    {
      "name": "<short assignment name>",
      "type": "<one of: writing, code, quiz, homework>",
      "due": "<verbatim due-date string from the syllabus>",
      "prompt": "<1-2 sentence summary of what the student must do>",
      "recurrence": null
    }
  ],
  "warnings": ["<one sentence per ambiguity you couldn't resolve>"]
}
```

### Rules

1. **`type` mapping.** Map syllabus terms to the allowed values:
   - "essay", "paper", "reflection", "critique", "memo" → `writing`
   - "problem set", "lab", "implementation", "coding assignment" → `code`
   - "quiz", "exam", "midterm", "final exam" → `quiz`
   - anything else → `homework`
   Never invent a new type.

2. **`due` is verbatim.** Copy the syllabus's date string exactly (e.g., `"Week 8"`, `"Friday May 3"`, `"TBD"`). Do not canonicalize.

3. **`prompt` is short.** 1–2 sentences. If the syllabus only gives a title with no description, write `""`.

4. **All `course.*` fields are present.** If you cannot infer a field, return `""` (empty string), not `null`, not omitted. The `term_start` field is the date of the first day of Week 1; look for phrases like "Week 1 (April 2)" or "Classes begin Monday, April 2" in the schedule section. Format as `YYYY-MM-DD`. If you cannot find a Week-1 anchor, return `""`.

5. **`recurrence` is per-row.**
   - For one-off assignments (e.g., "Final Paper due May 12"): `"recurrence": null`.
   - For series that recur weekly (e.g., "weekly quizzes", "research design critique each week × 7"): emit an object:
     ```json
     {
       "kind": "weekly",
       "count": <total occurrences, integer 1..52>,
       "anchor_weekday": "<Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday>",
       "first_week": <1-indexed week of the term the series starts, default 1>,
       "skip_weeks": [<term-week numbers to skip, default []>]
     }
     ```
   - For a series like *"Quizzes (10 points each × 7), due Fridays at 11:59 PM of the week they are assigned. Weekly assignments start the second week of class."*:
     ```json
     {"kind": "weekly", "count": 7, "anchor_weekday": "Friday", "first_week": 2, "skip_weeks": []}
     ```
   - Emit **one row per series**, not one row per occurrence. The orchestrator will expand it.
   - The `name` for a recurring row is the singular form ("Quiz", not "Quizzes"). The `due` is the human description ("Fridays of each week"). The structured detail lives in `recurrence`.

6. **`warnings` is always present.** Empty array if everything was clear. Add one sentence per piece of ambiguity (e.g., `"Couldn't parse a date for 'Final paper' — left as TBD"`).

7. **No extra fields.** Do not add commentary, examples, or fields outside this schema.

### Syllabus

```
{syllabus_text}
```

## Notes

The orchestrator's `syllabus_importer` service substitutes `{syllabus_text}`, sends this to litellm with `temperature=0`, then hands the raw response to `logic.parse_extraction()` which validates and normalizes the result.

### Architectural note for adopters

This skill is consumed by the orchestrator via the `/syllabus/extract` endpoint backed by the `syllabus_importer` service, **not** via the standard `logic_loader.py` path used by most code skills. `logic.py` also exposes a thin `run(input: dict) -> dict` wrapper (delegating to `parse_extraction`) so that adopters and automated harnesses calling skills through the standard contract can invoke this one the same way. The wrapper expects `{"llm_output": <str>}` as input and returns the parsed `{course, assignments, warnings}` dict — see `INPUT_SCHEMA` in `logic.py`.

## Standalone Usage (Adopters)

This skill is structurally a prompt template, not a tutor flow — it has no Socratic dialogue, no Tutor Stance section, no scratchpad. To use it without the parent orchestrator's `syllabus_importer` service:

1. **Extract syllabus text.** PDF → text via `pdftotext`, `pypdf`, or paste the syllabus content directly into a string.
2. **Substitute `{syllabus_text}`** in the **Prompt Template** section above with the extracted text. Everything between the "You are extracting structured data..." line and the closing ``` of the syllabus code fence is the prompt body.
3. **Call any LLM with `temperature=0`** (the determinism matters for schema adherence). Anthropic, OpenAI, Gemini — all work. The skill is provider-agnostic.
4. **Parse the response as JSON.** The model returns only the JSON object described in the schema; no markdown fences, no prose. If your runtime returns text wrapped in ```json fences anyway (some chat APIs do), strip them before parsing.
5. **Validate.** Confirm `course`, `assignments`, and `warnings` are present; coerce types if needed.

A minimal Python example:

```python
import json
from anthropic import Anthropic

prompt_template = open("skills/extract-syllabus/skills.md").read()
# Extract the prompt-body section between "## Prompt Template" and "## Notes".
# (You can also inline the prompt body directly to avoid the file read.)
prompt = prompt_template.split("## Prompt Template")[1].split("## Notes")[0]
prompt = prompt.replace("{syllabus_text}", syllabus_text)

client = Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    temperature=0,
    messages=[{"role": "user", "content": prompt}],
)
data = json.loads(response.content[0].text)
```

There is no `logic.py` requirement for standalone use — the skill is a one-shot prompt.
