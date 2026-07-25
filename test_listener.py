import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Adjusting microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("🗣️ Speak now!")
    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)

except sr.UnknownValueError:
    print("Could not understand what you said.")

except sr.RequestError as error:
    print("Recognition service error:", error)