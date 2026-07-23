import platform
import psutil


class System:

    @staticmethod
    def operating_system():
        return platform.system()

    @staticmethod
    def processor():
        return platform.processor()

    @staticmethod
    def python_version():
        return platform.python_version()

    @staticmethod
    def machine():
        return platform.machine()

    @staticmethod
    def total_ram():

        ram = psutil.virtual_memory().total

        return round(ram / (1024 ** 3), 2)