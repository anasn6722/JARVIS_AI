import time

from config.states import AssistantState
from voice.speech_manager import SpeechManager

speech_manager = SpeechManager()


assistant_state = AssistantState.SLEEPING

last_active = time.time()