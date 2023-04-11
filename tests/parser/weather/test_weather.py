from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from src.parser.weather.weather import ParseWeather

# Тестируем на сохранённой HTML Москвы
TOWN = 'Москва'


@pytest.fixture()
def pw(mocker):
    # Сохраним во внутренний словарик ParseWeather html
    with Path('tests/parser/weather/html/test_weather_moscow.html').open(
        encoding='utf-8'
    ) as f:
        html = f.readlines()

    parse_weather = ParseWeather()
    parse_weather.cache_town_soup[TOWN] = BeautifulSoup(str(html), 'html.parser')

    # Замокируем вызов _load_html()
    mocker.patch(
        'src.parser.weather.weather.ParseWeather._load_html'
    ).return_value = html

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

    assert pw.get_weather_on_day(TOWN) == res


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
