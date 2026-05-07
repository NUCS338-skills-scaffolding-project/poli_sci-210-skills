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
