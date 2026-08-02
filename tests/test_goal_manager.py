from ai.goal_manager import GoalManager


def main():

    gm = GoalManager()
    print(gm.all())

    goal = "Learn Django"

    print("=" * 50)
    print("NEXT TASK")
    print("=" * 50)

    print(gm.next_task(goal))

    print()

    print("=" * 50)
    print("PROGRESS")
    print("=" * 50)

    print(gm.progress(goal))

    print()

    print("=" * 50)
    print("COMPLETE TASK")
    print("=" * 50)

    gm.complete_task(
        goal,
        "Install Python",
    )

    print()

    print("=" * 50)
    print("NEW PROGRESS")
    print("=" * 50)

    print(gm.progress(goal))

    print()

    print("=" * 50)
    print("NEXT TASK")
    print("=" * 50)

    print(gm.next_task(goal))


if __name__ == "__main__":
    main()