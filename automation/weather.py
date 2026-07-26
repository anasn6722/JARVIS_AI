import requests


class WeatherController:

    BASE_URL = "https://wttr.in"

    def get_weather(self, city: str):
        try:
            response = requests.get(
                f"{self.BASE_URL}/{city}",
                params={"format": "j1"},
                timeout=5,
            )

            response.raise_for_status()

            data = response.json()

            current = data["current_condition"][0]

            return {
                "temperature": current["temp_C"],
                "description": current["weatherDesc"][0]["value"],
                "humidity": current["humidity"],
                "wind": current["windspeedKmph"],
            }

        except requests.RequestException:
            return None