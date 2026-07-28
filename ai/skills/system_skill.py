from ai.skills.base_skill import BaseSkill


class SystemSkill(BaseSkill):

    def __init__(self, brain):
        self.brain = brain

    def can_handle(self, intent):

        return intent in (
            "hello",
            "identity",
            "time",
            "open",
        )

    def execute(self, intent, command):

        return self.brain.registry.execute(
            intent,
            command,
        )