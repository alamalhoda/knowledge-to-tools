from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


RULE_KINDS = frozenset({"rule", "policy"})
PRINCIPLE_KIND = "principle"
SKILL_KINDS = frozenset({"architecture", "workflow", "skill", "reference"})
HIGH_PRIORITY = 80

AGENT_COLORS = {
    "architect": "#8B5CF6",
    "backend": "#3B82F6",
    "frontend": "#10B981",
    "reviewer": "#EF4444",
}


def safe_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def reset_output(base: Path, names: Sequence[str]) -> None:
    """Remove stale emitter artifacts so previous layouts cannot linger."""
    for name in names:
        path = base / name
        if path.is_dir():
            shutil.rmtree(path)
        elif path.is_file():
            path.unlink()


def knowledge_docs(ir_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    knowledge = ir_dict.get("knowledge", [])
    if isinstance(knowledge, dict):
        return list(knowledge.values())
    return list(knowledge or [])


def workflow_nodes(ir_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    workflows = ir_dict.get("workflows", [])
    if isinstance(workflows, dict):
        return list(workflows.values())
    return list(workflows or [])


def agents_map(ir_dict: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    agents = ir_dict.get("agents", {})
    if isinstance(agents, list):
        return {str(a.get("id")): a for a in agents if a.get("id")}
    return dict(agents or {})


def normalize_name(name: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", str(name).lower()).strip("-")
    normalized = re.sub(r"-+", "-", normalized)
    return normalized[:64] or "item"


def strip_legacy_frontmatter(raw: str) -> str:
    return re.sub(r"\A---\s*\n.*?\n---\s*\n", "", raw or "", flags=re.DOTALL).lstrip()


def yaml_quote(value: str) -> str:
    cleaned = str(value).replace("\r\n", "\n").replace("\n", " ").strip()
    return '"' + cleaned.replace("\\", "\\\\").replace('"', '\\"') + '"'


def truncate(text: str, limit: int) -> str:
    text = str(text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def kind_of(doc: Dict[str, Any]) -> str:
    return str(doc.get("kind") or "")


def doc_id(doc: Dict[str, Any]) -> str:
    return str(doc.get("id") or "")


def domain_of(doc: Dict[str, Any]) -> str:
    return str(doc.get("domain") or "shared")


def priority_of(doc: Dict[str, Any]) -> int:
    try:
        return int(doc.get("priority", 50))
    except (TypeError, ValueError):
        return 50


def summary_of(doc: Dict[str, Any]) -> str:
    content = doc.get("content") or {}
    return str(content.get("summary") or doc.get("id") or "")


def raw_body(doc: Dict[str, Any]) -> str:
    content = doc.get("content") or {}
    return strip_legacy_frontmatter(str(content.get("raw") or "")).strip()


def file_patterns(doc: Dict[str, Any]) -> List[str]:
    activation = doc.get("activation") or {}
    patterns = list(activation.get("file_patterns") or [])
    if patterns:
        return [str(p) for p in patterns if p]
    applies = doc.get("applies_to") or []
    if isinstance(applies, dict):
        return []
    return [str(p) for p in applies if p]


def skill_description(doc: Dict[str, Any], limit: int = 1024) -> str:
    content = doc.get("content") or {}
    base = (
        content.get("description")
        or summary_of(doc)
        or doc_id(doc).replace("-", " ")
    )
    patterns = file_patterns(doc)
    extra = ""
    if patterns:
        extra = f" Use when editing {', '.join(patterns[:6])}."
    kind = kind_of(doc)
    domain = domain_of(doc)
    prefix = f"{domain} {kind}: " if kind else ""
    return truncate(f"{prefix}{base}.{extra}".replace("..", "."), limit)


def yaml_block_list(key: str, items: Sequence[str]) -> str:
    if not items:
        return ""
    lines = [f"{key}:"]
    lines.extend(f"  - {yaml_quote(item)}" for item in items)
    return "\n".join(lines) + "\n"


def markdown_bullets(items: Iterable[str]) -> str:
    values = [str(item) for item in items if item]
    if not values:
        return "- None"
    return "\n".join(f"- {item}" for item in values)


def render_knowledge_body(doc: Dict[str, Any]) -> str:
    summary = summary_of(doc)
    raw = raw_body(doc)
    if not raw:
        return f"# {summary}\n" if summary else ""
    first = raw.splitlines()[0].strip()
    lead = re.sub(r"^#+\s*", "", first).strip()
    if summary and lead.lower() == summary.strip().lower():
        return raw
    if first.startswith("#"):
        return raw
    title = summary or doc_id(doc)
    return f"# {title}\n\n{raw}"


def render_workflow_skill_body(workflow: Dict[str, Any]) -> str:
    name = workflow.get("name") or workflow.get("id") or "Workflow"
    description = workflow.get("description") or ""
    triggers = workflow.get("triggers") or []
    stages = workflow.get("stages") or []
    agents = workflow.get("agents") or []

    lines = [
        f"# {name}",
        "",
        description,
        "",
        "## When to use",
        markdown_bullets(triggers) if triggers else "- Use when this multi-stage workflow applies.",
        "",
        "## Agents",
        markdown_bullets(agents),
        "",
        "## Stages",
        "",
    ]
    for index, stage in enumerate(stages, start=1):
        stage_name = stage.get("name") or stage.get("id") or f"stage-{index}"
        agent = stage.get("agent") or "unassigned"
        depends = ", ".join(stage.get("depends_on") or []) or "none"
        knowledge = ", ".join(stage.get("required_knowledge") or []) or "none"
        capabilities = ", ".join(stage.get("required_capabilities") or []) or "none"
        lines.extend(
            [
                f"{index}. **{stage_name}** (agent: `{agent}`)",
                f"   - Depends on: {depends}",
                f"   - Knowledge: {knowledge}",
                f"   - Capabilities: {capabilities}",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def workflow_skill_description(workflow: Dict[str, Any], limit: int = 1024) -> str:
    name = workflow.get("name") or workflow.get("id")
    description = workflow.get("description") or name
    triggers = workflow.get("triggers") or []
    extra = f" Triggers: {', '.join(str(t) for t in triggers[:8])}." if triggers else ""
    return truncate(f"{description}.{extra}".replace("..", "."), limit)


def agent_permissions(agent: Dict[str, Any]) -> Dict[str, Any]:
    return agent.get("permissions") or {}


def agent_readonly(agent: Dict[str, Any]) -> bool:
    return not bool(agent_permissions(agent).get("edit", True))


def agent_mode(agent: Dict[str, Any]) -> str:
    authority = agent.get("authority") or {}
    if authority.get("can_delegate"):
        return "all"
    if agent_readonly(agent):
        return "all"
    return "primary"


def agent_color(agent_id: str) -> str:
    return AGENT_COLORS.get(agent_id, "#3B82F6")


def permission_action(enabled: bool) -> str:
    return "allow" if enabled else "deny"


def render_agent_prompt(agent: Dict[str, Any]) -> str:
    display = agent.get("display_name") or agent.get("name") or agent.get("id") or "Agent"
    role = agent.get("role") or ""
    description = agent.get("description") or ""
    behavior = agent.get("behavior") or {}
    return (
        f"You are **{display}** — {role}\n\n"
        f"{description}\n\n"
        f"## Domains\n\n"
        f"{markdown_bullets(agent.get('domains') or [])}\n\n"
        f"## Knowledge Bindings\n\n"
        f"### Architecture\n"
        f"{markdown_bullets(agent.get('blueprints') or [])}\n\n"
        f"### Workflows\n"
        f"{markdown_bullets(agent.get('workflows') or [])}\n\n"
        f"### Skills\n"
        f"{markdown_bullets(agent.get('skills') or [])}\n\n"
        f"## Core Behavior\n\n"
        f"- Planning: {behavior.get('planning', 'optional')}\n"
        f"- Testing: {behavior.get('testing', 'optional')}\n"
        f"- Review Style: {behavior.get('review_style', 'balanced')}\n"
        f"- Response Format: {behavior.get('response_format', 'detailed')}\n\n"
        f"Follow Aegis engineering principles strictly.\n"
        f"Always consult the linked knowledge when making decisions.\n"
    )


def high_priority_docs(docs: Sequence[Dict[str, Any]], kinds: Iterable[str]) -> List[Dict[str, Any]]:
    wanted = set(kinds)
    return [
        doc
        for doc in docs
        if kind_of(doc) in wanted and priority_of(doc) >= HIGH_PRIORITY
    ]


def docs_of_kind(docs: Sequence[Dict[str, Any]], kinds: Iterable[str]) -> List[Dict[str, Any]]:
    wanted = set(kinds)
    return [doc for doc in docs if kind_of(doc) in wanted]


def cursor_always_apply(doc: Dict[str, Any]) -> bool:
    kind = kind_of(doc)
    patterns = file_patterns(doc)
    priority = priority_of(doc)
    if kind == "policy" and not patterns:
        return True
    if kind == PRINCIPLE_KIND and priority >= HIGH_PRIORITY:
        return True
    if kind == "rule" and not patterns and priority >= HIGH_PRIORITY:
        return True
    return False


def merge_skill_sources(ir_dict: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any], str]]:
    """Return (skill_name, source_dict, origin) with IR workflows winning on id clash."""
    items: Dict[str, Tuple[str, Dict[str, Any], str]] = {}
    for doc in docs_of_kind(knowledge_docs(ir_dict), SKILL_KINDS):
        name = normalize_name(doc_id(doc))
        items[name] = (name, doc, "knowledge")
    for workflow in workflow_nodes(ir_dict):
        name = normalize_name(str(workflow.get("id") or "workflow"))
        items[name] = (name, workflow, "workflow")
    return list(items.values())
