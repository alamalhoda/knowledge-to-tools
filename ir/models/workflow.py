from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass(frozen=True)
class Stage:
    id: str = ""
    name: str = ""
    agent: str = ""
    depends_on: List[str] = field(default_factory=list)
    required_knowledge: List[str] = field(default_factory=list)
    required_capabilities: List[str] = field(default_factory=list)
    status: str = "pending"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "agent": self.agent,
            "depends_on": list(self.depends_on),
            "required_knowledge": list(self.required_knowledge),
            "required_capabilities": list(self.required_capabilities),
            "status": self.status,
        }


@dataclass(frozen=True)
class WorkflowIR:
    type: str = "workflow_ir"
    id: str = ""
    name: str = ""
    description: str = ""
    domain: str = ""
    category: str = ""
    stages: List[Stage] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    agents: List[str] = field(default_factory=list)
    capabilities_required: List[str] = field(default_factory=list)
    priority: int = 50
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "type": self.type,
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "domain": self.domain,
            "category": self.category,
            "stages": [s.to_dict() for s in self.stages],
            "triggers": list(self.triggers),
            "agents": list(self.agents),
            "capabilities_required": list(self.capabilities_required),
            "priority": self.priority,
        }
        if self.tags:
            d["tags"] = list(self.tags)
        if self.metadata:
            d["metadata"] = dict(self.metadata)
        return d
