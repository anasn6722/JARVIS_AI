class PipelineContext:

    def __init__(self, text):

        self.input = text

        self.commands = []

        self.decisions = []

        self.current_command = None

        self.current_goal = None

        self.decision = None

        self.tasks = []

        self.graph = None  

        self.response = None

        self.stop = False