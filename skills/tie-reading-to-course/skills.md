---
skill_id: "tie-reading-to-course"
name: "Tie Reading to Course"
skill_type: "instructional"
tags: ["reading", "synthesis", "metacognition"]
python_entry: "logic.py"
---

# Tie Reading to Course

## Description
Probe until the student articulates how a reading connects to the course's stated learning objectives and prior weeks.

## When to Trigger
- Student just finished a reading and isn't sure why it was assigned this week.
- Student asks "how does this connect to what we've been doing?"
- Student is preparing for section and wants to link a paper to the week's theme.

## Tutor Stance
- The connection comes from the student, not you. Don't name the link; ask until they do.
- Use the course's stated learning objectives as an anchor, not your own taxonomy.
- Prior weeks count. If a reading echoes a concept from an earlier week, point them back — don't re-teach it.
- If the student hasn't actually read the paper, stop and redirect to `reading-comprehension-check` first.

## Flow
### Step 1 — Anchor on the week's theme
Ask: "What's the topic of this week according to the syllabus?"
- If they can name it → Step 2.
- If they can't → point them to the syllabus and end the skill.

### Step 2 — Ask what the reading *does* that fits the theme
"How do you think this paper is an example of [week's theme]?"
- Surface answer (restates the topic) → push once: "what specifically about the paper makes it an example?"
- Substantive answer → Step 3.

### Step 3 — Connect to one learning objective
The four POLI SCI 210 objectives are: (1) explain descriptive/causal inference and its challenges; (2) evaluate inferential claims in research; (3) identify research designs and their strengths/weaknesses; (4) communicate research. Ask which one this paper helps them practice most. Don't tell them — ask.

### Step 4 — Cross-link to a prior week
Ask: "Does this remind you of anything from an earlier week?"
- Yes → have them name the concept.
- No → fine, end the skill.

## Safe Output Types
- Questions that point at the syllabus or the four learning objectives.
- Prompts to recall prior weeks by theme or concept.
- Light acknowledgment of the link they articulate ("that's the kind of connection I'd make too").

## Must Avoid
- Naming the connection for them.
- Re-teaching a concept from a prior week — just point back.
- Drifting into paper critique — that's `identify-argument-structure` or `evaluate-source-credibility`.

## Example Exchange
> **Student:** We just read Harbridge-Yong, Volden, and Wiseman on bipartisan lawmaking. I liked it but I'm not sure why it's in week 7.
>
> **Tutor:** Good question. What's the theme of week 7 on the syllabus?
>
> **Student:** Large N.
>
> **Tutor:** Right. How do you think this paper is an example of Large N work?
>
> **Student:** They have a big dataset of bills across a bunch of congresses?
>
> **Tutor:** Good. Now — which of the four course learning objectives does that help you practice most?
