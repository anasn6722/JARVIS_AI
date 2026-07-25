import speech_recognition as sr


class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5,
                )

                print("🗣️ Speak now...")

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10,
                )

            text = self.recognizer.recognize_google(audio)

            print(f"✅ Recognized: {text}")

            return text

        except sr.WaitTimeoutError:
            print("⌛ No speech detected.")
            return ""

        except sr.UnknownValueError:
            print("❌ Could not understand speech.")
            return ""

        except sr.RequestError as error:
            print(f"❌ Speech recognition service error: {error}")
            return ""

        except Exception as error:
            print(f"❌ Unexpected error: {error}")
            return ""