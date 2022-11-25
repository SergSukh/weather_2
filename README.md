# weather_2
Сервис архива погоды в X крупнейщих городах мира по численности населения.
Источник данных о погоде API:
- 'https://api.openweathermap.org/data/2.5/weather'

Информация хранится в моделях:
- City(Модель город) сортировка по количеству населения
- Cloud(Облачность) количество вариантов ограниченно, приведет к сохранению места в БД
- Wind(Ветер) количество вариантов ограниченно, приведет к сохранению места в БД
- Temp(Температура)
- Weather(Погода) сортировка в порядке обновления(последнее обновление первым)

### Для развертывания проекта на локальной машине:
- клонируйте проект: git clone git@github.com:SergSukh/weather_50.git
- создайте файл <.env> в папке infra/
- запишите в файл: DB_ENGINE, DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT, API(weather API key), COUNT_CITY(Количество городов для мониторинга), TIME(период обновления в минутах, не обязательно, по умолчанию - 60)
- выполните команду $ docker-compose up -d


### Установка Docker: <a href=https://docs.docker.com/engine/install/ubuntu/>docker</a>


# Работа над проектом: Сергей Суханов
### Стек технологий: Python3, PostgreSQL, SQLalchemy, GIT, import csv, Schedule, Docker
