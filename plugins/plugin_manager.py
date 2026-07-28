import importlib
import inspect
import pkgutil

from plugins.base_plugin import BasePlugin


class PluginManager:

    def __init__(self):
        self.plugins = []

        self.load_plugins()

    def register(self, plugin):
        print(f"✅ Loaded plugin: {plugin.name}")
        self.plugins.append(plugin)

    def execute(self, intent, command):

        for plugin in self.plugins:

            if intent in plugin.SUPPORTED_INTENTS:

                return plugin.execute(command)

        return None

    def load_plugins(self):
        import plugins

        for _, module_name, _ in pkgutil.iter_modules(
            plugins.__path__
        ):

            if module_name in (
                "__init__",
                "base_plugin",
                "plugin_manager",
            ):
                continue

            module = importlib.import_module(
                f"plugins.{module_name}"
            )

            for _, obj in inspect.getmembers(
                module,
                inspect.isclass,
            ):

                if (
                    issubclass(obj, BasePlugin)
                    and obj is not BasePlugin
                ):
                    self.register(obj())