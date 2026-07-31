class ContextManager:

    def __init__(self):

        # Previous interaction
        self.last_intent = None
        self.last_command = None
        self.last_response = None

        # Current focus
        self.current_goal = None
        self.current_task = None
        self.current_topic = None

        # Applications & websites
        self.last_app = None
        self.last_website = None

        # Search information
        self.last_search = None
        self.last_video = None
        # Conversation
        self.last_person = None
        #new 
        self.last_tasks=[]

    def update(
        self,
        intent=None,
        command=None,
        response=None,
        goal=None,
        task=None,
        topic=None,
        app=None,
        website=None,
        search=None,
        person=None,
    ):

        if intent is not None:
            self.last_intent = intent

        if command is not None:
            self.last_command = command

        if response is not None:
            self.last_response = response

        if goal is not None:
            self.current_goal = goal

        if task is not None:
            self.current_task = task

        if topic is not None:
            self.current_topic = topic

        if app is not None:
            self.last_app = app

        if website is not None:
            self.last_website = website

        if search is not None:
            self.last_search = search

        if person is not None:
            self.last_person = person

    def clear(self):
        self.__init__()