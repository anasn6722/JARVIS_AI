from desktop_automation.planner.desktop_planner import DesktopPlanner


def main():
    planner = DesktopPlanner()

    commands = [
        "show windows",
        "active window",
        "focus VS Code",
        "switch to WhatsApp",
        "minimize VS Code",
        "maximize VS Code",
        "restore VS Code",
        "close VS Code",
    ]

    for command in commands:
        print(f"\nCOMMAND: {command}")

        plan = planner.plan(command)

        print("PLAN:", plan)


if __name__ == "__main__":
    main()