from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class AgentProfile:
    """Tool-agnostic agent profile representation."""
    id: str
    name: str
    display_name: str
    description: str
    role: str

    domains: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    workflows: List[str] = field(default_factory=list)
    blueprints: List[str] = field(default_factory=list)

    bundles: List[str] = field(default_factory=list)

    permissions: Dict[str, Any] = field(default_factory=dict)
    behavior: Dict[str, Any] = field(default_factory=dict)
    authority: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "role": self.role,
            "domains": self.domains,
            "skills": self.skills,
            "workflows": self.workflows,
            "blueprints": self.blueprints,
            "bundles": self.bundles,
            "permissions": self.permissions,
            "behavior": self.behavior,
            "authority": self.authority
        }


@dataclass
class Bundle:
    """Tool-agnostic bundle representation."""
    id: str
    name: str
    description: str
    skills: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "skills": self.skills
        }


@dataclass
class RuntimeIR:
    """
    Final IR consumed by emitters.
    Tool-neutral representation for agent systems.
    """
    version: str = "2.0"
    generated_at: str = ""

    knowledge: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    bundles: Dict[str, Bundle] = field(default_factory=dict)
    agents: Dict[str, AgentProfile] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bundles_dict = {k: (v.to_dict() if isinstance(v, Bundle) else v) for k, v in self.bundles.items()}
        agents_dict = {k: (v.to_dict() if isinstance(v, AgentProfile) else v) for k, v in self.agents.items()}
        return {
            "version": self.version,
            "generated_at": self.generated_at,
            "knowledge": self.knowledge,
            "bundles": bundles_dict,
            "agents": agents_dict
        }