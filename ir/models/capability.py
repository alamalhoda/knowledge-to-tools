from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass(frozen=True)
class CapabilityIR:
    type: str = "capability_ir"
    id: str = ""
    name: str = ""
    description: str = ""
    domain: str = ""
    category: str = ""
    tags: List[str] = field(default_factory=list)
    requires: List[str] = field(default_factory=list)
    provides: List[str] = field(default_factory=list)
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
            "requires": list(self.requires),
            "provides": list(self.provides),
            "priority": self.priority,
        }
        if self.tags:
            d["tags"] = list(self.tags)
        if self.metadata:
            d["metadata"] = dict(self.metadata)
        return d
