class ContextManager:

    def __init__(self):

        self.last_intent = None

        self.last_command = None

        self.last_app = None

        self.last_website = None

        self.last_search = None

        self.last_topic = None

        self.last_person = None

    def update(
        self,
        intent=None,
        command=None,
        app=None,
        website=None,
        search=None,
        topic=None,
        person=None,
    ):

        if intent is not None:
            self.last_intent = intent

        if command is not None:
            self.last_command = command

        if app is not None:
            self.last_app = app

        if website is not None:
            self.last_website = website

        if search is not None:
            self.last_search = search

        if topic is not None:
            self.last_topic = topic

        if person is not None:
            self.last_person = person

    def clear(self):

        self.__init__()