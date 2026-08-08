
from ai.tools.tool import Tool


class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(
        self,
        name,
        description,
        callback,
    ):
        self.tools[name] = Tool(
            name=name,
            description=description,
            callback=callback,
        )

    def get(self, name):
        return self.tools.get(name)

    def has(self, name):
        return name in self.tools

    def all(self):
        return self.tools
