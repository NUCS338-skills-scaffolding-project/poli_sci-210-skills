# validate_skills.py
# Checks all skills.md files for required YAML metadata fields
# If any fields are missing, the GitHub Action will fail and block the push

import os
import sys
import frontmatter

# These are the required fields every skills.md must have
REQUIRED_FIELDS = ["skill_id", "name", "tags", "python_entry"]

def validate_all_skills(root_dir="skills"):
    errors = []
    found = False

    for root, dirs, files in os.walk(root_dir):
        if "skills.md" in files:
            found = True
            filepath = os.path.join(root, "skills.md")

            with open(filepath) as f:
                post = frontmatter.load(f)

            # Check for each required field
            for field in REQUIRED_FIELDS:
                if field not in post.metadata:
                    errors.append(
                        f"ERROR: MISSING '{field}' in {filepath}"
                    )

    if not found:
        print("ERROR: No skills.md files found — skipping validation.")
        sys.exit(0)

    if errors:
        print("\nERROR: Validation Failed! Fix these issues before pushing:\n")
        for e in errors:
            print(e)
        print("\n💡 Every skills.md must include:")
        print("   skill_id, name, tags, python_entry")
        sys.exit(1)  # This fails the GitHub Action and blocks the push
    else:
        print("SUCCESS: All skills.md files passed validation!")
        sys.exit(0)

if __name__ == "__main__":
    validate_all_skills()
