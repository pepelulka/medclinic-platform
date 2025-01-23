package models

import _ "encoding/json"

type UserLogin struct {
	Login    string `json:"login"`
	Password string `json:"password"`
}

type UserInfo struct {
	Login     string `json:"login"`
	Role      string `json:"role"`
	PatientId int    `json:"patient_id"`
	DoctorId  int    `json:"doctor_id"`
}

type PatientCreate struct {
	Credentials UserLogin `json:"credentials"`
	PatientId   int       `json:"patient_id"`
}

type DoctorCreate struct {
	Credentials UserLogin `json:"credentials"`
	DoctorId    int       `json:"doctor_id"`
}

type AdminCreate struct {
	Credentials UserLogin `json:"credentials"`
}

// Structs for db insertion:

type PatientCreateHashed struct {
	Login        string
	PasswordHash string
	PatientId    int
}

type DoctorCreateHashed struct {
	Login        string
	PasswordHash string
	DoctorId     int
}

type AdminCreateHashed struct {
	Login        string
	PasswordHash string
}
