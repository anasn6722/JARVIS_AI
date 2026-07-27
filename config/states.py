from enum import Enum


class AssistantState(Enum):
    SLEEPING = 0
    LISTENING = 1
    THINKING = 2
    SPEAKING = 3