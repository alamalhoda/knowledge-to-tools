from pathlib import Path
from collections import defaultdict
import sys

ROOT = Path(".ai/knowledge")
INDEX_FILE = ROOT / "index.md"

REQUIRED_FIELDS = [
    "title",
    "summary",
    "domain",
    "category",
    "priority"
]


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, None

    parts = text.split("---", 2)
    meta_block = parts[1]
    body = parts[2] if len(parts) > 2 else ""

    meta = {}
    for line in meta_block.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()

    return meta, body


def lint_rule(path, meta):
    errors = []

    if meta is None:
        errors.append("Missing frontmatter")
        return errors

    for field in REQUIRED_FIELDS:
        if field not in meta or not meta[field]:
            errors.append(f"Missing or empty field: {field}")

    return errors


def collect_rules():
    rules = []
    errors_found = False

    for file in ROOT.rglob("*.md"):
        if file.name == "index.md":
            continue

        text = file.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)

        errors = lint_rule(file, meta)

        if errors:
            errors_found = True
            print(f"\n❌ {file}")
            for e in errors:
                print(f"   - {e}")

        else:
            rules.append((file, meta))

    return rules, errors_found


def build_index(rules):

    tree = defaultdict(lambda: defaultdict(list))

    for file, meta in rules:
        domain = meta["domain"]
        category = meta["category"]
        title = meta["title"]
        rel_path = file.relative_to(ROOT)

        tree[domain][category].append((title, rel_path))

    lines = [
        "# AI Knowledge Base",
        "",
        "---",
        "",
        "## 📚 Index",
        ""
    ]

    for domain in sorted(tree.keys()):
        lines.append(f"## {domain.capitalize()}")
        lines.append("")

        for category in sorted(tree[domain].keys()):
            lines.append(f"### {category}")
            lines.append("")

            for title, rel_path in sorted(tree[domain][category]):
                lines.append(f"- [{title}]({rel_path})")

            lines.append("")

    return "\n".join(lines)


def build_rule_graph(rules):

    lines = [
        "",
        "---",
        "",
        "## 🕸 Rule Graph",
        "",
        "```",
]

    for file, meta in rules:
        lines.append(f"{meta['domain']}::{meta['category']}::{meta['title']}")

        lines.append("```")

    return "\n".join(lines)


def main():

    print("🔍 Running Knowledge Audit...\n")

    rules, has_errors = collect_rules()

    if has_errors:
        print("\n🚨 Lint errors detected.")
        sys.exit(1)

    print("✅ Lint passed.\n")

    index_content = build_index(rules)
    graph_content = build_rule_graph(rules)

    INDEX_FILE.write_text(index_content + graph_content, encoding="utf-8")

    print(f"✅ Index + Graph generated at {INDEX_FILE}")
    print("\n🎯 Knowledge base is healthy.\n")


if __name__ == "__main__":
    main()
