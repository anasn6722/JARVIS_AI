from memory.database import Database


class ContextManager:

    def __init__(self):

        self.db = Database()
        # ==================================================
        # Previous Interaction
        # ==================================================

        self.last_intent = None
        self.last_command = None
        self.last_response = None

        # ==================================================
        # Current Focus
        # ==================================================

        self.current_goal = self.db.get_context("current_goal")
        self.current_task = self.db.get_context("current_task")
        self.current_topic = self.db.get_context("current_topic")
        self.current_project = self.db.get_context("current_project")
        self.current_lesson = self.db.get_context("current_lesson")

        # ==================================================
        # Goal Tracking
        # ==================================================

        self.last_goal_action = None
        self.task_history = []

        # ==================================================
        # Applications
        # ==================================================

        self.last_app = self.db.get_context("last_app")
        self.last_website = self.db.get_context("last_website")
        self.last_file = self.db.get_context("last_file")

        # ==================================================
        # Search
        # ==================================================

        self.last_search = self.db.get_context("last_search")
        self.last_video = self.db.get_context("last_video")

        # ==================================================
        # Conversation
        # ==================================================

        self.last_person = self.db.get_context("last_person")


    def update(
        self,
        intent=None,
        command=None,
        response=None,
        goal=None,
        task=None,
        topic=None,
        project=None,
        lesson=None,
        goal_action=None,
        app=None,
        website=None,
        file=None,
        search=None,
        person=None,
    ):

        # Previous interaction
        if intent is not None:
            self.last_intent = intent

        if command is not None:
            self.last_command = command

        if response is not None:
            self.last_response = response

        # Current focus
        if goal is not None:
            self.current_goal = goal
            self.db.set_context("current_goal", goal)

        if task is not None:
            self.current_task = task
            self.db.set_context("current_task", task)
        if topic is not None:
            self.current_topic = topic
            self.db.set_context("current_topic", topic)

        if project is not None:
            self.current_project = project
            self.db.set_context("current_project", project)

        if lesson is not None:
            self.current_lesson = lesson
            self.db.set_context("current_lesson", lesson)

        if goal_action is not None:
            self.last_goal_action = goal_action

        # Applications
        if app is not None:
            self.last_app = app
            self.db.set_context("last_app", app)

        if website is not None:
            self.last_website = website
            self.db.set_context("last_website", website)

        if file is not None:
            self.last_file = file
            self.db.set_context("last_file", file)

        # Search
        if search is not None:
            self.last_search = search
            self.db.set_context("last_search", search)

        # Conversation
        if person is not None:
            self.last_person = person
            self.db.set_context("last_person", person)

    # ==================================================
    # Task History
    # ==================================================

    def add_task_history(self, task):

        if task not in self.task_history:
            self.task_history.append(task)

        if len(self.task_history) > 20:
            self.task_history.pop(0)

    # ==================================================
    # Reset Context
    # ==================================================

    def current(self):

        return {
            "goal": self.current_goal,
            "task": self.current_task,
            "topic": self.current_topic,
            "project": self.current_project,
            "lesson": self.current_lesson,
        }
    
    
    def has_goal(self):
        return self.current_goal is not None
    
    
    def has_task(self):
        return self.current_task is not None
    
    
    def has_app(self):
        return self.last_app is not None
    
    
    def has_search(self):
        return self.last_search is not None
    
    
    def has_person(self):
        return self.last_person is not None
    
    def clear(self):

        self.last_intent = None
        self.last_command = None
        self.last_response = None

        self.current_goal = None
        self.current_task = None
        self.current_topic = None
        self.current_project = None
        self.current_lesson = None

        self.last_goal_action = None
        self.task_history = []

        self.last_app = None
        self.last_website = None
        self.last_file = None

        self.last_search = None
        self.last_video = None

        self.last_person = None

        keys = [
            "current_goal",
            "current_task",
            "current_topic",
            "current_project",
            "current_lesson",
            "last_app",
            "last_website",
            "last_file",
            "last_search",
            "last_person",
        ]

        for key in keys:
            self.db.delete_context(key)