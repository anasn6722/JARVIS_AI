
from desktop_automation.controller.desktop_controller import DesktopController


def main():
    desktop = DesktopController()

    print("\n=== ACTIVE WINDOW ===\n")

    active = desktop.active_window()

    print(active)

    print("\n=== FIND VS CODE ===\n")

    vscode = desktop.find_window(
        "visual studio code"
    )

    print(vscode)

    if not vscode:
        print(
            "Open VS Code before running this test."
        )
        return

    print("\n=== FOCUS VS CODE ===\n")

    success, response = desktop.focus_window(
        "visual studio code"
    )

    print("Success:", success)
    print("Response:", response)

    print("\n=== ACTIVE WINDOW ===\n")

    print(
        desktop.active_window()
    )


if __name__ == "__main__":
    main()