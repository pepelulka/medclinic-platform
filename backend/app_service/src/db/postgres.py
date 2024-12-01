import logging

import asyncpg

from settings import POSTGRES_SETTINGS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_connection_pool() -> asyncpg.Pool:
    connection_config = {
        'database': POSTGRES_SETTINGS['db'],
        'user': POSTGRES_SETTINGS['user'],
        'password': POSTGRES_SETTINGS['password'],
        'host': POSTGRES_SETTINGS['host'],
        'port': POSTGRES_SETTINGS['port'],
    }
    connection_pool: asyncpg.Pool = await asyncpg.create_pool(
        **connection_config,
        min_size=1,
        max_size=10,
    )
    return connection_pool

async def close_connection_pool(pool: asyncpg.Pool):
    await pool.close()
