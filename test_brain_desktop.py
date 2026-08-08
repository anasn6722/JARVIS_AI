
from ai.brain import Brain

brain = Brain()

print("\n" + "=" * 60)
print("TEST: DESKTOP PLANNER")
print("=" * 60)

commands = [
    "focus VS Code",
    "what is the active window",
    "show windows",
]

for command in commands:

    print("\n" + "-" * 60)
    print(f"COMMAND: {command}")
    print("-" * 60)

    response = brain.process(command)

    print(f"RESPONSE: {response}")
