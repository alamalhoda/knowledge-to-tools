from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

sys.path.insert(0, str(Path(__file__).parent.parent))

from ir.compiler import IRCompiler
from ir.validator import IRValidator
from ir.version import SUPPORTED_VERSIONS


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


def compute_test_source_hash(index: Dict[str, Any], agents: Dict[str, Any]) -> str:
    """Compute deterministic hash for testing."""
    payload = json.dumps({"index": index, "agents": agents}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def test_ir_schema_compliance() -> bool:
    """Test that compiled IR conforms to the formal IR schema."""
    index = load_json(Path("knowledge/index.json"))
    agents: Dict[str, Any] = {}
    for f in sorted(Path("agents").glob("*.json")):
        agents[f.stem] = load_json(f)

    workflows = load_json(Path("workflows/index.json"))
    capabilities = load_json(Path("capabilities/index.json"))
    knowledge_raw = load_knowledge_raw(index, Path("knowledge"))

    compiler = IRCompiler(
        knowledge_index=index,
        agents=agents,
        capabilities=capabilities,
        workflows=workflows,
        routes={},
        contracts={},
        knowledge_raw=knowledge_raw,
    )
    source_hash = compute_test_source_hash(index, agents)
    ir_root = compiler.compile(source_hash=source_hash)

    assert ir_root.version in SUPPORTED_VERSIONS, f"Unsupported version: {ir_root.version}"
    assert ir_root.generated_at, "generated_at must be set"
    assert len(ir_root.knowledge) > 0, "knowledge graph must not be empty"
    assert len(ir_root.agents) > 0, "agent graph must not be empty"

    for k in ir_root.knowledge:
        assert k.type == "knowledge_ir"
        assert k.id
        assert k.source
        assert k.domain
        assert k.kind
        assert k.content is not None
        assert k.content.raw
        assert k.content.summary

    for a in ir_root.agents:
        assert a.type == "agent_ir"
        assert a.id
        assert a.name
        assert a.display_name
        assert a.description
        assert a.role

    validator = IRValidator(ir_root)
    errors = validator.validate()
    assert len(errors) == 0, f"Validation errors: {[str(e) for e in errors]}"

    serialized = json.dumps(ir_root.to_dict(), sort_keys=True)
    assert len(serialized) > 0, "Serialized IR must not be empty"

    return True


def test_ir_determinism() -> bool:
    """Test that identical inputs produce structurally identical IR."""
    index = load_json(Path("knowledge/index.json"))
    agents: Dict[str, Any] = {}
    for f in sorted(Path("agents").glob("*.json")):
        agents[f.stem] = load_json(f)

    workflows = load_json(Path("workflows/index.json"))
    capabilities = load_json(Path("capabilities/index.json"))
    knowledge_raw = load_knowledge_raw(index, Path("knowledge"))
    source_hash = compute_test_source_hash(index, agents)

    compiler = IRCompiler(
        knowledge_index=index,
        agents=agents,
        capabilities=capabilities,
        workflows=workflows,
        routes={},
        contracts={},
        knowledge_raw=knowledge_raw,
    )

    generated_at = datetime.now(timezone.utc).isoformat()

    ir1 = compiler.compile(source_hash=source_hash, generated_at=generated_at)
    ir2 = compiler.compile(source_hash=source_hash, generated_at=generated_at)

    d1 = ir1.to_dict()
    d2 = ir2.to_dict()

    assert d1 == d2, "Determinism violation: identical inputs produced different IR"

    return True


def test_emitter_output_exists() -> bool:
    """Test that emitters produce expected output files."""
    kilo_agents = Path("aegis_output/kilo/agents")
    opencode_agents = Path("aegis_output/opencode/agents")
    opencode_config = Path("aegis_output/opencode/opencode.json")
    cursor_agents = Path("aegis_output/cursor/agents")

    assert kilo_agents.exists(), ".kilo/agents directory must exist"
    assert len(list(kilo_agents.glob("*.md"))) > 0, "Kilo agents must be generated"

    assert opencode_agents.exists(), ".opencode/agents directory must exist"
    assert len(list(opencode_agents.glob("*.json"))) > 0, "OpenCode agents must be generated"

    assert opencode_config.exists(), "opencode.json must be generated"

    assert cursor_agents.exists(), ".cursor/agents directory must exist"
    assert len(list(cursor_agents.glob("*.md"))) > 0, "Cursor agents must be generated"

    return True


def test_emitter_isolation() -> bool:
    """Test that emitters do not import from prohibited modules."""
    import ast
    import importlib.util

    emitter_files = [
        "emitters/base.py",
        "emitters/kilo.py",
        "emitters/opencode.py",
        "emitters/cursor.py",
    ]

    prohibited_modules = [
        "ai.knowledge",
        "ai.router",
        "ai.planning",
        "ai.generators",
        "ai.runtime",
    ]

    for emitter_file in emitter_files:
        path = Path(emitter_file)
        if not path.exists():
            continue

        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for prohibited in prohibited_modules:
                    if module.startswith(prohibited):
                        raise AssertionError(
                            f"Emitter {emitter_file} imports prohibited module: {module}"
                        )

    return True


def test_ir_stability() -> bool:
    """Test that IR output is stable across regenerations."""
    ir_path = Path("ir/ir_compiled.json")
    if not ir_path.exists():
        return True

    current = ir_path.read_text(encoding="utf-8")
    current_hash = hashlib.sha256(current.encode("utf-8")).hexdigest()

    snapshot_path = Path("tests/snapshots/ir_snapshot.hash")
    if snapshot_path.exists():
        expected_hash = snapshot_path.read_text(encoding="utf-8").strip()
        assert current_hash == expected_hash, (
            f"IR snapshot mismatch: {current_hash} != {expected_hash}"
        )
    else:
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot_path.write_text(current_hash, encoding="utf-8")
        print(f"Created IR snapshot: {current_hash}")

    return True


def test_agent_registry_consistency() -> bool:
    """Test that all agents in registry are valid and referenced."""
    index = load_json(Path("knowledge/index.json"))
    agents: Dict[str, Any] = {}
    for f in sorted(Path("agents").glob("*.json")):
        agents[f.stem] = load_json(f)

    workflows = load_json(Path("workflows/index.json"))
    capabilities = load_json(Path("capabilities/index.json"))
    knowledge_raw = load_knowledge_raw(index, Path("knowledge"))
    source_hash = compute_test_source_hash(index, agents)

    compiler = IRCompiler(
        knowledge_index=index,
        agents=agents,
        capabilities=capabilities,
        workflows=workflows,
        routes={},
        contracts={},
        knowledge_raw=knowledge_raw,
    )
    ir_root = compiler.compile(source_hash=source_hash)

    agent_ids = {a.id for a in ir_root.agents}
    for wf in ir_root.workflows:
        for stage in wf.stages:
            assert stage.agent in agent_ids, (
                f"Workflow {wf.id} stage {stage.id} references unknown agent {stage.agent}"
            )

    return True


def run_all_tests() -> int:
    tests = [
        ("IR Schema Compliance", test_ir_schema_compliance),
        ("IR Determinism", test_ir_determinism),
        ("Emitter Output Exists", test_emitter_output_exists),
        ("Emitter Isolation", test_emitter_isolation),
        ("IR Stability", test_ir_stability),
        ("Agent Registry Consistency", test_agent_registry_consistency),
    ]

    passed = 0
    failed = 0

    print("🧪 Running Aegis IR Architecture Snapshot Tests...\n")

    for name, test_fn in tests:
        try:
            result = test_fn()
            if result is not False:
                print(f"  ✔ {name}")
                passed += 1
            else:
                print(f"  ❌ {name}: returned False")
                failed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    raise SystemExit(run_all_tests())
