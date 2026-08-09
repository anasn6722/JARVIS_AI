from desktop_automation.handler.desktop_handler import DesktopHandler


def main():
    handler = DesktopHandler()

    print("\n=== CLOSE VS CODE ===\n")

    success, response = handler.handle(
        "close_window",
        "vs code",
    )

    print("Success:", success)
    print("Response:", response)


if __name__ == "__main__":
    main()