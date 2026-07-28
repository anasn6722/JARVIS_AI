class PluginDispatcher:

    def __init__(self):
        self.routes = {}

    def register(self, intent, plugin):

        self.routes[intent] = plugin

    def get_plugin(self, intent):

        return self.routes.get(intent)