from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from .models import (
    IRRoot,
    KnowledgeIR,
    Content,
    Activation,
    AgentIR,
    Permissions,
    Behavior,
    Authority,
    Routing,
    CapabilityIR,
    Stage,
    WorkflowIR,
    RouteIR,
    RoutingContext,
    ContextPack,
    ContractIR,
    Party,
    Condition,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _extract_key_points(text: str, max_items: int = 20) -> List[str]:
    return [line.strip() for line in text.split("\n")
            if line.strip().startswith(("- ", "✅", "❌", "**"))][:max_items]


def _parse_sections(text: str, max_items: int = 50) -> List[str]:
    return [line.strip() for line in text.split("\n") if line.strip().startswith("#")][:max_items]


def _extract_code_blocks(text: str, max_items: int = 10) -> List[str]:
    return re.findall(r'```(?:python|json|bash)?\n(.*?)\n```', text, re.DOTALL)[:max_items]


def _extract_keywords(text: str, max_items: int = 20) -> List[str]:
    words = set(word.lower() for word in text.split() if len(word) > 3)
    return list(words)[:max_items]


def _build_content(raw: str, summary: str) -> Content:
    return Content(
        raw=raw[:8000],
        summary=summary,
        key_points=_extract_key_points(raw),
        sections=_parse_sections(raw),
        code_blocks=_extract_code_blocks(raw),
    )


def _build_activation(doc: Dict[str, Any], raw: str) -> Activation:
    applies_to = doc.get("applies_to", [])
    title = doc.get("title", "")
    keywords = _extract_keywords(title + " " + raw[:500])
    return Activation(
        file_patterns=[str(p) for p in applies_to],
        keywords=keywords,
    )


class IRCompiler:
    """
    Compiles Knowledge Layer and Agent Layer inputs into a formal IRRoot.

    Responsibilities:
    - Load knowledge documents
    - Load agent definitions
    - Normalize data into typed IR models
    - Resolve relationships
    - Construct IRRoot

    Constraints:
    - Deterministic: identical inputs produce structurally identical IR
    - Side-effect free: no file I/O, no network calls
    - No emitter logic
    - No runtime orchestration
    - No CLI logic
    """

    def __init__(
        self,
        knowledge_index: Dict[str, Any],
        agents: Dict[str, Any],
        capabilities: Optional[Dict[str, Any]] = None,
        workflows: Optional[Dict[str, Any]] = None,
        routes: Optional[Dict[str, Any]] = None,
        contracts: Optional[Dict[str, Any]] = None,
        knowledge_raw: Optional[Dict[str, str]] = None,
    ) -> None:
        self.index = knowledge_index
        self.agents = agents
        self.capabilities = capabilities or {}
        self.workflows = workflows or {}
        self.routes = routes or {}
        self.contracts = contracts or {}
        self.knowledge_raw = knowledge_raw or {}

    def compile(self, source_hash: str = "") -> IRRoot:
        knowledge_nodes = self._compile_knowledge()
        capability_nodes = self._compile_capabilities()
        agent_nodes = self._compile_agents(knowledge_nodes, capability_nodes)
        workflow_nodes = self._compile_workflows(agent_nodes, capability_nodes, knowledge_nodes)
        route_nodes = self._compile_routes(agent_nodes, knowledge_nodes)
        contract_nodes = self._compile_contracts(agent_nodes, capability_nodes)

        return IRRoot(
            version="2.0",
            generated_at=_now_iso(),
            source_hash=source_hash,
            knowledge=knowledge_nodes,
            capabilities=capability_nodes,
            agents=agent_nodes,
            workflows=workflow_nodes,
            routes=route_nodes,
            contracts=contract_nodes,
        )

    def _compile_knowledge(self) -> List[KnowledgeIR]:
        nodes: List[KnowledgeIR] = []
        for doc in self.index.get("documents", []):
            raw = self.knowledge_raw.get(doc["id"], "")
            if not raw:
                raw = doc.get("content", {}).get("raw", "")

            summary = doc.get("title", doc.get("content", {}).get("summary", ""))
            content = _build_content(raw, summary)
            activation = _build_activation(doc, raw)

            node = KnowledgeIR(
                id=doc["id"],
                source=doc.get("path", ""),
                domain=doc.get("domain", "shared"),
                category=doc.get("category", "reference"),
                kind=doc.get("kind", "reference"),
                content=content,
                activation=activation,
                tags=[str(t) for t in doc.get("tags", [])],
                priority=int(doc.get("priority", 50)),
                status=str(doc.get("status", "active")),
                applies_to=[str(p) for p in doc.get("applies_to", [])],
                depends_on=[str(d) for d in doc.get("depends_on", [])],
                related=[str(r) for r in doc.get("related", [])],
                checksum=str(doc.get("checksum", "")),
            )
            nodes.append(node)

        nodes.sort(key=lambda n: (n.domain, n.category, -n.priority, n.id))
        return nodes

    def _compile_capabilities(self) -> List[CapabilityIR]:
        nodes: List[CapabilityIR] = []
        for cap_id, cap in self.capabilities.items():
            node = CapabilityIR(
                id=str(cap_id),
                name=str(cap.get("name", cap_id)),
                description=str(cap.get("description", "")),
                domain=str(cap.get("domain", "shared")),
                category=str(cap.get("category", "general")),
                tags=[str(t) for t in cap.get("tags", [])],
                requires=[str(r) for r in cap.get("requires", [])],
                provides=[str(p) for p in cap.get("provides", [])],
                priority=int(cap.get("priority", 50)),
                metadata=dict(cap.get("metadata", {})),
            )
            nodes.append(node)
        nodes.sort(key=lambda n: (n.domain, n.id))
        return nodes

    def _compile_agents(
        self,
        knowledge_nodes: List[KnowledgeIR],
        capability_nodes: List[CapabilityIR],
    ) -> List[AgentIR]:
        kb_by_id = {k.id: k for k in knowledge_nodes}
        cap_by_id = {c.id: c for c in capability_nodes}
        nodes: List[AgentIR] = []

        for agent_id, agent in self.agents.items():
            perms = agent.get("permissions", {})
            beh = agent.get("behavior", {})
            auth = agent.get("authority", {})
            rte = agent.get("routing", {})

            permissions = Permissions(
                shell=bool(perms.get("shell", False)),
                edit=bool(perms.get("edit", True)),
                read=bool(perms.get("read", True)),
                network=bool(perms.get("network", False)),
                planning=str(perms.get("planning", "optional")),
                review=str(perms.get("review", "optional")),
                testing=str(perms.get("testing", "optional")),
            )
            behavior = Behavior(
                planning=str(beh.get("planning", "optional")),
                testing=str(beh.get("testing", "optional")),
                review_style=str(beh.get("review_style", "balanced")),
                response_format=str(beh.get("response_format", "detailed")),
            )
            authority = Authority(
                level=str(auth.get("level", "mid")),
                can_delegate=bool(auth.get("can_delegate", False)),
                escalation_path=[str(e) for e in auth.get("escalation_path", [])],
            )
            routing = Routing(
                priority=int(rte.get("priority", 0)),
                match_domains=[str(d) for d in rte.get("match_domains", [])],
                match_patterns=[str(p) for p in rte.get("match_patterns", [])],
            )

            node = AgentIR(
                id=str(agent_id),
                name=str(agent.get("name", agent_id)),
                display_name=str(agent.get("display_name", agent_id)),
                description=str(agent.get("description", "")),
                role=str(agent.get("role", "")),
                domains=[str(d) for d in agent.get("knowledge", {}).get("domains", [])],
                skills=[str(s) for s in agent.get("skills", [])],
                workflows=[str(w) for w in agent.get("workflows", [])],
                blueprints=[str(b) for b in agent.get("blueprints", [])],
                bundles=[str(b) for b in agent.get("bundles", [])],
                capabilities=[str(c) for c in agent.get("capabilities", [])],
                permissions=permissions,
                behavior=behavior,
                authority=authority,
                routing=routing,
                metadata=dict(agent.get("metadata", {})),
            )
            nodes.append(node)

        nodes.sort(key=lambda n: n.id)
        return nodes

    def _compile_workflows(
        self,
        agent_nodes: List[AgentIR],
        capability_nodes: List[CapabilityIR],
        knowledge_nodes: List[KnowledgeIR],
    ) -> List[WorkflowIR]:
        agent_by_id = {a.id: a for a in agent_nodes}
        cap_by_id = {c.id: c for c in capability_nodes}
        kb_by_id = {k.id: k for k in knowledge_nodes}
        nodes: List[WorkflowIR] = []

        for wf_id, wf in self.workflows.items():
            stages = []
            for stage in wf.get("stages", []):
                stage_obj = Stage(
                    id=str(stage.get("id", "")),
                    name=str(stage.get("name", stage.get("id", ""))),
                    agent=str(stage.get("agent", "")),
                    depends_on=[str(d) for d in stage.get("depends_on", [])],
                    required_knowledge=[str(k) for k in stage.get("knowledge", stage.get("required_knowledge", []))],
                    required_capabilities=[str(c) for c in stage.get("required_capabilities", [])],
                    status=str(stage.get("status", "pending")),
                )
                stages.append(stage_obj)

            node = WorkflowIR(
                id=str(wf_id),
                name=str(wf.get("name", wf_id)),
                description=str(wf.get("description", "")),
                domain=str(wf.get("domain", "shared")),
                category=str(wf.get("category", "general")),
                stages=stages,
                tags=[str(t) for t in wf.get("tags", [])],
                triggers=[str(t) for t in wf.get("triggers", [])],
                agents=[str(a) for a in wf.get("agents", [])],
                capabilities_required=[str(c) for c in wf.get("capabilities_required", [])],
                priority=int(wf.get("priority", 50)),
                metadata=dict(wf.get("metadata", {})),
            )
            nodes.append(node)

        nodes.sort(key=lambda n: (n.domain, n.id))
        return nodes

    def _compile_routes(
        self,
        agent_nodes: List[AgentIR],
        knowledge_nodes: List[KnowledgeIR],
    ) -> List[RouteIR]:
        agent_by_id = {a.id: a for a in agent_nodes}
        kb_by_id = {k.id: k for k in knowledge_nodes}
        nodes: List[RouteIR] = []

        for route_id, route in self.routes.items():
            ctx = route.get("context", {})
            context = RoutingContext(
                task=str(ctx.get("task", "")),
                domain=ctx.get("domain"),
                intent=str(ctx.get("intent", ctx.get("task", ""))).lower(),
                files=[str(f) for f in ctx.get("files", [])],
                metadata=dict(ctx.get("metadata", {})),
            )
            cp = route.get("context_pack")
            context_pack = ContextPack(
                task=str(cp.get("task", "")) if cp else "",
                domain=cp.get("domain") if cp else None,
                files=[str(f) for f in cp.get("files", [])] if cp else [],
                knowledge_summary=str(cp.get("knowledge_summary", "")) if cp else "",
            ) if cp else None

            node = RouteIR(
                id=str(route_id),
                context=context,
                selected_agent=str(route.get("selected_agent", "")),
                selected_knowledge=[str(k) for k in route.get("selected_knowledge", [])],
                expanded_knowledge=[str(k) for k in route.get("expanded_knowledge", [])],
                confidence=float(route.get("confidence", 0.0)),
                context_pack=context_pack,
                match_reason=str(route.get("match_reason", "")),
                fallback_used=bool(route.get("fallback_used", False)),
            )
            nodes.append(node)

        nodes.sort(key=lambda n: n.id)
        return nodes

    def _compile_contracts(
        self,
        agent_nodes: List[AgentIR],
        capability_nodes: List[CapabilityIR],
    ) -> List[ContractIR]:
        valid_ids = {a.id for a in agent_nodes} | {c.id for c in capability_nodes}
        nodes: List[ContractIR] = []

        for contract_id, contract in self.contracts.items():
            parties = []
            for party in contract.get("parties", []):
                parties.append(Party(
                    id=str(party.get("id", "")),
                    role=str(party.get("role", "grantee")),
                    permissions=dict(party.get("permissions", {})),
                ))
            conditions = []
            for cond in contract.get("conditions", []):
                conditions.append(Condition(
                    field=str(cond.get("field", "")),
                    operator=str(cond.get("operator", "eq")),
                    value=cond.get("value"),
                ))

            node = ContractIR(
                id=str(contract_id),
                name=str(contract.get("name", contract_id)),
                description=str(contract.get("description", "")),
                domain=str(contract.get("domain", "shared")),
                parties=parties,
                conditions=conditions,
                expires_at=contract.get("expires_at"),
                priority=int(contract.get("priority", 50)),
                metadata=dict(contract.get("metadata", {})),
            )
            nodes.append(node)

        nodes.sort(key=lambda n: (n.domain, n.id))
        return nodes
