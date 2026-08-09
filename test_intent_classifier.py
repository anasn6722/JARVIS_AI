from ai.intent_classifier import IntentClassifier

classifier = IntentClassifier()

commands = [
    "minimize VS Code window",
    "maximize VS Code window",
    "restore VS Code window",
    "minimize the active window",
    "maximize the active window",
    "restore the active window",
    "focus VS Code",
    "what is the active window",
    "show windows",
]

for command in commands:
    result = classifier.classify(command)

    print(f"{command:<35} -> {result['intent']}")