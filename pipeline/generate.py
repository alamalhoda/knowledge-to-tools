import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from ir.transformer import IRTransformer
from core import AgentComposer
from emitters.kilo import KiloEmitter
from emitters.opencode import OpenCodeEmitter


def load_data():
    index_path = Path(".ai/knowledge/index.json")
    agents_dir = Path(".ai/agents")

    index = json.loads(index_path.read_text(encoding="utf-8"))
    agents = {}

    for f in agents_dir.glob("*.json"):
        agents[f.stem] = json.loads(f.read_text(encoding="utf-8"))

    return index, agents


def main():
    index, agents = load_data()

    # Step 1: Transform knowledge to IR format (extracts content, key points, etc.)
    print("🔧 Transforming knowledge to IR...")
    transformer = IRTransformer(index, agents)
    ir = transformer.transform_all()

    # Save intermediate IR
    ir_path = Path(".ai/ir/ir_data.json")
    ir_path.parent.mkdir(parents=True, exist_ok=True)
    ir_path.write_text(json.dumps(ir, indent=2), encoding="utf-8")
    print("✔ Knowledge IR generated.")

    # Step 2: Compose agents using shared core
    print("🔧 Composing agents...")
    composer = AgentComposer(ir.get("knowledge", []), agents)
    runtime_ir = composer.compose()

    runtime_path = Path(".ai/ir/runtime_ir.json")
    runtime_path.write_text(
        json.dumps(runtime_ir.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print("✔ Runtime IR generated.")

    # Step 3: Emit to Kilo
    print("\n📡 Emitting Kilo artifacts...")
    kilo_emitter = KiloEmitter(runtime_ir.to_dict())
    kilo_emitter.emit()

    # Step 4: Emit to OpenCode
    print("\n📡 Emitting OpenCode artifacts...")
    opencode_emitter = OpenCodeEmitter(runtime_ir.to_dict())
    opencode_emitter.emit()

    print("\n🎉 Aegis v2 generation pipeline completed (Kilo + OpenCode from shared IR).")


if __name__ == "__main__":
    main()