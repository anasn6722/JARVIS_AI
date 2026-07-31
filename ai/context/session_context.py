class SessionContext:

    def __init__(self):
        self.last_app = None
        self.last_website = None
        self.last_search = None
        self.last_person = None

    def remember_app(self, app):
        print("Remembering:", app)
        self.last_app = app
        
    def remember_website(self, site):
        self.last_website = site

    def remember_search(self, query):
        self.last_search = query

    def clear(self):
        self.last_app = None
        self.last_website = None
        self.last_search = None
        self.last_person = None