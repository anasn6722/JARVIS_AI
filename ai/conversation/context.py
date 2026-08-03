class Context:

    def __init__(self):

        # Conversation
        self.last_response = None

        # Goals
        self.current_goal = None
        self.current_task = None
        self.current_lesson = None

        # Opened things
        self.last_app = None
        self.last_website = None
        self.last_search = None
        self.last_file = None
        self.last_person = None

    def clear(self):

        self.last_response = None

        self.current_goal = None
        self.current_task = None
        self.current_lesson = None

        self.last_app = None
        self.last_website = None
        self.last_search = None
        self.last_file = None
        self.last_person = None