class SkillManager:

    def __init__(self):
        self.skills = []

    def register(self, skill):

        self.skills.append(skill)

    def execute(self, intent, command):

        for skill in self.skills:

            if skill.can_handle(intent):
                return skill.execute(
                    intent,
                    command,
                )

        return None