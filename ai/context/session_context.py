class SessionContext:

    def __init__(self):
        self.clear()

    # ------------------------
    # Applications
    # ------------------------

    def remember_app(self, app):
        print(f"Remembering app: {app}")

        self.last_app = app

        if app in self.open_apps:
            self.open_apps.remove(app)

        self.open_apps.append(app)

    def get_last_app(self):
        return self.last_app

    def get_previous_app(self):
        if len(self.open_apps) < 2:
            return None

        return self.open_apps[-2]

    def remove_last_app(self):
        if self.open_apps:
            self.open_apps.pop()

        self.last_app = self.open_apps[-1] if self.open_apps else None

    # ------------------------
    # Websites
    # ------------------------

    def remember_website(self, site):
        self.last_website = site

        if site in self.open_websites:
            self.open_websites.remove(site)

        self.open_websites.append(site)

    # ------------------------
    # Searches
    # ------------------------

    def remember_search(self, query):
        self.last_search = query
        self.search_history.append(query)

    # ------------------------
    # Conversation
    # ------------------------

    def remember_person(self, person):
        self.last_person = person

    def remember_topic(self, topic):
        self.current_topic = topic

    # ------------------------
    # Reset
    # ------------------------

    def clear(self):
        self.last_app = None
        self.last_website = None
        self.last_search = None
        self.last_person = None

        self.open_apps = []
        self.open_websites = []
        self.search_history = []

        self.current_topic = None
        self.current_goal = None