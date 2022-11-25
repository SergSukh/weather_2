import time

from .credentials import COUNT_CITY, Session
from .import_all_city import write_cityes2base
from .models import City, Weather
from .my_logger import logger


def check_city_records():
    """Проверка на наличие списка городов в БД в достаточном количестве"""
    resp = len(Session().query(City).all()) > COUNT_CITY
    Session().commit()
    return resp


def check_schedule():
    """Проверка последней загрузки погоды"""
    if (len(Session().query(Weather).all()) > 0):
        last_time = Session().query(
            Weather).order_by(Weather.id.desc()).first().timestamp
        if (60 + last_time - time.time()) > 0:
            logger.info('Активирована пауза')
            time.sleep(60 + last_time - time.time())
    Session().commit()
    logger.info('Выставлено расписание')
    return


def main_check():
    if not check_city_records():
        write_cityes2base()
    check_schedule()


if __name__ == '__main__':
    check_city_records()