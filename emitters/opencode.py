from __future__ import annotations

import json
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
        count = 0

        knowledge = ir_dict.get("knowledge", [])
        if isinstance(knowledge, dict):
            knowledge = list(knowledge.values())

        for k in knowledge:
            kind = k.get("kind")
            if kind not in {"rule", "principle", "reference", "policy", "skill"}:
                continue

            skill_path = skills_dir / f"{k['id']}.md"
            summary = k.get("content", {}).get("summary", "")
            raw = k.get("content", {}).get("raw", "")[:2500]

            content = f"""---
id: {k['id']}
type: {kind}
domain: {k['domain']}
generated_at: {_now_iso()}
---

# {summary}

{raw}

<!-- OpenCode Skill Reference -->
<!-- Domain: {k['domain']} -->
"""

            _safe_write(skill_path, content)
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
