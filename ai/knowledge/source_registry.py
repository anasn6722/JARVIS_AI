class SourceRegistry:
    """Registry for JARVIS knowledge sources."""

    def __init__(self):
        self.sources = {}

    def register(self, source):
        """Register a knowledge source."""
        self.sources[source.name] = source

    def get(self, name):
        """Get a source by name."""
        return self.sources.get(name)

    def all(self):
        """Return all registered knowledge sources."""
        return list(self.sources.values())

    def search(self, query):
        """Search all registered knowledge sources."""

        results = []

        for source in self.sources.values():
            try:
                result = source.search(query)

                if result:
                    results.append(result)

            except Exception as error:
                print(
                    f"Knowledge source failed: "
                    f"{source.name}: {error}"
                )

        return results