from automation.weather import WeatherController
from plugins.base_plugin import BasePlugin


class WeatherPlugin(BasePlugin):

    name = "weather"

    def __init__(self):
        self.weather = WeatherController()

    def can_handle(self, command: str):
        keywords = (
            "weather",
            "temperature",
            "forecast",
            "rain",
            "hot",
            "cold",
            "humidity",
            "wind",
            "outside",
        )

        return any(
            keyword in command.lower()
            for keyword in keywords
        )

    def execute(self, command: str):
        city = self.extract_city(command)

        data = self.weather.get_weather(city)

        if data is None:
            return "I couldn't retrieve the weather."

        return (
            f"🌤 Weather Report\n\n"
            f"📍 City: {city.title()}\n"
            f"🌡 Temperature: {data['temperature']}°C\n"
            f"☁ Condition: {data['description']}\n"
            f"💧 Humidity: {data['humidity']}%\n"
            f"💨 Wind Speed: {data['wind']} km/h"
        )

    def extract_city(self, command: str):
        command = command.lower()

        prefixes = (
            "weather in ",
            "temperature in ",
            "forecast for ",
            "forecast in ",
            "how hot is ",
            "how cold is ",
            "is it cold in ",
            "is it hot in ",
        )

        for prefix in prefixes:
            if prefix in command:
                city = command.split(prefix, 1)[1]
                return city.strip(" ?.")

        return "Bahawalnagar"