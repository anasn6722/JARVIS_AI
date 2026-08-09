from desktop_automation.controller.desktop_controller import DesktopController


def main():
    desktop = DesktopController()

    target = "visual studio code"

    print("\n=== INITIAL WINDOW ===\n")
    print(desktop.get_active_window())

    print("\n=== FIND VS CODE ===\n")
    vscode = desktop.find_window(target)
    print(vscode)

    if not vscode:
        print("Open VS Code before running this test.")
        return

    print("\n=== FOCUS VS CODE ===\n")
    success, response = desktop.focus_window(target)
    print("Success:", success)
    print("Response:", response)

    print("\n=== MINIMIZE VS CODE ===\n")
    success, response = desktop.minimize_window(target)
    print("Success:", success)
    print("Response:", response)

    print("\n=== RESTORE VS CODE ===\n")
    success, response = desktop.restore_window(target)
    print("Success:", success)
    print("Response:", response)

    print("\n=== MAXIMIZE VS CODE ===\n")
    success, response = desktop.maximize_window(target)
    print("Success:", success)
    print("Response:", response)

    print("\n=== FINAL ACTIVE WINDOW ===\n")
    print(desktop.get_active_window())
    print("\n=== CLOSE VS CODE ===\n")

    success, response = desktop.close_window(
        "visual studio code"
    )
    
    print("Success:", success)
    print("Response:", response)


if __name__ == "__main__":
    main()