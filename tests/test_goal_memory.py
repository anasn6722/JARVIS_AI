from ai.memory.goal_memory import GoalMemory


class TestGoal:
    def __init__(self, goal_id, title):
        self.id = goal_id
        self.title = title


def main():
    print("=" * 60)
    print("JARVIS GOAL MEMORY TEST")
    print("=" * 60)

    memory = GoalMemory()

    # ============================================================
    # ADD
    # ============================================================

    print("\n=== ADD GOALS ===")

    goal1 = TestGoal(
        "goal-001",
        "Show desktop information",
    )

    goal2 = TestGoal(
        "goal-002",
        "Open Visual Studio Code",
    )

    memory.add(goal1)
    memory.add(goal2)

    print("Goals stored:", len(memory.all()))

    # ============================================================
    # GET
    # ============================================================

    print("\n=== GET GOAL ===")

    goal = memory.get("goal-001")

    if goal:
        print("Found:", goal.title)
    else:
        print("Goal not found.")

    # ============================================================
    # ALL
    # ============================================================

    print("\n=== ALL GOALS ===")

    for goal in memory.all():
        print(
            goal.id,
            "->",
            goal.title,
        )

    # ============================================================
    # REMOVE
    # ============================================================

    print("\n=== REMOVE GOAL ===")

    memory.remove("goal-001")

    print(
        "Remaining goals:",
        len(memory.all()),
    )

    # ============================================================
    # CLEAR
    # ============================================================

    print("\n=== CLEAR MEMORY ===")

    memory.clear()

    print(
        "Remaining goals:",
        len(memory.all()),
    )

    print("\n" + "=" * 60)
    print("GOAL MEMORY TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()