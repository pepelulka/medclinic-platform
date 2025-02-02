from domain.doctor import Speciality
import asyncpg

from db.postgres import make_query_and_convert

class DoctorRepository:
    speciality_convert_function = lambda _, row: Speciality(name=row[0])

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_all_specialities(self):
        query = """
            SELECT name
            from clinic.specialities;
            """
        return await make_query_and_convert(
            self.pool,
            query,
            self.speciality_convert_function
        )

    async def create_speciality(self, speciality: Speciality) -> int | None:
        query = """
            INSERT INTO
                clinic.specialities (name)
            VALUES
                ($1);
        """
        conv_function = lambda row : int(row[0])
        return await make_query_and_convert(
            self.pool,
            query,
            conv_function,
            [speciality.name],
            expect_list=False
        )
