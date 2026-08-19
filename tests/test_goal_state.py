from datetime import datetime

from ai.agent.goal_state import GoalState
from ai.agent.goal_state_controller import GoalStateController
from ai.memory.goal_record import GoalRecord


def main():
    print("=== JARVIS GOAL STATE TEST ===")

    controller = GoalStateController()

    goal = GoalRecord(
        id="state-test-001",
        title="Test JARVIS goal",
        created=datetime.now(),
    )

    print("\n=== INITIAL ===")
    print("State:", controller.get_state(goal))

    assert controller.get_state(goal) == GoalState.PENDING

    print("\n=== START ===")
    success, message = controller.start(goal)
    print("Success:", success)
    print("Message:", message)

    goal.progress = 25

    print("State:", controller.get_state(goal))

    assert controller.get_state(goal) == GoalState.RUNNING

    print("\n=== PAUSE ===")
    success, message = controller.pause(goal)
    print("Success:", success)
    print("Message:", message)
    print("State:", controller.get_state(goal))

    assert controller.get_state(goal) == GoalState.PAUSED

    print("\n=== RESUME ===")
    success, message = controller.resume(goal)
    print("Success:", success)
    print("Message:", message)
    print("State:", controller.get_state(goal))

    assert controller.get_state(goal) == GoalState.RUNNING

    print("\n=== COMPLETE ===")
    success, message = controller.complete(goal)
    print("Success:", success)
    print("Message:", message)
    print("Progress:", goal.progress)
    print("State:", controller.get_state(goal))

    assert controller.get_state(goal) == GoalState.COMPLETED

    print("\n=== ARCHIVE ===")
    success, message = controller.archive(goal)
    print("Success:", success)
    print("Message:", message)
    print("State:", controller.get_state(goal))

    assert controller.get_state(goal) == GoalState.ARCHIVED

    print("\n=== RESTORE ===")
    success, message = controller.restore(goal)
    print("Success:", success)
    print("Message:", message)
    print("State:", controller.get_state(goal))

    assert controller.get_state(goal) == GoalState.COMPLETED

    print("\n=== TEST PASSED ===")


if __name__ == "__main__":
    main()