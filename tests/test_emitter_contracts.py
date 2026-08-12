from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict

sys.path.insert(0, str(Path(__file__).parent.parent))

from emitters.claude import ClaudeEmitter
from emitters.cursor import CursorEmitter
from emitters.kilo import KiloEmitter
from emitters.opencode import OpenCodeEmitter
from ir.compiler import IRCompiler


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_knowledge_raw(index: Dict[str, Any], knowledge_dir: Path) -> Dict[str, str]:
    raw_map: Dict[str, str] = {}
    for doc in index.get("documents", []):
        doc_id = doc.get("id", "")
        rel_path = doc.get("path", "")
        if not rel_path:
            continue
        if rel_path.startswith("knowledge/"):
            rel_path = rel_path[len("knowledge/"):]
        full_path = knowledge_dir / rel_path
        if full_path.exists():
            raw_map[doc_id] = full_path.read_text(encoding="utf-8")
        else:
            raw_map[doc_id] = doc.get("content", {}).get("raw", "")
    return raw_map


def compile_ir():
    index = load_json(Path("knowledge/index.json"))
    agents: Dict[str, Any] = {}
    for f in sorted(Path("agents").glob("*.json")):
        agents[f.stem] = load_json(f)
    workflows = load_json(Path("workflows/index.json"))
    capabilities = load_json(Path("capabilities/index.json"))
    knowledge_raw = load_knowledge_raw(index, Path("knowledge"))
    source_hash = hashlib.sha256(
        json.dumps({"index": index, "agents": agents}, sort_keys=True).encode()
    ).hexdigest()
    compiler = IRCompiler(
        knowledge_index=index,
        agents=agents,
        capabilities=capabilities,
        workflows=workflows,
        routes={},
        contracts={},
        knowledge_raw=knowledge_raw,
    )
    return compiler.compile(source_hash=source_hash)


def _frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    return parts[1] if len(parts) > 2 else ""


def test_cursor_contract() -> bool:
    ir = compile_ir()
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        CursorEmitter().emit(ir, base)

        rule = (base / "rules" / "backend-security-security.mdc").read_text(encoding="utf-8")
        assert "alwaysApply:" in rule
        assert "description:" in rule
        assert (base / "rules" / "shared-engineering-principles.mdc").exists()
        assert not (base / "rules" / "frontend-state-pinia.mdc").exists()

        pinia = (base / "skills" / "frontend-state-pinia" / "SKILL.md").read_text(encoding="utf-8")
        fm = _frontmatter(pinia)
        assert "name: frontend-state-pinia" in fm
        assert "description:" in fm
        assert "paths:" in fm

        arch = base / "skills" / "backend-architecture-django-architecture" / "SKILL.md"
        assert arch.exists()

        flow = (base / "skills" / "backend-api-flow" / "SKILL.md").read_text(encoding="utf-8")
        assert "name: backend-api-flow" in flow
        assert "## Stages" in flow

        reviewer = (base / "agents" / "reviewer.md").read_text(encoding="utf-8")
        assert "readonly: true" in reviewer
        assert "model: inherit" in reviewer
        backend = (base / "agents" / "backend.md").read_text(encoding="utf-8")
        assert "readonly: false" in backend

        agents_md = (base / "AGENTS.md").read_text(encoding="utf-8")
        assert "## Principles" in agents_md
        assert "`architect`" in agents_md
    return True


