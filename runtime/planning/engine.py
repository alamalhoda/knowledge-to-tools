import uuid
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

from ai.ir.runtime_payload import SerializedIRPayload
from ai.runtime.runtime_adapter import payload_to_runtime_dict


class PlanningEngine:
    """
    Aegis v2 Planning Engine — Advanced Agent Orchestration Core.
    Responsible for Workflow matching, DAG generation, dependency validation,
    and step-level knowledge binding.
    """

    def __init__(self, ir_data: Optional[Union[Dict[str, Any], SerializedIRPayload]] = None):
        if isinstance(ir_data, SerializedIRPayload):
            ir_data = payload_to_runtime_dict(ir_data)
        self.ir = ir_data or {}
        self.workflows = self._load_workflows()

    def _load_workflows(self) -> Dict[str, Dict]:
        """بارگذاری WorkflowIRها — در آینده از فایل‌های JSON/IR لود شود"""
        return {
            "backend-api-flow": {
                "id": "backend-api-flow",
                "name": "Backend REST API Implementation",
                "domain": "backend",
                "agents": ["architect", "backend", "reviewer"],
                "triggers": [r"rest\s?api", r"endpoint", r"crud", r"django", r"api"],
                "stages": [
                    {"id": "architecture", "agent": "architect", "depends_on": [], "knowledge": ["backend-architecture-django-architecture"]},
                    {"id": "implementation", "agent": "backend", "depends_on": ["architecture"], "knowledge": ["backend-api-rest"]},
                    {"id": "review", "agent": "reviewer", "depends_on": ["implementation"], "knowledge": ["backend-security-security"]}
                ]
            },
            "frontend-feature-flow": {
                "id": "frontend-feature-flow",
                "name": "Frontend Feature Development",
                "domain": "frontend",
                "agents": ["architect", "frontend", "reviewer"],
                "triggers": [r"vue", r"component", r"pinia", r"ui/ux", r"frontend"],
                "stages": [
                    {"id": "design", "agent": "architect", "depends_on": [], "knowledge": ["frontend-architecture-atomic-design"]},
                    {"id": "implementation", "agent": "frontend", "depends_on": ["design"], "knowledge": ["frontend-patterns-component-patterns"]},
                    {"id": "review", "agent": "reviewer", "depends_on": ["implementation"], "knowledge": []}
                ]
            }
        }

    def create_plan(self, routing_result: Dict[str, Any], context: Any) -> Dict[str, Any]:
        """Main entry point — Generates executable DAG plan"""
        assigned_agent = routing_result.get("agent", "unknown")
        task_description = str(getattr(context, 'task', context)).lower()

        workflow = self._find_best_workflow(assigned_agent, task_description)

        if workflow:
            steps = self._instantiate_dag_workflow(workflow, routing_result)
            workflow_id = workflow["id"]
        else:
            steps = self._generate_dynamic_plan(assigned_agent, routing_result)
            workflow_id = "dynamic-fallback"

        ordered_steps = self._topological_sort(steps)

        return {
            "plan_id": f"pln-{uuid.uuid4().hex[:12]}",
            "workflow_used": workflow_id,
            "metadata": {
                "agent": assigned_agent,
                "domain": routing_result.get("context_pack", {}).get("domain", "general"),
                "confidence": routing_result.get("confidence", 0.75),
                "generated_at": datetime.utcnow().isoformat() + "Z"
            },
            "steps": ordered_steps,
            "execution_graph": self._build_dependency_graph(ordered_steps),
            "knowledge_pack": self._bind_step_knowledge(ordered_steps, routing_result),
            "total_steps": len(ordered_steps)
        }

    def _find_best_workflow(self, agent: str, task: str) -> Optional[Dict]:
        """Regex-based workflow matching"""
        for wf in self.workflows.values():
            if agent not in wf.get("agents", []):
                continue
            if any(re.search(trigger, task, re.IGNORECASE) for trigger in wf.get("triggers", [])):
                return wf
        return None

    def _instantiate_dag_workflow(self, workflow: Dict, routing: Dict) -> List[Dict]:
        """Convert template to concrete steps"""
        return [
            {
                "id": stage["id"],
                "name": stage["id"].replace("_", " ").title(),
                "agent": stage["agent"],
                "depends_on": stage.get("depends_on", []),
                "required_knowledge": stage.get("knowledge", []),
                "status": "pending"
            }
            for stage in workflow.get("stages", [])
        ]

    def _topological_sort(self, steps: List[Dict]) -> List[Dict]:
        """DFS-based topological sort with cycle detection"""
        step_dict = {s["id"]: s for s in steps}
        adj = {s["id"]: s.get("depends_on", []) for s in steps}
        visited = set()
        temp_stack = set()
        order = []

        def visit(node_id: str):
            if node_id in temp_stack:
                raise ValueError(f"Cycle detected in workflow at node: {node_id}")
            if node_id not in visited:
                temp_stack.add(node_id)
                for dep in adj.get(node_id, []):
                    if dep in step_dict:
                        visit(dep)
                temp_stack.remove(node_id)
                visited.add(node_id)
                order.append(step_dict[node_id])

        for s in steps:
            if s["id"] not in visited:
                visit(s["id"])

        return order[::-1]  # Reverse to get correct execution order

    def _generate_dynamic_plan(self, agent: str, routing: Dict) -> List[Dict]:
        """Smart fallback plan"""
        return [
            {"id": "setup", "name": "Context & Architecture", "agent": "architect", "depends_on": [], "required_knowledge": [], "status": "pending"},
            {"id": "execution", "name": "Main Implementation", "agent": agent, "depends_on": ["setup"], "required_knowledge": [], "status": "pending"},
            {"id": "verification", "name": "Review & Validation", "agent": "reviewer", "depends_on": ["execution"], "required_knowledge": [], "status": "pending"}
        ]

    def _build_dependency_graph(self, steps: List[Dict]) -> Dict[str, List[str]]:
        return {s["id"]: s.get("depends_on", []) for s in steps}

    def _bind_step_knowledge(self, steps: List[Dict], routing: Dict) -> Dict[str, List[str]]:
        """Step-specific + limited global knowledge"""
        global_knowledge = routing.get("knowledge", [])[:6]
        mapping = {}
        for s in steps:
            combined = s.get("required_knowledge", []) + global_knowledge
            mapping[s["id"]] = list(dict.fromkeys(combined))  # deduplicate
        return mapping