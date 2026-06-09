from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass(frozen=True)
class RoutingContext:
    task: str = ""
    domain: Optional[str] = None
    intent: str = ""
    files: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "task": self.task,
            "intent": self.intent,
            "files": list(self.files),
        }
        if self.domain is not None:
            d["domain"] = self.domain
        if self.metadata:
            d["metadata"] = dict(self.metadata)
        return d


@dataclass(frozen=True)
class ContextPack:
    task: str = ""
    domain: Optional[str] = None
    files: List[str] = field(default_factory=list)
    knowledge_summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "task": self.task,
            "knowledge_summary": self.knowledge_summary,
            "files": list(self.files),
        }
        if self.domain is not None:
            d["domain"] = self.domain
        return d


@dataclass(frozen=True)
class RouteIR:
    type: str = "route_ir"
    id: str = ""
    context: RoutingContext = field(default_factory=RoutingContext)
    selected_agent: str = ""
    selected_knowledge: List[str] = field(default_factory=list)
    expanded_knowledge: List[str] = field(default_factory=list)
    confidence: float = 0.0
    context_pack: ContextPack | None = None
    match_reason: str = ""
    fallback_used: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "type": self.type,
            "id": self.id,
            "context": self.context.to_dict(),
            "selected_agent": self.selected_agent,
            "selected_knowledge": list(self.selected_knowledge),
            "expanded_knowledge": list(self.expanded_knowledge),
            "confidence": self.confidence,
            "match_reason": self.match_reason,
            "fallback_used": self.fallback_used,
        }
        if self.context_pack is not None:
            d["context_pack"] = self.context_pack.to_dict()
        return d
