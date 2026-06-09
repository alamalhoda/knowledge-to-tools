from typing import Dict, List, Any
from .skill_graph import SkillGraphBuilder
from .models import Bundle


class BundleBuilder:
    """
    Bundle construction - shared across all emitters.
    Groups skills into logical bundles for agent composition.
    """

    BUNDLE_CATEGORIES = {
        "engineering-foundation": {
            "name": "Engineering Foundation",
            "description": "Core engineering principles and practices",
            "domains": ["shared"],
            "kinds": ["principle", "policy", "rule"]
        },
        "backend-foundation": {
            "name": "Backend Foundation",
            "description": "Backend development essentials",
            "domains": ["backend"],
            "kinds": ["architecture", "rule", "skill", "reference"]
        },
        "frontend-foundation": {
            "name": "Frontend Foundation",
            "description": "Frontend development essentials",
            "domains": ["frontend"],
            "kinds": ["architecture", "rule", "skill", "reference"]
        }
    }

    def __init__(self, knowledge_base: List[Dict[str, Any]]):
        self.knowledge = knowledge_base
        self.graph_builder = SkillGraphBuilder(knowledge_base)

    def build_bundles(self) -> Dict[str, Bundle]:
        """Build all standard bundles as Bundle objects."""
        bundles = {}

        for bundle_id, bundle_meta in self.BUNDLE_CATEGORIES.items():
            skills = self._filter_by_criteria(
                bundle_meta["domains"],
                bundle_meta["kinds"]
            )

            bundles[bundle_id] = Bundle(
                id=bundle_id,
                name=bundle_meta["name"],
                description=bundle_meta["description"],
                skills=skills
            )

        return bundles

    def _filter_by_criteria(
        self,
        domains: List[str],
        kinds: List[str]
    ) -> List[str]:
        """Filter knowledge by domain and kind criteria."""
        result = []
        for doc in self.knowledge:
            domain = doc.get("domain")
            kind = doc.get("kind")
            doc_id = doc.get("id")

            if domain in domains and kind in kinds:
                result.append(doc_id)

        return sorted(result)