class CommandRouter:
    def route(self, intent: str) -> str:
        """
        Decide which system should handle the request.
        """

        routes = {
            "OPEN_APP": "PLUGIN",
            "WEATHER": "PLUGIN",
            "TIME": "PLUGIN",
            "GREETING": "BRAIN",
            "CHAT": "AI",
        }

        return routes.get(intent, "AI")