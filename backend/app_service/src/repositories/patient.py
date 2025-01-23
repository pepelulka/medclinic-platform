from domain.patient import Patient, PatientCreate
import asyncpg

from typing import List

from db.postgres import make_query, make_query_and_convert

class PatientRepository:
    convert_function = lambda _, row: Patient(
        patient_id=row[0],
        name=row[1],
        phone_number=row[2],
        email=row[3],
        birth_date=row[4]
    )

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_all(self):
        query = """
            SELECT patient_id, name, phone_number, email, birth_date
            from clinic.patients;
            """
        return await make_query_and_convert(
            self.pool,
            query,
            self.convert_function
        )

    async def get(self, patient_id):
        query = """
            SELECT patient_id, name, phone_number, email, birth_date
            from clinic.patients
            WHERE patient_id = $1;
            """
        return await make_query_and_convert(
            self.pool,
            query,
            self.convert_function,
            [patient_id],
            expect_list=False
        )

    async def update(self, patient_id: int, patient: PatientCreate):
        query = """
            UPDATE clinic.patients
            SET name = $1, phone_number = $2, email = $3, birth_date = $4
            WHERE patient_id = $5;
        """
        return await make_query(
            self.pool,
            query,
            (patient.name, patient.phone_number, patient.email, patient.birth_date, patient_id)
        )

    async def create(self, patient: PatientCreate) -> int | None:
        query = """
            INSERT INTO
                clinic.patients (name, phone_number, email, birth_date)
            VALUES
                ($1, $2, $3, $4)
            RETURNING 
                patient_id;
        """
        conv_function = lambda row : int(row[0])
        return await make_query_and_convert(
            self.pool,
            query,
            conv_function,
            [patient.name, patient.phone_number, patient.email, patient.birth_date],
            expect_list=False
        )
