class CommandRegistry:
    def __init__(self):
        self.commands = {}

    def register(self, intent, handler):
        self.commands[intent] = handler

    def execute(self, intent, *args):
        print("Registry intents:", self.commands.keys())
        print("Requested intent:", intent)
        if intent in self.commands:
            print("FOUND!")
            return self.commands[intent](*args)
        print("NOT FOUND!")
        return None