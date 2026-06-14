from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from .base import BaseEmitter
from ir.models import IRRoot


def _now_iso() -> str:
    return f"{datetime.now(timezone.utc).isoformat()}"


def _safe_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    _safe_write(path, json.dumps(data, indent=2, ensure_ascii=False))


def _normalize_skill_name(name: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    normalized = re.sub(r"-+", "-", normalized)
    return normalized[:64] or "skill"


def _yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _truncate_description(description: str) -> str:
    if len(description) <= 1024:
        return description
    return description[:1021] + "..."


def _raw_summary(raw: str) -> str:
    match = re.search(r"(?m)^summary:\s*(.+)$", raw or "")
    return match.group(1).strip() if match else ""


def _legacy_frontmatter(raw: str) -> str:
    match = re.match(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", raw or "", re.DOTALL)
    return match.group("body") if match else ""


def _parse_legacy_frontmatter(raw: str) -> Dict[str, str]:
    metadata: Dict[str, str] = {}
    current_list_key = ""

    for line in _legacy_frontmatter(raw).splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        list_match = re.match(r"^-\s*(.+)$", stripped)
        if list_match and current_list_key:
            list_value = list_match.group(1).strip().strip('"').strip("'")
            current_value = metadata.get(current_list_key, "")
            metadata[current_list_key] = f"{current_value}; {list_value}" if current_value else list_value
            continue

        key_match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not key_match:
            continue

        key, value = key_match.groups()
        value = value.strip().strip('"').strip("'")
        metadata[key] = value
        current_list_key = key if not value else ""

    return {key: value for key, value in metadata.items() if value and key in {
        "title",
        "summary",
        "domain",
        "category",
        "applies_to",
        "priority",
        "kind",
    }}


def _metadata_frontmatter(metadata: Dict[str, str]) -> str:
    if not metadata:
        return ""

    lines = ["metadata:"]
    for key in sorted(metadata):
        lines.append(f"  {key}: {_yaml_quote(metadata[key])}")

    return "\n".join(lines) + "\n"


def _strip_legacy_frontmatter(raw: str) -> str:
    return re.sub(r"\A---\s*\n.*?\n---\s*\n", "", raw or "", flags=re.DOTALL).lstrip()


def _skill_description(k: Dict[str, Any]) -> str:
    content = k.get("content", {})
    description = (
        content.get("description")
        or _raw_summary(content.get("raw", ""))
        or content.get("summary")
        or k.get("id", "skill").replace("-", " ").title()
    )
    return _truncate_description(str(description).strip() or "OpenCode skill")


def _skill_content(k: Dict[str, Any], description: str, skill_name: str) -> str:
    content = k.get("content", {})
    summary = content.get("summary", k.get("id"))
    raw = _strip_legacy_frontmatter(content.get("raw", ""))
    metadata = _metadata_frontmatter(_parse_legacy_frontmatter(content.get("raw", "")))

    return (
        f"---\n"
        f"name: {skill_name}\n"
        f"description: {_yaml_quote(description)}\n"
        f"{metadata}"
        f"---\n\n"
        f"# {summary}\n\n"
        f"{raw}\n"
    )


def _remove_legacy_skill_file(skills_dir: Path, skill_id: str, skill_name: str) -> None:
    for candidate in {skill_id, skill_name}:
        legacy_path = skills_dir / f"{candidate}.md"
        if legacy_path.is_file():
            legacy_path.unlink()


def _permission_action(value: bool) -> str:
    return "allow" if value else "deny"


def _permission_config(agent_ir: Dict[str, Any]) -> Dict[str, str]:
    permissions = agent_ir.get("permissions", {})
    permission = {
        "edit": _permission_action(permissions.get("edit", True)),
        "bash": _permission_action(permissions.get("shell", False)),
    }

    if permissions.get("network", False):
        permission["webfetch"] = "allow"
        permission["websearch"] = "allow"
    else:
        permission["webfetch"] = "deny"
        permission["websearch"] = "deny"

    return permission


def _agent_prompt(agent_ir: Dict[str, Any]) -> str:
    parts = []

    if agent_ir.get("role"):
        parts.append(agent_ir["role"])

    if agent_ir.get("behavior"):
        parts.append(f"Behavior: {json.dumps(agent_ir['behavior'], ensure_ascii=False)}")

    if agent_ir.get("authority"):
        parts.append(f"Authority: {json.dumps(agent_ir['authority'], ensure_ascii=False)}")

    return "\n\n".join(parts)


def _agent_config(agent_id: str, agent_ir: Dict[str, Any], default_agent_id: str) -> Dict[str, Any]:
    config = {
        "description": agent_ir.get("description", ""),
        "mode": "primary" if agent_id == default_agent_id else "subagent",
        "prompt": _agent_prompt(agent_ir),
        "permission": _permission_config(agent_ir),
    }

    return {key: value for key, value in config.items() if value not in ({}, "", [])}


class OpenCodeEmitter(BaseEmitter):
    """
    OpenCode-specific emitter — translates IRRoot to OpenCode format.
    Consumes IR only; does not read knowledge directly.
    """

    BASE_DIR = Path("aegis_output/opencode")

    def emit(self, ir: IRRoot, output_dir: Optional[Path] = None) -> None:
        ir_dict = self._ir_to_dict(ir)
        base = self._resolve_output_dir(output_dir)
        self._emit_skills(ir_dict, base)
        self._emit_agents(ir_dict, base)
        self._emit_config(ir_dict, base)
        print("🎉 OpenCodeEmitter: All OpenCode artifacts generated successfully!")

    def _emit_skills(self, ir_dict: Dict[str, Any], base: Path) -> None:
        skills_dir = base / "skills"
        skills_dir.mkdir(parents=True, exist_ok=True)
        count = 0

        knowledge = ir_dict.get("knowledge", [])
        if isinstance(knowledge, dict):
            knowledge = list(knowledge.values())

        for k in knowledge:
            kind = k.get("kind")
            if kind not in {"rule", "principle", "reference", "policy", "skill"}:
                continue

            skill_name = _normalize_skill_name(str(k["id"]))
            skill_dir = skills_dir / skill_name
            description = _skill_description(k)
            content = _skill_content(k, description, skill_name)

            _remove_legacy_skill_file(skills_dir, str(k["id"]), skill_name)
            _safe_write(skill_dir / "SKILL.md", content)
            count += 1

        print(f"✔ SkillsEmitter: Generated {count} skills.")

    def _emit_agents(self, ir_dict: Dict[str, Any], base: Path) -> None:
        agents_dir = base / "agents"
        count = 0
        agents = ir_dict.get("agents", {})
        default_agent_id = next(iter(agents.keys()), "")

        for agent_id, agent_ir in agents.items():
            agent_file = agents_dir / f"{agent_id}.json"
            _write_json(agent_file, _agent_config(agent_id, agent_ir, default_agent_id))
            count += 1

        print(f"✔ AgentsEmitter: Generated {count} agents.")

    def _emit_config(self, ir_dict: Dict[str, Any], base: Path) -> None:
        config_path = base / "opencode.json"
        agents = ir_dict.get("agents", {})
        default_agent_id = next(iter(agents.keys()), "")

        config = {
            "$schema": "https://opencode.ai/config.json",
            "default_agent": default_agent_id,
            "agent": {
                agent_id: _agent_config(agent_id, agent_ir, default_agent_id)
                for agent_id, agent_ir in agents.items()
            },
            "skills": {
                "paths": ["skills/"]
            }
        }

        _write_json(config_path, config)
        print("✔ ConfigEmitter: Generated opencode.json")
