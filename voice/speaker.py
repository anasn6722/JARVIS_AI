import pyttsx3


class Speaker:

    def speak(self, text):

        print("Creating engine...")

        engine = pyttsx3.init("sapi5")

        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)
        engine.setProperty("rate", 175)
        engine.setProperty("volume", 1.0)

        print("Speaking:", text)

        engine.say(text)
        engine.runAndWait()

        engine.stop()

        print("Finished")