from datetime import datetime

from ai.memory.goal_execution import GoalExecution


def main():
    print("=== JARVIS GOAL EXECUTION TEST ===")

    execution = GoalExecution(
        goal_id="goal-001",
        action="get_system_info",
        target="desktop",
        started=datetime.now(),
    )

    print("\n=== INITIAL ===")
    print("Goal ID:", execution.goal_id)
    print("Action:", execution.action)
    print("Target:", execution.target)
    print("Success:", execution.success)

    execution.completed = datetime.now()
    execution.success = True
    execution.result = (
        "{'operating_system': 'Windows 11'}"
    )

    print("\n=== COMPLETED ===")
    print("Started:", execution.started)
    print("Completed:", execution.completed)
    print("Success:", execution.success)
    print("Result:", execution.result)

    print("\n=== TEST PASSED ===")


if __name__ == "__main__":
    main()
