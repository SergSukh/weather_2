import time as t

from sqlalchemy import FLOAT, VARCHAR, Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base

from .credentials import Session, engine

Base = declarative_base(bind=engine)

CLOUD = {
    0: 'Ясно',
    1: 'Редкие облака',
    2: 'Переменная облачность',
    3: 'Переменная облачность',
    4: 'Переменная облачность',
    5: 'Переменная облачность',
    6: 'Облачно с прояснениями',
    7: 'Облачно с прояснениями',
    8: 'Облачно с прояснениями',
    9: 'Облачно',
    10: 'Пасмурнно',
}


class City(Base):
    """Модель город."""
    __tablename__ = 'city'
    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = Column(VARCHAR(50), nullable=False)
    state = Column(VARCHAR(50))
    population = Column(Integer)

    def __init__(self, name, state, population) -> str:
        self.name = name
        self.state = state
        self.population = population


class Cloud(Base):
    """Модель облачности индекс, возвращает текст из словаря"""
    __tablename__ = 'cloud'
    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    index = Column(Integer)

    def __init__(self, index) -> str:
        self.index = index

    def __str__(self) -> str:
        return f'{CLOUD[self.index//10]}'


class Wind(Base):
    """Модель ветер"""
    __tablename__ = 'wind'
    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    speed = Column(FLOAT)
    deg = Column(Integer)

    def __init__(self, speed, deg):
        self.speed = speed
        self.deg = deg

    def __str__(self) -> str:
        if self.deg > 23 and self.deg < 68:
            deg = 'СВ'
        elif self.deg >= 68 and self.deg < 112:
            deg = 'B'
        elif self.deg >= 112 and self.deg < 157:
            deg = 'ЮВ'
        elif self.deg >= 157 and self.deg < 202:
            deg = 'Ю'
        elif self.deg >= 202 and self.deg < 247:
            deg = 'ЮЗ'
        elif self.deg >= 247 and self.deg < 292:
            deg = 'З'
        elif self.deg >= 292 and self.deg < 337:
            deg = 'СЗ'
        else:
            deg = 'C'
        return f'{deg} {self.speed} м/с'


class Temp(Base):
    """Модель температуры"""
    __tablename__ = 'temp'
    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    temp = Column(FLOAT)
    feels_like = Column(FLOAT)
    temp_min = Column(FLOAT)
    temp_max = Column(FLOAT)

    def __init__(self, temp, feels_like, temp_min, temp_max) -> str:
        self.temp = temp
        self.feels_like = feels_like
        self.temp_min = temp_min
        self.temp_max = temp_max

    def __str__(self) -> str:
        return f'{self.temp}'


class Weather(Base):
    """Модель погоды."""
    __tablename__ = 'weather'
    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    city = Column(
        Integer, ForeignKey('city.id', ondelete='CASCADE'), nullable=False
    )
    timestamp = Column(Integer)
    temp = Column(
        Integer, ForeignKey('temp.id', ondelete='CASCADE'), nullable=False
    )
    wind = Column(
        Integer, ForeignKey('wind.id', ondelete='CASCADE'), nullable=False
    )
    cloud = Column(
        Integer, ForeignKey('cloud.id', ondelete='CASCADE'), nullable=False
    )
    preassure = Column(Integer)
    humidity = Column(Integer)

    def date_time(self):
        dt = t.strftime(
            "%a, %d %b %Y %H:%M:%S +0000", t.localtime(self.timestamp)
        )
        return f'{dt}'


def main_models():
    Base.metadata.create_all()
    s = Session()


if __name__ == '__main__':
    main_models()