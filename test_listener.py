from voice.listener import Listener

listener = Listener()

print("Speak now...")

text = listener.listen()

print(text)