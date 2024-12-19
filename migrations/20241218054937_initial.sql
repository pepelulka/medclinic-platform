-- +goose Up
-- +goose StatementBegin

BEGIN;

CREATE SCHEMA IF NOT EXISTS clinic;

CREATE TABLE IF NOT EXISTS clinic.doctors
(
    id SERIAL NOT NULL,
    name character varying(120) NOT NULL,
    speciality character varying(40) NOT NULL,
    experience integer,
    email character varying(40),
    phone_number character varying(12) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS clinic.patients
(
    id SERIAL NOT NULL,
    name character varying(120) NOT NULL,
    phone_number character varying(12) NOT NULL,
    email character varying(50),
    insurance_number character varying(40) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS clinic.medicines
(
    id SERIAL NOT NULL,
    name character varying(120),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS clinic.appointments
(
    id SERIAL NOT NULL,
    "time" timestamp with time zone NOT NULL,
    patient_id integer NOT NULL,
    doctor_id integer NOT NULL,
    clinic_id integer NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS clinic.clinics
(
    id SERIAL NOT NULL,
    address character varying(120) NOT NULL,
    name character varying(120) NOT NULL,
    phone character varying(12) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS clinic.medicine_stocks
(
    id SERIAL NOT NULL,
    clinic_id integer NOT NULL,
    medicine_id integer NOT NULL,
    amount integer NOT NULL,
    expiration_date date NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS clinic.speciality
(
    name character varying(40) NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS clinic.patient_history
(
    id SERIAL NOT NULL,
    patient_id integer NOT NULL,
    doctor_recorded_id integer,
    type character varying(20) NOT NULL,
    description text NOT NULL,
    record_time timestamp with time zone NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS clinic.appointments_history
(
    appointment_id INT NOT NULL,
    time timestamp with time zone NOT NULL,
    event_type character varying(40) NOT NULL, -- either create or cancel

    PRIMARY KEY (appointment_id, event_type)
);

ALTER TABLE IF EXISTS clinic.doctors
    ADD CONSTRAINT speciality FOREIGN KEY (speciality)
    REFERENCES clinic.speciality (name) MATCH SIMPLE
    ON UPDATE RESTRICT
    ON DELETE RESTRICT
    NOT VALID;


ALTER TABLE IF EXISTS clinic.appointments
    ADD CONSTRAINT clinic FOREIGN KEY (clinic_id)
    REFERENCES clinic.clinics (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS clinic.appointments
    ADD CONSTRAINT patient FOREIGN KEY (patient_id)
    REFERENCES clinic.patients (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS clinic.appointments
    ADD CONSTRAINT doctor FOREIGN KEY (doctor_id)
    REFERENCES clinic.doctors (id) MATCH SIMPLE
    ON UPDATE SET NULL
    ON DELETE SET NULL
    NOT VALID;


ALTER TABLE IF EXISTS clinic.medicine_stocks
    ADD CONSTRAINT medicine FOREIGN KEY (medicine_id)
    REFERENCES clinic.medicines (id) MATCH SIMPLE
    ON UPDATE RESTRICT
    ON DELETE RESTRICT
    NOT VALID;


ALTER TABLE IF EXISTS clinic.medicine_stocks
    ADD CONSTRAINT clinic FOREIGN KEY (clinic_id)
    REFERENCES clinic.clinics (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS clinic.patient_history
    ADD CONSTRAINT patient FOREIGN KEY (patient_id)
    REFERENCES clinic.patients (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS clinic.patient_history
    ADD CONSTRAINT doctor_recorded FOREIGN KEY (doctor_recorded_id)
    REFERENCES clinic.doctors (id) MATCH SIMPLE
    ON UPDATE SET NULL
    ON DELETE SET NULL
    NOT VALID;

ALTER TABLE IF EXISTS clinic.appointments_history
    ADD CONSTRAINT appointment FOREIGN KEY (appointment_id)
    REFERENCES clinic.appointments (id) MATCH SIMPLE
    ON UPDATE RESTRICT
    ON DELETE RESTRICT;

END;

BEGIN;

CREATE TABLE IF NOT EXISTS clinic.user_credentials
(
    login character varying (120),
    password_hash character varying (255),
    patient_id integer,
    role character varying (40),
    PRIMARY KEY (login)
);

ALTER TABLE IF EXISTS clinic.user_credentials
    ADD CONSTRAINT patient FOREIGN KEY (patient_id)
    REFERENCES clinic.patients (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

DROP SCHEMA IF EXISTS clinic CASCADE;

-- +goose StatementEnd
