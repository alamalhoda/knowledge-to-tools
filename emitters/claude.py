from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import BaseEmitter
from .common import (
    PRINCIPLE_KIND,
    RULE_KINDS,
    agent_permissions,
    agents_map,
    docs_of_kind,
    domain_of,
    file_patterns,
    high_priority_docs,
    kind_of,
    knowledge_docs,
    merge_skill_sources,
    normalize_name,
    render_agent_prompt,
    render_knowledge_body,
    render_workflow_skill_body,
    reset_output,
    safe_write,
    skill_description,
    summary_of,
    truncate,
    workflow_skill_description,
    yaml_block_list,
    yaml_quote,
)
from ir.models import IRRoot


def _model_for_authority(level: str) -> str:
    mapping = {
        "junior": "haiku",
        "mid": "sonnet",
        "senior": "opus",
        "lead": "opus",
        "principal": "opus",
    }
    return mapping.get(str(level).lower(), "inherit")


def _tools_for_permissions(permissions: Dict[str, Any]) -> str:
    tools = ["Read", "Grep", "Glob"]
    if permissions.get("shell"):
        tools.append("Bash")
    if permissions.get("edit", True):
        tools.extend(["Write", "Edit"])
    if permissions.get("network"):
        tools.extend(["WebFetch", "WebSearch"])
    return ", ".join(tools)


class ClaudeEmitter(BaseEmitter):
    """
    Claude Code artifacts per docs/tool-contracts/claude.md

    rule/policy -> .claude/rules/*.md (paths-scoped when applies_to exists)
    architecture/workflow/skill/reference + IR workflows -> .claude/skills/<id>/SKILL.md
    agents -> .claude/agents/<id>.md
    CLAUDE.md -> short always-on pointers
    """

    BASE_DIR = Path("aegis_output/claude")

    def emit(self, ir: IRRoot, output_dir: Optional[Path] = None) -> None:
        ir_dict = self._ir_to_dict(ir)
        base = self._resolve_output_dir(output_dir)
        reset_output(base, ["rules", "skills", "agents", "CLAUDE.md"])
        self._emit_rules(ir_dict, base)
        self._emit_skills(ir_dict, base)
        self._emit_agents(ir_dict, base)
        self._emit_claude_md(ir_dict, base)
        print("ClaudeEmitter: Claude Code artifacts generated.")

    def _emit_rules(self, ir_dict: Dict[str, Any], base: Path) -> None:
        rules_dir = base / "rules"
        count = 0
        for doc in docs_of_kind(knowledge_docs(ir_dict), RULE_KINDS):
            rule_id = normalize_name(doc.get("id", "rule"))
            patterns = file_patterns(doc)
            parts: List[str] = []
            if patterns:
                parts.append("---")
                parts.append(yaml_block_list("paths", patterns).rstrip())
                parts.append("---")
                parts.append("")
            parts.append(render_knowledge_body(doc))
            parts.append("")
            safe_write(rules_dir / f"{rule_id}.md", "\n".join(parts))
            count += 1
        print(f"  Rules: {count} files in rules/")

    def _emit_skills(self, ir_dict: Dict[str, Any], base: Path) -> None:
        skills_dir = base / "skills"
        count = 0
        for name, source, origin in merge_skill_sources(ir_dict):
            if origin == "workflow":
                description = workflow_skill_description(source, limit=1536)
                body = render_workflow_skill_body(source)
                paths: List[str] = []
                kind = "workflow"
                disable_model = False
                user_invocable = True
            else:
                description = skill_description(source, limit=1536)
                body = render_knowledge_body(source)
                paths = file_patterns(source)
                kind = kind_of(source)
                disable_model = kind == "workflow"
                user_invocable = kind != "reference"

            front = [
                "---",
                f"name: {name}",
                f"description: {yaml_quote(description)}",
            ]
            if paths:
                front.append(yaml_block_list("paths", paths).rstrip())
            if disable_model:
                front.append("disable-model-invocation: true")
            if not user_invocable:
                front.append("user-invocable: false")
            front.extend(["---", "", body, ""])
            safe_write(skills_dir / name / "SKILL.md", "\n".join(front))
            count += 1
        print(f"  Skills: {count} SKILL.md files")

    def _emit_agents(self, ir_dict: Dict[str, Any], base: Path) -> None:
        agents_dir = base / "agents"
        count = 0
        for agent_id, agent in agents_map(ir_dict).items():
            name = normalize_name(agent_id)
            permissions = agent_permissions(agent)
            authority = agent.get("authority") or {}
            description = yaml_quote(
                truncate(agent.get("description") or agent.get("role") or name, 1536)
            )
            tools = _tools_for_permissions(permissions)
            model = _model_for_authority(authority.get("level", "mid"))
            content = (
                f"---\n"
                f"name: {name}\n"
                f"description: {description}\n"
                f"tools: {tools}\n"
                f"model: {model}\n"
                f"---\n\n"
                f"{render_agent_prompt(agent)}"
            )
            safe_write(agents_dir / f"{name}.md", content)
            count += 1
        print(f"  Agents: {count} subagent files")

    def _emit_claude_md(self, ir_dict: Dict[str, Any], base: Path) -> None:
        docs = knowledge_docs(ir_dict)
        principles = docs_of_kind(docs, {PRINCIPLE_KIND})
        policies = high_priority_docs(docs, {"policy"}) or docs_of_kind(docs, {"policy"})
        architecture = docs_of_kind(docs, {"architecture"})

        lines = [
            "# Aegis Project",
            "",
            "Always-on conventions for Claude Code. Path-scoped rules live in `.claude/rules/`.",
            "On-demand procedures live in `.claude/skills/`. Roles live in `.claude/agents/`.",
            "",
            "@AGENTS.md",
            "",
            "## Always",
            "",
        ]
        always_items = principles + [p for p in policies if p not in principles]
        if always_items:
            for doc in always_items:
                lines.append(f"- {summary_of(doc)}")
        else:
            lines.append("- Follow project engineering principles.")

        lines.extend(["", "## Architecture pointers", ""])
        if architecture:
            for doc in architecture:
                lines.append(
                    f"- {domain_of(doc)}: {summary_of(doc)}. Details: skill `{normalize_name(doc.get('id', ''))}`"
                )
        else:
            lines.append("- None")

        lines.extend(["", "## Agents", ""])
        lines.append(
            "Delegate implementation to `backend` / `frontend`. "
            "Review via `reviewer`. Architecture via `architect`."
        )
        for agent_id, agent in agents_map(ir_dict).items():
            display = agent.get("display_name") or agent_id
            lines.append(f"- `{agent_id}` ({display})")
        lines.append("")
        safe_write(base / "CLAUDE.md", "\n".join(lines))
        print("  CLAUDE.md written")
