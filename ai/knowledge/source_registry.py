class SourceRegistry:


    def __init__(self):

        self.sources = {}


    def register(self, source):

        self.sources[source.name] = source



    def get(self, name):

        return self.sources.get(name)



    def all(self):

        return list(
            self.sources.values()
        )