from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ir.compiler import IRCompiler
from ir.validator import IRValidator
from emitters.future_ai import FutureAIEmitter


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    import json
    return json.loads(path.read_text(encoding="utf-8"))


def load_knowledge_raw(index: dict, knowledge_dir: Path) -> dict:
    raw_map = {}
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


def test_future_emitter_independence() -> int:
    """Simulate adding a new emitter without changing IR or compiler."""
    import hashlib

    index = load_json(Path(".ai/knowledge/index.json"))
    agents = {}
    for f in sorted(Path(".ai/agents").glob("*.json")):
        agents[f.stem] = load_json(f)

    workflows = load_json(Path(".ai/workflows/index.json"))
    capabilities = load_json(Path(".ai/capabilities/index.json"))
    knowledge_raw = load_knowledge_raw(index, Path(".ai/knowledge"))
    source_hash = hashlib.sha256(
        __import__('json').dumps({"index": index, "agents": agents}, sort_keys=True).encode()
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
    ir_root = compiler.compile(source_hash=source_hash)

    validator = IRValidator(ir_root)
    errors = validator.validate()
    if errors:
        print("❌ Base IR validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("✔ Base IR validation passed")

    output_dir = Path(".ai/tests/future_ai_output")
    if output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)

    emitter = FutureAIEmitter()
    emitter.emit(ir_root, output_dir)

    agents_dir = output_dir / "agents"
    skills_dir = output_dir / "skills"
    config_path = output_dir / "future_ai.json"

    assert agents_dir.exists(), "agents dir must exist"
    assert skills_dir.exists(), "skills dir must exist"
    assert config_path.exists(), "config must exist"
    assert len(list(agents_dir.glob("*.md"))) > 0, "agents must be generated"
    assert len(list(skills_dir.rglob("*.md"))) > 0, "skills must be generated"

    print(f"✔ FutureAI emitter generated {len(list(agents_dir.glob('*.md')))} agents")
    print(f"✔ FutureAI emitter generated {len(list(skills_dir.glob('*.md')))} skills")

    return 0


if __name__ == "__main__":
    raise SystemExit(test_future_emitter_independence())
