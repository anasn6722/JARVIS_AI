class SourceRegistry:

    def __init__(self):

        self.sources = []

    def register(self, source):

        self.sources.append(source)

    def all(self):

        return self.sources