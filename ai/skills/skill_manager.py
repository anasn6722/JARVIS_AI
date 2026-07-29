class SkillManager:

    def __init__(self):
        self.skills = []

    def register(self, skill):
        self.skills.append(skill)

    def execute(self, intent, command):
        print("SkillManager received:", intent)

        for skill in self.skills:
            print("Checking:", type(skill).__name__)

            if skill.can_handle(intent):
                print("Handled by:", type(skill).__name__)
                return skill.execute(intent, command)

        print("No skill handled:", intent)
        return None