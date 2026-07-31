from memory.goals import GoalMemory
from memory.history import HistoryMemory
from memory.profile import ProfileMemory


class MemoryManager:

    def __init__(self):

        self.profile = ProfileMemory()

        self.history = HistoryMemory()

        self.goals = GoalMemory()