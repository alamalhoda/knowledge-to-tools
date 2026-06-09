from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass(frozen=True)
class Condition:
    field: str = ""
    operator: str = "eq"
    value: Any = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field": self.field,
            "operator": self.operator,
            "value": self.value,
        }


@dataclass(frozen=True)
class Party:
    id: str = ""
    role: str = "grantee"
    permissions: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "permissions": dict(self.permissions),
        }


@dataclass(frozen=True)
class ContractIR:
    type: str = "contract_ir"
    id: str = ""
    name: str = ""
    description: str = ""
    domain: str = ""
    parties: List[Party] = field(default_factory=list)
    conditions: List[Condition] = field(default_factory=list)
    expires_at: Optional[str] = None
    priority: int = 50
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "type": self.type,
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "domain": self.domain,
            "parties": [p.to_dict() for p in self.parties],
            "conditions": [c.to_dict() for c in self.conditions],
            "priority": self.priority,
        }
        if self.expires_at is not None:
            d["expires_at"] = self.expires_at
        if self.metadata:
            d["metadata"] = dict(self.metadata)
        return d
