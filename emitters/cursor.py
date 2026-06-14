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


class CursorEmitter(BaseEmitter):
    """
    Cursor-specific emitter — translates IRRoot to Cursor format.
    Consumes IR only; does not read knowledge directly.
    """

    BASE_DIR = Path("aegis_output/cursor")

    def emit(self, ir: IRRoot, output_dir: Optional[Path] = None) -> None:
        ir_dict = self._ir_to_dict(ir)
        base = self._resolve_output_dir(output_dir)
        rules_dir = base / "rules"
        agents_dir = base / "agents"
        count_rules = 0
        count_agents = 0

        knowledge = ir_dict.get("knowledge", [])
        if isinstance(knowledge, dict):
            knowledge = list(knowledge.values())

        for doc in knowledge:
            kind = doc.get("kind")
            if kind not in {"rule", "principle", "reference", "policy"}:
                continue

            rule_path = rules_dir / f"{doc['id']}.mdc"
            raw = doc.get("content", {}).get("raw", "")

            content = f"""---
title: {doc.get('content', {}).get('summary', '')}
description: {doc.get('domain', '')} - {kind}
globs:
{self._format_globs(doc.get('activation', {}).get('file_patterns', []))}
alwaysApply: false
---

{raw}

<!-- Cursor Rule Reference -->
<!-- Generated: {_now_iso()} -->
<!-- Domain: {doc.get('domain', '')} -->
"""

            _safe_write(rule_path, content)
            count_rules += 1

        print(f"✔ RulesEmitter: Generated {count_rules} rules.")

        for agent_id, agent_ir in ir_dict.get("agents", {}).items():
            agent_file = agents_dir / f"{agent_id}.md"

            content = f"""---
name: {agent_id}
displayName: {agent_ir.get('display_name', agent_id)}
description: {agent_ir.get('description', '')}
version: 2.0
---

# {agent_ir.get('display_name', agent_id)}

{agent_ir.get('role', '')}

## Knowledge

**Domains:** {', '.join(agent_ir.get('domains', []))}

**Skills:** {len(agent_ir.get('skills', []))} items

**Workflows:** {', '.join(agent_ir.get('workflows', []))}

## Behavior

- Planning: {agent_ir.get('behavior', {}).get('planning', 'preferred')}
- Testing: {agent_ir.get('behavior', {}).get('testing', 'preferred')}
- Review: {agent_ir.get('behavior', {}).get('review_style', 'balanced')}
"""

            _safe_write(agent_file, content)
            count_agents += 1

        print(f"✔ AgentsEmitter: Generated {count_agents} agent definitions.")
        print("🎉 CursorEmitter: All Cursor artifacts generated successfully!")

    def _format_globs(self, patterns: List[str]) -> str:
        return "\n".join(f"  - {p}" for p in patterns[:10]) if patterns else ""
