from memory.chat_memory import ChatMemory
from memory.goals import GoalMemory
from memory.history import HistoryMemory
from memory.long_term import LongTermMemory
from memory.profile_memory import ProfileMemory


class MemoryManager:

    def __init__(self,db):

        self.profile = ProfileMemory(db)

        self.history = HistoryMemory(db)

        self.chat = ChatMemory(db)

        self.goals = GoalMemory(db)

        self.long_term = LongTermMemory(db)