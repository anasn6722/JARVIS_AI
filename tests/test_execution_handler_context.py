from ai.brain import Brain


def main():
    print("=== JARVIS EXECUTION HANDLER CONTEXT TEST ===")

    brain = Brain()

    print("\n=== PLANNER CONTEXT ===")

    context = brain.planner_context()

    print(context)

    print("\n=== TEST PASSED ===")


if __name__ == "__main__":
    main()