import fnmatch
from typing import Dict, List, Any, Optional


KIND_WEIGHT: Dict[str, int] = {
    "architecture": 45,
    "rule": 35,
    "policy": 30,
    "principle": 25,
    "workflow": 25,
    "skill": 20,
    "reference": 10
}


class RoutingContext:
    def __init__(
        self,
        task: str,
        files: Optional[List[str]] = None,
        domain: Optional[str] = None,
        intent: Optional[str] = None
    ):
        self.task = task
        self.files = files or []
        self.domain = domain
        self.intent = (intent or task).lower()


class KnowledgeResolver:
    """Shared knowledge resolution engine - tool agnostic."""

    def __init__(self, knowledge_base: List[Dict[str, Any]], agents: Dict[str, Any]):
        self.knowledge = knowledge_base
        self.agents = agents

    def score_knowledge(self, doc: Dict[str, Any], context: RoutingContext) -> float:
        score = 0.0

        if doc.get("domain") == context.domain:
            score += 40

        for pattern in doc.get("activation", {}).get("file_patterns", []):
            if any(fnmatch.fnmatch(f, pattern) for f in context.files):
                score += 50

        score += KIND_WEIGHT.get(doc.get("kind"), 0)
        score += doc.get("priority", 0)

        keywords = doc.get("activation", {}).get("keywords", [])
        if context.intent:
            score += sum(15 for kw in keywords if kw in context.intent)

        return score

    def expand_dependencies(self, selected: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ids = {s["id"] for s in selected}
        expanded = list(selected)
        for s in list(selected):
            for dep in s.get("relationships", {}).get("depends_on", []):
                dep_doc = next((d for d in self.knowledge if d["id"] == dep), None)
                if dep_doc and dep_doc["id"] not in ids:
                    expanded.append(dep_doc)
                    ids.add(dep_doc["id"])
        return expanded

    def match_agent(self, context: RoutingContext) -> Optional[Dict[str, Any]]:
        best: Optional[Dict[str, Any]] = None
        best_score = -1

        for agent in self.agents.values():
            score = 0
            domains = agent.get("knowledge", {}).get("domains", [])
            if context.domain in domains or any(d in domains for d in ["shared", context.domain]):
                score += 60
            score += agent.get("routing", {}).get("priority", 0) * 1.5

            if score > best_score:
                best_score = score
                best = agent
        return best or (list(self.agents.values())[0] if self.agents else None)

    def resolve(self, context: RoutingContext) -> Dict[str, Any]:
        ranked = sorted(
            self.knowledge,
            key=lambda d: self.score_knowledge(d, context),
            reverse=True
        )
        selected = ranked[:10]
        selected = self.expand_dependencies(selected)

        agent = self.match_agent(context)

        return {
            "agent": agent["id"] if agent else None,
            "knowledge": [s["id"] for s in selected],
            "confidence": round(min(0.98, len(selected) / 12), 2),
            "context_pack": {
                "task": context.task,
                "domain": context.domain,
                "files": context.files[:5]
            }
        }