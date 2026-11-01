#!/bin/bash
SKILLS_DIR="$HOME/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$SKILLS_DIR"

# Copies each skill folder in full (SKILL.md, references/, scripts/), skipping downloaded
# third-party binaries (vendor/) and Python caches. Existing local files that are not in the
# repo (for example a private references/casos-privados.md) are left untouched.
count=0
for skill_dir in "$SCRIPT_DIR/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    if [ -f "$skill_dir/SKILL.md" ]; then
        (cd "$skill_dir" && find . -type f -not -path "*/vendor/*" -not -path "*/__pycache__/*" -print0) |
        while IFS= read -r -d '' f; do
            mkdir -p "$SKILLS_DIR/$skill_name/$(dirname "$f")"
            cp "$skill_dir/$f" "$SKILLS_DIR/$skill_name/$f"
        done
        echo "Installed: $skill_name"
        count=$((count + 1))
    fi
done

echo "Done. $count skills installed to $SKILLS_DIR"
echo "Skills that need a third-party download (e.g. accesibilidad-wcag) explain it in their SKILL.md."
