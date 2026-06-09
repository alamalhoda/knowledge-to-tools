from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass(frozen=True)
class Permissions:
    shell: bool = False
    edit: bool = True
    read: bool = True
    network: bool = False
    planning: str = "optional"
    review: str = "optional"
    testing: str = "optional"


@dataclass(frozen=True)
class Behavior:
    planning: str = "optional"
    testing: str = "optional"
    review_style: str = "balanced"
    response_format: str = "detailed"


@dataclass(frozen=True)
class Authority:
    level: str = "mid"
    can_delegate: bool = False
    escalation_path: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Routing:
    priority: int = 0
    match_domains: List[str] = field(default_factory=list)
    match_patterns: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class AgentIR:
    type: str = "agent_ir"
    id: str = ""
    name: str = ""
    display_name: str = ""
    description: str = ""
    role: str = ""
    domains: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    workflows: List[str] = field(default_factory=list)
    blueprints: List[str] = field(default_factory=list)
    bundles: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    permissions: Permissions = field(default_factory=Permissions)
    behavior: Behavior = field(default_factory=Behavior)
    authority: Authority = field(default_factory=Authority)
    routing: Routing = field(default_factory=Routing)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "type": self.type,
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "role": self.role,
            "domains": list(self.domains),
            "skills": list(self.skills),
            "workflows": list(self.workflows),
            "blueprints": list(self.blueprints),
            "bundles": list(self.bundles),
            "capabilities": list(self.capabilities),
            "permissions": {
                "shell": self.permissions.shell,
                "edit": self.permissions.edit,
                "read": self.permissions.read,
                "network": self.permissions.network,
                "planning": self.permissions.planning,
                "review": self.permissions.review,
                "testing": self.permissions.testing,
            },
            "behavior": {
                "planning": self.behavior.planning,
                "testing": self.behavior.testing,
                "review_style": self.behavior.review_style,
                "response_format": self.behavior.response_format,
            },
            "authority": {
                "level": self.authority.level,
                "can_delegate": self.authority.can_delegate,
                "escalation_path": list(self.authority.escalation_path),
            },
            "routing": {
                "priority": self.routing.priority,
                "match_domains": list(self.routing.match_domains),
                "match_patterns": list(self.routing.match_patterns),
            },
        }
        if self.metadata:
            d["metadata"] = dict(self.metadata)
        return d
