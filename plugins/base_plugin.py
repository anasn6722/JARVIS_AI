class BasePlugin:
    """
    Base class for every JARVIS plugin.
    """

    name = ""

    def can_handle(self, command: str) -> bool:
        return False

    def execute(self, command: str):
        return None