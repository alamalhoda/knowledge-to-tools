#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    raise

try:
    import jsonschema
except ImportError:
    print("jsonschema is required: pip install jsonschema", file=sys.stderr)
    raise


ROOT = Path(__file__).resolve().parents[1]  # adjust if script location differs
KNOWLEDGE_DIR = ROOT / "knowledge"
SCHEMA_PATH = ROOT / "schema" / "knowledge.index.schema.json"
OUTPUT_PATH = KNOWLEDGE_DIR / "index.json"


ALLOWED_DOMAINS = {"shared", "frontend", "backend", "devops", "security", "data"}
ALLOWED_KINDS = {
    "rule", "policy", "principle", "architecture",
    "pattern", "workflow", "skill", "reference"
}
ALLOWED_STATUS = {"draft", "active", "deprecated"}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """
    Returns (metadata, body)
    Supports YAML frontmatter:
    ---
    key: value
    ---
    """
    if not content.startswith("---"):
        return {}, content

    parts = content.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, content

    fm_block = parts[0].replace("---\n", "", 1)
    body = parts[1]
    metadata = yaml.safe_load(fm_block) or {}
    if not isinstance(metadata, dict):
        return {}, content
    return metadata, body


def infer_from_path(path: Path) -> dict[str, str]:
"""
Infer domain/category from structure:
  knowledge/<domain>/<category>/<file>.md
"""
    rel = path.relative_to(KNOWLEDGE_DIR)
    parts = rel.parts

    inferred = {
        "domain": "shared",
        "category": "reference",
    }

    if len(parts) >= 2:
        inferred["domain"] = parts[0]
        inferred["category"] = parts[1] if len(parts) >= 3 else "reference"
    elif len(parts) == 1:
        inferred["domain"] = "shared"
        inferred["category"] = "reference"

    return inferred


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    return []


def build_document(path: Path) -> Optional[dict[str, Any]]:
    content = read_file(path)
    metadata, body = split_frontmatter(content)
    inferred = infer_from_path(path)

    title = metadata.get("title")
    if not title:
        # fallback from filename
        title = path.stem.replace("-", " ").replace("_", " ").title()

    domain = str(metadata.get("domain") or inferred["domain"]).strip().lower()
    category = str(metadata.get("category") or inferred["category"]).strip().lower()
    kind = str(metadata.get("kind") or "reference").strip().lower()
    status = str(metadata.get("status") or "active").strip().lower()

    # validation / normalization
    if domain not in ALLOWED_DOMAINS:
        domain = "shared"
    if kind not in ALLOWED_KINDS:
        kind = "reference"
    if status not in ALLOWED_STATUS:
        status = "active"

    doc_id = metadata.get("id")
    if not doc_id:
        # stable id from relative path without extension
        rel_no_ext = path.relative_to(KNOWLEDGE_DIR).with_suffix("")
        doc_id = slugify("-".join(rel_no_ext.parts))
    else:
        doc_id = slugify(str(doc_id))

    tags = normalize_list(metadata.get("tags"))
    applies_to = normalize_list(metadata.get("applies_to"))
    depends_on = normalize_list(metadata.get("depends_on"))
    related = normalize_list(metadata.get("related"))

    priority = metadata.get("priority", 50)
    try:
        priority = int(priority)
    except Exception:
        priority = 50
    priority = max(0, min(100, priority))

    checksum = sha256_text(content)

    document = {
        "id": doc_id,
        "title": str(title).strip(),
        "path": str(path.relative_to(ROOT).as_posix()),
        "domain": domain,
        "category": category,
        "kind": kind,
        "tags": tags,
        "priority": priority,
        "status": status,
        "applies_to": applies_to,
        "depends_on": depends_on,
        "related": related,
        "checksum": checksum,
    }

    # remove empty optional arrays to keep output cleaner
    cleaned = {}
    for k, v in document.items():
        if isinstance(v, list) and not v:
            continue
        cleaned[k] = v

    return cleaned


def collect_markdown_files() -> list[Path]:
    files = []
    for p in KNOWLEDGE_DIR.rglob("*.md"):
        if p.name.startswith("."):
            continue
        if p.name.lower() == "index.md":
            continue
        files.append(p)
    return sorted(files)


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def main() -> int:
    if not KNOWLEDGE_DIR.exists():
        print(f"Knowledge directory not found: {KNOWLEDGE_DIR}", file=sys.stderr)
        return 1

    schema = load_schema()
    documents: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for path in collect_markdown_files():
        doc = build_document(path)
        if not doc:
            continue

        if doc["id"] in seen_ids:
            print(f"[WARN] Duplicate id skipped: {doc['id']} ({path})", file=sys.stderr)
            continue

        seen_ids.add(doc["id"])
        documents.append(doc)

    # sort for deterministic output
    documents.sort(key=lambda d: (
        d.get("domain", ""),
        d.get("category", ""),
        -int(d.get("priority", 50)),
        d.get("title", "")
    ))

    index = {
        "version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "source": "knowledge",
        "documents": documents,
    }

    # validate against schema
    jsonschema.validate(instance=index, schema=schema)

    OUTPUT_PATH.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    print(f"Generated: {OUTPUT_PATH}")
    print(f"Documents: {len(documents)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
