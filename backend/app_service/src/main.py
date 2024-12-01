import asyncio

from db import postgres
from repositories.user import UserRepository
from models.user import User

async def async_main():
    conn_pool = await postgres.create_connection_pool()

    user_repo = UserRepository(conn_pool)

    await user_repo.create(
        User(name='Pepe', age=19)
    )
    await user_repo.create(
        User(name='Vika', age=20)
    )
    print(await user_repo.get_all())

    await postgres.close_connection_pool(conn_pool)

if __name__ == '__main__':
    asyncio.run(async_main())

    print('Going into infinite loop...')
    while True:
        pass
