from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import List, Tuple, Set


LAYERS = {
    "knowledge": "Knowledge Layer",
    "compiler": "Compiler Layer (IR Compiler)",
    "ir": "IR Layer",
    "runtime": "Runtime Layer",
    "emitters": "Emitters Layer",
    "pipeline": "Pipeline Layer",
}

PROHIBITED_EMITTER_IMPORTS = {
    "ai.knowledge",
    "ai.router",
    "ai.planning",
    "ai.generators",
    "ai.runtime",
    "ai.core",
}


def get_module_layer(module_path: Path) -> str:
    """Determine which layer a module belongs to."""
    rel_parts = module_path.relative_to(Path(".")).parts
    if rel_parts[0] in LAYERS:
        return rel_parts[0]
    return "unknown"


def find_python_files(base_dir: Path) -> List[Path]:
    """Find all Python files in .ai directory."""
    return list(base_dir.rglob("*.py"))


def analyze_imports(file_path: Path, base_dir: Path) -> List[Tuple[str, str]]:
    """Analyze imports in a Python file."""
    imports = []
    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (SyntaxError, UnicodeDecodeError):
        return imports

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(("import", alias.name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(("from", f"{module}.{alias.name}" if module else alias.name))

    return imports


def check_emitter_isolation() -> List[str]:
    """Verify emitters do not import prohibited modules."""
    violations = []
    emitter_dir = Path("emitters")
    for py_file in emitter_dir.rglob("*.py"):
        imports = analyze_imports(py_file, Path("."))
        for imp_type, imp_name in imports:
            for prohibited in PROHIBITED_EMITTER_IMPORTS:
                if imp_name.startswith(prohibited):
                    violations.append(
                        f"EMITTER_ISOLATION_VIOLATION: {py_file} imports {imp_name}"
                    )
    return violations


def check_dependency_direction() -> List[str]:
    """Check that dependency direction follows allowed flow."""
    violations = []
    base_dir = Path(".")
    files = find_python_files(base_dir)

    for file_path in files:
        if file_path.name == "__init__.py":
            continue

        layer = get_module_layer(file_path)
        if layer == "unknown":
            continue

        imports = analyze_imports(file_path, base_dir)
        for imp_type, imp_name in imports:
            if imp_type == "from" and "." in imp_name:
                parts = imp_name.split(".")
                if len(parts) >= 2 and parts[0] == "ai":
                    target_layer = parts[1]
                    if target_layer in LAYERS and target_layer != layer:
                        if target_layer == "knowledge" and layer != "compiler":
                            violations.append(
                                f"DEPENDENCY_DIRECTION_VIOLATION: {file_path} ({layer}) imports {imp_name} (knowledge)"
                            )
                        if layer == "emitters" and target_layer == "knowledge":
                            violations.append(
                                f"EMITTER_DEPENDENCY_VIOLATION: {file_path} ({layer}) imports {imp_name}"
                            )
    return violations


def check_circular_dependencies() -> List[str]:
    """Detect circular dependencies between modules."""
    import_graph: dict = {}
    base_dir = Path(".")
    files = find_python_files(base_dir)

    for file_path in files:
        if file_path.name == "__init__.py":
            continue

        rel_path = file_path.relative_to(base_dir)
        mod_key = str(rel_path.with_suffix("")).replace("/", ".")
        imports = analyze_imports(file_path, base_dir)
        dep_set: set = set()
        for imp_type, imp_name in imports:
            if imp_type == "from" and imp_name.startswith("ai."):
                dep_set.add(imp_name)
        import_graph[mod_key] = dep_set

    cycles = []
    for mod, deps in import_graph.items():
        for dep in deps:
            if dep in import_graph and mod in import_graph[dep]:
                cycles.append(f"CIRCULAR_DEPENDENCY: {mod} <-> {dep}")

    return cycles


def check_ir_immutability() -> List[str]:
    """Verify IR models are immutable (frozen dataclasses)."""
    violations = []
    models_dir = Path("ir/models")

    for py_file in models_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue

        source = py_file.read_text(encoding="utf-8")
        if "@dataclass" in source and "frozen=True" not in source:
            violations.append(
                f"IR_IMMUTABILITY_VIOLATION: {py_file} uses non-frozen dataclass"
            )

    return violations


def check_tool_leakage() -> List[str]:
    """Verify IR does not contain tool-specific configuration."""
    violations = []

    ir_compiled = Path("ir/ir_compiled.json")
    if not ir_compiled.exists():
        return violations

    data = json.loads(ir_compiled.read_text(encoding="utf-8"))

    for agent_id, agent in data.get("agents", {}).items():
        if "model" in agent:
            violations.append(f"TOOL_LEAKAGE: Agent {agent_id} contains 'model' field")
        if "temperature" in agent:
            violations.append(f"TOOL_LEAKAGE: Agent {agent_id} contains 'temperature' field")
        if "steps" in agent:
            violations.append(f"TOOL_LEAKAGE: Agent {agent_id} contains 'steps' field")
        if "context" in agent and isinstance(agent.get("context"), list):
            for ctx_item in agent["context"]:
                if ".kilo/" in ctx_item or ".opencode/" in ctx_item or ".cursor/" in ctx_item:
                    violations.append(
                        f"TOOL_LEAKAGE: Agent {agent_id} contains tool-specific context: {ctx_item}"
                    )
                    break

    return violations


def run_integrity_checks() -> int:
    """Run all architecture integrity checks."""
    print("🔍 Running Aegis IR Architecture Integrity Checks...\n")

    all_violations: List[str] = []

    checks = [
        ("Emitter Isolation", check_emitter_isolation),
        ("Dependency Direction", check_dependency_direction),
        ("Circular Dependencies", check_circular_dependencies),
        ("IR Immutability", check_ir_immutability),
        ("Tool Leakage", check_tool_leakage),
    ]

    for name, check_fn in checks:
        violations = check_fn()
        if violations:
            print(f"  ❌ {name}:")
            for v in violations:
                print(f"    - {v}")
            all_violations.extend(violations)
        else:
            print(f"  ✔ {name}")

    print(f"\nTotal violations: {len(all_violations)}")
    return 1 if all_violations else 0


if __name__ == "__main__":
    raise SystemExit(run_integrity_checks())
