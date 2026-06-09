from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from .base import BaseEmitter
from ir.models import IRRoot


def _now_iso() -> str:
    return f"{datetime.now(timezone.utc).isoformat()}"


def _safe_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class OpenCodeEmitter(BaseEmitter):
    """
    OpenCode-specific emitter — translates IRRoot to OpenCode format.
    Consumes IR only; does not read knowledge directly.
    """

    BASE_DIR = Path(".opencode")

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

        for agent_id, agent_ir in ir_dict.get("agents", {}).items():
            agent_file = agents_dir / f"{agent_id}.json"

            agent_config = {
                "name": agent_id,
                "displayName": agent_ir.get("display_name", agent_id),
                "description": agent_ir.get("description", ""),
                "role": agent_ir.get("role", ""),
                "version": "2.0",
                "knowledge": {
                    "domains": agent_ir.get("domains", []),
                    "skills": agent_ir.get("skills", []),
                    "workflows": agent_ir.get("workflows", []),
                    "blueprints": agent_ir.get("blueprints", [])
                },
                "permissions": {
                    "edit": agent_ir.get("permissions", {}).get("edit", True),
                    "shell": agent_ir.get("permissions", {}).get("shell", False),
                    "network": agent_ir.get("permissions", {}).get("network", False)
                },
                "behavior": agent_ir.get("behavior", {}),
                "authority": agent_ir.get("authority", {})
            }

            _safe_write(agent_file, str(__import__('json').dumps(agent_config, indent=2, ensure_ascii=False)))
            count += 1

        print(f"✔ AgentsEmitter: Generated {count} agents.")

    def _emit_config(self, ir_dict: Dict[str, Any], base: Path) -> None:
        config_path = base / "opencode.json"

        config = {
            "version": "2.0",
            "generated_at": _now_iso(),
            "agents": list(ir_dict.get("agents", {}).keys()),
            "knowledge": {
                "sources": ["skills/", "agents/"],
                "auto_load": True
            },
            "settings": {
                "context_awareness": True,
                "planner_integration": True
            }
        }

        _safe_write(config_path, str(__import__('json').dumps(config, indent=2, ensure_ascii=False)))
        print("✔ ConfigEmitter: Generated opencode.json")
