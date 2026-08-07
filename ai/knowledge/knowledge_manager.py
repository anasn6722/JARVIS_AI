from ai.knowledge.knowledge_router import KnowledgeRouter


class KnowledgeManager:


    def __init__(self, registry):

        self.router = KnowledgeRouter(
            registry.all()
        )


    def search(self, query):

        return self.router.search(query)