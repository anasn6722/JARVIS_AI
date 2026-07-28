from config.states import AssistantState
from core.logger import logger


class StateMachine:

    def __init__(self):

        self._state = AssistantState.SLEEPING

    @property
    def state(self):
        return self._state

    def change(self, new_state):

        if self._state == new_state:
            return

        logger.info(
            "STATE: %s -> %s",
            self._state.name,
            new_state.name,
        )

        self._state = new_state

    def is_sleeping(self):
        return self._state == AssistantState.SLEEPING

    def is_awake(self):
        return self._state == AssistantState.AWAKE

    def is_thinking(self):
        return self._state == AssistantState.THINKING

    def is_speaking(self):
        return self._state == AssistantState.SPEAKING