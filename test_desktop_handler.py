from desktop_automation.handler.desktop_handler import DesktopHandler


def main():
    handler = DesktopHandler()

    print("\n=== ACTIVE WINDOW ===\n")

    success, response = handler.handle(
        "active_window"
    )

    print("Success:", success)
    print("Response:", response)

    print("\n=== FIND VS CODE ===\n")

    success, response = handler.handle(
        "find_window",
        "visual studio code",
    )

    print("Success:", success)
    print("Response:", response)

    print("\n=== FOCUS VS CODE ===\n")

    success, response = handler.handle(
        "focus_window",
        "visual studio code",
    )

    print("Success:", success)
    print("Response:", response)

    print("\n=== MINIMIZE VS CODE ===\n")

    success, response = handler.handle(
        "minimize_window",
        "visual studio code",
    )

    print("Success:", success)
    print("Response:", response)

    print("\n=== RESTORE VS CODE ===\n")

    success, response = handler.handle(
        "restore_window",
        "visual studio code",
    )

    print("Success:", success)
    print("Response:", response)

    print("\n=== MAXIMIZE VS CODE ===\n")

    success, response = handler.handle(
        "maximize_window",
        "visual studio code",
    )

    print("Success:", success)
    print("Response:", response)


if __name__ == "__main__":
    main()