import time as t

from .credentials import API, COUNT_CITY, Session
from .get_api_weather import get_weather
from .models import City, Cloud, Temp, Weather, Wind
from .my_logger import logger


def get_pause(cityes):
    """Установка пауз в запросах при превышении числа запросов"""
    pause = {_: 0 for _ in range(len(cityes))}
    count_pause = len(cityes) // 59
    if count_pause != 0:
        for _ in range(1, count_pause + 1):
            pause[_*59] = 60
    return pause


def get_temp(resp, session):
    """Получение или создание экземпляра температуры"""
    
    if not session.query(session.query(Temp).filter(
        Temp.temp==resp['main']['temp'],
        Temp.feels_like==resp['main']['feels_like'],
        Temp.temp_min==resp['main']['temp_min'],
        Temp.temp_max==resp['main']['temp_max']).exists()).scalar():
        temp = Temp(
            temp=float(resp['main']['temp']),
            feels_like=float(resp['main']['feels_like']),
            temp_min=float(resp['main']['temp_min']),
            temp_max=float(resp['main']['temp_max'])
        )
        session.add(temp)
    temp_req = session.query(Temp).filter(
        Temp.temp==resp['main']['temp'],
        Temp.feels_like==resp['main']['feels_like'],
        Temp.temp_min==resp['main']['temp_min'],
        Temp.temp_max==resp['main']['temp_max']
    )
    return temp_req.all()[0]


def get_cloud(resp, session):
    """Получение или создание экземпляра облачности"""
    if not session.query(session.query(Cloud).filter(
        Cloud.index==resp['clouds']['all']).exists()).scalar():
        cloud = Cloud(
            index=resp['clouds']['all']
        )
        session.add(cloud)
    cloud_req = session.query(Cloud).filter(
        Cloud.index==resp['clouds']['all']
    )
    return cloud_req.all()[0]


def get_wind(resp, session):
    """Получение и создание экземпляра Ветер"""
    if not session.query(session.query(Wind).filter(
        Wind.speed==resp['wind']['speed'],
        Wind.deg==resp['wind']['deg']).exists()).scalar():
        wind = Wind(
            speed=resp['wind']['speed'],
            deg=resp['wind']['deg']
        )
        session.add(wind)
    wind_req = session.query(Wind).filter(
        Wind.speed==resp['wind']['speed'],
        Wind.deg==resp['wind']['deg']
    )
    return wind_req.all()[0]


def update_weather(cityes):
    pause = get_pause(cityes)
    for _ in range(len(cityes)):
        t.sleep(pause[_])
        resp = get_weather(cityes[_].name, API).json()
        session = Session()
        weather = Weather(
            city=cityes[_].id,
            timestamp=resp['dt'],
            temp=get_temp(resp, session).id,
            wind=get_wind(resp, session).id,
            cloud=get_cloud(resp, session).id,
            preassure=resp['main']['pressure'],
            humidity=resp['main']['humidity']
        )
        session.add(weather)
        session.commit()
    logger.info(f'Погода обновлена в {t.time()}')


def main_weather_updater():
    cityes = Session().query(City)[:COUNT_CITY]
    Session().expunge_all()
    Session().commit()
    update_weather(cityes)


if __name__ == '__main__':
    main_weather_updater()
