-- +goose Up
-- +goose StatementBegin

-- Создаем функцию триггер
CREATE OR REPLACE FUNCTION clinic.log_appointments_actions()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO clinic.appointments_history (appointment_id, time, event_type)
        VALUES (NEW.id, now(), 'create');
    END IF;
    RETURN NULL; -- Триггеры типа AFTER должны возвращать NULL
END;
$$ LANGUAGE plpgsql;

-- Навешиваем этот триггер
CREATE TRIGGER appointments_change_trigger
AFTER INSERT ON clinic.appointments
FOR EACH ROW
EXECUTE FUNCTION clinic.log_appointments_actions();

-- Была ли отменена запись
CREATE FUNCTION clinic.was_appointment_cancelled (_app_id INT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT
            1
        FROM
            clinic.appointments_history
        WHERE
            appointment_id = _app_id
                AND
            event_type = 'cancel'
    );
END
$$ LANGUAGE plpgsql;

CREATE VIEW clinic.future_uncancelled_appointments AS
    WITH cancelled_appointments_ids AS (
        SELECT
            appointment_id
        FROM
            clinic.appointments_history
        WHERE
            event_type = 'cancel'
    )
    SELECT *
    FROM
        clinic.appointments
    WHERE
        time > NOW()
            AND
        id not in (select * from cancelled_appointments_ids);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

DROP FUNCTION IF EXISTS clinic.log_appointments_actions CASCADE;
DROP FUNCTION IF EXISTS clinic.was_appointment_cancelled;
DROP VIEW IF EXISTS clinic.future_uncancelled_appointments;
DROP TABLE IF EXISTS clinic.appointments_history;

-- +goose StatementEnd
