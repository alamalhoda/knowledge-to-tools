from __future__ import annotations

from typing import Any, Dict, List, Optional


class ValidationError:
    def __init__(self, code: str, message: str, location: str = "") -> None:
        self.code = code
        self.message = message
        self.location = location

    def __str__(self) -> str:
        loc = f" [{self.location}]" if self.location else ""
        return f"[{self.code}]{loc} {self.message}"


class IRValidator:
    """
    Validates IRRoot instances for structural integrity, reference resolution,
    and schema compliance.

    Validation checks:
    - Duplicate IDs across all graphs
    - Missing dependencies
    - Workflow consistency (DAG validation)
    - Route consistency
    - Contract integrity
    - Agent validity
    - Schema compliance
    """

    def __init__(self, ir: Any) -> None:
        self.ir = ir
        self.errors: List[ValidationError] = []
        self._knowledge_ids: set[str] = set()
        self._agent_ids: set[str] = set()
        self._capability_ids: set[str] = set()
        self._workflow_ids: set[str] = set()

    def validate(self) -> List[ValidationError]:
        self.errors = []
        self._index_ids()
        self._check_version()
        self._check_duplicate_ids()
        self._check_knowledge_references()
        self._check_agent_references()
        self._check_capability_references()
        self._check_workflow_consistency()
        self._check_route_consistency()
        self._check_contract_integrity()
        return self.errors

    def _index_ids(self) -> None:
        self._knowledge_ids = {k.id for k in self.ir.knowledge}
        self._agent_ids = {a.id for a in self.ir.agents}
        self._capability_ids = {c.id for c in self.ir.capabilities}
        self._workflow_ids = {w.id for w in self.ir.workflows}
        all_ids = (
            self._knowledge_ids
            | self._agent_ids
            | self._capability_ids
            | self._workflow_ids
            | {r.id for r in self.ir.routes}
            | {c.id for c in self.ir.contracts}
        )
        self._all_ids = all_ids

    def _check_version(self) -> None:
        if not self.ir.version:
            self.errors.append(ValidationError(
                "MISSING_VERSION",
                "IRRoot.version is required",
                "IRRoot",
            ))

    def _check_duplicate_ids(self) -> None:
        seen: Dict[str, str] = {}
        for node_list, node_type in [
            (self.ir.knowledge, "knowledge"),
            (self.ir.agents, "agent"),
            (self.ir.capabilities, "capability"),
            (self.ir.workflows, "workflow"),
            (self.ir.routes, "route"),
            (self.ir.contracts, "contract"),
        ]:
            for node in node_list:
                nid = node.id
                if not nid:
                    self.errors.append(ValidationError(
                        "EMPTY_ID",
                        f"{node_type} node has empty id",
                        node_type,
                    ))
                    continue
                if nid in seen:
                    self.errors.append(ValidationError(
                        "DUPLICATE_ID",
                        f"Duplicate id '{nid}' in {node_type} (also in {seen[nid]})",
                        nid,
                    ))
                else:
                    seen[nid] = node_type

    def _check_knowledge_references(self) -> None:
        for agent in self.ir.agents:
            for skill_id in agent.skills:
                if skill_id not in self._knowledge_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Agent '{agent.id}' references unknown knowledge '{skill_id}'",
                        f"agents.{agent.id}.skills",
                    ))
            for bp_id in agent.blueprints:
                if bp_id not in self._knowledge_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Agent '{agent.id}' references unknown blueprint '{bp_id}'",
                        f"agents.{agent.id}.blueprints",
                    ))
            for wf_id in agent.workflows:
                if wf_id not in self._workflow_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Agent '{agent.id}' references unknown workflow '{wf_id}'",
                        f"agents.{agent.id}.workflows",
                    ))
            for cap_id in agent.capabilities:
                if cap_id not in self._capability_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Agent '{agent.id}' references unknown capability '{cap_id}'",
                        f"agents.{agent.id}.capabilities",
                    ))

    def _check_agent_references(self) -> None:
        for wf in self.ir.workflows:
            for stage in wf.stages:
                if stage.agent not in self._agent_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Workflow '{wf.id}' stage '{stage.id}' references unknown agent '{stage.agent}'",
                        f"workflows.{wf.id}.stages.{stage.id}.agent",
                    ))
            for agent_id in wf.agents:
                if agent_id not in self._agent_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Workflow '{wf.id}' references unknown agent '{agent_id}'",
                        f"workflows.{wf.id}.agents",
                    ))
            for cap_id in wf.capabilities_required:
                if cap_id not in self._capability_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Workflow '{wf.id}' requires unknown capability '{cap_id}'",
                        f"workflows.{wf.id}.capabilities_required",
                    ))

        for agent in self.ir.agents:
            for esc_id in agent.authority.escalation_path:
                if esc_id not in self._agent_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Agent '{agent.id}' escalation_path references unknown agent '{esc_id}'",
                        f"agents.{agent.id}.authority.escalation_path",
                    ))

    def _check_capability_references(self) -> None:
        for cap in self.ir.capabilities:
            for req_id in cap.requires:
                if req_id not in self._capability_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Capability '{cap.id}' requires unknown capability '{req_id}'",
                        f"capabilities.{cap.id}.requires",
                    ))
            for prov_id in cap.provides:
                if prov_id not in self._capability_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Capability '{cap.id}' provides unknown capability '{prov_id}'",
                        f"capabilities.{cap.id}.provides",
                    ))

    def _check_workflow_consistency(self) -> None:
        for wf in self.ir.workflows:
            stage_ids = {s.id for s in wf.stages}
            for stage in wf.stages:
                for dep_id in stage.depends_on:
                    if dep_id not in stage_ids:
                        self.errors.append(ValidationError(
                            "MISSING_DEPENDENCY",
                            f"Workflow '{wf.id}' stage '{stage.id}' depends on unknown stage '{dep_id}'",
                            f"workflows.{wf.id}.stages.{stage.id}.depends_on",
                        ))
            self._check_dag(wf)

    def _check_dag(self, wf: Any) -> None:
        stages = wf.stages
        stage_map = {s.id: s for s in stages}
        visited: set[str] = set()
        temp: set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in temp:
                self.errors.append(ValidationError(
                    "CIRCULAR_DEPENDENCY",
                    f"Workflow '{wf.id}' has circular dependency at stage '{node_id}'",
                    f"workflows.{wf.id}",
                ))
                return
            if node_id in visited:
                return
            temp.add(node_id)
            if node_id in stage_map:
                for dep_id in stage_map[node_id].depends_on:
                    visit(dep_id)
            temp.remove(node_id)
            visited.add(node_id)

        for stage in stages:
            if stage.id not in visited:
                visit(stage.id)

    def _check_route_consistency(self) -> None:
        for route in self.ir.routes:
            if route.selected_agent and route.selected_agent not in self._agent_ids:
                self.errors.append(ValidationError(
                    "UNRESOLVED_REFERENCE",
                    f"Route '{route.id}' references unknown agent '{route.selected_agent}'",
                    f"routes.{route.id}.selected_agent",
                ))
            for kb_id in route.selected_knowledge:
                if kb_id not in self._knowledge_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Route '{route.id}' references unknown knowledge '{kb_id}'",
                        f"routes.{route.id}.selected_knowledge",
                    ))
            for kb_id in route.expanded_knowledge:
                if kb_id not in self._knowledge_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Route '{route.id}' expanded knowledge references unknown '{kb_id}'",
                        f"routes.{route.id}.expanded_knowledge",
                    ))

    def _check_contract_integrity(self) -> None:
        valid_ids = self._agent_ids | self._capability_ids
        for contract in self.ir.contracts:
            for party in contract.parties:
                if party.id not in valid_ids:
                    self.errors.append(ValidationError(
                        "UNRESOLVED_REFERENCE",
                        f"Contract '{contract.id}' party references unknown '{party.id}'",
                        f"contracts.{contract.id}.parties",
                    ))

    def is_valid(self) -> bool:
        return len(self.errors) == 0
