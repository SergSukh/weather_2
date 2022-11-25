import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

API = os.getenv('API')
DB_NAME = os.getenv('DB_NAME')
PG_USER = os.getenv('POSTGRES_USER')
PG_PASS = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
COUNT_CITY = int(os.getenv('COUNT_CITY'))
TIME = int(os.getenv('TIME', default=60))

engine = create_engine(
    f'postgresql+psycopg2://{PG_USER}:{PG_PASS}@{DB_HOST}/{DB_NAME}',
    pool_size=20,
    max_overflow=0
)
Session = sessionmaker(bind=engine)