def test_kilo_contract() -> bool:
    ir = compile_ir()
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        KiloEmitter().emit(ir, base)

        assert (base / "rules" / "backend-security-security.md").exists()
        assert not (base / "architecture").exists()
        assert not (base / "workflows").exists()

        skill = (base / "skills" / "frontend-state-pinia" / "SKILL.md").read_text(encoding="utf-8")
        fm = _frontmatter(skill)
        assert "name: frontend-state-pinia" in fm
        assert "description:" in fm
        assert "aegis_kind:" in fm
        assert "id:" not in fm.split("metadata:", 1)[0]

        config = json.loads((base / "kilo.jsonc").read_text(encoding="utf-8"))
        assert ".kilo/rules/*.md" in config["instructions"]
        assert ".kilo/skills" in config["skills"]["paths"]

        reviewer = (base / "agents" / "reviewer.md").read_text(encoding="utf-8")
        assert "edit: deny" in reviewer
        assert "mode: all" in reviewer
        assert "steps:" not in _frontmatter(reviewer)
        assert "context:" not in _frontmatter(reviewer)

        assert (base / "AGENTS.md").exists()
        assert (base / "skills" / "backend-api-flow" / "SKILL.md").exists()
    return True


def test_claude_contract() -> bool:
    ir = compile_ir()
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        ClaudeEmitter().emit(ir, base)

        rule = (base / "rules" / "backend-security-security.md").read_text(encoding="utf-8")
        assert "paths:" in rule
        assert not (base / "rules" / "frontend-state-pinia.md").exists()

        pinia = (base / "skills" / "frontend-state-pinia" / "SKILL.md").read_text(encoding="utf-8")
        assert "name: frontend-state-pinia" in pinia
        assert "paths:" in pinia

        reference = (base / "skills" / "backend-core-quick-reference" / "SKILL.md").read_text(encoding="utf-8")
        assert "user-invocable: false" in reference

        workflow = (base / "skills" / "shared-rules-audit-checklist" / "SKILL.md").read_text(encoding="utf-8")
        assert "disable-model-invocation: true" in workflow

        claude_md = (base / "CLAUDE.md").read_text(encoding="utf-8")
        assert len(claude_md.splitlines()) < 200
        assert ".claude/rules/" in claude_md
        assert "@AGENTS.md" in claude_md

        reviewer = (base / "agents" / "reviewer.md").read_text(encoding="utf-8")
        assert "Write" not in _frontmatter(reviewer)
        assert "Read" in _frontmatter(reviewer)
        backend = (base / "agents" / "backend.md").read_text(encoding="utf-8")
        assert "Write" in _frontmatter(backend)
    return True


def test_opencode_contract() -> bool:
    ir = compile_ir()
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        OpenCodeEmitter().emit(ir, base)

        assert (base / "instructions" / "backend-security-security.md").exists()
        assert not list((base / "agents").glob("*.json"))
        assert (base / "agents" / "backend.md").exists()

        skill = (base / "skills" / "frontend-state-pinia" / "SKILL.md").read_text(encoding="utf-8")
        fm = _frontmatter(skill)
        assert "name: frontend-state-pinia" in fm
        assert "description:" in fm
        assert "compatibility: opencode" in fm
        for banned in ("id:", "kind:", "paths:", "domain:"):
            assert banned not in fm.split("metadata:", 1)[0]

        assert (base / "commands" / "shared-gitflow-branch-policy.md").exists()

        config = json.loads((base / "opencode.json").read_text(encoding="utf-8"))
        assert config["instructions"] == [".opencode/instructions/*.md"]
        assert config["permission"]["skill"]["*"] == "allow"

        reviewer = (base / "agents" / "reviewer.md").read_text(encoding="utf-8")
        assert "edit: deny" in reviewer
        assert "mode: all" in reviewer

        agents_md = (base / "AGENTS.md").read_text(encoding="utf-8")
        assert "## Principles" in agents_md
        assert "`backend`" in agents_md
    return True


def run_all_tests() -> int:
    tests = [
        ("Cursor contract", test_cursor_contract),
        ("Kilo contract", test_kilo_contract),
        ("Claude contract", test_claude_contract),
        ("OpenCode contract", test_opencode_contract),
    ]
    failed = 0
    print("Running emitter contract tests...\n")
    for name, fn in tests:
        try:
            fn()
            print(f"  OK {name}")
        except Exception as exc:
            print(f"  FAIL {name}: {exc}")
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run_all_tests())
