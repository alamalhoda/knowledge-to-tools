from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import BaseEmitter
from .common import (
    PRINCIPLE_KIND,
    RULE_KINDS,
    agent_readonly,
    agents_map,
    cursor_always_apply,
    docs_of_kind,
    domain_of,
    file_patterns,
    high_priority_docs,
    kind_of,
    knowledge_docs,
    merge_skill_sources,
    normalize_name,
    reset_output,
    render_agent_prompt,
    render_knowledge_body,
    render_workflow_skill_body,
    safe_write,
    skill_description,
    summary_of,
    workflow_skill_description,
    yaml_block_list,
    yaml_quote,
)
from ir.models import IRRoot


class CursorEmitter(BaseEmitter):
    """
    Cursor artifacts per docs/tool-contracts/cursor.md

    rule/policy/principle -> .cursor/rules/*.mdc
    architecture/workflow/skill/reference + IR workflows -> .cursor/skills/<id>/SKILL.md
    agents -> .cursor/agents/<id>.md
    AGENTS.md -> high-priority principles + agent index
    """

    BASE_DIR = Path("aegis_output/cursor")

    def emit(self, ir: IRRoot, output_dir: Optional[Path] = None) -> None:
        ir_dict = self._ir_to_dict(ir)
        base = self._resolve_output_dir(output_dir)
        reset_output(base, ["rules", "skills", "agents", "AGENTS.md"])
        self._emit_rules(ir_dict, base)
        self._emit_skills(ir_dict, base)
        self._emit_agents(ir_dict, base)
        self._emit_agents_md(ir_dict, base)
        print("CursorEmitter: Cursor artifacts generated.")

    def _emit_rules(self, ir_dict: Dict[str, Any], base: Path) -> None:
        rules_dir = base / "rules"
        count = 0
        for doc in docs_of_kind(knowledge_docs(ir_dict), RULE_KINDS | {PRINCIPLE_KIND}):
            rule_id = normalize_name(doc.get("id", "rule"))
            safe_write(rules_dir / f"{rule_id}.mdc", self._render_rule(doc))
            count += 1
        print(f"  Rules: {count} .mdc files")

    def _render_rule(self, doc: Dict[str, Any]) -> str:
        patterns = file_patterns(doc)
        always_apply = cursor_always_apply(doc)
        description = skill_description(doc, limit=500)
        lines = ["---", f"description: {yaml_quote(description)}"]
        if always_apply:
            lines.append("alwaysApply: true")
        else:
            lines.append("alwaysApply: false")
            if patterns:
                lines.append(yaml_block_list("globs", patterns).rstrip())
        lines.extend(["---", "", render_knowledge_body(doc), ""])
        return "\n".join(lines)

    def _emit_skills(self, ir_dict: Dict[str, Any], base: Path) -> None:
        skills_dir = base / "skills"
        count = 0
        for name, source, origin in merge_skill_sources(ir_dict):
            if origin == "workflow":
                description = workflow_skill_description(source)
                body = render_workflow_skill_body(source)
                paths: List[str] = []
                disable_model = False
            else:
                description = skill_description(source)
                body = render_knowledge_body(source)
                paths = file_patterns(source)
                disable_model = kind_of(source) == "workflow"

            front = ["---", f"name: {name}", f"description: {yaml_quote(description)}"]
            if paths:
                front.append(yaml_block_list("paths", paths).rstrip())
            if disable_model:
                front.append("disable-model-invocation: true")
            front.extend(["---", "", body, ""])
            safe_write(skills_dir / name / "SKILL.md", "\n".join(front))
            count += 1
        print(f"  Skills: {count} SKILL.md files")

    def _emit_agents(self, ir_dict: Dict[str, Any], base: Path) -> None:
        agents_dir = base / "agents"
        count = 0
        for agent_id, agent in agents_map(ir_dict).items():
            name = normalize_name(agent_id)
            readonly = "true" if agent_readonly(agent) else "false"
            description = yaml_quote(agent.get("description") or agent.get("role") or name)
            content = (
                f"---\n"
                f"name: {name}\n"
                f"description: {description}\n"
                f"model: inherit\n"
                f"readonly: {readonly}\n"
                f"---\n\n"
                f"{render_agent_prompt(agent)}"
            )
            safe_write(agents_dir / f"{name}.md", content)
            count += 1
        print(f"  Agents: {count} subagent files")

    def _emit_agents_md(self, ir_dict: Dict[str, Any], base: Path) -> None:
        docs = knowledge_docs(ir_dict)
        principles = high_priority_docs(docs, {PRINCIPLE_KIND}) or docs_of_kind(docs, {PRINCIPLE_KIND})
        architecture = docs_of_kind(docs, {"architecture"})

        lines = [
            "# Aegis Project Instructions",
            "",
            "Project rules live in `.cursor/rules/`. On-demand knowledge lives in `.cursor/skills/`.",
            "Specialized roles live in `.cursor/agents/`.",
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
            desc = agent.get("description") or agent.get("role") or ""
            lines.append(f"- `{agent_id}` ({display}): {desc}")
        lines.append("")
        safe_write(base / "AGENTS.md", "\n".join(lines))
        print("  AGENTS.md written")
