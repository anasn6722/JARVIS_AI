class DialogueState:
    """
    Working memory for the current conversation.

    This is NOT long-term memory.

    It stores only the current context.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.current_app = None
        self.current_website = None
        self.current_search = None
        self.current_goal = None
        self.current_topic = None
        self.current_skill = None

        self.last_user_command = None
        self.last_ai_response = None
        self.last_tool = None

        self.active_tasks = []

    # ---------- App ----------

    def set_app(self, app):
        self.current_app = app

    def get_app(self):
        return self.current_app

    # ---------- Website ----------

    def set_website(self, website):
        self.current_website = website

    def get_website(self):
        return self.current_website

    # ---------- Search ----------

    def set_search(self, search):
        self.current_search = search

    def get_search(self):
        return self.current_search

    # ---------- Goal ----------

    def set_goal(self, goal):
        self.current_goal = goal

    def get_goal(self):
        return self.current_goal

    # ---------- Topic ----------

    def set_topic(self, topic):
        self.current_topic = topic

    def get_topic(self):
        return self.current_topic

    # ---------- Skill ----------

    def set_skill(self, skill):
        self.current_skill = skill

    def get_skill(self):
        return self.current_skill

    # ---------- User ----------

    def set_last_command(self, command):
        self.last_user_command = command

    # ---------- AI ----------

    def set_last_response(self, response):
        self.last_ai_response = response

    # ---------- Tool ----------

    def set_last_tool(self, tool):
        self.last_tool = tool