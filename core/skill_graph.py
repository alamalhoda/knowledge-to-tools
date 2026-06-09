from typing import Dict, List, Any, Set, Union


class SkillGraphBuilder:
    """
    Builds skill dependency graph - tool agnostic.
    Transforms knowledge documents into skill relationships.
    """

    def __init__(self, knowledge_base: Union[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]):
        if isinstance(knowledge_base, dict):
            self.knowledge = list(knowledge_base.values())
        else:
            self.knowledge = knowledge_base
        self._index = {k["id"]: k for k in self.knowledge}

    def extract_skills_for_agent(
        self,
        agent_meta: Dict[str, Any],
        include_shared: bool = True
    ) -> Dict[str, List[str]]:
        """
        Extract skills based on agent configuration.
        Returns categorized skills: architecture, workflows, skills.
        """
        allowed_domains = agent_meta.get("knowledge", {}).get("domains", [])
        agent_tags = set(agent_meta.get("knowledge", {}).get("tags", []))

        matches = {
            "architecture": [],
            "workflows": [],
            "skills": []
        }

        for k in self.knowledge:
            domain = k.get("domain")
            kind = k.get("kind")
            kid = k.get("id")

            if not kid:
                continue

            k_tags = set(k.get("tags", []))

            domain_match = domain in allowed_domains
            shared_match = domain == "shared" and include_shared
            tag_match = bool(agent_tags.intersection(k_tags))

            if domain_match or shared_match or tag_match:
                if kind == "architecture":
                    matches["architecture"].append(kid)
                elif kind == "workflow":
                    matches["workflows"].append(kid)
                else:
                    matches["skills"].append(kid)

        return matches

    def build_dependency_graph(self) -> Dict[str, Set[str]]:
        """Build global dependency graph from all knowledge documents."""
        graph: Dict[str, Set[str]] = {}

        for doc in self.knowledge:
            doc_id = doc.get("id")
            deps = set(doc.get("relationships", {}).get("depends_on", []))
            related = set(doc.get("relationships", {}).get("related", []))
            graph[doc_id] = deps | related

        return graph

    def get_bundle_skills(self, bundle_ids: List[str]) -> Dict[str, List[str]]:
        """
        Get all skills for a bundle of knowledge IDs.
        Expands transitive dependencies.
        """
        all_ids = set(bundle_ids)
        to_process = list(bundle_ids)

        while to_process:
            current = to_process.pop()
            if current in self._index:
                doc = self._index[current]
                for dep in doc.get("relationships", {}).get("depends_on", []):
                    if dep not in all_ids and dep in self._index:
                        all_ids.add(dep)
                        to_process.append(dep)

        matches = {
            "architecture": [],
            "workflows": [],
            "skills": []
        }

        for doc_id in all_ids:
            if doc_id in self._index:
                doc = self._index[doc_id]
                kind = doc.get("kind")
                if kind == "architecture":
                    matches["architecture"].append(doc_id)
                elif kind == "workflow":
                    matches["workflows"].append(doc_id)
                else:
                    matches["skills"].append(doc_id)

        return matches