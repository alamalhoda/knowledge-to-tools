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


class CursorEmitter(BaseEmitter):
    """
    Cursor-specific emitter — translates RuntimeIR to Cursor format.
    Reads composed agents and generates .cursor/ structure.
    """

    BASE_DIR = Path(".cursor")

    def _get_knowledge_list(self) -> List[Dict[str, Any]]:
        knowledge = self.ir.get("knowledge", {})
        if isinstance(knowledge, dict):
            return list(knowledge.values())
        return knowledge

    def emit(self) -> None:
        self._emit_rules()
        self._emit_agents()
        print("🎉 CursorEmitter: All Cursor artifacts generated successfully!")

    def _emit_rules(self) -> None:
        rules_dir = self.BASE_DIR / "rules"
        count = 0

        for doc in self._get_knowledge_list():
            kind = doc.get("kind")
            if kind not in {"rule", "principle", "reference", "policy"}:
                continue

            rule_path = rules_dir / f"{doc['id']}.mdc"
            raw = doc.get("content", {}).get("raw", "")[:3000]

            content = f"""---
title: {doc['content'].get('summary', '')}
description: {doc.get('domain', '')} - {kind}
globs:
{self._format_globs(doc.get('activation', {}).get('file_patterns', []))}
alwaysApply: false
---

{raw}

<!-- Cursor Rule Reference -->
<!-- Generated: {now_iso()} -->
<!-- Domain: {doc['domain']} -->
"""

            safe_write(rule_path, content)
            count += 1

        print(f"✔ RulesEmitter: Generated {count} rules.")

    def _format_globs(self, patterns: List[str]) -> str:
        return "\n".join(f"  - {p}" for p in patterns[:10]) if patterns else ""

    def _emit_agents(self) -> None:
        agents_dir = self.BASE_DIR / "agents"
        count = 0

        for agent_id, agent_ir in self.ir.get("agents", {}).items():
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

            safe_write(agent_file, content)
            count += 1

        print(f"✔ AgentsEmitter: Generated {count} agent definitions.")