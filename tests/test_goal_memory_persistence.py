from datetime import datetime
from pathlib import Path

from ai.agent.task import Task
from ai.memory.goal_memory import GoalMemory
from ai.memory.goal_record import GoalRecord

TEST_FILE = Path("data/test_goals.json")


def main():
    print("=" * 60)
    print("JARVIS PERSISTENT GOAL MEMORY TEST")
    print("=" * 60)

    # ------------------------------------------------------------
    # CLEAN OLD TEST DATA
    # ------------------------------------------------------------

    if TEST_FILE.exists():
        TEST_FILE.unlink()

    # ------------------------------------------------------------
    # CREATE MEMORY
    # ------------------------------------------------------------

    memory = GoalMemory(
        file_path=TEST_FILE,
    )

    task1 = Task(
        action="get_system_info",
    )

    task2 = Task(
        action="get_display_info",
    )

    goal = GoalRecord(
        id="goal-persistence-001",
        title="Test persistent desktop goal",
        created=datetime.now(),
        tasks=[
            task1,
            task2,
        ],
        progress=50.0,
    )

    # ------------------------------------------------------------
    # SAVE
    # ------------------------------------------------------------

    print("\n=== ADD AND SAVE ===")

    memory.add(goal)

    print(
        "Saved:",
        TEST_FILE.exists(),
    )

    # ------------------------------------------------------------
    # CREATE NEW MEMORY INSTANCE
    # ------------------------------------------------------------

    print("\n=== RELOAD MEMORY ===")

    new_memory = GoalMemory(
        file_path=TEST_FILE,
    )

    loaded_goal = new_memory.get(
        "goal-persistence-001"
    )

    if loaded_goal:
        print(
            "Loaded:",
            loaded_goal.title,
        )
        print(
            "Progress:",
            loaded_goal.progress,
        )
        print(
            "Tasks:",
            len(loaded_goal.tasks),
        )

        for task in loaded_goal.tasks:
            print(
                task.id,
                "->",
                task.action,
            )
    else:
        print("ERROR: Goal was not loaded.")

    # ------------------------------------------------------------
    # MODIFY
    # ------------------------------------------------------------

    print("\n=== MODIFY AND SAVE ===")

    loaded_goal.tasks[0].completed = True
    loaded_goal.progress = 75.0

    new_memory.save()

    # ------------------------------------------------------------
    # RELOAD AGAIN
    # ------------------------------------------------------------

    print("\n=== VERIFY MODIFICATION ===")

    final_memory = GoalMemory(
        file_path=TEST_FILE,
    )

    final_goal = final_memory.get(
        "goal-persistence-001"
    )

    print(
        "Progress:",
        final_goal.progress,
    )

    print(
        "First task completed:",
        final_goal.tasks[0].completed,
    )

    # ------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------

    print("\n=== DELETE ===")

    final_memory.remove(
        "goal-persistence-001"
    )

    print(
        "Goal exists:",
        final_memory.get(
            "goal-persistence-001"
        ),
    )

    # ------------------------------------------------------------
    # CLEANUP
    # ------------------------------------------------------------

    if TEST_FILE.exists():
        TEST_FILE.unlink()

    print("\n" + "=" * 60)
    print("PERSISTENT GOAL MEMORY TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()