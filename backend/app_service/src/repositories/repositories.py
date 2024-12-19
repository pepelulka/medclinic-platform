import asyncpg

from typing import List

from domain.models import (
    Clinic,
    Doctor, DoctorCreate,
    Patient, PatientCreate,
    Speciality, PatientHistoryEventPreview,
    AppointmentPreview, AppointmentCreate,
    AppointmentLogPreview
)

from db.postgres import make_query, make_query_and_convert

class ClinicRepository:
    convert_function = lambda _, row: Clinic(id=int(row[0]), address=row[1], name=row[2], phone=row[3])

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_all(self) -> List[Clinic]:
        query = """
            SELECT id, address, name, phone
            FROM clinic.clinics;
        """
        return await make_query_and_convert(
            self.pool,
            query,
            self.convert_function
        )

    async def get(self, clinic_id) -> Clinic | None:
        query = """
            SELECT id, address, name, phone
            FROM clinic.clinics
            WHERE id = $1;
        """
        return await make_query_and_convert(
            self.pool,
            query,
            self.convert_function,
            query_params=(clinic_id),
            expect_list=False
        )

class DoctorRepository:
    convert_function = lambda _, row: Doctor(
        id=int(row[0]),
        name=row[1],
        speciality=Speciality(name=row[2]),
        experience=None if row[3] is None else int(row[3]),
        email=row[4],
        phone_number=row[5]
    )

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_all(self):
        query = """
        SELECT id, name, speciality, experience, email, phone_number
        from clinic.doctors;
        """
        return await make_query_and_convert(
            self.pool,
            query,
            self.convert_function
        )

    async def get(self, doctor_id):
        query = """
        SELECT id, name, speciality, experience, email, phone_number
        from clinic.doctors
        WHERE id = $1;
        """
        return await make_query_and_convert(
            self.pool,
            query,
            self.convert_function,
            (doctor_id),
            expect_list=False
        )

    async def get_all_specialities(self):
        query = """
        SELECT
            name
        FROM 
            clinic.speciality
        ORDER BY
            name;
        """
        conv_function = lambda row : Speciality(name=row[0])
        return await make_query_and_convert(
            self.pool,
            query,
            conv_function
        )

    async def create(self, doctor: DoctorCreate):
        query = """
        INSERT INTO
            clinic.doctors (name, speciality, experience, email, phone_number)
        VALUES
            ($1, $2, $3, $4, $5);
        """
        await make_query(
            self.pool,
            query,
            [doctor.name, doctor.speciality, doctor.experience, doctor.email, doctor.phone_number]
        )

class PatientRepository:
    convert_function = lambda _, row: Patient(
        id=int(row[0]),
        name=row[1],
        phone_number=row[2],
        email=row[3],
        insurance_number=row[4]
    )

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_all(self):
        query = """
            SELECT id, name, phone_number, email, insurance_number
            from clinic.patients;
            """
        return await make_query_and_convert(
            self.pool,
            query,
            self.convert_function
        )

    async def get(self, patient_id):
        query = """
            SELECT id, name, phone_number, email, insurance_number
            from clinic.patients
            WHERE id = $1;
            """
        return await make_query_and_convert(
            self.pool,
            query,
            self.convert_function,
            (patient_id),
            expect_list=False
        )

    async def update(self, patient_id: int, patient: PatientCreate):
        query = """
            UPDATE clinic.patients
            SET name = $1, phone_number = $2, email = $3, insurance_number = $4
            WHERE id = $5;
        """
        return await make_query(
            self.pool,
            query,
            [patient.name, patient.phone_number, patient.email, patient.insurance_number, patient_id]
        )

    async def create(self, patient: PatientCreate) -> int | None:
        query = """
            INSERT INTO
                clinic.patients (name, phone_number, email, insurance_number)
            VALUES
                ($1, $2, $3, $4)
            RETURNING 
                id;
        """
        conv_function = lambda row : int(row[0])
        return await make_query_and_convert(
            self.pool,
            query,
            conv_function,
            [patient.name, patient.phone_number, patient.email, patient.insurance_number],
            expect_list=False
        )

class PatientHistoryRepository:
    convert_function = lambda _, row: PatientHistoryEventPreview(
        doctor_name=row[0],
        type=row[1],
        description=row[2],
        record_time=row[3]
    )

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    def get_history_preview(self, patient_id: int):
        query = """
            SELECT docs.name, events.type, events.description, events.record_time
            FROM clinic.patient_history as events
                LEFT JOIN clinic.doctors as docs
                ON events.doctor_recorded_id = docs.id
            WHERE events.patient_id = $1
            ORDER BY events.record_time;
        """
        return make_query_and_convert(
            self.pool,
            query,
            self.convert_function,
            [patient_id]
        )

