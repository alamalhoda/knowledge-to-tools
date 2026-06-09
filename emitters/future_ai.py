from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from ir.models import IRRoot


def _now_iso() -> str:
    return f"{datetime.now(timezone.utc).isoformat()}"


def _safe_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class FutureAIEmitter:
    """
    Hypothetical 'future_ai' emitter — validates tool independence.

    This emitter consumes IRRoot only and produces output for a
    hypothetical future AI tool without modifying IR or compiler.
    """

    BASE_DIR = Path(".future_ai")

    def emit(self, ir: IRRoot, output_dir: Optional[Path] = None) -> None:
        ir_dict = ir.to_dict()
        base = self._resolve_output_dir(output_dir)
        self._emit_agents(ir_dict, base)
        self._emit_skills(ir_dict, base)
        self._emit_config(ir_dict, base)
        print("🎉 FutureAIEmitter: All future_ai artifacts generated successfully!")

    def _resolve_output_dir(self, output_dir: Optional[Path] = None) -> Path:
        if output_dir is not None:
            return output_dir
        return self.BASE_DIR

    def _emit_agents(self, ir_dict: Dict[str, Any], base: Path) -> None:
        agents_dir = base / "agents"
        count = 0

        for agent_id, agent_ir in ir_dict.get("agents", {}).items():
            agent_file = agents_dir / f"{agent_id}.md"

            content = f"""---
id: {agent_id}
name: {agent_ir.get('name', agent_id)}
displayName: {agent_ir.get('display_name', agent_id)}
description: {agent_ir.get('description', '')}
role: {agent_ir.get('role', '')}
generated_at: {_now_iso()}
---

# {agent_ir.get('display_name', agent_id)}

{agent_ir.get('description', '')}

## Domains
{', '.join(agent_ir.get('domains', []))}

## Skills
{', '.join(agent_ir.get('skills', []))}

## Workflows
{', '.join(agent_ir.get('workflows', []))}

## Blueprints
{', '.join(agent_ir.get('blueprints', []))}

## Permissions
- Shell: {agent_ir.get('permissions', {}).get('shell', False)}
- Edit: {agent_ir.get('permissions', {}).get('edit', True)}
- Network: {agent_ir.get('permissions', {}).get('network', False)}

## Behavior
- Planning: {agent_ir.get('behavior', {}).get('planning', 'optional')}
- Testing: {agent_ir.get('behavior', {}).get('testing', 'optional')}
- Review: {agent_ir.get('behavior', {}).get('review_style', 'balanced')}
"""

            _safe_write(agent_file, content)
            count += 1

        print(f"✔ FutureAIEmitter: Generated {count} agents.")

    def _emit_skills(self, ir_dict: Dict[str, Any], base: Path) -> None:
        skills_dir = base / "skills"
        count = 0

        knowledge = ir_dict.get("knowledge", [])
        if isinstance(knowledge, dict):
            knowledge = list(knowledge.values())

        for k in knowledge:
            kind = k.get("kind")
            if kind not in {"rule", "principle", "reference", "policy", "skill", "workflow", "architecture"}:
                continue

            skill_path = skills_dir / f"{k['id']}.md"
            summary = k.get("content", {}).get("summary", "")
            raw = k.get("content", {}).get("raw", "")[:1500]

            content = (
                f"---\n"
                f"id: {k['id']}\n"
                f"kind: {kind}\n"
                f"domain: {k['domain']}\n"
                f"category: {k.get('category', '')}\n"
                f"generated_at: {_now_iso()}\n"
                f"---\n\n"
                f"# {summary}\n\n"
                f"{raw}\n"
            )

            _safe_write(skill_path, content)
            count += 1

        print(f"✔ FutureAIEmitter: Generated {count} skills.")

    def _emit_config(self, ir_dict: Dict[str, Any], base: Path) -> None:
        config_path = base / "future_ai.json"

        config = {
            "version": "2.0",
            "generated_at": _now_iso(),
            "agents": list(ir_dict.get("agents", {}).keys()),
            "knowledge_count": len(ir_dict.get("knowledge", [])),
            "workflow_count": len(ir_dict.get("workflows", [])),
            "capability_count": len(ir_dict.get("capabilities", [])),
            "contract_count": len(ir_dict.get("contracts", [])),
            "settings": {
                "context_awareness": True,
                "knowledge_integration": True,
                "tool_agnostic": True,
            },
        }

        _safe_write(config_path, str(__import__('json').dumps(config, indent=2, ensure_ascii=False)))
        print("✔ FutureAIEmitter: Generated future_ai.json")
