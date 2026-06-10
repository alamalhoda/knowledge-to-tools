from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any

from .models.root import IRRoot
from .models.knowledge import KnowledgeIR
from .models.capability import CapabilityIR
from .models.agent import AgentIR
from .models.workflow import WorkflowIR
from .models.route import RouteIR
from .models.contracts import ContractIR


@dataclass(frozen=True)
class SerializedIRPayload:
    version: str = ""
    generated_at: str = ""
    source_hash: str = ""
    knowledge: List[Dict[str, Any]] = field(default_factory=list)
    capabilities: List[Dict[str, Any]] = field(default_factory=list)
    agents: Dict[str, Any] = field(default_factory=dict)
    workflows: List[Dict[str, Any]] = field(default_factory=list)
    routes: List[Dict[str, Any]] = field(default_factory=list)
    contracts: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_ir(cls, ir: IRRoot) -> SerializedIRPayload:
        return cls(
            version=ir.version,
            generated_at=ir.generated_at,
            source_hash=ir.source_hash,
            knowledge=[k.to_dict() for k in ir.knowledge],
            capabilities=[c.to_dict() for c in ir.capabilities],
            agents={a.id: a.to_dict() for a in ir.agents},
            workflows=[w.to_dict() for w in ir.workflows],
            routes=[r.to_dict() for r in ir.routes],
            contracts=[c.to_dict() for c in ir.contracts],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "generated_at": self.generated_at,
            "source_hash": self.source_hash,
            "knowledge": list(self.knowledge),
            "capabilities": list(self.capabilities),
            "agents": dict(self.agents),
            "workflows": list(self.workflows),
            "routes": list(self.routes),
            "contracts": list(self.contracts),
        }
