from pathlib import Path
from typing import Any, Dict, List, Tuple


SOURCE_ROOT = Path("old_cursor_rules")
DEST_ROOT = Path(".ai/knowledge")


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    meta_text = parts[1]
    body = parts[2].strip()

    meta = {}
    globs = []

    for line in meta_text.splitlines():
        line = line.strip()

        if line.startswith("description:"):
            meta["description"] = line.split(":", 1)[1].strip()

        elif line.startswith("alwaysApply:"):
            value = line.split(":", 1)[1].strip().lower()
            meta["alwaysApply"] = value == "true"

        elif line.startswith("- "):
            globs.append(line[2:].strip())

    if globs:
        meta["globs"] = globs

    return meta, body


def map_priority(always_apply: bool) -> int:
    return 80 if always_apply else 50


def build_title(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title()


def extract_domain_category(path: Path) -> Tuple[str, str]:
    parts = path.parts
    domain = parts[1] if len(parts) > 1 else "shared"
    category = parts[2] if len(parts) > 2 else "general"
    return domain, category


def build_frontmatter(meta: Dict[str, Any]) -> str:
    lines = [
        "---",
        f"title: {meta['title']}",
        f"summary: {meta['summary']}",
        f"domain: {meta['domain']}",
        f"category: {meta['category']}",
        "applies_to:",
    ]

    for g in meta.get("applies_to", []):
        lines.append(f"  - {g}")

    lines.append(f"priority: {meta['priority']}")
    lines.append("---\n")

    return "\n".join(lines)


def convert_file(src_file: Path) -> None:
    text = src_file.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    domain, category = extract_domain_category(src_file)

    new_meta = {
        "title": build_title(src_file.stem),
        "summary": meta.get("description", ""),
        "domain": domain,
        "category": category,
        "applies_to": meta.get("globs", []),
        "priority": map_priority(meta.get("alwaysApply", False)),
    }

    frontmatter = build_frontmatter(new_meta)

    relative = src_file.relative_to(SOURCE_ROOT)
    dest_file = (DEST_ROOT / relative).with_suffix(".md")

    dest_file.parent.mkdir(parents=True, exist_ok=True)

    dest_file.write_text(frontmatter + "\n" + body + "\n", encoding="utf-8")

    print(f"✅ {src_file} -> {dest_file}")


def main() -> None:
    files = list(SOURCE_ROOT.rglob("*.mdc"))

    print(f"Found {len(files)} cursor rules\n")

    for f in files:
        convert_file(f)

    print("\n✅ Migration finished\n")


if __name__ == "__main__":
    main()
