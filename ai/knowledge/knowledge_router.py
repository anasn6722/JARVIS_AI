from ai.knowledge.models.knowledge_result import KnowledgeResult


class KnowledgeRouter:
    """Routes queries through registered knowledge sources."""

    def __init__(self, registry):
        self.registry = registry

    def search(self, query):
        """Search registered knowledge sources."""

        if not query:
            return KnowledgeResult(
                success=False,
                source="KnowledgeRouter",
                query="",
                content="",
                confidence=0.0,
            )

        best_result = None

        for source in self.registry.all():

            try:
                result = source.search(query)

                if not result.success:
                    continue

                if (
                    best_result is None
                    or result.confidence
                    > best_result.confidence
                ):
                    best_result = result

            except Exception as error:
                print("=" * 60)
                print("KNOWLEDGE SOURCE ERROR")
                print("SOURCE:", source.name)
                print("ERROR:", error)
                print("=" * 60)

        if best_result is not None:
            return best_result

        return KnowledgeResult(
            success=False,
            source="KnowledgeRouter",
            query=query,
            content="",
            confidence=0.0,
        )

    def route(self, query):
        """Backward-compatible alias for search()."""

        return self.search(query)