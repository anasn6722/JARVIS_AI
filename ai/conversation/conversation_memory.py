
from ai.conversation.context import Context


class ConversationMemory:

    def __init__(self):

        self.context = Context()

    # ============================================================
    # APP MEMORY
    # ============================================================

    def remember_app(self, app):

        self.context.last_app = app
        self.context.last_reference = (
            "app",
            app,
        )

        print(f"🧠 Memory: app = {app}")
        print(
            f"🧠 Memory: reference = "
            f"{self.context.last_reference}"
        )

    def forget_app(self, app):

        if self.context.last_app == app:

            self.context.last_app = None

            if (
                self.context.last_reference
                and self.context.last_reference[0] == "app"
                and self.context.last_reference[1] == app
            ):
                self.context.last_reference = None

            print(f"🧠 Memory: removed app = {app}")

    # ============================================================
    # WEBSITE MEMORY
    # ============================================================

    def remember_website(self, website):

        self.context.last_website = website
        self.context.last_reference = (
            "website",
            website,
        )

        print(f"🧠 Memory: website = {website}")
        print(
            f"🧠 Memory: reference = "
            f"{self.context.last_reference}"
        )

    def forget_website(self, website):

        if self.context.last_website == website:

            self.context.last_website = None

            if (
                self.context.last_reference
                and self.context.last_reference[0] == "website"
                and self.context.last_reference[1] == website
            ):
                self.context.last_reference = None

            print(
                f"🧠 Memory: removed website = "
                f"{website}"
            )

    # ============================================================
    # SEARCH MEMORY
    # ============================================================

    def remember_search(self, query):

        self.context.last_search = query
        self.context.last_reference = (
            "search",
            query,
        )

        print(f"🧠 Memory: search = {query}")
        print(
            f"🧠 Memory: reference = "
            f"{self.context.last_reference}"
        )

    # ============================================================
    # CLEAR MEMORY
    # ============================================================

    def clear(self):

        self.context.last_app = None
        self.context.last_website = None
        self.context.last_search = None
        self.context.last_reference = None

        print("🧠 Memory cleared.")

    # ============================================================
    # GET LAST APP
    # ============================================================

    def get_last_app(self):

        return self.context.last_app

    # ============================================================
    # GET LAST WEBSITE
    # ============================================================

    def get_last_website(self):

        return self.context.last_website

    # ============================================================
    # GET LAST SEARCH
    # ============================================================

    def get_last_search(self):

        return self.context.last_search

    # ============================================================
    # GET LAST REFERENCE
    # ============================================================

    def get_last_reference(self):

        return self.context.last_reference

    # ============================================================
    # SHORTCUT METHODS
    # ============================================================

    def last_app(self):

        return self.get_last_app()

    def last_website(self):

        return self.get_last_website()

    def last_search(self):

        return self.get_last_search()

    def last_reference(self):

        return self.get_last_reference()
