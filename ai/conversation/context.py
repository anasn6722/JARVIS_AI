class Context:

    def __init__(self):

        self.last_app = None
        self.last_website = None
        self.last_search = None
        self.last_file = None
        self.last_person = None

    def clear(self):

        self.last_app = None
        self.last_website = None
        self.last_search = None
        self.last_file = None
        self.last_person = None