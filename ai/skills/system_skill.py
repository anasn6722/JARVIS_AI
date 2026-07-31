from ai.skills.base_skill import BaseSkill


class SystemSkill(BaseSkill):

    def __init__(self, brain):
        self.brain = brain

    def can_handle(self, intent):
        print("SystemSkill checking:", intent)

        return intent in (
            "hello",
            "identity",
            "time",
            "open",
            "search",
            "youtube",
            "set_name",
            "get_name",
            "history",
            "last_message",
            "add_goal",
            "show_goals",
        )

    def execute(self, command):

        return self.brain.registry.execute(
            command.intent,
            command,
        )