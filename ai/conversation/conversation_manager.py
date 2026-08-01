from ai.conversation.dialogue_state import DialogueState


class ConversationManager:
    """
    Responsible for maintaining the current conversation state.
    """

    def __init__(self):
        self.state = DialogueState()

    def update(self, command):
        """
        Update the dialogue state after understanding a command.
        """

        self.state.set_last_command(command.original)

        entities = command.entities

        apps = entities.get("apps", [])
        websites = entities.get("websites", [])
        searches = entities.get("searches", [])
        goals = entities.get("goals", [])

        if apps:
            self.state.set_app(apps[0])

        if websites:
            self.state.set_website(websites[0])

        if searches:
            self.state.set_search(searches[0])

        if goals:
            self.state.set_goal(goals[0])

    def remember_response(self, response):
        self.state.set_last_response(response)

    def state_data(self):
        return self.state