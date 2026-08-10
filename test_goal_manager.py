from ai.goal_manager import GoalManager


class InMemoryGoalMemory:
    """Simple memory implementation for testing GoalManager."""

    def __init__(self):
        self.goals = {}

    def add(self, goal):
        self.goals[goal.id] = goal

    def get(self, goal_id):
        return self.goals.get(goal_id)

    def all(self):
        return list(self.goals.values())

    def remove(self, goal_id):
        self.goals.pop(goal_id, None)


class TestTask:
    """Minimal task object for GoalManager testing."""

    def __init__(self, action):
        self.action = action
        self.completed = False


def main():
    print("=" * 60)
    print("JARVIS GOAL MANAGER TEST")
    print("=" * 60)

    # ============================================================
    # BUILD MEMORY
    # ============================================================

    memory = InMemoryGoalMemory()

    goal_manager = GoalManager(
        memory,
    )

    print("\n=== CREATING GOAL ===")

    tasks = [
        TestTask("get_system_info"),
        TestTask("get_display_info"),
        TestTask("list_windows"),
    ]

    goal = goal_manager.create_goal(
        "Show my current desktop information",
        tasks,
    )

    print("Goal ID:", goal.id)
    print("Goal:", goal.title)

    # ============================================================
    # INITIAL PROGRESS
    # ============================================================

    print("\n=== INITIAL PROGRESS ===")

    goal_manager.update_progress(goal)

    print("Progress:", goal.progress)
    print("Completed:", goal.completed)

    # ============================================================
    # NEXT TASK
    # ============================================================

    print("\n=== NEXT TASK ===")

    next_task = goal_manager.next_task(goal)

    if next_task:
        print("Next task:", next_task.action)
    else:
        print("No remaining tasks.")

    # ============================================================
    # COMPLETE FIRST TASK
    # ============================================================

    print("\n=== COMPLETE FIRST TASK ===")

    tasks[0].completed = True

    goal_manager.update_progress(goal)

    print("Progress:", goal.progress)
    print("Completed:", goal.completed)

    next_task = goal_manager.next_task(goal)

    if next_task:
        print("Next task:", next_task.action)

    # ============================================================
    # COMPLETE SECOND TASK
    # ============================================================

    print("\n=== COMPLETE SECOND TASK ===")

    tasks[1].completed = True

    goal_manager.update_progress(goal)

    print("Progress:", goal.progress)
    print("Completed:", goal.completed)

    next_task = goal_manager.next_task(goal)

    if next_task:
        print("Next task:", next_task.action)

    # ============================================================
    # COMPLETE FINAL TASK
    # ============================================================

    print("\n=== COMPLETE FINAL TASK ===")

    tasks[2].completed = True

    goal_manager.update_progress(goal)

    print("Progress:", goal.progress)
    print("Completed:", goal.completed)

    next_task = goal_manager.next_task(goal)

    print("Next task:", next_task)

    # ============================================================
    # RETRIEVE GOAL
    # ============================================================

    print("\n=== RETRIEVE GOAL ===")

    retrieved = goal_manager.get_goal(
        goal.id,
    )

    print("Retrieved:", retrieved.title)

    # ============================================================
    # ALL GOALS
    # ============================================================

    print("\n=== ALL GOALS ===")

    for stored_goal in goal_manager.all_goals():
        print(
            stored_goal.id,
            "->",
            stored_goal.title,
        )

    # ============================================================
    # DELETE
    # ============================================================

    print("\n=== DELETE GOAL ===")

    goal_manager.delete_goal(
        goal.id,
    )

    print(
        "Remaining goals:",
        len(goal_manager.all_goals()),
    )

    print("\n" + "=" * 60)
    print("GOAL MANAGER TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()