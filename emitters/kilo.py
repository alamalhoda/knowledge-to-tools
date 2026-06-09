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


class KiloEmitter(BaseEmitter):
    """
    Kilo-specific emitter — translates RuntimeIR to Kilo format.
    Reads composed agents and generates .kilo/ structure.
    """

    BASE_DIR = Path(".kilo")

    def _get_knowledge_list(self) -> List[Dict[str, Any]]:
        knowledge = self.ir.get("knowledge", {})
        if isinstance(knowledge, dict):
            return list(knowledge.values())
        return knowledge

    def emit(self) -> None:
        self._emit_skills()
        self._emit_workflows()
        self._emit_architecture()
        self._emit_agents()
        print("🎉 KiloEmitter: All Kilo artifacts generated successfully!")

    def _emit_skills(self) -> None:
        skills_dir = self.BASE_DIR / "skills"
        count = 0

        for k in self._get_knowledge_list():
            kind = k.get("kind")
            if kind not in {"rule", "principle", "reference", "policy", "skill"}:
                continue

            skill_path = skills_dir / k["id"] / "SKILL.md"
            summary = k["content"]["summary"]
            raw = k["content"]["raw"][:2000]

            content = (
                f"---\n"
                f"id: {k['id']}\n"
                f"kind: {kind}\n"
                f"domain: {k['domain']}\n"
                f"generated_at: {now_iso()}\n"
                f"---\n\n"
                f"# {summary}\n\n"
                f"{raw}\n\n"
                f"---\n"
                f"**Domain**: {k['domain']}  \n"
                f"**Kind**: {kind}\n"
            )

            safe_write(skill_path, content)
            count += 1

        print(f"✔ SkillsEmitter: Generated {count} skills.")

    def _emit_workflows(self) -> None:
        wf_dir = self.BASE_DIR / "workflows"
        count = 0

        for k in self._get_knowledge_list():
            if k.get("kind") != "workflow":
                continue

            path = wf_dir / k["id"] / "WORKFLOW.md"
            summary = k["content"]["summary"]
            raw = k["content"]["raw"]

            content = (
                f"---\n"
                f"id: {k['id']}\n"
                f"kind: workflow\n"
                f"domain: {k['domain']}\n"
                f"generated_at: {now_iso()}\n"
                f"---\n\n"
                f"# Workflow: {summary}\n\n"
                f"{raw}\n"
            )

            safe_write(path, content)
            count += 1

        print(f"✔ WorkflowEmitter: Generated {count} workflows.")

    def _emit_architecture(self) -> None:
        arch_dir = self.BASE_DIR / "architecture"
        count = 0

        for k in self._get_knowledge_list():
            if k.get("kind") != "architecture":
                continue

            path = arch_dir / k["id"] / "BLUEPRINT.md"
            summary = k["content"]["summary"]
            raw = k["content"]["raw"]

            content = (
                f"---\n"
                f"id: {k['id']}\n"
                f"kind: architecture\n"
                f"domain: {k['domain']}\n"
                f"generated_at: {now_iso()}\n"
                f"---\n\n"
                f"# Architecture Blueprint: {summary}\n\n"
                f"{raw}\n"
            )

            safe_write(path, content)
            count += 1

        print(f"✔ ArchitectureEmitter: Generated {count} architectures.")

    def _emit_agents(self) -> None:
        agents_dir = self.BASE_DIR / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        agents_data = self.ir.get("agents", {})

        summary_sections: List[str] = [
            "# Aegis Agents",
            "",
            "_Generated automatically from Aegis Framework_",
            "",
        ]

        for agent_id, agent_ir in agents_data.items():
            agent_file = agents_dir / f"{agent_id}.md"

            matches = self._resolve_agent_skills(agent_ir)

            agent_md = self._render_kilo_agent_md(agent_id, agent_ir, matches)
            safe_write(agent_file, agent_md)

            summary_sections.append(
                self._render_summary_section(agent_id, agent_ir, matches)
            )

        safe_write(Path(self.BASE_DIR / "AGENTS.md"), "\n".join(summary_sections))

        print(f"✔ AgentsEmitter: Generated {len(agents_data)} agents in .kilo/agents/ and AGENTS.md summary.")

    def _resolve_agent_skills(self, agent_ir: Dict[str, Any]) -> Dict[str, List[str]]:
        return {
            "skills": agent_ir.get("skills", []),
            "workflows": agent_ir.get("workflows", []),
            "architecture": agent_ir.get("blueprints", [])
        }

    def _render_kilo_agent_md(self, agent_id: str, meta: Dict[str, Any], matches: Dict[str, List[str]]) -> str:
        display = meta.get("display_name", agent_id)
        role = meta.get("role", "")
        desc = meta.get("description", "")

        permissions = meta.get("permissions", {})
        bash_perm = "allow" if permissions.get("shell") else "deny"
        edit_perm = "allow" if permissions.get("edit", True) else "deny"

        frontmatter = f"""---
name: {agent_id}
display_name: {display}
description: {desc}
mode: primary
color: "#3B82F6"

model: gpt-4o
temperature: 0.2

permission:
  edit: {edit_perm}
  bash: {bash_perm}
  read: allow

tools:
  - edit
  - read
  - bash

context:
  - .kilo/skills
  - .kilo/workflows
  - .kilo/architecture

steps: 30
---
"""

        arch = "\n".join(f"- {x}" for x in matches["architecture"]) or "- None"
        wf = "\n".join(f"- {x}" for x in matches["workflows"]) or "- None"
        skills = "\n".join(f"- {x}" for x in matches["skills"]) or "- None"

        body = f"""You are **{display}** — {role}

{desc}

## Knowledge Bindings (Aegis)

### Architecture
{arch}

### Workflows
{wf}

### Skills / Rules
{skills}

## Core Behavior

Planning: {meta.get("behavior", {}).get("planning", "preferred")}
Testing: {meta.get("behavior", {}).get("testing", "preferred")}
Review Style: {meta.get("behavior", {}).get("review_style", "balanced")}

Follow Aegis engineering principles strictly.
Always consult the linked knowledge when making decisions.
"""

        return frontmatter + body

    def _render_summary_section(self, agent_id: str, meta: Dict[str, Any], matches: Dict[str, List[str]]) -> str:
        display = meta.get("display_name", agent_id)
        role = meta.get("role", "")
        desc = meta.get("description", "")

        arch = ", ".join(matches["architecture"]) or "None"
        wf = ", ".join(matches["workflows"]) or "None"
        skills_count = len(matches["skills"])

        return f"""
## 🤖 Agent: {display}

**Internal ID:** `{agent_id}`  
**Role:** {role}  
**Description:** {desc}

### Architecture Blueprints
{arch}

### Operative Workflows
{wf}

### Active Skills / Rules
{skills_count} items linked

---
"""