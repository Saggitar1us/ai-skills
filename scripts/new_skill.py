#!/usr/bin/env python3
"""Создаёт новый скилл из шаблона.

Использование:
    python3 scripts/new_skill.py my-skill "Короткое описание, когда использовать скилл"
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
        sys.exit('Использование: python3 scripts/new_skill.py <имя-скилла> "<описание>"')

    name, description = sys.argv[1], sys.argv[2]
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        sys.exit("Имя: латиница в нижнем регистре, цифры и дефисы, до 64 символов (например, sales-coach).")
    if "<" in description or ">" in description:
        sys.exit("В описании нельзя использовать угловые скобки.")

    target = PLUGINS / name
    if target.exists():
        sys.exit(f"Скилл {name} уже существует: {target}")

    shutil.copytree(TEMPLATE, target)
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

    print(f"Готово: {target.relative_to(ROOT)}")
    print(f"Отредактируйте plugins/{name}/skills/{name}/SKILL.md, затем запустите: python3 scripts/build.py")


if __name__ == "__main__":
    main()
