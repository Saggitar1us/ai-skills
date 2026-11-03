#!/usr/bin/env python3
"""Проверяет скиллы, собирает zip-архивы в dist/ и обновляет .claude-plugin/marketplace.json.

Использование:
    python3 scripts/build.py
"""
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
DIST = ROOT / "dist"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

MARKETPLACE_NAME = "ai-skills"
OWNER = {"name": "Mikhail Sidelnikov"}


def read_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError(f"{skill_md}: нет frontmatter (блока --- в начале файла)")
    data = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def main() -> None:
    errors, entries = [], []
    DIST.mkdir(exist_ok=True)

    for plugin_dir in sorted(p for p in PLUGINS.iterdir() if p.is_dir()):
        name = plugin_dir.name
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        if not manifest_path.exists():
            errors.append(f"{name}: нет .claude-plugin/plugin.json")
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("name") != name:
            errors.append(f"{name}: name в plugin.json должно совпадать с именем папки")

        skill_dirs = sorted(d for d in (plugin_dir / "skills").glob("*") if (d / "SKILL.md").exists())
        if not skill_dirs:
            errors.append(f"{name}: нет ни одного skills/<имя>/SKILL.md")
            continue

        for skill_dir in skill_dirs:
            try:
                fm = read_frontmatter(skill_dir / "SKILL.md")
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if fm.get("name") != skill_dir.name:
                errors.append(f"{skill_dir}: name во frontmatter должно совпадать с именем папки")
            if not fm.get("description"):
                errors.append(f"{skill_dir}: пустое description во frontmatter")

            # Архив для загрузки в Claude: папка скилла целиком
            zip_path = DIST / f"{skill_dir.name}.zip"
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for file in sorted(skill_dir.rglob("*")):
                    if file.is_file():
                        zf.write(file, file.relative_to(skill_dir.parent))
            print(f"  dist/{zip_path.name}")

        entries.append({
            "name": name,
            "source": f"./plugins/{name}",
            "description": manifest.get("description", ""),
            "version": manifest.get("version", "0.1.0"),
        })

    if errors:
        print("\nОшибки:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    MARKETPLACE.parent.mkdir(exist_ok=True)
    MARKETPLACE.write_text(
        json.dumps({"name": MARKETPLACE_NAME, "owner": OWNER, "plugins": entries}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nmarketplace.json обновлён: {len(entries)} скилл(ов)")


if __name__ == "__main__":
    main()
