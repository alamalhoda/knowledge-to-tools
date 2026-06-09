from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import json

from .base import BaseEmitter


def safe_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def now_iso() -> str:
    return f"{datetime.utcnow().isoformat()}Z"


class OpenCodeEmitter(BaseEmitter):
    """
    OpenCode-specific emitter — translates RuntimeIR to OpenCode format.
    Reads composed agents and generates .opencode/ structure.
    """

    BASE_DIR = Path(".opencode")

    def emit(self) -> None:
        self._emit_skills()
        self._emit_agents()
        self._emit_config()
        print("🎉 OpenCodeEmitter: All OpenCode artifacts generated successfully!")

    def _emit_skills(self) -> None:
        skills_dir = self.BASE_DIR / "skills"
        count = 0

        for k in self.ir.get("knowledge", {}).values():
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
generated_at: {now_iso()}
---

# {summary}

{raw}

<!-- OpenCode Skill Reference -->
<!-- Domain: {k['domain']} -->
"""

            safe_write(skill_path, content)
            count += 1

        print(f"✔ SkillsEmitter: Generated {count} skills.")

    def _emit_agents(self) -> None:
        agents_dir = self.BASE_DIR / "agents"
        count = 0

        for agent_id, agent_ir in self.ir.get("agents", {}).items():
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

            safe_write(agent_file, json.dumps(agent_config, indent=2, ensure_ascii=False))
            count += 1

        print(f"✔ AgentsEmitter: Generated {count} agents.")

    def _emit_config(self) -> None:
        config_path = self.BASE_DIR / "opencode.json"

        config = {
            "version": "2.0",
            "generated_at": now_iso(),
            "agents": list(self.ir.get("agents", {}).keys()),
            "knowledge": {
                "sources": ["skills/", "agents/"],
                "auto_load": True
            },
            "settings": {
                "context_awareness": True,
                "planner_integration": True
            }
        }

        safe_write(config_path, json.dumps(config, indent=2, ensure_ascii=False))
        print("✔ ConfigEmitter: Generated opencode.json")