class ReasoningEngine:

    def __init__(self, brain):
        self.brain = brain

    def analyze(self, command):

        entities = command.entities

        return {
            "intent": command.intent,
            "goal": (entities.get("goals") or [None])[0],
            "app": (entities.get("apps") or [None])[0],
            "website": (entities.get("websites") or [None])[0],
            "search": (entities.get("searches") or [None])[0],
            "command": command.original,
        }