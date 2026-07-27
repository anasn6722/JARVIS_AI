from enum import Enum


class AssistantState(Enum):
    SLEEPING = 0
    AWAKE = 1
    LISTENING = 2
    THINKING = 3
    SPEAKING = 4