class CommandRegistry:
    def __init__(self):
        self.commands = {}

    def register(self, intent, handler):
        self.commands[intent] = handler

    def execute(self, intent, *args):
        if intent in self.commands:
            return self.commands[intent](*args)

        return "Sorry, I don't understand that command yet."