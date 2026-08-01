from ai.conversation.context import Context


class ConversationMemory:

    def __init__(self):

        self.context = Context()


    def remember_app(self, app):

        self.context.last_app = app


    def forget_app(self, app):

        if self.context.last_app == app:
            self.context.last_app = None


    def remember_website(self, website):

        self.context.last_website = website


    def forget_website(self, website):

        if self.context.last_website == website:
            self.context.last_website = None


    def remember_search(self, query):

        self.context.last_search = query


    def clear(self):

        self.context.last_app = None
        self.context.last_website = None
        self.context.last_search = None


    def get_last_app(self):

        return self.context.last_app


    def get_last_website(self):

        return self.context.last_website


    def get_last_search(self):

        return self.context.last_search