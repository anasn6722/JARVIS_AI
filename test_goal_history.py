from datetime import datetime

from ai.memory.goal_history import GoalHistory
from ai.memory.goal_memory import GoalMemory
from ai.memory.goal_record import GoalRecord


def main():
    print("\n=== JARVIS GOAL HISTORY TEST ===")

    memory = GoalMemory()
    history = GoalHistory(memory)

    goal = GoalRecord(
        id="goal-history-001",
        title="Test desktop goal",
        created=datetime.now(),
    )

    memory.add(goal)

    print("\n=== INITIAL ===")
    print("Active:", len(history.active()))
    print("Paused:", len(history.paused()))
    print("Completed:", len(history.completed()))
    print("Archived:", len(history.archived()))

    print("\n=== PAUSE ===")

    success, message = history.pause(goal.id)

    print("Success:", success)
    print("Message:", message)
    print("Paused:", goal.paused)

    print("\n=== RESUME ===")

    success, message = history.resume(goal.id)

    print("Success:", success)
    print("Message:", message)
    print("Paused:", goal.paused)

    print("\n=== COMPLETE ===")

    goal.completed = True
    goal.progress = 100.0

    print("Completed:", goal.completed)
    print("Progress:", goal.progress)

    print("\n=== ARCHIVE ===")

    success, message = history.archive(goal.id)

    print("Success:", success)
    print("Message:", message)
    print("Archived:", goal.archived)

    print("\n=== RESTORE ===")

    success, message = history.restore(goal.id)

    print("Success:", success)
    print("Message:", message)
    print("Archived:", goal.archived)

    print("\n=== FINAL STATUS ===")

    print("Active:", len(history.active()))
    print("Paused:", len(history.paused()))
    print("Completed:", len(history.completed()))
    print("Archived:", len(history.archived()))


if __name__ == "__main__":
    main()