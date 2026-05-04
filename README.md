# POLI SCI 210 — Skills Catalog

Tutoring skills library for Northwestern's **Introduction to Empirical Methods in Political Science** (POLI SCI 210). Built against the [Skills Scaffolding Project](Team-Guide.md) (Team-Guide v0.2). The orchestrator hosting these skills walks students through reading, critiquing, and writing about empirical political-science papers — Socratic by default, never producing prose for the student.

---

## At a glance

| | |
|---|---|
| **Skills** | 41 (+ 1 template) |
| **Orchestrators** | 5 (1 RDC top + 3 RDC phases, 1 writing, 1 AI memo) |
| **Chains** | 3 end-to-end (RDC, AI memo, analyze-writing) |
| **Stances covered** | All four — `socratic`, `hint`, `reframe`, `meta` |
| **Schema** | Team-Guide v0.2 (zero validation errors) |
| **Course** | POLI SCI 210, Spring 2026 |

Course assignments supported: weekly quizzes, research design critiques (RDCs, 700–1,000 words ×7), AI memos (500–1,000 words ×4), section participation.

---

## Catalog by group

### Reading & comprehension (8)

| skill | one-liner |
|---|---|
| [`comp-check`](skills/comp-check/skills.md) | Socratic probing of a specific reading without summarizing it. |
| [`explain-back-check`](skills/explain-back-check/skills.md) | Feynman-style: student explains in their own words; tutor probes. |
| [`decompose-arg`](skills/decompose-arg/skills.md) | Map a reading's argument as thesis → main claims → sub-claims/evidence. |
| [`compare-readings`](skills/compare-readings/skills.md) | Articulate similarities, differences, tensions across two sources. |
| [`tie-to-course`](skills/tie-to-course/skills.md) | Connect a reading to course objectives and prior weeks. |
| [`concept-example`](skills/concept-example/skills.md) | Student produces their own example; tutor probes whether it fits. |
| [`source-credibility`](skills/source-credibility/skills.md) | Assess authorship, methodology, venue, bias by question, not verdict. |
| [`quiz-prep`](skills/quiz-prep/skills.md) | Practice questions at varying difficulty; hints, not answers. |

### Writing (5 + 1 orchestrator)

| skill | one-liner |
|---|---|
| [`analyze-writing`](skills/analyze-writing/skills.md) | **Orchestrator.** Auto-classifies plan vs. draft mode; routes through writing sub-skills. |
| [`scaffold-writing`](skills/scaffold-writing/skills.md) | Walks structure of short-form academic writing without drafting any. |
| [`cohesion-check`](skills/cohesion-check/skills.md) | Sentence/paragraph transitions; topic chains, given-new flow. |
| [`flow-check`](skills/flow-check/skills.md) | Order of argument sections; inter-section logical progression. |
| [`evidence-placement`](skills/evidence-placement/skills.md) | Whether evidence sits next to the claim it supports. |
| [`reasoning-check`](skills/reasoning-check/skills.md) | Warrants linking evidence to claims; surfaces logical gaps. |

### Research Design Critique chain (1 top + 3 phase orchestrators + 9 leaves)

The RDC chain implements a 3-phase pedagogy: **investigate → map → judge**. Generic enough to apply to any class teaching empirical paper critique.

| skill | role | one-liner |
|---|---|---|
| [`critique-design`](skills/critique-design/skills.md) | **top orchestrator** | Routes through phases 1–3; hands off to `scaffold-writing`. |
| [`orient-paper`](skills/orient-paper/skills.md) | **Phase 1 (grasp)** | Sub-orchestrator: orient → trace evidence → probe choices. |
| [`first-pass-orient`](skills/first-pass-orient/skills.md) | Phase 1 leaf | Initial orientation: question, design type, headline finding. |
| [`trace-evidence`](skills/trace-evidence/skills.md) | Phase 1 leaf | Trace headline claim to the specific table/figure that supports it. |
| [`author-choices`](skills/author-choices/skills.md) | Phase 1 leaf | Surface 2–3 design choices with plausible alternatives. |
| [`map-design`](skills/map-design/skills.md) | **Phase 2 (map)** | Sub-orchestrator: skeleton → operationalization → method-week alignment. |
| [`design-skeleton`](skills/design-skeleton/skills.md) | Phase 2 leaf | Build a structured map: question, hypothesis, design type, sample, treatment, outcome. |
| [`op-check`](skills/op-check/skills.md) | Phase 2 leaf | Bridge concept to measure; surface operationalization gaps. |
| [`method-align`](skills/method-align/skills.md) | Phase 2 leaf | Apply the week's method-specific course concerns to the paper's design. |
| [`form-critique`](skills/form-critique/skills.md) | **Phase 3 (judge)** | Sub-orchestrator: inference threats → scope → alternatives. |
| [`inference-threats`](skills/inference-threats/skills.md) | Phase 3 leaf | Threats to inference *within* the studied sample (internal validity). |
| [`scope-check`](skills/scope-check/skills.md) | Phase 3 leaf | Conditions under which the claim might not hold *outside* the sample. |
| [`alt-designs`](skills/alt-designs/skills.md) | Phase 3 leaf | Propose 1–2 concrete design changes addressing surfaced critiques. |

