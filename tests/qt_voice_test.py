import sys

import pyttsx3
from PySide6.QtWidgets import QApplication, QPushButton

app = QApplication(sys.argv)

engine = pyttsx3.init("sapi5")

def speak():
    print("Speaking...")
    engine.say("Hello from Qt")
    engine.runAndWait()
    print("Finished")

button = QPushButton("Speak")
button.clicked.connect(speak)
button.show()

sys.exit(app.exec())