from ai.knowledge.models.knowledge_result import KnowledgeResult
from ai.knowledge.sources.base import KnowledgeSource


class DummySource(KnowledgeSource):

    @property
    def name(self):

        return "Dummy"

    def search(self, query):

        return KnowledgeResult(

            success=True,

            source="Dummy",

            query=query,

            content=f"I found information about '{query}'.",
        )