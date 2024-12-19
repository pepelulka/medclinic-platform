import asyncpg

from auth.models import PatientUserCreate, UserLogin, UserInfo
from db.postgres import make_query
from auth.auth import hash_password, check_password

class UserCredentialsRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create_patient(self, patient: PatientUserCreate):
        query = """
        INSERT INTO
            clinic.user_credentials (login, password_hash, patient_id, role) 
        VALUES
            ($1, $2, $3, 'patient');
        """
        await make_query(
            self.pool,
            query,
            [patient.login, hash_password(patient.password), patient.patient_id]
        )

    async def create_admin(self, credentials: UserLogin):
        query = """
                INSERT INTO
                    clinic.user_credentials (login, password_hash, role) 
                VALUES
                    ($1, $2, 'admin');
                """
        await make_query(
            self.pool,
            query,
            [credentials.login, hash_password(credentials.password)]
        )

    # Returns None if there's no such user or invalid login/password pair
    async def check_user(self, user: UserLogin) -> UserInfo | None:
        query = """
        SELECT
            login, password_hash, patient_id, role 
        FROM
            clinic.user_credentials
        WHERE
            login = $1;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, user.login)
        if len(rows) == 0:
            return None
        row = rows[0]
        password_hash = row[1]
        if not check_password(user.password, password_hash):
            return None
        return UserInfo(
            login = user.login,
            role = row[3],
            patient_id = None if row[2] is None else int(row[2])
        )
