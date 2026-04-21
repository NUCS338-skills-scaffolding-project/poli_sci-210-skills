 Welcome to the Skills Scaffolding Project — Team Guide

This guide walks you through everything you need to do as a course team.
Follow these steps and you should be good to go!
Please reach out if you are stuck anywhere

---

## Your Task Checklist
- Generate your repository from the Admin template
- Define your course-level `metadata.yaml`
- Create `skills` folders for every unique learning objective
- Write `skills.md` using the mandatory schema
- Implement reusable Python logic in `logic.py`
- Verify your code runs locally before pushing

---

## Step 1 — Set Up Your Repository

> Do NOT create a new repo from scratch.

1. Go to the `skill-standard-template` repo in the Organization
2. Click the green **"Use this template"** button
3. Name your repo using your course ID e.g. `CS213-skills`
4. Set the **Owner** to the Organization *(not your personal account)*
5. Click **"Create repository"**

---

## Step 2 — Create Your Course Metadata

In the root of your repo, create a file called `metadata.yaml`:

```yaml
course_id: "COURSE-01"
course_name: "Your Course Name Here"
team: "team-01"
spoc_contact: "admin@example.com" : the person who would be the main contact for the team
```

> Fill in your own course ID, name, and team name.

---

## Step 3 — Develop a Skill

For **every skill** your course teaches, do the following:

### 3a — Create the Skill Folder
Inside `/skills/`, create a folder named after your skill: /skills/your-skill-name/
### 3b — Create skills.md
Create a `skills.md` file inside that folder.
You **must** include this YAML header at the very top:

```yaml
---
skill_id: "SKILL-NAME"
name: "Human Readable Skill Name"
tags: ["topic1", "topic2"]
python_entry: "logic.py"
---
```

Then below the header, document your skill:

```markdown
# Skill Name

## Description
What does this skill teach or do?

## Usage
How should other teams use this skill?

## Example
Give a short example here.
```

> If the YAML header is missing or incomplete, your push will be
> automatically rejected by the Admin's validation rule.

### 3c — Write Your Logic
Create a `logic.py` file in the same folder.
Make it **modular** so other teams can import it:

```python
def run(input):
    """
    Main entry point for this skill.
    :param input: dict of input parameters
    :return: result
    """
    return f"Skill executed with input: {input}"
```

---

## Step 4 — Verify Before Pushing

Before pushing your changes, make sure:
- Your `skills.md` has the full YAML header at the top
- `skill_id` follows the format: `SKILL-NAME`
- `logic.py` is in the same folder as `skills.md`
- Your Python code runs without errors locally

---

## Step 5 — Push Your Changes

Once everything looks good:

1. Commit your changes to the `main` branch
2. The Admin's system will **automatically detect** your new skill
3. It will be added to the global `catalog.json` in the Skills Registry
4. Other teams will then be able to fetch your skill using:
```bash
   python scripts/fetch_skill.py --id SKILL-NAME
```

---

## 📁 Your Repo Structure Should Look Like This
your-repo/
├── metadata.yaml
├── skills/
│   ├── skill-one/
│   │   ├── skills.md
│   │   └── logic.py
│   └── skill-two/
│       ├── skills.md
│       └── logic.py
└── examples/
└── demo.py
---

## Common Issues

| Problem | Fix |
|--------|-----|
| Push rejected | Check your `skills.md` has all required YAML fields |
| Skill not in catalog | Make sure you pushed to `main` not another branch |
| Can't find template | Make sure you accepted your Organization invite email |
| YAML header not working | Make sure `---` is the very first line of the file |

---

## Need Help?
Reachout to us!
