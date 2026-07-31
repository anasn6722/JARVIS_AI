class TaskExecutor:

    def __init__(self, brain):
        self.brain = brain

    def execute(self, tasks):

        responses = []

        for task in tasks:

            if task.action == "open":
                responses.append(
                    self.brain.handle_open_task(task.target)
                )

            elif task.action == "search":
                responses.append(
                    self.brain.handle_search_task(task.target)
                )

            elif task.action == "time":
                responses.append(
                    self.brain.handle_time(None)
                )

        return responses