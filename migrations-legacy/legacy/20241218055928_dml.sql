-- +goose Up
-- +goose StatementBegin

insert into
    clinic.speciality (name)
values
    ('Терапевт'),
    ('Кардиолог'),
    ('Врач УЗИ'),
    ('Нейрохирург');

insert into
    clinic.doctors (name, speciality, phone_number)
values
    ('Ибрагимов Далгат', 'Терапевт', '+79991234567'),
    ('Формалев Александр', 'Нейрохирург', '+19876543210');

insert into
    clinic.patients (name, phone_number, email, insurance_number)
values
    ('Рустамхан Рамалданов', '+79999999999', 'pepe@pepe.com', '123456789'),
    ('Халимов Исмаилджон', '+71234567890', 'pepe@pepe.ya.ru', '123456780');

insert into
    clinic.medicines (name)
values
    ('Аспирин'),
    ('Корвалол'),
    ('Аскорбиновая кислота');

insert into
    clinic.clinics (address, name, phone)
values
    ('Москва, ул. Маркса 5', 'Пепе-мед', '+79991201213');

with aspirin_id as (
    select id from clinic.medicines
    where name = 'Аспирин'
), pepe_clinic_id as (
    select id from clinic.clinics
    where name = 'Пепе-мед'
)
insert into
    clinic.medicine_stocks (clinic_id, medicine_id, amount, expiration_date)
values
    ( (select * from pepe_clinic_id), (select * from aspirin_id), 12, '2027-08-15' );

insert into
    clinic.patient_history (patient_id, doctor_recorded_id, type, description, record_time)
values
    (1, 1, 'diagnosis', 'Простуда. Надо кушать больше аскорбинок', '2022-10-19 10:12:00+03'),
    (2, 1, 'diagnosis', 'Ушиб', '2022-10-20 14:00:00+03'),
    (1, 2, 'recovery', 'Простуда', '2022-10-22 12:05:00+03'),
    (2, 1, 'test', 'Рентген. Результат - все в поряде ;)', '2022-10-21 12:00:00+03'),
    (2, 1, 'recovery', 'Ушиб', '2022-10-27 14:00:00+03');

-- +goose StatementEnd
