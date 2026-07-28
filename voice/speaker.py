import pyttsx3


class Speaker:

    _engine = None

    def __init__(self):

        if Speaker._engine is None:
            Speaker._engine = pyttsx3.init()

            Speaker._engine.setProperty("rate",175)
            Speaker._engine.setProperty("volume",1.0)

        self.engine = Speaker._engine

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()