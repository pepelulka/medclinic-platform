package db

import (
	"auth_service/config"
	"auth_service/internal/models"
	"database/sql"
	"fmt"

	_ "github.com/lib/pq"
)

type UserRepository struct {
	DB *sql.DB
}

func CreateUserRepository(config config.Config) (UserRepository, error) {
	connStr := fmt.Sprintf(
		"postgres://%s:%s@%s:%d/%s?sslmode=disable",
		config.Database.User,
		config.Database.Password,
		config.Database.Host,
		config.Database.Port,
		config.Database.DbName,
	)

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return UserRepository{}, err
	}
	return UserRepository{
		DB: db,
	}, nil
}

func (repo *UserRepository) Close() error {
	return repo.DB.Close()
}

func (repo *UserRepository) GetInfoByLogin(login string) (models.UserInfo, error) {
	var info models.UserInfo

	row := repo.DB.QueryRow(
		"SELECT login, role, COALESCE(patient_id, 0), COALESCE(doctor_id, 0) "+
			"FROM clinic.user_credentials "+
			"WHERE login = $1;",
		login,
	)
	if err := row.Scan(&info.Login, &info.Role, &info.PatientId, &info.DoctorId); err != nil {
		return models.UserInfo{}, err
	}
	return info, nil
}

func (repo *UserRepository) GetPasswordHashByLogin(login string) (string, error) {
	var passwordHash string

	row := repo.DB.QueryRow(
		"SELECT password_hash "+
			"FROM clinic.user_credentials "+
			"WHERE login = $1;",
		login,
	)
	if err := row.Scan(&passwordHash); err != nil {
		return "", err
	}
	return passwordHash, nil
}

func (repo *UserRepository) CreateAdmin(user models.AdminCreateHashed) error {
	_, err := repo.DB.Exec(
		`
INSERT INTO clinic.user_credentials (login, password_hash, role, patient_id, doctor_id)
VALUES ($1, $2, 'admin', NULL, NULL);
		`,
		user.Login,
		user.PasswordHash,
	)
	return err
}

func (repo *UserRepository) CreatePatient(patient models.PatientCreateHashed) error {
	_, err := repo.DB.Exec(
		`
INSERT INTO clinic.user_credentials (login, password_hash, role, patient_id, doctor_id)
VALUES ($1, $2, 'patient', $3, NULL);
		`,
		patient.Login,
		patient.PasswordHash,
		patient.PatientId,
	)
	return err
}

func (repo *UserRepository) CreateDoctor(patient models.DoctorCreateHashed) error {
	_, err := repo.DB.Exec(
		`
INSERT INTO clinic.user_credentials (login, password_hash, role, patient_id, doctor_id)
VALUES ($1, $2, 'doctor', NULL, $3);
		`,
		patient.Login,
		patient.PasswordHash,
		patient.DoctorId,
	)
	return err
}
