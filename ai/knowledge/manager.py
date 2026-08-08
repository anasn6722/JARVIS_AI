
class KnowledgeManager:
    """Coordinates knowledge sources through the source router."""

    def __init__(self, router):
        self.router = router

    def search(self, query):
        """Search available knowledge sources."""

        if not query:
            return None

        return self.router.search(query)
