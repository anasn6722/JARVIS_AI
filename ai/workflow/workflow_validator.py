class WorkflowValidator:

    def __init__(self, brain):

        self.brain = brain

    def validate(self, task):

        action = task.action.lower()

        if action == "open":

            return self.validate_open(task)

        if action == "search":

            return self.validate_search(task)

        if action == "youtube":

            return self.validate_browser(task)

        return True