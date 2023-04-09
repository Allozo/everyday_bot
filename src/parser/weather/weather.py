import requests
from bs4 import BeautifulSoup

from src.parser.weather.schemas import WeatherHours, DailyWeather


class ParseWeather:
    def __init__(self) -> None:
        self.dict_town_url = {
            "Москва": "https://www.gismeteo.ru/weather-moscow-4368/",
            "Санкт-Петербург": "https://www.gismeteo.ru/weather-sankt-peterburg-4079/",
        }

        self.cache_town_soup: dict[str, BeautifulSoup] = {}

    def _load_html(self, town: str) -> None:
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "referer": "https://www.google.com/",
        }

        res = requests.get(self.dict_town_url[town], headers=header)
        self.cache_town_soup[town] = BeautifulSoup(res.content, "html.parser")

    def _get_list_time(self, town: str) -> list[(str, str)]:
        soup = self.cache_town_soup[town]

        block_time = soup.find(class_="widget-row-time").find_all(
            class_="row-item"
        )
        res = [
            (time.text[:-2].strip(), time.find(class_="time-sup").text.strip())
            for time in block_time
        ]
        return res

    def _get_list_status(self, town: str) -> list[str]:
        soup = self.cache_town_soup[town]

        block_status = soup.find(class_="widget-row-icon").find_all(
            class_="row-item"
        )

        res = [
            status.find(class_="weather-icon")["data-text"].strip()
            for status in block_status
        ]

        return res

    def _get_list_temperature(self, town: str) -> list[str]:
        soup = self.cache_town_soup[town]

        block_temperature = soup.find(
            class_="widget-row-chart-temperature"
        ).find_all(class_="value")

        res = [
            temperature.find(class_="unit unit_temperature_c").text.strip()
            for temperature in block_temperature
        ]

        return res

    def get_weather_on_day(self, town: str) -> DailyWeather:
        self._load_html(town)

        list_time = self._get_list_time(town)
        list_status = self._get_list_status(town)
        list_temperature = self._get_list_temperature(town)

        list_weather = [
            WeatherHours(time=time, temperature=temperature, status=status)
            for time, temperature, status in zip(
                list_time, list_temperature, list_status
            )
        ]

        res = DailyWeather(town_name=town, list_weather_hours=list_weather)

        return str(res)


def main():
    weather = ParseWeather()

    print(weather.get_weather_on_day("Москва"))
    print(weather.get_weather_on_day("Санкт-Петербург"))


if __name__ == "__main__":
    main()
