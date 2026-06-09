from typing import Dict, List, Any, Optional
from datetime import datetime
from .models import AgentProfile, Bundle, RuntimeIR
from .bundler import BundleBuilder
from .skill_graph import SkillGraphBuilder


class AgentComposer:
    """
    Composes agents from knowledge and bundles.
    Tool-agnostic composition layer.
    """

    def __init__(self, knowledge_base: List[Dict[str, Any]], agents_config: Dict[str, Any]):
        self.knowledge = knowledge_base
        self.agents_config = agents_config
        self.graph_builder = SkillGraphBuilder(knowledge_base)

    def compose(self) -> RuntimeIR:
        """Compose full IR from knowledge and agents."""
        bundles = BundleBuilder(self.knowledge).build_bundles()

        ir = RuntimeIR(
            generated_at=datetime.utcnow().isoformat() + "Z",
            knowledge={k["id"]: k for k in self.knowledge},
            bundles=bundles
        )

        for agent_id, agent_config in self.agents_config.items():
            profile = self._create_agent_profile(agent_id, agent_config)
            ir.agents[agent_id] = profile

        return ir

    def _create_agent_profile(self, agent_id: str, config: Dict[str, Any]) -> AgentProfile:
        """Create agent profile from configuration."""
        matches = self.graph_builder.extract_skills_for_agent(config)

        return AgentProfile(
            id=agent_id,
            name=config.get("name", agent_id),
            display_name=config.get("display_name", agent_id),
            description=config.get("description", ""),
            role=config.get("role", ""),
            domains=config.get("knowledge", {}).get("domains", []),
            skills=matches.get("skills", []),
            workflows=matches.get("workflows", []),
            blueprints=matches.get("architecture", []),
            permissions=config.get("permissions", {}),
            behavior=config.get("behavior", {}),
            authority=config.get("authority", {})
        )