class PlanningGraph:

    def __init__(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append(task)

    def all(self):
        return self.tasks

    def clear(self):
        self.tasks.clear()