
class ToolExecutor:

    def __init__(self, registry):
        self.registry = registry

    def execute(
        self,
        tool_name,
        argument="",
    ):
        # ====================================================
        # FIND TOOL
        # ====================================================

        tool = self.registry.get(tool_name)

        if tool is None:
            print(
                f"Tool not found: {tool_name}"
            )
            return None

        # ====================================================
        # DEBUG
        # ====================================================

        print(
            f"Tool: {tool_name}",
            argument,
        )

        # ====================================================
        # TOOLS WITHOUT ARGUMENTS
        # ====================================================

        if tool_name == "close_last":

            return tool.callback()

        # ====================================================
        # NORMAL TOOLS
        # ====================================================

        return tool.callback(argument)
