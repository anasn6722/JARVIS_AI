from config.states import AssistantState
from core import app_state


class AssistantController:

    def __init__(self, brain, speech_manager):

        self.brain = brain
        self.speech = speech_manager

    def wake(self):

        app_state.state_machine.change(
            AssistantState.AWAKE
        )

    def sleep(self):

        app_state.state_machine.change(
            AssistantState.SLEEPING
        )

    def process(self, command):

        app_state.state_machine.change(
            AssistantState.THINKING
        )

        response = self.brain.process(command)

        app_state.state_machine.change(
            AssistantState.SPEAKING
        )

        self.speech.say(response)

        return response