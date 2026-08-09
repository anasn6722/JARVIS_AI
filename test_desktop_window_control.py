from desktop_automation.controller.desktop_controller import (
    DesktopController,
)


def main():
    desktop = DesktopController()

    print("\n=== FIND VS CODE ===")

    window = desktop.find_window("vs code")

    print(window)

    if not window:
        print("VS Code not found.")
        return

    print("\n=== MINIMIZE VS CODE ===")

    success, response = desktop.minimize_window(
        "vs code"
    )

    print("Success:", success)
    print("Response:", response)

    input("\nPress Enter to restore VS Code...")

    print("\n=== RESTORE VS CODE ===")

    success, response = desktop.restore_window(
        "vs code"
    )

    print("Success:", success)
    print("Response:", response)

    input("\nPress Enter to maximize VS Code...")

    print("\n=== MAXIMIZE VS CODE ===")

    success, response = desktop.maximize_window(
        "vs code"
    )

    print("Success:", success)
    print("Response:", response)

    input("\nPress Enter to restore VS Code...")

    print("\n=== RESTORE VS CODE ===")

    success, response = desktop.restore_window(
        "vs code"
    )

    print("Success:", success)
    print("Response:", response)


if __name__ == "__main__":
    main()

