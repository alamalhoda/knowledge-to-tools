from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass(frozen=True)
class Content:
    raw: str
    summary: str
    key_points: List[str] = field(default_factory=list)
    sections: List[str] = field(default_factory=list)
    code_blocks: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Activation:
    file_patterns: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class KnowledgeIR:
    type: str = "knowledge_ir"
    id: str = ""
    source: str = ""
    domain: str = ""
    category: str = ""
    kind: str = ""
    content: Content | None = None
    activation: Activation | None = None
    tags: List[str] = field(default_factory=list)
    priority: int = 50
    status: str = "active"
    applies_to: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    related: List[str] = field(default_factory=list)
    checksum: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "type": self.type,
            "id": self.id,
            "source": self.source,
            "domain": self.domain,
            "category": self.category,
            "kind": self.kind,
            "content": {
                "raw": self.content.raw if self.content else "",
                "summary": self.content.summary if self.content else "",
                "key_points": list(self.content.key_points) if self.content else [],
                "sections": list(self.content.sections) if self.content else [],
                "code_blocks": list(self.content.code_blocks) if self.content else [],
            },
            "activation": {
                "file_patterns": list(self.activation.file_patterns) if self.activation else [],
                "keywords": list(self.activation.keywords) if self.activation else [],
            },
            "priority": self.priority,
            "status": self.status,
            "applies_to": list(self.applies_to),
            "depends_on": list(self.depends_on),
            "related": list(self.related),
            "relationships": {
                "depends_on": list(self.depends_on),
                "related": list(self.related),
            },
        }
        if self.tags:
            d["tags"] = list(self.tags)
        if self.checksum:
            d["checksum"] = self.checksum
        return d
