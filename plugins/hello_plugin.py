from plugins.base_plugin import BasePlugin


class HelloPlugin(BasePlugin):

    name = "hello"

    def can_handle(self, command: str):
        return command in (
            "hello",
            "hi",
            "hey",
        )

    def execute(self, command: str):
        return "Hello Anas! 👋"