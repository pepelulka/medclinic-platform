import asyncpg

from typing import List

from models.user import User

class UserRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create(self, user: User):
        query = """
            INSERT INTO users
                (name, age)
            VALUES
                ($1, $2);
        """
        params = (user.name, user.age)
        async with self.pool.acquire() as conn:
            await conn.execute(query, *params)

    async def get_all(self) -> List[User]:
        query = """
            SELECT name, age
            FROM users;
        """
        async with self.pool.acquire() as conn:
            rows: List[asyncpg.Record] = await conn.fetch(query)
        result = [
            User(name=row[0], age=int(row[1]))
            for row in rows
        ]
        return result
