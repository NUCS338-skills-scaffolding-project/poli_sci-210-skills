---
skill_id: "extract-syllabus"
name: "Extract Syllabus"
skill_type: "code"
tags: ["import", "syllabus", "course-setup"]
course_types: ["cs", "humanities"]
learning_goal_tags: []
python_entry: "logic.py"
---

# Extract Syllabus

## Description
Extracts course metadata and an assignment list from raw syllabus text. Used by the orchestrator's `/syllabus/extract` endpoint to bootstrap a course's assignments from a PDF or pasted text.

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
    "term": "<e.g. 'Spring 2026' — empty string if missing>"
  },
  "assignments": [
    {
      "name": "<short assignment name>",
      "type": "<one of: writing, code, quiz, homework>",
      "due": "<verbatim due-date string from the syllabus>",
      "prompt": "<1-2 sentence summary of what the student must do>"
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

4. **All `course.*` fields are present.** If you cannot infer a field, return `""` (empty string), not `null`, not omitted.

5. **`warnings` is always present.** Empty array if everything was clear. Add one sentence per piece of ambiguity (e.g., `"Couldn't parse a date for 'Final paper' — left as TBD"`).

6. **No extra fields.** Do not add commentary, examples, or fields outside this schema.

### Syllabus

```
{syllabus_text}
```

## Notes

The orchestrator's `syllabus_importer` service substitutes `{syllabus_text}`, sends this to litellm with `temperature=0`, then hands the raw response to `logic.parse_extraction()` which validates and normalizes the result.

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
