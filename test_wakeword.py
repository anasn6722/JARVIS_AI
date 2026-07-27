from voice.wake_word import WakeWordDetector

detector = WakeWordDetector()


tests = [
    "hey jarvis",
    "jarvis open chrome",
    "what is weather"
]


for text in tests:
    print(text, "=>", detector.detect(text))