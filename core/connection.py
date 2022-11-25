import psycopg2
from psycopg2 import Error as E
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from .credentials import DB_HOST, DB_NAME, DB_PORT, PG_PASS, PG_USER
from .models import main_models
from .my_logger import logger


def connect(database=None):
    try:
        connection = psycopg2.connect(
            user=PG_USER,
            password=PG_PASS,
            host=DB_HOST,
            port=DB_PORT,
            database=database
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    except (Exception, E) as e:
        logger.debug(f'Ошибка подключения к Postgres {e}')
    return connection


def create_db(connection, name):
    try:
        cursor = connection.cursor()
        sql_create_database = f'create database {name}'
        cursor.execute(sql_create_database)
        logger.info(f'БД {name} создана успешно')
    except (Exception, E) as e:
        logger.debug(f'Ошибка подключения к Postgres {e}')
    main_models()
    logger.info('Модели городов и погоды созданы в новой БД')


def check_db(connection, name_db):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT datname FROM pg_database;')
        list_database = cursor.fetchall()
    except (Exception, E) as e:
        logger.debug(f'Ошибка при попытке доступа к БД {e}')
    return (name_db,) in list_database


def create_table(connection, name_table):
    try:
        cursor = connection.cursor()
        create_table_query = f'''CREATE TABLE {name_table} (
            city_id serial NOT NULL PRIMARY KEY,
            city_name VARCHAR (50) NOT NULL,
            state VARCHAR (50) NOT NULL,
            population INTEGER NOT NULL
        ); '''
        cursor.execute(create_table_query)
        connection.commit()
    except (Exception, E) as e:
        logger.debug(f'Ошибка при создании таблицы {name_table} {e}')


def check_table(connection, name_table):
    try:
        cursor = connection.cursor()
        cursor.execute(
            'SELECT EXISTS' +
            '(SELECT * FROM information_schema.tables WHERE table_name=%s)',
            (f'{name_table}',)
        )
    except (Exception, E) as e:
        logger.debug(f'Ошибка проверки таблицы {name_table}, {e}')
    return bool(cursor.rowcount)


def main_connection():
    connection = connect()
    if not check_db(connection, DB_NAME):
        create_db(connection, DB_NAME)
    connection.close()


if __name__ == '__main__':
    main_connection()