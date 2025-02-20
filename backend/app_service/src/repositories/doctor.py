from domain.doctor import Speciality, DoctorCreate, DoctorCreateResult
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

    async def create_doctor(self, doctor: DoctorCreate) -> DoctorCreateResult:
        # Step 1. Checking for specialities to exist
        query_all_specialities = """
            SELECT 
                name
            FROM
                clinic.specialities;
        """
        all_specialities = await make_query_and_convert(
            self.pool,
            query_all_specialities,
            lambda row : row[0],
            expect_list=True
        )
        absent_specialities = []
        for speciality in doctor.specialities:
            if speciality.name not in all_specialities:
                absent_specialities.append(speciality.name)
        if absent_specialities:
            raise Exception(f"Specialities don't exist: {', '.join(absent_specialities)}")

        # Step 2. Adding doctor and specialities mapping in the one transaction
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                doctor_id = await conn.fetchval(
                    "INSERT INTO clinic.doctors (name, email, phone_number) VALUES ($1, $2, $3) RETURNING doctor_id;",
                    doctor.name,
                    doctor.email,
                    doctor.phone_number
                )

                doctor_specialities_map_entries = [
                    (doctor_id, speciality.name) for speciality in doctor.specialities
                ]

                await conn.executemany(
                    "INSERT INTO clinic.doctor_specialities_map VALUES ($1, $2);",
                    doctor_specialities_map_entries
                )

        return DoctorCreateResult(doctor_id=doctor_id)
