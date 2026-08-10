import platform

import psutil


def get_system_info(target=None):
    """Return basic operating system information."""

    information = {
        "operating_system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }

    if target:
        target = target.lower().strip()

        if target in information:
            return {
                target: information[target],
            }

    return information


def get_display_info(target=None):
    """Return basic display information."""

    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()

        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()

        root.destroy()

        information = {
            "screen_resolution": f"{width}x{height}",
        }

        if target:
            target = target.lower().strip()

            if target in information:
                return {
                    target: information[target],
                }

        return information

    except Exception as error:
        return {
            "screen_resolution": "Unknown",
            "error": str(error),
        }


def list_active_processes(target=None):
    """Return currently running processes."""

    processes = []

    for process in psutil.process_iter(
        ["pid", "name"],
    ):
        try:
            processes.append(
                {
                    "pid": process.info["pid"],
                    "name": process.info["name"],
                }
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return processes