class Conversation:

    def __init__(self):

        self.last_command = None
        self.last_response = None
        self.topic = None

    def update(self, command):

        self.last_command = command

    def remember_response(self, response):

        self.last_response = response

    def clear(self):

        self.last_command = None
        self.last_response = None
        self.topic = None