from ai.knowledge.models.knowledge_result import KnowledgeResult
from ai.knowledge.sources.base import KnowledgeSource


class MemorySource(KnowledgeSource):

    def __init__(self, memory):
        self.memory = memory

    @property
    def name(self):
        return "Memory"

    def search(self, query):

        try:

            result = self.memory.search(query)

            if not result:
                return KnowledgeResult(
                    success=False,
                    source=self.name,
                    query=query,
                    content="",
                    confidence=0.0,
                )

            return KnowledgeResult(
                success=True,
                source=self.name,
                query=query,
                content=result,
                confidence=1.0,
            )

        except Exception:

            return KnowledgeResult(
                success=False,
                source=self.name,
                query=query,
                content="",
                confidence=0.0,
            )