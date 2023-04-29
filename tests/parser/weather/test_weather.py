import sys
from pathlib import Path

import pytest

from config import Test
from src.cache.base_cache import BaseCache
from src.parser.weather.weather import ParseWeather

# Тестируем на сохранённой HTML Москвы
TOWN = 'Москва'


@pytest.fixture()
def pw(mocker):
    path_html_test = 'tests/parser/weather/html/test_weather_moscow.html'
    with Path(path_html_test).open(encoding='utf-8') as f:
        html = f.readlines()

    if Test.TYPE_CACHE == 'DICT':
        cache = BaseCache.create_cache(type_cache=Test.TYPE_CACHE)
    elif (
        Test.TYPE_CACHE == 'REDIS'
        and Test.REDIS_HOST is not None
        and Test.REDIS_PORT is not None
    ):
        cache = BaseCache.create_cache(
            type_cache=Test.TYPE_CACHE,
            kwargs={'host': Test.REDIS_HOST, 'port': Test.REDIS_PORT},
        )
    else:
        sys.exit(f'Передали не корректный кэш {Test.TYPE_CACHE=}')

    parse_weather = ParseWeather(cache=cache)

    # Сохраним в Redis загруженную html
    parse_weather.cache_town_soup.set(TOWN, str(html))

    # Замокируем вызов _load_html_in_cache()
    mocker.patch(
        'src.parser.weather.weather.ParseWeather._load_html_in_cache'
    ).return_value = None

    return parse_weather


def test_get_weather_on_day(pw):
    res = '\n'.join(
        [
            'Погода в городе: Москва',
            '0:00  --  +8 -- Облачно, без осадков',
            '3:00  --  +7 -- Пасмурно, без осадков',
            '6:00  --  +6 -- Облачно, без осадков',
            '9:00  -- +10 -- Облачно, без осадков',
            '12:00 -- +14 -- Пасмурно, без осадков',
            '15:00 -- +14 -- Пасмурно, без осадков',
            '18:00 -- +13 -- Облачно, без осадков',
            '21:00 -- +10 -- Ясно',
        ]
    )

    assert str(pw.get_weather_on_day(TOWN)) == res


def test_get_list_time(pw):
    res = [
        ('0', '00'),
        ('3', '00'),
        ('6', '00'),
        ('9', '00'),
        ('12', '00'),
        ('15', '00'),
        ('18', '00'),
        ('21', '00'),
    ]

    assert pw._get_list_time(TOWN) == res  # pylint: disable=protected-access


def test_get_list_temperature(pw):
    res = [
        '+8',
        '+7',
        '+6',
        '+10',
        '+14',
        '+14',
        '+13',
        '+10',
    ]

    assert pw._get_list_temperature(TOWN) == res  # pylint: disable=protected-access


def test_get_list_status(pw):
    res = [
        'Облачно, без осадков',
        'Пасмурно, без осадков',
        'Облачно, без осадков',
        'Облачно, без осадков',
        'Пасмурно, без осадков',
        'Пасмурно, без осадков',
        'Облачно, без осадков',
        'Ясно',
    ]

    assert pw._get_list_status(TOWN) == res  # pylint: disable=protected-access