### AI Memo chain (1 orchestrator + 3 sub-skills, reuses `scaffold-writing`)

The only chain in the catalog that crosses tutor↔AI mode boundaries. Claude leaves tutor mode for the explanation phase, then returns for evaluation.

| skill | role | one-liner |
|---|---|---|
| [`ai-memo`](skills/ai-memo/skills.md) | **top orchestrator** | Routes the chain; manages mode-transition banners. |
| [`pick-week-concept`](skills/pick-week-concept/skills.md) | step 1 | Narrow a week's slides to one concrete memo-shaped concept. |
| [`ai-explain`](skills/ai-explain/skills.md) | step 2 | **Leaves tutor mode.** Claude as rote AI source; transcript captured. |
| [`eval-ai-response`](skills/eval-ai-response/skills.md) | step 3 | Evaluate AI's transcript against course material (back in tutor mode). |
| `scaffold-writing` | step 4 | (reused from writing group) — structures the 500–1,000 word memo. |

### Stance archetypes — moment-to-moment moves (5)

Freestanding skills covering all four Team-Guide stances. Invocable from any conversation; not bound to a specific assignment. No `logic.py`, no scratchpads (pure prompt flows).

| skill | stance | one-liner |
|---|---|---|
| [`adjust-to-level`](skills/adjust-to-level/skills.md) | meta | Recalibrate explanation depth/vocabulary on signal. |
| [`reframe-trace`](skills/reframe-trace/skills.md) | reframe | Walk one concrete worked example step-by-step. |
| [`concept-hint`](skills/concept-hint/skills.md) | hint | Name the principle when Socratic probing has stalled. |
| [`counter-example`](skills/counter-example/skills.md) | socratic | Student finds a falsifying case for their own claim. |
| [`ask-prediction`](skills/ask-prediction/skills.md) | socratic | Commit to a prediction before any reveal. |

### Cross-cutting & metacognition (5)

Closes gaps not addressed by the chains: stats interpretation, hypothesis formation, peer review, end-of-session reflection, quiz-time strategy.

| skill | stance | one-liner |
|---|---|---|
| [`stat-intuition`](skills/stat-intuition/skills.md) | socratic | Translate coefficients/p-values into substantive units the student can feel. |
| [`frame-hypothesis`](skills/frame-hypothesis/skills.md) | socratic | Sharpen a research intuition into a falsifiable hypothesis. |
| [`play-reviewer`](skills/play-reviewer/skills.md) | meta | Switch student from writer-mode to reviewer-mode on a draft. |
| [`session-reflect`](skills/session-reflect/skills.md) | meta | End-of-session reflection log; consolidates across skills. |
| [`quiz-triage`](skills/quiz-triage/skills.md) | meta | Diagnose during-quiz time/triage failure modes; rule-test. |

### Template (1)

[`example-skill`](skills/example-skill/skills.md) — the v0.2 schema template. Use as a starting point for new skills.

---

## Orchestrator flow diagrams

### Research Design Critique

```
critique-design (top)
├── orient-paper (Phase 1: grasp)
│   ├── first-pass-orient
│   ├── trace-evidence    ← optional callout: stat-intuition
│   └── author-choices
├── map-design (Phase 2: map)
│   ├── design-skeleton
│   ├── op-check
│   └── method-align
├── form-critique (Phase 3: judge)
│   ├── inference-threats
│   ├── scope-check
│   └── alt-designs
├── (handoff)             → scaffold-writing
└── (close)               ← optional callout: session-reflect
```

### AI Memo

```
ai-memo (top)
├── pick-week-concept            (tutor mode)
├── --- mode banner: tutor → AI ---
├── ai-explain                   (rote AI mode; writes transcript)
├── --- mode banner: AI → tutor ---
├── eval-ai-response             (tutor mode)
├── scaffold-writing             (tutor mode; reused)
└── (close)                      ← optional callout: session-reflect
```

### Analyze Writing

```
analyze-writing (top)
├── (auto-classify: plan vs. draft)
├── plan mode chain:
│   ├── scaffold-writing
│   └── decompose-arg
├── draft mode chain:
│   ├── decompose-arg
│   ├── flow-check
│   ├── evidence-placement
│   ├── reasoning-check
│   └── cohesion-check
├── (finalize)                   ← optional callout: play-reviewer (draft mode only)
└── (close)                      ← optional callout: session-reflect
```

