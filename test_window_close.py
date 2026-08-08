
from automation.desktop.window_manager import WindowManager


def main():
    print("\n=== FIND VS CODE ===\n")

    vscode = WindowManager.find_window(
        "visual studio code"
    )

    if not vscode:
        print("VS Code window not found.")
        return

    print("Found:")
    print(vscode)

    hwnd = vscode["hwnd"]

    print("\n=== CLOSING VS CODE WINDOW ===\n")

    success = WindowManager.close_window(hwnd)

    print(
        "Close result:",
        success,
    )

    print("\n=== VERIFY WINDOW ===\n")

    remaining = WindowManager.find_window(
        "visual studio code"
    )

    if remaining:
        print(
            "Window is still open:",
            remaining,
        )
    else:
        print(
            "VS Code window is no longer detected."
        )


if __name__ == "__main__":
    main()
