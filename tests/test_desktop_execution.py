from desktop_automation.handler.desktop_handler import DesktopHandler


def main():
    handler = DesktopHandler()

    commands = [
        "active window",
        "show windows",
        "focus VS Code",
        "minimize VS Code",
        "restore VS Code",
        "maximize VS Code",
    ]

    for command in commands:
        print("\n" + "=" * 50)
        print(f"COMMAND: {command}")
        print("=" * 50)

        success, response = handler.execute(command)

        print("Success:", success)
        print("Response:", response)


if __name__ == "__main__":
    main()