import logging

import requests
from bs4 import BeautifulSoup

from src.cache.base_cache import BaseCache
from src.config import LOGGER_CONFIG
from src.parser.weather.schemas import DailyWeather, WeatherHours

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


class ParseWeather:
    def __init__(self, cache: BaseCache) -> None:
        self.dict_town_url = {
            'Москва': 'https://www.gismeteo.ru/weather-moscow-4368/',
            'Санкт-Петербург': 'https://www.gismeteo.ru/weather-sankt-peterburg-4079/',
        }

        # Будут храниться html-ки страниц, чтобы не спамить сервера запросами
        logger.info('В качестве кэша выбран %s', cache.__class__.__name__)
        self.cache_town_soup = cache

    def _load_html_in_cache(self, town: str) -> None:
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',  # pylint: disable=line-too-long
            'referer': 'https://www.google.com/',
        }

        res = requests.get(self.dict_town_url[town], headers=header, timeout=5)
        self.cache_town_soup.set(town, res.content.decode('utf-8'))
        # Хранится значение будет 30 минут
        self.cache_town_soup.expire(town, 30 * 60)

    def _get_list_time(self, town: str) -> list[tuple[str, str]]:
        html_page = self.cache_town_soup.get(town)
        soup = BeautifulSoup(html_page, 'html.parser')

        block_time = soup.find(class_='widget-row-time').find_all(class_='row-item')
        res = [
            (time.text[:-2].strip(), time.find(class_='time-sup').text.strip())
            for time in block_time
        ]
        return res

    def _get_list_status(self, town: str) -> list[str]:
        html_page = self.cache_town_soup.get(town)
        soup = BeautifulSoup(html_page, 'html.parser')

        block_status = soup.find(class_='widget-row-icon').find_all(class_='row-item')

        res = [
            status.find(class_='weather-icon')['data-text'].strip()
            for status in block_status
        ]

        return res

    def _get_list_temperature(self, town: str) -> list[str]:
        html_page = self.cache_town_soup.get(town)
        soup = BeautifulSoup(html_page, 'html.parser')

        block_temperature = soup.find(class_='widget-row-chart-temperature').find_all(
            class_='value'
        )

        res = [
            temperature.find(class_='unit unit_temperature_c').text.strip()
            for temperature in block_temperature
        ]

        return res

    def get_weather_on_day(self, town: str) -> DailyWeather:
        logger.info('Получим погоду для города %s', town)

        if town not in self.dict_town_url:
            logger.error('Город %s отсутствует среди списка возможных городов')

        if not self.cache_town_soup.get(town):
            self._load_html_in_cache(town)

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

        logger.info('Успешно получили погоду для города %s', town)

        return res


def main() -> None:
    # breakpoint()
    cache = BaseCache.create_cache('DICT')
    weather = ParseWeather(cache=cache)

    print(weather.get_weather_on_day('Москва'))
    print(weather.get_weather_on_day('Санкт-Петербург'))


if __name__ == '__main__':
    main()
