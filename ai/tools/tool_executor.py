class ToolExecutor:

    def __init__(self, registry):
        self.registry = registry

    def execute(
        self,
        tool_name,
        argument,
    ):
        tool = self.registry.get(tool_name)

        if tool is None:
            print(f"Tool not found: {tool_name}")
            return None

        return tool.callback(argument)