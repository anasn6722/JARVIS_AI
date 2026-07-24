import platform
import psutil
import sys


class System:

    @staticmethod
    def operating_system():
        return platform.system()

    @staticmethod
    def processor():
        return platform.processor()

    @staticmethod
    def python_version():
        return sys.version.split()[0]

    @staticmethod
    def total_ram():
        return round(psutil.virtual_memory().total / (1024**3), 2)

    @staticmethod
    def ram_used():
        return round(psutil.virtual_memory().used / (1024**3), 2)

    @staticmethod
    def cpu_usage():
        return psutil.cpu_percent(interval=1)