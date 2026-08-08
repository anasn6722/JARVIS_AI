
from desktop_automation.controller.desktop_controller import DesktopController
from desktop_automation.handler.desktop_handler import DesktopHandler


def main():
    controller = DesktopController()

    desktop = DesktopHandler(
        controller
    )

    print("\n=== ACTIVE WINDOW ===\n")

    success, response = (
        desktop.active_window()
    )

    print("Success:", success)
    print("Response:", response)

    print("\n=== FOCUS VS CODE ===\n")

    success, response = (
        desktop.focus_window(
            "visual studio code"
        )
    )

    print("Success:", success)
    print("Response:", response)

    print("\n=== WINDOWS ===\n")

    success, response = (
        desktop.list_windows()
    )

    print("Success:", success)

    for window in response:
        print("-", window)


if __name__ == "__main__":
    main()
