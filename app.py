import time

import schedule

from core.chek_city_scheduler import main_check
from core.connection import main_connection
from core.credentials import TIME
from core.weather_update import main_weather_updater


def schedule_weather_update():
    main_weather_updater()



def main():
    main_connection()
    main_check()
    main_weather_updater()
    schedule.every(TIME).minutes.do(schedule_weather_update)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()