class AppointmentRepository:
    convert_function = lambda _, row: AppointmentPreview(
        id=int(row[0]),
        time=row[1],
        doctor_name=row[2],
        clinic_address=row[3]
    )

    def __init__(self, pool):
        self.pool = pool

    async def patient_id_from_appointment_id(self, appointment_id) -> int | None:
        query = """
        SELECT 
            patient_id
        FROM
            clinic.appointments
        WHERE
            id = $1
        LIMIT 1;
        """

        conv_function = lambda x : int(x[0])
        return await make_query_and_convert(
            self.pool,
            query,
            conv_function,
            [appointment_id],
            expect_list=False
        )

    async def delete(self, appointment_id):
        query = """
        DELETE FROM 
            clinic.appointments
        WHERE
            id = $1;
        """
        return await make_query(
            self.pool,
            query,
            [appointment_id]
        )

    # We want this operation to be idempotent, so if we already cancelled this appointment
    # or there is no such appointment we just ignore it
    async def cancel(self, appointment_id):
        test_query = """
        SELECT
            1
        FROM
            clinic.appointments
        WHERE
            id = $1
                AND
            NOT clinic.was_appointment_cancelled($1); 
        """
        test_result = await make_query_and_convert(
            self.pool,
            test_query,
            lambda row : row[0],
            [appointment_id],
            expect_list=False
        )
        if test_result is None:
            return None # There's no such appointment or appointment was already cancelled
        query = """
        INSERT INTO
            clinic.appointments_history (appointment_id, event_type, time)
        VALUES
            ($1, 'cancel', NOW());
        """
        await make_query(
            self.pool,
            query,
            [appointment_id]
        )


    async def get_all_relevant_by_user(self, patient_id) -> List[AppointmentPreview]:
        query = """
        SELECT
            a.id as id,
            a.time as time,
            d.name as doctor_name,
            c.address as clinic_address
        FROM
            clinic.future_uncancelled_appointments as a
            LEFT JOIN clinic.doctors as d
                ON a.doctor_id = d.id
            LEFT JOIN clinic.clinics as c
                ON a.clinic_id = c.id
        WHERE
            a.patient_id = $1
        ORDER BY
            a.time;
        """
        return await make_query_and_convert(
            self.pool,
            query,
            self.convert_function,
            [patient_id]
        )

    async def create(self, appointment: AppointmentCreate):
        query = """
        INSERT INTO 
            clinic.appointments (
                patient_id,
                doctor_id,
                clinic_id,
                time
            )
        VALUES
            ($1, $2, $3, $4);
        """
        await make_query(
            self.pool,
            query,
            [
                appointment.patient_id,
                appointment.doctor_id,
                appointment.clinic_id,
                appointment.time
            ]
        )

class AppointmentHistoryRepository:
    convert_function = lambda _, row: AppointmentLogPreview(
        patient_id=int(row[0]),
        patient_name=row[1],
        appointment_id=int(row[2]),
        appointment_time=row[3],
        event_time=row[4],
        doctor_id=int(row[5]),
        doctor_name=row[6],
        clinic_address=row[7],
        event_type=row[8]
    )

    def __init__(self, pool):
        self.pool = pool

    async def get_count(self):
        query = """
        SELECT count(*)
        FROM clinic.appointments_history;
        """
        return await make_query_and_convert(
            self.pool,
            query,
            lambda row: int(row[0]),
            [],
            expect_list=False
        )

    async def get_window(self, skip=0, limit=10):
        query = """
        SELECT
            a.patient_id,
            p.name,
            al.appointment_id,
            a.time,
            al.time,
            a.doctor_id,
            d.name,
            c.address,
            al.event_type
        FROM clinic.appointments_history as al
            LEFT JOIN
                clinic.appointments as a
                    ON al.appointment_id = a.id
            LEFT JOIN
                clinic.patients as p
                    ON a.patient_id = p.id
            LEFT JOIN
                clinic.doctors as d
                    ON a.doctor_id = d.id
            LEFT JOIN
                clinic.clinics as c
                    ON a.clinic_id = c.id
        ORDER BY a.time DESC
        OFFSET $1 
        LIMIT $2;
        """
        return await make_query_and_convert(
            self.pool,
            query,
            self.convert_function,
            [skip, limit]
        )
