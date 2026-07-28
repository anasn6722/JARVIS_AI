import time

from core.state_machine import StateMachine
from voice.speech_manager import SpeechManager

speech_manager = SpeechManager()

state_machine = StateMachine()

last_active = time.time()