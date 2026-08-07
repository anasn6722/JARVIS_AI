from ai.knowledge.knowledge_result import KnowledgeResult


class KnowledgeManager:

    def __init__(self, registry):
        self.registry = registry

    def search(self, query):

        best_result = None

        for source in self.registry.all():

            try:

                result = source.search(query)

                if not result:
                    continue

                if result.success:
                    return result

                if best_result is None:
                    best_result = result

            except Exception as e:
                print(f"{source.__class__.__name__} failed:", e)

        return best_result or KnowledgeResult(
            success=False,
            source="",
            query=query,
            content="",
            confidence=0.0,
        )