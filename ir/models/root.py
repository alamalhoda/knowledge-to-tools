from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from .knowledge import KnowledgeIR
from .capability import CapabilityIR
from .agent import AgentIR
from .workflow import WorkflowIR
from .route import RouteIR
from .contracts import ContractIR


@dataclass(frozen=True)
class IRRoot:
    version: str = "2.0"
    generated_at: str = ""
    source_hash: str = ""
    knowledge: List[KnowledgeIR] = field(default_factory=list)
    capabilities: List[CapabilityIR] = field(default_factory=list)
    agents: List[AgentIR] = field(default_factory=list)
    workflows: List[WorkflowIR] = field(default_factory=list)
    routes: List[RouteIR] = field(default_factory=list)
    contracts: List[ContractIR] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "generated_at": self.generated_at,
            "source_hash": self.source_hash,
            "knowledge": [k.to_dict() for k in self.knowledge],
            "capabilities": [c.to_dict() for c in self.capabilities],
            "agents": {a.id: a.to_dict() for a in self.agents},
            "workflows": [w.to_dict() for w in self.workflows],
            "routes": [r.to_dict() for r in self.routes],
            "contracts": [c.to_dict() for c in self.contracts],
        }

    def knowledge_by_id(self) -> Dict[str, KnowledgeIR]:
        return {k.id: k for k in self.knowledge}

    def agent_by_id(self) -> Dict[str, AgentIR]:
        return {a.id: a for a in self.agents}

    def capability_by_id(self) -> Dict[str, CapabilityIR]:
        return {c.id: c for c in self.capabilities}

    def workflow_by_id(self) -> Dict[str, WorkflowIR]:
        return {w.id: w for w in self.workflows}
