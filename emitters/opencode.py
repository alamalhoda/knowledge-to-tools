from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from .base import BaseEmitter
from .common import (
    PRINCIPLE_KIND,
    RULE_KINDS,
    agent_mode,
    agent_permissions,
    agents_map,
    docs_of_kind,
    domain_of,
    kind_of,
    knowledge_docs,
    merge_skill_sources,
    normalize_name,
    permission_action,
    render_agent_prompt,
    render_knowledge_body,
    render_workflow_skill_body,
    reset_output,
    safe_write,
    skill_description,
    summary_of,
    workflow_skill_description,
    yaml_quote,
)
from ir.models import IRRoot


class OpenCodeEmitter(BaseEmitter):
    """
    OpenCode artifacts per docs/tool-contracts/opencode.md

    rule/policy -> .opencode/instructions/*.md + opencode.json instructions
    architecture/workflow/skill/reference + IR workflows -> .opencode/skills/<id>/SKILL.md
    knowledge workflows also -> .opencode/commands/<id>.md
    agents -> .opencode/agents/<id>.md
    AGENTS.md -> principles + pointers
    """

    BASE_DIR = Path("aegis_output/opencode")

    def emit(self, ir: IRRoot, output_dir: Optional[Path] = None) -> None:
        ir_dict = self._ir_to_dict(ir)
        base = self._resolve_output_dir(output_dir)
        reset_output(
            base,
            ["instructions", "skills", "commands", "agents", "opencode.json", "AGENTS.md"],
        )
        self._emit_instructions(ir_dict, base)
        self._emit_skills(ir_dict, base)
        self._emit_commands(ir_dict, base)
        self._emit_agents(ir_dict, base)
        self._emit_config(base)
        self._emit_agents_md(ir_dict, base)
        print("OpenCodeEmitter: OpenCode artifacts generated.")

    def _emit_instructions(self, ir_dict: Dict[str, Any], base: Path) -> None:
        instructions_dir = base / "instructions"
        count = 0
        for doc in docs_of_kind(knowledge_docs(ir_dict), RULE_KINDS):
            name = normalize_name(doc.get("id", "rule"))
            safe_write(instructions_dir / f"{name}.md", render_knowledge_body(doc) + "\n")
            count += 1
        print(f"  Instructions: {count} files")

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
                kind = kind_of(source) or "skill"
                domain = domain_of(source)

            content = (
                f"---\n"
                f"name: {name}\n"
                f"description: {yaml_quote(description)}\n"
                f"compatibility: opencode\n"
                f"metadata:\n"
                f"  aegis_kind: {yaml_quote(str(kind))}\n"
                f"  aegis_domain: {yaml_quote(str(domain))}\n"
                f"---\n\n"
                f"{body}\n"
            )
            safe_write(skills_dir / name / "SKILL.md", content)
            count += 1
        print(f"  Skills: {count} SKILL.md files")

    def _emit_commands(self, ir_dict: Dict[str, Any], base: Path) -> None:
        commands_dir = base / "commands"
        count = 0
        for doc in docs_of_kind(knowledge_docs(ir_dict), {"workflow"}):
            name = normalize_name(doc.get("id", "workflow"))
            summary = summary_of(doc)
            body = render_knowledge_body(doc)
            content = (
                f"---\n"
                f"description: {yaml_quote(summary or name)}\n"
                f"---\n\n"
                f"{body}\n"
            )
            safe_write(commands_dir / f"{name}.md", content)
            count += 1
        print(f"  Commands: {count} command files")

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
                f"permission:\n"
                f"  edit: {permission_action(bool(permissions.get('edit', True)))}\n"
                f"  bash: {permission_action(bool(permissions.get('shell', False)))}\n"
                f"  webfetch: {permission_action(bool(permissions.get('network', False)))}\n"
                f"  websearch: {permission_action(bool(permissions.get('network', False)))}\n"
                f"---\n\n"
                f"{render_agent_prompt(agent)}"
            )
            safe_write(agents_dir / f"{name}.md", content)
            count += 1
        print(f"  Agents: {count} markdown agents")

    def _emit_config(self, base: Path) -> None:
        config = {
            "$schema": "https://opencode.ai/config.json",
            "instructions": [".opencode/instructions/*.md"],
            "permission": {
                "skill": {
                    "*": "allow",
                }
            },
        }
        safe_write(base / "opencode.json", json.dumps(config, indent=2, ensure_ascii=False) + "\n")
        print("  opencode.json written")

    def _emit_agents_md(self, ir_dict: Dict[str, Any], base: Path) -> None:
        docs = knowledge_docs(ir_dict)
        principles = docs_of_kind(docs, {PRINCIPLE_KIND})
        policies = docs_of_kind(docs, {"policy"})
        architecture = docs_of_kind(docs, {"architecture"})

        lines = [
            "# Aegis Project Instructions",
            "",
            "Stable rules are also loaded from `.opencode/instructions/` via `opencode.json`.",
            "On-demand knowledge lives in `.opencode/skills/`. Roles live in `.opencode/agents/`.",
            "",
            "## Principles",
            "",
        ]
        if principles:
            for doc in principles:
                lines.append(f"- {summary_of(doc)}")
        else:
            lines.append("- None")

        lines.extend(["", "## Policies", ""])
        if policies:
            for doc in policies:
                lines.append(f"- {summary_of(doc)}")
        else:
            lines.append("- None")

        lines.extend(["", "## Architecture pointers", ""])
        if architecture:
            for doc in architecture:
                lines.append(
                    f"- {domain_of(doc)}: {summary_of(doc)}. See skill `{normalize_name(doc.get('id', ''))}`."
                )
        else:
            lines.append("- None")

        lines.extend(["", "## Agents", ""])
        lines.append("Use `@backend`, `@frontend`, `@architect`, `@reviewer` for specialized work.")
        for agent_id, agent in agents_map(ir_dict).items():
            display = agent.get("display_name") or agent_id
            desc = agent.get("description") or ""
            lines.append(f"- `{agent_id}` ({display}): {desc}")
        lines.append("")
        safe_write(base / "AGENTS.md", "\n".join(lines))
        print("  AGENTS.md written")
