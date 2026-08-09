from ai.brain import Brain


def run_test(brain, command):
    print("\n" + "-" * 60)
    print(f"COMMAND: {command}")
    print("-" * 60)

    response = brain.process(command)

    print(f"\nRESPONSE: {response}")


def main():
    brain = Brain()

    print("\n" + "=" * 60)
    print("TEST: FULL DESKTOP WINDOW CONTROL")
    print("=" * 60)

    commands = [
        # Existing
        "focus VS Code",
        "what is the active window",
        "show windows",

        # Target window controls
        "minimize VS Code window",
        "restore VS Code window",
        "maximize VS Code window",
        "restore VS Code window",

        # Active window controls
        "minimize the active window",
        "restore the active window",
        "maximize the active window",
        "restore the active window",
    ]

    for command in commands:
        run_test(brain, command)


if __name__ == "__main__":
    main()