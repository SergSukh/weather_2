import csv
import os

from .credentials import Session
from .models import City


def write_cityes2base():
    path = './data/'
    os.chdir(path)
    s = Session()


    with open('csvData.csv', encoding="utf-8") as csvfile:
        reader = csv.DictReader(
            csvfile, fieldnames=['rank', 'city', 'country', 'pop2022']
        )
        city = []
        for _ in reader:
            city.append(City(
                name=_['city'],
                state=_['country'],
                population=_['pop2022']
            ))
        s.add_all(city)
        s.commit()


if __name__ == '__main__':
    write_cityes2base()