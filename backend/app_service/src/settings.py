import os

from dotenv import load_dotenv

from typing import Dict

load_dotenv()

POSTGRES_SETTINGS: Dict[str, str] = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'db': os.getenv('POSTGRES_DB'),
    'host': 'postgres',
    'port': '5432',
}

POSTGRES_TIMESTAMP_WITH_TIMEZONE_FORMAT = "%Y-%m-%d %H:%M:%S%z"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
DB_POOL_MIN_CONNECTIONS = 1
DB_POOL_MAX_CONNECTIONS = 10
