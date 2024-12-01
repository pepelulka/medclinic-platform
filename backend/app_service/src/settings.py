import logging
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