---

## Cross-orchestrator wiring

These skills are invoked **optionally** by orchestrators when specific conversational signals fire. The orchestrator offers; the student opts in.

| from | step | invokes | trigger |
|---|---|---|---|
| `trace-evidence` | Step 3 (read what's there) | `stat-intuition` | Student names a number but glosses over its substantive meaning. |
| `analyze-writing` | Step 7 (finalize) | `play-reviewer` | Draft mode only. Adversarial pass before close. |
| `analyze-writing` | Step 7 (finalize) | `session-reflect` | After recap, before exit. |
| `ai-memo` | Step 8 (finalize) | `session-reflect` | Especially valuable post-mode-crossing chain. |
| `critique-design` | Step 7 (handoff) | `session-reflect` | After 13-skill chain consolidates. |

---

## Stance coverage

| stance | what it does | skills |
|---|---|---|
| **socratic** | Asks back instead of answering. | All reading, writing, RDC-leaf, AI-evaluation skills + `counter-example`, `ask-prediction`, `stat-intuition`, `frame-hypothesis` |
| **hint** | Gives a partial answer / directional pointer when asking-back has stalled. | `concept-hint`, `quiz-prep`, `ai-explain` |
| **reframe** | Restates the situation in different terms (e.g., concrete trace). | `reframe-trace` |
| **meta** | Acts on the tutoring process itself (mode shifts, calibration, reflection). | All orchestrators + `adjust-to-level`, `play-reviewer`, `session-reflect`, `quiz-triage` |

---

## Repository layout

```
poli_sci-210-skills/
├── metadata.yaml              # course id + spoc contact + skills_used
├── README.md                  # this file
├── Team-Guide.md              # v0.2 schema reference
├── skills/
│   └── <skill-id>/
│       ├── skills.md          # YAML header + tutor flow (mandatory)
│       └── logic.py           # OPTIONAL — only when the skill needs helper logic / completion gates
├── materials/                 # course slides, readings
├── students/                  # per-student session logs and submissions
│   └── <name>/
│       ├── session-logs/      # written by `session-reflect`
│       ├── ai-memos/          # transcripts written by `ai-explain`
│       └── submissions/       # student drafts
└── docs/                      # gitignored — working notes
```

### Schema conventions (per Team-Guide v0.2)

- `skill_id` — kebab-case, ≤ 18 characters, must match folder name.
- `name` — Title Case, no trailing `"Skill"`.
- `skill_type` — `instructional` (no `logic.py` required) or `code` (`logic.py` required).
- `stance` — `socratic` | `hint` | `reframe` | `meta` (instructional only).
- `course_types` — subset of `["cs", "humanities"]`.
- `learning_goal_tags` — at least one tag from the controlled vocabulary.
- `python_entry` — declared **only if** `logic.py` is shipped.

Run validation locally:

```bash
python3 -c "
import os, re, yaml
for d in sorted(os.listdir('skills')):
    p = f'skills/{d}/skills.md'
    if not os.path.isfile(p): continue
    m = re.match(r'^---\n(.*?)\n---', open(p).read(), re.DOTALL)
    meta = yaml.safe_load(m.group(1))
    print(d, '✓' if meta.get('skill_id') == d else '✗')
"
```

---

## Adopting skills from this repo

Per Team-Guide §9: any team can fetch a skill by id:

```bash
python scripts/fetch_skill.py --id <skill-id>
```

The skills with the broadest cross-course applicability:

- **Stance archetypes:** `counter-example`, `ask-prediction`, `concept-hint`, `reframe-trace`, `adjust-to-level`
- **Metacognition:** `session-reflect`, `quiz-triage`
- **Writing:** `scaffold-writing`, `cohesion-check`, `flow-check`, `evidence-placement`, `reasoning-check`
- **Empirical critique pattern:** the entire `critique-design` → `orient-paper` → `map-design` → `form-critique` chain is generic for any class teaching empirical paper critique.

POLI SCI 210-specific (less directly portable): `tie-to-course`, `method-align`, the `ai-memo` chain (built around the course's specific AI-memo assignment).

---

## Course context

POLI SCI 210 is Northwestern's intro empirical methods course in political science. Students learn to:

- Read and analyze political-science research papers.
- Distinguish descriptive vs. causal inference claims.
- Identify research-design types and weigh strengths/weaknesses.
- Design and critique experiments and observational studies.
- Communicate methodological evaluations in writing.

Every skill in this catalog is Socratic-by-default — the student does the thinking, which is the same demand the course's assignments make.

---

## Maintainers

- **SPOC contact:** [bryanmurray2026@u.northwestern.edu](mailto:bryanmurray2026@u.northwestern.edu)
- **Course ID:** POLISCI-210
