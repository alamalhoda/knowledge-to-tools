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


class KiloEmitter(BaseEmitter):
    """
    Kilo-specific emitter — translates IRRoot to Kilo format.
    Consumes IR only; does not read knowledge directly.
    """

    def emit(self, ir: IRRoot, output_dir: Optional[Path] = None) -> None:
        ir_dict = self._ir_to_dict(ir)
        base = self._resolve_output_dir(output_dir)
        self._emit_skills(ir_dict, base)
        self._emit_workflows(ir_dict, base)
        self._emit_architecture(ir_dict, base)
        self._emit_agents(ir_dict, base)
        print("🎉 KiloEmitter: All Kilo artifacts generated successfully!")

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

            skill_path = skills_dir / k["id"] / "SKILL.md"
            summary = k.get("content", {}).get("summary", "")
            raw = k.get("content", {}).get("raw", "")[:2000]

            content = (
                f"---\n"
                f"id: {k['id']}\n"
                f"kind: {kind}\n"
                f"domain: {k['domain']}\n"
                f"generated_at: {_now_iso()}\n"
                f"---\n\n"
                f"# {summary}\n\n"
                f"{raw}\n\n"
                f"---\n"
                f"**Domain**: {k['domain']}  \n"
                f"**Kind**: {kind}\n"
            )

            _safe_write(skill_path, content)
            count += 1

        print(f"✔ SkillsEmitter: Generated {count} skills.")

    def _emit_workflows(self, ir_dict: Dict[str, Any], base: Path) -> None:
        wf_dir = base / "workflows"
        count = 0

        knowledge = ir_dict.get("knowledge", [])
        if isinstance(knowledge, dict):
            knowledge = list(knowledge.values())

        for k in knowledge:
            if k.get("kind") != "workflow":
                continue

            path = wf_dir / k["id"] / "WORKFLOW.md"
            summary = k.get("content", {}).get("summary", "")
            raw = k.get("content", {}).get("raw", "")

            content = (
                f"---\n"
                f"id: {k['id']}\n"
                f"kind: workflow\n"
                f"domain: {k['domain']}\n"
                f"generated_at: {_now_iso()}\n"
                f"---\n\n"
                f"# Workflow: {summary}\n\n"
                f"{raw}\n"
            )

            _safe_write(path, content)
            count += 1

        print(f"✔ WorkflowEmitter: Generated {count} workflows.")

    def _emit_architecture(self, ir_dict: Dict[str, Any], base: Path) -> None:
        arch_dir = base / "architecture"
        count = 0

        knowledge = ir_dict.get("knowledge", [])
        if isinstance(knowledge, dict):
            knowledge = list(knowledge.values())

        for k in knowledge:
            if k.get("kind") != "architecture":
                continue

            path = arch_dir / k["id"] / "BLUEPRINT.md"
            summary = k.get("content", {}).get("summary", "")
            raw = k.get("content", {}).get("raw", "")

            content = (
                f"---\n"
                f"id: {k['id']}\n"
                f"kind: architecture\n"
                f"domain: {k['domain']}\n"
                f"generated_at: {_now_iso()}\n"
                f"---\n\n"
                f"# Architecture Blueprint: {summary}\n\n"
                f"{raw}\n"
            )

            _safe_write(path, content)
            count += 1

        print(f"✔ ArchitectureEmitter: Generated {count} architectures.")

    def _emit_agents(self, ir_dict: Dict[str, Any], base: Path) -> None:
        agents_dir = base / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        agents_data = ir_dict.get("agents", {})
        knowledge_list = ir_dict.get("knowledge", [])
        if isinstance(knowledge_list, dict):
            knowledge_list = list(knowledge_list.values())

        summary_sections: List[str] = [
            "# Aegis Agents",
            "",
            "_Generated automatically from Aegis Framework_",
            "",
        ]

        for agent_id, agent_ir in agents_data.items():
            agent_file = agents_dir / f"{agent_id}.md"

            matches = self._resolve_agent_skills(agent_ir, knowledge_list)

            agent_md = self._render_kilo_agent_md(agent_id, agent_ir, matches)
            _safe_write(agent_file, agent_md)

            summary_sections.append(
                self._render_summary_section(agent_id, agent_ir, matches)
            )

        _safe_write(Path(base / "AGENTS.md"), "\n".join(summary_sections))

        print(f"✔ AgentsEmitter: Generated {len(agents_data)} agents in .kilo/agents/ and AGENTS.md summary.")

    def _resolve_agent_skills(self, agent_ir: Dict[str, Any], knowledge: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        domains = set(agent_ir.get("domains", []))
        
        matched_skills = []
        matched_workflows = list(agent_ir.get("workflows", []))
        matched_architecture = list(agent_ir.get("blueprints", []))
        
        for k in knowledge:
            k_domain = k.get("domain", "")
            k_kind = k.get("kind", "")
            if k_domain not in domains and k_domain != "shared":
                continue
            
            if k_kind in {"rule", "principle", "reference", "policy", "skill"}:
                matched_skills.append(k["id"])
            elif k_kind == "workflow" and k["id"] not in matched_workflows:
                matched_workflows.append(k["id"])
            elif k_kind == "architecture" and k["id"] not in matched_architecture:
                matched_architecture.append(k["id"])
        
        return {
            "skills": matched_skills,
            "workflows": matched_workflows,
            "architecture": matched_architecture
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
