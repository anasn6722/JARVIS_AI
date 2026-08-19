import threading

import pyttsx3

print(threading.current_thread().name)

engine = pyttsx3.init("sapi5")

voices = engine.getProperty("voices")

for i, voice in enumerate(voices):
    print(i, voice.id, voice.name)


engine.say("Hello Anas, voice test successful")
engine.runAndWait()