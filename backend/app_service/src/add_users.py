import asyncio

from auth.db import UserCredentialsRepository
from auth.models import PatientUserCreate, UserLogin
from db.postgres import create_connection_pool, close_connection_pool


# Скрипт для создания пользователей в БД
async def amain():
    pool = await create_connection_pool()
    repo = UserCredentialsRepository(pool)

    admin = UserLogin(
        login='admin',
        password='admin',
    )

    pepelulka = PatientUserCreate(
        login='pepelulka',
        password='123456',
        patient_id=1
    )

    await repo.create_admin(admin)
    await repo.create_patient(pepelulka)

    await close_connection_pool(pool)

asyncio.run(amain())
