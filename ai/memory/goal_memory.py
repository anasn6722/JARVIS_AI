class GoalMemory:

    def __init__(self):

        self.goals = {}

    def add(self, goal):

        self.goals[goal.id] = goal

    def get(self, goal_id):

        return self.goals.get(goal_id)

    def all(self):

        return list(self.goals.values())

    def remove(self, goal_id):

        self.goals.pop(goal_id, None)

    def clear(self):

        self.goals.clear()