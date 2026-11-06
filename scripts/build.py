#!/usr/bin/env python3
"""Validate skills, build zip archives in dist/, update .claude-plugin/marketplace.json
and the skills table in README.md.

Usage:
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
README = ROOT / "README.md"

MARKETPLACE_NAME = "ai-skills"
OWNER = {"name": "Mikhail Sidelnikov"}

NAME_RE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
VERSION_RE = re.compile(r"\d+\.\d+\.\d+")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
README_START = "<!-- skills:start -->"
README_END = "<!-- skills:end -->"
# Fixed timestamp so zips only change when their content changes.
ZIP_DATE = (2020, 1, 1, 0, 0, 0)


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        inner = value[1:-1]
        return inner.replace("''", "'") if value[0] == "'" else inner.replace('\\"', '"')
    return value


def read_frontmatter(skill_md: Path) -> dict:
    """Minimal YAML frontmatter parser: `key: value`, quoted values,
    block scalars (`|`, `>`) and indented continuation lines."""
    text = skill_md.read_text(encoding="utf-8").replace("\r\n", "\n")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError(f"{skill_md}: missing frontmatter (--- block at the top of the file)")
    data, key, block = {}, None, None
    for line in match.group(1).splitlines():
        if line[:1] in (" ", "\t") and key:
            sep = "\n" if block == "|" else " "
            data[key] = (data[key] + sep + line.strip()).strip()
            continue
        if ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        block = value[0] if value[:1] in ("|", ">") else None
        data[key] = "" if block else unquote(value)
    return data


def is_packaged(rel: Path) -> bool:
    """Skip hidden files/folders (.DS_Store etc.) and Python caches."""
    return not any(part.startswith(".") or part == "__pycache__" for part in rel.parts)


def build_zip(skill_dir: Path) -> Path:
    zip_path = DIST / f"{skill_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(skill_dir.rglob("*")):
            rel = file.relative_to(skill_dir.parent)
            if not is_packaged(rel) or not file.is_file():
                continue
            info = zipfile.ZipInfo(rel.as_posix(), ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, file.read_bytes())
    return zip_path


def update_readme(entries: list) -> None:
    text = README.read_text(encoding="utf-8")
    if README_START not in text or README_END not in text:
        raise ValueError(f"README.md: markers {README_START} / {README_END} not found")
    rows = ["| Skill | Description | Download |", "|---|---|---|"]
    for e in entries:
        link = f"plugins/{e['name']}/skills/{e['name']}/SKILL.md"
        desc = e["description"].replace("|", "\\|")
        rows.append(f"| [{e['name']}]({link}) | {desc} | [zip](https://github.com/sidelnikovmike/ai-skills/raw/main/dist/{e['name']}.zip) |")
    table = "\n".join(rows)
    pattern = re.compile(re.escape(README_START) + r".*?" + re.escape(README_END), re.S)
    README.write_text(pattern.sub(f"{README_START}\n{table}\n{README_END}", text), encoding="utf-8")


def validate_skill(skill_dir: Path, errors: list) -> bool:
    try:
        fm = read_frontmatter(skill_dir / "SKILL.md")
    except ValueError as exc:
        errors.append(str(exc))
        return False
    name, desc = fm.get("name", ""), fm.get("description", "")
    ok = True
    if name != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name must match the folder name")
        ok = False
    if not NAME_RE.fullmatch(name) or len(name) > MAX_NAME:
        errors.append(f"{skill_dir.name}: name must be lowercase letters, digits and hyphens, up to {MAX_NAME} chars")
        ok = False
    if not desc:
        errors.append(f"{skill_dir.name}: empty description in frontmatter")
        ok = False
    elif len(desc) > MAX_DESCRIPTION:
        errors.append(f"{skill_dir.name}: description is {len(desc)} chars, max {MAX_DESCRIPTION}")
        ok = False
    if "<" in desc or ">" in desc:
        errors.append(f"{skill_dir.name}: description must not contain angle brackets")
        ok = False
    return ok


def main() -> None:
    errors, entries = [], []
    DIST.mkdir(exist_ok=True)

    for plugin_dir in sorted(p for p in PLUGINS.iterdir() if p.is_dir()):
        name = plugin_dir.name
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        if not manifest_path.exists():
            errors.append(f"{name}: missing .claude-plugin/plugin.json")
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("name") != name:
            errors.append(f"{name}: name in plugin.json must match the folder name")
        if not VERSION_RE.fullmatch(str(manifest.get("version", ""))):
            errors.append(f"{name}: version in plugin.json must look like 1.2.3")
        if not manifest.get("description"):
            errors.append(f"{name}: empty description in plugin.json")

        skill_dirs = sorted(d for d in (plugin_dir / "skills").glob("*") if (d / "SKILL.md").exists())
        if not skill_dirs:
            errors.append(f"{name}: no skills/<name>/SKILL.md found")
            continue

        for skill_dir in skill_dirs:
            if validate_skill(skill_dir, errors):
                print(f"  dist/{build_zip(skill_dir).name}")

        entries.append({
            "name": name,
            "source": f"./plugins/{name}",
            "description": manifest.get("description", ""),
            "version": manifest.get("version", "0.1.0"),
        })

    if errors:
        print("\nErrors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    MARKETPLACE.parent.mkdir(exist_ok=True)
    MARKETPLACE.write_text(
        json.dumps({"name": MARKETPLACE_NAME, "owner": OWNER, "plugins": entries}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nmarketplace.json updated: {len(entries)} skill(s)")
    try:
        update_readme(entries)
        print("README.md skills table updated")
    except ValueError as exc:
        sys.exit(f"\nError: {exc}")


if __name__ == "__main__":
    main()
