-- +goose Up
-- +goose StatementBegin

BEGIN;

CREATE SCHEMA IF NOT EXISTS clinic;

CREATE TABLE IF NOT EXISTS clinic.specialities
(
    name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS clinic.doctors
(
    doctor_id SERIAL PRIMARY KEY,
    name character varying(255) NOT NULL,
    email character varying(128) NOT NULL,
    phone_number character varying(12) NOT NULL
);

CREATE TABLE IF NOT EXISTS clinic.doctor_specialities_map
(
    doctor_id integer,
    speciality varchar(255),
    CONSTRAINT fk_doctor_id FOREIGN KEY (doctor_id) REFERENCES clinic.doctors (doctor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY (doctor_id, speciality)
);

CREATE TABLE IF NOT EXISTS clinic.patients
(
    patient_id SERIAL PRIMARY KEY,
    name varchar(255) NOT NULL,
    phone_number varchar(12) NOT NULL,
    email varchar(128),
    birth_date date
);

CREATE TABLE IF NOT EXISTS clinic.clinics
(
    clinic_id SERIAL PRIMARY KEY,
    address varchar(255) NOT NULL,
    name character varying(255),
    phone_number character varying(12) NOT NULL
);


CREATE TABLE IF NOT EXISTS clinic.slots
(
    doctor_id integer NOT NULL,
    start_time time NOT NULL,
    clinic_id integer NOT NULL,
    PRIMARY KEY (doctor_id, start_time),
    CONSTRAINT fk_doctor_id FOREIGN KEY (doctor_id) REFERENCES clinic.doctors (doctor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_clinic_id FOREIGN KEY (clinic_id) REFERENCES clinic.clinics (clinic_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS clinic.appointments
(
    doctor_id integer NOT NULL,
    start_time time NOT NULL,
    patient_id integer NOT NULL,
    clinic_id integer NOT NULL,
    PRIMARY KEY (doctor_id, start_time),
    CONSTRAINT fk_doctor_id FOREIGN KEY (doctor_id) REFERENCES clinic.doctors (doctor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_clinic_id FOREIGN KEY (clinic_id) REFERENCES clinic.clinics (clinic_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_patient_id FOREIGN KEY (patient_id) REFERENCES clinic.patients (patient_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS clinic.history
(
    record_id SERIAL PRIMARY KEY,
    record_time timestamp NOT NULL,
    doctor_id integer NOT NULL,
    patient_id integer NOT NULL,
    title varchar(255) NOT NULL,
    description text,
    CONSTRAINT fk_doctor_id FOREIGN KEY (doctor_id) REFERENCES clinic.doctors (doctor_id)
        ON DELETE SET NULL
        ON UPDATE SET NULL,
    CONSTRAINT fk_patient_id FOREIGN KEY (patient_id) REFERENCES clinic.patients (patient_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS clinic.history_records_s3_files
(
    record_id integer NOT NULL,
    s3_path varchar(255) NOT NULL,
    PRIMARY KEY (record_id, s3_path),
    CONSTRAINT fk_record_id FOREIGN KEY (record_id) REFERENCES clinic.history (record_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

END;

BEGIN;

CREATE TABLE IF NOT EXISTS clinic.user_credentials
(
    login character varying (128) PRIMARY KEY,
    password_hash character varying (255) NOT NULL,
    role character varying (40) NOT NULL,
    doctor_id integer,
    patient_id integer,
    CONSTRAINT fk_doctor_id FOREIGN KEY (doctor_id) REFERENCES clinic.doctors (doctor_id)
        ON DELETE SET NULL
        ON UPDATE SET NULL,
    CONSTRAINT fk_patient_id FOREIGN KEY (patient_id) REFERENCES clinic.patients (patient_id)
        ON DELETE SET NULL
        ON UPDATE SET NULL
);

END;

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

DROP SCHEMA IF EXISTS clinic CASCADE;

-- +goose StatementEnd
