
from automation.desktop.window_manager import WindowManager


def main():
    print("\n=== ACTIVE WINDOW ===\n")

    active = WindowManager.get_active_window()

    print(active)

    print("\n=== FIND VS CODE ===\n")

    vscode = WindowManager.find_window(
        "visual studio code"
    )

    print(vscode)

    if not vscode:
        print("VS Code window not found.")
        return

    print("\n=== FOCUS VS CODE ===\n")

    success = WindowManager.focus_window(
        vscode["hwnd"]
    )

    print(
        "Focus result:",
        success,
    )

    print("\n=== ACTIVE WINDOW AFTER FOCUS ===\n")

    active = WindowManager.get_active_window()

    print(active)


if __name__ == "__main__":
    main()
