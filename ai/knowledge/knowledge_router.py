class KnowledgeRouter:

    def __init__(self, registry):
        self.registry = registry

    def route(self, query):

        return self.registry.all()