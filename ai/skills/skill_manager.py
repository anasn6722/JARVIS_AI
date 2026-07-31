class SkillManager:

    def __init__(self):
        self.skills = []

    def register(self, skill):
        self.skills.append(skill)

    def execute(self, command):

        for skill in self.skills:

            if skill.can_handle(command.intent):
                return skill.execute(command)

        return None