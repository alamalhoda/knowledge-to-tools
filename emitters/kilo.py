from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from .base import BaseEmitter
from .common import (
    PRINCIPLE_KIND,
    RULE_KINDS,
    agent_color,
    agent_mode,
    agent_permissions,
    agents_map,
    docs_of_kind,
    domain_of,
    knowledge_docs,
    merge_skill_sources,
    normalize_name,
    permission_action,
    render_agent_prompt,
    reset_output,
    render_knowledge_body,
    render_workflow_skill_body,
    safe_write,
    skill_description,
    summary_of,
    workflow_skill_description,
    yaml_quote,
)
from ir.models import IRRoot


class KiloEmitter(BaseEmitter):
    """
    Kilo artifacts per docs/tool-contracts/kilo.md

    rule/policy -> .kilo/rules/*.md + kilo.jsonc instructions
    architecture/workflow/skill/reference + IR workflows -> .kilo/skills/<id>/SKILL.md
    agents -> .kilo/agents/<id>.md
    AGENTS.md -> principles + agent index
    """

    BASE_DIR = Path("aegis_output/kilo")

    def emit(self, ir: IRRoot, output_dir: Optional[Path] = None) -> None:
        ir_dict = self._ir_to_dict(ir)
        base = self._resolve_output_dir(output_dir)
        reset_output(
            base,
            ["rules", "skills", "agents", "architecture", "workflows", "kilo.jsonc", "AGENTS.md"],
        )
        self._emit_rules(ir_dict, base)
        self._emit_skills(ir_dict, base)
        self._emit_agents(ir_dict, base)
        self._emit_config(base)
        self._emit_agents_md(ir_dict, base)
        print("KiloEmitter: Kilo artifacts generated.")

    def _emit_rules(self, ir_dict: Dict[str, Any], base: Path) -> None:
        rules_dir = base / "rules"
        count = 0
        for doc in docs_of_kind(knowledge_docs(ir_dict), RULE_KINDS):
            rule_id = normalize_name(doc.get("id", "rule"))
            body = render_knowledge_body(doc)
            safe_write(rules_dir / f"{rule_id}.md", body + "\n")
            count += 1
        print(f"  Rules: {count} markdown files")

    def _emit_skills(self, ir_dict: Dict[str, Any], base: Path) -> None:
        skills_dir = base / "skills"
        count = 0
        for name, source, origin in merge_skill_sources(ir_dict):
            if origin == "workflow":
                description = workflow_skill_description(source)
                body = render_workflow_skill_body(source)
                kind = "workflow"
                domain = source.get("domain", "shared")
            else:
                description = skill_description(source)
                body = render_knowledge_body(source)
                kind = source.get("kind", "skill")
                domain = domain_of(source)

            content = (
                f"---\n"
                f"name: {name}\n"
                f"description: {yaml_quote(description)}\n"
                f"metadata:\n"
                f"  aegis_kind: {yaml_quote(str(kind))}\n"
                f"  aegis_domain: {yaml_quote(str(domain))}\n"
                f"---\n\n"
                f"{body}\n"
            )
            safe_write(skills_dir / name / "SKILL.md", content)
            count += 1
        print(f"  Skills: {count} SKILL.md files")

    def _emit_agents(self, ir_dict: Dict[str, Any], base: Path) -> None:
        agents_dir = base / "agents"
        count = 0
        for agent_id, agent in agents_map(ir_dict).items():
            name = normalize_name(agent_id)
            permissions = agent_permissions(agent)
            description = yaml_quote(agent.get("description") or agent.get("role") or name)
            content = (
                f"---\n"
                f"description: {description}\n"
                f"mode: {agent_mode(agent)}\n"
                f"color: {yaml_quote(agent_color(name))}\n"
                f"permission:\n"
                f"  edit: {permission_action(bool(permissions.get('edit', True)))}\n"
                f"  bash: {permission_action(bool(permissions.get('shell', False)))}\n"
                f"  read: {permission_action(bool(permissions.get('read', True)))}\n"
                f"---\n\n"
                f"{render_agent_prompt(agent)}"
            )
            safe_write(agents_dir / f"{name}.md", content)
            count += 1
        print(f"  Agents: {count} agent files")

    def _emit_config(self, base: Path) -> None:
        config = {
            "instructions": [".kilo/rules/*.md"],
            "skills": {
                "paths": [".kilo/skills"],
            },
        }
        safe_write(base / "kilo.jsonc", json.dumps(config, indent=2) + "\n")
        print("  kilo.jsonc written")

    def _emit_agents_md(self, ir_dict: Dict[str, Any], base: Path) -> None:
        docs = knowledge_docs(ir_dict)
        principles = docs_of_kind(docs, {PRINCIPLE_KIND})
        architecture = docs_of_kind(docs, {"architecture"})

        lines = [
            "# Aegis Agents",
            "",
            "Generated from Aegis Framework. Copy this file to the project root.",
            "Rules: `.kilo/rules/` via `kilo.jsonc` instructions. Skills: `.kilo/skills/`.",
            "",
            "## Principles",
            "",
        ]
        if principles:
            for doc in principles:
                lines.append(f"- {summary_of(doc)}")
        else:
            lines.append("- None")

        lines.extend(["", "## Architecture pointers", ""])
        if architecture:
            for doc in architecture:
                lines.append(
                    f"- {domain_of(doc)}: {summary_of(doc)}. Details: skill `{normalize_name(doc.get('id', ''))}`"
                )
        else:
            lines.append("- None")

        lines.extend(["", "## Agents", ""])
        for agent_id, agent in agents_map(ir_dict).items():
            display = agent.get("display_name") or agent_id
            role = agent.get("role") or ""
            desc = agent.get("description") or ""
            lines.extend(
                [
                    f"## Agent: {display}",
                    "",
                    f"**Internal ID:** `{agent_id}`",
                    f"**Role:** {role}",
                    f"**Description:** {desc}",
                    "",
                    "### Architecture Blueprints",
                    ", ".join(agent.get("blueprints") or []) or "None",
                    "",
                    "### Operative Workflows",
                    ", ".join(agent.get("workflows") or []) or "None",
                    "",
                    "### Active Skills",
                    f"{len(agent.get('skills') or [])} items linked",
                    "",
                    "---",
                    "",
                ]
            )
        safe_write(base / "AGENTS.md", "\n".join(lines))
        print("  AGENTS.md written")
