from typing import List
import asyncpg

from settings import POSTGRES_SETTINGS, DB_POOL_MAX_CONNECTIONS, DB_POOL_MIN_CONNECTIONS

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
        min_size=DB_POOL_MIN_CONNECTIONS,
        max_size=DB_POOL_MAX_CONNECTIONS,
    )
    return connection_pool

async def close_connection_pool(pool: asyncpg.Pool):
    await pool.close()

# Функции для сокращения шаблонного кода:

# Делает запрос, применяет к каждой строке функцию convert_function и возвращает список значений
# Если указан expect_list=False, возвращает первый объект, либо None, если бд ничего не вернула.
async def make_query_and_convert(pool, query_text, convert_function, query_params=(), expect_list=True):
    async with pool.acquire() as conn:
        rows: List[asyncpg.Record] = await conn.fetch(query_text, *query_params)
    if expect_list:
        result = [
            convert_function(row) for row in rows
        ]
        return result
    if len(rows) == 0:
        return None
    return convert_function(rows[0])

# Просто делает запрос
async def make_query(pool, query_text, query_params=()):
    async with pool.acquire() as conn:
        await conn.execute(query_text, *query_params)
