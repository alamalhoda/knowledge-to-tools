from __future__ import annotations

import re
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


def _normalize_name(name: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    normalized = re.sub(r"-+", "-", normalized)
    return normalized[:64] or "skill"


def _truncate_description(description: str, limit: int = 1536) -> str:
    description = str(description).strip()
    if len(description) <= limit:
        return description
    return description[: limit - 3].rstrip() + "..."


def _strip_legacy_frontmatter(raw: str) -> str:
    return re.sub(r"\A---\s*\n.*?\n---\s*\n", "", raw or "", flags=re.DOTALL).lstrip()


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


def _skill_description(k: Dict[str, Any]) -> str:
    content = k.get("content", {})
    description = (
        content.get("description")
        or content.get("summary")
        or k.get("id", "skill").replace("-", " ").title()
    )
    return _truncate_description(description or "Claude Code skill")


class ClaudeEmitter(BaseEmitter):
    """
    Claude Code-specific emitter — translates IRRoot to Claude Code format.

    Consumes IR only; does not read knowledge directly.

    Maps:
      - agents   -> .claude/agents/<name>.md    (subagents)
      - knowledge (rule/principle/reference/policy/skill)
                -> .claude/skills/<name>/SKILL.md (skills)
      - base knowledge -> CLAUDE.md               (project memory)
    """

    BASE_DIR = Path("aegis_output/claude")

    def emit(self, ir: IRRoot, output_dir: Optional[Path] = None) -> None:
        ir_dict = self._ir_to_dict(ir)
        base = self._resolve_output_dir(output_dir)
        self._emit_agents(ir_dict, base)
        self._emit_skills(ir_dict, base)
        self._emit_claude_md(ir_dict, base)
        print("🎉 ClaudeEmitter: All Claude Code artifacts generated successfully!")

    def _emit_agents(self, ir_dict: Dict[str, Any], base: Path) -> None:
        agents_dir = base / "agents"
        count = 0

        for agent_id, agent_ir in ir_dict.get("agents", {}).items():
            agent_file = agents_dir / f"{_normalize_name(agent_id)}.md"
            content = self._render_agent_md(agent_id, agent_ir)
            _safe_write(agent_file, content)
            count += 1

        print(f"✔ AgentsEmitter: Generated {count} agents in .claude/agents/.")

    def _render_agent_md(self, agent_id: str, meta: Dict[str, Any]) -> str:
        name = _normalize_name(agent_id)
        display = meta.get("display_name", agent_id)
        description = _truncate_description(meta.get("description", ""))
        permissions = meta.get("permissions", {})
        authority = meta.get("authority", {})
        behavior = meta.get("behavior", {})

        model = _model_for_authority(authority.get("level", "mid"))
        tools = _tools_for_permissions(permissions)

        frontmatter = (
            f"---\n"
            f"name: {name}\n"
            f"description: {description}\n"
            f"tools: {tools}\n"
            f"model: {model}\n"
            f"---\n\n"
        )

        knowledge = self._agent_knowledge_links(meta)

        body = (
            f"You are **{display}** — {meta.get('role', '')}\n\n"
            f"{meta.get('description', '')}\n\n"
            f"## Domains\n\n"
            f"{self._bullet(meta.get('domains', [])) or '- None'}\n\n"
            f"## Knowledge Bindings (Aegis)\n\n"
            f"### Architecture Blueprints\n"
            f"{knowledge['architecture'] or '- None'}\n\n"
            f"### Workflows\n"
            f"{knowledge['workflows'] or '- None'}\n\n"
            f"### Skills / Rules\n"
            f"{knowledge['skills'] or '- None'}\n\n"
            f"## Core Behavior\n\n"
            f"- Planning: {behavior.get('planning', 'optional')}\n"
            f"- Testing: {behavior.get('testing', 'optional')}\n"
            f"- Review Style: {behavior.get('review_style', 'balanced')}\n"
            f"- Response Format: {behavior.get('response_format', 'detailed')}\n\n"
            f"Follow Aegis engineering principles strictly.\n"
            f"Always consult the linked knowledge when making decisions.\n"
        )

        return frontmatter + body

    def _agent_knowledge_links(self, meta: Dict[str, Any]) -> Dict[str, str]:
        return {
            "architecture": self._bullet(meta.get("blueprints", [])),
            "workflows": self._bullet(meta.get("workflows", [])),
            "skills": self._bullet(meta.get("skills", [])),
        }

    @staticmethod
    def _bullet(items: List[str]) -> str:
        if not items:
            return ""
        return "\n".join(f"- {item}" for item in items)

    def _emit_skills(self, ir_dict: Dict[str, Any], base: Path) -> None:
        skills_dir = base / "skills"
        skills_dir.mkdir(parents=True, exist_ok=True)
        count = 0

        knowledge = ir_dict.get("knowledge", [])
        if isinstance(knowledge, dict):
            knowledge = list(knowledge.values())

        for k in knowledge:
            kind = k.get("kind")
            if kind not in {"rule", "principle", "reference", "policy", "skill"}:
                continue

            skill_name = _normalize_name(str(k["id"]))
            skill_dir = skills_dir / skill_name
            content = self._render_skill_md(k, skill_name)
            _safe_write(skill_dir / "SKILL.md", content)
            count += 1

        print(f"✔ SkillsEmitter: Generated {count} skills in .claude/skills/.")

    def _render_skill_md(self, k: Dict[str, Any], skill_name: str) -> str:
        content = k.get("content", {})
        summary = content.get("summary", k.get("id"))
        raw = _strip_legacy_frontmatter(content.get("raw", ""))
        description = _skill_description(k)

        frontmatter = (
            f"---\n"
            f"name: {skill_name}\n"
            f"description: {description}\n"
            f"---\n\n"
        )

        trailing = (
            f"\n---\n"
            f"**Domain**: {k.get('domain', 'shared')}  \n"
            f"**Kind**: {k.get('kind', 'skill')}\n"
        )

        raw_stripped = raw.strip()
        raw_first_line = raw_stripped.splitlines()[0] if raw_stripped else ""
        raw_lead = re.sub(r"^#+\s*", "", raw_first_line).strip()

        if summary and raw_lead.lower() == summary.strip().lower():
            body = f"{raw}{trailing}"
        else:
            body = f"# {summary}\n\n{raw}{trailing}"

        return frontmatter + body

    def _emit_claude_md(self, ir_dict: Dict[str, Any], base: Path) -> None:
        knowledge = ir_dict.get("knowledge", [])
        if isinstance(knowledge, dict):
            knowledge = list(knowledge.values())

        principles: List[str] = []
        for k in knowledge:
            if k.get("kind") in {"rule", "principle", "policy"}:
                summary = k.get("content", {}).get("summary", k.get("id"))
                domain = k.get("domain", "shared")
                principles.append(f"- **[{domain}]** {summary}")

        sections = [
            "# Aegis Project Knowledge",
            "",
            "_Generated automatically from Aegis Framework (knowledge-to-tools)._",
            "",
            "This file contains team-wide engineering principles and rules. ",
            "Detailed procedures live in `.claude/skills/` and specialized roles in `.claude/agents/`.",
            "",
            "## Engineering Principles & Rules",
            "",
        ]

        if principles:
            sections.extend(principles)
        else:
            sections.append("- None")

        sections.append("")
        sections.append(f"<!-- Generated: {_now_iso()} -->")

        _safe_write(base / "CLAUDE.md", "\n".join(sections))
        print("✔ CLAUDE.md: Generated project memory file.")
