import requests

from .credentials import API
from .my_logger import logger

URL = 'https://api.openweathermap.org/data/2.5/weather'


def get_weather(city, api):
    """Запрос погоды в городе"""
    data = {
        'q': city,
        'units': 'metric',
        'appid': api
    }
    while True:
        try:
            resp = requests.get(URL, params=data)
            break
        except Exception as e:
            logger.debug(e)
        
    return resp


def test(city):
    assert get_weather(city, API).status_code == 200
    assert get_weather(city, None).status_code == 401
    assert get_weather(city, '12345678').status_code == 401
    assert type(get_weather(city, API).json()) == dict


if __name__ == '__main__':
    test('Moscow')
