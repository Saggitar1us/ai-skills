#!/usr/bin/env python3
"""Create a new skill from the template.

Usage:
    python3 scripts/new_skill.py my-skill "One sentence on when to use the skill"
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "template"
PLUGINS = ROOT / "plugins"
DEFAULT_AUTHOR = "Mikhail Sidelnikov"


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit('Usage: python3 scripts/new_skill.py <skill-name> "<description>"')

    name, description = sys.argv[1], sys.argv[2]
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        sys.exit("Name: lowercase letters, digits and hyphens, up to 64 chars (e.g. sales-coach).")
    if "<" in description or ">" in description:
        sys.exit("Description must not contain angle brackets.")

    target = PLUGINS / name
    if target.exists():
        sys.exit(f"Skill {name} already exists: {target}")

    shutil.copytree(TEMPLATE, target, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))
    (target / "skills" / "SKILL_NAME").rename(target / "skills" / name)

    title = name.replace("-", " ").capitalize()
    for path in target.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            text = (text.replace("SKILL_NAME", name)
                        .replace("SKILL_DESCRIPTION", description.replace('"', '\\"') if path.suffix == ".json" else description)
                        .replace("SKILL_TITLE", title)
                        .replace("AUTHOR_NAME", DEFAULT_AUTHOR))
            path.write_text(text, encoding="utf-8")

    print(f"Done: {target.relative_to(ROOT)}")
    print(f"Edit plugins/{name}/skills/{name}/SKILL.md, then run: python3 scripts/build.py")


if __name__ == "__main__":
    main()
