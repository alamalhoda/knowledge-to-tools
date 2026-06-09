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
from ir.version import IR_VERSION, SUPPORTED_VERSIONS, raise_if_unsupported, UnsupportedIRVersionError
from emitters.kilo import KiloEmitter
from emitters.opencode import OpenCodeEmitter
from emitters.cursor import CursorEmitter


def compute_source_hash(index: Dict[str, Any], agents: Dict[str, Any]) -> str:
    """Compute deterministic hash of source inputs."""
    payload = json.dumps({"index": index, "agents": agents}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_knowledge_raw(index: Dict[str, Any], knowledge_dir: Path) -> Dict[str, str]:
    """Load raw source text for each knowledge document."""
    raw_map: Dict[str, str] = {}
    for doc in index.get("documents", []):
        doc_id = doc.get("id", "")
        rel_path = doc.get("path", "")
        if not rel_path:
            continue
        full_path = knowledge_dir / rel_path
        if full_path.exists():
            raw_map[doc_id] = full_path.read_text(encoding="utf-8")
        else:
            raw_map[doc_id] = doc.get("content", {}).get("raw", "")
    return raw_map


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_or_exit(ir_root: Any) -> None:
    validator = IRValidator(ir_root)
    errors = validator.validate()
    if errors:
        print("\n🚨 IR validation failed:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    print("✔ IR validation passed.")


def main() -> int:
    now_iso = datetime.now(timezone.utc).isoformat()

    index_path = Path(".ai/knowledge/index.json")
    agents_dir = Path(".ai/agents")
    workflows_dir = Path(".ai/workflows")
    capabilities_dir = Path(".ai/capabilities")
    knowledge_dir = Path(".ai/knowledge")

    index = load_json(index_path)
    agents: Dict[str, Any] = {}
    for f in sorted(agents_dir.glob("*.json")):
        agents[f.stem] = load_json(f)

    workflows = load_json(workflows_dir / "index.json")
    capabilities = load_json(capabilities_dir / "index.json")
    contracts: Dict[str, Any] = {}
    routes: Dict[str, Any] = {}

    knowledge_raw = load_knowledge_raw(index, knowledge_dir)
    source_hash = compute_source_hash(index, agents)

    print("🔧 Compiling IR...")
    compiler = IRCompiler(
        knowledge_index=index,
        agents=agents,
        capabilities=capabilities,
        workflows=workflows,
        routes=routes,
        contracts=contracts,
        knowledge_raw=knowledge_raw,
    )
    ir_root = compiler.compile(source_hash=source_hash)

    if ir_root.version not in SUPPORTED_VERSIONS:
        raise UnsupportedIRVersionError(
            f"Compiled IR version '{ir_root.version}' is not supported. "
            f"Supported: {SUPPORTED_VERSIONS}"
        )

    save_json(Path(".ai/ir/ir_compiled.json"), ir_root.to_dict())
    print(f"✔ IR compiled (version {ir_root.version}).")

    print("🔧 Validating IR...")
    validate_or_exit(ir_root)

    print("🔧 Emitting Kilo artifacts...")
    KiloEmitter().emit(ir_root, Path(".kilo"))

    print("\n🔧 Emitting OpenCode artifacts...")
    OpenCodeEmitter().emit(ir_root, Path(".opencode"))

    print("\n🔧 Emitting Cursor artifacts...")
    CursorEmitter().emit(ir_root, Path(".cursor"))

    print("\n🎉 Aegis v2 generation pipeline completed (IR → Kilo + OpenCode + Cursor).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
