import speech_recognition as sr


class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5,
            )

            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            return text

        except sr.UnknownValueError:
            return ""

        except sr.RequestError:
            return "Internet connection required."