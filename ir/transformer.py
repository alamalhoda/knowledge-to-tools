import json
import re
from pathlib import Path
from typing import Dict, List, Any


class IRTransformer:
    def __init__(self, knowledge_index: Dict[str, Any], agents: Dict[str, Any]) -> None:
        self.index = knowledge_index
        self.agents = agents
        self.knowledge_root = Path("knowledge")

    def to_knowledge_ir(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        source_path = self.knowledge_root / Path(doc["path"]).relative_to("knowledge")
        raw = source_path.read_text(encoding="utf-8") if source_path.exists() else doc.get("title", "")

        return {
            "type": "knowledge_ir",
            "id": doc["id"],
            "source": doc["path"],
            "domain": doc["domain"],
            "category": doc["category"],
            "kind": doc["kind"],
            "content": {
                "raw": raw[:3000],
                "summary": doc.get("title", ""),
                "key_points": self._extract_key_points(raw),
                "sections": self._parse_sections(raw),
                "code_blocks": self._extract_code_blocks(raw)
            },
            "activation": {
                "file_patterns": doc.get("applies_to", []),
                "keywords": self._extract_keywords(doc.get("title", "") + " " + raw[:500])
            },
            "priority": doc.get("priority", 50),
            "relationships": {
                "depends_on": doc.get("depends_on", []),
                "related": doc.get("related", [])
            }
        }

    def transform_all(self) -> Dict[str, Any]:
        ir: Dict[str, Any] = {
            "version": 2,
            "generated_at": "2026-06-07T23:00:00Z",
            "knowledge": [self.to_knowledge_ir(d) for d in self.index["documents"]],
            "agents": self._transform_agents()
        }
        return ir

    def _transform_agents(self) -> Dict[str, Any]:
        return {
            name: {
                "type": "agent_ir",
                "id": name,
                **agent
            } for name, agent in self.agents.items()
        }

    def _extract_key_points(self, text: str) -> List[str]:
        return [line.strip() for line in text.split("\n")
                if line.strip().startswith(("- ", "✅", "❌", "**"))][:15]

    def _parse_sections(self, text: str) -> List[str]:
        return [line.strip() for line in text.split("\n") if line.strip().startswith("#")]

    def _extract_code_blocks(self, text: str) -> List[str]:
        return re.findall(r'```(?:python|json|bash)?\n(.*?)\n```', text, re.DOTALL)[:8]

    def _extract_keywords(self, text: str) -> List[str]:
        words = set(word.lower() for word in text.split() if len(word) > 3)
        return list(words)[:20]